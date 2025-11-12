#!/bin/bash
# Convenience script to run Windows .bat files from WSL
# Usage: ./run_windows_bat.sh scripts/windows/STATUS_CHECK.bat

if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-bat-file>"
    echo ""
    echo "Examples:"
    echo "  $0 scripts/windows/STATUS_CHECK.bat"
    echo "  $0 START_PHIGEN_SYSTEM.bat"
    echo "  $0 RUN_PASSWORD_VAULT.bat"
    exit 1
fi

BAT_FILE="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Convert to absolute path if relative
if [[ ! "$BAT_FILE" = /* ]]; then
    BAT_FILE="$SCRIPT_DIR/$BAT_FILE"
fi

# Check if file exists
if [ ! -f "$BAT_FILE" ]; then
    echo "Error: File not found: $BAT_FILE"
    exit 1
fi

# Convert to Windows path
WIN_PATH=$(wslpath -w "$BAT_FILE")

echo "Running: $WIN_PATH"
echo ""

# Run through cmd.exe
cmd.exe /c "$WIN_PATH"
