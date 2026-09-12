# Forest OS: Open Source Forestry, Arboriculture, and Canopy Toolkit

**Document ID:** SPEC-FOREST-OS-RESEARCH-002  
**Target Platform:** Forest OS on Omarchy (Arch Linux Rolling Substrate)  
**Author:** AG-Orchestrator  
**Governance:** doc-414 compliant (zero em dashes)  

---

## 1. Overview & Vision

Forest OS is designed to be the sovereign computational operating system for ecological land stewards, foresters, consulting arborists, and canopy scientists. 

To turn Forest OS into an indispensable field and lab workstation without turning the underlying Arch Linux system into an unmaintainable sprawl of conflicting packages, we structure these tools into a **Three-Tier Anti-Bloat Architecture**:
* **Tier 1 (Host CLI & Micro-Packages):** Fast, compiled C/C++ binaries, standard GDAL/PDAL point cloud filters, and standalone Python CLI tools managed in isolated `uv` virtual environments.
* **Tier 2 (Workstation Desktop GUI):** Native Qt/Wayland desktop software (QGIS with forestry plugins, CloudCompare, pyDendron) installed via system packages or user Flatpaks.
* **Tier 3 (Scientific Container Engines):** Specialized runtimes (R-spatial, heavy Fortran/Java simulation engines, WebODM photogrammetry) packaged as Docker/Podman containers that mount host working directories and leave the root filesystem untouched.

---

## 2. Comprehensive Tool Taxonomy

### Category 1: 3D Forest Inventory, LiDAR, & Tree Reconstruction

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **lidR** | Airborne LiDAR processing, ground classification, canopy height model (CHM) generation, and individual tree segmentation. | R / C++ (Rcpp) | Tier 3 (Container) | `github.com/Jean-Romain/lidR` |
| **TreeLS** | Terrestrial Laser Scanning (TLS) point cloud analysis, automated stem detection, DBH measurement, and tree isolation. | R / C++ | Tier 3 (Container) | `r-universe.dev/packages/TreeLS` |
| **3DFin** | Automated 3D forest inventory from TLS/MLS/photogrammetry; computes height, DBH, and tree location with QGIS/CloudCompare plugins. | Python / C++ | Tier 2 (QGIS Plugin) | `github.com/3DFin/3DFin` |
| **TreeSeg** | Near-automatic extraction of individual tree point clouds from large-area LiDAR by segmenting stems and crowns. | C++ / PCL | Tier 1 (Host CLI) | `github.com/apburt/treeseg` |
| **TreeQSM** | Quantitative Structure Modeling; reconstructs 3D tree geometry, branch architecture, and volume using cylinder fitting. | MATLAB / Python | Tier 3 (Container) | `github.com/InverseTampere/TreeQSM` |
| **PyTLidar** | Modern Python alternative to TreeQSM with GUI; generates volumetric branch models from TLS point clouds. | Python | Tier 1 (`uv` CLI/GUI) | `ecoevorxiv.org` / PyTLidar |
| **rTwig** | Optimizes QSM volume estimation by correcting branch overestimation using empirical branch diameter measurements. | R | Tier 3 (Container) | `github.com/TreeQSM/rTwig` |
| **PDAL** | Point Data Abstraction Library; industrial pipeline engine for translating, filtering, and cropping massive LAS/LAZ point clouds. | C++ | Tier 1 (Host Native) | `github.com/PDAL/PDAL` |

---

### Category 2: Machine Learning, Computer Vision, & Canopy Crown Detection

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **DeepForest** | Pre-trained deep learning (PyTorch) model for individual tree crown detection from RGB aerial and drone imagery. | Python / PyTorch | Tier 1 (`uv` CLI) | `github.com/weecology/DeepForest` |
| **pycrown** | Fast tree top detection and crown delineation from raster Canopy Height Models using Cython and Numba. | Python / Cython | Tier 1 (`uv` CLI) | `github.com/manaakiwhenua/pycrown` |
| **TreeEyed** | QGIS AI plugin integrating DeepForest and HighResCanopyHeight for automated tree monitoring in GIS maps. | Python / QGIS | Tier 2 (QGIS Plugin) | `github.com/afruizh/TreeEyed` |
| **ForestTools** | Detects individual treetops via variable window filters and segments crowns via marker-controlled watersheds. | R | Tier 3 (Container) | `github.com/andrew-plowright/ForestTools` |
| **rGEDI** | Direct interface to NASA GEDI spaceborne lidar data; extracts vertical canopy profiles and models full-waveform metrics. | R / C | Tier 3 (Container) | `github.com/carlos-alberto-silva/rGEDI` |

---

### Category 3: Dendrochronology, Wood Anatomy, & Growth Rings

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **dplR** | The canonical open-source standard for dendrochronology; statistical cross-dating, detrending, and climate chronology building. | R | Tier 3 (Container) | `github.com/opendendro/dplR` |
| **dplPy** | Modern Python port of dplR under the OpenDendro project; handles standard Tucson/TRiDaS formats and statistical analysis. | Python | Tier 1 (`uv` CLI) | `github.com/opendendro/dplPy` |
| **pyDendron** | Web-based and desktop GUI for interactive tree ring dating, measurement visualization, and sample cross-dating. | Python | Tier 2 (Desktop App) | `pypi.org/project/pyDendron` |
| **TRAS** | Tree Ring Analyzer Suite; automatic ring boundary delineation and manual correction on high-resolution wood cross-sections. | Python / OpenCV | Tier 1 (`uv` CLI) | `arxiv.org` (TRAS Suite) |
| **treeclim** | Modeling climate-growth relationships using response functions and seasonal correlation analyses. | R | Tier 3 (Container) | `CRAN.R-project.org/package=treeclim` |

---

### Category 4: Forest Growth, Silviculture, & Disturbance Simulators

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **FVS / pyFVS** | USDA Forest Vegetation Simulator; individual-tree growth-and-yield simulation under silvicultural treatment scenarios. | Fortran / Python / C | Tier 3 (Container) | `github.com/USDAForestService/ForestVegetationSimulator` |
| **microfvs** | Modern REST API wrapper for FVS developed by Vibrant Planet for scalable cloud/local growth simulations. | Python / Docker | Tier 3 (Container) | `github.com/Vibrant-Planet-Open-Science/microfvs` |
| **LANDIS-II** | Landscape-scale forest succession, wildfire disturbance, insect outbreaks, and seed dispersal modeling over centuries. | C# / .NET Core | Tier 3 (Container) | `github.com/LANDIS-II-Foundation` |
| **Capsis** | Open simulation platform for silvicultural modeling (e.g. mixed species growth, crown competition, thinning regimes). | Java | Tier 3 (Container) | `capsis.cirad.fr` |
| **Cell2Fire** | Spatial cell-based wildfire growth simulator; models fire spread across terrain and fuel beds to guide prescribed burns. | C++ / Python | Tier 3 (Container) | `github.com/cell2fire/cell2fire` |
| **FMT** | Forest Management Tool; high-performance C++ library for solving forest planning and sustainable harvest scheduling models. | C++ | Tier 1 (Host CLI) | `github.com/Bureau-du-Forestier-en-chef/FMT` |

---

### Category 5: Field Arboriculture, Urban Forestry, & Canopy Health

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **QField / QFieldSync** | Offline mobile data collection for field foresters and tree risk inspectors; synchronizes seamlessly with desktop QGIS. | C++ / Qt / Android | Tier 2 (Desktop Sync) | `github.com/opengisch/QField` |
| **OpenTreeMap** | Collaborative platform for municipal and community urban tree inventories, health tracking, and ecosystem service benefits. | Python / Django / GIS | Tier 3 (Container) | `github.com/otm-legacy/otm-legacy` |
| **hemispheR** | Automated processing of hemispherical (fisheye) photography to compute Leaf Area Index (LAI) and canopy openness. | R | Tier 3 (Container) | `CRAN.R-project.org/package=hemispheR` |
| **CanopyWatch** | Open tool for mapping urban tree canopy equity, analyzing shade cover against heat stress and neighborhood metrics. | TypeScript / React | Tier 1 (Web / Node) | `github.com/meyeringn/canopy-watch` |
| **SylvCiT** | Decision-support software helping urban foresters plan functional tree diversity and climatic resilience in cities. | Python / GIS | Tier 2 (GUI) | `auf.isa-arbor.com` |

---

### Category 6: Bioacoustics, Biodiversity Tracking, & Photogrammetry

| Tool | Core Capability | Language / Stack | Forest OS Tier | Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **BirdNET-Analyzer** | Automated acoustic detection and classification of avian vocalizations in forest canopies from field audio recorders. | Python / TFLite | Tier 1 (`uv` CLI) | `github.com/kahst/BirdNET-Analyzer` |
| **scikit-maad** | Quantitative bioacoustics package for calculating acoustic indices (entropy, biophony vs. anthrophony) in forest soundscapes. | Python | Tier 1 (`uv` CLI) | `github.com/scikit-maad/scikit-maad` |
| **pyinaturalist** | API client for iNaturalist; pulls verified botanical occurrences, phenology records, and species distributions into GIS layers. | Python | Tier 1 (`uv` CLI) | `github.com/pyinat/pyinaturalist` |
| **WebODM** | OpenDroneMap workstation; processes raw drone imagery into orthomosaics, Digital Surface Models (DSM), and 3D forest point clouds. | Python / C++ / Node | Tier 3 (Container) | `github.com/OpenDroneMap/WebODM` |
| **CloudCompare** | 3D point cloud editor equipped with the Cloth Simulation Filter (CSF) for bare-earth extraction and CANUPO for 3D vegetation classification. | C++ / Qt | Tier 2 (Native Desktop) | `github.com/CloudCompare/CloudCompare` |

---

## 3. The Forest OS Packaging Plan

To install and maintain these tools without bloating the host system:

### 1. The `forest-geo` CLI Subsystem (Host Native)
Run via native Arch packages and Mise:
```bash
# Core C/C++ libraries
pacman -S gdal pdal cloudcompare qgis

# Isolated Python CLI tools via uv
uv tool install deepforest
uv tool install pyfia
uv tool install birdnet-analyzer
uv tool install dplpy
```

### 2. The `forest-r-engine` Container (Zero Host R Pollutions)
Instead of compiling 80 different R geospatial libraries on Arch Linux (which often breaks across rolling GCC updates), Forest OS runs an optimized Docker/Podman container:
* Base Image: `rocker/geospatial:latest`
* Pre-installed packages: `lidR`, `TreeLS`, `rGEDI`, `ForestTools`, `hemispheR`, `dplR`, `BIOMASS`, `treeclim`.
* CLI Wrapper: A host shell script `forest r <script.R>` that mounts the current working directory and executes inside the container in milliseconds.

### 3. The `forest-odm` Photogrammetry Worker
* WebODM runs as a local Docker compose profile.
* Enabled only when the user is actively processing drone imagery batches.
* GPU acceleration passed through via NVIDIA Container Toolkit or OpenCL.
