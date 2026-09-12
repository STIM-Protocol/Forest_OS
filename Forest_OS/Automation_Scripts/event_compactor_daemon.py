#!/usr/bin/env python3
"""
id: "SYL-105"
title: "Event Compactor Daemon"
tags: [maintenance, compaction, sqlite-vec, forest-os]
created: 2026-05-07
modified: 2026-05-07
stim_version: 1.0
---
Purpose: Prevent inode exhaustion from thousands of tiny JSON coordination events.
Ingests COMPOST/agent_coordination/*.json nightly at 03:00, writes to events_ledger.sqlite (sqlite-vec),
deletes raw JSON files after successful compaction.
"""
import json
import sqlite3
import gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

# Directories
EVENTS_DIR = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination"
LEDGER_DIR = Path.home() / "Myceliate_Master" / "UNDERSTORY" / "system" / "event_ledger"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = LEDGER_DIR / "events_ledger.sqlite"

# Retention: keep events for 90 days in ledger (older purged)
RETENTION_DAYS = 90


def init_db():
    """Create SQLite ledger with vector extension support."""
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Core events table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        agent TEXT NOT NULL,
        action TEXT NOT NULL,
        doc_id TEXT,
        details TEXT,
        command TEXT,
        raw_json TEXT,
        ingested_at TEXT NOT NULL
    )
    """)

    # Indexes for fast querying
    cur.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_agent_action ON events(agent, action)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_doc_id ON events(doc_id)")

    conn.commit()
    return conn


def ingest_events(dry_run=False):
    """Read all .json files from EVENTS_DIR and write to ledger."""
    event_files = sorted(EVENTS_DIR.glob("*.json"))
    if not event_files:
        print(f"[{datetime.utcnow():%Y-%m-%d %H:%M:%S}] No events to compact.")
        return 0

    conn = init_db()
    cur = conn.cursor()
    ingested = 0
    errors = []

    for event_file in event_files:
        try:
            with open(event_file, 'r') as f:
                raw = f.read()
                data = json.loads(raw)

            # Normalize fields
            timestamp = data.get("timestamp", "")
            agent = data.get("agent", "unknown")
            action = data.get("action", "unknown")
            doc_id = data.get("doc_id", "")
            details = data.get("details", "")
            command = data.get("command", "")

            cur.execute("""
                INSERT INTO events (timestamp, agent, action, doc_id, details, command, raw_json, ingested_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, agent, action, doc_id, details, command, raw,
                datetime.utcnow().isoformat() + "Z"
            ))

            ingested += 1

            if dry_run:
                print(f"  [DRY] Would compact: {event_file.name}")
            else:
                event_file.unlink()  # delete raw JSON after ingest
                print(f"  ✓ Compacted: {event_file.name}")

        except Exception as e:
            errors.append((event_file.name, str(e)))
            print(f"  ✗ Error on {event_file.name}: {e}")

    if not dry_run:
        conn.commit()

        # Purge old records (older than RETENTION_DAYS)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)).isoformat() + "Z"
        cur.execute("DELETE FROM events WHERE timestamp < ?", (cutoff,))
        purged = cur.rowcount

        conn.close()
        print(f"\n✓ Ingested {ingested} events. Purged {purged} old records (> {RETENTION_DAYS}d).")
    else:
        print(f"\n[DRY RUN] Would ingest {ingested} events, purge old records.")

    if errors:
        print(f"\n⚠️  Errors ({len(errors)}):")
        for fname, err in errors[:5]:
            print(f"  {fname}: {err}")

    return ingested


def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("=== EVENT COMPACTOR — DRY RUN ===\n")
        ingest_events(dry_run=True)
    else:
        print("=== EVENT COMPACTOR — NIGHTLY RUN ===\n")
        ingest_events(dry_run=False)


if __name__ == "__main__":
    main()
