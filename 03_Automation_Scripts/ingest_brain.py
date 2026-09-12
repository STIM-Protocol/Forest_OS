#!/usr/bin/env python3
"""
Ingest Forest OS core protocol documents into the Mycelial Brain.
"""

import requests
import json
import re
from pathlib import Path

MCP_URL = "https://mycelial-brain-mcp-1084814124987.us-central1.run.app/mcp"

def mcp_call(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }
    resp = requests.post(MCP_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["result"]

def main():
    # Determine starting doc ID from existing brain index
    try:
        list_result = mcp_call("tools/call", {"name": "brain_list", "arguments": {}})
        existing = json.loads(list_result["content"][0]["text"]) if list_result.get("content") else []
        max_id = max([int(d.get("path", "doc-0").replace("doc-", "")) for d in existing], default=122)
    except Exception as e:
        print(f"  Note: Could not query existing docs ({e}); starting at doc-123")
        max_id = 122
    next_id = max_id + 1

    # Define documents to ingest: (filepath, tags, description)
    docs = [
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/ROOT_MANIFEST.md",
         ["protocol", "forest-os", "core", "constitution"],
         "Forest OS ROOT_MANIFEST: Constitutional principles, architecture, and Heartwood/Cambium pattern."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/WORLD_MODEL.md",
         ["protocol", "world-model", "system-state", "forest-os"],
         "World Model: Live system snapshot of vaults, agents, brain, and operational parameters."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/TAG_TAXONOMY.md",
         ["protocol", "taxonomy", "tags", "forest-os"],
         "Tag Taxonomy: Canonical vocabulary for classification and discovery."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/HEARTWOOD_CAMBIUM_PATTERN.md",
         ["protocol", "heartwood-cambium", "file-format", "forest-os"],
         "Heartwood/Cambium Pattern Specification: The .md + .jsonld pair format."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/INGESTION_PIPELINE.md",
         ["protocol", "ingestion", "pipeline", "forest-os"],
         "Ingestion Pipeline: Raw material to Forest Heartwood transformation process."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/00_Core_Protocols/SYNC_PROTOCOLS.md",
         ["protocol", "sync", "multi-vault", "forest-os"],
         "Sync Protocols: Forest, Library, Greenhouse, Understory, Compost, and Brain coordination."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/01_Docs/README.md",
         ["documentation", "forest-os", "public", "introduction"],
         "Forest OS public README: Overview, quick start, directory map, and survivability strategy."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/01_Docs/PROJECT_LAUNCH_COMPLETE.md",
         ["project", "status", "forest-os", "launch"],
         "Forest OS Project Launch Complete: Implementation status and next actions."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/01_Docs/OPERATIONAL_STATUS.md",
         ["status", "operational", "forest-os", "snapshot"],
         "Forest OS Operational Status: Live system snapshot, component health, metrics."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/02_Agent_Definitions/AGENT_REGISTRY.md",
         ["agent", "registry", "forest-os", "specification"],
         "Forest OS Agent Registry: Definitions and responsibilities of all autonomous agents."),
        
        ("/home/george/Myceliate_Master/GREENHOUSE/Active/Forest_OS/02_Agent_Definitions/AGENT_CHARTERS.md",
         ["agent", "charter", "forest-os", "protocol"],
         "Agent Charters: Operational directives for the six core agents."),
        
        ("/home/george/Myceliate_Master/UNDERSTORY/Research/Forest_OS/architecture-diagrams/system-overview.mmd",
         ["architecture", "diagram", "forest-os", "mermaid"],
         "Forest OS System Architecture: Mermaid diagram of vaults, agents, and data flow."),
        
        ("/home/george/Myceliate_Master/FOREST/001_PROJECTS/Forest_OS/01JWWZ1N-forest-os-project-manifest.md",
         ["project", "manifest", "forest-os", "01JWWZ1N"],
         "Forest OS Project Manifest: Mission, scope, structure, and 200-year design horizon."),
        
        ("/home/george/Myceliate_Master/FOREST/001_PROJECTS/Forest_OS/01JWWZ1Q-200-year-preservation-plan.md",
         ["preservation", "longevity", "200-year", "forest-os"],
         "200-year Preservation Plan: Layered archives, format migration, succession planning."),
    ]
    
    print(f"Preparing to ingest {len(docs)} Forest OS documents starting at doc-{next_id}...")
    
    for filepath, tags, description in docs:
        path = Path(filepath)
        if not path.exists():
            print(f"  SKIP: {path.name} not found")
            continue
        
        content = path.read_text()
        doc_path = f"doc-{next_id}"
        result = mcp_call("tools/call", {
            "name": "brain_write",
            "arguments": {
                "content": content,
                "tags": tags,
                "path": doc_path
            }
        })
        
        match = re.search(r"doc-\d+", result["content"][0]["text"])
        if match:
            doc_id = match.group(0)
            print(f"  ✓ Ingested {path.name} -> {doc_id} ({description})")
        else:
            print(f"  ? Ingested {path.name} (no ID returned)")
        next_id += 1
    
    print("\nIngest complete. Forest OS protocols are now searchable in the Mycelial Brain.")

if __name__ == "__main__":
    main()
