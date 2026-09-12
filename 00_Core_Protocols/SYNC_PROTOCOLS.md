# Sync Protocols: Multi-Vault Coordination

**Version:** 1.0.0
**Status:** Operational
**Scope:** Rules for synchronizing data across Forest, Library, Greenhouse, Understory, Compost, and Brain

---

## 1. Core Sync Principles

1. **Single source of truth per vault** — Forest holds canonical working knowledge; Library holds source binaries; Compost is archive.
2. **One-way flow into Forest** — once a document enters Forest, edits stay in Forest. Do not overwrite from Library.
3. **Two-way mirror between Compost and Drive** — Compost is the decay zone; Drive archive is backup.
4. **Brain is read-only search index** — never write directly to Brain; always go through Forest → brain_create.

---

## 2. Vault Relationships

```
[Library] --(extract)--> [Forest] --(publish)--> [Brain]
   |                                         |
   v                                         v
[Compost] <--(archived)--- [Forest .trash]   [Query API]
```

---

### 2.1 Forest ↔ Library

**Direction:** Library → Forest (extraction only)

**When:**
- New PDF added to `LIBRARY/PDF_Refugia/`
- New image batch copied to `LIBRARY/Media/`

**Process:**
1. Run `extract_library.sh` (OCR + text extraction)
2. Output `.md` text files to `LIBRARY/_extracted/`
3. Human reviews and moves relevant extracts to appropriate Forest bucket
4. Originals remain in Library untouched

**Never:** Edit Library binary directly from Forest.

---

### 2.2 Forest ↔ Greenhouse

**Direction:** Forest → Greenhouse (code/config migration)

**When:**
- Agent skill matured and ready for versioning
- Protocol needs to graduate from experiment to standard

**Process:**
1. Identify document in Forest with `status/experimental` or `bucket/greenhouse`
2. Promote by moving to `GREENHOUSE/Active/` and adding Git tracking
3. Commit to `greenhouse-main` branch
4. Update Forest document `relations` with `see_also: green-house-repo-url`

**Reverse:** Deprecated Greenhouse code moves to `Compost/` and Forest links are updated.

---

### 2.3 Forest ↔ Understory

**Direction:** Bidirectional but asymmetric

**Lab → Forest:** When a design doc stabilizes, copy to `004_RESOURCES/Design_Docs/` and link back to Lab.

**Forest → Lab:** Research outputs from `004_RESOURCES/` that require prototyping get a companion project in `UNDERSTORY/RESEARCH/`.

**Rule:** Lab is for *unstable* work-in-progress; Forest is for *stable* references.

---

### 2.4 Forest ↔ Compost

**Direction:** Forest → Compost (decay)

**When:**
- Document marked `status/deprecated` or `status/archived`
- Version superseded by newer doc (`supersedes` relation set)
- Duplicate identified

**Process:**
1. Move file to `COMPOST/<bucket>/<original_path>` preserving directory structure
2. Update Forest: mark `status/archived`, add `relations.moved_to: "compost/..."`
3. Run backup script: `backup_forest.sh` saves state before major pruning

**Two-way mirror:** `COMPOST/Drive_Archive/` contains Google Drive backup of same files for long-term cold storage.

---

### 2.5 Forest ↔ Brain

**Direction:** Forest → Brain (publish only)

**Trigger:** Any document in Forest with `status/active` and `subject` tag may be ingested.

**Process:**
1. Call `brain_create` or `brain_update` via MCP with document content and metadata
2. If success: document now searchable via `brain_search`
3. Record `brain_doc_id` in Cambium `relations.brain_id`
4. Never delete from Brain directly — Forest is source of truth

**Updates:** If Heartwood changes significantly (major version bump), call `brain_update`. Minor edits: optional.

**Bulk re-sync:** Run `sync_forest_to_brain.py` periodically (weekly) to catch missed documents.

---

## 3. Scheduled Sync Operations

| Cron Schedule | Operation | Script |
|---------------|-----------|--------|
| Daily 02:00 | Full Forest backup to Drive | `backup_forest.sh` |
| Daily 03:00 | Heartbeat memory capture | OpenClaw internal |
| Weekly Sun 04:00 | Forest → Brain incremental sync | `sync_brain.py --incremental` |
| Monthly 1st | Compost pruning audit | `prune_compost.sh --dry-run` |
| Quarterly | Full vault health check | `vault_audit.py` |

---

## 4. Conflict Resolution

**Scenario:** Same document edited both in Forest and Library (violates principle).

**Resolution:**
1. Forest version *always* wins. Library is source material only.
2. If Forest doc derived from Library PDF is updated, regenerate PDF export if needed.
3. Log conflict in `FOREST/000_DASHBOARD/CONFLICT_LOG.md` with resolution.

**Scenario:** Two Forest docs cover same topic.

**Resolution:**
1. Merge content into higher-level doc.
2. Mark duplicates `status/deprecated` and move to Compost.
3. Add `relations.superseded_by` link.

---

## 5. Observability

**Logs:**
- All sync operations log to `~/sync_logs/forest-sync-YYYY-MM-DD.log`
- Errors send Telegram alert to George

**Metrics:**
- `forest_document_count`
- `brain_indexed_count`
- `compost_size_gb`
- `sync_success_rate`

**Dashboard:** `FOREST/000_DASHBOARD/SYNC_STATUS.md` auto-updates via cron.

---

## 6. Recovery Procedures

**Forest corruption:** Restore from latest Drive backup (`forest_drive` remote) or local `backup_forest.sh` tarball.

**Brain data loss:** Re-ingest entire Forest (slow but complete).

**Library loss:** Restore from original sources (PDFs may be unrecoverable if not backed up).

**Compost restore:** If file moved incorrectly, retrieve from `COMPOST/Drive_Archive/` Google Drive.

---

*Sync protocols are operating procedures. Update after any infrastructure change.*
