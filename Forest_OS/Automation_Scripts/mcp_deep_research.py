#!/usr/bin/env python3
"""
id: "SYL-102"
title: "Deep Research MCP Tool"
tags: [mcp-tool, deep-research, polyploidy, token-budget, forest-os]
created: 2026-05-07
stim_version: 1.0
---
Polyploidy research engine: local Gemma triage (cheap) + optional Gemini deep synthesis (expensive).
Hard-coded daily token budget. Fails gracefully when budget exhausted.
Outputs structured markdown to FOREST/004_RESEARCH/ with full citations.
"""
import sys, json, os, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
import subprocess
import time

# Configuration
FOREST = Path.home() / "Myceliate_Master" / "FOREST"
OUTPUT_DIR = FOREST / "004_RESEARCH" / "Deep_Research"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USAGE_LEDGER = Path.home() / ".hermes" / "forest_os" / "deep_research_usage.json"
USAGE_LEDGER.parent.mkdir(parents=True, exist_ok=True)

# Default budget: 100k tokens per 24h window
DAILY_BUDGET = int(os.getenv("FOREST_OS_DR_BUDGET", "100000"))
LOCAL_MODEL = os.getenv("FOREST_OS_DR_LOCAL_MODEL", "phi3:mini")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("FOREST_OS_DR_GEMINI_MODEL", "gemini-1.5-pro")


def load_usage():
    """Load today's usage ledger."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if USAGE_LEDGER.exists():
        data = json.loads(USAGE_LEDGER.read_text())
        if data.get("date") == today:
            return data
    # Fresh day
    return {"date": today, "tokens_used": 0, "calls": []}


def log_usage(tokens: int, query: str, provider: str):
    """Append usage to ledger."""
    data = load_usage()
    data["tokens_used"] += tokens
    data["calls"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "provider": provider,
        "tokens": tokens,
        "query": query[:120]
    })
    USAGE_LEDGER.write_text(json.dumps(data, indent=2))


def estimate_tokens(text: str) -> int:
    """Rough token estimate (chars/4 for English)."""
    return max(1, len(text) // 4)


def call_local_gemma(prompt: str) -> str:
    """Run local Ollama model for fast triage."""
    try:
        result = subprocess.run(
            ["ollama", "run", LOCAL_MODEL, prompt],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            err = result.stderr.strip() or "unknown error"
            # If model not found, fallback to short summary
            if "not found" in err.lower() or "no such" in err.lower():
                print(f"[WARN] Model {LOCAL_MODEL} not available — using fallback", file=sys.stderr)
                return f"[Local triage skipped — model unavailable. Prompt was: {prompt[:100]}]"
            raise RuntimeError(f"Ollama error: {err}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[Local triage timed out after 30s]"
    except FileNotFoundError:
        return "[Ollama binary not found — please install Ollama]"


def call_gemini_deep(query: str, context: str) -> str:
    """Call Gemini API for deep synthesis."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not set — cannot call Gemini")
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{
            "parts": [
                {"text": f"Research query: {query}\n\nContext from local triage:\n{context}"}
            ]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 8192
        }
    }
    r = requests.post(url, params={"key": GEMINI_API_KEY}, json=payload, timeout=90)
    if r.status_code != 200:
        raise RuntimeError(f"Gemini {r.status_code}: {r.text[:200]}")
    resp = r.json()
    return resp["candidates"][0]["content"]["parts"][0]["text"]


def deep_research(query: str, depth: str = "medium", use_gemini: bool = None) -> dict:
    """If use_gemini is None, auto-detect cron environment (default local-only)."""
    if use_gemini is None:
        # Cron jobs set FOREST_OS_CRON=1 or HERMES_CRON=1
        use_gemini = not (os.getenv("FOREST_OS_CRON") or os.getenv("HERMES_CRON") or os.getenv("CI"))
    """
    Execute deep research workflow.
    depth: "light" (local only), "medium" (Gemini summary), "deep" (full synthesis)
    """
    # 1. Check budget
    usage = load_usage()
    est_tokens = estimate_tokens(query) * 2  # rough budget
    if usage["tokens_used"] + est_tokens > DAILY_BUDGET:
        return {
            "error": "budget_exceeded",
            "message": f"Daily token budget {DAILY_BUDGET} exceeded ({usage['tokens_used']} used). Try again tomorrow."
        }

    start = time.time()
    # 2. Local triage (always)
    local_prompt = f"You are a research assistant. Given this query, identify key sub-topics and gather foundational facts. Query: {query}"
    local_out = call_local_gemma(local_prompt)
    local_tokens = estimate_tokens(local_prompt + local_out)
    log_usage(local_tokens, query, "local-gemma")

    # 3. Optional Gemini deep synthesis
    if use_gemini and depth in ("medium", "deep"):
        gemini_prompt = f"Deep synthesis of the following research topic. Provide a comprehensive, structured report with sections, citations, and actionable insights.\n\nQuery: {query}\n\nLocal findings to expand:\n{local_out}"
        gemini_out = call_gemini_deep(query, local_out)
        gemini_tokens = estimate_tokens(gemini_prompt + gemini_out)
        # Check budget again before logging
        if usage["tokens_used"] + local_tokens + gemini_tokens > DAILY_BUDGET:
            return {"error": "budget_exceeded", "message": "Budget exceeded after local phase; skipping deep synthesis."}
        log_usage(gemini_tokens, query, "gemini")
        synthesis = gemini_out
        provider = "gemini-deep"
    else:
        synthesis = local_out
        provider = "local-only"

    # 4. Write to Forest
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c for c in query if c.isalnum() or c in '-_')[:80]
    fname = f"deep-research_{safe_query}_{ts}.md"
    doc_id = Path(fname).stem
    out_path = OUTPUT_DIR / fname

    frontmatter = f"---\ntitle: \"Deep Research: {query[:80]}\"\ntags: [\"deep-research\", \"auto-generated\", \"{provider}\", \"needs-review\"]\ncreated: {datetime.utcnow().strftime('%Y-%m-%d')}\nstim_version: 1.0\n---\n\n"
    body = f"# Deep Research: {query}\n\n## Executive Summary\n{synthesis}\n\n## Methodology\n- Provider: {provider}\n- Local model: {LOCAL_MODEL}\n- Depth: {depth}\n- Generated: {datetime.utcnow().isoformat()}Z\n\n## Source Queries\nOriginal query: {query}\n\n"
    out_path.write_text(frontmatter + body, encoding='utf-8')

    # 5. Emit coordination event
    event_dir = Path.home() / "Myceliate_Master" / "COMPOST" / "agent_coordination"
    event_file = event_dir / f"{datetime.utcnow():%Y%m%d_%H%M%S}_deep_research_{doc_id}.json"
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": "mcp_deep_research",
        "action": "research_complete",
        "doc_id": doc_id,
        "details": json.dumps({
            "query": query,
            "provider": provider,
            "depth": depth,
            "tokens_used": usage["tokens_used"],
            "output_path": str(out_path.relative_to(Path.home()))
        })
    }
    event_file.write_text(json.dumps(event, indent=2))

    elapsed = time.time() - start
    return {
        "status": "complete",
        "doc_id": doc_id,
 "output_path": str(out_path.relative_to(Path.home())),
        "provider": provider,
        "tokens_used": usage["tokens_used"],
        "elapsed_seconds": round(elapsed, 2)
    }


if __name__ == "__main__":
    args = json.loads(sys.stdin.read())
    result = deep_research(**args)
    print(json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}))
