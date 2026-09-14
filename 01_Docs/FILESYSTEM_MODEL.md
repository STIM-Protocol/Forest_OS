# Forest OS Filesystem Model

**Authority:** this document is the canonical guide to the Forest OS file-structure model. Historical and duplicated descriptions live in `00_Core_Protocols/WORLD_MODEL.md`, `01_Docs/FOREST_OS_IMPLEMENTATION.md`, `01_Docs/QUICK_REFERENCE.md`, and `Forest_OS/` — see [DOCUMENT_AUTHORITY.md](DOCUMENT_AUTHORITY.md) for routing.

Forest OS distinguishes three layers that are often conflated:

1. **The operating environment** — Forest OS as a whole: a Linux-based environment combining the file model, agent workflows, and the forestry workbench. The filesystem taxonomy is a subsystem, not the whole of Forest OS.
2. **The vault lifecycle and support zones** — where content lives and how it matures.
3. **The knowledge representation** — how a single item is encoded (Heartwood/Cambium).

---

## 1. Lifecycle stages and support zones

The lifecycle vocabulary is:

```
Seed  →  Arboretum  →  Understory  →  Forest
```

On an operating machine these appear as directories. Actual directory spellings matter and are not inferred from stage names — note the bank suffix:

| Directory | Stage/zone | Role |
|---|---|---|
| `SEED_BANK/` | Seed | Capture and intake: downloads, raw field data, unprocessed material |
| `ARBORETUM/` | Arboretum | Developing projects and active work |
| `UNDERSTORY/` | Understory | Supporting system and research functions. Distinct root-of-trust/system content lives separately from experimental work inside this zone |
| `FOREST/` | Forest | Mature knowledge and operating projects, organized in numbered topic buckets |

Support zones sit alongside the lifecycle and do not participate in it:

| Directory | Role |
|---|---|
| `00_CANOPY/` | Consolidated project/migration views and the visualizer. A **view** over authoritative records — rebuildable, never a second database |
| `LIBRARY/` | Source, reference, and archive material. Brain exports are private by default |
| `COMPOST/` | Retired, superseded, or candidate-for-review material. Not automatic trash; deletion still requires a decision |

Other support directories may exist on a given machine (quarantine, tools, backups). Document only what is actually present.

**What this is not:** the older **Greenhouse / Garden / Nursery / Laboratory** names (2026-04 era documents, and path defaults in some automation scripts) are historical. They are retained in old documents for provenance. A path string inside `03_Automation_Scripts/ingest_brain.py` or similar is evidence of a stale source default, not proof that the path is deployed or that the script is scheduled anywhere — find the caller and configuration before changing runtime behavior.

---

## 2. Forest topic buckets

Mature content inside `FOREST/` uses numbered buckets. The buckets actually in use on the reference machine include:

```
FOREST/
├── 000_DASHBOARD/
├── 001_PROJECTS/
├── 002_IDEAS/          (and 002_KANBAN on some machines)
├── 003_PEOPLE/
├── 004_RESEARCH/       (and 004_RESOURCES on some machines)
├── 005_JOURNAL/
├── 006_BUSINESS/
└── 007_SYSTEM/         (system root-of-trust content)
```

Bucket numbering has grown organically and varies slightly between machines; document the live structure rather than inventing missing categories. Content is placed in the correct bucket by type; a `005_JOURNAL` item is a journal entry, regardless of project.

---

## 3. Heartwood/Cambium knowledge pairs

Every knowledge item is a **pair** sharing one stable ID:

* **Heartwood** — the content file (`<ID>-<slug>.md`).
* **Cambium** — the metadata sidecar (`<ID>-<slug>.jsonld`) carrying `@context`, `id`, `type`, `tags`, and `relations`.

Heartwood/Cambium is a **representation** pattern, independent of the directory lifecycle: the same pair exists at every stage. It is not a maturity level and not a competing directory scheme.

### Mutability — what is actually immutable

* **Original evidence** (raw field data, source captures) is immutable: retain it, never edit it in place.
* **Released versions** of a document are immutable as *versions*: a major revision gets a new ID and a `supersedes` relation; the old file is retained.
* **Working content** is editable in place: update the Heartwood `.md`, increment `updated` in Cambium, keep the ID. This is explicitly permitted by `00_Core_Protocols/HEARTWOOD_CAMBIUM_PATTERN.md` ("Updating Existing Nodes").
* The filesystem itself enforces nothing. Immutability here is a convention, not a mechanism; do not describe the metaphor as an enforcement property.

### Identifiers (corrected)

The checklist in `HEARTWOOD_CAMBIUM_PATTERN.md` historically said to "Generate UUIDv7: `uuidgen -r`". **That claim is wrong on two counts:**

1. `uuidgen -r` generates a random UUID (**UUIDv4**), not UUIDv7. Version 7 is a time-ordered UUID; no standard `uuidgen` flag produces it.
2. The 11-character prefixes seen in practice (e.g. `01JWWZ1M`) and the short timestamp+random string built by `harden_forest.py` are **display aliases**, not UUIDv7. They are lexicographic time-sortable, which is a useful property, but they are not standards-compliant UUIDs.

**Current practice:** existing IDs are preserved exactly as-is. Display aliases remain aliases; never treat them as full UUIDs or rekey files to "fix" them.

**For genuinely new UUIDv7 IDs** (only when a runtime actually provides a v7 generator):

* Python ≥ 3.13 has no stdlib v7; use `uuid7` (PyPI) or implement RFC 9562 §5.7 (48-bit big-endian Unix millisecond timestamp in the first 12 hex digits, version nibble `7`, variant nibble `8`, 12 bits of monotonic counter/random, 62 random bits). Always verify the version nibble is `7` and the variant bits are `10x` after generation.
* Do **not** change deployed ID generation as part of documentation work — that is a separate source/runtime repair (tracked as follow-up R3). No bulk rekeying, no renaming of existing files, ever, under a documentation task.

---

## 4. A synthetic worked example

The following is **synthetic**, used to illustrate the model. It describes no real file.

A field crew inventories 40 trees on a plot:

1. **Seed:** The raw tally CSV and drone orthomosaic land in `SEED_BANK/Inbox/field_2026_06_12/`. The originals are never edited again (immutable evidence).
2. **Arboretum:** Work begins in `ARBORETUM/Active/plot_42_inventory/`. A Heartwood/Cambium pair is created: `0198F2A4-plot-42-first-pass.md` + `.jsonld` (ID generated by a real UUIDv7 generator, version nibble checked). Analysis notebooks, QC scripts, and the first draft live here; the raw files are referenced by `relations`, never moved.
3. **Understory:** The QC methodology is generic enough to become a reusable procedure and is filed under the Understory zone's research functions, with a `related` link back to the plot work.
4. **Forest:** The validated inventory report is promoted to `FOREST/001_PROJECTS/plot_42/` as `0198F2B7-plot-42-inventory-v1.md`. Promotion moves the pair and updates relations; nothing is duplicated by hand.
5. **Supersession:** A boundary correction produces `0199A1C3-plot-42-inventory-v2.md` with `supersedes: 0198F2B7`. The v1 file is **retained**, its Cambium gains a `superseded_by` relation, and the v1 Heartwood gains a one-line pointer to v2.
6. **Retirement:** The superseded scratch workspace from Arboretum eventually goes to `COMPOST/` — a deliberate decision, not an automatic purge.

Throughout: Canopy views that display this project are regenerated from the records; if the views and the records disagree, the records win.

---

## 5. Configuration separation

* **Ubuntu and Omarchy (Arch) dotfiles stay separate.** They are different hosts with different package managers and conventions; a setting correct on one is not automatically correct on the other.
* **Indexes, Canopy views, and the workbench page are rebuildable projections.** They can be regenerated from records and configuration at any time. Treat them as outputs, not sources.
* **Repository vs vault:** this Git repository is source; the operating vault (`~/Myceliate_Master/` on the reference machine) is personal data. Public documentation must only ever show a **synthetic** vault example — never real document names, people, or project titles from an operating vault.

---

*Established as the canonical filesystem guide by FOREST-OS-REPO-ALIGNMENT-001, September 2026. Historical descriptions remain in place under `00_Core_Protocols/` and `Forest_OS/`, routed via [DOCUMENT_AUTHORITY.md](DOCUMENT_AUTHORITY.md).*
