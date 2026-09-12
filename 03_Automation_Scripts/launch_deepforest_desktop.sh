#!/usr/bin/env bash
# Forest OS: DeepForest Interactive CLI Launcher
# Provides terminal interface for DeepForest canopy crown detection.
# Doc-414 compliant (zero em dashes).

set -euo pipefail

echo "======================================================================"
echo " 🌲 Forest OS: DeepForest Tree Crown Detection"
echo "======================================================================"
echo "Pre-trained PyTorch deep learning for individual tree crown detection."
echo "Running in isolated user-space Python 3.11 environment (Tier 1 uv tool)."
echo "======================================================================"
echo ""

if command -v deepforest >/dev/null 2>&1; then
    deepforest --help
    echo ""
    echo "Example execution:"
    echo "  deepforest --input plot_orthomosaic.tif --output crowns.shp --patch-size 400"
    echo ""
    read -rp "Press Enter to exit or Ctrl+C to terminate..."
else
    echo "Error: deepforest not found in PATH." >&2
    exit 1
fi
