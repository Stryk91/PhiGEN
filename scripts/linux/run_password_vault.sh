#!/bin/bash
# Launch PhiGEN Password Vault GUI
# Usage: ./scripts/linux/run_password_vault.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$SCRIPT_DIR"

echo "[PhiGEN Password Vault]"
echo "Launching Password Vault GUI..."
echo ""

# Activate virtual environment and run
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    # Set Qt platform explicitly for WSL/X11 compatibility
    export QT_QPA_PLATFORM=xcb
    export DISPLAY=${DISPLAY:-:0}
    python -m src.password_vault.app
else
    echo "Error: Virtual environment not found at $SCRIPT_DIR/.venv"
    exit 1
fi
