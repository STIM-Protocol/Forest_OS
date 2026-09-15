#!/usr/bin/env python3
"""forest_search MCP server (stdio): semantic search over the Forest index.

Exposes one tool: forest_search(query: str, k: int = 5) -> top-k chunks
with path, heading, snippet, score. Wraps sqlite-vec search logic.
JSON-RPC 2.0 and MCP 2024-11-05 compliant.
Governance: Doc-414 compliant (Zero em dashes, strict claims discipline).
"""
import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path
import numpy as np
import sqlite_vec

# Environment configuration
DEFAULT_VAULT_ROOT = str(Path.home() / "Myceliate_Master")
VAULT_ROOT = os.environ.get("FOREST_VAULT_ROOT", DEFAULT_VAULT_ROOT)
DEFAULT_DB_PATH = os.path.join(VAULT_ROOT, "UNDERSTORY", "SYSTEM", "forest-index", "forest_index.db")
DB_PATH = os.environ.get("FOREST_INDEX_DB", DEFAULT_DB_PATH)
OLLAMA_ENDPOINT = os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434/api/embed")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "nomic-embed-text")
MAX_K = int(os.environ.get("FOREST_SEARCH_MAX_K", "20"))
MAX_SNIPPET_LEN = 300


def log_diag(msg: str) -> None:
    """Write diagnostic messages to stderr to preserve clean stdout JSON-RPC framing."""
    sys.stderr.write(f"[forest_search_mcp] {msg}\n")
    sys.stderr.flush()


def embed(text: str) -> np.ndarray:
    """Generate embedding vector using local Ollama endpoint."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "input": [f"search_query: {text}"]
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.load(r)
            embeddings = res.get("embeddings") or [res.get("embedding")]
            if not embeddings or not embeddings[0]:
                raise ValueError("Empty embedding returned from Ollama endpoint.")
            return np.array(embeddings[0], dtype=np.float32)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to reach Ollama at {OLLAMA_ENDPOINT}: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Embedding error: {e}") from e


def is_path_safe(file_path: str, root_dir: str) -> bool:
    """Verify that file_path resolves within root_dir and does not escape via traversal or symlink."""
    try:
        target = Path(file_path).resolve()
        root = Path(root_dir).resolve()
        return root == target or root in target.parents
    except Exception:
        return False


def search(query: str, k: int = 5, db_override: str = None) -> list:
    """Search the vector database. Returns structured results or raises informative errors."""
    active_db = db_override or DB_PATH
    if not os.path.exists(active_db):
        raise FileNotFoundError(
            f"INDEX_NOT_INITIALIZED: Database not found at {active_db}. "
            "Please build the index using 'python3 forest_index.py' before querying."
        )

    clamped_k = max(1, min(k, MAX_K))
    q_vec = embed(query)

    # Use read-only URI mode to guarantee no mutation occurs on search
    db_uri = f"file:{os.path.abspath(active_db)}?mode=ro"
    db = sqlite3.connect(db_uri, uri=True)
    try:
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)

        rows = db.execute(
            """
            SELECT c.file_path, c.heading, v.distance, c.text
            FROM vec_chunks v
            JOIN chunks c ON c.id = v.chunk_id
            WHERE embedding MATCH ?
              AND k = ?
            ORDER BY v.distance
            """,
            (sqlite_vec.serialize_float32(q_vec), clamped_k),
        ).fetchall()

        results = []
        for p, h, d, t in rows:
            # Guard against path traversal outside the vault root
            if not is_path_safe(p, VAULT_ROOT):
                continue
            clean_snippet = " ".join(t.split())[:MAX_SNIPPET_LEN]
            results.append({
                "score": round(1.0 - float(d), 3),
                "path": p,
                "heading": h or "",
                "snippet": clean_snippet
            })
        return results
    finally:
        db.close()


TOOLS = [{
    "name": "forest_search",
    "description": "Semantic search over the local Forest index. Returns top-k chunks with file path, heading, snippet, score. Read-only and offline.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural-language search query"
            },
            "k": {
                "type": "integer",
                "description": f"Number of results (default 5, maximum {MAX_K})",
                "default": 5
            }
        },
        "required": ["query"]
    }
}]


def send_rpc(msg: dict) -> None:
    """Send JSON-RPC message to stdout."""
    raw = json.dumps(msg)
    sys.stdout.write(raw + "\n")
    sys.stdout.flush()


def handle_message(msg: dict) -> None:
    """Process incoming JSON-RPC 2.0 messages."""
    msg_id = msg.get("id")
    method = msg.get("method")
    params = msg.get("params", {})

    if method == "initialize":
        send_rpc({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "forest_search",
                    "version": "1.0.0"
                }
            }
        })
    elif method == "notifications/initialized":
        pass
    elif method == "tools/list":
        send_rpc({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        })
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "forest_search":
            query = args.get("query", "").strip()
            if not query:
                send_rpc({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": "Error: 'query' parameter cannot be empty."}],
                        "isError": True
                    }
                })
                return
            try:
                k_val = int(args.get("k", 5))
                res = search(query, k_val)
                send_rpc({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=1)}]
                    }
                })
            except FileNotFoundError as e:
                send_rpc({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps({
                                "error": "INDEX_NOT_INITIALIZED",
                                "message": str(e)
                            })
                        }],
                        "isError": True
                    }
                })
            except Exception as e:
                send_rpc({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"error: {e}"}],
                        "isError": True
                    }
                })
        else:
            send_rpc({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Tool '{name}' not found"
                }
            })
    elif method == "ping":
        send_rpc({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {}
        })
    else:
        if msg_id is not None:
            send_rpc({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            })


def main() -> None:
    """Main input loop parsing JSON-RPC over stdin."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        if line.startswith("Content-Length:"):
            length = int(line.split(":")[1].strip())
            sys.stdin.readline()
            body = sys.stdin.read(length)
            try:
                msg = json.loads(body)
            except Exception:
                continue
        else:
            try:
                msg = json.loads(line)
            except Exception:
                continue

        handle_message(msg)


if __name__ == "__main__":
    main()
