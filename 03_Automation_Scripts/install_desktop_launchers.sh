#!/usr/bin/env bash
# Forest OS: Desktop Launcher & Icon Installer
# Integrates Forest OS applications into user GNOME/XDG application menus.
# Doc-414 compliant (zero em dashes).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

ICONS_SRC="${WORKSPACE_ROOT}/04_Configuration/desktop/icons"
APPS_SRC="${WORKSPACE_ROOT}/04_Configuration/desktop/applications"
MENU_SRC="${WORKSPACE_ROOT}/04_Configuration/desktop/menu"

ICONS_DEST="${HOME}/.local/share/icons/hicolor/scalable/apps"
APPS_DEST="${HOME}/.local/share/applications"
DIR_DEST="${HOME}/.local/share/desktop-directories"
MENU_DEST="${HOME}/.config/menus/applications-merged"
BIN_DEST="${HOME}/.local/bin"

echo "======================================================================"
echo " 🌲 Forest OS: Installing Desktop Launchers and Icons"
echo "======================================================================"

# Ensure directories exist
mkdir -p "${ICONS_DEST}" "${APPS_DEST}" "${DIR_DEST}" "${MENU_DEST}" "${BIN_DEST}"

# 1. Install helper executables
echo "Installing CLI launcher helpers into ${BIN_DEST}..."
ln -sf "${WORKSPACE_ROOT}/03_Automation_Scripts/forest-workbench" "${BIN_DEST}/forest-workbench"
ln -sf "${WORKSPACE_ROOT}/03_Automation_Scripts/launch_rstudio_desktop.sh" "${BIN_DEST}/forest-rstudio-launch"
ln -sf "${WORKSPACE_ROOT}/03_Automation_Scripts/launch_sim_desktop.sh" "${BIN_DEST}/forest-sim-launch"
ln -sf "${WORKSPACE_ROOT}/03_Automation_Scripts/launch_deepforest_desktop.sh" "${BIN_DEST}/forest-deepforest-launch"

# 2. Install scalable SVG icons
echo "Installing scalable SVG icons into ${ICONS_DEST}..."
cp -v "${ICONS_SRC}"/*.svg "${ICONS_DEST}/"

# 3. Install desktop entries
echo "Installing desktop entries into ${APPS_DEST}..."
cp -v "${APPS_SRC}"/*.desktop "${APPS_DEST}/"

# 4. Install XDG menu definition
echo "Installing XDG menu hierarchy..."
if [ -f "${MENU_SRC}/forest-os.directory" ]; then
    cp -v "${MENU_SRC}/forest-os.directory" "${DIR_DEST}/"
fi
if [ -f "${MENU_SRC}/forest-os.menu" ]; then
    cp -v "${MENU_SRC}/forest-os.menu" "${MENU_DEST}/"
fi

# 5. Refresh desktop database
echo "Refreshing FreeDesktop application database..."
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APPS_DEST}"
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t "${HOME}/.local/share/icons/hicolor" 2>/dev/null || true
fi

echo "======================================================================"
echo " [PASS] Forest OS desktop integration completed successfully."
echo " Launchers are now available in your desktop application menu."
echo "======================================================================"
