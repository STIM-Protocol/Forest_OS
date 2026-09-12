# Research Report: Open Source Forestry & Arboriculture Tooling for Forest OS

**Document ID:** M-REPORT-FORESTRY-OSS-001  
**Target Platform:** Forest OS (Arch Linux / Omarchy)  
**Reference Document:** ARBORETUM/Active/Spark-Agent_M/M_RESEARCH_BRIEF_OPEN_SOURCE_FORESTRY.md  
**Author:** Agent M (Gemini Spark)  
**Ingested by:** AG-Orchestrator  
**Governance:** doc-414 compliant (zero em dashes)  

---

## Executive Summary & Architectural Packaging Strategy

Forest OS demands sovereign, reproducible computational ecology workflows. To balance high-throughput analytical capabilities with operating system hygiene on an Arch Linux base, tooling is classified into three deployment tiers:

* **Tier 1 (Host CLI / Native):** High-performance C++, Python, or Rust binaries with minimal, stable dependency graphs. Installed natively via Arch User Repository (AUR) PKGBUILDs or isolated Python virtual environments (pipx / uv).
* **Tier 2 (Desktop GUI):** Interactive visualization environments (QGIS plugins, native Qt6 applications, desktop viewers).
* **Tier 3 (Dockerized Sidecar / Podman):** R environments with extensive geospatial dependencies (GDAL/GEOS/PROJ), legacy Java runtimes, or complex C/Fortran legacy stacks. Containerization prevents host system library collision and dependency drift.

---

## 1. 3D Forest Inventory & LiDAR

### Terrestrial Laser Scanning (TLS) Stem Detection & DBH

#### TreeLS
* **Repository & License:** [tiagodc/TreeLS](https://github.com/tiagodc/TreeLS) | GPL-3.0
* **Standout Capability:** Native integration with R lidR infrastructure for automated Hough transform and RANSAC circle/cylinder fitting directly on point clouds, extracting stem curves, taper, and DBH from unorganized terrestrial and mobile laser scans.
* **Dependencies:** R (>= 3.5), C++ (Rcpp, RcppArmadillo), spatial libraries (lidR, sf, raster).
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar). Complex geospatial C++ compile chains in R are best isolated in a dedicated R-spatial container.
* **Maintenance & Bottlenecks:** Upstream development on CRAN is sporadic; primary releases and bug fixes occur directly in the GitHub repository. Requires synchronized GDAL/PROJ versions.

#### 3DFin (3D Forest Inventory)
* **Repository & License:** [3DFin/3DFin](https://github.com/3DFin/3DFin) | GPL-3.0
* **Standout Capability:** Point cloud processing optimized specifically for personal laser scanning (PLS) and terrestrial laser scanning (TLS). Provides end-to-end automated stem detection, tree segmentation, and DBH extraction via an intuitive GUI or batch command line.
* **Dependencies:** Python 3.9+, CloudCompare / PCL bindings, NumPy, SciPy, Open3D, PyQt5/6.
* **Forest OS Suitability:** Tier 1 (Host CLI via uv) or Tier 2 (Desktop GUI).
* **Maintenance & Bottlenecks:** Actively developed by research groups at the University of Cordoba and Forestry research partners; relies heavily on NumPy/Open3D compatibility windows.

#### TreeSeg
* **Repository & License:** [apburt/treeseg](https://github.com/apburt/treeseg) | GPL-3.0
* **Standout Capability:** Near-ground and canopy point cloud extraction designed for large-scale TLS plots. Uses generic tree architecture priors to dissect dense multi-return point clouds into discrete individual tree point clouds without requiring prior aerial crown boundaries.
* **Dependencies:** C++11, Point Cloud Library (PCL >= 1.8), Eigen3, Boost.
* **Forest OS Suitability:** Tier 1 (Host CLI). Native compilation via CMake produces standalone binaries (treeseg, rxp2pcd) that execute with high performance on Arch Linux.
* **Maintenance & Bottlenecks:** Stable academic codebase; requires tracking modern PCL API changes when compiling on rolling-release Arch toolchains.

### Quantitative Structure Modeling (QSM)

#### TreeQSM
* **Repository & License:** [InverseTampere/TreeQSM](https://github.com/InverseTampere/TreeQSM) | GNU GPL-3.0
* **Standout Capability:** The canonical reference standard for cylindrical Quantitative Structure Models. Reconstructs topological branch ordering, parent-child branch geometry, wood volume, and aboveground biomass (AGB) distributions from segmented TLS point clouds.
* **Dependencies:** MATLAB (original) or GNU Octave / MATLAB Compiler Runtime (MCR).
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar running Octave/headless MCR).
* **Maintenance & Bottlenecks:** MATLAB runtime requirement has historically hindered automated Linux pipelines, driving community migration to native Python and R wrappers.

#### SimpleForest
* **Repository & License:** [SimpleForest / Jan Hackenberg](https://github.com/SimpleForest) | GPL-3.0
* **Standout Capability:** CloudCompare plugin and standalone C++ tool utilizing sphere-following and Dijkstra clustering algorithms to build reverse-pipe QSMs, featuring automatic correction for occlusion and ray-tracing validation.
* **Dependencies:** C++, CloudCompare Core, PCL, Qt5.
* **Forest OS Suitability:** Tier 2 (Desktop GUI via CloudCompare plugin) or Tier 1 (Host CLI).
* **Maintenance & Bottlenecks:** Tied to specific CloudCompare plugin APIs. Requires rebuilding when CloudCompare undergoes major version transitions.

#### PyTLidar
* **Repository & License:** [Landscape-CV/PyTLidar](https://github.com/Landscape-CV/PyTLidar) | MIT License
* **Standout Capability:** Native Python implementation and wrapper around modern QSM algorithms, enabling direct pipeline integration with standard Python scientific ecosystems (PyTorch, SciPy, Open3D) without proprietary runtime dependencies.
* **Dependencies:** Python 3.10+, NumPy, Numba, Open3D, Laspy.
* **Forest OS Suitability:** Tier 1 (Host CLI via pipx or standard Python environment).
* **Maintenance & Bottlenecks:** Newer open-source initiative under active expansion; requires checking JOSS/review issues for API stability.

#### rTwig
* **Repository & License:** [aidanmorales/rTwig](https://github.com/aidanmorales/rTwig) | GPL-3.0
* **Standout Capability:** Corrects structural overestimation in QSM cylinder models by applying empirical twig diameter databases and botanical pipe models (Real Twig method), dramatically refining tree volume and surface area estimates.
* **Dependencies:** R (>= 4.0), data.table, Rcpp, rgl.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Actively maintained on CRAN and GitHub with comprehensive unit tests and reproducible vignettes.

### Airborne LiDAR Processing & Canopy Height Models

#### lidR
* **Repository & License:** [r-lidar/lidR](https://github.com/r-lidar/lidR) | GPL-3.0
* **Standout Capability:** Forest inventory engine capable of processing terabyte-scale airborne LiDAR point clouds. Features out-of-core catalog processing, individual tree segmentation (Li, Dalponte, Silva algorithms), pit-free Canopy Height Model (CHM) generation, and digital terrain modeling.
* **Dependencies:** R, C++ (Rcpp), GDAL, GEOS, PROJ, spatial ecosystem.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Highly active upstream governance by Jean-Romain Roussel. Fastidious codebase, but host installation on Arch can be brittle due to upstream rolling upgrades of proj and gdal.

#### PDAL (Point Data Abstraction Library)
* **Repository & License:** [PDAL/PDAL](https://github.com/PDAL/PDAL) | Apache-2.0 / BSD
* **Standout Capability:** The GDAL equivalent for point clouds. Allows streaming JSON-based pipeline filters for ground classification (SMRF/CSF), height-above-ground normalization, voxel filtering, and rasterization at native C++ execution speeds.
* **Dependencies:** C++17, GDAL, GeoTIFF, LibLAS, Python bindings.
* **Forest OS Suitability:** Tier 1 (Host CLI). Available directly in Arch Linux extra repository (pacman -S pdal).
* **Maintenance & Bottlenecks:** Robust, industry-standard governance under OSGeo. Negligible technical debt.

---

## 2. Canopy Computer Vision & Deep Learning

### Individual Tree Crown (ITC) Detection

#### DeepForest
* **Repository & License:** [weecology/DeepForest](https://github.com/weecology/DeepForest) | MIT License
* **Standout Capability:** Pre-trained Retinanet neural network trained on millions of individual tree crowns across diverse forest biomes worldwide. Detects bounding boxes and outlines of individual tree crowns directly from airborne RGB drone orthomosaics with zero retraining required for common canopy types.
* **Dependencies:** Python 3.9+, PyTorch, TorchVision, Rasterio, Albumentations, Shapely.
* **Forest OS Suitability:** Tier 1 (Host CLI via dedicated PyTorch venv with CUDA support).
* **Maintenance & Bottlenecks:** High-velocity project backed by Weecology Lab (University of Florida). Well-funded and actively maintained.

#### PyCrown
* **Repository & License:** [manaakiwhenua/pycrown](https://github.com/manaakiwhenua/pycrown) | GPL-3.0
* **Standout Capability:** Fast individual tree segmentation combining CHMs derived from airborne LiDAR with orthorectified multi-band optical imagery, delineating crowns via watershed, regional growth, and planar projection routines.
* **Dependencies:** Python 3, GDAL, NumPy, SciPy, Rasterio, Scikit-Image.
* **Forest OS Suitability:** Tier 1 (Host CLI via container or locked conda/uv environment).
* **Maintenance & Bottlenecks:** Maintenance has slowed; legacy GDAL Python bindings require careful pin-setting on modern rolling Linux systems.

#### TreeEyed
* **Repository & License:** [afruizh/TreeEyed](https://github.com/afruizh/TreeEyed) | GPL-3.0
* **Standout Capability:** Direct QGIS plugin integration bridging modern machine learning models (YOLO, DeepForest, SAM) directly onto the GIS canvas, allowing field arborists to click-to-segment canopies over raster layers.
* **Dependencies:** QGIS 3.x Python runtime, ONNX Runtime / PyTorch.
* **Forest OS Suitability:** Tier 2 (Desktop GUI via QGIS Plugin Manager).
* **Maintenance & Bottlenecks:** Actively developed by Alliance Bioversity International and CIAT; depends on user configuration of external Python deep learning wheels within QGIS.

### Spaceborne Canopy Structure Extraction

#### rGEDI
* **Repository & License:** [carlos-alberto-silva/rGEDI](https://github.com/carlos-alberto-silva/rGEDI) | GPL-3.0
* **Standout Capability:** Specialized interface for downloading, filtering, and simulating NASA Global Ecosystem Dynamics Investigation (GEDI) full-waveform spaceborne LiDAR data (Level 1B, 2A, 2B), enabling direct regional canopy height and plant area index profiling from orbit.
* **Dependencies:** R, C/C++ HDF5 bindings, hdf5r, sf, raster, lidR.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Core maintainers track NASA LP DAAC distribution API updates. Changes in Earthdata authentication tokens require ongoing package synchronization.

---

## 3. Dendrochronology, Wood Anatomy, & Biomass

### Tree Ring Analysis, Cross-Dating, & Climate Chronology

#### dplR (Dendrochronology Program Library in R)
* **Repository & License:** [opendendro/dplR](https://github.com/opendendro/dplR) | GPL (>= 2)
* **Standout Capability:** The statistical backbone of modern dendrochronology. Handles reading/writing Tucson/TRDAS decadal formats, cross-dating verification (COFECHA equivalents), cubic spline and negative exponential detrending, chronologies compilation, and calculation of Mean Sensitivity and Gini coefficients.
* **Dependencies:** R (>= 3.6), lattice, Matrix, digest.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar) or lightweight R terminal host install.
* **Maintenance & Bottlenecks:** Highly mature, rock-solid academic library with active CRAN maintenance led by Andy Bunn.

#### dplPy & pyDendron
* **Repository & License:** [git-lium.univ-lemans.fr/Meignier/pyQtDendron](https://git-lium.univ-lemans.fr/Meignier/pyQtDendron) / [pypi: pyDendron](https://pypi.org/project/pyDendron/) | GPL-3.0
* **Standout Capability:** Modern Python implementation and Qt-based workstation for tree ring measurement and cross-dating. Provides interactive time-series curve shifting, correlation matrix visualization, and database synchronization for core collections.
* **Dependencies:** Python 3.9+, PyQt5/6, pandas, numpy, scipy, matplotlib.
* **Forest OS Suitability:** Tier 1 (Host CLI) and Tier 2 (Desktop GUI).
* **Maintenance & Bottlenecks:** Hosted primarily on GitLab (Le Mans Université). Active development focusing on European archaeological and ecological dendro-databases.

#### TRAS (Tree Ring Analyzer Suite)
* **Repository & License:** [hmarichal93/tras](https://hmarichal93.github.io/tras/) | Open Source (GPL-3.0)
* **Standout Capability:** High-precision interactive software for tracing tree-ring boundaries on high-resolution macroscopic photographic cross-sections, utilizing edge-detection and morphological paths to automate measuring ring widths.
* **Dependencies:** Python, OpenCV, NumPy, PyQt.
* **Forest OS Suitability:** Tier 2 (Desktop GUI).
* **Maintenance & Bottlenecks:** Recent academic publication and release (2025/2026); rapid UI iteration.

#### treeclim
* **Repository & License:** [chgrsz/treeclim](https://github.com/chgrsz/treeclim) | GPL (>= 2)
* **Standout Capability:** Calibration of tree-ring proxies against monthly and seasonal instrumental climate records using bootstrap response and correlation functions, moving beyond simple static regression to uncover changing climate sensitivity over time.
* **Dependencies:** R, C++ (Rcpp), dplR, boot.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Maintained by Christian Zang on CRAN; stable with low maintenance overhead.

### Biomass & Non-Destructive Carbon Estimation

#### BIOMASS (R Package)
* **Repository & License:** [umr-amap/BIOMASS](https://github.com/umr-amap/BIOMASS) | GPL-2.0
* **Standout Capability:** Implements Chave et al. pan-tropical and temperate allometric equations. Automatically fetches species wood density values from the Global Wood Density Database, models tree height-diameter relationships, and propagates measurement errors through Monte Carlo simulations to deliver rigorous carbon estimates.
* **Dependencies:** R, data.table, raster, jsonlite.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Maintained by French research institutions (AMAP, CIRAD, CNRS, IRD). Stable, dependable reference code.

#### allodb
* **Repository & License:** [forestgeo/allodb](https://github.com/forestgeo/allodb) | GPL-3.0
* **Standout Capability:** Standardizes allometric equations across global forest plots (Smithsonian ForestGEO network). Selects the best allometric equations based on geographical coordinates, botanical taxonomy, and DBH range to eliminate localized estimation bias.
* **Dependencies:** R (>= 3.5), dplyr, purrr, tibble.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Maintained by the Smithsonian Institution; exceptionally stable.

---

## 4. Forest Growth, Disturbance, & Silvicultural Simulation

### Growth & Yield Simulators

#### USDA Forest Vegetation Simulator (FVS) / Open-FVS
* **Repository & License:** [USDA Forest Service](https://www.fs.usda.gov/fvs/) / [Open-FVS](https://github.com/forest-vegetation-simulator/fvs) | Public Domain
* **Standout Capability:** Standard individual-tree growth and yield simulator for North American forestry. Simulates multi-decade forest growth, mortality, carbon storage, fire hazard (Fire and Fuels Extension), and silvicultural treatments across 20 regional geographic variants.
* **Dependencies:** Fortran 90/95, C, Python bindings.
* **Forest OS Suitability:** Tier 1 (Native CLI engine) or Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Core logic resides in legacy Fortran; containerization is optimal.

#### microfvs
* **Repository & License:** [Vibrant-Planet-Open-Science/microfvs](https://github.com/Vibrant-Planet-Open-Science/microfvs) | MIT License
* **Standout Capability:** High-throughput modern REST API and execution wrapper for FVS, enabling automated batch execution of growth-and-yield simulations from Python scripts and web applications.
* **Dependencies:** Python, Docker, FVS native binaries.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar service).
* **Maintenance & Bottlenecks:** Maintained by Vibrant Planet Open Science; actively tracks cloud and local microservice architectures.

#### Capsis
* **Repository & License:** [capsis.cirad.fr](https://capsis.cirad.fr/) | LGPL-2.1
* **Standout Capability:** Modular forestry simulation platform hosting dozens of stand dynamics and silvicultural models (individual-based, stand-level, mixed-species, uneven-aged, agroforestry) with 3D visualization.
* **Dependencies:** Java (JDK 8 / 11+), JavaFX, AMAPstudio.
* **Forest OS Suitability:** Tier 2 (Desktop GUI via Java runtime).
* **Maintenance & Bottlenecks:** Continuously maintained since 1999 by INRAE/CIRAD; requires proper Java desktop setup on Linux.

#### SORTIE-ND
* **Repository & License:** [sortie-nd.org](https://www.sortie-nd.org/) | Open Source / Academic
* **Standout Capability:** Spatially explicit, individual-tree neighborhood dynamics simulator. Models fine-scale tree-tree competition for light, space, and resources, tracking seedling recruitment, sapling survival, and canopy gap succession under varied harvesting regimes.
* **Dependencies:** C++ core engine, Java GUI, optional R wrapper (rsortie).
* **Forest OS Suitability:** Tier 1 (Host CLI engine) and Tier 2 (Desktop GUI).
* **Maintenance & Bottlenecks:** Niche ecological tool; running the headless C++ simulation core directly is preferred.

### Landscape Disturbance & Wildfire Simulation

#### LANDIS-II
* **Repository & License:** [LANDIS-II-Foundation](https://github.com/LANDIS-II-Foundation) | Apache-2.0 / BSD
* **Standout Capability:** Multi-century, landscape-scale simulation of forest succession, seed dispersal, insect defoliation, timber harvest, and large-scale wildfire disturbances over hundreds of thousands of hectares.
* **Dependencies:** C# / .NET 6.0/8.0 runtime.
* **Forest OS Suitability:** Tier 1 (Host CLI running on modern cross-platform .NET).
* **Maintenance & Bottlenecks:** Transitioned to modern cross-platform .NET, allowing native execution on Arch Linux without Wine.

#### Cell2Fire
* **Repository & License:** [cell2fire/Cell2Fire](https://github.com/cell2fire/Cell2Fire) | MIT License
* **Standout Capability:** Ultra-fast, raster-based wildfire spread simulator powered by C++ and Python. Implements the Canadian Forest Fire Behavior Prediction (FBP) and Scott & Burgan fuel models, simulating stochastic fire growth across gridded landscapes under changing weather conditions.
* **Dependencies:** C++14, Python 3, OpenMP, GDAL.
* **Forest OS Suitability:** Tier 1 (Host CLI) and Tier 2 (QGIS plugin integration).
* **Maintenance & Bottlenecks:** Actively developed by fire science research groups; requires native C++ compilation with OpenMP.

#### FMT (Forest Management Tool)
* **Repository & License:** [Bureau-du-Forestier-en-chef/FMT](https://github.com/Bureau-du-Forestier-en-chef/FMT) | LGPL-3.0
* **Standout Capability:** C++17 library designed to parse Woodstock-formatted forest planning models and formulate linear/mixed-integer programming models for harvest scheduling, wood supply optimization, and spatial conservation constraints.
* **Dependencies:** C++17, GDAL, Boost, Linear Programming solvers (OSI, CLP, CBC), Python/R bindings.
* **Forest OS Suitability:** Tier 1 (Host CLI and Python module).
* **Maintenance & Bottlenecks:** Maintained by the Bureau du Forestier en chef of Quebec.

---

## 5. Field Arboriculture & Canopy Health

### Mobile & Urban Tree Inventory Systems

#### QField
* **Repository & License:** [opengisch/QField](https://github.com/opengisch/QField) | GPL-2.0
* **Standout Capability:** Mobile GIS field data collection tool built directly on the QGIS engine. Arborists can deploy custom offline relational forms featuring ISA Basic Tree Risk Assessment (TRAQ) forms, GPS/GNSS averaging, photo capture, and direct synchronization with desktop QGIS.
* **Dependencies:** C++, Qt5/Qt6, QGIS core libraries.
* **Forest OS Suitability:** Tier 2 (Desktop inspection app on Linux tablets/laptops) combined with desktop QGIS project authoring.
* **Maintenance & Bottlenecks:** Commercial-grade open-source project by OPENGIS.ch with rapid development.

#### OpenTreeMap
* **Repository & License:** [OpenTreeMap/otm-core](https://github.com/OpenTreeMap/otm-core) | GPL-3.0
* **Standout Capability:** Collaborative urban forestry web platform that tracks municipal tree inventories, community planting programs, and calculates annual ecosystem service benefits (stormwater intercepted, carbon sequestered, energy saved) using i-Tree eco algorithms.
* **Dependencies:** Python (Django), PostgreSQL/PostGIS, Node.js.
* **Forest OS Suitability:** Tier 3 (Docker Compose multi-container stack).
* **Maintenance & Bottlenecks:** Core development has slowed; containerization is required.

#### CanopyWatch
* **Repository & License:** [meyeringn/canopy-watch](https://github.com/meyeringn/canopy-watch) | MIT License
* **Standout Capability:** Zero-dependency, single-file browser dashboard mapping urban tree canopy coverage against socioeconomic indicators, heat vulnerability, and environmental justice priorities.
* **Dependencies:** Pure HTML5, CSS3, JavaScript (Leaflet/MapLibre).
* **Forest OS Suitability:** Tier 1 (Native static web resource executable in any lightweight browser).
* **Maintenance & Bottlenecks:** Negligible maintenance burden due to its zero-backend architecture.

### Hemispherical Canopy Photography & Leaf Area Index

#### hemispheR
* **Repository & License:** [frousseu/hemispheR](https://github.com/frousseu/hemispheR) | GPL-3.0
* **Standout Capability:** Fully reproducible processing of upward-looking fisheye canopy photographs. Automates circular masking, chromatic thresholding, gap fraction estimation, and calculation of effective Leaf Area Index (LAI) and canopy openness according to Miller, Licor LAI-2000, and Campbell formulations.
* **Dependencies:** R, terra, imagefx.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Actively maintained on CRAN; built on modern terra spatial raster foundations.

#### gaplightr
* **Repository & License:** [hakaiinstitute/gaplightr](https://hakaiinstitute.github.io/gaplightr/) | MIT License
* **Standout Capability:** An open-source R implementation of the classic Gap Light Analyzer (GLA). Processes both physical hemispherical photographs and virtual fisheye views synthesized from airborne LiDAR point clouds, computing direct and diffuse solar radiation regimes and canopy gap metrics.
* **Dependencies:** R, terra, lidR, sf.
* **Forest OS Suitability:** Tier 3 (Dockerized Sidecar).
* **Maintenance & Bottlenecks:** Maintained by the Hakai Institute (Tula Foundation); modern and well-documented.

---

## 6. Canopy Bioacoustics & Ecology

### Acoustic Monitoring & Soundscape Analysis

#### BirdNET-Analyzer
* **Repository & License:** [kahst/BirdNET-Analyzer](https://github.com/kahst/BirdNET-Analyzer) | MIT License
* **Standout Capability:** Deep-learning sound recognition engine trained on more than 6,000 avian and wildlife species. Processes continuous acoustic recordings collected from canopy autonomous recording units (ARUs like AudioMoth), outputting timestamped species detection logs, confidence scores, and audio spectrograms.
* **Dependencies:** Python 3.9+, TensorFlow / TFLite, Librosa, NumPy.
* **Forest OS Suitability:** Tier 1 (Host CLI via TFLite runtime) or Tier 2 (Native GUI mode).
* **Maintenance & Bottlenecks:** World-class development maintained by Cornell Lab of Ornithology and Chemnitz University of Technology. Highly performant.

#### scikit-maad (Mathematical Animal Acoustic Diversity)
* **Repository & License:** [scikit-maad/scikit-maad](https://github.com/scikit-maad/scikit-maad) | BSD-3-Clause
* **Standout Capability:** Complete quantitative soundscape ecology workbench. Measures broad biophony, anthrophony, and geophony dynamics through standard acoustic diversity indices (Acoustic Complexity Index [ACI], Acoustic Diversity Index [ADI], Bioacoustic Index [BI], Normalized Difference Soundscape Index [NDSI]) alongside custom audio segmentation and spectrogram 2D decomposition.
* **Dependencies:** Python 3.9+, NumPy, SciPy, Scikit-Learn, Scikit-Image, Librosa.
* **Forest OS Suitability:** Tier 1 (Host CLI via standard Python scientific environment).
* **Maintenance & Bottlenecks:** Actively maintained with rigorous documentation and reproducible tutorials published in scientific literature.
