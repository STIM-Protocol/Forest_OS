#!/usr/bin/env python3
"""
Forest Lint: Validate Heartwood/Cambium compliance across the Forest.
"""

import os
import json
import sys
from pathlib import Path

FOREST_ROOT = Path("/home/george/Myceliate_Master/FOREST")

def validate_pair(md_path):
    """Check that a Heartwood file has a matching Cambium with required fields."""
    cambium = md_path.with_suffix(".jsonld")
    if not cambium.exists():
        return f"Missing Cambium for {md_path.name}"

    try:
        with open(cambium) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return f"Invalid JSON-LD in {cambium.name}: {e}"

    required = ["@context", "id", "type", "tags", "relations"]
    missing = [k for k in required if k not in data]
    if missing:
        return f"Missing fields in {cambium.name}: {missing}"

    return None  # OK

def main():
    errors = []
    for md in FOREST_ROOT.rglob("*.md"):
        # Skip index files and non-documentation
        if md.name.startswith("_"):
            continue
        err = validate_pair(md)
        if err:
            errors.append(err)

    if errors:
        print("LINT FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("All documents compliant.")
        sys.exit(0)

if __name__ == "__main__":
    main()
