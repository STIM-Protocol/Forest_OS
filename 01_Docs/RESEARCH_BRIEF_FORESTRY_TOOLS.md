# Research Brief: Open Source Forestry, Arboriculture, and Canopy Ecology Tooling

**Document ID:** SPEC-FOREST-OS-TOOLKIT-001  
**Target Substrates:** Forest OS / Omarchy Workstation  
**Author:** AG-Orchestrator  
**Governance:** doc-414 compliant (zero em dashes)  

---

## 1. Directive Objective

Curate, evaluate, and package the definitive suite of open-source software, models, and computational utilities for tree stewards, arborists, foresters, and canopy researchers inside **Forest OS**.

---

## 2. Packaging Architecture: Zero-Bloat Deployment

To prevent polluting the Arch Linux / Omarchy root filesystem, Forest OS implements a 3-tier delivery strategy:

```
[ Forest OS User / Field Steward ]
                 │
  ┌──────────────┼──────────────┐
  ▼              ▼              ▼
[ Tier 1 ]     [ Tier 2 ]     [ Tier 3 ]
Host CLI /     Desktop GUI    Containerized
Lightweight    Workstations   Runtimes
(PDAL, Python) (QGIS, QField) (Docker/Podman)
```

1. **Tier 1: Host Native CLI (Fast & Lightweight)**
   * Single binaries, standard Linux geospatial tools (`gdal`, `pdal`, `lasview`).
   * Managed via `uv` in dedicated virtual environments (e.g. `deepforest`, `pyfia`, `pyrealm`).
2. **Tier 2: Desktop Workstation GUIs (Visual Exploration)**
   * `QGIS` with specialized forestry plugins (`TreeEyed`, `3DFin`, `QFieldSync`).
   * `CloudCompare` with vegetation classification plugins (`CSF`, `CANUPO`).
   * `pyDendron` for tree ring imaging and cross-dating.
3. **Tier 3: Containerized Scientific Engines (Zero Host Pollution)**
   * `forest-r-engine`: Complete R geospatial stack (`lidR`, `TreeLS`, `rGEDI`, `hemispheR`, `dplR`).
   * `webodm`: Local GPU-accelerated photogrammetry for UAV forest canopy maps.
   * `forest-sim-engine`: Complex growth and disturbance simulators (`FVS`, `LANDIS-II`, `Cell2Fire`).

---

## 3. Comprehensive Tool Registry & Evaluation

See [`FORESTRY_TOOLS_TAXONOMY_AND_RESEARCH.md`](file:///home/george/Myceliate_Master/ARBORETUM/Active/Forest_OS/01_Docs/FORESTRY_TOOLS_TAXONOMY_AND_RESEARCH.md) for full benchmark and evaluation details.
