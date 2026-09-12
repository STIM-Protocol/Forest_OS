# Tag Taxonomy: Canonical Vocabulary for Forest OS

**Version:** 1.0.0
**Status:** Authoritative
**Maintainer:** Forest OS Protocol Council

---

## 1. Philosophy

Tags are the semantic ligaments of the Forest. They enable:
- Cross-document discovery
- Query expansion
- Automated routing to correct Forest buckets
- Visual organization and mental model alignment

Tags are **lowercase**, **kebab-case**, and **singular** unless defining a compound concept.

---

## 2. Core Domain Tags (Top-Level Categories)

### 2.1 People & Entities
`person/<name>`: Individual human or agent profiles
- Example: `person/ryder`, `person/chelsea`, `person/bodhi`

`agent/<name>`: AI agent identities and capabilities
- Example: `agent/openclaw`, `agent/bodhi`, `agent/gemini`

`organization/<name>`: Companies, institutions, groups
- Example: `organization/osu`, `organization/google`, `organization/ua-local-669`

### 2.2 Knowledge Types
`concept`: Abstract ideas, frameworks, principles
- Example: `concept/compound-growth`, `concept/ai-readiness`

`decision`: Choice points requiring analysis or action
- Example: `decision/college-vs-trade`, `decision/embedding-model`

`research`: Structured inquiry or deep-dive outputs
- Example: `research/gemini-career-path`, `research/embedding-models`

`protocol`: Rules, standards, or operational procedures
- Example: `protocol/forest-os`, `protocol/stop-slop`

`tool`: Software, utilities, or instruments
- Example: `tool/openclaw`, `tool/gemini-cli`, `tool/nomic-embed`

`skill`: Capability or competency definition
- Example: `skill/email-automation`, `skill/wiki-sync`

### 2.3 Lifecycle & Status
`status/active`: Currently in use, relevant
`status/archived`: Preserved but no longer active
`status/experimental`: Prototyping, not production-ready
`status/deprecated`: Superseded, avoid using

### 2.4 Time & Priority
`priority/critical`: Must address immediately
`priority/high`: Important, schedule soon
`priority/medium`: Next-cycle work
`priority/low`: backlog item

`time/future`: Forward-looking, scheduled
`time/current`: Active this quarter
`time/past`: Historical, for reference only

---

## 3. Subject Matter Tags

These describe the *content domain*:

`subject/ai`: Artificial intelligence, machine learning, LLMs
`subject/engineering`: Mechanical, electrical, aerospace
`subject/construction`: Trades, building, infrastructure
`subject/education`: Learning, degrees, training programs
`subject/finance`: Money, salaries, benefits, valuations
`subject/health`: Medical, wellness, physical condition
`subject/wrestling`: Athletic sport, competition
`subject/robotics`: Mechatronics, automation
`subject/forest-os`: Our core ecosystem itself

---

## 4. Technical & System Tags

`tech/google-cloud`: Google Cloud Platform services
`tech/cloud-run`: Serverless container platform
`tech/vertex-ai`: ML/AI platform
`tech/gemini`: Google Gemini models
`tech/openclaw`: The agent runtime itself
`tech/mcp`: Model Context Protocol
`tech/embedding`: Vector representation models
`tech/agents-cli`: Google Agents CLI toolchain

`format/markdown`: `.md` files
`format/jsonld`: JSON-LD metadata sidecars
`format/pdf`: Portable Document Format
`format/image`: Visual media (png, jpg, svg)

`bucket/001_projects`: Active workstreams
`bucket/002_ideas`: Early concepts
`bucket/003_people`: Person-centric data
`bucket/004_resources`: Evergreen reference
`bucket/005_journal`: Daily logs
`bucket/006_business`: Org & finance

---

## 5. Agent Action Tags

`action/create`: Making new entities
`action/read`: Retrieval / observation
`action/update`: Modification of existing
`action/delete`: Removal or archival
`action/sync`: Data synchronization
`action/ingest`: Inbound processing
`action/query`: Search / retrieval action

`agent/sessions_spawn`: Sub-agent creation
`agent/eval`: Performance evaluation
`agent/deploy`: Production rollout

---

## 6. Tag Composition Rules

1. **Every Heartwood file must have at least one subject tag** (`subject/*`).
2. **Every People dossier must include `person/<slug>` and a status tag**.
3. **Every Research document must include `research` and relevant domain tags**.
4. **Bucket placement is authoritative**: the folder path supersedes tags for location.
5. **Tags in Cambium `relations` field define graph edges**; tags in frontmatter define classification.

---

## 7. Forbidden & discouraged tags

**Never use:**
- Generic tags like `misc`, `stuff`, `general`
- Duplicate semantics (`concept/idea` is redundant)
- Person names without `person/` prefix (use `person/george`, not just `george`)
- Project codes without context (use `project/ryder-education`, not `ryder-edu`)

---

## 8. Tag Maintenance

- **Adding a new tag:** First check if an existing tag fits. If not, propose in `FOREST/000_DASHBOARD/TAG_PROPOSALS.md`.
- **Deprecating a tag:** Mark document with `status/deprecated`, update references, do not reuse the tag string.
- **Renaming a tag:** Create migration script; update all documents in batch; document in CHANGELOG.

---

## 9. Quick Reference Table

| Tag Pattern | Meaning | Example |
|-------------|---------|---------|
| `person/*` | Individual person | `person/ryder` |
| `agent/*` | AI agent | `agent/bodhi` |
| `subject/*` | Content domain | `subject/ai` |
| `tech/*` | Technology stack | `tech/gemini` |
| `format/*` | File type | `format/jsonld` |
| `bucket/*` | Forest location | `bucket/003_people` |
| `status/*` | Lifecycle stage | `status/active` |
| `action/*` | Operation type | `action/create` |
| `research` | Is a research output | `research` |
| `protocol` | Is a protocol doc | `protocol` |
| `concept` | Is a conceptual framework | `concept` |

---

## 10. Usage Examples

**Ryder Education Dossier:**
```yaml
tags:
  - person/ryder
  - subject/education
  - subject/ai
  - decision/college-vs-trade
  - research
  - status/active
```

**Technical Design Document:**
```yaml
tags:
  - concept
  - subject/forest-os
  - tech/mcp
  - bucket/004_resources
  - status/draft
```

**Daily Journal Entry:**
```yaml
tags:
  - time/current
  - subject/personal
  - bucket/005_journal
  - status/active
```

---

*This taxonomy is living. Propose extensions via PR to `FOREST/000_DASHBOARD/TAG_TAXONOMY.md`.*
