#!/usr/bin/env python3
"""
Forest Hardener: Apply minimal structural compliance to existing Forest files.
- Adds missing .jsonld sidecars with basic metadata
- Replaces em dashes with colons (only that stop-slop rule)
- Preserves all other content exactly
- Skips files that already have sidecars or are in .trash
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

FOREST = Path("/home/george/Myceliate_Master/FOREST")

def generate_uuidv7():
    # Simplified: use timestamp-based short ID for now
    import time
    ts = int(time.time() * 1000)
    return f"{ts:x}"[:8].upper() + os.urandom(3).hex().upper()  # ~11 chars

def guess_type_from_path(path):
    """Infer document type from folder location."""
    parts = path.parts
    if "005_JOURNAL" in parts:
        return "journal"
    elif "004_RESOURCES" in parts:
        return "resource"
    elif "003_PEOPLE" in parts:
        return "dossier"
    elif "002_IDEAS" in parts:
        return "idea"
    elif "001_PROJECTS" in parts:
        return "project"
    elif "006_BUSINESS" in parts:
        return "business"
    elif "000_DASHBOARD" in parts:
        return "dashboard"
    return "document"

def guess_tags_from_path(path):
    """Extract tag hints from folder structure."""
    tags = []
    parts = path.parts
    # Bucket tag
    if "001_PROJECTS" in parts:
        tags.append("bucket/001_projects")
    elif "002_IDEAS" in parts:
        tags.append("bucket/002_ideas")
    elif "003_PEOPLE" in parts:
        tags.append("bucket/003_people")
        # person tag from subfolder
        person_dir = [p for p in parts if p in ["ryder", "chelsea", "george_steward", "george"]]
        if person_dir:
            tags.append(f"person/{person_dir[0]}")
    elif "004_RESOURCES" in parts:
        tags.append("bucket/004_resources")
    elif "005_JOURNAL" in parts:
        tags.append("bucket/005_journal")
    elif "006_BUSINESS" in parts:
        tags.append("bucket/006_business")
    # Subject hints
    if "Mozi" in str(path):
        tags.append("subject/mozi-insights")
    if "Food" in str(path):
        tags.append("subject/food")
    if "AI" in str(path).upper():
        tags.append("subject/ai")
    return tags

def create_cambium(md_path):
    """Generate a minimal, compliant .jsonld sidecar."""
    stem = md_path.stem
    # Use filename stem as ID (do not rename files); pad if needed
    doc_id = stem[:16] if len(stem) > 0 else generate_uuidv7()

    doc_type = guess_type_from_path(md_path)
    tags = guess_tags_from_path(md_path)

    cambium = {
        "@context": "https://for.est/contexts/forest-centennial-os/v1",
        "id": doc_id,
        "type": doc_type,
        "name": stem.replace('-', ' ').replace('_', ' ').title(),
        "tags": tags,
        "relations": {
            "path": str(md_path.relative_to(FOREST))
        },
        "created": datetime.fromtimestamp(md_path.stat().st_mtime).isoformat()
    }

    cambium_path = md_path.with_suffix('.jsonld')
    with open(cambium_path, 'w') as f:
        json.dump(cambium, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Created {cambium_path.name} (id={doc_id}, type={doc_type})")

def process_md_file(md_path):
    """Apply hardening to a single markdown file."""
    original = md_path.read_text()
    modified = original

    # Only change: replace em dashes with colons
    if "\u2014" in original:
        modified = modified.replace(" \u2014 ", ": ")
        modified = modified.replace("\u2014", ": ")
        print(f"  ℹ Fixed em dashes in {md_path.name}")

    if modified != original:
        md_path.write_text(modified)

    # Ensure sidecar exists
    cambium = md_path.with_suffix('.jsonld')
    if not cambium.exists():
        create_cambium(md_path)
    else:
        print(f"  ✓ Sidecar already exists for {md_path.name}")

def main():
    print("Forest Hardener: Structural compliance pass")
    print("=" * 50)

    # Find all .md files in Forest, excluding .trash and hidden dirs
    md_files = []
    for root, dirs, files in os.walk(FOREST):
        # Skip .trash, .git, node_modules
        dirs[:] = [d for d in dirs if d not in ['.trash', '.git', 'node_modules', '.antigravity_context']]
        for f in files:
            if f.endswith('.md'):
                md_files.append(Path(root) / f)

    print(f"Found {len(md_files)} markdown files to inspect")

    processed = 0
    for md in sorted(md_files):
        try:
            process_md_file(md)
            processed += 1
        except Exception as e:
            print(f"  ✗ Error on {md.name}: {e}")

    print(f"\nHardening complete. Processed {processed} files.")

if __name__ == "__main__":
    main()
