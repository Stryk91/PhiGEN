#!/bin/bash
# PhiGEN Status Check - WSL/Linux
# Convenience wrapper for scripts/linux/status_check.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scripts/linux/status_check.sh" "$@"
