# Forest OS: Master Project Handoff Pack & Genesis Specification

**Document ID:** SPEC-FOREST-OS-HANDOFF-001  
**Source:** AG-Orchestrator  
**Destination:** Forest OS Core Workspace (`/home/george/Myceliate_Master/ARBORETUM/Active/Forest_OS`)  
**Date:** September 11, 2026  
**Governance:** doc-414 compliant (zero em dashes)  

---

## 1. Executive Summary & Charter

Forest OS is a sovereign operating environment and digital workbench designed for forest ecologists, arborists, conservationists, and land stewards. It bridges two complementary pillars:

1. **Biomimetic Knowledge Organism:** A decentralized file system architecture using natural forest metabolic tiers (Spores for task packets, Cambium for autonomous edits, Heartwood for immutable versioned truth, Compost for ephemeral logs, and Greenhouse for staging).
2. **Empirical Forestry Workbench:** A curated, zero-bloat distribution of open-source software for tree canopy analysis, drone and satellite LiDAR processing, tree ring analysis, forest growth simulation, bioacoustics, and spatial inventory.

This handoff pack transfers all architectural discoveries, tool qualification catalogs, multi-distro installation pipelines, and empirical verification results established in the Orchestrator into the dedicated Forest OS project space.

---

## 2. The Forestry Open-Source Landscape (Agent M Empirical Study)

Agent M (Gemini Spark) completed a comprehensive research run evaluating 33 prominent open-source forestry tools against four strict production criteria: Active Maintenance, True FOSS Licensing, Linux Native Viability, and Standalone Utility.

All 33 evaluated tools have been promoted into the active catalog (`forest-tools/catalog/forestry_tools.json`) across seven functional domains:

### Domain 1: Canopy & Aerial Tree Detection
* **DeepForest:** Deep learning model (RetinaNet) for individual tree crown detection from airborne RGB imagery. Qualified for Tier 1 CLI (`uv tool`).
* **Detectree2:** Mask R-CNN pixel-level segmentation for tree crown delineation. Qualified for Tier 1 CLI.

### Domain 2: Point Clouds & Forest LiDAR
* **CloudCompare:** High-performance 3D point cloud and mesh processing software. Qualified for Tier 2 Desktop GUI (native distro packages/Flatpak).
* **pytlidar:** Python package for reading and processing terrestrial and airborne LiDAR data. Qualified for Tier 1 CLI.
* **3dfin:** 3D Forest Inventory tool for tree detection and cylinder fitting on LiDAR. Qualified for Tier 1 CLI.
* **lidR:** The standard R framework for forestry airborne laser scanning. Qualified for Tier 3 Container (`forest-r-engine`).
* **TreeLS:** Terrestrial Laser Scanning (TLS) point cloud processing in R (tree stem detection, DBH measurement). Qualified for Tier 3 Container (`forest-r-engine`).
* **rGEDI:** NASA GEDI spaceborne full-waveform LiDAR metrics in R. Qualified for Tier 3 Container (`forest-r-engine`).

### Domain 3: Tree Physiology, Rings, & Biomass
* **pyDendron:** Modern Python crossdating and tree-ring analysis software. Qualified for Tier 1 CLI (`uv tool`).
* **dplR:** Dendrochronology Program Library in R (ring-width chronology, climate response). Qualified for Tier 3 Container (`forest-r-engine`).
* **BIOMASS:** Robust biomass and carbon stock estimation using pantropical allometry in R. Qualified for Tier 3 Container (`forest-r-engine`).
* **allodb:** Standardized tree biomass allometric equations database in R. Qualified for Tier 3 Container (`forest-r-engine`).

### Domain 4: Tree Growth, Yield, & Simulation
* **FVS (Forest Vegetation Simulator):** US Forest Service individual-tree growth and yield simulation model. Qualified for Tier 3 Container (`forest-sim`).
* **microfvs:** Lightweight standalone C port of FVS engine. Qualified for Tier 3 Container (`forest-sim`).
* **Capsis:** Modular Java forestry simulation platform (growth, dynamics, wood quality). Qualified for Tier 3 Container.
* **Landis-II:** Spatially dynamic forest landscape disturbance and succession model (.NET core). Qualified for Tier 3 Container.
* **Sortie-ND:** Neighborhood dynamics, spatially explicit forest succession model. Qualified for Tier 3 Container.

### Domain 5: Field Inventory, GIS, & Mapping
* **QGIS:** The premier open-source desktop Geographic Information System. Qualified for Tier 2 Desktop GUI.
* **GDAL:** Geospatial Data Abstraction Library for raster and vector translation. Qualified for Tier 1 CLI / Tier 2 native.
* **OpenForis Collect / Arena:** FAO mobile and web field survey collection platform. Qualified for Tier 3 Container / Web Service.

### Domain 6: Acoustic & Biodiversity Monitoring
* **BirdNET-Analyzer:** Deep learning acoustic bird identification engine from raw audio. Qualified for Tier 1 CLI (`uv tool`).
* **BatDetect2:** Deep learning bat echolocation call detection and classification. Qualified for Tier 1 CLI (`uv tool`).
* **scikit-maad:** Quantitative acoustic ecology and soundscape analysis in Python. Qualified for Tier 1 CLI (`uv tool`).

### Domain 7: Urban Forestry & Tree Health
* **i-Tree Open:** Ecosystem service calculations and urban canopy assessment modules. Qualified for Tier 3 Container.
* **OpenTreeMap:** Collaborative crowdsourced urban tree mapping engine. Qualified for Tier 3 Container.

---

## 3. The Three-Tier Zero-Bloat Packaging Architecture

To prevent dependency collisions, system library bloat, and broken builds, Forest OS implements a strict three-tier architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Forest OS Host System                           │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 1: Host User-Space CLI Tools                                      │
│   • Isolated Python environments via `uv tool install --python 3.11`   │
│   • Binaries in `~/.local/bin/` (DeepForest, BirdNET, pyDendron)       │
│   • Zero interference with host system packages or system Python       │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Native Desktop GUI & System GIS                                │
│   • Managed by distro package manager (APT, Pacman) or Flatpak         │
│   • Native OpenGL/Vulkan acceleration (QGIS, CloudCompare)             │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Scientific Container Sidecars (Podman / Docker)                │
│   • `forest-r-engine`: Complete R spatial stack (lidR, TreeLS, GEDI)   │
│   • `forest-sim`: Legacy simulation platforms (FVS, microfvs, Capsis)  │
│   • Eliminates C-shared library breakages on rolling Linux releases    │
└────────────────────────────────────────────────────────────────────────┘
```

### Key Technical Safeguards:
1. **Isolated Python Runtime:** Python tools are installed using `uv tool install --python 3.11 <package>`, pinning their internal virtualenvs to a standalone Python 3.11 binary. This protects tools against system Python deprecations, Debian PEP 668 externally managed environment locks, and rolling glibc changes.
2. **Container Isolation for R & Fortran:** R spatial packages depend heavily on exact versions of `libgdal`, `libproj`, and `libgeos`. Packaging these inside a single reproducible container (`forest-r-engine`) guarantees stability across host distribution upgrades.

---

## 4. Cross-Distribution Neutrality & Forward Compatibility

Forest OS is engineered for total cross-distribution parity across Linux environments:

* **Current Verified Host:** Ubuntu 26.04.1 LTS (Resolute Raccoon), Linux kernel 7.0.0-31-generic.
* **Upcoming Target:** Ubuntu 26.10 with Linux kernel 7.3.
* **Alternative Target:** Arch Linux / Omarchy rolling environment.

Because Tier 1 tools run in user-space via `uv tool` and Tier 3 tools run in container runtimes, upgrades to the host operating system, glibc, or Linux kernel cannot break the scientific stack.

The `forest-tools` CLI planner (`core/planner.py` and distro adapters) detects the host platform automatically and generates distribution-accurate declarative install plans:
```bash
forest-tools plan --all-ready
```

---

## 5. Live Host Verification Status (Completed)

All primary Tier 1 and Tier 2 tools have been installed and empirically verified on the current machine:

| Tool | Tier | Target Executable | Installation Method | Verification Result |
| :--- | :--- | :--- | :--- | :--- |
| **BirdNET-Analyzer** | Tier 1 CLI | `birdnet-analyze` | `uv tool install --python 3.11 birdnet-analyzer` | PASS (`--help` returned code 0) |
| **DeepForest** | Tier 1 CLI | `deepforest` | `uv tool install --python 3.11 deepforest` | PASS (v2.1.0 CLI operational) |
| **pyDendron** | Tier 1 CLI | `pyDendron` | `uv tool install --python 3.11 pydendron` | PASS (v1.7.5 CLI operational) |
| **QGIS** | Tier 2 GUI | `qgis` | Native APT package | PASS (QGIS 3.42.3 active) |
| **GDAL** | Tier 1/2 | `gdalinfo` | Native APT package (`gdal-bin`) | PASS (GDAL 3.10.2 active) |

Automated verification tests are integrated into `forest-tools`:
```bash
forest-tools verify audio
forest-tools verify canopy-imagery
forest-tools verify rings-and-biomass
forest-tools verify field
```

---

## 6. Repository Index & Relevant Paths

### Core Documentation
* Handoff Pack: `ARBORETUM/Active/Forest_OS/01_Docs/FOREST_OS_PROJECT_HANDOFF_PACK.md`
* Agent M Research Report: `ARBORETUM/Active/Forest_OS/01_Docs/M_REPORT_FORESTRY_OSS_001.md`
* Tooling Taxonomy & Specs: `ARBORETUM/Active/Forest_OS/01_Docs/FORESTRY_TOOLS_TAXONOMY_AND_RESEARCH.md`
* Agent M Research Brief: `ARBORETUM/Active/Forest_OS/01_Docs/RESEARCH_BRIEF_FORESTRY_TOOLS.md`
* Core Forest OS Specs: `ARBORETUM/Active/Forest_OS/01_Docs/FOREST_OS_IMPLEMENTATION.md`

### Tool Management Engine (`forest-tools`)
* Location: `ARBORETUM/Active/Omarchy Migration Preparedness/forest-tools/`
* Catalog: `forest-tools/catalog/forestry_tools.json`
* Ubuntu Adapter: `forest-tools/adapters/ubuntu.py`
* Execution Planner: `forest-tools/core/planner.py`
* CLI Interface: `forest-tools/cli.py`
* Automated Tier 1 Installer: `scripts/install_forester_tier1.sh`

### Orchestration & Fleet Links
* Fleet Router: `ARBORETUM/Active/AG-Orchestrator/ROUTER.md` (domain: `product-forest-os`)
* Project Symlink: `ARBORETUM/Active/AG-Orchestrator/projects/08_forest_os`
* Fleet Conversation Registry: `UNDERSTORY/AG_Instructions/conversations.json` (`forest-os-canonical`)

---

## 7. Immediate Roadmap & Sprint Backlog

Now that the foundation, catalog, and verification are established, the next development sprint in the Forest OS chat space will tackle:

1. **Sprint 1: Tier 3 Container Definitions (Podman / Docker)**
   * Create `Containerfile.forest-r-engine` containing Ubuntu base, R-spatial libraries, `lidR`, `TreeLS`, `rGEDI`, `BIOMASS`, and `dplR`.
   * Create `Containerfile.forest-sim` containing compiled FVS and `microfvs` with CLI runners.
   * Add container launch wrappers to `~/.local/bin/` so users can run `forest-r <script>` directly from the host.

2. **Sprint 2: Desktop Integration & Field Launchers**
   * Create `.desktop` entries for GUI-capable user-space tools (e.g. `birdnet-gui`, `pyDendron`).
   * Configure desktop menu category: `Forestry & Ecology`.

3. **Sprint 3: Forest OS Spore Queue Automated Pipeline**
   * Connect inbound drone orthomosaics and sound recordings into `FOREST/Spore_Queue/`.
   * Trigger automatic tree crown detection via `deepforest` and species identification via `birdnet-analyze`.
   * Write structured JSON-LD reports into Cambium / Heartwood layers.
