#!/usr/bin/env bash
# Forest OS: Desktop Launcher & Icon Uninstaller
# Cleans up installed Forest OS desktop shortcuts and icons.
# Doc-414 compliant (zero em dashes).

set -euo pipefail

ICONS_DEST="${HOME}/.local/share/icons/hicolor/scalable/apps"
APPS_DEST="${HOME}/.local/share/applications"
DIR_DEST="${HOME}/.local/share/desktop-directories"
MENU_DEST="${HOME}/.config/menus/applications-merged"
BIN_DEST="${HOME}/.local/bin"

echo "======================================================================"
echo " 🌲 Forest OS: Uninstalling Desktop Launchers and Icons"
echo "======================================================================"

# Remove desktop entries
rm -f "${APPS_DEST}"/forest-*.desktop

# Remove icons
rm -f "${ICONS_DEST}"/forest-*.svg

# Remove menu definitions
rm -f "${DIR_DEST}/forest-os.directory"
rm -f "${MENU_DEST}/forest-os.menu"

# Remove helper symlinks
rm -f "${BIN_DEST}/forest-workbench"
rm -f "${BIN_DEST}/forest-rstudio-launch"
rm -f "${BIN_DEST}/forest-sim-launch"
rm -f "${BIN_DEST}/forest-deepforest-launch"

# Refresh desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APPS_DEST}"
fi

echo "======================================================================"
echo " [PASS] Forest OS desktop launchers successfully uninstalled."
echo "======================================================================"
