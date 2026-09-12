#!/bin/bash
# Forest OS: forest-sim container entrypoint
# Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)

set -e

# Activate microfvs Python virtual environment if present
if [ -d "/opt/microfvs-env" ]; then
    export PATH="/opt/microfvs-env/bin:${PATH}"
fi

# List available variants
if [ "$1" = "variants" ] || [ "$1" = "--variants" ] || [ "$1" = "list" ]; then
    echo "======================================================================"
    echo " Forest OS: Available FVS Variants in Container"
    echo "======================================================================"
    find /usr/local/bin /opt/fvs/bin -maxdepth 1 -name "FVS*" 2>/dev/null | xargs -n 1 basename | sort -u
    exit 0
fi

# Serve microfvs REST API
if [ "$1" = "serve" ] || [ "$1" = "--web" ]; then
    echo "======================================================================"
    echo " Starting Forest OS microfvs REST API Service"
    echo " Endpoint: http://localhost:8000"
    echo " Documentation: http://localhost:8000/docs"
    echo "======================================================================"
    exec uvicorn microfvs.main:app --host 0.0.0.0 --port 8000
fi

# Execute fvs subcommand: fvs <variant> <keyword_file>
if [ "$1" = "fvs" ]; then
    shift
    variant="$1"
    shift
    # Support both "pn" and "FVSpn" naming
    if [[ "${variant}" == FVS* ]]; then
        exec_name="${variant}"
    else
        exec_name="FVS${variant}"
    fi

    if command -v "${exec_name}" >/dev/null 2>&1; then
        exec "${exec_name}" "$@"
    elif [ -f "/opt/fvs/bin/${exec_name}" ]; then
        exec "/opt/fvs/bin/${exec_name}" "$@"
    else
        echo "Error: FVS variant '${exec_name}' not found."
        echo "Available variants:"
        find /usr/local/bin /opt/fvs/bin -maxdepth 1 -name "FVS*" 2>/dev/null | xargs -n 1 basename | sort -u
        exit 1
    fi
fi

# Direct invocation of FVS variant executables (e.g. FVSpn input.key)
if [[ "$1" == FVS* ]]; then
    exec "$@"
fi

# Run microfvs CLI
if [ "$1" = "microfvs" ]; then
    shift
    if [ "$1" = "serve" ]; then
        exec uvicorn microfvs.main:app --host 0.0.0.0 --port 8000
    fi
    exec python3 -m microfvs "$@"
fi

# Default usage if no arguments provided
if [ $# -eq 0 ]; then
    echo "======================================================================"
    echo " Forest OS: Simulation Sidecar (forest-sim)"
    echo " Tools: USDA FVS (Forest Vegetation Simulator) & Vibrant Planet microfvs"
    echo "======================================================================"
    echo ""
    echo "Usage:"
    echo "  forest-sim fvs <variant> <keyword_file>     Run FVS variant simulation"
    echo "  forest-sim variants                        List available FVS variants"
    echo "  forest-sim serve                           Launch microfvs REST API on port 8000"
    echo "  forest-sim python <script.py>              Run Python simulation script"
    echo "  forest-sim bash                            Open interactive container shell"
    echo ""
    echo "Available FVS Variants:"
    find /usr/local/bin /opt/fvs/bin -maxdepth 1 -name "FVS*" 2>/dev/null | xargs -n 1 basename | sort -u | tr '\n' ' '
    echo ""
    exit 0
fi

# Fall through to execute custom command
exec "$@"
