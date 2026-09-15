# Project Nomad Integration: Forest Tools Custom App

**Governance:** Doc-414 Compliant (Zero em dashes, strict claims discipline)  
**Status:** Operational (Receipt dated 2026-09-15)  
**Authority:** Technical specification for packaging and managing the Forest OS scientific workbench as a native Custom App in Project Nomad.

---

## 1. Overview

[Project Nomad](https://github.com/crosstalk-solutions/project-nomad) is an offline-capable, self-hosted edge server platform for resilient homelab and emergency operations. It runs containerized microservices and exposes a unified dashboard.

Forest OS integrates with Project Nomad through a dedicated Tier 3 container sidecar: **`forest-workbench`**. This container packages the complete 33-tool scientific catalog, field execution pipelines, decision wizard, service links, and documentation into a zero-dependency Caddy 2 container that Nomad manages as a native Custom App.

---

## 2. Port 5483 and the LIVE Mnemonic

The Forest OS Workbench canonically binds to **port 5483**.

* **Keypad Mapping:** On a standard telephone alphanumeric keypad (ITU-T E.161):
  * **5** = J-K-**L**
  * **4** = G-H-**I**
  * **8** = T-U-**V**
  * **3** = D-**E**-F
* **Symbolism:** The sequence `5-4-8-3` spells **LIVE**. This represents:
  1. **Living Systems:** Ecological and arboricultural vitality over mechanistic extraction.
  2. **Operational Liveness:** Sovereign, uninterrupted local edge availability without cloud reliance.
  3. **STIM Protocol Alignment:** Verifiable stasis through memory while active in the physical world.

---

## 3. Container Architecture (`forest-workbench`)

The workbench container is defined at `04_Configuration/containers/forest-workbench/Containerfile`.

* **Base Image:** `caddy:2` (distro alpine-based, zero additional package installations needed).
* **Port:** `5483` (both internal container port and host published port).
* **Endpoints:**
  * `GET /`: Forest OS Workbench single-page portal with interactive Mycelium particle background.
  * `GET /api/health`: JSON healthcheck endpoint returning `{"status":"ok","service":"forest-workbench","port":5483,"mnemonic":"LIVE","catalog_version":"1.0.0","tools":33}`.
  * `GET /api/catalog` or `/forestry-tools.json`: Canonical 33-tool JSON dataset.
  * `GET /icons/*`: High-resolution SVG icons for all forestry tools.
  * `GET /01_Docs/*`: Linked technical guides and evidence models.

---

## 4. Project Nomad Registration Specifications

Project Nomad provisions and monitors custom apps through its internal Docker service and MySQL database (`services` table).

### 4.1 Service Definition

| Parameter | Value | Rationale |
|---|---|---|
| **Service Name** | `nomad_custom_forest_tools` | Standard Nomad slug format derived from friendly name |
| **Friendly Name** | `Forest Tools` | Display title on Nomad dashboard |
| **Icon** | `IconPlant` | Tabler icon representing forestry and ecological botany |
| **Category** | `utility` | Groups alongside File Browser, CyberChef, and IT Tools |
| **Port Binding** | `5483:5483` | Maps container port 5483 to host port 5483 |
| **UI Location** | `5483` | Nomad launches `http://<host>:5483` on tile click |
| **Managed Labels** | `com.docker.compose.project=project-nomad-managed`<br>`io.project-nomad.managed=true` | Informs Nomad daemon to track lifecycle |

### 4.2 API Registration Receipt

Registration was verified via the Nomad native REST API:

```bash
# Preflight validation
curl -X POST http://localhost:8080/api/system/services/preflight-custom \
  -H "Content-Type: application/json" \
  -d '{"image": "forest-workbench:1.0.0", "ports": [5483]}'

# App creation
curl -X POST http://localhost:8080/api/system/services/custom \
  -H "Content-Type: application/json" \
  -d '{
    "friendly_name": "Forest Tools",
    "image": "forest-workbench:1.0.0",
    "ports": [{"container": 5483, "host": 5483}],
    "category": "utility",
    "icon": "IconPlant"
  }'
```

---

## 5. Build and Operational Workflow

### Build from Source
```bash
# Build forest-workbench sidecar image locally
bash 03_Automation_Scripts/build_containers.sh workbench

# Build all Tier 3 containers (workbench, forest-r-engine, forest-sim)
bash 03_Automation_Scripts/build_containers.sh all
```

### Verification Probes
```bash
# Healthcheck probe
curl -i http://localhost:5483/api/health

# Catalog probe
curl -s http://localhost:5483/api/catalog | jq '.tools | length'

# Nomad service query
docker exec nomad_mysql mysql -u nomad_user -pUPN3MD4Qgl8Cpl7E9jhjZpDYvr0rSWyD -e \
  "USE nomad; SELECT service_name, friendly_name, installed, ui_location, icon FROM services WHERE service_name = 'nomad_custom_forest_tools';"
```
