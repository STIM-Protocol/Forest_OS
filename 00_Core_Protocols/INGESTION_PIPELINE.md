# Ingestion Pipeline: From Raw Material to Forest Heartwood

**Version:** 1.0.0
**Status:** Operational
**Scope:** How external data becomes authoritative Forest knowledge

---

## 1. Pipeline Stages

```
[Source] → [Capture] → [Convert] → [Categorize] → [Synthesize] → [Heartwood + Cambium] → [Forest/]
```

---

### Stage 1: Capture

**Sources:**
- PDFs (research papers, manuals)
- Web pages (articles, blog posts)
- Voice memos (meetings, insights)
- Screenshots (diagrams, error messages)
- Physical notes (scanned)

**Method:**
- Manual download / screenshot → `GREENHOUSE/Active/Neocambrian_Academy/04_INGESTION/`
- Automated ingestion bots (future) watch email, RSS, cloud storage

**Naming:** `YYYY-MM-DD_source_description.ext` (e.g., `2026-04-26_google-embedding-announcement.pdf`)

---

### Stage 2: Convert

Normalize to searchable text:

| Source | Tool | Output |
|--------|------|--------|
| PDF (text-based) | `pdftotext` or `pdf2md` | `.md` text |
| PDF (scanned/OCR) | Tesseract + layout analysis | `.md` with metadata |
| Image (diagram) | OCR + alt-text generation | `.md` description + keep original in LIBRARY |
| Audio / Voice | Whisper (local) or Deepgram | Transcribed `.md` |
| Web page | `web_fetch` + readablity parser | Clean `.md` |
| Video | Frame sampling + OCR + audio transcription | Multi-part `.md` |

**Storage:**
- Binary originals → `LIBRARY/<category>/`
- Extracted text → staging area for synthesis

---

### Stage 3: Categorize

Determine target Forest bucket:

| Content Type | Destination Bucket | Example |
|--------------|-------------------|---------|
| Active project with tasks | `001_PROJECTS` | `mycelial-brain-mcp-v2/` |
| Idea, seed, half-baked concept | `002_IDEAS` | `agents-cli-experiment/` |
| Person profile, dossier | `003_PEOPLE` | `ryder/education/` |
| Reference material, evergreen | `004_RESOURCES` | `embedding-models-comparison/` |
| Daily log, insight, journal | `005_JOURNAL` | `2026-04-26-insights/` |
| Business admin, finance | `006_BUSINESS` | `invoices/q2-2026/` |

**Decision triggers:**
- Is this about a *specific person*? → `003_PEOPLE/<person>/`
- Is this *time-serialized* (daily)? → `005_JOURNAL/<YYYY-MM-DD>/`
- Is this *actionable with tasks*? → `001_PROJECTS/<project>/`
- Is this *reference only* (no action)? → `004_RESOURCES/<topic>/`

---

### Stage 4: Synthesize

Transform raw extracted text into **Heartwood**:

1. **Summarize** — condense to essential facts, remove filler.
2. **Structure** — add H1/H2 headings, tables, bullet lists.
3. **Cite** — add source attribution (URL, title, date accessed).
4. **Tag** — apply `TAG_TAXONOMY.md` tags.
5. **Metadata extraction** — identify author, date, domain.

**Tools:** Use a synthesis agent (OpenClaw sub-session) or manual writing. The goal: a concise, reference-ready Markdown document.

---

### Stage 5: Heartwood + Cambium

Create the paired files:

**Step A:** Write `HEARTWOOD` (`.md`)
- Place in target bucket folder
- Use clear title and structured sections
- Include relevant data tables, comparisons, diagrams (as code blocks or links to images)

**Step B:** Write `CAMBURY` (`.jsonld`)
- Generate ID: `01JWWZ1M`-style slug
- Fill required fields (`@context`, `id`, `type`, `name`, `tags`, `relations`)
- Set `parent` relation to bucket root doc if exists, else bucket folder path
- Set `created` timestamp

**Step C:** Validate
- Run `forest-lint` (if implemented)
- Check tag spelling against `TAG_TAXONOMY.md`
- Confirm file location matches bucket rules

---

### Stage 6: Forest Integration

- File is now live in Forest
- Trigger `brain_create` if content is reference-worthy
- Add index entry if bucket maintains `_index.md`
- Schedule periodic `prune_forest_to_library.sh` sync for LIBRARY assets

---

## 2. Special Cases

### 2.1 Person Dossiers (003_PEOPLE)

All person-centric materials go under `003_PEOPLE/<person_slug>/`. Create subfolders:

```
003_PEOPLE/ryder/
├── 01_Profile/           (bio, contact, preferences)
├── 02_Education_and_Development/   (school, training, certifications)
├── 03_Career/            (jobs, projects, performance reviews)
├── 04_Health/            (medical, fitness, records)
├── 05_Relations/         (family, network map)
└── 06_Goals_and_Milestones/   (OKRs, KPIs, tracking)
```

Each subfolder can contain multiple Heartwood docs.

### 2.2 Research Synthesis

When you produce a **research dossier** (like the Ryder analysis):
1. Start in `004_RESOURCES/Research/` as `temp_<topic>_bulk.md`
2. Synthesize into concise Heartwood
3. Move to final bucket: `003_PEOPLE/<person>/` if person-specific, else `004_RESOURCES/`
4. Create `.jsonld` with `type: "research"` or `"dossier"`
5. Ingest to Brain as new doc

### 2.3 Daily Journal

`005_JOURNAL/Daily/2026-04-26.md` is the daily log.
At end of day:
- Review entries
- Extract insights → create `005_JOURNAL/Insights/` docs
- Flag action items → create `001_PROJECTS/` tasks
- Move completed items → `006_BUSINESS/` or appropriate bucket

---

## 3. Automation Hooks

**Proposed scripts:**
- `forest-ingest-pdf --source <file>` — auto-OCR, categorize, suggest tags
- `forest-from-url --url <link>` — fetch page, clean, draft Heartwood
- `forest-synthesize --input <temp.md> --topic <subject>` — AI-assisted summarization

**Triggers:**
- File drop in `GREENHOUSE/Active/Neocambrian_Academy/04_INGESTION/` → auto-start pipeline
- New `brain_create` success → auto-generate Cambium sidecar if missing

---

## 4. Quality Gates

Before a document is considered **live**:

1. **Heartwood passes visual scan** — readable, well-structured
2. **Cambium well-formed JSON-LD** — valid syntax, required fields present
3. **Tags are canonical** — every tag exists in taxonomy
4. **Relations resolve** — parent/child IDs exist or are being created concurrently
5. **No sensitive data** — PII redacted if needed (use `redact` workflow)
6. **Backed up** — file exists in at least two locations (local + Drive sync)

---

*Pipeline is iterative. Refine as new media types arrive.*
