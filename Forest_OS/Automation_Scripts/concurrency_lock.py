#!/usr/bin/env python3
"""
Concurrency Lock — Zombie-Proof File Lock
Provides atomic file-level locking using fcntl.flock (kernel-managed).
Unlike PID-file locks, flock locks are automatically released when the
owning process dies, preventing permanent deadlocks from PID recycling.

Usage: with file_lock("my_doc_id"): ... critical section ...
"""
import fcntl
import os
import time
from contextlib import contextmanager
from pathlib import Path

LOCK_DIR = Path.home() / ".hermes" / "forest_locks"
LOCK_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def file_lock(identifier: str, timeout: float = 30.0):
    """
    Acquire an exclusive flock lock on a file.
    Lock auto-releases if process dies (kernel-managed).
    """
    lock_file = LOCK_DIR / f"{(hash(identifier) & 0xFFFFFFFF):08x}.lock"
    fd = None

    start = time.time()
    while True:
        try:
            fd = os.open(lock_file, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o644)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Lock acquired — write PID for debugging only
            os.write(fd, str(os.getpid()).encode())
            break
        except (FileExistsError, BlockingIOError):
            if time.time() - start > timeout:
                raise TimeoutError(f"Lock timeout: {identifier}")
            time.sleep(0.1)
        except Exception as e:
            if fd:
                os.close(fd)
            raise

    try:
        yield lock_file
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            os.close(fd)
            lock_file.unlink()
        except Exception:
            pass


def test_lock():
    """Simple sanity test."""
    print("Testing file_lock...")
    with file_lock("test_lock"):
        print("  ✓ Lock acquired")
        time.sleep(0.5)
    print("  ✓ Lock released")


if __name__ == "__main__":
    test_lock()
