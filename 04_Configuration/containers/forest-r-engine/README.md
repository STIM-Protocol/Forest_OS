# forest-r-engine: Forest OS Scientific R Container Sidecar

**Document ID:** SPEC-CONTAINER-FOREST-R-001  
**Image Name:** `forest-r-engine`  
**Base Image:** `rocker/geospatial:latest`  
**Governance:** Doc-414 Compliant (Zero em dashes, strict claims discipline)  

---

## 1. Purpose & Scope

The `forest-r-engine` container sidecar isolates complex R-spatial and dendrochronological toolchains from the host operating system. R spatial packages (such as `lidR`, `TreeLS`, and `sf`) require precise ABI synchronization with underlying C/C++ libraries (`libgdal`, `libgeos`, `libproj`). Packaging these inside a container guarantees stability across host distribution upgrades (Ubuntu 26.04/26.10, Arch Linux) while completely preventing host package collisions.

---

## 2. Qualified Package Inventory

| Package | Domain | Capability | Upstream Source |
| :--- | :--- | :--- | :--- |
| **lidR** | Airborne LiDAR Processing | Point cloud classification, CHM generation, individual tree segmentation (Li, Dalponte, Silva). | `github.com/r-lidar/lidR` |
| **TreeLS** | Terrestrial Laser Scanning | Stem detection, cylinder fitting, DBH extraction from TLS and MLS point clouds. | `github.com/tiagodc/TreeLS` |
| **rGEDI** | Spaceborne Canopy Profiling | Processing and simulation of NASA GEDI spaceborne full-waveform LiDAR data. | `github.com/carlos-alberto-silva/rGEDI` |
| **BIOMASS** | Biomass & Carbon Stock | Pantropical and temperate allometric equations (Chave et al.), error propagation via Monte Carlo. | `github.com/umr-amap/BIOMASS` |
| **dplR** | Dendrochronology | Statistical cross-dating (COFECHA equivalent), spline detrending, chronology building. | `github.com/opendendro/dplR` |
| **allodb** | Standardized Allometry | Smithsonian ForestGEO allometric equations database with coordinate-based equation selection. | `github.com/forestgeo/allodb` |
| **ForestTools** | Crown Segmentation | Variable window filtering for treetop detection and watershed crown delineation. | `github.com/andrew-plowright/ForestTools` |
| **hemispheR** | Canopy Photography | Processing upward-looking fisheye photographs for Leaf Area Index (LAI) and canopy openness. | CRAN (`hemispheR`) |
| **treeclim** | Dendroclimatology | Bootstrapped response and correlation functions relating tree rings to instrumental climate records. | `github.com/chgrsz/treeclim` |

---

## 3. Building the Container Image

Build with Docker or Podman from this directory:

```bash
docker build -t forest-r-engine -f Containerfile .
```

Or execute via the Forest OS build orchestrator:

```bash
bash 03_Automation_Scripts/build_containers.sh r-engine
```

---

## 4. Usage Patterns

### Headless Script Execution
Execute an R script located in the host directory:
```bash
forest-r analysis.R
```

### Single Command Evaluation
Run an inline R expression:
```bash
forest-r -e 'library(lidR); cat("lidR version:", as.character(packageVersion("lidR")), "\n")'
```

### Interactive R Shell
Launch an interactive R terminal session with working directory mapped to the host folder:
```bash
forest-r
```

### Interactive RStudio Server Web IDE
Launch RStudio Server accessible from host browser at `http://localhost:8787`:
```bash
forest-r --web
```
Default credentials:
* **Username:** `rstudio`
* **Password:** `forest` (configurable via `RSTUDIO_PASSWORD` environment variable)
