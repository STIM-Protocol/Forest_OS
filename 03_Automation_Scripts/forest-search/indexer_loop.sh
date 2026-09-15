#!/bin/bash
# indexer_loop.sh: Optional watchdog script for long-running batch indexing.
# Governance: Doc-414 compliant (Zero em dashes, strict claims discipline).
# Note: This is an optional manual maintenance utility. Do not start as a permanent background daemon.

set -euo pipefail

VAULT_ROOT="${FOREST_VAULT_ROOT:-$HOME/Myceliate_Master}"
INDEX_DIR="${VAULT_ROOT}/UNDERSTORY/SYSTEM/forest-index"
DB_PATH="${FOREST_INDEX_DB:-${INDEX_DIR}/forest_index.db}"
LOG_DIR="${INDEX_DIR}"
LOOP_LOG="${LOG_DIR}/loop.log"
BUILD_LOG="${LOG_DIR}/build.log"

mkdir -p "${LOG_DIR}"

last_count=-1
last_change=$(date +%s)

echo "[$(date '+%F %T')] Starting forest indexer loop supervisor (target: ${VAULT_ROOT})" >> "${LOOP_LOG}"

while true; do
  if ! pgrep -f "forest_index.py" >/dev/null; then
    echo "[$(date '+%F %T')] Indexer inactive or died, spawning incremental run" >> "${LOOP_LOG}"
    python3 "${INDEX_DIR}/forest_index.py" \
      --incremental \
      --root "${VAULT_ROOT}" \
      --db "${DB_PATH}" >> "${BUILD_LOG}" 2>&1 &
  fi

  COUNT=$(python3 -c "import sqlite3; db=sqlite3.connect('${DB_PATH}'); print(db.execute('SELECT COUNT(*) FROM files').fetchone()[0]); db.close()" 2>/dev/null || echo 0)
  NOW=$(date +%s)

  if [ "$COUNT" != "$last_count" ]; then
    last_count=$COUNT
    last_change=$NOW
  else
    # Detect stall (no progress in 10 minutes)
    if [ $((NOW - last_change)) -gt 600 ]; then
      echo "[$(date '+%F %T')] Stall detected: file count ($COUNT) unchanged for 10 minutes. Restarting indexer process." >> "${LOOP_LOG}"
      pkill -9 -f "forest_index.py" || true
      last_change=$NOW
    fi
  fi

  sleep 60
done
