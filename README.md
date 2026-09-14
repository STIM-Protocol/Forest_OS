# Forest OS: Forestry & Arboriculture Workbench on Linux

[![STIM-AI](https://img.shields.io/badge/STIM--AI-v7.0011-1a4a2e?style=flat&labelColor=0d2818)](https://github.com/STIM-Protocol/stim-core)
[![Reference Implementation](https://img.shields.io/badge/Reference-Implementation_v1-brightgreen?style=flat)](https://github.com/STIM-Protocol/Forest_OS)
[![Workbench Port 5483](https://img.shields.io/badge/Workbench-Port_5483-7fbbb3?style=flat)](04_Configuration/desktop/forest_workbench.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-20_function_source_inventory_(not_a_fresh_run)-83c092?style=flat)](#automated-test-inventory)

Forest OS is a Linux-based operating environment for ecological land stewards, foresters, consulting arborists, and canopy researchers. It combines three things:

1. **A knowledge and file model** — the Heartwood/Cambium document pattern and a lifecycle-based vault layout (below).
2. **Agent workflows** — multi-agent coordination for research, ingestion, and maintenance.
3. **A forestry scientific workbench** — host user-space CLI tools, native desktop GIS, and containerized R/Fortran sidecars.

Forest OS is the **STIM Protocol Reference Implementation v1**. STIM-AI stands for **Stasis Through Inferred Memory** (canonical technical expansion, [seven-axiom specification v7.0011](https://github.com/STIM-Protocol/white-paper)). "Sovereign, Transparent, Immutable, Minimal" and "Standardized Truth & Immutable Memory" are engineering mnemonics used in some historical documents; they are not the protocol definition.

> **Scope statement.** This repository is *source*. Your personalized working copy (the "operating vault") lives elsewhere on your machine and is created by you, not by cloning. Forest OS is not a tested, installable distribution image; packaging an installable image is a future ambition, not a present deliverable. Claims here are documentation-level unless a dated verification receipt says otherwise.

---

## 1. Two trees: repository source vs. operating vault

Do not confuse these. The Git repository you are looking at is the **source** for scripts, protocols, and the workbench. The **operating vault** is your personal knowledge root where documents live and the lifecycle actually happens.

### Repository source (this repo)

```
Forest_OS/                       # this repository
├── 00_Core_Protocols/           # STIM specifications, world model, ingestion, sync
├── 01_Docs/                     # implementation notes, handoff packs, reports
│   ├── FILESYSTEM_MODEL.md      # canonical filesystem guide (start here)
│   ├── FORESTRY_WORKBENCH.md    # tool catalog source, packaging, evidence model
│   ├── VERIFICATION_AND_COMPATIBILITY.md  # what is tested, where, and what is not
│   └── DOCUMENT_AUTHORITY.md    # which document governs which topic
├── 02_Agent_Definitions/        # agent charters and registry
├── 03_Automation_Scripts/       # CLI wrappers, container builders, installers
├── 04_Configuration/            # container recipes, desktop launchers, workbench HTML
├── 05_Tests/                    # component test suites (see Section 8)
├── Documentation/               # historical copies (see 01_Docs/DOCUMENT_AUTHORITY.md)
├── Forest_OS/                   # historical protocol copies (see 01_Docs/DOCUMENT_AUTHORITY.md)
├── doc-200.md, doc-202.md, doc-210.md   # governance / cadence documents
├── CONTRIBUTING.md
└── LICENSE                      # MIT (repository code; bundled third-party tools keep their own licenses)
```

### Operating vault (your machine, example layout)

Documented in full in [01_Docs/FILESYSTEM_MODEL.md](01_Docs/FILESYSTEM_MODEL.md). Lifecycle stages:

```
Seed  →  Arboretum  →  Understory  →  Forest
```

On an operating machine these appear as directories such as:

```
~/Myceliate_Master/              # example operating-vault root (personalized, not part of this repo)
├── SEED_BANK/                   # Seed: intake, capture, downloads
├── ARBORETUM/                   # Arboretum: developing/active projects
├── UNDERSTORY/                  # Understory: supporting system & research functions
├── FOREST/                      # Forest: mature knowledge in numbered topic buckets
├── 00_CANOPY/                   # support zone: consolidated views (a projection, not a second database)
├── LIBRARY/                     # support zone: reference/archive material
└── COMPOST/                     # support zone: retired/superseded material
```

**Heartwood/Cambium pairing** is independent of the directory lifecycle: every knowledge item is a pair of a Heartwood content file (`.md`) and a Cambium metadata sidecar (`.jsonld`) sharing one stable ID. Lifecycle directories say *where an item is in its journey*; Heartwood/Cambium say *how it is represented*.

### Historical naming

Older documents in this repository (2026-04 era) used a **Greenhouse / Garden / Nursery / Laboratory** vocabulary. Those names are historical. The current lifecycle vocabulary is Seed → Arboretum → Understory → Forest, and support zones (Canopy, Library, Compost) sit alongside it. Historical references in `00_Core_Protocols/`, `Documentation/`, and `Forest_OS/` are retained for provenance and are labeled in [01_Docs/DOCUMENT_AUTHORITY.md](01_Docs/DOCUMENT_AUTHORITY.md). Some automation scripts still contain old path defaults; a script containing an old path is not evidence that the path is deployed — see [01_Docs/FILESYSTEM_MODEL.md](01_Docs/FILESYSTEM_MODEL.md) before changing any runtime behavior.

---

## 2. The forestry workbench in brief

The workbench is a static local web page (`04_Configuration/desktop/forest_workbench.html`) served by `forest-workbench` on port 5483. It carries a **33-entry tool catalog snapshot** across seven domains, field-pipeline recipe examples, a decision wizard, and a services overview.

* **Catalog source of truth:** [04_Configuration/forestry-tools.json](04_Configuration/forestry-tools.json) (33 tools + 3 supporting applications, reconciled with the `forest-tools` planner catalog). The HTML dataset mirrors it; where they disagree, the JSON governs.
* **Status labels are snapshots, not telemetry.** Badges such as "Ready" or "verified" in the HTML are documented snapshot values with a source and timestamp; nothing on the page polls a live service. See [01_Docs/FORESTRY_WORKBENCH.md](01_Docs/FORESTRY_WORKBENCH.md) for the evidence-grade model.
* **Packaging classes:** Tier 1 host user-space CLI (`uv tool`), Tier 2 native desktop GIS, Tier 3 container sidecars. These are packaging categories, not the seven STIM-AI axioms and not the separate action-permission tiers.

Full details: [01_Docs/FORESTRY_WORKBENCH.md](01_Docs/FORESTRY_WORKBENCH.md).

---

## 3. Quick start (source orientation)

This gets you reading and using the workbench from source. It does **not** install every scientific tool.

**Prerequisites:** Linux (Ubuntu LTS or interim releases, or Arch-based systems), Python 3.11+, and either Docker or Podman *only if* you want the Tier 3 containers. Native QGIS/GDAL and the Tier 1 CLI tools are separate installs — see [01_Docs/FORESTRY_WORKBENCH.md](01_Docs/FORESTRY_WORKBENCH.md).

```bash
# 1. Explore the source (no build needed)
$EDITOR 01_Docs/FILESYSTEM_MODEL.md
$EDITOR 04_Configuration/desktop/forest_workbench.html

# 2. Serve the workbench directly from the repo (no install)
python3 03_Automation_Scripts/forest-workbench --help   # show wrapper options

# 3. Optional, later: build container sidecars (large downloads, minutes of CPU)
./03_Automation_Scripts/build_containers.sh all

# 4. Optional, later: install desktop launchers.
#    This symlinks forest-workbench, forest-rstudio-launch, forest-sim-launch and
#    forest-deepforest-launch into ~/.local/bin and copies .desktop files.
./03_Automation_Scripts/install_desktop_launchers.sh
```

**What launcher installation does *not* do:** it does not put `forest-r` or `forest-sim` on your PATH, and it does not install DeepForest, BirdNET, pyDendron, QGIS, or the `forest-tools` planner. Those are separate installs documented in [01_Docs/FORESTRY_WORKBENCH.md](01_Docs/FORESTRY_WORKBENCH.md). The `forest-tools` planner referenced by the workbench wizard is a separately maintained dependency, not bundled in this repository.

```bash
# Once you have separately installed and PATH-configured the wrappers:
forest-r script.R        # run an R script inside forest-r-engine
forest-sim variants      # list Open-FVS variants
```

### Safety notes (read before serving)

* The current `forest-workbench` server and the container wrappers (`forest-r`, `forest-sim`) are **not demonstrably loopback-only** by default. The workbench binds all interfaces and the wrappers publish container ports without an explicit `127.0.0.1` host address. On any multi-user or networked machine, verify actual listening addresses (`ss -tlnp`) before assuming localhost-only access, or run behind a firewall you control.
* The RStudio wrapper uses a static default password and prints it to the terminal; override it via `RSTUDIO_PASSWORD` and treat it as non-secret only if you have changed it.
* Wrappers mount your **current working directory** into the container with write access. A container sidecar reduces dependency collisions; it is not a security boundary for files you mount, and it does not make the host immune to failures.
* Do not put credentials in any file under the mounted directory.

---

## 4. Desktop integration

Seven FreeDesktop launchers with SVG icons live in `04_Configuration/desktop/`:

| Launcher | Exec |
|---|---|
| Forest OS Workbench | `forest-workbench` |
| BirdNET Canopy Analyzer | `birdnet-gui` |
| pyDendron Tree-Ring Analysis | `pyDendron` |
| Forest RStudio Scientific Engine | `forest-rstudio-launch` |
| Forest-Sim Open-FVS Simulator | `forest-sim-launch` |
| DeepForest Canopy Detection | `forest-deepforest-launch` |
| QGIS Forestry Edition | `qgis %F` |

Creating a launcher creates a menu entry only; it is not evidence the underlying tool is installed.

---

## 5. Agents

The coordination model distinguishes **operating agents** (currently: Bodhi, Hermes, AG, M), **standards** (Sequoia — a constitutional arbiter *standard*, not a running process), and **historical/conceptual archetypes** (Quercus, Sylvan, Umbra/Kai, Arbor as described in doc-202). Detailed charters: [doc-202.md](doc-202.md) and [02_Agent_Definitions/](02_Agent_Definitions/). The older diagram in this README's history gave active roles to retired names; treat agent claims as configuration-dependent and verify against the live system before relying on them.

---

## 6. Platforms and compatibility

* **Current development host (owner-reported):** Ubuntu 26.04 LTS.
* **Support targets:** Ubuntu LTS and interim releases, and Arch Linux / Omarchy. Ubuntu uses LTS and interim releases; it is not a rolling distribution.
* **Not a tested claim:** host/guest parity, future-release parity, or "upgrades cannot break the scientific stack". Containerization reduces dependency-collision risk; shared-kernel, driver, and integration failure modes remain.
* Evidence, skipped checks, and unknowns: [01_Docs/VERIFICATION_AND_COMPATIBILITY.md](01_Docs/VERIFICATION_AND_COMPATIBILITY.md).

---

## 7. Reproducibility posture

Both container recipes currently use `:latest` base images and install GitHub dependencies without pinned revisions. The R install script fails if required packages cannot load, which is a useful guard, but its printed checks are not archived build receipts. Until image digests and package versions are recorded, treat builds as **repeatable-in-practice, not reproducible-by-pin**.

---

## 8. Automated test inventory

The repository contains 20 test functions across three modules (source inventory, not a fresh run result):

| Module | Test functions | What they inspect |
|---|---|---|
| `05_Tests/test_cli_wrappers.py` | 7 | bash syntax, CLI help flags, exit codes |
| `05_Tests/test_container_recipes.py` | 6 | Containerfile directives, package manifests |
| `05_Tests/test_desktop_launchers.py` | 7 | FreeDesktop validation, SVG icons, server HTTP 200 |

**What this does and does not establish:** these are component-level source/behavior checks. They are not an executed 20/20 run receipt, and they are not evidence that the five field-pipeline recipes have been validated end-to-end or that scientific outputs (canopy detection, biomass, tree rings, growth) are correct. Dated run receipts with passed/failed/skipped counts and host identity belong in [01_Docs/VERIFICATION_AND_COMPATIBILITY.md](01_Docs/VERIFICATION_AND_COMPATIBILITY.md) when they exist; absent receipts are recorded as unknown, not assumed passing.

```bash
python3 -m unittest discover -s 05_Tests/ -p "test_*.py"
```

> Note: the desktop test module can start the workbench web server on a fixed port and may skip if a validator is missing. Do not run full test discovery blindly on a machine where that port is in use.

---

## 9. Document authority

Where multiple copies of a protocol exist (e.g. `00_Core_Protocols/` vs `Forest_OS/`, `01_Docs/` vs `Documentation/`), [01_Docs/DOCUMENT_AUTHORITY.md](01_Docs/DOCUMENT_AUTHORITY.md) lists the authoritative copy, generated mirrors, and historical duplicates. Do not edit a historical copy expecting it to change behavior.

---

## 10. Related repositories

| Repository | Purpose |
|---|---|
| [stim-core](https://github.com/STIM-Protocol/stim-core) | Loop 1 thermodynamic metrics & Protocol 0 hardware root of trust |
| [stim-guard](https://github.com/STIM-Protocol/stim-guard) | Epistemic Sieve Membrane & Adrenaline Protocol |
| [mycelial-brain-mcp](https://github.com/STIM-Protocol/mycelial-brain-mcp) | Vector-graph persistent memory MCP server |
| [white-paper](https://github.com/STIM-Protocol/white-paper) | Full STIM-AI v7.0011 specification (canonical seven axioms) |
| [gpd-framework](https://github.com/STIM-Protocol/gpd-framework) | Get Physics Done: computational physics substrate |

---

*"The forest is not a resource; it is a relationship."* (Seventh Generation Principle)
