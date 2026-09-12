---
namespace: forest-os.quick-reference
cycle: 2026-Q2
author: george.steward
timestamp: 2026-05-04T15:00:00Z
source: [file:///ARBORETUM/Active/Forest_OS/Documentation/QUICK_REFERENCE.txt]
lineage: [seed→arboretum→lab→forest]
integrity: sha256:c3d4e5f6g7h8
stim_version: 1.0
type: quick-reference
status: operational
---

# Forest OS — Quick Reference Card

**Version:** 2.0  |  **Generated:** 2026-05-04  |  **Status:** OPERATIONAL

## SERVICE COMMANDS
────────────────
```bash
# Start All
systemctl --user start hermes-gateway.service

# Stop All
systemctl --user stop hermes-gateway.service

# Restart
systemctl --user restart hermes-gateway.service

# Status
systemctl --user status hermes-gateway.service

# Logs (follow)
journalctl --user -u hermes-gateway.service -f
```

## MODEL COMMANDS
──────────────
```bash
# List Models
ollama list

# Pull Model
ollama pull gemma3n:latest

# Run Model (interactive)
ollama run gemma3n:latest

# Serve (daemon)
ollama serve &
```

## CRON JOBS
─────────
```bash
# List scheduled jobs
crontab -l

# Edit crontab
crontab -e

# Manual run
/path/to/script.sh

# Test forest_os_cron_manager
forest_os_cron_manager.py --test
```

## RCLONE SYNC
───────────
```bash
# List remotes
rclone listremotes

# Dry run (safe preview)
rclone sync --dry-run ~/Myceliate_Master/FOREST forest_drive:FOREST/

# Full sync with progress
rclone sync ~/Myceliate_Master/FOREST forest_drive:FOREST/ --progress --transfers=8

# Sync with backup
rclone sync ~/Myceliate_Master/UNDERSTORY library_drive:LAB/ \
  --backup-dir=library_drive:LAB/backup/$(date +%Y%m%d) \
  --suffix=.bak.$(date +%Y%m%d)
```

## FILE LOCATIONS
──────────────
```
Hermes Config:    ~/.hermes/config.yaml
Hermes Env:       ~/.hermes/.env
Sessions:         ~/.hermes/sessions/
Snapshots:        ~/.hermes/state-snapshots/
Logs:             ~/.openclaw/logs/
Scripts:          ~/Myceliate_Master/UNDERSTORY/SYSTEM/Scripts/
```

## DOCUMENTATION
─────────────
```
Implementation:   ~/Myceliate_Master/ARBORETUM/Active/Forest_OS/01_Docs/
                  FOREST_OS_IMPLEMENTATION.md

Comparative:      ~/Myceliate_Master/ARBORETUM/Active/Forest_OS/01_Docs/
                  COMPARATIVE_ANALYSIS_KARPATHY_VS_FOREST.md

Protocols:        ~/Myceliate_Master/ARBORETUM/Active/Forest_OS/01_Docs/
```

## KEY DIRECTORIES (Myceliate_Master/)
────────────────────────────────────
```
FOREST/            Production systems          (1,742 files)
UNDERSTORY/        R&D & experiments           (186,540 files)
ARBORETUM/           Development                 (1,904 files)
SEED_BANK/         Active projects             (90,115 files)
COMPOST/           Recycling                   (3 files)
LEGACY_QUARANTINE/ Isolation                   (421,916 files)
```

## TROUBLESHOOTING
───────────────
```bash
# Gateway crash
systemctl --user restart hermes-gateway.service

# Cron failure
systemctl --user restart cron.service

# Memory full
rm -rf ~/.hermes/sessions/*.json   # Keep recent 10
rm -rf ~/.hermes/state-snapshots/

# Rclone connection fail
rclone config reconnect forest_drive:

# Ollama out of memory
ollama run phi3:mini  # Use smaller model
```

## EMERGENCY COMMANDS
────────────────
```bash
# All logs (last 1000 lines)
journalctl --user --no-pager | tail -1000

# Disk usage
du -sh ~/Myceliate_Master/

# Running processes
ps aux | grep -E "hermes|ollama|cron"

# HermeS health check
hermes health-check
```

---
**Forest OS Status**: OPERATIONAL  
**Last Updated**: 2026-05-04  
**Next Review**: 2026-05-11