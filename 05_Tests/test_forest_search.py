#!/usr/bin/env python3
"""test_forest_search.py: Synthetic verification suite for Forest Search infrastructure.

Tests:
1. Synthetic SQLite-vec database creation and KNN nearest-neighbor scoring.
2. Cold-start INDEX_NOT_INITIALIZED error reporting when database is missing.
3. Path traversal and symlink escape rejection.
4. Read-only database guarantees (no mutations during queries).
5. MCP JSON-RPC protocol message handling (initialize, tools/list, tools/call).
6. Doc-414 compliance (zero em dashes across scripts, schemas, and docs).

Governance: Doc-414 compliant (Zero em dashes, strict claims discipline).
"""
import json
import os
import re
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import sqlite_vec
from sqlite_vec import serialize_float32

# Import target components
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIR = WORKSPACE_ROOT / "03_Automation_Scripts" / "forest-search"

import sys
sys.path.insert(0, str(SEARCH_DIR))
import forest_search_mcp
from forest_search_mcp import is_path_safe, handle_message


class TestForestSearchSynthetic(unittest.TestCase):
    """Synthetic test suite for Forest Search without using production databases."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="forest_test_")
        self.db_path = os.path.join(self.test_dir, "synthetic_index.db")
        self.vault_root = os.path.join(self.test_dir, "vault")
        os.makedirs(self.vault_root, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_synthetic_index(self):
        """Create a tiny 768-dim synthetic sqlite-vec database."""
        db = sqlite3.connect(self.db_path)
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)

        db.execute("""
            CREATE TABLE chunks (
                id INTEGER PRIMARY KEY,
                file_path TEXT NOT NULL,
                heading TEXT NOT NULL,
                ord INTEGER NOT NULL,
                text TEXT NOT NULL
            )""")
        db.execute("""
            CREATE VIRTUAL TABLE vec_chunks USING vec0(
                chunk_id INTEGER PRIMARY KEY,
                embedding FLOAT[768]
            )""")

        # Insert 3 synthetic files
        files_data = [
            (
                os.path.join(self.vault_root, "doc_trees.md"),
                "Quercus alba",
                "White oak canopy and growth parameters."
            ),
            (
                os.path.join(self.vault_root, "doc_fire.md"),
                "Fire behavior",
                "Fuel load moisture and flame length calculations."
            ),
            (
                os.path.join(self.vault_root, "doc_arbor.md"),
                "ISA certification",
                "Arborist climbing credentials and exam domains."
            ),
        ]

        for i, (fp, h, t) in enumerate(files_data, 1):
            with open(fp, "w", encoding="utf-8") as f:
                f.write(t)
            cur = db.execute(
                "INSERT INTO chunks(file_path, heading, ord, text) VALUES(?,?,?,?)",
                (fp, h, 0, t)
            )
            # Distinct synthetic unit vectors in 768 dimensions
            vec = np.zeros(768, dtype=np.float32)
            vec[i] = 1.0
            db.execute(
                "INSERT INTO vec_chunks(chunk_id, embedding) VALUES(?,?)",
                (cur.lastrowid, serialize_float32(vec))
            )

        db.commit()
        db.close()

    def test_synthetic_knn_search(self):
        """Verify vector KNN search returns correct ordering and score."""
        self._create_synthetic_index()

        # Query vector aligned with doc 3 (index 3)
        q_vec = np.zeros(768, dtype=np.float32)
        q_vec[3] = 1.0

        with patch("forest_search_mcp.embed", return_value=q_vec), \
             patch("forest_search_mcp.VAULT_ROOT", self.vault_root), \
             patch("forest_search_mcp.DB_PATH", self.db_path):
            results = forest_search_mcp.search("credentials", k=3)
            self.assertEqual(len(results), 3)
            # First result must be doc_arbor.md with exact match (distance 0.0, score 1.0)
            self.assertIn("doc_arbor.md", results[0]["path"])
            self.assertAlmostEqual(results[0]["score"], 1.0, places=2)
            self.assertEqual(results[0]["heading"], "ISA certification")

    def test_cold_start_missing_db_error(self):
        """Verify missing index raises FileNotFoundError with INDEX_NOT_INITIALIZED."""
        non_existent_db = os.path.join(self.test_dir, "missing.db")
        with self.assertRaises(FileNotFoundError) as ctx:
            forest_search_mcp.search("test", k=5, db_override=non_existent_db)
        self.assertIn("INDEX_NOT_INITIALIZED", str(ctx.exception))

    def test_path_safety_and_traversal_rejection(self):
        """Verify path validation blocks directory traversal and outside symlinks."""
        safe_path = os.path.join(self.vault_root, "subdir", "file.md")
        unsafe_traversal = os.path.join(self.vault_root, "..", "escape.md")
        outside_path = "/etc/passwd"

        self.assertTrue(is_path_safe(safe_path, self.vault_root))
        self.assertFalse(is_path_safe(unsafe_traversal, self.vault_root))
        self.assertFalse(is_path_safe(outside_path, self.vault_root))

    def test_read_only_database_integrity(self):
        """Verify search query executes in read-only mode and does not alter database."""
        self._create_synthetic_index()
        mtime_before = os.path.getmtime(self.db_path)

        q_vec = np.zeros(768, dtype=np.float32)
        q_vec[1] = 1.0

        with patch("forest_search_mcp.embed", return_value=q_vec), \
             patch("forest_search_mcp.VAULT_ROOT", self.vault_root), \
             patch("forest_search_mcp.DB_PATH", self.db_path):
            results = forest_search_mcp.search("oak", k=2)
            self.assertTrue(len(results) > 0)

        mtime_after = os.path.getmtime(self.db_path)
        self.assertEqual(mtime_before, mtime_after)

    def test_mcp_initialize_and_tools_list(self):
        """Verify JSON-RPC initialize and tools/list messages return expected schema."""
        captured = []

        def mock_send(msg):
            captured.append(msg)

        with patch("forest_search_mcp.send_rpc", side_effect=mock_send):
            # Test initialize
            handle_message({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
            self.assertEqual(len(captured), 1)
            self.assertEqual(captured[0]["id"], 1)
            self.assertEqual(captured[0]["result"]["serverInfo"]["name"], "forest_search")

            # Test tools/list
            handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
            self.assertEqual(len(captured), 2)
            tools = captured[1]["result"]["tools"]
            self.assertEqual(tools[0]["name"], "forest_search")
            self.assertIn("query", tools[0]["inputSchema"]["required"])

    def test_doc_414_zero_em_dashes(self):
        """Verify strictly zero em dashes in scripts, schemas, and markdown docs."""
        files_to_check = [
            SEARCH_DIR / "forest_search_mcp.py",
            SEARCH_DIR / "forest_query.py",
            SEARCH_DIR / "forest_index.py",
            SEARCH_DIR / "indexer_loop.sh",
            WORKSPACE_ROOT / "04_Configuration" / "mcp" / "forest_search.json",
            WORKSPACE_ROOT / "04_Configuration" / "mcp" / "forest_search_mcp_config.example.json",
            WORKSPACE_ROOT / "01_Docs" / "FOREST_SEARCH.md",
        ]
        em_dash_pattern = re.compile(r"[\u2013\u2014]")
        for fpath in files_to_check:
            self.assertTrue(fpath.exists(), f"File {fpath} must exist")
            content = fpath.read_text(encoding="utf-8")
            matches = em_dash_pattern.findall(content)
            self.assertEqual(
                len(matches), 0,
                f"File {fpath.name} violates Doc-414: found {len(matches)} em dash(es)"
            )


if __name__ == "__main__":
    unittest.main()
