#!/usr/bin/env python3
"""Forest semantic query tool: top-k chunks from forest_index.db.

Usage:
  python3 forest_query.py 'ISA cert number' [-k 5]

Returns: file path, heading, score (cosine, higher is better), 200-char snippet.
Governance: Doc-414 compliant (Zero em dashes, strict claims discipline).
"""
import argparse
import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path
import numpy as np
import sqlite_vec

DEFAULT_VAULT_ROOT = str(Path.home() / "Myceliate_Master")
VAULT_ROOT = os.environ.get("FOREST_VAULT_ROOT", DEFAULT_VAULT_ROOT)
DEFAULT_DB_PATH = os.path.join(VAULT_ROOT, "UNDERSTORY", "SYSTEM", "forest-index", "forest_index.db")
DB_PATH = os.environ.get("FOREST_INDEX_DB", DEFAULT_DB_PATH)
OLLAMA_URL = os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434/api/embed")
MODEL = os.environ.get("OLLAMA_MODEL", "nomic-embed-text:latest")


def embed_query(text: str) -> np.ndarray:
    """Generate query embedding from local Ollama endpoint."""
    payload = json.dumps({"model": MODEL, "input": [f"search_query: {text}"]}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        vecs = data.get("embeddings") or [data["embedding"]]
        return np.asarray(vecs, dtype=np.float32)[0]
    except urllib.error.URLError as e:
        sys.exit(f"Error: Could not reach Ollama at {OLLAMA_URL}: {e.reason}")
    except Exception as e:
        sys.exit(f"Embedding error: {e}")


def is_path_safe(file_path: str, root_dir: str) -> bool:
    """Verify that file_path resolves within root_dir."""
    try:
        target = Path(file_path).resolve()
        root = Path(root_dir).resolve()
        return root == target or root in target.parents
    except Exception:
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Forest semantic query tool")
    ap.add_argument("query", help="Natural language search query")
    ap.add_argument("-k", type=int, default=5, help="Number of results (default: 5)")
    ap.add_argument("--db", default=DB_PATH, help="Path to sqlite-vec database")
    args = ap.parse_args()

    active_db = args.db
    if not os.path.exists(active_db):
        sys.exit(
            f"Error (INDEX_NOT_INITIALIZED): Database not found at {active_db}.\n"
            "Build the index first using 'python3 forest_index.py'."
        )

    db_uri = f"file:{os.path.abspath(active_db)}?mode=ro"
    db = sqlite3.connect(db_uri, uri=True)
    try:
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)

        q = embed_query(args.query)
        rows = db.execute(
            """
            SELECT c.file_path, c.heading, v.distance, c.text
            FROM vec_chunks v
            JOIN chunks c ON c.id = v.chunk_id
            WHERE embedding MATCH ?
              AND k = ?
            ORDER BY v.distance
            """,
            (sqlite_vec.serialize_float32(q), max(1, args.k)),
        ).fetchall()

        if not rows:
            print(f"No results found for query {args.query!r}. Check if index is populated.")
            return

        print(f"Query: {args.query!r} (top {len(rows)} results)")
        count = 0
        for path, heading, dist, text in rows:
            if not is_path_safe(path, VAULT_ROOT):
                continue
            count += 1
            score = 1.0 - float(dist)
            snippet = " ".join(text.split())[:200]
            print(f"\n[{count}] score={score:.3f} path={path}")
            print(f"    heading: {heading or '(none)'}")
            print(f"    snippet: {snippet}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
