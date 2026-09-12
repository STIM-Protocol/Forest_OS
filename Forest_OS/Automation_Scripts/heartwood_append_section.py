#!/usr/bin/env python3
"""
id: "SYL-101b"
title: "Heartwood Section Appender"
tags: [mcp-tool, heartwood, versioned-patch, forest-os]
created: 2026-05-07
stim_version: 1.0
---
Append a new markdown section to an existing .md file with full diff logging.
Creates a unified diff in COMPOST/agent_coordination/edits/ before modifying file.
Tags file with needs-review, autonomous-edit.
"""
import sys, json, difflib
from pathlib import Path
from datetime import datetime, timezone

FOREST = Path.home() / "Myceliate_Master" / "FOREST"
EDITS_DIR = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination" / "edits"
EDITS_DIR.mkdir(parents=True, exist_ok=True)

def append_section(rel_path: str, heading: str, content: str, summary: str = ""):
    full = FOREST / rel_path
    if not full.exists():
        raise FileNotFoundError(f"No such Heartwood file: {rel_path}")

    original = full.read_text(encoding='utf-8')

    # Determine frontmatter
    if original.startswith('---'):
        fm_end = original.find('\n---\n') + 4
        front = original[:fm_end]
        body = original[fm_end:]  # includes everything after closing ---
    else:
        front = ""
        body = original

    # Build new section
    new_section = f"\n## {heading}\n\n{content}\n"

    # New file content: front + body + new_section (no duplicate front)
    patched = front + body.rstrip("\n") + new_section

    # Compute unified diff (original vs patched)
    diff_lines = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        patched.splitlines(keepends=True),
        fromfile=f"a/{rel_path}",
        tofile=f"b/{rel_path}",
        lineterm=""
    ))
    diff_text = "".join(diff_lines)

    # Write diff to edits ledger
    doc_id = Path(rel_path).stem
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    diff_path = EDITS_DIR / f"{doc_id}_{ts}.diff"
    meta = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "Sylvan_The_Beaver",
        "doc_id": doc_id,
        "summary": summary or f"Append section: {heading}",
        "status": "needs-review"
    }
    diff_path.write_text("---\n" + json.dumps(meta, indent=2) + "\n---\n" + diff_text, encoding='utf-8')

    # Tag frontmatter (append needs-review, autonomous-edit)
    if front:
        lines = front.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('tags:'):
                try:
                    tags = json.loads(line.split(':',1)[1].strip())
                except:
                    tags = []
                for t in ['needs-review', 'autonomous-edit']:
                    if t not in tags:
                        tags.append(t)
                lines[i] = f"tags: {json.dumps(tags)}"
                break
        new_front = '\n'.join(lines)
    else:
        new_front = "---\ntags: [\"needs-review\", \"autonomous-edit\"]\n---\n"

    # Write patched file with new frontmatter tags
    full.write_text(new_front + body.rstrip("\n") + new_section, encoding='utf-8')

    return {
        "status": "appended_and_tagged",
        "doc_id": doc_id,
        "rel_path": rel_path,
        "diff_path": str(diff_path.relative_to(Path.home())),
        "heading": heading,
        "bytes_added": len(new_section)
    }

if __name__ == "__main__":
    args = json.loads(sys.stdin.read())
    result = append_section(**args)
    print(json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}))
