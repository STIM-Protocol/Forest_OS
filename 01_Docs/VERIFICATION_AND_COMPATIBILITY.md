# Forest OS Verification and Compatibility

**Authority:** this document is the canonical record of what is verified, on what platform, at what scope, and what remains unknown. It absorbs and supersedes the verification claims scattered through the README history, `01_Docs/OPERATIONAL_STATUS.md`, `01_Docs/PROJECT_LAUNCH_COMPLETE.md`, and `01_Docs/FOREST_OS_PROJECT_HANDOFF_PACK.md` §5 (see [DOCUMENT_AUTHORITY.md](DOCUMENT_AUTHORITY.md)).

**Standing rule:** every claim below carries a scope and a source. "Unknown" is a valid, preferred entry over an invented pass or failure. Source parsing is not runtime qualification.

---

## 1. Platform evidence

| Platform | Role | Status | Evidence |
|---|---|---|---|
| Ubuntu 26.04 LTS | Development host (owner-reported) | In use | Owner report; no archived machine receipt in this repo |
| Ubuntu LTS / interim releases | Support target | Documented target | Ubuntu publishes LTS (e.g. 26.04) and interim releases; Ubuntu is not a rolling distribution. 26.10 was a future release at documentation time — any parity claim for it is untested |
| Arch Linux / Omarchy | Alternative target | Documented target | Dotfiles and environments remain separate from Ubuntu's; no parity receipt exists |
| Installable image | Future ambition | **Not a deliverable** | No tested ISO/image exists; the repository is source only |

**Not claimed:** host/guest parity, cross-distro parity, "upgrades cannot break the scientific stack", zero-footprint isolation. Containerization reduces dependency-collision risk; shared-kernel, driver, hardware, storage, and integration failure modes remain.

---

## 2. Component test inventory (source-level)

Static inventory of `05_Tests/` — **20 test functions**:

| Module | Count | Inspects |
|---|---|---|
| `test_cli_wrappers.py` | 7 | bash syntax, CLI help flags, exit codes |
| `test_container_recipes.py` | 6 | Containerfile directives, package manifests |
| `test_desktop_launchers.py` | 7 | FreeDesktop validation, SVG icons, server HTTP 200 |

**Interpretation:**

* This is a **source inventory**, not a fresh execution result. A dated run receipt (passed/failed/skipped + host identity + commit) gets recorded below only when an actual run happens.
* The desktop module can start the workbench web server on a fixed port and may skip if its validator is absent. Do not run blind test discovery on a workstation where the port is busy; a pre-existing service on that port is not your test result.
* These tests do **not** qualify the five field-pipeline recipes end-to-end, nor the scientific correctness of canopy, biomass, tree-ring, or growth outputs.

**Run receipts:** *(none recorded yet — unknown until a dated, host-scoped run exists)*

---

## 3. Host tool verification (owner-reported, September 2026 scope)

From the handoff pack's verification table. Scope: one Ubuntu host, smoke-test grade (`--help`/CLI startup), not workflow qualification.

| Tool | Grade | Receipt |
|---|---|---|
| BirdNET-Analyzer | Smoke-tested (`--help` exit 0) | Handoff pack §5 table, 2026-09-11 |
| DeepForest | Smoke-tested (v2.1.0 CLI operational) | Handoff pack §5 table, 2026-09-11 |
| pyDendron | Smoke-tested (v1.7.5 CLI operational) | Handoff pack §5 table, 2026-09-11 |
| QGIS | Installed (v3.42.3, APT) | Handoff pack §5 table |
| GDAL | Installed (v3.10.2, `gdal-bin`) | Handoff pack §5 table |

A `--help` check is not a complete ecological analysis test. Newer installed versions on the machine supersede any earlier planning values; do not downgrade receipts to match older notes.

---

## 4. Container recipes

| Aspect | Status | Note |
|---|---|---|
| Base images | `:latest` (both recipes) | Unpinned; rebuilds may drift. Image digests not yet recorded — **unknown** |
| GitHub dependencies | Unpinned revisions | Recorded as a reproducibility gap (follow-up R3) |
| R package guard | `install_packages.R` fails if required packages cannot load | Useful guard; its printed checks are not archived build receipts |
| `forest-sim` FVS variants | **Unknown** | The compile helper's list has 20 entries and tolerates failures; the current Containerfile starts from an upstream FVS image and does not invoke the helper. The helper neither proves nor disproves the image's actual variant inventory — inspect the exact image and capture its executable list before claiming any count (20, 22, or otherwise) |
| Reproducibility posture | Repeatable-in-practice, not reproducible-by-pin | See README §7 |

---

## 5. Skipped checks and known unknowns

* No independent synthetic scientific workflow has been run (follow-up R4).
* No archived image digests or package-version manifests.
* No machine inventory or hardware receipt is published (and none should be — private data).
* Actual listening addresses of the workbench server and container services have not been verified from this repo's documentation task; see the README safety notes and follow-up R1.
* The `forest-tools` planner's per-group `verify` commands exist in that separate project; their outputs have not been independently reviewed here.

---

## 6. How to add a receipt

When a check actually runs, append a row here with: **date, host role (dev host / guest / CI), commit or image digest, exact passed/failed/skipped counts, and the receipt location.** Do not edit historical receipts; supersede them.
