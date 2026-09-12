#!/usr/bin/env python3
"""
id: "SYL-101a"
title: "Cambium Link Appender"
tags: [mcp-tool, cambium, autonomous-link, forest-os]
created: 2026-05-07
stim_version: 1.0
---
Append a semantic triple to a .jsonld file's relations.autonomous_links array.
Autonomous write to Cambium layer only. Tags file with needs-review, autonomous-link.
"""
import sys, json
from pathlib import Path
from datetime import datetime, timezone

FOREST = Path.home() / "Myceliate_Master" / "FOREST"

def append_link(rel_path: str, subject: str, predicate: str, obj: str, summary: str = ""):
    full = FOREST / rel_path
    if not full.exists():
        raise FileNotFoundError(f"No such Cambium file: {rel_path}")

    text = full.read_text(encoding='utf-8')
    # Split YAML frontmatter (---) and JSON-LD body
    if text.startswith('---'):
        fm_end = text.find('\n---\n') + 4
        frontmatter = text[:fm_end]
        body = text[fm_end:]
    else:
        frontmatter = ""
        body = text

    # Parse body JSON
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON-LD in {rel_path}: {e}")

    # Ensure relations structure exists
    if 'relations' not in data:
        data['relations'] = {}
    if 'autonomous_links' not in data['relations']:
        data['relations']['autonomous_links'] = []

    # Build link with timestamp
    link = {
        "subject": subject,
        "predicate": predicate,
        "object": obj,
        "added_by": "Sylvan_The_Beaver",
        "added_at": datetime.utcnow().isoformat() + "Z",
        "summary": summary
    }
    data['relations']['autonomous_links'].append(link)

    # Re-serialize with minimal spacing
    new_body = json.dumps(data, indent=2, ensure_ascii=False)

    # Tag frontmatter: append needs-review, autonomous-link
    if frontmatter:
        lines = frontmatter.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('tags:'):
                try:
                    tags = json.loads(line.split(':',1)[1].strip())
                except:
                    tags = []
                for t in ['needs-review', 'autonomous-link']:
                    if t not in tags:
                        tags.append(t)
                lines[i] = f"tags: {json.dumps(tags)}"
                break
        new_front = '\n'.join(lines)
    else:
        new_front = "---\ntags: [\"needs-review\", \"autonomous-link\"]\n---\n"

    full.write_text(new_front + new_body, encoding='utf-8')

    # Return metadata
    doc_id = Path(rel_path).stem
    return {
        "status": "appended",
        "doc_id": doc_id,
        "rel_path": rel_path,
        "link_count": len(data['relations']['autonomous_links']),
        "tags": ["needs-review", "autonomous-link"]
    }

if __name__ == "__main__":
    args = json.loads(sys.stdin.read())
    result = append_link(**args)
    print(json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}))
