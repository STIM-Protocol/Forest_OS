# forest-sim: Forest OS Growth & Yield Simulation Container Sidecar

**Document ID:** SPEC-CONTAINER-FOREST-SIM-001  
**Image Name:** `forest-sim`  
**Base Image:** `ubuntu:24.04`  
**Governance:** Doc-414 Compliant (Zero em dashes, strict claims discipline)  

---

## 1. Purpose & Scope

The `forest-sim` container sidecar provides individual-tree growth, yield, and forest disturbance simulation capabilities. The core engine is the USDA Forest Vegetation Simulator (Open-FVS), a Fortran 90/95 modeling suite with 20 regional geographic variants. Containerization encapsulates the legacy Fortran compiler toolchain (`gfortran`), preventing compiler drifts and library incompatibilities across host Linux distributions. In addition, it packages Vibrant Planet's `microfvs` Python REST API service for programmatic batch simulation execution.

---

## 2. Qualified Package Inventory

| Tool | Domain | Capability | Upstream Source |
| :--- | :--- | :--- | :--- |
| **USDA Open-FVS** | Growth & Yield Simulation | Multi-decade individual-tree growth, mortality, carbon, and fire hazard across 20 regional variants. | `github.com/forest-vegetation-simulator/fvs` |
| **microfvs** | REST API & Batch Runner | Modern FastAPI service wrapping FVS execution for automated high-throughput cloud and local modeling. | `github.com/Vibrant-Planet-Open-Science/microfvs` |

---

## 3. Regional FVS Variants

By default, the image compiles key Western and nationwide variants to optimize build time and storage footprint:

* **FVSpn:** Pacific Northwest (coastal Washington and Oregon)
* **FVSwc:** West Coast (coastal and cascade Oregon/Washington)
* **FVSca:** California (statewide)
* **FVSso:** Southern Oregon / Northern California
* **FVSie:** Inland Empire (eastern WA, northern ID, western MT)
* **FVSut:** Utah
* **FVScr:** Central Rockies
* **FVStt:** Tetons
* **FVSbm:** Blue Mountains
* **FVSec:** East Cascades
* **FVSci:** Central Idaho
* **FVSws:** Western Sierra Nevada
* **FVSnc:** Northern California
* **FVSkt:** Kootenai / Kaniksu
* **FVSem:** Eastern Montana
* **FVSak:** Alaska
* **FVSoc:** Olympic Peninsula

To compile all 20 standard nationwide variants (including Lake States `FVSls`, Northeast `FVSne`, and Southern `FVSsn`), pass the build argument:
```bash
docker build --build-arg FVS_VARIANTS=all -t forest-sim -f Containerfile .
```

---

## 4. Building the Container Image

Build with Docker or Podman from this directory:

```bash
docker build -t forest-sim -f Containerfile .
```

Or execute via the Forest OS build orchestrator:

```bash
bash 03_Automation_Scripts/build_containers.sh sim
```

---

## 5. Usage Patterns

### Direct Simulation Run
Run a regional FVS variant with an existing keyword input file:
```bash
forest-sim fvs pn input.key
```
Or execute directly by variant binary name:
```bash
forest-sim FVSpn input.key
```

### List Available Variants
Display all compiled FVS executables installed in the container:
```bash
forest-sim variants
```

### Run microfvs REST API
Launch the microfvs service accessible at `http://localhost:8000`:
```bash
forest-sim serve
```
Interactive API documentation will be available at `http://localhost:8000/docs`.

### Run Python Simulation Scripts
Execute a Python script using the container virtual environment:
```bash
forest-sim python run_batch_simulation.py
```

### Interactive Shell
Open a bash shell inside the simulation container with host folder mapped:
```bash
forest-sim bash
```
