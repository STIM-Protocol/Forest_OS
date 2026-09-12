# Forest OS Protocol Index

**Version:** 1.0.0
**Last Updated:** 2026-04-26
**Scope:** Canonical reference for all Forest OS protocol documents

---

## Protocol Documents Hierarchy

### Tier 1: Foundational Principles
- **[ROOT_MANIFEST.md](./ROOT_MANIFEST.md)**: Core philosophy, architecture, and Forest taxonomy. *This is the constitution.*

### Tier 2: Operational State
- **[WORLD_MODEL.md](./WORLD_MODEL.md)**: Current system snapshot: vaults, agents, brain state, active projects.

### Tier 3: Vocabulary & Standards
- **[TAG_TAXONOMY.md](./TAG_TAXONOMY.md)**: Canonical tag set, usage rules, forbidden patterns.
- **[HEARTWOOD_CAMBIUM_PATTERN.md](./HEARTWOOD_CAMBIUM_PATTERN.md)**: Detailed file format specification for `.md` + `.jsonld` pairs.

### Tier 4: Implementation Guides
- **[INGESTION_PIPELINE.md](./INGESTION_PIPELINE.md)**: How new knowledge enters the Forest (PDF → OCR → Forest).
- **[SYNC_PROTOCOLS.md](./SYNC_PROTOCOLS.md)**: Forest ↔ Library ↔ Compost sync procedures.
- **[BRAIN_INTEGRATION.md](./BRAIN_INTEGRATION.md)**: MCP service operations, doc lifecycle, embedding model specs.

### Tier 5: Governance
- **[CHANGELOG.md](./CHANGELOG.md)**: Version history of protocol changes.
- **[PROPOSALS.md](./PROPOSALS.md)**: Open RFCs and community feedback.

---

## Document Cross-Reference

| Document | Primary Audience | Frequency of Update |
|----------|------------------|---------------------|
| ROOT_MANIFEST | All users | Rare (major philosophy shifts) |
| WORLD_MODEL | Operators / maintainers | Weekly or on major state change |
| TAG_TAXONOMY | Authors / AI agents | As new domains emerge |
| HEARTWOOD_CAMBIUM | Content creators | Every new file type |
| INGESTION_PIPELINE | Data engineers | When new source formats added |
| SYNC_PROTOCOLS | DevOps | After infrastructure changes |
| BRAIN_INTEGRATION | Backend developers | Model or MCP version bumps |
| CHANGELOG | Everyone | Every commit |
| PROPOSALS | Stakeholders | Active RFC period |

---

## Quick Navigation by Task

**"I need to create a new Forest document."**
→ Read `HEARTWOOD_CAMBIUM_PATTERN.md` → follow `TAG_TAXONOMY.md` → place in correct bucket per `ROOT_MANIFEST.md`.

**"I want to understand current system state."**
→ Read `WORLD_MODEL.md`.

**"Which tag should I use for X?"**
→ Search `TAG_TAXONOMY.md`.

**"How do I add a new research PDF?"**
→ Follow `INGESTION_PIPELINE.md`.

**"What changed in the last week?"**
→ Read `CHANGELOG.md`.

**"I want to propose a new bucket."**
→ Draft `PROPOSALS.md` entry.

---

## Versioning

Protocol documents follow semantic versioning independently:
- **Major:** Structural change (e.g., adding new bucket tier)
- **Minor:** New sub-protocol or expanded tag set
- **Patch:** Clarification, typo fix, example update

The `ROOT_MANIFEST` is the single source of truth for version compatibility; all other docs must reference its version in their frontmatter.

---

*This index itself is a protocol document. Maintain accuracy.*
