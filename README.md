# Forest OS

**Autonomous Knowledge Organism — STIM Reference Implementation v1**

*A living, self-governing AI ecosystem that operates under biomimetic Layer 0 governance.*

---

## 🎯 Executive Summary

Forest OS is formally declared the **STIM Reference Implementation v1** — the first empirically-validated Layer 0 governance framework for AI systems. Built on the principle that intelligence emerges from properly constrained systems rather than architectural guidelines, Forest OS demonstrates measurable, self-correcting governance through real-time FLOPs accounting and tool constraint enforcement.

> **"Governance is middleware, not overlay."** — STIM Protocol Principle

---

## 🌲 Architecture Overview

### Core Agents

| Agent | Role | Description |
|-------|------|-------------|
| **Hermes Agent** | Primary Orchestrator | Operator-Nova skills, cron job management, multi-agent coordination |
| **Sylvan Agent** | Deep Research Specialist | Autonomous research, literature synthesis, philosophical analysis |
| **Bodhi** | Administrative Assistant | Document consolidation, knowledge organization, formatting |
| **Pecan Pi** | Code Generation | Sub-agent for hierarchical code development and refactoring | Pecan Pi is a subordinate agent managed by Hermes, it does NOT generate code independently |
| **Quercus** | Administrative Coordinator | Task organization, routing, operational workflows |
| **Sequoia** | Elder Guardian | Wisdom-oriented reasoning, mentorship, strategic oversight |

### Knowledge Infrastructure

- **Mycelial Brain MCP** — Persistent vector-graph memory with semantic search
- **Obsidian Second Brain** — Local-first knowledge management with LiveSync
- **GitHub Integration** — GitOps workflow for code and documentation versioning

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User-Facing Layer                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Space Agent PWA (Browser / Desktop)                 │   │
│   │  - Dynamic UI (forms, charts, logs)                  │   │
│   │  - Onscreen agent overlay                             │   │
│   └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    Orchestration Layer                    │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Hermes Agent (v0.12+)                                │   │
│   │  - Command & control                                    │   │
│   │  - Cron job scheduling                                 │   │
│   │  - Multi-agent delegation                              │   │
│   └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    Governance Layer                         │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  STIM Protocol Layer 0                                │   │
│   │  - FLOPs budgeting & tracking                         │   │
│   │  - Tool constraint enforcement                        │   │
│   │  - Circuit breaker activation                         │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 STIM Protocol — Layer 0 Governance

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Layered Approach** | Governance is middleware, not overlay |
| **Substrate-Grounding** | Intelligence emerges from constrained physical processes |
| **Empirical Validation** | Every action generates measurable FLOPs compliance |
| **Self-Correction** | Tool violations trigger automatic circuit breakers |

### Three-Loop Recursive Architecture

| Loop | Purpose | Metrics |
|------|---------|---------|
| **Loop 1 (Entropy)** | Thermodynamic bounds | Token usage reduction (3x → 0.5x baseline) |
| **Loop 2 (Mycelial)** | Interconnectedness check | Cross-agent context sharing validation |
| **Loop 3 (Security)** | Proliferation risk | MAIM protocol triggers (0 incidents to date) |

### Empirical Results (Day 1 — 2026-05-08)

| Metric | Value | Status |
|--------|-------|--------|
| Tasks Completed | 2 | ✅ |
| FLOPs Efficiency | 68.9% | ✅ (adjusted after correction) |
| Tool Compliance | 85% | ✅ |
| Token Usage | ~200k | ✅ |
| Self-Corrections | 2/2 resolved | ✅ |

---

## 🚀 Key Features

### 1. Autonomous GitOps Pipeline
- Cron-triggered publishing to GitHub
- Automatic metadata tagging and categorization
- Branch protection with semantic versioning

### 2. Multi-Agent Orchestration
- Hierarchical delegation with skill-based routing
- Brain sync for persistent state across sessions
- Telegram integration for human-in-the-loop feedback

### 3. Self-Healing Governance
- Real-time FLOPs budget tracking
- Automatic circuit breakers on constraint violations
- Incident post-mortem generation with correction verification

### 4. Knowledge Persistence
- Vector-graph memory with semantic search
- Bidirectional sync with Obsidian vault
- Daily compaction and archival workflows

---

## 📁 Repository Structure

```
forest-os/
├── NURSERY/              # Active development (git-ignored)
├── LABORATORY/           # Experimental / in-progress work
├── GARDEN/               # Stable, versioned artifacts
│   ├── 001_PROJECTS/     # Project foundations
│   ├── 002_IDEAS/        # Concept development
│   ├── 003_AUDIBLE/      # Audio book tracking
│   └── 007_SYSTEM/       # Operational protocols
├── LOG/                  # Session logs and metrics
├── SEED_BANK/            # Core reference materials
└── SKILLS/                # Agent capability definitions
```

---

## 🛠️ Getting Started

### Prerequisites
- Linux environment (optimized for Ubuntu 24.04+)
- Python 3.11+ with virtual environment
- Node.js 18+ for Space Agent integration
- GitHub account with SSH keys configured

### Quick Start

```bash
# Clone the repository
git clone git@github.com:STIM-Protocol/Forest_OS.git
cd Forest_OS

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize Hermes agent
hermes setup

# Run STIM compliance check
python -m stim.check --config stim-core/config.yaml
```

### Configuration

Key configuration files:
- `hermes.yaml` — Agent settings and model routing
- `stim-manifest.json` — FLOPs budgets and tool constraints
- `brain.yaml` — Mycelial Brain connection settings

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [STIM Reference Implementation](GARDEN/000_HERMES/thesis/forest-os-stim-reference-implementation-v1.md) | Formal declaration and empirical validation |
| [Forest OS × Space Agent Integration](LABORATORY/SYSTEM/Design_Docs/Forest_OS_x_Space_Agent_Integration_Plan.md) | Frontend integration strategy |
| [Deep Think Analysis](GARDEN/007_SYSTEM/outcomes/stim-deep-think-analysis-2026-05-08.md) | Philosophical foundations |
| [Implementation Plan](GARDEN/007_SYSTEM/tasks/stim-implementation-plan.md) | Roadmap and milestones |

---

## 🤝 Contributing

Forest OS operates under the STIM Protocol. All contributions must:

1. Declare FLOPs budget in task manifest
2. Use allowed toolsets only
3. Include Loop 1 post-mortem on completion
4. Pass MAIM security screening

See `CONTRIBUTING.md` for full protocol requirements.

---

## 📜 License

Forest OS is licensed under the MIT License. See `LICENSE` for details.

---

## 🔗 Links

- **GitHub**: https://github.com/STIM-Protocol/Forest_OS
- **STIM Protocol**: https://github.com/STIM-Protocol
- **Mycelial Brain**: https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp

---

> *"The best code is no code at all. The best governance is invisible governance."*  
> — Forest OS Principle