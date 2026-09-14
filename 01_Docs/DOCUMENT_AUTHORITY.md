# Forest OS Document Authority

**Purpose:** the repository contains several generations of overlapping documents. This map names one **current authoritative source per topic**, and classifies the rest as generated mirrors or historical copies. Edit the authoritative copy; link, don't duplicate.

---

## 1. Authority map

| Topic | Authoritative source | Generated mirror | Historical copy |
|---|---|---|---|
| Filesystem model (lifecycle, zones, Heartwood/Cambium, IDs) | **[01_Docs/FILESYSTEM_MODEL.md](FILESYSTEM_MODEL.md)** | — | `00_Core_Protocols/WORLD_MODEL.md` (2026-04 snapshot, uses Greenhouse vault vocabulary), `01_Docs/FOREST_OS_IMPLEMENTATION.md` §lifecycle, `01_Docs/QUICK_REFERENCE.md` §110-116 |
| Document pattern mechanics (checklists, node updates) | `00_Core_Protocols/HEARTWOOD_CAMBIUM_PATTERN.md` (with the ID-generation correction noted in FILESYSTEM_MODEL §3) | `.jsonld` sidecars in same folder | `Forest_OS/HEARTWOOD_CAMBIUM_PATTERN.md` |
| Forestry tool catalog & workbench | **[01_Docs/FORESTRY_WORKBENCH.md](FORESTRY_WORKBENCH.md)** + `04_Configuration/forestry-tools.json` (data) | `04_Configuration/desktop/forest_workbench.html` dataset (derived view) | `01_Docs/FOREST_OS_PROJECT_HANDOFF_PACK.md`, `01_Docs/M_REPORT_FORESTRY_OSS_001.md`, `01_Docs/FORESTRY_TOOLS_TAXONOMY_AND_RESEARCH.md`, `01_Docs/RESEARCH_BRIEF_FORESTRY_TOOLS.md` |
| Verification & compatibility | **[01_Docs/VERIFICATION_AND_COMPATIBILITY.md](VERIFICATION_AND_COMPATIBILITY.md)** | — | `01_Docs/OPERATIONAL_STATUS.md`, `01_Docs/PROJECT_LAUNCH_COMPLETE.md`, README history |
| World/system narrative (2026-04 state) | — | — | `00_Core_Protocols/WORLD_MODEL.md` (dated snapshot; agent/model names reflect April 2026, not current fleet) |
| Agent model | `doc-202.md` + `02_Agent_Definitions/` (as governed by doc-200) | — | README agent diagram history |
| Ingestion / sync procedures | `00_Core_Protocols/INGESTION_PIPELINE.md`, `00_Core_Protocols/SYNC_PROTOCOLS.md` | `.jsonld` sidecars | `Forest_OS/INGESTION_PIPELINE.md`, `Forest_OS/SYNC_PROTOCOLS.md` — note these describe pre-lifecycle (GREENHOUSE-era) paths; the path defaults in `03_Automation_Scripts/ingest_brain.py` match the historical layout, not the current one |
| Project manifest | `00_Core_Protocols/ROOT_MANIFEST.md` | `Forest_OS/ROOT_MANIFEST.md` (byte-identical at the audited commit) | `Forest_OS/01JWWZ1N-forest-os-project-manifest.*` |
| STIM-AI definition | Canonical expansion: **Stasis Through Inferred Memory**; seven axioms pinned in the [STIM-AI v7.0011 specification](https://github.com/STIM-Protocol/white-paper). Do not redefine the acronym in this repo. | — | README history (Sovereign/Transparent/Immutable/Minimal), `01_Docs/FOREST_OS_IMPLEMENTATION.md` (Standardized Truth & Immutable Memory) — engineering mnemonics, not definitions |
| Governance & cadence | `doc-200.md`, `doc-210.md`, `CONTRIBUTING.md` | — | — |

---

## 2. Deprecation summary (concise)

* **Greenhouse / Garden / Nursery / Laboratory** as the operating taxonomy: **deprecated**. Current vocabulary: Seed → Arboretum → Understory → Forest plus support zones (00_CANOPY, LIBRARY, COMPOST). Historical mentions are context, retained for provenance. Runtime sources still carrying old path defaults (e.g. `ingest_brain.py`) are quarantined from recommended usage until separately corrected with approval — do not follow them.
* **"Real-time health indicators" / "Ready" badges as telemetry:** deprecated as descriptions. They are static snapshot labels — see FORESTRY_WORKBENCH §3.
* **"20/20 passing" as an unconditional badge:** deprecated. The 20-test inventory is real; a passing *result* requires a dated run receipt — see VERIFICATION_AND_COMPATIBILITY §2.
* **`uuidgen -r` produces UUIDv7:** **false.** `uuidgen -r` yields UUIDv4. The 11-char prefixes are display aliases, not UUIDs — see FILESYSTEM_MODEL §3.
* **"22 compiled FVS variants":** unverified for the current image (helper list = 20, container uses upstream image) — see VERIFICATION_AND_COMPATIBILITY §4.
* **Ubuntu "rolling" language / 26.10 parity:** deprecated. Ubuntu uses LTS + interim releases; 26.10 was unreleased at documentation time.
* **36-tool count as the workbench catalog:** the HTML/JSON workbench dataset is 33 tools (+3 supporting applications). 36 counted tools+foundations in the earlier planner inventory. Keep the inventories distinct — see FORESTRY_WORKBENCH §1.

---

## 3. Rules

1. One authoritative source per topic. If two pages disagree, this map decides.
2. Historical copies are not deleted and not silently edited; if correction is essential, add a dated pointer to the authoritative page instead.
3. Generated mirrors (e.g. the workbench HTML dataset) are regenerated from their source; fix the source first.
4. Inbound links were updated together with this page as part of FOREST-OS-REPO-ALIGNMENT-001.
