#!/usr/bin/env python3
"""Forest semantic index builder.

Walks a configured Forest vault root, chunks markdown-family files by heading
(~1000 characters, 100 character overlap), embeds chunks locally via Ollama
nomic-embed-text (768-dimensional), and stores vectors, text, path, and mtime
in a sqlite-vec database.

Usage:
  python3 forest_index.py --doctor        # preflight check (dependencies, Ollama, disk space)
  python3 forest_index.py --incremental   # only embed new/changed files (mtime compare)
  python3 forest_index.py --full          # wipe and rebuild index from scratch

Governance: Doc-414 compliant (Zero em dashes, strict claims discipline).
"""
import argparse
import json
import os
import shutil
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
import numpy as np
import sqlite_vec
from sqlite_vec import serialize_float32

DEFAULT_VAULT_ROOT = str(Path.home() / "Myceliate_Master")
VAULT_ROOT = os.environ.get("FOREST_VAULT_ROOT", DEFAULT_VAULT_ROOT)
DEFAULT_DB_PATH = os.path.join(VAULT_ROOT, "UNDERSTORY", "SYSTEM", "forest-index", "forest_index.db")
DB_PATH = os.environ.get("FOREST_INDEX_DB", DEFAULT_DB_PATH)
DEFAULT_LOG_PATH = os.path.join(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", "build.log")
LOG_PATH = os.environ.get("FOREST_INDEX_LOG", DEFAULT_LOG_PATH)

MODEL = os.environ.get("OLLAMA_MODEL", "nomic-embed-text:latest")
EMBED_DIM = 768
OLLAMA_URL = os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434/api/embed")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
MAX_FILE_BYTES = 5 * 1024 * 1024   # skip files larger than 5 MB
BATCH = 4

SKIP_DIRS = {
    "node_modules", ".venv", "venv", ".git", ".obsidian",
    "BACKUPS", "LEGACY_QUARANTINE", "SEED_BANK_LEGACY",
}
SKIP_TOPLEVEL = {"BACKUPS", "LEGACY_QUARANTINE", "SEED_BANK_LEGACY"}
EXTS = {".md", ".markdown", ".txt", ".jsonld"}


def log(msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        log_dir = os.path.dirname(LOG_PATH)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def iter_files(root: str):
    """Walk vault root and yield eligible markdown/text files."""
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        parts = rel.split(os.sep)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if parts[0] in SKIP_TOPLEVEL:
            dirnames[:] = []
            continue
        for name in filenames:
            if os.path.splitext(name)[1].lower() in EXTS:
                yield os.path.join(dirpath, name)


def split_long(text: str):
    """Fixed-size window split for text without headings."""
    if len(text) <= CHUNK_SIZE:
        return [text] if text.strip() else []
    out = []
    step = CHUNK_SIZE - CHUNK_OVERLAP
    for i in range(0, len(text), step):
        piece = text[i:i + CHUNK_SIZE]
        if piece.strip():
            out.append(piece)
        if i + CHUNK_SIZE >= len(text):
            break
    return out


def chunk_by_heading(text: str):
    """Split markdown text into sections by ATX headings, then window long sections."""
    lines = text.splitlines()
    sections = []
    cur_h, cur = "", []
    for line in lines:
        if line.lstrip().startswith("#"):
            if cur or cur_h:
                sections.append((cur_h, "\n".join(cur)))
            cur_h, cur = line.lstrip().lstrip("#").strip(), [line]
        else:
            cur.append(line)
    if cur or cur_h:
        sections.append((cur_h, "\n".join(cur)))

    chunks = []
    for heading, body in sections:
        body = body.strip()
        if not body:
            continue
        if len(body) <= CHUNK_SIZE:
            pieces = [body]
        else:
            pieces = split_long(body)
        for piece in pieces:
            h = heading[:200]
            content = f"{h}\n{piece}" if h and piece != body else piece
            if not h and piece == body:
                content = piece
            chunks.append({"heading": h, "text": content})
    return chunks


def chunk_file(path: str):
    try:
        if os.path.getsize(path) > MAX_FILE_BYTES:
            return []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return []
    if not text.strip():
        return []
    is_md = path.lower().endswith((".md", ".markdown"))
    if is_md and any(line.lstrip().startswith("#") for line in text.splitlines()):
        return chunk_by_heading(text)
    return [{"heading": "", "text": c} for c in split_long(text)]


def embed_batch(texts: list) -> np.ndarray:
    """Send text batch to local Ollama embedding endpoint with exponential backoff."""
    payload = json.dumps({
        "model": MODEL,
        "input": texts,
    }).encode("utf-8")
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                OLLAMA_URL,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read())
            vecs = data.get("embeddings") or data.get("embedding")
            if vecs and isinstance(vecs[0], list):
                return np.asarray(vecs, dtype=np.float32)
            return np.asarray([vecs], dtype=np.float32)
        except Exception as e:
            if attempt == 3:
                raise
            log(f"Embed retry ({attempt + 1}/3) after error: {e}")
            time.sleep(2 * (attempt + 1))


def open_db(db_path: str):
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    return db


def init_db(db: sqlite3.Connection):
    db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            mtime REAL NOT NULL,
            size INTEGER NOT NULL,
            n_chunks INTEGER NOT NULL
        )""")
    db.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            file_path TEXT NOT NULL,
            heading TEXT NOT NULL,
            ord INTEGER NOT NULL,
            text TEXT NOT NULL
        )""")
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
            chunk_id INTEGER PRIMARY KEY,
            embedding FLOAT[768]
        )""")
    db.commit()


def run_doctor(root: str, db_path: str) -> bool:
    """Preflight diagnostic: verify Ollama, disk space, and root accessibility."""
    print("=== Forest Index Preflight Doctor ===")
    all_ok = True

    # 1. Check Root Directory
    print(f"Checking vault root: {root}")
    if os.path.isdir(root):
        file_count = sum(1 for _ in iter_files(root))
        print(f"  [OK] Vault root accessible ({file_count} indexable markdown/text files found)")
    else:
        print(f"  [FAIL] Vault root directory does not exist: {root}")
        all_ok = False

    # 2. Check Disk Headroom
    db_dir = os.path.dirname(os.path.abspath(db_path))
    os.makedirs(db_dir, exist_ok=True)
    free_bytes = shutil.disk_usage(db_dir).free
    free_gb = free_bytes / (1024 ** 3)
    print(f"Checking disk headroom at {db_dir}:")
    if free_gb < 2.0:
        print(f"  [WARN] Free disk space is low: {free_gb:.2f} GB available (recommend at least 2.0 GB)")
    else:
        print(f"  [OK] Sufficient disk space: {free_gb:.2f} GB available")

    # 3. Check Ollama Connectivity and Model
    print(f"Checking Ollama endpoint ({OLLAMA_URL}):")
    try:
        test_payload = json.dumps({"model": MODEL, "input": ["test ping"]}).encode("utf-8")
        req = urllib.request.Request(OLLAMA_URL, data=test_payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if "embeddings" in data or "embedding" in data:
                print(f"  [OK] Ollama reachable and model '{MODEL}' embedded test string successfully")
            else:
                print(f"  [FAIL] Ollama responded without embedding data: {data}")
                all_ok = False
    except Exception as e:
        print(f"  [FAIL] Could not embed test string via Ollama: {e}")
        print(f"         Ensure Ollama is running and run: ollama pull {MODEL}")
        all_ok = False

    # 4. Check sqlite-vec extension
    print("Checking sqlite-vec extension:")
    try:
        test_db = sqlite3.connect(":memory:")
        test_db.enable_load_extension(True)
        sqlite_vec.load(test_db)
        test_db.enable_load_extension(False)
        print("  [OK] sqlite-vec loaded into SQLite in-memory database")
    except Exception as e:
        print(f"  [FAIL] sqlite-vec extension loading failed: {e}")
        all_ok = False

    if all_ok:
        print("\nAll preflight checks passed. Indexer is ready.")
    else:
        print("\nPreflight checks failed. Please resolve the errors above.")
    return all_ok


def main():
    ap = argparse.ArgumentParser(description="Forest semantic indexer")
    ap.add_argument("--doctor", action="store_true", help="Run preflight diagnostics and exit")
    ap.add_argument("--incremental", action="store_true", help="Skip files already indexed (mtime compare)")
    ap.add_argument("--full", action="store_true", help="Wipe and rebuild index from scratch")
    ap.add_argument("--root", default=VAULT_ROOT, help=f"Vault root directory (default: {VAULT_ROOT})")
    ap.add_argument("--db", default=DB_PATH, help=f"Database file path (default: {DB_PATH})")
    ap.add_argument("--batch", type=int, default=BATCH, help="Embedding batch size (default: 4)")
    args = ap.parse_args()

    if args.doctor:
        sys.exit(0 if run_doctor(args.root, args.db) else 1)

    fresh = not os.path.exists(args.db)
    db = open_db(args.db)
    init_db(db)

    if fresh or args.full:
        if not fresh:
            log("Full rebuild requested: clearing existing index tables")
            db.executescript("DELETE FROM chunks; DELETE FROM vec_chunks; DELETE FROM files;")
            db.commit()

    known = dict(db.execute("SELECT path, mtime FROM files"))
    all_files = list(iter_files(args.root))
    todo, skipped = [], 0
    for p in all_files:
        try:
            st = os.stat(p)
        except OSError:
            continue
        prev = known.get(p)
        if prev is not None and abs(prev - st.st_mtime) < 1e-6:
            skipped += 1
            continue
        todo.append(p)

    mode = "incremental" if args.incremental else "full"
    log(f"{mode}: {len(all_files)} files found, {skipped} unchanged, {len(todo)} to index")

    # Clean removed files
    removed = set(known) - set(all_files)
    if removed:
        for p in removed:
            db.execute("DELETE FROM vec_chunks WHERE chunk_id IN (SELECT id FROM chunks WHERE file_path=?)", (p,))
            db.execute("DELETE FROM chunks WHERE file_path=?", (p,))
            db.execute("DELETE FROM files WHERE path=?", (p,))
        db.commit()
        log(f"Removed {len(removed)} deleted files from index")

    t0 = time.time()
    n_files = n_chunks = 0
    texts, metas = [], []

    def flush():
        nonlocal n_files, n_chunks
        if not texts:
            return
        vecs = embed_batch(texts)
        ids = []
        for (fp, heading, ordn, chunk_text) in metas:
            cur = db.execute(
                "INSERT INTO chunks(file_path, heading, ord, text) VALUES(?,?,?,?)",
                (fp, heading, ordn, chunk_text)
            )
            ids.append(cur.lastrowid)
        db.executemany(
            "INSERT INTO vec_chunks(chunk_id, embedding) VALUES(?,?)",
            [(cid, serialize_float32(v)) for cid, v in zip(ids, vecs)]
        )
        db.commit()
        n_chunks += len(metas)
        texts.clear()
        metas.clear()

    current_file = None
    for i, p in enumerate(sorted(todo)):
        try:
            st = os.stat(p)
        except OSError:
            continue
        chunks = chunk_file(p)
        if current_file is not None and current_file != p:
            flush()
        current_file = p
        if not chunks:
            db.execute("INSERT OR REPLACE INTO files(path,mtime,size,n_chunks) VALUES(?,?,?,0)",
                       (p, st.st_mtime, st.st_size))
            db.commit()
            n_files += 1
            continue
        for ordn, c in enumerate(chunks):
            texts.append(f"search_document: {c['text']}")
            metas.append((p, c["heading"], ordn, c["text"]))
        db.execute("INSERT OR REPLACE INTO files(path,mtime,size,n_chunks) VALUES(?,?,?,?)",
                   (p, st.st_mtime, st.st_size, len(chunks)))
        n_files += 1
        if len(texts) >= args.batch:
            flush()
        if (i + 1) % 500 == 0:
            el = time.time() - t0
            log(f"Progress {i+1}/{len(todo)} files, {n_chunks} chunks, {el:.0f}s elapsed")
    flush()

    db.commit()
    db.close()
    db_size = os.path.getsize(args.db) / (1024 * 1024)
    log(f"DONE {mode}: files indexed {n_files}, chunks {n_chunks}, db {db_size:.1f} MB, wall {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
