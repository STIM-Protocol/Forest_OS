# Forest Search: Local Semantic Index & Knowledge Infrastructure

## 1. Overview and Architecture

Forest Search is a local, sovereign semantic search engine designed for Forest OS vaults. It enables natural-language retrieval across thousands of markdown notes, field logs, arboricultural records, and system documents without leaking private contents to the web.

```
Vault Markdown Files (*.md, *.jsonld)
                │
                ▼
      Heading-Based Chunking (~1000 chars)
                │
                ▼
     Local Ollama (nomic-embed-text, 768-dim)
                │
                ▼
    sqlite-vec Database (vec0 virtual table, cosine metric)
                │
         ───────┴───────
        │               │
        ▼               ▼
 CLI Query Tool    MCP Stdio Server
(forest_query.py) (forest_search_mcp.py)
                        │
                        ▼
           Local Agent Fleet (AG, Hermes, OpenClaw)
```

### Core Characteristics
* **Zero Cloud Leakage:** All embeddings and vector searches execute strictly on localhost. No private documents or queries leave the host machine.
* **Storage Footprint:** Backed by a single SQLite database leveraging the `sqlite-vec` extension.
* **Vector Model:** Defaults to `nomic-embed-text` running on local Ollama (`http://127.0.0.1:11434/api/embed`).
* **Governance Compliance:** Doc-414 compliant (zero em dashes, strict claims discipline).

---

## 2. Vault vs. Repository Boundary

In Forest OS, the Git repository is source code only. The operating vault (e.g. `~/Myceliate_Master`) holds private documents and generated data.

* **Excluded from Git:** The database (`forest_index.db`), build logs (`build.log`), watchdog logs (`loop.log`), and all private markdown files remain strictly in your local vault. They must never be staged or committed to Git.
* **Self-Hosted Indexing:** Users downloading Forest OS build their own local index over their personal knowledge base using `forest_index.py`.

---

## 3. Environment Variables and Configuration

| Variable | Default | Purpose |
|---|---|---|
| `FOREST_VAULT_ROOT` | `~/Myceliate_Master` | Root path of the operating vault to index and search. |
| `FOREST_INDEX_DB` | `$FOREST_VAULT_ROOT/UNDERSTORY/SYSTEM/forest-index/forest_index.db` | Absolute path to the sqlite-vec database. |
| `OLLAMA_ENDPOINT` | `http://127.0.0.1:11434/api/embed` | Local Ollama embedding URL (must bind to loopback). |
| `OLLAMA_MODEL` | `nomic-embed-text` | Embedding model name pulled in Ollama. |
| `FOREST_SEARCH_MAX_K` | `20` | Maximum allowed top-k chunk results per query. |

---

## 4. Operational Workflow

### Step 1: Preflight Doctor Check
Verify that all prerequisites are satisfied before initiating any build:

```bash
python3 03_Automation_Scripts/forest-search/forest_index.py --doctor
```

The doctor command checks:
1. Vault root directory accessibility and file count.
2. Disk space headroom (recommending at least 2.0 GB free).
3. Local Ollama responsiveness and `nomic-embed-text` model availability.
4. `sqlite-vec` extension dynamic loadability.

### Step 2: Initial Index Build
Run an explicit indexing pass:

```bash
python3 03_Automation_Scripts/forest-search/forest_index.py --full
```

### Step 3: Incremental Updates
Only files with modified timestamps (`mtime`) will be processed:

```bash
python3 03_Automation_Scripts/forest-search/forest_index.py --incremental
```

### Step 4: Terminal CLI Query
Test search results from the command line:

```bash
python3 03_Automation_Scripts/forest-search/forest_query.py "ISA certification requirements" -k 5
```

---

## 5. MCP Tool Integration

The MCP server (`forest_search_mcp.py`) exposes a single tool: `forest_search(query: str, k: int = 5)`.

### Cold-Start Behavior
If a search query is issued before the index is built, the server immediately returns a structured error without performing an unexpected scan or package download:

```json
{
  "error": "INDEX_NOT_INITIALIZED",
  "message": "Database not found at <path>. Build the index using 'python3 forest_index.py' before querying."
}
```

### Security and Scope Boundaries
1. **Path Traversal Guards:** Returned file paths are validated against `FOREST_VAULT_ROOT`. Traversal attempts or symlinks pointing outside the vault root are rejected.
2. **Read-Only SQLite Connections:** Searches open SQLite in URI read-only mode (`?mode=ro`) to prevent index corruption.
3. **OS Account Security Boundary:** In single-user environments, processes executing under the same system account share filesystem permissions. Application-level filtering must be complemented by system-level user controls if multi-tenant isolation is required.
4. **Cloud Isolation:** Cloud-hosted agents (e.g. remote instances) cannot reach localhost stdio without an authorized local proxy. This ensures local system notes remain unexposed.
