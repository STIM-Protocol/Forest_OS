<!-- HISTORICAL COPY: see 01_Docs/DOCUMENT_AUTHORITY.md for the authoritative source. -->

# Heartwood / Cambium: File Pattern Specification

**Version:** 1.0.0
**Applies to:** All primary knowledge nodes in the Forest

---

## Concept

Each *authoritative* knowledge entity in Forest OS exists as a **pair**:

```
01JWWZ1M-example-person-dossier.md      ← Heartwood (human-readable content)
01JWWZ1M-example-person-dossier.jsonld  ← Cambium (machine-readable metadata)
```

- **Heartwood** is the substance. It is the prose, tables, diagrams, and narrative.
- **Cambium** is the living layer. It holds the ID, tags, relations, and context that connect this node to the ecosystem.

The Cambium enables indexing, discovery, and automated operations without polluting the Heartwood.

---

## Heartwood Format (`.md`)

- **Primary format:** GitHub-flavored Markdown
- **Frontmatter:** Optional but recommended YAML block at the top for quick metadata
- **Structure:** Free-form, but should include:
  - Title (H1)
  - Metadata block (author, date, subject)
  - Table of contents (optional, auto-gen OK)
  - Main content sections
  - Appendices / references

**Rules:**
- No em dashes: use colons, semicolons, or restructure.
- No passive voice.
- No filler adverbs.
- Direct, dense prose.
- Cite sources inline with footnotes or brackets.

**Example frontmatter:**
```markdown
---
Author: Example Person
Date: 2026-04-26
Subject: College Decision Analysis
Tags: person/example subject/education research
---

# The College Imperative: My Strategic Analysis
...
```

---

## Cambium Format (`.jsonld`)

- **Schema:** JSON-LD with `@context` pointing to Forest OS vocabulary
- **Required fields:**
  - `@context`: `"https://for.est/contexts/forest-centennial-os/v1"`
  - `id`: Heartwood ID (exact filename stem, e.g., `"01JWWZ1M"`)
  - `type`: Node type (`"dossier"`, `"research"`, `"protocol"`, `"concept"`, etc.)
  - `name`: Human-readable title (string)
  - `tags`: Array of tag strings (must be valid per `TAG_TAXONOMY.md`)
  - `relations`: Object mapping relation types to node IDs or paths

**Optional fields:**
- `created`: ISO 8601 timestamp
- `updated`: ISO 8601 timestamp (last content edit)
- `author`: String or array
- `version`: Semantic version if tracked
- `dependsOn`: Array of prerequisite node IDs
- `supersedes`: ID of previous version

**Relations format:**
```json
{
  "relations": {
    "parent": "doc-115",
    "child_of": "01JWWZ1K",
    "mentions": ["person/example-2", "organization/osu"],
    "see_also": ["01JWWZ1N"]
  }
}
```

**Example Cambium:**
```json
{
  "@context": "https://for.est/contexts/forest-centennial-os/v1",
  "id": "01JWWZ1M",
  "type": "dossier",
  "name": "Example Person Decision Master Dossier",
  "tags": ["person/example", "subject/education", "research"],
  "relations": {"parent": "doc-115"},
  "created": "2026-04-26T13:00:00-05:00"
}
```

---

## Creation Checklist

When adding a new primary node:

1. [ ] Choose correct Forest bucket (001–006)
2. [ ] Generate UUIDv7: `uuidgen -r` or equivalent (11 chars: 01JWWZ1M)
3. [ ] Create descriptive slug: `-example-person-dossier.md`
4. [ ] Write Heartwood (`.md`) first: focus on content
5. [ ] Draft Cambium (`.jsonld`) second: extract ID, type, tags from content
6. [ ] Validate tags against `TAG_TAXONOMY.md`
7. [ ] Set `relations` linking to parent bucket root or related nodes
8. [ ] Save both files side-by-side in the bucket
9. [ ] Run `forest-lint` (if available) or manual peer review
10. [ ] Add entry to bucket index if one exists

---

## Updating Existing Nodes

- **Heartwood edits:** Update the `.md` file, increment `updated` in Cambium, keep same ID.
- **Metadata changes:** Edit Cambium directly; do not touch Heartwood unless content changes.
- **Versioning:** If a document undergoes major restructuring, consider `supersedes` relation and create new ID; otherwise edit in place.

---

## Tools & Automation

- `forest-new <type> "<title>"`: scaffolding script (proposed)
- `forest-lint <path>`: validates Heartwood/Cambium pair compliance
- `forest-sync`: pushes new/updated documents to Mycelial Brain via MCP

---

*Pattern established 2026-04-26. Revise as ecosystem evolves.*
