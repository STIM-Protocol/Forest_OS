# Agent Model Strategy: Hybrid Local-Cloud Sovereignty

**Version:** 1.0.0
**Status:** Operational
**Purpose:** Define agent-to-model allocation for Forest OS (2026-04-26 context)

## Strategy Overview
To balance privacy, speed, and deep reasoning, Forest OS employs a **Hybrid Model Pattern**. Routine, high-frequency, or private tasks are handled by local models (). Complex, multimodal, or deep research tasks utilize the Gemini Ultra-tier cloud models.

## Model Registry

### 1. Local (Ollama / Local Inference)
- **Model:** `gemma4:e2b` (Primary Workhorse)
- **Use Cases:** Memory distillation, Linting, Brain metadata generation, Offline chat.
- **Why:** Zero latency, 100% privacy, zero token cost.
- **Future-Proofing:** Architecture agnostic; ready for `gemma4:26b` local upgrade.

### 2. Cloud (Gemini API / Ultra Subscription)
- **Model:** `gemini-3.1-pro-preview` (Deep Reasoning/Think)
- **Use Cases:** Web-augmented Deep Research, Cross-document insight synthesis, Multimodal PDF/OCR/Image ingestion.
- **Why:** Unmatched chain-of-thought depth, Deep Research capabilities, multimodal handling.

## Agent Allocation Logic
- **Memory Agent:** `gemma4:e2b` (Local). Distillation is routine and private.
- **Ingest Agent:** `gemini-3.1-pro-preview` (Cloud). Requires deep multimodal understanding.
- **Lint Agent:** Rule-based (No LLM).
- **Brain Agent:** Nomic Embed (Local) + `gemma4:e2b` (Metadata).
- **Synthesis Agent:** `gemini-3.1-pro-preview` (Cloud). Requires high-level reasoning and synthesis.

## Fault Tolerance Strategy
1. **Cloud-First for Research:** If a task requires external data, prioritize Cloud Deep Research.
2. **Local-Fallback:** If Cloud is unavailable, agents revert to local model for basic summarization.
3. **Kilo-Fallback:** If everything else fails, the `kilo` model ensures system availability for critical alerts.

*This strategy governs all autonomous agent tasking moving forward.*
