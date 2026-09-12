#!/usr/bin/env python3
"""
test_container_recipes.py - Verification suite for Forest OS container definitions
Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)
"""

import os
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = WORKSPACE_ROOT / "04_Configuration" / "containers"


class TestContainerRecipes(unittest.TestCase):
    """Test suite verifying Containerfiles, entrypoints, and build scripts."""

    def test_r_engine_structure(self):
        """Verify forest-r-engine directory and file structure."""
        r_dir = CONFIG_DIR / "forest-r-engine"
        self.assertTrue(r_dir.exists(), "forest-r-engine directory must exist")
        self.assertTrue((r_dir / "Containerfile").exists(), "Containerfile must exist")
        self.assertTrue((r_dir / "install_packages.R").exists(), "install_packages.R must exist")
        self.assertTrue((r_dir / "entrypoint.sh").exists(), "entrypoint.sh must exist")
        self.assertTrue((r_dir / "README.md").exists(), "README.md must exist")

    def test_r_engine_containerfile_contents(self):
        """Verify key instructions in forest-r-engine Containerfile."""
        content = (CONFIG_DIR / "forest-r-engine" / "Containerfile").read_text(encoding="utf-8")
        self.assertIn("FROM rocker/geospatial", content)
        self.assertIn("libhdf5-dev", content)
        self.assertIn("install_packages.R", content)
        self.assertIn("ENTRYPOINT", content)
        self.assertIn("EXPOSE 8787", content)
        self.assertIn("/workspace", content)

    def test_r_engine_packages_coverage(self):
        """Verify that all required scientific packages are present in install_packages.R."""
        content = (CONFIG_DIR / "forest-r-engine" / "install_packages.R").read_text(encoding="utf-8")
        required_packages = [
            "lidR",
            "TreeLS",
            "rGEDI",
            "BIOMASS",
            "dplR",
            "allodb",
            "ForestTools",
            "hemispheR",
            "treeclim"
        ]
        for pkg in required_packages:
            self.assertIn(pkg, content, f"Package '{pkg}' must be defined in install_packages.R")

    def test_sim_structure(self):
        """Verify forest-sim directory and file structure."""
        sim_dir = CONFIG_DIR / "forest-sim"
        self.assertTrue(sim_dir.exists(), "forest-sim directory must exist")
        self.assertTrue((sim_dir / "Containerfile").exists(), "Containerfile must exist")
        self.assertTrue((sim_dir / "compile_fvs.sh").exists(), "compile_fvs.sh must exist")
        self.assertTrue((sim_dir / "entrypoint.sh").exists(), "entrypoint.sh must exist")
        self.assertTrue((sim_dir / "README.md").exists(), "README.md must exist")

    def test_sim_containerfile_contents(self):
        """Verify key instructions in forest-sim Containerfile."""
        content = (CONFIG_DIR / "forest-sim" / "Containerfile").read_text(encoding="utf-8")
        self.assertIn("usfs-fvs", content)
        self.assertIn("microfvs", content)
        self.assertIn("ENTRYPOINT", content)
        self.assertIn("EXPOSE 8000", content)
        self.assertIn("/workspace", content)

    def test_doc_414_compliance(self):
        """Verify zero em dashes across all authored container files."""
        for root, dirs, files in os.walk(CONFIG_DIR):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                if file.endswith((".pyc", ".pyo")):
                    continue
                fpath = Path(root) / file
                data = fpath.read_bytes()
                em_dash_bytes = bytes([0xE2, 0x80, 0x94])
                self.assertNotIn(
                    em_dash_bytes,
                    data,
                    f"Em dash detected in {fpath.relative_to(WORKSPACE_ROOT)}"
                )


if __name__ == "__main__":
    unittest.main()
