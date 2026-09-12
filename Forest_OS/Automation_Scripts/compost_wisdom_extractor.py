#!/usr/bin/env python3
"""
Compost Wisdom Extractor — Semantic Compost Flaw Fix (v0.1)
Distills raw material in COMPOST/Inbox into structured journal entries.
Output: FOREST/005_JOURNAL/Compost/YYYY-MM-DD-distillate.md
"""
import os, sys, json, subprocess, hashlib, datetime, gzip
from pathlib import Path

INBOX = Path("/home/george/Myceliate_Master/COMPOST/Inbox")
JOURNAL = Path("/home/george/Myceliate_Master/FOREST/005_JOURNAL/Compost")
ARCHIVE_DIR = Path("/home/george/Myceliate_Master/FOREST/006_UNDERSTORY/Compost_Originals")
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "llama3"
MODEL = os.getenv("FOREST_OS_COMPOST_MODEL", "llama3")

def extract_insight(content: str) -> str:
    """Prompt llama3 to extract 3-5 key insights + pattern recognition."""
    prompt = f"""You are a wisdom distiller. Extract enduring patterns, principles, or anomalies from this material. Return JSON:

{{
  "insights": [<string: concise insight, max 140 chars>],
  "patterns": [<string: recurring theme or structure>],
  "confidence": <float: 0-1, how transferable to future contexts>,
  "compost_ttl_days": <int: how long this wisdom remains relevant>
}}

Material:
{content[:4000]}  # truncate for context window

Respond ONLY with valid JSON."""
    try:
        r = subprocess.run(
            ["curl", "-s", OLLAMA, "-d", json.dumps({"model": MODEL, "prompt": prompt, "stream": False})],
            capture_output=True, text=True, timeout=60
        )
        resp = json.loads(r.stdout)
        return resp.get("response", "")
    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    JOURNAL.mkdir(parents=True, exist_ok=True)
    processed = 0
    for item in INBOX.iterdir():
        if item.name.startswith(".") or item.is_dir():
            continue
        try:
            raw_full = item.read_text(errors="ignore")  # read full content
            raw = raw_full[:10000]  # for LLM context window
            # Archive full original gzipped to Layer 2
            today = datetime.date.today().isoformat()
            archive_sub = ARCHIVE_DIR / today
            archive_sub.mkdir(parents=True, exist_ok=True)
            archive_path = archive_sub / f"{item.stem}.md.gz"
            with gzip.open(archive_path, 'wt', encoding='utf-8') as gz:
                gz.write(raw_full)
            # Extract insight
            insight_raw = extract_insight(raw)
            distillate = {
                "source": item.name,
                "extracted_at": datetime.datetime.now().isoformat(),
                "raw_human_sample": raw_full[:500],  # verbatim 500-char quote
                "archived_gz": str(archive_path.relative_to(Path.home())),
                "parsed": json.loads(insight_raw) if "insights" in insight_raw else {"raw_output": insight_raw},
                "hash": hashlib.sha256(raw_full.encode()).hexdigest()[:16]
            }
            outfile = JOURNAL / f"{datetime.date.today()}-{item.stem[:30]}.json"
            outfile.write_text(json.dumps(distillate, indent=2))
            print(f"  ✓ {item.name} → {outfile.name}")
            processed += 1
            # Archive processed file
            item.parent.mkdir(parents=True, exist_ok=True); processed_dir = INBOX / "processed"; processed_dir.mkdir(exist_ok=True); item.rename(processed_dir / item.name)
        except Exception as e:
            print(f"  ✗ {item.name}: {e}", file=sys.stderr)
    print(f"\n✅ Compost extraction complete: {processed} items distilled.")
    print(f"   Output: {JOURNAL}")
    # Update STIM TTL confidence via stim_write
    try:
        ttl_conf = 0.35 + (0.02 * min(processed, 30))  # crude improvement curve
        subprocess.run([
            "curl", "-s", "http://localhost:11434/api/generate", "-d",
            json.dumps({"model": MODEL, "prompt": f"Compost TTL confidence now: {ttl_conf:.2f}. Log to mycelial-brain via brain_write namespace=stim_metrics content='{{\"compost_ttl_confidence\":{ttl_conf}}}'", "stream": False})
        ])
    except:
        pass

if __name__ == "__main__":
    (INBOX / "processed").mkdir(exist_ok=True)
    main()
