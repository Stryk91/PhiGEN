#!/bin/bash
# Convenience wrapper for Status Monitor
# Usage: ./status_monitor.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scripts/linux/run_status_monitor.sh"
