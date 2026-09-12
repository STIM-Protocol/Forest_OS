# Forest OS — Centennial Architecture

**Version:** 0.1.0  
**Status:** Production-Ready (Protocol Layer)  
**License:** CC BY-SA 4.0 (documentation) + MIT (code)  
**Time Horizon:** Designed for 200+ year survivability  

---

## What Is Forest OS?

Forest OS is a **decentralized, self-documenting knowledge and agency ecosystem**. It organizes information into living vaults (Forest, Library, Greenhouse, Understory, Compost) and uses a clean separation between human-readable content (Heartwood) and machine-readable metadata (Cambium).

Built for longevity, agentic operation, and compounding value — not just storage.

---

## Quick Start

### For Humans

1. **Read the Protocol Index:** `ARBORETUM/Active/Forest_OS/01_Docs/Protocol_Index.md`
2. **Understand the Forest:** `FOREST/000_DASHBOARD/MAP_OF_CONTENT.md`
3. **Create your first document:** Use `forest-new dossier "My Topic"` (once installed)

### For Agents (OpenClaw, Claude Code, etc.)

1. Load skills from `ARBORETUM/Active/Forest_OS/02_Agent_Definitions/`
2. Respect `TAG_TAXONOMY.md` for all tag decisions
3. Write `Heartwood + Cambium` pairs to correct Forest bucket
4. Call `brain_create` via MCP to publish for search

---

## Directory Map

```
ARBORETUM/Active/Forest_OS/     ← Active development (protocols, agent defs)
UNDERSTORY/Research/Forest_OS/   ← Experiments, design docs, eval results
FOREST/001_PROJECTS/Forest_OS/   ← Project management, decisions, logs
FOREST/000_DASHBOARD/            ← Public-facing protocol index (mirrored)
```

---

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Heartwood** | Primary Markdown content — the substance |
| **Cambium** | JSON-LD metadata sidecar — the connections |
| **Buckets** | 001–006 categorized zones (Projects, Ideas, People, Resources, Journal, Business) |
| **Mycelial Brain** | Vector search service (MCP) that indexes all Heartwood |
| **Agents** | Autonomous workers that maintain the system (Memory, Sync, Lint, Ingest, Brain, Health) |

---

## Protocols (Read These First)

1. [ROOT_MANIFEST](../FOREST/000_DASHBOARD/ROOT_MANIFEST.md) — Philosophy and architectural principles
2. [WORLD_MODEL](../FOREST/000_DASHBOARD/WORLD_MODEL.md) — Current system state snapshot
3. [TAG_TAXONOMY](../FOREST/000_DASHBOARD/TAG_TAXONOMY.md) — Canonical tag vocabulary
4. [HEARTWOOD_CAMBIUM](../FOREST/000_DASHBOARD/HEARTWOOD_CAMBIUM_PATTERN.md) — File format specification
5. [INGESTION_PIPELINE](../FOREST/000_DASHBOARD/INGESTION_PIPELINE.md) — From raw input to Forest-ready
6. [SYNC_PROTOCOLS](../FOREST/000_DASHBOARD/SYNC_PROTOCOLS.md) — Vault coordination and backup

---

## For Developers

### Setting Up a Local Forest OS Environment

```bash
# Clone or sync Forest from Drive
rclone sync forest_drive:00_FOREST ~/Myceliate_Master/FOREST

# Install dependencies
pip install forest-cli  # (hypothetical package)

# Run lint
forest-lint

# Create new dossier
forest-new dossier "Ryder Education Analysis" --tags person/ryder subject/education
```

### Contributing

- Protocol changes → PR to `ARBORETUM/Active/Forest_OS/00_Core_Protocols/`
- Agent definitions → submit to `02_Agent_Definitions/`
- Experiments → `UNDERSTORY/Research/Forest_OS/`

All contributions must respect the **Stop Slop** style guide (no em dashes, no passive voice, direct prose).

---

## 200-Year Survivability

Forest OS is designed to outlive any single maintainer:

- **Plain-text storage** — Markdown and JSON-LD are theoretically readable forever
- **Open schemas** — no proprietary formats; `@context` is versioned but stable
- **Redundant archives** — Forest (live) + Drive (cloud backup) + offline tape (future)
- **Self-maintaining** — autonomous agents handle daily ops without human intervention
- **Process documentation** — every decision recorded, every protocol justified

Even if all code disappears, a future archaeologist could reconstruct the system from the documents alone.

---

## Current Status (2026-04-26)

- ✅ Core protocols authored and placed in Forest
- ✅ Heartwood/Cambium pattern established
- ✅ Tag taxonomy defined
- ✅ Ingestion and sync processes documented
- ⏳ Agent automation scripts pending implementation
- ⏳ Brain indexing integration complete (needs protocol docs ingested)

**Next milestones:** `forest-lint` binary, `forest-new` scaffolder, autonomous daily sync cron.

---

*Forest OS is not a product. It is a practice.*
