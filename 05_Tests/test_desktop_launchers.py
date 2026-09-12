#!/usr/bin/env python3
"""
Forest OS: Test Suite for Desktop Launchers and Consolidated Workbench
Doc-414 compliant (zero em dashes).
"""

import os
import re
import shutil
import signal
import subprocess
import time
import urllib.request
from pathlib import Path
import unittest

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DESKTOP_DIR = WORKSPACE_ROOT / "04_Configuration" / "desktop"
APPS_DIR = DESKTOP_DIR / "applications"
ICONS_DIR = DESKTOP_DIR / "icons"
HTML_FILE = DESKTOP_DIR / "forest_workbench.html"
SCRIPTS_DIR = WORKSPACE_ROOT / "03_Automation_Scripts"

EXPECTED_DESKTOP_FILES = [
    "forest-workbench.desktop",
    "forest-birdnet.desktop",
    "forest-pydendron.desktop",
    "forest-rstudio.desktop",
    "forest-sim.desktop",
    "forest-deepforest.desktop",
    "forest-qgis.desktop",
]

EXPECTED_ICONS = [
    "forest-os.svg",
    "forest-workbench.svg",
    "forest-birdnet.svg",
    "forest-pydendron.svg",
    "forest-rstudio.svg",
    "forest-sim.svg",
    "forest-deepforest.svg",
]

class TestForestDesktopSuite(unittest.TestCase):

    def test_01_desktop_files_exist(self):
        """Verify all 7 expected desktop launcher files exist in source directory."""
        for filename in EXPECTED_DESKTOP_FILES:
            filepath = APPS_DIR / filename
            self.assertTrue(filepath.is_file(), f"Missing desktop file: {filename}")

    def test_02_svg_icons_exist(self):
        """Verify all expected SVG icons exist and are non-empty."""
        for icon_name in EXPECTED_ICONS:
            icon_path = ICONS_DIR / icon_name
            self.assertTrue(icon_path.is_file(), f"Missing icon: {icon_name}")
            self.assertGreater(icon_path.stat().st_size, 100, f"Icon appears empty: {icon_name}")

    def test_03_desktop_file_validation(self):
        """Run desktop-file-validate on all desktop entries."""
        validate_bin = shutil.which("desktop-file-validate")
        if not validate_bin:
            self.skipTest("desktop-file-validate not available on host")

        for filename in EXPECTED_DESKTOP_FILES:
            filepath = APPS_DIR / filename
            res = subprocess.run(
                [validate_bin, str(filepath)],
                capture_output=True,
                text=True
            )
            self.assertEqual(res.returncode, 0, f"Validation failed for {filename}: {res.stderr} {res.stdout}")

    def test_04_exec_targets_resolve(self):
        """Ensure the primary command in Exec= resolves to an executable binary or wrapper."""
        for filename in EXPECTED_DESKTOP_FILES:
            filepath = APPS_DIR / filename
            content = filepath.read_text(encoding="utf-8")
            match = re.search(r"^Exec=([^\s]+)", content, re.MULTILINE)
            self.assertTrue(match, f"No Exec= line found in {filename}")
            binary_name = match.group(1)

            # Check if binary is in PATH
            resolved = shutil.which(binary_name)
            self.assertIsNotNone(resolved, f"Exec command '{binary_name}' in {filename} not found in PATH")

    def test_05_doc_414_compliance_zero_em_dashes(self):
        """Enforce doc-414 compliance: zero em dashes across all desktop files, scripts, and HTML."""
        files_to_check = list(APPS_DIR.glob("*.desktop")) + \
                         list(SCRIPTS_DIR.glob("*.sh")) + \
                         [SCRIPTS_DIR / "forest-workbench", HTML_FILE]

        for filepath in files_to_check:
            if not filepath.exists():
                continue
            text = filepath.read_text(encoding="utf-8")
            self.assertNotIn("\u2014", text, f"Doc-414 violation (em dash) detected in: {filepath.name}")

    def test_06_workbench_html_structure(self):
        """Verify workbench HTML contains required modules, tools dataset, and canvas."""
        self.assertTrue(HTML_FILE.is_file(), "forest_workbench.html missing")
        content = HTML_FILE.read_text(encoding="utf-8")

        # Verify key modules
        self.assertIn("mycelium-canvas", content)
        self.assertIn("toolsData", content)
        self.assertIn("5483", content)
        self.assertIn("8787", content)
        self.assertIn("8000", content)
        self.assertIn("lidR", content)
        self.assertIn("TreeLS", content)
        self.assertIn("DeepForest", content)
        self.assertIn("Open-FVS", content)
        self.assertIn("pyDendron", content)

    def test_07_workbench_server_lifecycle(self):
        """Test launching the workbench server on port 5483 and querying via HTTP."""
        server_script = SCRIPTS_DIR / "forest-workbench"
        proc = subprocess.Popen(
            [str(server_script), "--port", "5483", "--no-browser"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        time.sleep(1.2)
        try:
            req = urllib.request.Request("http://localhost:5483/")
            with urllib.request.urlopen(req, timeout=3) as response:
                self.assertEqual(response.status, 200)
                body = response.read().decode("utf-8")
                self.assertIn("Forest OS", body)
                self.assertIn("5483", body)
        finally:
            proc.send_signal(signal.SIGINT)
            proc.wait(timeout=3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
