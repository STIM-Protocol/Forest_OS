# World Model: Forest OS Operational State

**Version:** 2026-04-26-Current
**Status:** Live System Snapshot
**Maintainer:** Bodhi (Arboracle) + George Steward

---

## 1. Executive Overview

The Forest OS is a personal knowledge and agency ecosystem that treats information as a living organism. It is designed for high-agency individuals who require frictionless knowledge synthesis, retrieval, and action across multiple modalities and domains.

**Current State:**
- **Vault Size:** ~27,000 objects across five primary vaults (Forest, Library, Greenhouse, Understory, Compost)
- **Active Sync:** Mycelial Brain MCP service running on Google Cloud Run (`mycelial-brain-mcp-1084814124987.us-central1.run.app`)
- **Brain Document Count:** ~118 ingested docs (latest: doc-122 BODHI STIM v1.0 Review)
- **Knowledge Workers:** 1 primary (George Steward), multi-agent sub-session support via OpenClaw

---

## 2. System Architecture

### 2.1 Physical Vaults

| Vault | Purpose | Primary Format | Sync Status |
|-------|---------|----------------|-------------|
| **Forest** | Active working knowledge, projects, people, journals | Markdown + JSON-LD sidecars | Daily heartbeat sync → Drive |
| **Library** | Reference materials (PDFs, images, media) | Native binaries + extracted `.md` text | Batch processed, OCR complete |
| **Greenhouse** | Experimental agents, active learning projects | Mixed (code, configs, protocols) | Git-tracked |
| **Understory** | System design docs, research, prototypes | Markdown + diagrams | Version-controlled |
| **Compost** | Decay zone — deprecated or archived content | Anything | Periodic pruning |

### 2.2 The Mycelial Brain

The brain is a **document embedding + retrieval service** running as a Cloud Run container. It:
- Accepts new documents via `brain_create` / `brain_update` calls
- Generates vector embeddings using the configured model (currently Nomic Embed v1.5)
- Stores vectors in a Qdrant-backed vector database
- Returns ranked search results via `brain_search` and `brain_list`

**Key Endpoints:**
- REST API: `https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp`
- MCP protocol: Native OpenClaw integration via `sessions_spawn` and tool bridging

**Current Brain Contents:**
- `doc-115` ROOT_MANIFEST (Forest OS structure)
- `doc-112` World Model (this doc, when ingested)
- `doc-122` BODHI STIM v1.0 Review (operational intelligence)
- Plus ~115 earlier research artifacts

---

## 3. Orchestration Layer

### 3.1 OpenClaw Agent Runtime

OpenClaw is the local agent execution environment. It provides:
- **Tool access:** filesystem, exec, web, browser, MCP bridging
- **Session management:** `sessions_spawn` for isolated sub-agents
- **Memory persistence:** Daily memory flush to `memory/YYYY-MM-DD.md`
- ** heartbeats:** Periodic check-ins and proactive tasking

OpenClaw runs as a direct user agent (Telegram-integrated) and also supports ACP harnesses when needed.

### 3.2 Sub-Agent Model

Long-running or specialized work is delegated to sub-agents:
- `sessions_spawn(context:"isolated")` by default
- `context:"fork"` used when child needs parent transcript
- Each sub-agent gets its own conversation history and can be steered/killed independently

This isolates failures and enables parallel workstreams.

---

## 4. Knowledge Flow Protocols

### 4.1 Ingestion Paths

1. **Manual Research** → Gemini/Perplexity via browser → synthesis → Forest dossier
2. **External Documents** → Library (binary) + OCR → Markdown text → Forest extraction if relevant
3. **Agent Outputs** → Direct write to Forest following Heartwood/Cambium pattern
4. **Conversation Artifacts** → memory/YYYY-MM-DD.md → periodic distillation into MEMORY.md

### 4.2 Output Destinations

- **Forest** — finalized, actionable knowledge, ready for retrieval
- **Compost** — deprecated concepts, old versions, decayed ideas
- **Brain** — after Forest stabilization, doc is ingested into MCP for semantic search

---

## 5. Current Operational Parameters

### 5.1 Embedding Model

**Model:** `nomic-embed-text-v1.5` (self-hosted via Hugging Face)
- **Context Window:** 8,192 tokens
- **Dimensions:** 768 (fixed)
- **Modality:** Text only (images converted via OCR first)
- **Hosting:** Local GPU inference (cost: fixed infrastructure)
- **Rationale:** Full control, no per-token fees, sufficient quality for text-heavy corpus

**Alternatives under evaluation:** Gemini Embedding 2 (multimodal but expensive, cloud-only).

### 5.2 Agent Defaults

- **Main Agent Model:** `kilocode/kilo-auto/free` (default) — lightweight, fast, sufficient for daily ops
- **High-Reasoning Override:** `google/gemini-3.1-pro-preview` (used when explicitly requested)
- **Fallback Chain:** Pro → Flash Lite → Gemini CLI variants

### 5.3 File Naming & Metadata

- **Heartwood ID:** UUIDv7 format: `01JWWZ1M-descriptive-slug.md`
- **Cambium Sidecar:** Same basename with `.jsonld`
- **Required Cambium fields:** `@context`, `id`, `type`, `tags`, `relations`
- **Buckets:** Must reside in correct numbered FOREST folder (001–006) based on content type

---

## 6. Active Projects & Workstreams

| Project | Status | Location | Next Action |
|---------|--------|----------|-------------|
| **Ryder Education Dossier** | Complete (01JWWZ1M) | Forest/003_PEOPLE/Ryder/ | Share with Collin |
| **Chelsea Medical Consolidation** | Complete | Forest/003_PEOPLE/Chelsea/ | Ongoing sync |
| **Forest OS Protocol Authored** | In Progress | Forest/000_DASHBOARD/ | Finalize World Model, Tag Taxonomy |
| **Mycelial Brain MCP** | Running (rev. 00046-fbb) | Cloud Run | Monitor, ingest new docs |

---

## 7. Known Gaps & TODO

- [ ] **Centralized Protocol Registry** — all Forest OS standards in one searchable index
- [ ] **Tag Taxonomy Master List** — canonical tag definitions and usage guidelines
- [ ] **Automated Forest Linter** — validate Heartwood/Cambium compliance on commit
- [ ] **Brain-to-Forest Sync Direction** — currently one-way (Forest → Brain); need reverse for updates
- [ ] **Versioned Agent Deployments** — track which agent version produced which artifact
- [ ] **Cross-Vault Search UI** — unified search across Forest, Library, Greenhouse

---

## 8. Evolutionary Notes

**2026-04-24:** Major re-organization to person-centric Forest structure (Chelsea Medical, Ryder Education). Established COMPOST two-way mirror with Google Drive.

**2026-04-25:** Mycelial Brain connection restored after Cloud Run deployment fix; ROOT_MANIFEST and BODHI STIM ingested.

**2026-04-26:** Implemented Heartwood/Cambium pattern systematically; removed em dashes per Stop Slop; began Forest OS protocol documentation.

---

## 9. Governance

- **Protocol Changes:** Require consensus between George Steward and Bodhi; documented in `FOREST/000_DASHBOARD/CHANGELOG.md`
- **Brain Ingestions:** Triggered by explicit `brain_create` / `brain_update` calls; new docs auto-numbered
- **Tag Additions:** New tags must be registered in the Tag Taxonomy to avoid semantic drift

---

*End of World Model — Living Document, Update as State Evolves*
