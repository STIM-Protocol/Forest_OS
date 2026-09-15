# Forest OS Forestry Workbench

**Authority:** this document is the canonical description of the tool catalog, its source, packaging classes, and the evidence model for status labels. Historical narratives: `01_Docs/FOREST_OS_PROJECT_HANDOFF_PACK.md`, `01_Docs/M_REPORT_FORESTRY_OSS_001.md`, `01_Docs/FORESTRY_TOOLS_TAXONOMY_AND_RESEARCH.md` (see [DOCUMENT_AUTHORITY.md](DOCUMENT_AUTHORITY.md)).

---

## 1. Catalog source of truth

The canonical machine-readable catalog is:

**[`04_Configuration/forestry-tools.json`](../04_Configuration/forestry-tools.json)** — 33 tools plus 3 supporting applications (36 items total; the earlier planner inventory's "36" counted tools and foundations together — see the reconciliation table below).

This file is the sanitized publication of the maintained catalog from the separately maintained **`forest-tools`** planner project (not bundled in this repository). It is reconciled with the workbench HTML dataset; where the JSON and the HTML disagree, **the JSON governs**.

Each tool entry carries: stable `id`, `name`, `group`/`domain`, `upstream_url`, `license`, `tier` (packaging class), `install_method`, `readiness` (catalog disposition), `dependencies`, and `constraints`.

### Reconciliation with the earlier 36-tool inventory

An earlier September 8 planning effort referenced a 36-tool count that included foundation packages. The inventories are different things:

| Inventory | Count | What it is |
|---|---|---|
| `forestry-tools.json` tools | **33** | End-user forestry tools across 7 domains |
| `forestry-tools.json` supporting_applications | **4** | Infrastructure applications (QGIS, GDAL, CloudCompare, Forest Search) |
| Earlier installer/foundations list | 36 | The 33 tools **plus foundation packages** counted as line items |

**Computed total: 33 tools + 4 supporting applications = 37 items when supporting applications are included; the domain tools count remains strictly 33.** Foundation packages remain separately identifiable in the `forest-tools` planner's foundations list and are not merged into the 33.

### Domains (computed from the JSON, count of tools)

| Group | Tools |
|---|---|
| `growth-and-fire` | 7 |
| `point-clouds` | 9 |
| `rings-and-biomass` | 6 |
| `canopy-imagery` | 4 |
| `field` | 3 |
| `canopy-photography` | 2 |
| `audio` | 2 |
| **Total** | **33** |

Note: the workbench HTML dataset and this JSON are **different 33-entry views**, not copies. 28 entries match by normalized name; the JSON includes Capsis, gaplightr, OpenTreeMap, SimpleForest, and SORTIE-ND (which the HTML omits), while the HTML adds CloudCompare, dplPy, ForestTools, pyfia, and pyFVS (not in the JSON's 33 tools). Both total 33 — the overlapping-but-not-identical state is itself a known drift, and reconciliation of the HTML dataset to the JSON is queued. Until then: where they disagree on facts (licenses, tiers), the JSON governs; the HTML remains the rendered snapshot view.

Regenerate counts from the JSON rather than trusting prose.

### License notes

* **Code license ≠ model/data license.** BirdNET-Analyzer's *code* and its *model* are licensed separately; the catalog's single `license` field records the code license, and the model/data terms must be checked upstream before redistribution or commercial use.
* PyTLidar's GPL label was corrected previously and is correct in the catalog — do not re-litigate it.
* The repository's MIT license covers repository code only. It does **not** relicense bundled or cataloged third-party tools.

---

## 2. Packaging classes (tiers)

These are **packaging categories**, not the seven STIM-AI axioms and not the separate action-permission tiers.

| Tier | Mechanism | Examples |
|---|---|---|
| **Tier 1** | Host user-space CLI via `uv tool install --python 3.11 <pkg>` | DeepForest, BirdNET-Analyzer, pyDendron, dplPy, pyfia, pytlidar |
| **Tier 2** | Native distro packages / Flatpak (APT, Pacman) | QGIS, GDAL, CloudCompare, QField |
| **Tier 3** | Container sidecars (Docker/Podman) via repo wrappers | `forest-r-engine` (lidR, TreeLS, rGEDI, BIOMASS, dplR, allodb, ForestTools, hemispheR, treeclim), `forest-sim` (Open-FVS, microfvs) |

Tier 3 wrappers mount the current working directory into the container and are documented in the README's safety notes (not loopback-only by default; writable mounts).

---

## 3. Evidence model: what a label means

Status labels must be interpreted against this grade ladder. **Missing evidence is unknown — it is never an invented pass or failure.**

| Grade | Meaning | Does NOT imply |
|---|---|---|
| **Cataloged** | Present in `forestry-tools.json` | Not installed, not tested |
| **Recipe available** | A build/install path exists (Containerfile, install method) | Not built or run |
| **Installed** | Present on a named host at a recorded version | Not smoke-tested |
| **Smoke-tested** | `--help` / import check passed on a host at a timestamp | Not a functional or scientific validation |
| **Workflow-qualified** | A synthetic workflow ran with defined inputs, expected outputs, and tolerances | Not independent review |
| **Independently reviewed** | A second party reproduced the evidence | — |

Any displayed status must carry: **scope** (which host, which role), **timestamp**, **source/commit or image digest**, and a **receipt** (log, ticket, or document reference). Labels without receipts are downgraded to the highest grade their receipt actually supports.

### Snapshot labels in the workbench HTML

The workbench page (`04_Configuration/desktop/forest_workbench.html`) is a **static page served by a local Python server**. It contains no fetch/WebSocket/health client. Therefore:

* The "Executive Telemetry" cards and per-tool `verified` flags are **hardcoded snapshot values**, not live telemetry and not real-time health indicators.
* Of the 33 catalog entries, the HTML marks 30 `verified: true` and 3 `verified: false` (TreeSeg, TreeQSM, Cell2Fire at the snapshot commit). These flags mean *catalogued-and-snapshot-verified at source*, at best smoke-test grade for the host where that snapshot was taken.
* Service cards ("Ready" badges for RStudio `:8787`, microfvs `:8000`) describe the service **as configured**, not a live probe. A "Ready" badge does not prove the container is currently running.
* The page footer/header should carry the snapshot's source commit and date. Real telemetry would require an actual health client; that is a separate bounded implementation (follow-up R-series), not a prerequisite for honest labels.

---

## 4. Prerequisites and availability

* **`forest-tools` planner:** separately maintained (see `01_Docs/FOREST_OS_PROJECT_HANDOFF_PACK.md` §6 for its workspace location). It provides `forest-tools plan`, `forest-tools verify <group>`, and distro adapters. **It is not bundled in this repository** and the public quick start does not depend on it.
* **Native QGIS / GDAL:** install via your distro's package manager (Tier 2). Not installed by any script in this repository.
* **Tier 1 tools:** install individually with `uv tool install --python 3.11 <pkg>`. Not installed by `install_desktop_launchers.sh`.
* **Tier 3 containers:** `./03_Automation_Scripts/build_containers.sh all` — large downloads, multi-minute builds, and (for Open-FVS) upstream licensing considerations. Optional; not needed to read documentation or serve the workbench.

### PATH reality check

`install_desktop_launchers.sh` symlinks exactly four commands into `~/.local/bin`: `forest-workbench`, `forest-rstudio-launch`, `forest-sim-launch`, `forest-deepforest-launch`. It does **not** install `forest-r`, `forest-sim`, or `forest-tools`. Ensure `~/.local/bin` is on PATH for the launcher commands themselves.

---

## 5. Recipes and snippets

The workbench "Field Pipelines" recipes and the wizard's generated bash snippets are **examples**, not validated production workflows:

* Wizard goal-matching uses OR-based branch logic and can recommend a recipe whose input type does not match your data — always check the input column before running.
* Some snippets are templates with commented-out analysis calls; they will not produce scientific output until completed.
* Label status: examples until each pipeline has a dated, host-scoped run receipt (see the evidence ladder above). End-to-end scientific qualification is a separate follow-up (R4) requiring synthetic fixtures, CRS/units checks, expected outputs, and tolerances.

---

## 6. Preserved material

The Everforest palette, icons, recipe texts, and the manual content of the workbench page are retained. This document governs their *interpretation*, not their design.
