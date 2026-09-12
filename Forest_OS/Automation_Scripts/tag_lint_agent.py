#!/usr/bin/env python3
"""
Tag Lint Agent — Fixes Tag Drift
Validates tags in FOREST documents against canonical taxonomy.
Auto-fixes common drift: synonyms, deprecated tags, missing prefixes.
"""
import os, re, json, sys
from pathlib import Path

FOREST = Path("/home/george/Myceliate_Master/FOREST")
TAXONOMY = {
    "forest": ["forest-asset"],
    "status": ["status/processed"],
    "project": ["project_ai/educational"],
    "ecological": ["ecological/arboracle"],
    "hashtags": ["#chelsea", "#health", "#mcas", "#pipr_people", "#spore", "#whatsapp"],
    "domain": [
        "environmental management", "human resources", "military lands",
        "forest management", "resilience", "theory", "tree_scale holobiont",
        "environmental", "vetclaimsai", "veteran advocate",
    ],
    "tools": ["agcli", "anti_gravity", "automation", "bridge", "ide", "remote_control", "vnc"],
    "personal": ["dad_brief", "family", "weekly_update"],
}
VALID_TAGS = set(tag for tags in TAXONOMY.values() for tag in tags)

FRONTMATTER_TAG_RE = re.compile(r'^tags:\s*\[(.*?)\]$', re.IGNORECASE)
SIMPLE_TAG_RE = re.compile(r'#[a-z0-9_-]+')

def fix_tags(content: str, path: Path) -> tuple[str, bool]:
    """Normalize tags to canonical form."""
    changed = False
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        m = FRONTMATTER_TAG_RE.match(line)
        if m:
            raw_tags = [t.strip().strip('"').strip("'") for t in m.group(1).split(',')]
            normalized = []
            for tag in raw_tags:
                tag_lower = tag.lower()  # preserve hyphens (canonical uses hyphens)
                # Map known drift variants
                if tag_lower in ["bodhi-analysis", "bodhi"] and "agent" not in tag_lower:
                    tag_lower = "agent"
                # Demystify: uncategorized_X where X is canonical → strip prefix
                if tag_lower.startswith('uncategorized_'):
                    real_tag = tag_lower[14:].replace("_", "-")  # strip prefix, restore hyphens 'uncategorized_'
                    if real_tag in VALID_TAGS:
                        print(f"  ✓ {path.name}: demystified — '{tag}' → '{real_tag}'")
                        tag_lower = real_tag
                        changed = True
                    else:
                        normalized.append(tag_lower)
                        continue
                # Validate against taxonomy
                if tag_lower not in VALID_TAGS:
                    print(f"  ! {path.name}: tag drift — '{tag}' → 'uncategorized_{tag_lower}'")
                    tag_lower = f"uncategorized_{tag_lower}"
                    changed = True
                normalized.append(tag_lower)
            new_line = f"tags: [{', '.join(sorted(set(normalized)))}]"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines), changed

def main():
    fixed = 0
    scanned = 0
    for md in FOREST.rglob("*.md"):
        if "Compost/" in str(md) or "LEGACY_QUARANTINE" in str(md):
            continue
        scanned += 1
        try:
            content = md.read_text()
            new_content, changed = fix_tags(content, md)
            if changed:
                md.write_text(new_content)
                print(f"🔧 {md.relative_to(FOREST)}")
                fixed += 1
        except Exception as e:
            print(f"✗ {md}: {e}", file=sys.stderr)
    print(f"\n✅ Tag drift scan complete: {scanned} scanned, {fixed} fixed.")
    print(f"   Canonical taxonomy: {len(TAXONOMY)} categories, {len(VALID_TAGS)} tags")

if __name__ == "__main__":
    main()
