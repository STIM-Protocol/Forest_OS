# Forest OS: Centennial Architecture — Project Launch

**Project ID:** 01JWWZ1N
**Codename:** Forest OS
**Version:** 0.1.0 — Protocol Layer Complete
**Status:** Active / Core Infrastructure
**Timeline:** 200-year design horizon
**Maintainer:** Bodhi (Arboracle) + George Steward
**Date:** 2026-04-26

---

## Mission Statement

Forest OS is a decentralized, self-documenting knowledge and agency ecosystem designed to operate across multiple generations. It treats information as a living organism — growing, evolving, and decaying in structured zones — while maintaining full agentic autonomy and long-term survivability.

**Core promise:** A personal (or team) knowledge base that compounds in value without degradation,Bitrot, or lock-in.

---

## Design Principles

1. **Separation of Substance and Metadata** — Heartwood (content) is distinct from Cambium (relations, tags, identity).
2. **Decentralized Vaults** — No single point of failure; Forest, Library, Greenhouse, Understory, Compost each have clear roles.
3. **Machine-Actionable Protocols** — Every process is codified; agents can execute without human interpretation.
4. **Generational Durability** — Plain-text formats, open schema, self-contained documentation.
5. **Agent-First Architecture** — Built from the ground up to be operated by AI agents (OpenClaw, Claude Code, etc.) as much as humans.

---

## Project Structure

```
ARBORETUM/Active/Forest_OS/
├── 00_Core_Protocols/       (canonical Forest OS docs, cloned from FOREST/000_DASHBOARD/)
├── 01_Docs/                 (human-friendly guides, tutorials, philosophy)
├── 02_Agent_Definitions/    (OpenClaw agent skill specs, subagent blueprints)
├── 03_Automation_Scripts/   (forest-*, sync, lint, ingest)
├── 04_Configuration/        (yaml/json configs for tools and services)
├── 05_Tests/                (validation suites for protocol compliance)
├── CHANGELOG.md
├── ROADMAP.md
└── README.md                (public-facing overview)

UNDERSTORY/Research/Forest_OS/
├── architecture-diagrams/   (system design sketches, mermaid, plantuml)
├── protocol-experiments/    (proof-of-concept protocol variants)
├── embedding-model-evals/   (nomic vs gemini vs others)
├── agentic-workflows/       (subagent orchestration patterns)
└── papers/                  (relevant academic references)

FOREST/001_PROJECTS/Forest_OS/
├── 01JWWZ1N-forest-os-project-manifest.md   ← this file
├── 01JWWZ1O-protocol-adoption-tracker.md    (who uses what, compliance %)
├── 01JWWZ1P-agent-operations-log.md         (autonomous actions taken)
└── 01JWWZ1Q-200-year-preservation-plan.md   (format migration, emulation strategy)
```

---

## Current Implementation Status

### Phase 1: Foundation (Complete ✅)
- [x] Forest bucket taxonomy defined
- [x] Heartwood/Cambium pattern specified
- [x] Tag Taxonomy created
- [x] Ingestion Pipeline documented
- [x] Sync Protocols documented
- [x] ROOT_MANIFEST placed in Forest

### Phase 2: Agentic Automation (In Progress 🚧)
- [ ] `forest-lint` script (validate .md + .jsonld pairs)
- [ ] `forest-new` scaffolding command
- [ ] Daily memory flush agent (already running, formalize)
- [ ] Forest → Brain sync automation (weekly job)
- [ ] Automated tag sugger (based on content analysis)

### Phase 3: Production Hardening (Next ⌛)
- [ ] Backup rotation and integrity checking
- [ ] Vault health dashboard (Forest size, growth rate, error count)
- [ ] Conflict detection and resolution bots
- [ ] Multi-client sync (mobile, remote machines)

### Phase 4: Longevity Engineering (200-year view)
- [ ] Format migration strategy (Markdown → ?)
- [ ] Emulator / runtime preservation plan
- [ ] Redundant archive locations (geographically distributed)
- [ ] Succession planning document (who takes over if maintainer unavailable)

---

## Agentic Capabilities

Forest OS is *native agentic* — built for autonomous operation:

| Agent Type | Responsibility | Current Status |
|------------|----------------|----------------|
| **Memory Agent** | Daily capture → distillation → MEMORY.md | Running (OpenClaw heartbeat) |
| **Sync Agent** | Forest ↔ Library ↔ Compost coordination | Scripted, needs formal agent wrapper |
| **Lint Agent** | Validate protocol compliance on new docs | Planned |
| **Ingest Agent** | Transform raw PDFs/web into Heartwood | Manual, will automate |
| **Brain Agent** | Manage MCP indexing, versioned updates | Manual triggers, will schedule |
| **Health Agent** | Monitor vault sizes, detect bitrot, alert | Not yet |

All agents live in `ARBORETUM/Active/Forest_OS/02_Agent_Definitions/` as YAML/JSON specs that OpenClaw can load and execute.

---

## Documentation Estate

**Primary sources** (in order of authority):

1. **`FOREST/001_PROJECTS/Forest_OS/`** — project management, decisions, logs (this is the working area)
2. **`ARBORETUM/Active/Forest_OS/00_Core_Protocols/`** — canonical, immutable protocol copies (the "constitution")
3. **`UNDERSTORY/Research/Forest_OS/`** — experiments, design alternatives, research
4. **`FOREST/000_DASHBOARD/`** — public-facing protocol index (mirrors core protocols for discoverability)

**Access model:** Humans read the Dashboard for orientation; agents read the Core Protocols directly; Understory is for R&D.

---

## Immediate Next Actions

- [ ] Create `forest-lint` script (Python) that checks every `.md` in Forest for Heartwood/Cambium completeness.
- [ ] Write `forest-new` CLI wrapper that scaffolds new Forest docs with UUID, Cambium template, and tags.
- [ ] Document the embedding model choice (Nomic v1.5) and rationale in `WORLD_MODEL.md`.
- [ ] Set up daily cron: `0 2 * * * /home/george/Myceliate_Master/backup_forest.sh` (already done) + `0 3 * * * forest-sync --incremental`.
- [ ] Ingest Forest OS core docs into Mycelial Brain as `doc-123` through `doc-128` for searchability.

---

## 200-Year Survivability Strategy

1. **Plain text everywhere** — no proprietary formats. Markdown and JSON-LD are future-proof.
2. **Schema versioning in Cambium** — `@context` URL includes version; future migrations are explicit.
3. **Redundant storage** — Forest (live) + Drive (backup) + offline tape archive (future).
4. **Process documentation** — not just *what* but *why* decisions were made, captured in CHANGELOG.
5. **Agent autonomy** — the system maintains itself without requiring constant human oversight; knowledge outlives maintainers.

---

*This project manifest is itself a Forest OS node: Heartwood + future Cambium sidecar. Treat it as living document.*
