#!/usr/bin/env bash
# Forest OS: RStudio Scientific Environment Launcher
# Launches the forest-r-engine container with RStudio Server on port 8787.
# Doc-414 compliant (zero em dashes).

set -euo pipefail

echo "======================================================================"
echo " 🌲 Forest OS: Launching RStudio LiDAR Scientific Sidecar"
echo "======================================================================"
echo "Container: forest-r-engine"
echo "Port:      http://localhost:8787"
echo ""

# Check if container is already running or start it
if command -v forest-r >/dev/null 2>&1; then
    echo "Starting RStudio Server in background..."
    forest-r --web &
    sleep 2
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:8787" >/dev/null 2>&1 || true
    fi
else
    echo "Error: forest-r wrapper not found in PATH." >&2
    exit 1
fi
