#!/usr/bin/env python3
"""
id: "SYL-101"
title: "brain_suggest_patch MCP Tool"
tags: [mcp-tool, writeback, versioning, forest-os]
created: 2026-05-07
modified: 2026-05-07
stim_version: 1.0
---
Purpose: Enable Sylvan to propose edits to Forest files without overwriting.
All edits are versioned patches (unified diff) + STIM frontmatter preserved.
Gate: Changes tagged `needs-review, autonomous-edit` until human approves.
"""
import sys
import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

# MCP endpoint
BASE = "https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp"

# Forest root
FOREST = Path.home() / "Myceliate_Master" / "FOREST"

# Edits ledger (for diff storage)
EDITS_DIR = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination" / "edits"
EDITS_DIR.mkdir(parents=True, exist_ok=True)


def mcp_call(method: str, params: Dict[str, Any]) -> Dict:
    import requests
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": f"tools/call",
        "params": {
            "name": method,
            "arguments": params
        }
    }
    r = requests.post(BASE, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["result"]


def read_forest_file(rel_path: str) -> str:
    """Read file from Forest, verify exists."""
    full = FOREST / rel_path
    if not full.exists():
        raise FileNotFoundError(f"Forest file not found: {rel_path}")
    return full.read_text(encoding='utf-8')


def write_diff_file(doc_id: str, diff_text: str, summary: str) -> Path:
    """Write unified diff to edits ledger with metadata."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    fname = f"{doc_id}_{ts}.diff"
    path = EDITS_DIR / fname
    meta = {
        "doc_id": doc_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "Sylvan_The_Beaver",
        "summary": summary,
        "status": "needs-review"
    }
    content = "---\n" + json.dumps(meta, indent=2) + "\n---\n" + diff_text
    path.write_text(content, encoding='utf-8')
    return path


def apply_patch(original: str, patch_operation: Dict[str, Any]) -> str:
    """
    Apply a structured patch to markdown content.
    patch_operation = {
        "operation": "append" | "prepend" | "replace_section" | "insert_after",
        "section": "## Title" (optional),
        "content": "new markdown text",
        "summary": "human-readable description"
    }
    Returns patched content string.
    """
    op = patch_operation["operation"]
    new_content = patch_operation.get("content", "")
    summary = patch_operation.get("summary", "(no summary)")

    if op == "append":
        return original.rstrip("\n") + f"\n\n<!-- autonomous-edit: {summary} -->\n{new_content}\n"

    elif op == "prepend":
        return f"<!-- autonomous-edit: {summary} -->\n{new_content}\n\n" + original.lstrip("\n")

    elif op == "insert_after":
        section = patch_operation.get("section", "")
        if section and section in original:
            parts = original.split(section, 1)
            return parts[0] + section + f"\n\n<!-- autonomous-edit: {summary} -->\n{new_content}\n" + parts[1]
        else:
            raise ValueError(f"Section not found: {section!r}")

    elif op == "replace_section":
        section = patch_operation.get("section", "")
        if section and section in original:
            return original.replace(section, f"<!-- autonomous-edit: {summary} -->\n{new_content}\n")
        else:
            raise ValueError(f"Section not found: {section!r}")

    else:
        raise ValueError(f"Unknown operation: {op}")


def suggest_patch(rel_path: str, patch_operation: Dict[str, Any], tags_override: list = None) -> Dict[str, Any]:
    """
    MCP tool: Sylvan calls this to propose an edit.
    Steps:
    1. Read original from Forest
    2. Apply structured patch
    3. Compute unified diff
    4. Write .diff to COMPOST/agent_coordination/edits/
    5. Tag original file with `needs-review, autonomous-edit`
    6. Return patch metadata + diff path
    """
    doc_id = Path(rel_path).stem

    # 1. Read original
    original = read_forest_file(rel_path)

    # 2. Apply patch
    try:
        patched = apply_patch(original, patch_operation)
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({"error": str(e), "stage": "apply_patch"})
            }]
        }

    # 3. Compute unified diff (simple line-based)
    import difflib
    diff_lines = list(difflib.unified_diff(
        original.splitlines(keepends=True),
        patched.splitlines(keepends=True),
        fromfile=f"a/{rel_path}",
        tofile=f"b/{rel_path}",
        lineterm=""
    ))
    diff_text = "".join(diff_lines)

    if not diff_text.strip():
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({"error": "Patch produced no changes", "stage": "diff_check"})
            }]
        }

    # 4. Write diff to edits ledger
    summary = patch_operation.get("summary", "(no summary)")
    diff_path = write_diff_file(doc_id, diff_text, summary)

    # 5. Tag the original Forest file (append needs-review tag to frontmatter)
    # Read YAML frontmatter, append tags, write back
    if original.startswith("---"):
        # Split frontmatter
        front_end = original.find("\n---\n") + 4
        frontmatter = original[:front_end]
        body = original[front_end:]

        # Parse tags line
        tags_line = "tags:"
        if tags_line in frontmatter:
            # Append new tags
            if tags_override:
                new_tags = tags_override
            else:
                new_tags = ["needs-review", "autonomous-edit"]
            # Find tags line and append
            lines = frontmatter.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('tags:'):
                    existing = line.split(':', 1)[1].strip()
                    # Parse list like [a, b, c]
                    import ast
                    try:
                        tag_list = ast.literal_eval(existing) if existing.startswith('[') else []
                    except:
                        tag_list = []
                    for t in new_tags:
                        if t not in tag_list:
                            tag_list.append(t)
                    lines[i] = f"tags: {json.dumps(tag_list)}"
                    break
            new_front = '\n'.join(lines)
            new_content = new_front + body
        else:
            # No tags — add one
            new_front = frontmatter.rstrip('\n') + f"\ntags: {json.dumps(['needs-review', 'autonomous-edit'])}\n"
            new_content = new_front + body
    else:
        # No frontmatter — prepend
        new_content = f"---\ntags: [\"needs-review\", \"autonomous-edit\"]\n---\n\n{original}"

    # Write back to Forest (this is the actual edit — requires Hermes patch authority)
    # Sylvan delegates to Hermes who has file write access
    with open(FOREST / rel_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # 6. Return result
    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "status": "proposed",
                "doc_id": doc_id,
                "rel_path": rel_path,
                "summary": summary,
                "diff_path": str(diff_path.relative_to(Path.home())),
                "tags_added": ["needs-review", "autonomous-edit"],
                "bytes_added": len(patched) - len(original)
            }, indent=2)
        }]
    }


# MCP dispatch
if __name__ == "__main__":
    # Read JSON-RPC request from stdin
    request = json.loads(sys.stdin.read())
    method = request["params"]["name"]
    args = request["params"]["arguments"]

    if method == "brain_suggest_patch":
        result = suggest_patch(**args)
    else:
        result = {"error": f"Unknown method: {method}"}

    # Print JSON-RPC response
    print(json.dumps({
        "jsonrpc": "2.0",
        "id": request["id"],
        "result": result
    }))
