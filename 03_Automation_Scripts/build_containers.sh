#!/bin/bash
# Forest OS: Tier 3 Scientific Container Build Orchestrator
# Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)

set -e

SCRIPT_DIR="$(cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_DIR="${WORKSPACE_ROOT}/04_Configuration/containers"

# Detect container runtime
detect_runtime() {
    if command -v podman >/dev/null 2>&1; then
        echo "podman"
    elif command -v docker >/dev/null 2>&1; then
        echo "docker"
    else
        echo ""
    fi
}

RUNTIME=$(detect_runtime)
if [ -z "${RUNTIME}" ]; then
    echo "Error: Neither podman nor docker was found in PATH." >&2
    exit 1
fi

print_help() {
    cat <<EOF
Forest OS Container Build Orchestrator
Runtime: ${RUNTIME}

Usage:
  bash build_containers.sh [TARGET] [OPTIONS]

Targets:
  all               Build both forest-r-engine and forest-sim (default)
  r-engine          Build forest-r-engine only
  sim               Build forest-sim only

Options:
  --all-variants    Compile all 20 Open-FVS variants for forest-sim (default: western)
  --no-symlinks     Skip installing wrapper symlinks into ~/.local/bin/
  -h, --help        Show this help reference
EOF
}

TARGET="all"
FVS_SCOPE="western"
INSTALL_SYMLINKS=true

for arg in "$@"; do
    case "$arg" in
        all|r-engine|sim)
            TARGET="$arg"
            ;;
        --all-variants)
            FVS_SCOPE="all"
            ;;
        --no-symlinks)
            INSTALL_SYMLINKS=false
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo "Unknown argument: $arg" >&2
            print_help
            exit 1
            ;;
    esac
done

install_symlinks() {
    if [ "${INSTALL_SYMLINKS}" = true ]; then
        LOCAL_BIN="${HOME}/.local/bin"
        mkdir -p "${LOCAL_BIN}"
        chmod +x "${SCRIPT_DIR}/forest-r"
        chmod +x "${SCRIPT_DIR}/forest-sim"
        ln -sf "${SCRIPT_DIR}/forest-r" "${LOCAL_BIN}/forest-r"
        ln -sf "${SCRIPT_DIR}/forest-sim" "${LOCAL_BIN}/forest-sim"
        echo "Installed CLI wrappers into ${LOCAL_BIN}:"
        echo "  - ${LOCAL_BIN}/forest-r -> ${SCRIPT_DIR}/forest-r"
        echo "  - ${LOCAL_BIN}/forest-sim -> ${SCRIPT_DIR}/forest-sim"
    fi
}

build_r_engine() {
    echo "======================================================================"
    echo " Building Container Image: forest-r-engine"
    echo " Context: ${CONFIG_DIR}/forest-r-engine"
    echo "======================================================================"
    if [ ! -d "${CONFIG_DIR}/forest-r-engine" ]; then
        echo "Error: Directory ${CONFIG_DIR}/forest-r-engine does not exist." >&2
        return 1
    fi
    "${RUNTIME}" build \
        -t forest-r-engine \
        -f "${CONFIG_DIR}/forest-r-engine/Containerfile" \
        "${CONFIG_DIR}/forest-r-engine"
    echo "[PASS] forest-r-engine build completed."
}

build_sim() {
    echo "======================================================================"
    echo " Building Container Image: forest-sim (FVS Scope: ${FVS_SCOPE})"
    echo " Context: ${CONFIG_DIR}/forest-sim"
    echo "======================================================================"
    if [ ! -d "${CONFIG_DIR}/forest-sim" ]; then
        echo "Error: Directory ${CONFIG_DIR}/forest-sim does not exist." >&2
        return 1
    fi
    "${RUNTIME}" build \
        --build-arg FVS_VARIANTS="${FVS_SCOPE}" \
        -t forest-sim \
        -f "${CONFIG_DIR}/forest-sim/Containerfile" \
        "${CONFIG_DIR}/forest-sim"
    echo "[PASS] forest-sim build completed."
}

# Main execution dispatch
case "${TARGET}" in
    all)
        build_r_engine
        build_sim
        ;;
    r-engine)
        build_r_engine
        ;;
    sim)
        build_sim
        ;;
esac

install_symlinks

echo "======================================================================"
echo " Forest OS Tier 3 container build pipeline finished successfully."
echo "======================================================================"
