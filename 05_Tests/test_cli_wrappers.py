#!/usr/bin/env python3
"""
test_cli_wrappers.py - Verification suite for Forest OS host CLI wrappers
Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)
"""

import os
import subprocess
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSPACE_ROOT / "03_Automation_Scripts"


class TestCliWrappers(unittest.TestCase):
    """Test suite verifying CLI wrappers, execution flags, and help menus."""

    def test_scripts_exist_and_executable(self):
        """Verify that wrapper scripts exist and have execute bit set."""
        scripts = ["forest-r", "forest-sim", "build_containers.sh"]
        for s in scripts:
            spath = SCRIPTS_DIR / s
            self.assertTrue(spath.exists(), f"Script '{s}' must exist")
            self.assertTrue(os.access(spath, os.X_OK), f"Script '{s}' must be executable")

    def test_bash_syntax(self):
        """Verify that all bash scripts pass syntax validation (bash -n)."""
        scripts = ["forest-r", "forest-sim", "build_containers.sh"]
        for s in scripts:
            spath = SCRIPTS_DIR / s
            res = subprocess.run(["bash", "-n", str(spath)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f"Syntax error in {s}: {res.stderr}")

    def test_forest_r_help(self):
        """Verify forest-r --help returns code 0 and usage text."""
        res = subprocess.run([str(SCRIPTS_DIR / "forest-r"), "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Forest OS Scientific R Engine CLI (forest-r)", res.stdout)
        self.assertIn("--web", res.stdout)
        self.assertIn("/workspace", res.stdout)

    def test_forest_sim_help(self):
        """Verify forest-sim --help returns code 0 and usage text."""
        res = subprocess.run([str(SCRIPTS_DIR / "forest-sim"), "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Forest OS Growth & Yield Simulation CLI (forest-sim)", res.stdout)
        self.assertIn("fvs", res.stdout)
        self.assertIn("microfvs", res.stdout)

    def test_build_containers_help(self):
        """Verify build_containers.sh --help returns code 0 and options."""
        res = subprocess.run([str(SCRIPTS_DIR / "build_containers.sh"), "--help"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Forest OS Container Build Orchestrator", res.stdout)
        self.assertIn("r-engine", res.stdout)
        self.assertIn("sim", res.stdout)

    def test_missing_image_fails_cleanly(self):
        """Verify wrappers exit cleanly with code 1 when images are unbuilt."""
        test_env_r = {**os.environ, "FOREST_R_IMAGE": "forest-r-engine-unbuilt-test"}
        res_r = subprocess.run([str(SCRIPTS_DIR / "forest-r"), "-e", "1+1"], capture_output=True, text=True, env=test_env_r)
        self.assertEqual(res_r.returncode, 1)
        self.assertIn("is not built", res_r.stderr)

        test_env_sim = {**os.environ, "FOREST_SIM_IMAGE": "forest-sim-unbuilt-test"}
        res_sim = subprocess.run([str(SCRIPTS_DIR / "forest-sim"), "variants"], capture_output=True, text=True, env=test_env_sim)
        self.assertEqual(res_sim.returncode, 1)
        self.assertIn("is not built", res_sim.stderr)

    def test_doc_414_compliance(self):
        """Verify zero em dashes across scripts and test files."""
        for check_dir in [SCRIPTS_DIR, WORKSPACE_ROOT / "05_Tests"]:
            for root, dirs, files in os.walk(check_dir):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for file in files:
                    if file.endswith((".pyc", ".pyo")):
                        continue
                    fpath = Path(root) / file
                    data = fpath.read_bytes()
                    # Check for em dash byte sequence
                    em_dash_bytes = bytes([0xE2, 0x80, 0x94])
                    self.assertNotIn(
                        em_dash_bytes,
                        data,
                        f"Em dash detected in {fpath.relative_to(WORKSPACE_ROOT)}"
                    )


if __name__ == "__main__":
    unittest.main()
