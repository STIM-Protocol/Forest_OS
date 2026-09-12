#!/usr/bin/env python3
"""
Forest OS Git Publisher — pi-dev automation

Publishes Forest OS changes to GitHub and updates the monorepo submodule pointer.
Safe to run frequently (cron every 15min) or manually.

Usage:
  python forest_os_git_publisher.py [--dry-run] [--force]
  python forest_os_git_publisher.py --status   # just report state

Behavior:
  1. Checks Forest_OS working tree for uncommitted changes
  2. If changes exist, commits with timestamped message
  3. Pushes to configured remote (GitHub)
  4. Updates monorepo submodule pointer (git add + commit)
  5. Logs all actions to ~/.hermes/logs/forest_os_git_publisher.log

Remote configuration:
  - Set remote on bare repo: git -C UNDERSTORY/SOURCE_CONTROL/Forest_OS.git remote add origin <url>
  - Monorepo submodule URL is updated automatically after push

Exit codes:
  0 — published successfully or nothing to do
  1 — uncommitted changes conflict (manual review needed)
  2 — remote not configured
  3 — push failed
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

FOREST_REPO = Path('/home/george/Myceliate_Master/ARBORETUM/Active/Forest_OS')
BARE_REPO = Path('/home/george/Myceliate_Master/UNDERSTORY/SOURCE_CONTROL/Forest_OS.git')
MONOREPO = Path('/home/george/Myceliate_Master')
LOG_FILE = Path('/home/george/.hermes/logs/forest_os_git_publisher.log')

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = LOG_FILE.read_text() if LOG_FILE.exists() else ''
    LOG_FILE.write_text(existing + line + '\n')

def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        log(f"ERROR: {cmd}")
        log(f"  stdout: {result.stdout[:200]}")
        log(f"  stderr: {result.stderr[:200]}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result

def get_remote_url():
    result = run(f"git -C {BARE_REPO} remote get-url origin", check=False)
    return result.stdout.strip() if result.returncode == 0 else None

def status():
    print("=== Forest OS Git Publisher — Status ===\n")
    
    # Check remote
    remote = get_remote_url()
    print(f"Remote: {'configured → ' + remote if remote else 'NOT SET (run: git -C UNDERSTORY/SOURCE_CONTROL/Forest_OS.git remote add origin <url>)'}")
    
    # Check Forest_OS working tree
    result = run("git status --short", cwd=FOREST_REPO, check=False)
    changes = result.stdout.strip()
    print(f"Working tree: {'clean' if not changes else f'{len(changes.splitlines())} changed files'}")
    if changes:
        print("  Changes:")
        for line in changes.splitlines()[:10]:
            print(f"    {line}")
    
    # Check if ahead of remote
    if remote:
        result = run("git rev-list --count @{u}..HEAD 2>/dev/null || echo 0", 
                     cwd=FOREST_REPO, check=False)
        ahead = int(result.stdout.strip() or 0)
        print(f"Ahead of remote: {ahead} commit(s)")
    
    # Monorepo submodule status
    result = run("git submodule status ARBORETUM/Active/Forest_OS", 
                 cwd=MONOREPO, check=False)
    print(f"Monorepo submodule pointer: {result.stdout.strip()}")
    
    return 0 if not changes else 1

def publish(dry_run=False, force=False):
    log("=== Publish run starting ===")
    
    # 1. Verify remote configured
    remote = get_remote_url()
    if not remote:
        log("ERROR: Remote not configured. Aborting.")
        print("Set remote first: git -C UNDERSTORY/SOURCE_CONTROL/Forest_OS.git remote add origin <url>")
        return 2
    
    # 2. Check for uncommitted changes
    result = run("git status --porcelain", cwd=FOREST_REPO, check=False)
    uncommitted = result.stdout.strip()
    if uncommitted and not force:
        log("ERROR: Uncommitted changes detected. Use --force to auto-commit.")
        print("Uncommitted files:")
        print(uncommitted)
        return 1
    
    # 3. Commit any staged/unstaged changes
    if uncommitted:
        log("Committing local changes...")
        run("git add -A", cwd=FOREST_REPO)
        commit_msg = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M')} — forest_os_git_publisher"
        run(f'git commit -m "{commit_msg}"', cwd=FOREST_REPO)
        log("✓ Committed")
    else:
        log("Working tree clean — nothing to commit")
    
    # 4. Push to remote
    log(f"Pushing to {remote}...")
    if dry_run:
        log("[DRY-RUN] Would push to remote")
    else:
        result = run("git push origin main", cwd=FOREST_REPO, check=False)
        if result.returncode != 0:
            log(f"ERROR: Push failed — {result.stderr[:200]}")
            return 3
        log("✓ Pushed to remote")
    
    # 5. Update monorepo submodule pointer
    log("Updating monorepo submodule pointer...")
    run("git add ARBORETUM/Active/Forest_OS", cwd=MONOREPO)
    result = run("git commit -m 'chore(forest-os): update submodule to latest published'",
                 cwd=MONOREPO, check=False)
    if result.returncode == 0:
        log("✓ Monorepo submodule pointer updated")
    else:
        log("No monorepo change (submodule pointer already at latest)")
    
    # 6. Sync submodule URL to use remote (not bare local path)
    remote_url_cfg = f"url = {remote}"
    run(f"git config -f .gitmodules submodule.ARBORETUM/Active/Forest_OS.url {remote}",
        cwd=MONOREPO)
    run("git submodule sync --recursive", cwd=MONOREPO)
    log("✓ Submodule URL synced to remote")
    
    log("=== Publish run complete ===")
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Forest OS Git Publisher (pi-dev automation)')
    parser.add_argument('--dry-run', action='store_true', help='show what would be done')
    parser.add_argument('--force', action='store_true', help='auto-commit uncommitted changes')
    parser.add_argument('--status', action='store_true', help='show status only, no publish')
    args = parser.parse_args()
    
    try:
        if args.status:
            sys.exit(status())
        else:
            sys.exit(publish(dry_run=args.dry_run, force=args.force))
    except Exception as e:
        log(f"FATAL: {e}")
        sys.exit(1)
