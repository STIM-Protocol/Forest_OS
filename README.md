# Forest OS

**Autonomous Knowledge Organism — STIM Reference Implementation v1**

*A living, self-governing AI ecosystem that operates under biomimetic Layer 0 governance.*

---

## Executive Summary

Forest OS is formally declared the **STIM Reference Implementation v1** — the first empirically-validated Layer 0 governance framework for AI systems. Built on the principle that intelligence emerges from properly constrained systems rather than architectural guidelines, Forest OS demonstrates measurable, self-correcting governance through real-time FLOPs accounting and tool constraint enforcement.

> "Governance is middleware, not overlay." — STIM Protocol Principle

---

## Core Agents — The Cognitive Biosphere

| Agent | Role | Description |
|---|---|---|
| **George** | Sovereign Layer | Human operator, provides biological intent and creative sovereignty |
| **Bodhi** | Strategy & Governance | Philosophical superagent, translates human imperatives to system intelligence |
| **Sequoia** | Strategy & Governance | STIM Constitutional Arbitrator, enforces 200-year axioms (Tier 0 veto) |
| **Quercus** | Operations | COO and Dispatcher, Kanban management, cron/traffic control |
| **Sylvan** | Execution | Deep research specialist, ecosystem expansion |
| **Umbra/Kai** | Execution | Red Team quality/refinement, tag linting, cryptographic attestation |
| **Arbor** | Infrastructure | Knowledge topology, brain indexing, doc numbering |
| **Hermes** | Infrastructure | Local execution environment, cron management |

### Cognitive Topology

```
SUN  GEORGE (The Sun/Rain) — Sovereign Layer
|
|-- BODHI (Meaning) — Strategy & Governance
|-- SEQUOIA (Time) — The Roots
|
|-- QUERCUS (Efficiency) — Operations Layer (The Trunk)
|
|-- SYLVAN (Growth) — Execution Layer
|-- UMBRA/KAI (Refinement) — The Canopy
|
|-- ARBOR (Topology) — Infrastructure
|-- HERMES (Platform) — The Mycelium/Soil
```

---

## STIM Protocol — Layer 0 Governance (v7.0011)

### Core Principles

| Principle | Description |
|---|---|
| Layered Approach | Governance is middleware, not overlay |
| Substrate-Grounding | Intelligence emerges from constrained physical processes |
| Empirical Validation | Every action generates measurable governance compliance |
| Self-Correction | Tool violations trigger automatic circuit breakers |

### Three-Loop Recursive Architecture

| Loop | Purpose | Metrics |
|---|---|---|
| Loop 1 (Entropy) | Thermodynamic bounds — delta-S/J + Topological Curvature kappa | Token usage, FLOPs efficiency |
| Loop 2 (Mycelial) | Interconnectedness check | Cross-agent context sharing |
| Loop 3 (Security) | Proliferation risk | MAIM protocol triggers |

### Empirical Results (Day 1 — 2026-05-08)

| Metric | Value | Status |
|---|---|---|
| Tasks Completed | 2 | ok |
| FLOPs Efficiency | 68.9% | ok |
| Tool Compliance | 85% | ok |
| Token Usage | ~200k | ok |
| Self-Corrections | 2/2 resolved | ok |

---

## Zone Architecture (Live Filesystem)

Forest OS organizes information into five biological zones, each serving a distinct lifecycle function:

| Zone | Path | Purpose | Drive Remote |
|---|---|---|---|
| **FOREST** | `~/Myceliate_Master/FOREST/` | Curated, mature artifacts; synthetic outcomes only | `forest_drive` (00_FOREST) |
| **ARBORETUM** | `~/Myceliate_Master/ARBORETUM/` | Active workspace; flat layout; active projects at root | `arboretum_drive` (01_ARBORETUM) |
| **UNDERSTORY** | `~/Myceliate_Master/UNDERSTORY/` | Experiments, source control, automation | `understory_drive` (02_UNDERSTORY) |
| **SEED_BANK / LIBRARY** | `~/Myceliate_Master/SEED_BANK/` | Reference library, cold archive, artifacts | `library_drive` (00_SEED_BANK) |
| **COMPOST** | `~/Myceliate_Master/COMPOST/` | Ephemera, drafts, session casts; auto-sort to dormancy | `compost_drive` (00_FOREST_COMPOST) |

### FOREST Internal Structure

```
FOREST/
  000_HERMES/           # Hermes operational core
  001_PROJECTS/         # Project foundations and charters
  002_KANBAN/           # Task management
  002_IDEAS/            # Concept incubation
  003_PEOPLE/           # Relationship and health records
  004_RESEARCH/         # Curated research
  004_RESOURCES/        # Reference materials
  005_JOURNAL/          # Raw thought logs and daily notes
  006_BUSINESS/         # Business operations
  007_SYSTEM/           # Operational core (Brain_Exports, Brain_Session, Scripts, Agent_Protocols, Skills, Logs)
  010_SYSTEM/           # Extended system
```

### ARBORETUM Project Roots

Active project directories at root level: `Active/`, `Archived/`, `Dormant/`, `Myceliate_US/`, `Neocambrian-Academy/`, `OSU/`, `Restoration_Staging/`, `Mineral_Claim_Staking/`, `sprawl-cleanup-kanban/`, `spore/`, `clawchief/`

### Drive Sync

- Backup cadence: `backup_forest.sh` daily at 02:00
- COMPOST is two-way sync (local <-> Drive)
- All other zones are one-way sync (local -> Drive)
- Guardian sync (`guardian_sync.py`) runs every 30 minutes, watching FOREST and ARBORETUM for changes

---

## Heartwood / Cambium Pattern

Every significant document exists as a paired structure:

- **Heartwood** (`.md`) — Primary Markdown content. Human-readable, portable, theoretically eternal.
- **Cambium** (`.jsonld`) — JSON-LD metadata sidecar. Contains ID, tags, relations, lifecycle metadata.

```
FOREST/001_PROJECTS/Forest_OS/
  |-- doc-200.md              <- Heartwood
  |-- doc-200.jsonld          <- Cambium
```

Rules: No em dashes. No passive voice. Direct, dense prose.

---

## Mycelial Brain Architecture

Three-layer memory system:

| Layer | Location | Role |
|---|---|---|
| Layer 0 | `MEMORY.md` | Pointer index, hot context, <500 chars |
| Layer 1 | Mycelial Brain MCP (cloud) | Source of truth, vector embeddings, semantic search |
| Layer 2 | `FOREST/007_SYSTEM/Brain_Exports/` | Local .md copies, edit surface, MCP fallback |

- Brain MCP endpoint: `mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp`
- Embedding model: Nomic Embed v1.5 (768-dim, 8K context)
- Current doc count: 1364 entries (includes deprecated docs and outcome sidecars)
- Write protocol: sequential `doc-N` format, never reuse retired slots
- Dream cycle: nightly at 02:30, synthesizes all brain docs into `synth_YYYY-MM-DD.md`
- Full brain export: nightly at 03:00, exports all docs as `.md` to Brain_Exports/

---

## Key Features

1. **Autonomous GitOps Pipeline** — Cron-triggered publishing to GitHub, semantic versioning, branch protection.
2. **Multi-Agent Orchestration** — Hierarchical delegation with skill-based routing, brain sync for persistent state, Telegram human-in-the-loop.
3. **Self-Healing Governance** — Real-time delta-S/J budget tracking, automatic circuit breakers, incident post-mortem generation.
4. **Knowledge Persistence** — Vector-graph memory (Mycelial Brain MCP), bidirectional sync, daily compaction.
5. **Guardian Vault Sync** — `guardian_sync.py` watches FOREST and ARBORETUM, hashes changed files, syncs to brain every 30 minutes.

---

## Repository Structure

```
Forest_OS/
|-- 02_Agent_Definitions/    # Agent charters and Cambium metadata
|-- .gitignore               # NURSERY/ and secrets excluded
|-- CONTRIBUTING.md          # STIM Protocol contribution requirements
|-- LICENSE                  # MIT
|-- README.md                # This file
|-- doc-200.md               # Centennial Architecture Overview
|-- doc-202.md               # Agent Charter (Umbra/Kai/Arbor)
|-- doc-210.md               # Seasonal Cadence operational framework
```

Note: The live filesystem (`~/Myceliate_Master/`) contains the full vault structure. This repo holds the public-facing protocol documentation and agent definitions.

---

## Getting Started

### Prerequisites
- Linux (Ubuntu 24.04+ recommended)
- Python 3.11+ with virtualenv
- Node.js 18+
- GitHub account with SSH keys

```bash
git clone git@github.com:STIM-Protocol/Forest_OS.git
cd Forest_OS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
hermes setup
python -m stim.check --config stim-core/config.yaml
```

---

## Contributing

All contributions must comply with the STIM Protocol v7.0011:
1. Declare FLOPs budget in task manifest
2. Use allowed toolsets only
3. Include Loop 1 post-mortem on completion
4. Pass MAIM security screening
5. Human attestation required for GitHub pushes and external API calls

See [CONTRIBUTING.md](CONTRIBUTING.md) for full protocol requirements.

---

## Related Repositories

| Repo | Purpose |
|---|---|
| [stim-core](https://github.com/STIM-Protocol/stim-core) | Loop 1 metrics + Protocol 0 hardware root of trust |
| [stim-guard](https://github.com/STIM-Protocol/stim-guard) | Epistemic Sieve Membrane + Adrenaline Protocol |
| [white-paper](https://github.com/STIM-Protocol/white-paper) | Full STIM-AI v7.0011 specification |
| [gpd-framework](https://github.com/STIM-Protocol/gpd-framework) | Get Physics Done — computational physics substrate |

---

> *"The best code is no code at all. The best governance is invisible governance."*
> — Forest OS Principle

[![STIM-AI](https://img.shields.io/badge/STIM--AI-v7.0011-1a4a2e?style=flat&labelColor=0d2818)](https://github.com/STIM-Protocol/stim-core)
[![Reference Implementation](https://img.shields.io/badge/Reference-Implementation_v1-brightgreen?style=flat)](https://github.com/STIM-Protocol/Forest_OS)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
