# Forest OS: Sovereign Forestry & Arboriculture Workbench
### Autonomous Knowledge Organism &bull; STIM Protocol Reference Implementation v1

[![STIM-AI](https://img.shields.io/badge/STIM--AI-v7.0011-1a4a2e?style=flat&labelColor=0d2818)](https://github.com/STIM-Protocol/stim-core)
[![Reference Implementation](https://img.shields.io/badge/Reference-Implementation_v1-brightgreen?style=flat)](https://github.com/STIM-Protocol/Forest_OS)
[![Port 5483 LIVE](https://img.shields.io/badge/Workbench-Port_5483_(LIVE)-7fbbb3?style=flat)](http://localhost:5483)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/STIM-Protocol/Forest_OS/blob/main/LICENSE)
[![Tests: 20 Passing](https://img.shields.io/badge/Tests-20_Passed-83c092?style=flat)](#automated-test-verification)

Forest OS is the sovereign computational operating system for ecological land stewards, foresters, consulting arborists, and canopy researchers. It functions simultaneously as an **autonomous, biomimetic AI knowledge organism** and as a **heavy scientific field-to-lab workstation**. 

Forest OS is formally declared the **STIM Protocol Reference Implementation v1**, demonstrating how Layer 0 governance constraints (Thermodynamic entropy tracking, substrate grounding, and strict host isolation) manage heterogeneous, multi-modal ecological computing pipelines without system degradation.

---

## 1. Executive Summary & Case Study Thesis

Traditional ecological computing suffers from severe environment fragility: unmaintained Fortran growth models, archived CRAN packages, conflicting GDAL/GEOS C-bindings, and massive Python dependency collisions.

Forest OS solves this through a **Three-Tier Zero-Bloat Architecture** governed by the STIM Protocol (Sovereign, Transparent, Immutable, Minimal):

1. **Sovereign:** Absolute host protection. No root pollution, no global `pip install`. User-space execution via `uv tool` and container sidecars.
2. **Transparent:** Standardized POSIX CLI wrappers, FreeDesktop XDG desktop entries, custom SVG icons, and a consolidated web workbench on port 5483.
3. **Immutable:** Biomimetic lifecycle: Spores (raw ingest) &rarr; Cambium (active state) &rarr; Heartwood (immutable published models) &rarr; Compost (pruned ephemera) &rarr; Greenhouse (experimental algorithms).
4. **Minimal:** Elimination of runtime duplication. Host-native C++ where performance matters, compiled OCI sidecars for complex R and Fortran suites.

---

## 2. The Cognitive Biosphere (Core Agents)

Forest OS operates under hierarchical multi-agent coordination grounded in biological metaphors:

```
SUN:  GEORGE (The Sun/Rain) - Sovereign Human Operator
 |
 |-- BODHI (Meaning) - Strategy & Governance
 |-- SEQUOIA (Time) - The Roots (STIM Constitutional Arbitrator, Tier 0 Veto)
 |
 |-- QUERCUS (Efficiency) - Operations Director (The Trunk: Dispatch, Cron, Locks)
 |
 |-- SYLVAN (Growth) - Execution Layer (Polyploidy & Forest Research)
 |-- UMBRA / KAI (Refinement) - The Canopy (Red Team Quality, Cryptographic Attestation)
 |
 |-- ARBOR (Topology) - Infrastructure (Knowledge Graphs, Doc Indexing)
 |-- HERMES (Platform) - Soil & Mycelium (Local Execution Substrate)
```

| Agent | Role | Description |
|---|---|---|
| **George** | Sovereign Layer | Human operator, provides biological intent, ground-truth field data, and creative sovereignty |
| **Bodhi** | Strategy & Governance | Philosophical superagent, translates human imperatives to system intelligence |
| **Sequoia** | Strategy & Governance | STIM Constitutional Arbitrator, enforces 200-year preservation axioms (Tier 0 veto) |
| **Quercus** | Operations | COO and Dispatcher, Kanban state management, cron scheduling, and traffic control |
| **Sylvan** | Execution | Deep research specialist, ecological modeling, and toolchain evaluation |
| **Umbra / Kai**| Execution | Red Team refinement, tag linting, code quality auditing, and cryptographic attestation |
| **Arbor** | Infrastructure | Knowledge topology, Mycelial Brain indexing, and doc numbering |
| **Hermes** | Infrastructure | Local execution environment, container orchestration, and hardware monitoring |

---

## 3. The Three-Tier Zero-Bloat Scientific Architecture

Forest OS provides complete operational parity across **Ubuntu (26.04/26.10 LTS/rolling)** and **Arch Linux / Omarchy**:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                    FOREST OS WORKBENCH (Port 5483)                     │
 │          Consolidated Web Portal, Field Recipes & Decision Wizard      │
 └───────────────────┬───────────────────────────────┬────────────────────┘
                     │                               │
 ┌───────────────────▼──────────────┐   ┌────────────▼────────────────────┐
 │  TIER 1: HOST USER-SPACE CLI     │   │  TIER 2: WORKSTATION DESKTOP    │
 │  Isolated uv virtual environments│   │  Native Qt / Wayland / C++      │
 │  • DeepForest (Canopy Crown AI)  │   │  • QGIS (Geographic Info System)│
 │  • BirdNET (Bioacoustics)        │   │  • GDAL / PDAL (Point Clouds)   │
 │  • pyDendron (Tree-Ring GUI)     │   │  • CloudCompare (3D Vegetation) │
 │  • pyfia (USFS FIA Analysis)     │   │  • Desktop Launchers & Icons    │
 └──────────────────────────────────┘   └─────────────────────────────────┘
                     │
 ┌───────────────────▼────────────────────────────────────────────────────┐
 │  TIER 3: SCIENTIFIC CONTAINER SIDECARS (Docker / Podman)               │
 │  OCI sidecars mounting current working directory, zero host footprint  │
 │  • forest-r-engine (lidR, TreeLS, rGEDI, BIOMASS, allodb, RStudio 8787)│
 │  • forest-sim (22 compiled USFS Open-FVS regional variants, microfvs)  │
 └────────────────────────────────────────────────────────────────────────┘
```

### Empirical Sidecar Verification Matrix
| Sidecar Container | Package / Component | Verified Version | Capability |
| :--- | :--- | :--- | :--- |
| `forest-r-engine` | `lidR` | v4.3.3 | Airborne LiDAR CHM, ground classification & tree segmentation |
| `forest-r-engine` | `TreeLS` | v2.0.6 | Terrestrial Laser Scanning (TLS) stem isolation & DBH extraction |
| `forest-r-engine` | `rGEDI` | v0.5.7 | NASA GEDI spaceborne full-waveform canopy modeling |
| `forest-r-engine` | `BIOMASS` | v2.2.7.1 | Aboveground Biomass (AGB) calculation & carbon auditing |
| `forest-r-engine` | `dplR` | v1.7.9 | Canonical dendrochronological cross-dating & detrending |
| `forest-r-engine` | `allodb` | v0.0.1.9000 | ForestGEO global allometric biomass equations |
| `forest-r-engine` | `ForestTools` | v1.0.3 | Variable window filters & marker-controlled watershed crowns |
| `forest-r-engine` | `hemispheR` | v1.1.8 | Hemispherical fisheye photography canopy openness & LAI |
| `forest-r-engine` | `treeclim` | v2.0.8.0 | Climate-growth response functions & seasonal correlation |
| `forest-sim` | Open-FVS | 22 Variants | Full USFS nationwide compiled geographic variant suite |
| `forest-sim` | `microfvs` | v0.2.0 | FastAPI REST service for cloud and local growth simulations |

---

## 4. Master Consolidated Workbench (Port 5483)

Forest OS ships with an integrated, sovereign web portal built with the Everforest dark palette, glassmorphism, and an animated mycorrhizal spore canvas:

* **Default URL:** `http://localhost:5483` (Mnemonic: 5483 spells `LIVE` on phone keypad)
* **Launcher Command:** `forest-workbench`
* **Features:**
  * **Executive Telemetry Bar:** Real-time health indicators for Tier 1, Tier 2, and Tier 3 runtimes.
  * **Comprehensive 33-Tool Catalog:** Filterable across 7 forestry domains with dynamic keyword search and one-click copyable CLI execution snippets.
  * **5 Production Field Pipelines:** Tested end-to-end recipes for Drone Crown Detection, Airborne LiDAR Processing, Bioacoustics Inventory, Tree Ring Dating, and Stand Growth Modeling.
  * **Forester's Interactive Decision Wizard:** Correlates input field data (e.g. Drone RGB, TLS, Increment Cores, Audio) with management objectives to prescribe toolchains and generate executable bash scripts.
  * **Local Services Hub:** Direct access to RStudio Server (`:8787`), microfvs REST API (`:8000`), pyDendron, and BirdNET.

---

## 5. FreeDesktop XDG Desktop Integration

Forest OS integrates directly into GNOME, XFCE, and Wayland application menus with custom scalable SVG icons in `04_Configuration/desktop/`:

* `forest-workbench.desktop` &bull; **Forest OS Workbench** (Exec: `forest-workbench`)
* `forest-birdnet.desktop` &bull; **BirdNET Canopy Analyzer** (Exec: `birdnet-gui`)
* `forest-pydendron.desktop` &bull; **pyDendron Tree-Ring Analysis** (Exec: `pyDendron`)
* `forest-rstudio.desktop` &bull; **Forest RStudio Scientific Engine** (Exec: `forest-rstudio-launch`)
* `forest-sim.desktop` &bull; **Forest-Sim Open-FVS Simulator** (Exec: `forest-sim-launch`)
* `forest-deepforest.desktop` &bull; **DeepForest Canopy Detection** (Exec: `forest-deepforest-launch`)
* `forest-qgis.desktop` &bull; **QGIS Forestry Edition** (Exec: `qgis %F`)

Install or remove launchers with single commands:
```bash
./03_Automation_Scripts/install_desktop_launchers.sh
./03_Automation_Scripts/uninstall_desktop_launchers.sh
```

---

## 6. Repository Layout

```
Forest_OS/
├── 00_Core_Protocols/         # STIM specifications, world models, ingestion pipelines
├── 01_Docs/                   # Implementation notes, handoff packs, empirical reports
├── 02_Agent_Definitions/      # Agent charters (Sequoia, Quercus, Sylvan, Umbra/Kai)
├── 03_Automation_Scripts/     # CLI wrappers, container builders, desktop installers
│   ├── forest-workbench       # Local web server on port 5483
│   ├── forest-r               # Headless CLI wrapper for forest-r-engine
│   ├── forest-sim             # CLI wrapper for Open-FVS 22 regional variants
│   ├── build_containers.sh    # Multi-container OCI build orchestrator
│   └── install_desktop_launchers.sh # FreeDesktop integration script
├── 04_Configuration/          # Container recipes, desktop launchers, and web portal
│   ├── containers/            # Containerfiles for forest-r-engine & forest-sim
│   └── desktop/               # forest_workbench.html, .desktop files, and SVG icons
├── 05_Tests/                  # Automated verification suites (20/20 passing)
├── Documentation/             # Academic briefs, comparative analyses, and field guides
├── Forest_OS/                 # Inner agent workspace, sync watchers, and knowledge
├── CONTRIBUTING.md            # STIM Protocol contribution and Stop Slop requirements
├── LICENSE                    # MIT License
├── doc-200.md                 # Centennial Architecture Overview
├── doc-202.md                 # Agent Charters & Cognitive Topology
└── doc-210.md                 # Seasonal Cadence operational framework
```

---

## 7. Quick Start Guide

### Prerequisites
* Linux (Ubuntu 24.04/26.04 LTS or Arch Linux / Omarchy)
* Docker or Podman
* Python 3.11+ and `uv` package manager

### 1. Build Container Sidecars
```bash
# Build both forest-r-engine and forest-sim
./03_Automation_Scripts/build_containers.sh all
```

### 2. Install Desktop Launchers & CLI Helpers
```bash
./03_Automation_Scripts/install_desktop_launchers.sh
```

### 3. Launch the Consolidated Workbench
```bash
# Starts local web server on port 5483 and opens browser
forest-workbench
```

### 4. Run CLI Workflows
```bash
# Execute R LiDAR script without installing R on host
forest-r script.R

# Query Open-FVS compiled variants
forest-sim variants

# Run DeepForest tree crown detection in isolated uv environment
deepforest --input canopy.tif --output crowns.shp
```

---

## 8. Automated Test Verification

Forest OS enforces test-driven stability across containers, CLI wrappers, desktop entries, and style rules:

```bash
python3 -m unittest discover -s 05_Tests/ -p "test_*.py" -v
```

* `test_cli_wrappers.py`: 7 passed (bash syntax, CLI help flags, exit codes).
* `test_container_recipes.py`: 6 passed (Containerfile directives, package manifests).
* `test_desktop_launchers.py`: 7 passed (FreeDesktop validation, SVG icons, server HTTP 200).
* **Total: 20 passed, 0 failed.**

---

## 9. Code Quality & Governance

Forest OS adheres to rigorous engineering standards and STIM Layer 0 Governance:
* **Dense, Direct Prose:** Direct, capable, plain, and disciplined technical documentation. Zero marketing hyperbole, unnecessary fillers, or conversational tropes.
* **Biological Claims Discipline:** Biological analogies are framed strictly as working hypotheses with explicit kill criteria, never established physical mechanisms.
* **Substrate Purity:** Host preservation via containerized sidecars and user-space tooling. No uncontained system dependencies or global package pollution.
* **Two-Tier Execution Policy:** Tier 1 operations are autonomous and idempotent; Tier 2 operations (git push, rm, container rebuilds, external network sends) require explicit human confirmation.

---

## 10. Related Repositories

| Repository | Purpose |
|---|---|
| [stim-core](https://github.com/STIM-Protocol/stim-core) | Loop 1 thermodynamic metrics & Protocol 0 hardware root of trust |
| [stim-guard](https://github.com/STIM-Protocol/stim-guard) | Epistemic Sieve Membrane & Adrenaline Protocol |
| [mycelial-brain-mcp](https://github.com/STIM-Protocol/mycelial-brain-mcp) | Vector-graph persistent memory MCP server powering Forest OS |
| [white-paper](https://github.com/STIM-Protocol/white-paper) | Full STIM-AI v7.0011 architectural specification |
| [gpd-framework](https://github.com/STIM-Protocol/gpd-framework) | Get Physics Done: computational physics substrate |

---

*"The forest is not a resource; it is a relationship."* (Seventh Generation Principle)
