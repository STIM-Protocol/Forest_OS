# **Research Report: Open Source Forestry & Arboriculture Tooling for Forest OS**

**Document ID:** M-REPORT-FORESTRY-OSS-001 **Target Platform:** Forest OS (Arch Linux / Omarchy) **Reference Document:** ARBORETUM/Active/Spark-Agent\_M/M\_RESEARCH\_BRIEF\_OPEN\_SOURCE\_FORESTRY.md **Governance:** doc-414 compliant (zero em dashes)

## **Executive Summary & Architectural Packaging Strategy**

Forest OS demands sovereign, reproducible computational ecology workflows. To balance high-throughput analytical capabilities with operating system hygiene on an Arch Linux base, tooling is classified into three deployment tiers:

> * **Tier 1 (Host CLI / Native):** High-performance C++, Python, or Rust binaries with minimal, stable dependency graphs. Installed natively via Arch User Repository (AUR) PKGBUILDs or isolated Python virtual environments (pipx / uv).  
> * **Tier 2 (Desktop GUI):** Interactive visualization environments (QGIS plugins, native Qt6 applications, desktop viewers).  
> * **Tier 3 (Dockerized Sidecar / Podman):** R environments with extensive geospatial dependencies (GDAL/GEOS/PROJ), legacy Java runtimes, or complex C/Fortran legacy stacks. Containerization prevents host system library collision and dependency drift.

## **1\. 3D Forest Inventory & LiDAR**

### **Terrestrial Laser Scanning (TLS) Stem Detection & DBH**

#### **TreeLS**

> * **Repository & License:** [tiagodc/TreeLS](https://github.com/tiagodc/TreeLS) | GPL-3.0  
> * **Standout Capability:** Native integration with R's lidR infrastructure for automated Hough transform and RANSAC circle/cylinder fitting directly on point clouds, extracting stem curves, taper, and DBH from unorganized terrestrial and mobile laser scans.  
> * **Dependencies:** R (\>= 3.5), C++ (Rcpp, RcppArmadillo), spatial libraries (lidR, sf, raster).  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar). Complex geospatial C++ compile chains in R are best isolated in a dedicated R-spatial container.  
> * **Maintenance & Bottlenecks:** Upstream development on CRAN is sporadic; primary releases and bug fixes occur directly in the GitHub repository. Requires synchronized GDAL/PROJ versions.

#### **3DFin (3D Forest Inventory)**

> * **Repository & License:** [3DFin/3DFin](https://github.com/3DFin/3DFin) | GPL-3.0  
> * **Standout Capability:** Point cloud processing optimized specifically for personal laser scanning (PLS) and terrestrial laser scanning (TLS). Provides end-to-end automated stem detection, tree segmentation, and DBH extraction via an intuitive GUI or batch command line.  
> * **Dependencies:** Python 3.9+, CloudCompare / PCL bindings, NumPy, SciPy, Open3D, PyQt5/6.  
> * **Forest OS Suitability:** Tier 1 (Host CLI via uv) or Tier 2 (Desktop GUI).  
> * **Maintenance & Bottlenecks:** Actively developed by research groups at the University of Cordoba and Forestry research partners; relies heavily on NumPy/Open3D compatibility windows.

#### **TreeSeg**

> * **Repository & License:** [apburt/treeseg](https://github.com/apburt/treeseg) | GPL-3.0  
> * **Standout Capability:** Near-ground and canopy point cloud extraction designed for large-scale TLS plots. Uses generic tree architecture priors to dissect dense multi-return point clouds into discrete individual tree point clouds without requiring prior aerial crown boundaries.  
> * **Dependencies:** C++11, Point Cloud Library (PCL \>= 1.8), Eigen3, Boost.  
> * **Forest OS Suitability:** Tier 1 (Host CLI). Native compilation via CMake produces standalone binaries (treeseg, rxp2pcd) that execute with high performance on Arch Linux.  
> * **Maintenance & Bottlenecks:** Stable academic codebase; requires tracking modern PCL API changes when compiling on rolling-release Arch toolchains.

### **Quantitative Structure Modeling (QSM)**

#### **TreeQSM**

> * **Repository & License:** [InverseTampere/TreeQSM](https://github.com/InverseTampere/TreeQSM) | GNU GPL-3.0  
> * **Standout Capability:** The canonical reference standard for cylindrical Quantitative Structure Models. Reconstructs topological branch ordering, parent-child branch geometry, wood volume, and aboveground biomass (AGB) distributions from segmented TLS point clouds.  
> * **Dependencies:** MATLAB (original) or GNU Octave / MATLAB Compiler Runtime (MCR).  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar running Octave/headless MCR).  
> * **Maintenance & Bottlenecks:** MATLAB runtime requirement has historically hindered automated Linux pipelines, driving community migration to native Python and R wrappers.

#### **SimpleForest**

> * **Repository & License:** [SimpleForest / Jan Hackenberg](https://github.com/SimpleForest) | GPL-3.0  
> * **Standout Capability:** CloudCompare plugin and standalone C++ tool utilizing sphere-following and Dijkstra clustering algorithms to build reverse-pipe QSMs, featuring automatic correction for occlusion and ray-tracing validation.  
> * **Dependencies:** C++, CloudCompare Core, PCL, Qt5.  
> * **Forest OS Suitability:** Tier 2 (Desktop GUI via CloudCompare plugin) or Tier 1 (Host CLI).  
> * **Maintenance & Bottlenecks:** Tied to specific CloudCompare plugin APIs. Requires rebuilding when CloudCompare undergoes major version transitions.

#### **PyTLidar**

> * **Repository & License:** [Landscape-CV/PyTLidar](https://github.com/Landscape-CV/PyTLidar) | MIT License  
> * **Standout Capability:** Native Python implementation and wrapper around modern QSM algorithms, enabling direct pipeline integration with standard Python scientific ecosystems (PyTorch, SciPy, Open3D) without proprietary runtime dependencies.  
> * **Dependencies:** Python 3.10+, NumPy, Numba, Open3D, Laspy.  
> * **Forest OS Suitability:** Tier 1 (Host CLI via pipx or standard Python environment).  
> * **Maintenance & Bottlenecks:** Newer open-source initiative under active expansion; requires checking JOSS/review issues for API stability.

#### **rTwig**

> * **Repository & License:** [aidanmorales/rTwig](https://github.com/aidanmorales/rTwig) | GPL-3.0  
> * **Standout Capability:** Corrects structural overestimation in QSM cylinder models by applying empirical twig diameter databases and botanical pipe models (Real Twig method), dramatically refining tree volume and surface area estimates.  
> * **Dependencies:** R (\>= 4.0), data.table, Rcpp, rgl.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * **Maintenance & Bottlenecks:** Actively maintained on CRAN and GitHub with comprehensive unit tests and reproducible vignettes.

### **Airborne LiDAR Processing & Canopy Height Models**

#### **lidR**

> * **Repository & License:** [r-lidar/lidR](https://github.com/r-lidar/lidR) | GPL-3.0  
> * **Standout Capability:** Forest inventory engine capable of processing terabyte-scale airborne LiDAR point clouds. Features out-of-core catalog processing, individual tree segmentation (Li, Dalponte, Silva algorithms), pit-free Canopy Height Model (CHM) generation, and digital terrain modeling.  
> * **Dependencies:** R, C++ (Rcpp), GDAL, GEOS, PROJ, spatial ecosystem.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * **Maintenance & Bottlenecks:** Highly active upstream governance by Jean-Romain Roussel. Fastidious codebase, but host installation on Arch can be brittle due to upstream rolling upgrades of proj and gdal.

#### **PDAL (Point Data Abstraction Library)**

> * **Repository & License:** [PDAL/PDAL](https://github.com/PDAL/PDAL) | Apache-2.0 / BSD  
> * **Standout Capability:** The GDAL equivalent for point clouds. Allows streaming JSON-based pipeline filters for ground classification (SMRF/CSF), height-above-ground normalization, voxel filtering, and rasterization at native C++ execution speeds.  
> * **Dependencies:** C++17, GDAL, GeoTIFF, LibLAS, Python bindings.  
> * **Forest OS Suitability:** Tier 1 (Host CLI). Available directly in Arch Linux extra repository (pacman \-S pdal).  
> * **Maintenance & Bottlenecks:** Robust, industry-standard governance under OSGeo. Negligible technical debt.

## **2\. Canopy Computer Vision & Deep Learning**

### **Individual Tree Crown (ITC) Detection**

#### **DeepForest**

> * **Repository & License:** [weecology/DeepForest](https://github.com/weecology/DeepForest) | MIT License  
> * **Standout Capability:** Pre-trained Retinanet neural network trained on millions of individual tree crowns across diverse forest biomes worldwide. Detects bounding boxes and outlines of individual tree crowns directly from airborne RGB drone orthomosaics with zero retraining required for common canopy types.  
> * **Dependencies:** Python 3.9+, PyTorch, TorchVision, Rasterio, Albumentations, Shapely.  
> * **Forest OS Suitability:** Tier 1 (Host CLI via dedicated PyTorch venv with CUDA support).  
> * **Maintenance & Bottlenecks:** High-velocity project backed by Weecology Lab (University of Florida). Well-funded and actively maintained.

#### **PyCrown**

> * **Repository & License:** [manaakiwhenua/pycrown](https://github.com/manaakiwhenua/pycrown) | GPL-3.0  
> * **Standout Capability:** Fast individual tree segmentation combining CHMs derived from airborne LiDAR with orthorectified multi-band optical imagery, delineating crowns via watershed, regional growth, and planar projection routines.  
> * **Dependencies:** Python 3, GDAL, NumPy, SciPy, Rasterio, Scikit-Image.  
> * **Forest OS Suitability:** Tier 1 (Host CLI via container or locked conda/uv environment).  
> * **Maintenance & Bottlenecks:** Maintenance has slowed; legacy GDAL Python bindings require careful pin-setting on modern rolling Linux systems.

#### **TreeEyed**

> * **Repository & License:** [afruizh/TreeEyed](https://github.com/afruizh/TreeEyed) | GPL-3.0  
> * **Standout Capability:** Direct QGIS plugin integration bridging modern machine learning models (YOLO, DeepForest, SAM) directly onto the GIS canvas, allowing field arborists to click-to-segment canopies over raster layers.  
> * **Dependencies:** QGIS 3.x Python runtime, ONNX Runtime / PyTorch.  
> * **Forest OS Suitability:** Tier 2 (Desktop GUI via QGIS Plugin Manager).  
> * **Maintenance & Bottlenecks:** Actively developed by Alliance Bioversity International and CIAT; depends on user configuration of external Python deep learning wheels within QGIS.

### **Spaceborne Canopy Structure Extraction**

#### **rGEDI**

> * **Repository & License:** [carlos-alberto-silva/rGEDI](https://github.com/carlos-alberto-silva/rGEDI) | GPL-3.0  
> * **Standout Capability:** Specialized interface for downloading, filtering, and simulating NASA Global Ecosystem Dynamics Investigation (GEDI) full-waveform spaceborne LiDAR data (Level 1B, 2A, 2B), enabling direct regional canopy height and plant area index profiling from orbit.  
> * **Dependencies:** R, C/C++ HDF5 bindings, hdf5r, sf, raster, lidR.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * **Maintenance & Bottlenecks:** Core maintainers track NASA LP DAAC distribution API updates. Changes in Earthdata authentication tokens require ongoing package synchronization.

## **3\. Dendrochronology, Wood Anatomy, & Biomass**

### **Tree Ring Analysis, Cross-Dating, & Climate Chronology**

#### **dplR (Dendrochronology Program Library in R)**

> * **Repository & License:** [opendendro/dplR](https://github.com/opendendro/dplR) | GPL (\>= 2\)  
> * **Standout Capability:** The statistical backbone of modern dendrochronology. Handles reading/writing Tucson/TRDAS decadal formats, cross-dating verification (COFECHA equivalents), cubic spline and negative exponential detrending, chronologies compilation, and calculation of Mean Sensitivity and Gini coefficients.  
> * **Dependencies:** R (\>= 3.6), lattice, Matrix, digest.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar) or lightweight R terminal host install.  
> * **Maintenance & Bottlenecks:** Highly mature, rock-solid academic library with active CRAN maintenance led by Andy Bunn.

#### **dplPy & pyDendron**

> * **Repository & License:** [git-lium.univ-lemans.fr/Meignier/pyQtDendron](https://git-lium.univ-lemans.fr/Meignier/pyQtDendron) / [pypi: pyDendron](https://pypi.org/project/pyDendron/) | GPL-3.0  
> * **Standout Capability:** Modern Python implementation and Qt-based workstation for tree ring measurement and cross-dating. Provides interactive time-series curve shifting, correlation matrix visualization, and database synchronization for core collections.  
> * **Dependencies:** Python 3.9+, PyQt5/6, pandas, numpy, scipy, matplotlib.  
> * **Forest OS Suitability:** Tier 1 (Host CLI) and Tier 2 (Desktop GUI).  
> * **Maintenance & Bottlenecks:** Hosted primarily on GitLab (Le Mans Université). Active development focusing on European archaeological and ecological dendro-databases.

#### **TRAS (Tree Ring Analyzer Suite)**

> * **Repository & License:** [hmarichal93/tras](https://hmarichal93.github.io/tras/) | Open Source (GPL-3.0)  
> * **Standout Capability:** High-precision interactive software for tracing tree-ring boundaries on high-resolution macroscopic photographic cross-sections, utilizing edge-detection and morphological paths to automate measuring ring widths.  
> * **Dependencies:** Python, OpenCV, NumPy, PyQt.  
> * **Forest OS Suitability:** Tier 2 (Desktop GUI).  
> * **Maintenance & Bottlenecks:** Recent academic publication and release (2025/2026); rapid UI iteration.

#### **treeclim**

> * **Repository & License:** [chgrsz/treeclim](https://github.com/chgrsz/treeclim) | GPL (\>= 2\)  
> * **Standout Capability:** Calibration of tree-ring proxies against monthly and seasonal instrumental climate records using bootstrap response and correlation functions, moving beyond simple static regression to uncover changing climate sensitivity over time.  
> * **Dependencies:** R, C++ (Rcpp), dplR, boot.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * **Maintenance & Bottlenecks:** Maintained by Christian Zang on CRAN; stable with low maintenance overhead.

### **Biomass & Non-Destructive Carbon Estimation**

#### **BIOMASS (R Package)**

> * **Repository & License:** [umr-amap/BIOMASS](https://github.com/umr-amap/BIOMASS) | GPL-2.0  
> * **Standout Capability:** Implements Chave et al. pan-tropical and temperate allometric equations. Automatically fetches species wood density values from the Global Wood Density Database, models tree height-diameter relationships, and propagates measurement errors through Monte Carlo simulations to deliver rigorous carbon estimates.  
> * **Dependencies:** R, data.table, raster, jsonlite.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * **Maintenance & Bottlenecks:** Maintained by French research institutions (AMAP, CIRAD, CNRS, IRD). Stable, dependable reference code.

#### **allodb**

> * **Repository & License:** [forestgeo/allodb](https://github.com/forestgeo/allodb) | GPL-3.0  
> * **Standout Capability:** Standardizes allometric equations across global forest plots (Smithsonian ForestGEO network). Selects the best allometric equations based on geographical coordinates, botanical taxonomy, and DBH range to eliminate localized estimation bias.  
> * **Dependencies:** R (\>= 3.5), dplyr, purrr, tibble.  
> * **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).  
> * \*\*Maintenance &\# Research Report: Open Source Forestry & Arboriculture Tooling for Forest OS

**Document ID:** M-REPORT-FORESTRY-OSS-001 **Target Platform:** Forest OS (Arch Linux / Omarchy) **Reference Document:** ARBORETUM/Active/Spark-Agent\_M/M\_RESEARCH\_BRIEF\_OPEN\_SOURCE\_FORESTRY.md **Governance:** doc-414 compliant (zero em dashes)

## **Packaging Framework for Forest OS**

To preserve host OS stability on Arch Linux while delivering sovereign field and lab computing capabilities, tooling is divided across three execution tiers:

> * **Tier 1 (Host CLI / Native):** C, C++, Rust, and standalone Python CLI tools with minimal dependencies, packaged via Arch User Repository (AUR) PKGBUILDs or isolated via uv / pipx.  
> * **Tier 2 (Desktop GUI):** Native Qt/GTK desktop applications and QGIS plugins for visual analysis and field planning.  
> * **Tier 3 (Containerized Sidecar):** R-spatial stacks, Java environments, legacy Fortran engines, or heavy deep-learning frameworks isolated in Podman/Docker containers to prevent rolling-release library collisions.

## **1\. 3D Forest Inventory & LiDAR**

### **Terrestrial Laser Scanning (TLS) Stem Detection & DBH**

> * [**TreeLS**](https://github.com/tiagodc/TreeLS)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Native integration with R point clouds for automated Hough transform and RANSAC circle/cylinder fitting, extracting stem curves, taper, and DBH directly from TLS and mobile laser scanner plots.  
  * **Dependencies:** R (\>= 3.5), C++ (Rcpp, RcppArmadillo), lidR.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar). Isolates complex R-spatial compilation flags from Arch rolling updates.  
  * **Maintenance / Bottlenecks:** Upstream CRAN releases are infrequent; active fixes land directly on GitHub.  
> * [**3DFin**](https://github.com/3DFin/3DFin)  
  * **License:** GPL-3.0  
  * **Standout Capability:** End-to-end automated stem isolation and DBH measurement optimized for both TLS and personal mobile laser scanners (PLS), featuring a dedicated visual verification interface.  
  * **Dependencies:** Python 3.9+, Open3D, NumPy, SciPy, CloudCompare/PCL hooks, PyQt.  
  * **Forest OS Tier:** Tier 1 (Host CLI via uv) or Tier 2 (Desktop GUI).  
  * **Maintenance / Bottlenecks:** Actively developed by the University of Cordoba; closely tracks Open3D and NumPy compatibility.  
> * [**TreeSeg**](https://github.com/apburt/treeseg)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Dissects massive, unorganized multi-scan TLS plot point clouds into individual tree point clouds using generic tree architecture priors without requiring prior aerial crown polygons.  
  * **Dependencies:** C++11, Point Cloud Library (PCL \>= 1.8), Eigen3, Boost.  
  * **Forest OS Tier:** Tier 1 (Host CLI). Native compilation produces lean, high-throughput command-line binaries (treeseg, rxp2pcd).  
  * **Maintenance / Bottlenecks:** Stable academic codebase; requires guarding against breaking API updates in modern PCL releases.

### **Quantitative Structure Modeling (QSM)**

> * [**TreeQSM**](https://github.com/InverseTampere/TreeQSM)  
  * **License:** GNU GPL-3.0  
  * **Standout Capability:** The canonical reference standard for QSM. Constructs hierarchical cylinder topologies to compute stem/branch volume, branch size frequency distributions, and aboveground biomass (AGB).  
  * **Dependencies:** MATLAB / GNU Octave.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar running headless GNU Octave).  
  * **Maintenance / Bottlenecks:** Historically dependent on proprietary MATLAB; executing via Octave requires careful validation of optimization toolboxes.  
> * [**SimpleForest**](https://github.com/SimpleForest)  
  * **License:** GPL-3.0  
  * **Standout Capability:** CloudCompare plugin and standalone C++ tool using sphere-following algorithms and Dijkstra pathfinding to generate reverse-pipe QSMs with automated occlusion correction.  
  * **Dependencies:** C++, CloudCompare Core, PCL, Qt5.  
  * **Forest OS Tier:** Tier 2 (Desktop GUI via CloudCompare plugin) or Tier 1 (Host CLI).  
  * **Maintenance / Bottlenecks:** Tied to CloudCompare plugin interfaces, requiring recompilation when CloudCompare updates.  
> * [**PyTLidar**](https://github.com/Landscape-CV/PyTLidar)  
  * **License:** MIT License  
  * **Standout Capability:** Python-native QSM extraction and structural metric computation, providing direct integration with PyTorch, SciPy, and Open3D scientific workflows without legacy runtimes.  
  * **Dependencies:** Python 3.10+, NumPy, Numba, Laspy, Open3D.  
  * **Forest OS Tier:** Tier 1 (Host CLI via pipx).  
  * **Maintenance / Bottlenecks:** Fast-evolving new codebase; API contracts continue to mature through open journal reviews.  
> * [**rTwig**](https://github.com/aidanmorales/rTwig)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Corrects structural overestimation in QSM cylinder models by integrating empirical twig diameter databases and botanical pipe models (the Real Twig method) to yield highly accurate woody volume estimates.  
  * **Dependencies:** R (\>= 4.0), Rcpp, data.table, rgl.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Actively maintained on CRAN with extensive unit test coverage.

### **Airborne LiDAR Processing & Canopy Height Models**

> * [**lidR**](https://github.com/r-lidar/lidR)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Out-of-core spatial engine capable of processing terabyte-scale airborne LiDAR point clouds. Delivers pit-free Canopy Height Models (CHMs), digital terrain models, and individual tree segmentation (Li, Dalponte, and Silva algorithms).  
  * **Dependencies:** R, C++ (Rcpp), GDAL, GEOS, PROJ.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Exceptionally maintained by Jean-Romain Roussel; relies on synchronized GDAL/PROJ libraries that frequently collide on rolling Arch Linux installs.  
> * [**PDAL (Point Data Abstraction Library)**](https://github.com/PDAL/PDAL)  
  * **License:** Apache-2.0 / BSD  
  * **Standout Capability:** High-performance point cloud manipulation engine. Executes JSON-defined streaming pipelines for ground classification (SMRF, CSF), height-above-ground normalization, rasterization, and voxel thinning.  
  * **Dependencies:** C++17, GDAL, GeoTIFF, LibLAS.  
  * **Forest OS Tier:** Tier 1 (Host CLI). Installed natively via pacman \-S pdal.  
  * **Maintenance / Bottlenecks:** Industry-standard OSGeo foundation project with zero technical debt.

## **2\. Canopy Computer Vision & Deep Learning**

### **Individual Tree Crown (ITC) Detection**

> * [**DeepForest**](https://github.com/weecology/DeepForest)  
  * **License:** MIT License  
  * **Standout Capability:** Pre-trained neural network trained on millions of tree crowns across global biomes. Delivers instant individual crown bounding box predictions on airborne RGB drone orthomosaics with zero manual training.  
  * **Dependencies:** Python 3.9+, PyTorch, TorchVision, Rasterio, Albumentations.  
  * **Forest OS Tier:** Tier 1 (Host CLI via dedicated CUDA venv) or Tier 3 (GPU-accelerated container).  
  * **Maintenance / Bottlenecks:** Highly active engineering from the Weecology Lab (University of Florida).  
> * [**PyCrown**](https://github.com/manaakiwhenua/pycrown)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Combines LiDAR CHMs and multispectral drone imagery to delineate individual crowns and calculate crown spread, crown volume, and tree top positions using watershed and regional growth routines.  
  * **Dependencies:** Python 3, GDAL, NumPy, SciPy, Rasterio, Scikit-Image.  
  * **Forest OS Tier:** Tier 1 (Host CLI in isolated venv).  
  * **Maintenance / Bottlenecks:** Infrequent upstream updates; requires explicit pinning of legacy GDAL Python bindings.  
> * [**TreeEyed**](https://github.com/afruizh/TreeEyed)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Integrates computer vision models (including YOLO and DeepForest) directly inside the QGIS map canvas, enabling click-and-run crown delineation over georeferenced raster layers.  
  * **Dependencies:** QGIS 3.x Python environment, ONNX Runtime / PyTorch.  
  * **Forest OS Tier:** Tier 2 (Desktop GUI via QGIS Plugin Manager).  
  * **Maintenance / Bottlenecks:** Backed by Alliance Bioversity and CIAT; requires users to manually install Python AI runtime dependencies into the local QGIS environment.

### **Spaceborne Canopy Structure Extraction**

> * [**rGEDI**](https://github.com/carlos-alberto-silva/rGEDI)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Downloads, filters, and processes NASA GEDI spaceborne full-waveform LiDAR data (Level 1B, 2A, 2B), enabling orbital extraction of canopy height profiles, vertical plant area indices, and ground elevation models.  
  * **Dependencies:** R, C/C++ HDF5 bindings, hdf5r, sf, lidR.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Must continuously adapt to NASA Earthdata authentication and LP DAAC distribution API updates.

## **3\. Dendrochronology, Wood Anatomy, & Biomass**

### **Tree Ring Analysis, Cross-Dating, & Climate Chronology**

> * [**dplR**](https://github.com/opendendro/dplR)  
  * **License:** GPL (\>= 2\)  
  * **Standout Capability:** The statistical standard in tree-ring research. Handles standard decadal formats (Tucson/TRDAS), cross-dating verification (COFECHA equivalents), detrending (splines, modified negative exponential), and chronology development (Mean Sensitivity, EPS, Gini coefficient).  
  * **Dependencies:** R (\>= 3.6), Matrix, lattice.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar) or Host R CLI.  
  * **Maintenance / Bottlenecks:** Very stable reference package maintained on CRAN by Andy Bunn.  
> * [**pyDendron / pyQtDendron**](https://git-lium.univ-lemans.fr/Meignier/pyQtDendron)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Modern Python workstation for dendrochronologists featuring an interactive graphical canvas for manual ring width cross-dating, visual curve synchronization, and statistical correlation scoring.  
  * **Dependencies:** Python 3.9+, PyQt5/6, pandas, numpy, scipy, matplotlib.  
  * **Forest OS Tier:** Tier 2 (Desktop GUI) and Tier 1 (Host CLI via [pyDendron on PyPI](https://pypi.org/project/pyDendron/)).  
  * **Maintenance / Bottlenecks:** Actively developed at Le Mans Université with recurring releases.  
> * [**TRAS (Tree Ring Analyzer Suite)**](https://hmarichal93.github.io/tras/)  
  * **License:** GPL-3.0  
  * **Standout Capability:** High-precision computer vision tool for interactive detection and tracing of tree rings on macroscopic wood disc photographs and cores, automating radial measurement paths.  
  * **Dependencies:** Python 3, OpenCV, PyQt, NumPy.  
  * **Forest OS Tier:** Tier 2 (Desktop GUI).  
  * **Maintenance / Bottlenecks:** Modern project with ongoing UI and feature refinements.  
> * [**treeclim**](https://github.com/chgrsz/treeclim)  
  * **License:** GPL (\>= 2\)  
  * **Standout Capability:** Calculates bootstrap response and correlation functions between tree-ring chronologies and monthly/seasonal climate datasets, capturing non-stationary climate responses across decades.  
  * **Dependencies:** R, C++ (Rcpp), dplR, boot.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Stable, well-maintained academic utility.

### **Biomass & Non-Destructive Carbon Estimation**

> * [**BIOMASS**](https://github.com/umr-amap/BIOMASS)  
  * **License:** GPL-2.0  
  * **Standout Capability:** Implements Chave et al. pan-tropical allometries, fetches wood density automatically from the Global Wood Density Database, fits local height-diameter curves, and estimates carbon stocks with propagated measurement uncertainties via Monte Carlo runs.  
  * **Dependencies:** R, data.table, raster, jsonlite.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Formally maintained by French research institutions (AMAP, CIRAD, CNRS, IRD). Highly reliable.  
> * [**allodb**](https://github.com/forestgeo/allodb)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Unified calibration framework for allometric biomass estimation across global forests (Smithsonian ForestGEO network), selecting optimal localized equations based on geographic coordinates, taxonomic status, and DBH ranges.  
  * **Dependencies:** R (\>= 3.5), dplyr, purrr.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Backed by the Smithsonian Institution; very stable.

## **4\. Forest Growth, Disturbance, & Silvicultural Simulation**

### **Growth & Yield Simulators**

> * [**USDA Forest Vegetation Simulator (FVS)**](https://www.fs.usda.gov/fvs/) **/ [Open-FVS](https://github.com/forest-vegetation-simulator/fvs)**  
  * **License:** Public Domain / US Government Work  
  * **Standout Capability:** The standard individual-tree growth and yield simulator for North American forestry. Simulates multi-decade forest growth, mortality, carbon storage, fire hazard (Fire and Fuels Extension), and custom silvicultural treatments across 20 regional geographic variants.  
  * **Dependencies:** Fortran 90/95, C, Python bindings.  
  * **Forest OS Tier:** Tier 1 (Native CLI engine) or Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Core logic resides in decades-old Fortran; modern deployments wrap compilation within Docker or headless Python runtimes.  
> * [**microfvs**](https://github.com/Vibrant-Planet-Open-Science/microfvs)  
  * **License:** MIT License  
  * **Standout Capability:** High-throughput modern REST API and execution wrapper for FVS, enabling automated batch execution of growth-and-yield simulations from Python scripts and web applications.  
  * **Dependencies:** Python, Docker, FVS native binaries.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar service).  
  * **Maintenance / Bottlenecks:** Maintained by Vibrant Planet Open Science; actively tracks cloud and local microservice architectures.  
> * [**Capsis**](https://capsis.cirad.fr/)  
  * **License:** LGPL-2.1  
  * **Standout Capability:** Modular forestry simulation platform hosting dozens of stand dynamics and silvicultural models (individual-based, stand-level, mixed-species, uneven-aged, and agroforestry systems) with rich 3D visualization.  
  * **Dependencies:** Java (JDK 8 / 11+), JavaFX, AMAPstudio.  
  * **Forest OS Tier:** Tier 2 (Desktop GUI via Java runtime).  
  * **Maintenance / Bottlenecks:** Continuously maintained since 1999 by INRAE/CIRAD; requires proper Java/JavaFX desktop setup on Linux.  
> * [**SORTIE-ND**](https://www.sortie-nd.org/)  
  * **License:** Open Source / Academic  
  * **Standout Capability:** Spatially explicit, individual-tree neighborhood dynamics simulator. Models fine-scale tree-tree competition for light, space, and resources, tracking seedling recruitment, sapling survival, and canopy gap succession under varied harvesting regimes.  
  * **Dependencies:** C++ core engine, Java GUI, optional R wrapper (rsortie).  
  * **Forest OS Tier:** Tier 1 (Host CLI engine) and Tier 2 (Desktop GUI).  
  * **Maintenance / Bottlenecks:** Niche ecological tool; legacy GUI components benefit from containerization or running the headless C++ simulation core directly.

### **Landscape Disturbance & Wildfire Simulation**

> * [**LANDIS-II**](https://github.com/LANDIS-II-Foundation)  
  * **License:** Apache-2.0 / BSD  
  * **Standout Capability:** Multi-century, landscape-scale simulation of forest succession, seed dispersal, insect defoliation, timber harvest, and large-scale wildfire disturbances over hundreds of thousands of hectares.  
  * **Dependencies:** C\# / .NET 6.0/8.0 runtime.  
  * **Forest OS Tier:** Tier 1 (Host CLI running on modern cross-platform .NET).  
  * **Maintenance / Bottlenecks:** Transitioned from legacy .NET Framework to modern cross-platform .NET, allowing native execution on Arch Linux without Wine. Extension modules must be checked for version compatibility.  
> * [**Cell2Fire**](https://github.com/cell2fire/Cell2Fire)  
  * **License:** MIT License  
  * **Standout Capability:** Ultra-fast, raster-based wildfire spread simulator powered by C++ and Python. Implements the Canadian Forest Fire Behavior Prediction (FBP) and Scott & Burgan fuel models, simulating stochastic fire growth across gridded landscapes under changing weather conditions.  
  * **Dependencies:** C++14, Python 3, OpenMP, GDAL.  
  * **Forest OS Tier:** Tier 1 (Host CLI) and Tier 2 (QGIS plugin integration).  
  * **Maintenance / Bottlenecks:** Actively developed by fire science research groups; requires native C++ compilation with OpenMP for parallel execution.  
> * [**FMT (Forest Management Tool)**](https://github.com/Bureau-du-Forestier-en-chef/FMT)  
  * **License:** LGPL-3.0  
  * **Standout Capability:** C++17 library designed to parse Woodstock-formatted forest planning models and formulate linear/mixed-integer programming models for harvest scheduling, wood supply optimization, and spatial conservation constraints.  
  * **Dependencies:** C++17, GDAL, Boost, Linear Programming solvers (OSI, CLP, CBC, or Gurobi), Python/R bindings.  
  * **Forest OS Tier:** Tier 1 (Host CLI and Python module).  
  * **Maintenance / Bottlenecks:** Maintained by the Bureau du Forestier en chef of Quebec; sophisticated optimization tool requiring careful linkage to linear programming libraries.

## **5\. Field Arboriculture & Canopy Health**

### **Mobile & Urban Tree Inventory Systems**

> * [**QField**](https://github.com/opengisch/QField)  
  * **License:** GPL-2.0  
  * **Standout Capability:** Mobile GIS field data collection tool built directly on the QGIS engine. Arborists can deploy custom offline relational forms featuring ISA Basic Tree Risk Assessment (TRAQ) forms, GPS/GNSS averaging, photo capture, and direct cloud/local synchronization with desktop QGIS.  
  * **Dependencies:** C++, Qt5/Qt6, QGIS core libraries (Android, iOS, Windows, Linux).  
  * **Forest OS Tier:** Tier 2 (Desktop inspection app on Linux tablets/laptops) combined with desktop QGIS project authoring.  
  * **Maintenance / Bottlenecks:** Commercial-grade open-source project by OPENGIS.ch with rapid development and rock-solid stability.  
> * [**OpenTreeMap**](https://github.com/OpenTreeMap/otm-core)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Collaborative urban forestry web platform that tracks municipal tree inventories, community planting programs, and calculates annual ecosystem service benefits (stormwater intercepted, carbon sequestered, energy saved) using i-Tree eco algorithms.  
  * **Dependencies:** Python (Django), PostgreSQL/PostGIS, Node.js.  
  * **Forest OS Tier:** Tier 3 (Docker Compose multi-container stack).  
  * **Maintenance / Bottlenecks:** Core development has slowed in recent years; deploying requires running in containerized environments with pinned Python and PostgreSQL versions.  
> * [**CanopyWatch**](https://github.com/meyeringn/canopy-watch)  
  * **License:** MIT License  
  * **Standout Capability:** Zero-dependency, single-file browser dashboard mapping urban tree canopy coverage against socioeconomic indicators, heat vulnerability, and environmental justice priorities.  
  * **Dependencies:** Pure HTML5, CSS3, JavaScript (Leaflet/MapLibre).  
  * **Forest OS Tier:** Tier 1 (Native static web resource executable in any lightweight browser).  
  * **Maintenance / Bottlenecks:** Very low maintenance burden due to its zero-backend architecture.

### **Hemispherical Canopy Photography & Leaf Area Index**

> * [**hemispheR**](https://github.com/frousseu/hemispheR)  
  * **License:** GPL-3.0  
  * **Standout Capability:** Fully reproducible processing of upward-looking fisheye canopy photographs. Automates circular masking, chromatic thresholding, gap fraction estimation, and calculation of effective Leaf Area Index (LAI) and canopy openness according to Miller, Licor LAI-2000, and Campbell formulations.  
  * **Dependencies:** R, terra, imagefx.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Actively maintained on CRAN; built on modern terra spatial raster foundations.  
> * [**gaplightr**](https://hakaiinstitute.github.io/gaplightr/)  
  * **License:** MIT License  
  * **Standout Capability:** An open-source R implementation of the classic Gap Light Analyzer (GLA). Processes both physical hemispherical photographs and virtual fisheye views synthesized from airborne LiDAR point clouds, computing direct and diffuse solar radiation regimes and canopy gap metrics.  
  * **Dependencies:** R, terra, lidR, sf.  
  * **Forest OS Tier:** Tier 3 (Dockerized Sidecar).  
  * **Maintenance / Bottlenecks:** Maintained by the Hakai Institute (Tula Foundation); modern and well-documented.

## **6\. Canopy Bioacoustics & Ecology**

### **Acoustic Monitoring & Soundscape Analysis**

> * [**BirdNET-Analyzer**](https://github.com/kahst/BirdNET-Analyzer)  
  * **License:** MIT License  
  * **Standout Capability:** Deep-learning sound recognition engine trained on more than 6,000 avian and wildlife species. Processes continuous acoustic recordings collected from canopy autonomous recording units (ARUs like AudioMoth), outputting timestamped species detection logs, confidence scores, and audio spectrograms.  
  * **Dependencies:** Python 3.9+, TensorFlow / TFLite, Librosa, NumPy.  
  * **Forest OS Tier:** Tier 1 (Host CLI via TFLite runtime) or Tier 2 (Native GUI mode).  
  * **Maintenance / Bottlenecks:** World-class development maintained by the K. Lisa Yang Center for Conservation Bioacoustics at the Cornell Lab of Ornithology and Chemnitz University of Technology. Highly performant.  
> * [**scikit-maad (Mathematical Animal Acoustic Diversity)**](https://github.com/scikit-maad/scikit-maad)  
  * **License:** BSD-3-Clause  
  * **Standout Capability:** Complete quantitative soundscape ecology workbench. Measures broad biophony, anthrophony, and geophony dynamics through standard acoustic diversity indices (Acoustic Complexity Index \[ACI\], Acoustic Diversity Index \[ADI\], Bioacoustic Index \[BI\], Normalized Difference Soundscape Index \[NDSI\]) alongside custom audio segmentation and spectrogram 2D decomposition.  
  * **Dependencies:** Python 3.9+, NumPy, SciPy, Scikit-Learn, Scikit-Image, Librosa.  
  * **Forest OS Tier:** Tier 1 (Host CLI via standard Python scientific environment).  
  * **Maintenance / Bottlenecks:** Actively maintained with rigorous documentation and reproducible tutorials published in scientific literature.

## **Synthesis Matrix for Forest OS Deployment**

| Tool | Domain | Primary Language | Recommended Forest OS Tier | Primary Deliverable |
| :---- | :---- | :---- | :---- | :---- |
| **TreeLS** | 3D / TLS | R / C++ | Tier 3 (Container) | Stem curve & DBH extraction |
| **3DFin** | 3D / TLS | Python / C++ | Tier 1 (CLI) / Tier 2 (GUI) | Automated 3D TLS/PLS inventory |
| **TreeSeg** | 3D / TLS | C++11 | Tier 1 (Native Host CLI) | Standalone point cloud tree segmenter |
| **TreeQSM** | 3D / QSM | MATLAB / Octave | Tier 3 (Container) | Topological branch cylinder modeling |
| **SimpleForest** | 3D / QSM | C++ | Tier 1 (CLI) / Tier 2 (GUI) | Dijkstra reverse-pipe QSM |
| **PyTLidar** | 3D / QSM | Python | Tier 1 (Native Host CLI) | Pythonic QSM & structural metrics |
| **rTwig** | 3D / QSM | R | Tier 3 (Container) | Twig diameter & volume correction |
| **lidR** | 3D / Airborne | R / C++ | Tier 3 (Container) | Large-scale ALS processing & CHMs |
| **PDAL** | 3D / Airborne | C++17 | Tier 1 (Native Host CLI) | High-speed point cloud filtering |
| **DeepForest** | Canopy Vision | Python / PyTorch | Tier 1 (Native Host CLI) | Pre-trained RGB crown detection |
| **PyCrown** | Canopy Vision | Python | Tier 1 (Host CLI) | LiDAR \+ optical crown delineation |
| **TreeEyed** | Canopy Vision | Python / QGIS | Tier 2 (Desktop GUI) | QGIS interactive AI crown mapping |
| **rGEDI** | Spaceborne | R / C | Tier 3 (Container) | NASA GEDI orbital LiDAR profiling |
| **dplR** | Dendrochronology | R | Tier 3 (Container) | Statistical ring detrending & dating |
| **pyDendron** | Dendrochronology | Python / Qt | Tier 1 (CLI) / Tier 2 (GUI) | Interactive cross-dating workstation |
| **TRAS** | Dendrochronology | Python / Qt | Tier 2 (Desktop GUI) | Optical ring tracing & measuring |
| **treeclim** | Dendrochronology | R / C++ | Tier 3 (Container) | Bootstrapped climate-growth models |
| **BIOMASS** | Carbon / Biomass | R | Tier 3 (Container) | Pan-tropical allometry & wood density |
| **allodb** | Carbon / Biomass | R | Tier 3 (Container) | Standardized ForestGEO allometries |
| **USDA FVS** | Growth & Yield | Fortran / C | Tier 1 (CLI) / Tier 3 (Container) | Standard North American stand simulator |
| **microfvs** | Growth & Yield | Python | Tier 3 (Container API) | Microservice REST wrapper for FVS |
| **Capsis** | Growth & Yield | Java | Tier 2 (Desktop GUI) | Multi-model stand & agroforestry platform |
| **SORTIE-ND** | Growth & Yield | C++ / Java | Tier 1 (CLI) / Tier 2 (GUI) | Spatially explicit competition model |
| **LANDIS-II** | Succession & Fire | C\# (.NET Core) | Tier 1 (Native Host CLI) | Multi-century landscape disturbance |
| **Cell2Fire** | Wildfire Spread | C++ / Python | Tier 1 (CLI) / Tier 2 (GUI) | Fast raster fire growth simulator |
| **FMT** | Harvest Planning | C++17 | Tier 1 (Native Host CLI) | Forest management linear programming |
| **QField** | Field Inventory | C++ / Qt / QGIS | Tier 2 (Desktop / Mobile GUI) | Offline GPS tree risk & inventory forms |
| **OpenTreeMap** | Urban Inventory | Python / PostGIS | Tier 3 (Container Compose) | Municipal inventory & eco-benefits |
| **CanopyWatch** | Urban Equity | HTML5 / JS | Tier 1 (Browser Static) | Canopy equity & heat vulnerability map |
| **hemispheR** | Canopy Health | R | Tier 3 (Container) | Fisheye LAI & canopy openness |
| **gaplightr** | Canopy Health | R | Tier 3 (Container) | Real & virtual LiDAR Gap Light Analyzer |
| **BirdNET** | Bioacoustics | Python / TFLite | Tier 1 (CLI) / Tier 2 (GUI) | Automated avian sound classifier |
| **scikit-maad** | Bioacoustics | Python | Tier 1 (Native Host CLI) | Soundscape acoustic diversity indices |

