#!/usr/bin/env python3
"""
FOREST_OS_CRON_MANAGER — file-based mutex for multi-agent cron coordination.
Ensures only one agent (Pi/Hermes/Bodhi) executes scheduled tasks at a time.
"""

import os
import sys
import time
import fcntl
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Optional
# Event logging for coordination
import json
from datetime import datetime
EVENT_DIR = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination"
EVENT_DIR.mkdir(parents=True, exist_ok=True)

def cron_log_event(action: str, cmd: str, details: str = ""):
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "forest_os_cron_manager",
        "action": action,
        "doc_id": "",
        "details": details,
        "command": cmd
    }
    fname = EVENT_DIR / f"{datetime.utcnow():%Y%m%d_%H%M%S}_cron_{action}.json"
    with open(fname, 'w') as f:
        json.dump(event, f, indent=2)


LOCK_DIR = Path.home() / ".hermes"
LOCK_FILE = LOCK_DIR / "cron.lock"
LOCK_TIMEOUT_SECONDS = 3600  # 1 hour stale threshold

def acquire_lock() -> Optional[int]:
    """Acquire exclusive lock via PID file. Returns PID if lock acquired, None if failed."""
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR | os.O_EXCL, 0o644)
        # Lock created fresh — write our PID
        os.write(fd, str(os.getpid()).encode())
        os.fsync(fd)
        return os.getpid()
    except FileExistsError:
        # Lock exists — check if stale
        try:
            with open(LOCK_FILE, 'r') as f:
                lock_pid = int(f.read().strip())
            
            # Check if PID still alive
            try:
                os.kill(lock_pid, 0)  # raises ESRCH if dead
                # PID alive — lock held
                return None
            except ProcessLookupError:
                # Stale lock — steal it
                os.remove(LOCK_FILE)
                return acquire_lock()
        except (ValueError, FileNotFoundError):
            # Corrupted lock — remove and retry
            try:
                os.remove(LOCK_FILE)
            except:
                pass
            return acquire_lock()
    except Exception as e:
        print(f"[CRON_MANAGER] Lock acquisition failed: {e}", file=sys.stderr)
        return None

def release_lock(pid: int):
    """Release lock if we own it."""
    try:
        with open(LOCK_FILE, 'r') as f:
            lock_pid = int(f.read().strip())
        if lock_pid == pid:
            os.remove(LOCK_FILE)
    except Exception:
        pass  # Best effort

def main():
    if len(sys.argv) < 2:
        print("Usage: forest_os_cron_manager.py <command> [args...]", file=sys.stderr)
        sys.exit(1)
    
    pid = acquire_lock()
    if pid is None:
        cron_log_event("lock_contention", " ".join(sys.argv[1:]), "lock_held_by_other")
        print(f"[CRON_MANAGER] Skipping run — lock held by another agent", file=sys.stderr)
        sys.exit(0)  # Not an error — normal contention
    
    try:
        cron_log_event("lock_acquired", " ".join(sys.argv[1:]))
        cmd = sys.argv[1:]
        
        is_hermes_update = (len(cmd) >= 2 and Path(cmd[0]).name == "hermes" and cmd[1] == "update")
        
        if is_hermes_update:
            import subprocess
            res = subprocess.run(cmd)
            if res.returncode == 0:
                print("[CRON_MANAGER] hermes update succeeded. Running post-update json shadow patcher...")
                patch_script = "/home/george/Myceliate_Master/FOREST/007_SYSTEM/scripts/patch_json_shadowing.py"
                if os.path.exists(patch_script):
                    subprocess.run([sys.executable, patch_script])
                else:
                    print(f"[CRON_MANAGER] WARNING: patch script not found at {patch_script}", file=sys.stderr)
            sys.exit(res.returncode)
        else:
            os.execvp(cmd[0], cmd)
    except Exception as e:
        cron_log_event("exec_error", " ".join(sys.argv[1:]), str(e))
        raise
    finally:
        release_lock(pid)
        cron_log_event("lock_released", " ".join(sys.argv[1:]))

if __name__ == "__main__":
    main()
