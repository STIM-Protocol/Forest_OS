#!/usr/bin/env bash
# Forest OS: Open-FVS Growth Simulation Environment Launcher
# Launches the forest-sim container environment or microfvs daemon.
# Doc-414 compliant (zero em dashes).

set -euo pipefail

echo "======================================================================"
echo " 🌲 Forest OS: Open-FVS Forest Growth Simulator"
echo "======================================================================"
echo "Available Commands:"
echo "  1) List all 22 compiled regional FVS variants"
echo "  2) Launch microfvs REST API daemon (port 8000)"
echo "  3) Open interactive simulation shell inside container"
echo "  4) Exit"
echo "======================================================================"

if [ $# -gt 0 ]; then
    forest-sim "$@"
    exit 0
fi

read -rp "Select option [1-4]: " choice

case "$choice" in
    1)
        forest-sim variants
        read -rp "Press Enter to exit..."
        ;;
    2)
        echo "Starting microfvs REST API on http://localhost:8000..."
        if command -v xdg-open >/dev/null 2>&1; then
            (sleep 2 && xdg-open "http://localhost:8000/docs" >/dev/null 2>&1) &
        fi
        forest-sim serve
        ;;
    3)
        forest-sim /bin/bash
        ;;
    *)
        echo "Exiting."
        exit 0
        ;;
esac
