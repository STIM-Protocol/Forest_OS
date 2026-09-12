#!/bin/bash
# Forest OS: Open-FVS Compilation and Setup Script
# Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)

set -e

VARIANT_SCOPE="${1:-western}"
echo "======================================================================"
echo " Forest OS: Compiling USDA Open-FVS Simulators (Scope: ${VARIANT_SCOPE})"
echo "======================================================================"

SRC_DIR="/tmp/open-fvs"
INSTALL_DIR="/opt/fvs/bin"
mkdir -p "${INSTALL_DIR}"

if [ ! -d "${SRC_DIR}" ]; then
    echo "Cloning USDA Open-FVS upstream repository..."
    git clone --depth 1 https://github.com/forest-vegetation-simulator/fvs.git "${SRC_DIR}"
fi

cd "${SRC_DIR}"

# Define variants based on scope
if [ "${VARIANT_SCOPE}" = "all" ]; then
    VARIANTS=("pn" "wc" "ca" "so" "ie" "ut" "cr" "tt" "bm" "ec" "ci" "ws" "nc" "kt" "em" "ak" "oc" "ls" "ne" "sn")
else
    # Western states priority list
    VARIANTS=("pn" "wc" "ca" "so" "ie" "ut" "cr" "tt" "bm" "ec" "ci" "ws" "nc" "kt" "em" "ak" "oc")
fi

echo "Configuring CMake build for Open-FVS..."
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release

echo "Building FVS variant targets..."
for var in "${VARIANTS[@]}"; do
    target="FVS${var}"
    echo "Compiling variant: ${target}..."
    if cmake --build build --target "${target}" -j"$(nproc)" 2>/dev/null; then
        if [ -f "build/bin/${target}" ]; then
            cp "build/bin/${target}" "${INSTALL_DIR}/"
            ln -sf "${INSTALL_DIR}/${target}" "/usr/local/bin/${target}"
            echo "  [PASS] Installed ${target} to /usr/local/bin/${target}"
        fi
    else
        echo "  [WARN] Variant ${target} build failed or target name differed."
    fi
done

# If specific variant targets were not separated by CMake, build default targets
if [ -z "$(ls -A "${INSTALL_DIR}")" ]; then
    echo "Building all available build targets..."
    cmake --build build -j"$(nproc)" || true
    find build -type f -executable -name "FVS*" -exec cp {} "${INSTALL_DIR}/" \;
    for f in "${INSTALL_DIR}"/*; do
        if [ -f "$f" ]; then
            bname=$(basename "$f")
            ln -sf "$f" "/usr/local/bin/${bname}"
            echo "  [PASS] Installed ${bname} to /usr/local/bin/${bname}"
        fi
    done
fi

# Clean up build artifacts to minimize container image size
cd /
rm -rf "${SRC_DIR}"

echo "======================================================================"
echo " Open-FVS binaries installed in ${INSTALL_DIR}:"
ls -la "${INSTALL_DIR}"
echo "======================================================================"
