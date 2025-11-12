#!/bin/bash
# Convenience wrapper for Password Vault
# Usage: ./password_vault.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scripts/linux/run_password_vault.sh"
