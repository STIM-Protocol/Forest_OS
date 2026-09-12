#!/usr/bin/env python3
"""
id: "SYL-103a"
title: "Compost Prospector"
tags: [maintenance, compost, prospecting, forest-os]
created: 2026-05-07
stim_version: 1.0
---
Prospects COMPOST decay zones for files old/isolated enough to merit wisdom extraction.
Moves candidates to COMPOST/Inbox/ for compost_wisdom_extractor to process.
Option B (autonomous prospecting) per Council advisory.
"""
import sys, os, json
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

COMPOST = Path("/home/george/Myceliate_Master/COMPOST")
INBOX = COMPOST / "Inbox"
# Decay zones older than 30 days become candidates
AGE_THRESHOLD_DAYS = 30

def prospector(dry_run=False):
    candidates = []
    now = datetime.now()
    inbox_files = set(INBOX.iterdir()) if INBOX.exists() else set()

    # Walk COMPOST excluding Inbox and hidden
    for root, dirs, files in os.walk(COMPOST):
        root_path = Path(root)
        if root_path == INBOX or root_path in INBOX.parents:
            continue  # skip Inbox processing area
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            if fname.startswith('.'):
                continue
            path = root_path / fname
            if path.is_file():
                # Age check
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                age = now - mtime
                if age.days >= AGE_THRESHOLD_DAYS:
                    candidates.append(path)

    print(f"Found {len(candidates)} candidate files older than {AGE_THRESHOLD_DAYS}d")
    moved = 0
    for cand in candidates:
        # Avoid moving if already in Inbox or already prospected tag? Could check tags, but simple move
        dest = INBOX / cand.name
        if dest.exists():
            # Append timestamp to avoid collision
            dest = INBOX / f"{cand.stem}_{int(cand.stat().st_mtime)}{cand.suffix}"
        if dry_run:
            print(f"  [DRY] Would move: {cand.relative_to(COMPOST.parent)} → Inbox/")
        else:
            cand.rename(dest)
            print(f"  ✓ Moved: {cand.name} → Inbox/")
            moved += 1
            # Emit coordination event
            event_dir = COMPOST / "agent_coordination"
            event_dir.mkdir(parents=True, exist_ok=True)
            event_file = event_dir / f"{datetime.utcnow():%Y%m%d_%H%M%S}_prospector_move.json"
            event = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "agent": "compost_prospector",
                "action": "file_moved",
                "doc_id": cand.stem,
                "details": json.dumps({"src": str(cand.relative_to(COMPOST.parent)), "dst": "Inbox/"})
            }
            event_file.write_text(json.dumps(event, indent=2))

    if not dry_run:
        # Also prune empty dirs in COMPOST
        for root, dirs, files in os.walk(COMPOST, topdown=False):
            root_path = Path(root)
            if root_path == COMPOST:
                continue
            try:
                if not any(root_path.iterdir()):
                    root_path.rmdir()
                    print(f"  🗑️ Removed empty dir: {root_path.relative_to(COMPOST.parent)}")
            except OSError:
                pass  # dir not empty or permission

    print(f"\n✅ Prospector complete: {moved} files moved to Inbox")
    return moved

if __name__ == "__main__":
    dry = '--dry-run' in sys.argv
    prospector(dry_run=dry)
