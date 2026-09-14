> **HISTORICAL DOCUMENT NOTE (FOREST-OS-REPO-ALIGNMENT-001).** This page predates the current lifecycle vocabulary and uses older names (Greenhouse-era paths, "Standardized Truth & Immutable Memory"). The canonical STIM-AI expansion is **Stasis Through Inferred Memory**; the current filesystem model is [FILESYSTEM_MODEL.md](FILESYSTEM_MODEL.md). Retained for provenance.

---
namespace: forest-os.implementation
cycle: 2026-Q2
author: george.steward
timestamp: 2026-05-04T15:00:00Z
source: [file:///ARBORETUM/Active/Forest_OS/Documentation/FOREST_OS_IMPLEMENTATION.md]
lineage: [seed→arboretum→lab→forest]
integrity: sha256:a1b2c3d4e5f6
stim_version: 1.0
type: implementation-documentation
status: operational
---

# Forest OS Implementation Document

**Version:** 2.0  |  **Date:** 2026-05-04  |  **Status:** OPERATIONAL
**Author:** George Steward (Neocambrian Architect)
**System:** Myceliate_Master Sovereign Stack

================================================================================
1. EXECUTIVE SUMMARY
================================================================================

Forest OS is a biomimetic multi-agent operating system designed for digital
sovereignty at industrial scale. It orchestrates distributed intelligence
across hierarchical namespaces (FOREST↔UNDERSTORY↔ARBORETUM) using automated
cron workflows, systemd service supervision, and rclone cloud synchronization.

Unlike traditional knowledge bases, Forest OS treats information as a living
ecosystem with birth (ARBORETUM), maturation (UNDERSTORY), production (FOREST),
and decomposition (COMPOST) phases. Each phase has distinct operational
characteristics, tooling, and governance protocols.

Core Principles:
  • STIM Protocols: Standardized Truth & Immutable Memory
  • Namespace Isolation: Provenance-tracked writes with YAML headers
  • Hermetic Cycles: FOREST/LAB/ARBORETUM/COMPOST lifecycle management
  • Sovereign Automation: Local-first, cron-scheduled, agent-orchestrated
  • Distributed Context: Mycelial Brain MCP for cross-repository retrieval

================================================================================
2. BIOMIMETIC ARCHITECTURE (6-LAYER STACK)
================================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: FOREST              (Production / Mature Systems)              │
│  Path: ~/Myceliate_Master/FOREST/                                       │
│  Scale: 259 dirs, 1,742 files                                           │
│  Role: Fruiting systems, maintained documentation, active business      │
│  Access: Read-optimized, write-governed                                │
│  Sync: Real-time via rclone → forest_drive                             │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: UNDERSTORY          (Experimental / R&D)                      │
│  Path: ~/Myceliate_Master/UNDERSTORY/                                   │
│  Scale: 23,262 dirs, 186,540 files                                      │
│  Role: Technical research, prototype systems, spore protocols          │
│  Access: Full read/write, version-controlled                          │
│  Sync: Scheduled → library_drive                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: ARBORETUM            (Development / Growth)                    │
│  Path: ~/Myceliate_Master/ARBORETUM/                                      │
│  Scale: 448 dirs, 1,904 files                                           │
│  Role: Sprouting projects, new initiatives                             │
│  Access: Active development, frequent writes                           │
│  Sync: On-commit → ARBORETUM_drive                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 4: SEED_BANK          (Active Projects / Germinating)           │
│  Path: ~/Myceliate_Master/SEED_BANK/                                    │
│  Scale: 10,005 dirs, 90,115 files                                       │
│  Role: Current initiatives, client work, active development seeds      │
│  Access: Project-specific, permission-scoped                          │
│  Sync: Incremental → understory_drive (ARBORETUM), library_drive (SEED_BANK) │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 5: COMPOST            (Decomposition / Recycling)               │
│  Path: ~/Myceliate_Master/COMPOST/                                      │
│  Scale: 3 files                                                         │
│  Role: Legacy cleanup, nutrient return, archive compression             │
│  Access: Write-only (automated), read-rare                             │
│  Sync: Monthly → compost_drive                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 6: LEGACY_QUARANTINE  (Isolation / Containment)                │
│  Path: ~/Myceliate_Master/LEGACY_QUARANTINE/                           │
│  Scale: 45,159 dirs, 421,916 files                                      │
│  Role: Security containment, deprecated systems, audit trail            │
│  Access: Read-only, air-gapped where possible                          │
│  Sync: None (isolated) or → understory_drive on approval               │
└─────────────────────────────────────────────────────────────────────────┘

Namespace Conventions:
  • All paths use forward slashes (/) regardless of OS
  • Filenames: kebab-case (hyphen-separated, lowercase)
  • Directories: kebab-case or PascalCase for Projects
  • Extensions: .md for markdown, .jsonld for linked data, .yml for config
  • Headers: YAML frontmatter required in all .md files

================================================================================
3. STIM PROTOCOLS (Standardized Truth & Immutable Memory)
================================================================================

3.1 Provenance Tracking
────────────────────────
Every write operation includes:
  ---
  namespace: forest.005.journal
  cycle: 2026-Q2
  author: george.steward
  timestamp: 2026-05-04T14:30:00Z
  source: [file:///UNDERSTORY/spore-protocol/experiment-042.md]
  lineage: [seed→arboretum→lab→forest]
  integrity: sha256:abc123...
  ---

3.2 Write Governance
─────────────────────
  • Directories have immutable headers (first 50 lines reserved)
  • All modifications append; never modify-history (except corrections)
  • Corrections use [CORR-YYYYMMDD-NNN] tags
  • Deletions move to COMPOST, never rm

3.3 Memory Immutability
───────────────────────
  • Core AGENTS.md never modified after creation (versioned instead)
  • Historical snapshots retained at ~/.hermes/state-snapshots/
  • Quarterly archive to cold storage (compressed + encrypted)

================================================================================
4. AUTOMATION INFRASTRUCTURE
================================================================================

4.1 Cron Schedule (forest_os_cron_manager)
───────────────────────────────────────────
  # ┌───────────── minute (0-59)
  # │ ┌───────────── hour (0-23)
  # │ │ ┌───────────── day of month (1-31)
  # │ │ │ ┌───────────── month (1-12)
  # │ │ │ │ ┌───────────── day of week (0-6)
  # │ │ │ │ │

  # Sync myceliate scripts (every 15 minutes)
  */15 * * * * forest_os_cron_manager.py ~/Myceliate_Master/UNDERSTORY/SYSTEM/sync-myceliate.sh

  # Backup forest (daily at 2:00 AM)
  0 2 * * * forest_os_cron_manager.py ~/Myceliate_Master/backup_forest.sh

  # Compost nudge (every 12 hours)
  0 */12 * * * forest_os_cron_manager.py ~/Myceliate_Master/UNDERSTORY/SYSTEM/compost-nudge.sh

  # Wiki health check (weekly, Sundays 3:00 AM)
  0 3 * * 0 forest_os_cron_manager.py ~/Myceliate_Master/bin/wiki-lint.sh

  # Rclone sync verification (daily 4:00 AM)
  0 4 * * * forest_os_cron_manager.py ~/Myceliate_Master/bin/verify-sync.sh

Mutex Management:
  • Lock file: ~/.hermes/cron.lock
  • PID + timestamp tracking
  • Auto-break stale locks (>1hr old)
  • Prevents overlapping cron executions

4.2 Systemd User Services
────────────────────────────
  hermes-gateway.service:
    - Type: simple
    - Restart: always (5 attempts, exponential backoff)
    - Environment: PATH, VIRTUAL_ENV, HERMES_HOME
    - WorkingDirectory: ~/.hermes/hermes-agent
    - ExecStart: python -m hermes_cli.main gateway run --replace
    - Function: Central message routing + agent spawning

  openclaw-gateway.service:
    - Type: oneshot (triggered)
    - Function: OpenClaw IDE integration

  Custom services in ~/.config/systemd/user/
  Reload: systemctl --user daemon-reload
  Logs: journalctl --user -u hermes-gateway.service -f

4.3 Rclone Remotes
──────────────────
  [forest_drive]
  type = drive
  scope = drive.file
  service_account_file = ~/.config/rclone/forest-sa.json
  team_drive = ABC123

  [library_drive]
  type = drive
  scope = drive
  service_account_file = ~/.config/rclone/library-sa.json
  team_drive = XYZ789

  [ARBORETUM_drive]
  type = s3
  provider = Cloudflare
  env_auth = false
  access_key_id = ${ARBORETUM_KEY}
  secret_access_key = ${ARBORETUM_SECRET}
  endpoint = ${ARBORETUM_ENDPOINT}

  Sync patterns:
    rclone sync ~/Myceliate_Master/FOREST forest_drive:FOREST/ --progress --transfers=8
    rclone sync ~/Myceliate_Master/UNDERSTORY library_drive:LAB/ --backup-dir=library_drive:LAB/backup/$(date +%Y%m%d) --suffix=.bak.$(date +%Y%m%d)

================================================================================
5. AGENT ORCHESTRATION (Hermes Framework)
================================================================================

5.1 Central Controller
──────────────────────
  Process: hermes-cli.main (gateway mode)
  Role: Master orchestrator for all AI agents
  Protocol: MCP (Model Context Protocol)
  Transport: stdio / HTTP / SSE
  Capabilities:
    • Spawn subagents with isolated contexts
    • Delegate parallel workstreams (max 3 concurrent)
    • Tool discovery and dynamic loading
    • Cross-agent memory sharing (via Mycelial Brain)

5.2 Subagent Patterns
─────────────────────
  Leaf Agents (role='leaf'):
    - Execute specific tasks
    - No further delegation
    - Return results to orchestrator
    - Tools: terminal, file, web, vision

  Orchestrator Agents (role='orchestrator'):
    - Can spawn child agents (max depth: 2)
    - Coordinate complex workflows
    - Aggregate results
    - Example: Research coordinator → Literature reader + Synthesizer

5.3 Delegation Workflow
───────────────────────
  1. User request arrives at Hermes gateway
  2. Gateway analyzes complexity (token count, tools needed)
  3. If complex → delegate_task(role='orchestrator')
  4. Orchestrator spawns specialized leaf agents
  5. Results collected and summarized
  6. Final response returned to user
  7. All state logged to memory/YYYY-MM-DD.md

Toolsets Available:
  • terminal: Shell execution (foreground/background)
  • file: Read/write/patch with fuzzy matching
  • web: HTTP requests, browser automation
  • vision: Image analysis (CLIP, SAM)
  • memory: Long-term storage (MEMORY.md)
  • session_search: Cross-session recall
  • cronjob: Schedule recurring tasks
  • mcp: Connect to external MCP servers (Mycelial Brain)

================================================================================
6. KNOWLEDGE MANAGEMENT SYSTEM
================================================================================

6.1 Mycelial Brain MCP
──────────────────────
  URL: https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp
  Function: Distributed knowledge retrieval across repositories
  Features:
    • brain_write(namespace, content, tags): Store with provenance
    • brain_read(path): Retrieve specific item
    • brain_search(query, limit): Semantic search
    • brain_list(): Available knowledge domains
    • stim_write(author, namespace, content): STIM protocol writes
    • log_outcome(action, result): Track experiments

6.2 Directory Structure
───────────────────────
  Myceliate_Master/
  ├── FOREST/                  # Production
  │   ├── 001_PRODUCTION/
  │   ├── 002_OPERATIONS/
  │   ├── 003_FINANCE/
  │   ├── 004_RESOURCES/       # ← Wiki could live here
  │   ├── 005_JOURNAL/
  │   └── 006_BUSINESS/
  |
  ├── UNDERSTORY/              # R&D
  │   ├── spore-protocol-master/    # Agent protocols
  │   ├── SOURCE_CONTROL/          # Versioned code
  │   ├── PRIME_DIRECTIVE_FOLDER_PRESERVATION.jsonld
  │   └── SYSTEM/
  │       └── Scripts/
  │           ├── forest_os_cron_manager.py
  │           ├── backup_forest.sh
  │           └── soil-grower
  |
  ├── ARBORETUM/                 # Development
  │   ├── Neocambrian_Academy/
  │   ├── Restoration_Staging/
  │   └── assets/
  |
  ├── SEED_BANK/               # Active projects
  │   ├── 003_PEOPLE/
  │   ├── 2026/
  │   └── Brain_Export/
  |
  ├── COMPOST/                 # Recycling
  └── LEGACY_QUARANTINE/       # Containment
.openclaw.pre-migration
│   │   │   └── pre-migration/  └── pre-migration/
6.3 Knowledge Flow
───────────────────
  New Information → SEED_BANK (germination)
                    ↓
                ARBORETUM (development)
                    ↓
              UNDERSTORY (experimentation)
                    ↓
                FOREST (production)
                    ↓
              COMPOST (recycling)

  Cross-linking: Mycelial Brain indexes all layers, enabling queries
  like "find all mentions of 'soil protocol' across SEED_BANK and LAB"

6.4 Forest Wiki OS (Karpathy LLM Wiki Integration)
─────────────────────────────────────────────────
  Location: ~/Myceliate_Master/FOREST/004_RESOURCES/Knowledge/LLM_Wiki/
  Purpose:  LLM-maintained knowledge base for synthesized insights
  Paradigm: "LLM as wiki maintainer, human as curator" (Karpathy)
  Layers:   1. Raw Sources (immutable documents: papers, articles, data)
            2. Wiki (LLM-generated markdown: summaries, entities, concepts)
            3. Schema (AGENTS.md: conventions, ingestion workflows)

  Workflow Integration:
    • Automated ingestion of research papers/lab results into Raw Sources
    • Hermes Agent (LLM) maintains Wiki: creates/updates pages, cross-references
    • Mycelial Brain MCP indexes Wiki for semantic search and retrieval
    • Cron job triggers weekly Wiki health checks (linting)
    • Wiki generates summaries/reports for SEED_BANK initiatives

================================================================================
7. LOCAL INFRASTRUCTURE
================================================================================

7.1 Model Serving (Ollama)
───────────────────────────
  Models Available:
    • gemma3n:latest    (2.0 GB) - Primary for fast tasks
    • phi3:mini         (2.2 GB) - Cheap reasoning
    • llama3.2:latest   (2.0 GB) - General purpose
    • llama3.2:3b       (2.0 GB) - Lightweight
    • gemma4:e2b        (7.2 GB) - Heavy reasoning

  Configuration:
    providers.ollama.base_url: http://localhost:11434
    providers.ollama.api_key: ollama
    smart_model_routing.cheap_model: phi3:mini

  Used for:
    • Cron job execution
    • Heartbeat processing
    • File system operations
    • Fast queries (<2s response)
    • Fallback when Kilo unavailable

7.2 Gateway Routing (Kilo + Gemini)
─────────────────────────────────────
  Primary: Kilo Gateway (kilo-auto/free)
    URL: https://api.kilo.ai/api/gateway
    Provider: OpenRouter-compatible
    Models: Claude, Gemini, OpenAI, etc.
    Cost: Free tier

  Fallback: Gemini (quota-limited)
    URL: https://generativelanguage.googleapis.com/v1beta
    Key: env:GOOGLE_API_KEY (currently placeholder)
    Models: gemini-2.5-flash, gemini-3.1-pro
    Status: Quota exhausted (fallback only)

  Configuration Flow:
    1. User request → Smart routing check
    2. Simple (<800 chars, <150 words) → phi3:mini (local)
    3. Complex → Kilo Gateway (free)
    4. Kilo fail → gemini-2.5-flash (quota)
    5. All fail → gemma3n:latest (local)

7.3 Filesystem & Docker
────────────────────────
  Terminal Backend: local
  Docker Image: nikolaik/python-nodejs:python3.11-nodejs20
  Container Resources:
    CPU: 1 core
    Memory: 5 GB
    Disk: 50 GB
  Persistent volumes: Enabled
  Mount CWD: Disabled (security)

================================================================================
8. CONFIGURATION FILES
================================================================================

8.1 Main Config: ~/.hermes/config.yaml
───────────────────────────────────────
  model:
    provider: kilo              # Primary router
    default: kilo-auto/free     # Default model
    base_url: https://api.kilo.ai/api/gateway

  providers:
    gemini:                     # Secondary (quota-limited)
      base_url: https://generativelanguage.googleapis.com/v1beta
      api_key: env:GOOGLE_API_KEY
    ollama:                     # Primary for local
      base_url: http://localhost:11434
      api_key: ollama

  fallback_providers: [ollama]  # Chain: Kilo → Ollama

  smart_model_routing:
    enabled: false              # Disable for now (Gemini quota)
    cheap_model:
      provider: ollama
      model: phi3:mini
    fallback_model:
      provider: ollama
      model: gemma3n:latest

  agent:
    max_turns: 90
    gateway_timeout: 1800
    restart_drain_timeout: 60

8.2 Environment: ~/.hermes/.env
─────────────────────────────────
  # Gateway tokens
  HERMES_GATEWAY_TOKEN=***
  TELEGRAM_BOT_TOKEN=***

  # API keys (currently placeholders)
  GOOGLE_API_KEY=***          # Needs rotation
  GOOGLE_AI_API_KEY=***       # Needs rotation
  KILOCODE_API_KEY=***
  ANTHROPIC_API_KEY=***

  # Integration URLs
  HASS_URL=http://homeassistant.local:8123
  TELEGRAM_HOME_CHANNEL=8470661390

  # Settings
  HERCULES_MAX_ITERATIONS=90

8.3 Systemd: ~/.config/systemd/user/hermes-gateway.service
──────────────────────────────────────────────────────────
  [Unit]
  Description=Hermes Agent Gateway
  After=network-online.target

  [Service]
  Type=simple
  ExecStart=/home/george/.hermes/hermes-agent/venv/bin/python             -m hermes_cli.main gateway run --replace
  WorkingDirectory=/home/george/.hermes/hermes-agent
  Restart=always
  RestartSec=60

  [Install]
  WantedBy=default.target

================================================================================
9. CRITICAL OPERATIONS PROCEDURES
================================================================================

9.1 Starting the System
───────────────────────
  1. Start Ollama:
     $ ollama serve &
     $ ollama pull gemma3n:latest
     $ ollama pull phi3:mini

  2. Start Hermes Gateway:
     $ systemctl --user start hermes-gateway.service
     $ systemctl --user status hermes-gateway.service

  3. Verify models:
     $ hermes health-check
     $ ollama list

  4. Check cron:
     $ crontab -l
     $ systemctl --user status cron.service

9.2 Stopping the System
───────────────────────
  1. Stop Hermes:
     $ systemctl --user stop hermes-gateway.service

  2. Stop Ollama (if needed):
     $ pkill -f "ollama serve"

9.3 Emergency Recovery
───────────────────────
  If gateway crashes:
    $ journalctl --user -u hermes-gateway.service -n 100
    $ cat /home/george/.hermes/sessions/*.json | tail -100
    $ systemctl --user restart hermes-gateway.service

  If cron fails:
    $ systemctl --user restart cron.service
    $ /home/george/Myceliate_Master/UNDERSTORY/SYSTEM/Scripts/forest_os_cron_manager.py --test

  If memory full:
    $ rm -rf ~/.hermes/sessions/*.json   # Keep last 10
    $ rm -rf ~/.hermes/state-snapshots/  # Keep recent

================================================================================
10. MONITORING & HEALTH CHECKS
================================================================================