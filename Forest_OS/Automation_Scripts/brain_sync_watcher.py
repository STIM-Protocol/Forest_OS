#!/usr/bin/env python3
"""
id: "05698db6"
title: "Brain_Sync_Watcher"
tags: [monitoring, sync, mcp, forest-os]
created: 2026-05-02
modified: 2026-05-07
stim_version: 1.0
"""
import sys
import os
import time
import requests
import hashlib
import json
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Concurrency lock for multi-agent coordination
LOCK_DIR = Path.home() / ".hermes" / "forest_locks"
LOCK_DIR.mkdir(parents=True, exist_ok=True)

def file_lock(identifier: str, timeout: float = 30.0):
    """Acquire exclusive file lock."""
    lock_file = LOCK_DIR / f"{hash(identifier) & 0xFFFFFFFF:08x}.lock"
    fd = None; start = time.time()
    while True:
        try:
            fd = os.open(lock_file, os.O_CREAT | os.O_RDWR | os.O_EXCL, 0o644)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return lock_file
        except FileExistsError:
            if time.time() - start > timeout:
                raise TimeoutError(f"Lock timeout: {identifier}")
            time.sleep(0.1)

def file_unlock(lock_file):
    try: lock_file.unlink()
    except: pass

# Event logging
from datetime import datetime
EVENT_DIR = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination"
EVENT_DIR.mkdir(parents=True, exist_ok=True)

def log_event(agent: str, action: str, doc_id: str, details: str = ""):
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": agent, "action": action, "doc_id": doc_id, "details": details
    }
    fname = EVENT_DIR / f"{datetime.utcnow():%Y%m%d_%H%M%S}_{agent}_{action}.json"
    with open(fname, 'w') as f:
        json.dump(event, f, indent=2)

BASE = "https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp"
WATCH_DIR = Path.home() / "Myceliate_Master" / "FOREST" / "007_SYSTEM"
DEBOUNCE_SECONDS = 30
pending_pushes = {}
MAX_RETRIES = 3
INITIAL_BACKOFF = 60

def write_hash_sidecar(doc_id, content, export_dir):
    h = hashlib.md5(content.encode("utf-8")).hexdigest()
    with open(Path(export_dir) / f"{doc_id}.hash", 'w') as f:
        f.write(h)
    return h

def read_hash_sidecar(doc_id, export_dir):
    p = Path(export_dir) / f"{doc_id}.hash"
    return p.read_text().strip() if p.exists() else None

def mcp_read(doc_id):
    r = requests.post(BASE, json={
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": "brain_read", "arguments": {"path": doc_id}}
    }, timeout=30)
    try: return r.json()["result"]["content"][0]["text"]
    except: return ""

def _do_push_with_retry(filepath, retry_count=0):
    doc_id = Path(filepath).stem
    if doc_id.endswith(".hash"): return
    
    lock = None
    try:
        lock = file_lock(f"push_{doc_id}", timeout=60)
        # Critical section
        with open(filepath, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        brain_content = mcp_read(doc_id)
        brain_hash = hashlib.md5(brain_content.encode()).hexdigest() if brain_content else None
        last_hash = read_hash_sidecar(doc_id, WATCH_DIR)
        
        if last_hash and brain_hash and brain_hash != last_hash:
            conflict = WATCH_DIR / f"{doc_id}_CONFLICT_{int(time.time())}.md"
            conflict.write_text(f"# CONFLICT\n# Agent modified brain:\n\n{brain_content}\n")
            log_event("brain_sync_watcher", "conflict", doc_id, str(conflict))
            print(f"  ⚠️  CONFLICT: {doc_id} — saved to {conflict}")
            return
        
        r = requests.post(BASE, json={
            "jsonrpc": "2.0", "id": 1,
            "method": "tools/call",
            "params": {
                "name": "brain_write",
                "arguments": {
                    "path": doc_id, "content": new_content,
                    "tags": ["local-edit", "sync", "george-authored", "human-authority"]
                }
            }
        }, timeout=30)
        
        if r.status_code in (429, 503):
            if retry_count < MAX_RETRIES:
                backoff = INITIAL_BACKOFF * (2 ** retry_count)
                print(f"  ⏳ {r.status_code} for {doc_id}, retry {retry_count+1}/{MAX_RETRIES} in {backoff}s")
                time.sleep(backoff)
                _do_push_with_retry(filepath, retry_count+1)
            else:
                log_event("brain_sync_watcher", "failed", doc_id, "max_retries")
                print(f"  ❌ Max retries exceeded: {doc_id}")
            return
        
        result = r.json()["result"]["content"][0]["text"]
        write_hash_sidecar(doc_id, new_content, WATCH_DIR)
        log_event("brain_sync_watcher", "mcp_write", doc_id)
        print(f"  ✓ Synced: {doc_id}")
        
    except Exception as e:
        if retry_count < MAX_RETRIES:
            backoff = INITIAL_BACKOFF * (2 ** retry_count)
            print(f"  ⚠️  Error: {e}, retry {retry_count+1}/{MAX_RETRIES}")
            time.sleep(backoff)
            _do_push_with_retry(filepath, retry_count+1)
        else:
            log_event("brain_sync_watcher", "error", doc_id, str(e))
            print(f"  ❌ Failed after retries: {e}")
    finally:
        if lock:
            try: lock.unlink()
            except: pass

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".md"): return
        self.schedule(event.src_path)
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".md"): return
        self.schedule(event.src_path)
    def schedule(self, filepath):
        doc_id = Path(filepath).stem
        if doc_id in pending_pushes:
            pending_pushes[doc_id].cancel()
        t = threading.Timer(DEBOUNCE_SECONDS, lambda: _do_push_with_retry(filepath))
        pending_pushes[doc_id] = t
        t.start()

def main():
    print(f"👁  Watching {WATCH_DIR} for changes...")
    print(f"   Debounce: {DEBOUNCE_SECONDS}s, Retries: {MAX_RETRIES}")
    observer = Observer()
    observer.schedule(Handler(), str(WATCH_DIR), recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
