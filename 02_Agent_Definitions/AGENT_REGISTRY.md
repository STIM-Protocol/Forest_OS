# Forest OS Agent Definitions

**Version:** 0.1.0
**Purpose:** Canonical blueprint for autonomous agents operating within the Forest OS ecosystem.

---

## Agent Philosophy

Every Forest OS agent is:
- **Goal-directed** — has a clear objective and success criteria
- **Self-documenting** — logs actions to appropriate Forest locations
- **Failure-resilient** — retries with backoff, alerts on persistent errors
- **Observable** — emits structured logs and metrics
- **Protocol-compliant** — respects Heartwood/Cambium standards

---

## Core Agent Registry

### 1. Memory Agent (`agent:forest:memory`)

**Responsibility:** Daily capture, distillation, and memory management.

**Triggers:**
- Heartbeat (every 30 min)
- End-of-day (22:00)
- Manual `/memory flush`

**Actions:**
- Review `memory/YYYY-MM-DD.md` for new entries
- Extract significant learnings, decisions, events
- Update `MEMORY.md` with distilled entries
- Flag contradictions for review

**Success Metric:** `MEMORY.md` grows without becoming noisy; no daily entries lost.

**Log Destination:** `005_JOURNAL/Agent_Logs/Memory_Agent/`

---

### 2. Sync Agent (`agent:forest:sync`)

**Responsibility:** Multi-vault coordination and backup.

**Triggers:**
- Cron: daily 02:00, weekly Sun 04:00
- Manual `forest-sync` command

**Actions:**
- Run `backup_forest.sh` → Google Drive
- Execute `sync_forest_to_brain.py --incremental`
- Prune `COMPOST/` based on retention policy (90-day TTL)
- Generate `SYNC_STATUS.md` report

**Success Metric:** All vaults present in at least two locations; zero sync failures.

**Log Destination:** `005_JOURNAL/Agent_Logs/Sync_Agent/`

---

### 3. Lint Agent (`agent:forest:lint`)

**Responsibility:** Protocol compliance validation.

**Triggers:**
- Pre-commit hook (local)
- Post-write validation (on Forest file creation)
- Daily audit scan

**Actions:**
- Check every `.md` in Forest has matching `.jsonld` (or intentional omission)
- Validate Cambium JSON-LD syntax
- Verify tags exist in `TAG_TAXONOMY.md`
- Confirm UUID format correctness
- Report violations to `FOREST/000_DASHBOARD/LINT_ISSUES.md`

**Success Metric:** 100% of new documents pass lint; no protocol violations accumulate.

**Log Destination:** `005_JOURNAL/Agent_Logs/Lint_Agent/`

---

### 4. Ingest Agent (`agent:forest:ingest`)

**Responsibility:** Transform raw materials into Heartwood.

**Triggers:**
- File drop in `GREENHOUSE/Active/Neocambrian_Academy/04_INGESTION/`
- Manual `forest-ingest <file>`

**Actions:**
- Detect file type (PDF, image, audio, web)
- Route to appropriate extractor (OCR, Whisper, etc.)
- Generate draft Heartwood in `FOREST/002_IDEAS/temp-<topic>/`
- Suggest tags based on content analysis
- Notify human for review

**Success Metric:** >90% of ingested items produce usable draft within 5 minutes.

**Log Destination:** `005_JOURNAL/Agent_Logs/Ingest_Agent/`

---

### 5. Brain Agent (`agent:forest:brain`)

**Responsibility:** Mycelial Brain lifecycle management.

**Triggers:**
- New Forest document with `status/active` and `subject/*`
- Forest document update (major version change)
- Weekly full re-sync

**Actions:**
- Call MCP `brain_create` or `brain_update`
- Record returned `brain_doc_id` in Cambium `relations.brain_id`
- Retry failed ingestions with exponential backoff
- Generate `BRAIN_SYNC_LOG.md` audit trail

**Success Metric:** Brain index size matches Forest active document count (±5%).

**Log Destination:** `005_JOURNAL/Agent_Logs/Brain_Agent/`

---

### 6. Health Agent (`agent:forest:health`)

**Responsibility:** System monitoring and alerting.

**Triggers:**
- Every 15 minutes (continuous)
- Threshold breach detection

**Actions:**
- Check vault sizes (alert if >80% capacity)
- Monitor CPU/memory of Cloud Run services
- Detect duplicate文档 (hash collision)
- Watch for stale agents (no heartbeat in 2h)
- Send Telegram alerts on anomalies

**Success Metric:** Issues detected within 5 minutes; zero alert fatigue.

**Log Destination:** `005_JOURNAL/Agent_Logs/Health_Agent/`

---

## Agent Lifecycle

### Creation
1. Define spec in this directory (`<agent-name>.yaml`)
2. Implement as OpenClaw subagent or Cloud Run service
3. Register in `FOREST/000_DASHBOARD/AGENT_REGISTRY.md`
4. Assign identity card (UUID + public key if needed)

### Operation
- Agents run isolated (`context: "isolated"`) unless they need parent transcript.
- Each agent writes logs to its dedicated `005_JOURNAL/Agent_Logs/<agent>/` folder.
- Heartbeat via `session_status` every 5 min for long-running agents.

### Termination
- Mark `status/archived` in registry
- Move logs to `COMPOST/agent-logs/`
- Remove scheduled triggers

---

## Communication Protocol

Agents communicate via:
- **Direct tool calls** (when one agent invokes another's skill)
- **Shared Forest writes** (agents drop handoff notes in `005_JOURNAL/Agent_Handoffs/`)
- **Event bus** (future: Redis or Pub/Sub for real-time)

All inter-agent messages must include:
```yaml
from: agent:forest:<name>
to: agent:forest:<name> | human:george
timestamp: ISO 8601
correlation_id: UUID
action: <task_type>
payload: { ... }
```

---

*Agent definitions evolve. Add new agents via PR to `GREENHOUSE/Active/Forest_OS/02_Agent_Definitions/`.*
