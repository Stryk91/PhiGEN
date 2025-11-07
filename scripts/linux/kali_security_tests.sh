#!/bin/bash
################################################################################
# PhiGEN Kali Linux Security Testing Suite
#
# Usage:
#   ./kali_security_tests.sh [test_name]
#   ./kali_security_tests.sh all          # Run all tests
#   ./kali_security_tests.sh secrets      # Run only secret detection
#   ./kali_security_tests.sh static       # Run only static analysis
#
# Requirements:
#   - Kali Linux
#   - Python 3.11+
#   - Tools: bandit, semgrep, truffleHog, gitleaks, safety
################################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
PROJECT_ROOT="/mnt/e/PythonProjects/PhiGEN"
REPORT_DIR="${PROJECT_ROOT}/security_reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create report directory
mkdir -p "$REPORT_DIR"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_tool() {
    if ! command -v "$1" &> /dev/null; then
        print_error "Tool not found: $1"
        echo "Install with: pip3 install $2"
        return 1
    fi
    return 0
}

################################################################################
# Test 1: Secret Detection
################################################################################

test_secrets() {
    print_header "TEST 1: Secret Detection & Credential Scanning"

    cd "$PROJECT_ROOT" || exit 1

    # TruffleHog - Deep secret scanning
    print_warning "Running TruffleHog (Git history scan)..."
    if check_tool "trufflehog" "truffleHog"; then
        trufflehog filesystem . \
            --json \
            --no-update \
            > "$REPORT_DIR/trufflehog_${TIMESTAMP}.json" 2>&1 || true

        # Check results
        SECRETS_FOUND=$(grep -c "Raw" "$REPORT_DIR/trufflehog_${TIMESTAMP}.json" || echo "0")
        if [ "$SECRETS_FOUND" -gt 0 ]; then
            print_error "Found $SECRETS_FOUND potential secrets!"
            echo "Report: $REPORT_DIR/trufflehog_${TIMESTAMP}.json"
        else
            print_success "TruffleHog: No secrets found"
        fi
    fi

    # Gitleaks - Git-specific secret detection
    print_warning "Running Gitleaks..."
    if check_tool "gitleaks" "gitleaks"; then
        gitleaks detect \
            --source . \
            --report-path "$REPORT_DIR/gitleaks_${TIMESTAMP}.json" \
            --verbose 2>&1 || true

        if [ -f "$REPORT_DIR/gitleaks_${TIMESTAMP}.json" ]; then
            LEAKS=$(jq 'length' "$REPORT_DIR/gitleaks_${TIMESTAMP}.json" 2>/dev/null || echo "0")
            if [ "$LEAKS" -gt 0 ]; then
                print_error "Found $LEAKS credential leaks!"
                echo "Report: $REPORT_DIR/gitleaks_${TIMESTAMP}.json"
            else
                print_success "Gitleaks: No leaks detected"
            fi
        fi
    fi

    # Manual pattern search for Discord token
    print_warning "Searching for Discord tokens..."
    if grep -r "MTM5MDY1MzgyMjUzNTM0MDE2Mg" . --exclude-dir=.git 2>/dev/null; then
        print_error "CRITICAL: Hardcoded Discord token found!"
    else
        print_success "No hardcoded Discord tokens"
    fi

    # Search for other common secrets
    print_warning "Searching for other credential patterns..."
    PATTERNS=(
        "password\s*=\s*['\"][^'\"]{8,}['\"]"
        "api_key\s*=\s*['\"][^'\"]{16,}['\"]"
        "secret\s*=\s*['\"][^'\"]{8,}['\"]"
        "token\s*=\s*['\"][^'\"]{16,}['\"]"
        "AKIA[0-9A-Z]{16}"
    )

    for pattern in "${PATTERNS[@]}"; do
        MATCHES=$(grep -rn -E "$pattern" . --include="*.py" --exclude-dir=.git 2>/dev/null || true)
        if [ ! -z "$MATCHES" ]; then
            print_error "Pattern match: $pattern"
            echo "$MATCHES" | head -3
        fi
    done
}

################################################################################
# Test 2: Static Code Analysis
################################################################################

test_static_analysis() {
    print_header "TEST 2: Static Code Analysis"

    cd "$PROJECT_ROOT" || exit 1

    # Bandit - Python security linter
    print_warning "Running Bandit..."
    if check_tool "bandit" "bandit"; then
        bandit -r . \
            -f json \
            -o "$REPORT_DIR/bandit_${TIMESTAMP}.json" \
            -ll 2>&1 || true

        # Parse results
        if [ -f "$REPORT_DIR/bandit_${TIMESTAMP}.json" ]; then
            HIGH=$(jq '[.results[] | select(.issue_severity=="HIGH")] | length' \
                "$REPORT_DIR/bandit_${TIMESTAMP}.json" 2>/dev/null || echo "0")
            MEDIUM=$(jq '[.results[] | select(.issue_severity=="MEDIUM")] | length' \
                "$REPORT_DIR/bandit_${TIMESTAMP}.json" 2>/dev/null || echo "0")

            echo "Results:"
            echo "  HIGH:   $HIGH issues"
            echo "  MEDIUM: $MEDIUM issues"

            if [ "$HIGH" -gt 0 ]; then
                print_error "High severity issues found!"
            else
                print_success "No high severity issues"
            fi
        fi
    fi

    # Semgrep - Pattern-based analysis
    print_warning "Running Semgrep..."
    if check_tool "semgrep" "semgrep"; then
        semgrep \
            --config=p/security-audit \
            --json \
            --output="$REPORT_DIR/semgrep_${TIMESTAMP}.json" \
            . 2>&1 || true

        if [ -f "$REPORT_DIR/semgrep_${TIMESTAMP}.json" ]; then
            FINDINGS=$(jq '.results | length' "$REPORT_DIR/semgrep_${TIMESTAMP}.json" 2>/dev/null || echo "0")
            if [ "$FINDINGS" -gt 0 ]; then
                print_warning "Semgrep found $FINDINGS potential issues"
            else
                print_success "Semgrep: No issues found"
            fi
        fi
    fi

    # Pylint - Code quality & security
    print_warning "Running Pylint (security checks)..."
    if check_tool "pylint" "pylint"; then
        find . -name "*.py" -not -path "./.git/*" -exec \
            pylint {} --disable=all \
            --enable=bad-builtin,exec-used,eval-used \
            + > "$REPORT_DIR/pylint_${TIMESTAMP}.txt" 2>&1 || true

        if grep -q "exec-used\|eval-used" "$REPORT_DIR/pylint_${TIMESTAMP}.txt"; then
            print_error "Dangerous function usage detected!"
        else
            print_success "No dangerous function usage"
        fi
    fi
}

################################################################################
# Test 3: Dependency Vulnerabilities
################################################################################

test_dependencies() {
    print_header "TEST 3: Dependency Vulnerability Scanning"

    cd "$PROJECT_ROOT" || exit 1

    # Safety - Known vulnerability database
    print_warning "Running Safety check..."
    if check_tool "safety" "safety"; then
        safety check \
            --json \
            --output "$REPORT_DIR/safety_${TIMESTAMP}.json" \
            2>&1 || true

        if [ -f "$REPORT_DIR/safety_${TIMESTAMP}.json" ]; then
            VULNS=$(jq 'length' "$REPORT_DIR/safety_${TIMESTAMP}.json" 2>/dev/null || echo "0")
            if [ "$VULNS" -gt 0 ]; then
                print_error "Found $VULNS vulnerable dependencies!"
            else
                print_success "No known vulnerabilities in dependencies"
            fi
        fi
    fi

    # pip-audit (alternative to safety)
    print_warning "Running pip-audit..."
    if check_tool "pip-audit" "pip-audit"; then
        pip-audit --format json > "$REPORT_DIR/pip_audit_${TIMESTAMP}.json" 2>&1 || true
    fi
}

################################################################################
# Test 4: Cryptographic Analysis
################################################################################

test_cryptography() {
    print_header "TEST 4: Cryptographic Implementation Testing"

    cd "$PROJECT_ROOT" || exit 1

    print_warning "Testing encryption implementation..."

    # Create test script
    cat > /tmp/test_crypto.py << 'EOFPYTHON'
import sys
sys.path.insert(0, '/mnt/e/PythonProjects/PhiGEN')

from password_vault_backend import VaultEncryption, PasswordVault
import tempfile
import os

print("=" * 60)
print("CRYPTOGRAPHIC IMPLEMENTATION TEST")
print("=" * 60)

# Test 1: Key derivation consistency
print("\n[TEST 1] Key Derivation Consistency")
e1 = VaultEncryption('TestPassword123!')
e2 = VaultEncryption('TestPassword123!')

if e1.salt == e2.salt:
    print("❌ FAIL: Same salt used (should be random)")
else:
    print("✅ PASS: Unique salts generated")

# Test 2: Encryption/Decryption with same password
print("\n[TEST 2] Encrypt/Decrypt Cycle")
try:
    plaintext = "SecretPassword123!"
    encrypted = e1.encrypt(plaintext)
    decrypted = e1.decrypt(encrypted)

    if decrypted == plaintext:
        print("✅ PASS: Same instance can decrypt")
    else:
        print("❌ FAIL: Decryption mismatch")
except Exception as e:
    print(f"❌ FAIL: {e}")

# Test 3: Cross-instance decryption (CRITICAL BUG TEST)
print("\n[TEST 3] Cross-Instance Decryption (CRITICAL)")
print("Testing if encryption key is properly derived from password...")

# Use same salt to simulate reopening vault
salt = e1.salt
e3 = VaultEncryption('TestPassword123!', salt=salt)

try:
    encrypted = e1.encrypt("test_data")
    decrypted = e3.decrypt(encrypted)
    print("❌ FAIL: Different instance can decrypt (unexpected!)")
    print("This means the bug might be fixed or salt is working")
except Exception as e:
    print("✅ EXPECTED FAILURE: Cannot decrypt across instances")
    print(f"Error: {e}")
    print("⚠️  This confirms the encryption bug exists!")

# Test 4: Vault integration test
print("\n[TEST 4] Full Vault Lifecycle Test")
with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tf:
    test_db = tf.name

try:
    # Create vault
    v1 = PasswordVault(test_db)
    v1.set_master_password("VaultTest123!")
    entry_id = v1.add_password("test_site", "user@test.com", "secret123")
    v1.lock()

    print("✅ Created vault and saved password")

    # Reopen vault (simulates app restart)
    v2 = PasswordVault(test_db)
    if v2.unlock("VaultTest123!"):
        print("✅ Vault unlocked successfully")

        try:
            entries = v2.get_all_passwords()
            if len(entries) > 0 and entries[0].password == "secret123":
                print("✅ PASS: Password retrieved correctly!")
                print("🎉 ENCRYPTION BUG IS FIXED!")
            else:
                print("❌ FAIL: Password mismatch or not found")
                print("🔴 ENCRYPTION BUG STILL EXISTS!")
        except Exception as e:
            print(f"❌ FAIL: Cannot decrypt passwords: {e}")
            print("🔴 CRITICAL: ENCRYPTION BUG CONFIRMED!")
    else:
        print("❌ FAIL: Cannot unlock vault")

finally:
    if os.path.exists(test_db):
        os.unlink(test_db)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
EOFPYTHON

    # Run the test
    python3 /tmp/test_crypto.py

    # Cleanup
    rm /tmp/test_crypto.py
}

################################################################################
# Test 5: SQL Injection Testing
################################################################################

test_sql_injection() {
    print_header "TEST 5: SQL Injection Testing"

    print_warning "Analyzing SQL queries..."

    cd "$PROJECT_ROOT" || exit 1

    # Search for potentially unsafe SQL
    print_warning "Checking for unsafe SQL patterns..."

    UNSAFE_PATTERNS=(
        "\.format\(.*SELECT"
        "f\".*SELECT"
        "%.*SELECT"
        "execute\(.*\+.*\)"
    )

    SAFE=true
    for pattern in "${UNSAFE_PATTERNS[@]}"; do
        MATCHES=$(grep -rn -E "$pattern" . --include="*.py" --exclude-dir=.git 2>/dev/null || true)
        if [ ! -z "$MATCHES" ]; then
            print_error "Unsafe SQL pattern found: $pattern"
            echo "$MATCHES"
            SAFE=false
        fi
    done

    if [ "$SAFE" = true ]; then
        print_success "No unsafe SQL patterns detected"
    fi

    # Check for parameterized queries (good)
    print_warning "Verifying parameterized queries..."
    PARAM_COUNT=$(grep -r "execute.*\?" . --include="*.py" --exclude-dir=.git | wc -l)
    print_success "Found $PARAM_COUNT parameterized queries (good practice)"
}

################################################################################
# Test 6: Command Injection Testing
################################################################################

test_command_injection() {
    print_header "TEST 6: Command Injection Vulnerability Testing"

    cd "$PROJECT_ROOT" || exit 1

    print_warning "Searching for command injection vulnerabilities..."

    # Look for subprocess with shell=True
    FILES_WITH_SHELL=$(grep -rn "subprocess.*shell=True" . --include="*.py" --exclude-dir=.git || true)

    if [ ! -z "$FILES_WITH_SHELL" ]; then
        print_error "Found subprocess calls with shell=True:"
        echo "$FILES_WITH_SHELL"
        echo ""
        print_error "These are potential command injection vulnerabilities!"
    else
        print_success "No shell=True found in subprocess calls"
    fi

    # Look for os.system
    FILES_WITH_SYSTEM=$(grep -rn "os\.system" . --include="*.py" --exclude-dir=.git || true)

    if [ ! -z "$FILES_WITH_SYSTEM" ]; then
        print_error "Found os.system calls:"
        echo "$FILES_WITH_SYSTEM"
    else
        print_success "No os.system calls found"
    fi

    # Look for eval/exec
    FILES_WITH_EVAL=$(grep -rn "\(eval\|exec\)(" . --include="*.py" --exclude-dir=.git || true)

    if [ ! -z "$FILES_WITH_EVAL" ]; then
        print_error "Found eval/exec calls:"
        echo "$FILES_WITH_EVAL"
    else
        print_success "No eval/exec calls found"
    fi
}

################################################################################
# Test 7: Path Traversal Testing
################################################################################

test_path_traversal() {
    print_header "TEST 7: Path Traversal Vulnerability Testing"

    cd "$PROJECT_ROOT" || exit 1

    print_warning "Checking for path traversal vulnerabilities..."

    # Look for open() calls without validation
    FILES=$(grep -rn "open(" . --include="*.py" --exclude-dir=.git | \
            grep -v "sanitize\|validate\|resolve\|is_relative_to" || true)

    if [ ! -z "$FILES" ]; then
        print_warning "Found file operations that may need path validation:"
        echo "$FILES" | head -10
        echo ""
        echo "Review these manually for path traversal risks"
    fi

    # Check for Path.resolve() usage (good)
    RESOLVED=$(grep -r "Path.*resolve\|pathlib" . --include="*.py" --exclude-dir=.git | wc -l)
    if [ "$RESOLVED" -gt 0 ]; then
        print_success "Found $RESOLVED uses of path resolution (good practice)"
    fi
}

################################################################################
# Test 8: Password Cracking Simulation
################################################################################

test_password_cracking() {
    print_header "TEST 8: Password Strength Testing (Cracking Simulation)"

    print_warning "Benchmarking key derivation speed..."

    cat > /tmp/test_kdf_speed.py << 'EOFPYTHON'
import sys
sys.path.insert(0, '/mnt/e/PythonProjects/PhiGEN')

from password_vault_backend import VaultEncryption
import time

iterations = 100
start = time.time()

for i in range(iterations):
    VaultEncryption('test_password_123')

elapsed = time.time() - start
per_attempt = (elapsed / iterations) * 1000

print(f"Key derivation speed: {per_attempt:.2f}ms per attempt")
print(f"Brute force rate: {1000/per_attempt:.0f} attempts/second")
print(f"")
print(f"Time to crack (estimates):")
print(f"  1,000 passwords:     {(per_attempt * 1000 / 1000):.1f} seconds")
print(f"  10,000 passwords:    {(per_attempt * 10000 / 1000 / 60):.1f} minutes")
print(f"  100,000 passwords:   {(per_attempt * 100000 / 1000 / 3600):.1f} hours")
print(f"  1,000,000 passwords: {(per_attempt * 1000000 / 1000 / 3600 / 24):.1f} days")
EOFPYTHON

    python3 /tmp/test_kdf_speed.py
    rm /tmp/test_kdf_speed.py

    print_warning "For reference:"
    echo "  - OWASP recommends: >1000ms per attempt"
    echo "  - Current PBKDF2 iterations: 100,000"
    echo "  - Recommended: 600,000 iterations or Argon2id"
}

################################################################################
# Test 9: Generate Summary Report
################################################################################

generate_summary() {
    print_header "Generating Security Summary Report"

    SUMMARY_FILE="$REPORT_DIR/summary_${TIMESTAMP}.txt"

    cat > "$SUMMARY_FILE" << EOF
PhiGEN Security Test Summary
Generated: $(date)
==============================================================================

REPORTS GENERATED:
$(ls -lh "$REPORT_DIR" | tail -n +2)

CRITICAL ISSUES TO VERIFY:
1. Check trufflehog report for exposed Discord token
2. Review bandit report for high severity issues
3. Verify encryption bug fix with cryptography test
4. Check for shell=True in subprocess calls
5. Verify path validation in file operations

NEXT STEPS:
1. Review all JSON reports in: $REPORT_DIR
2. Prioritize CRITICAL and HIGH severity findings
3. Implement fixes from remediation guide
4. Re-run tests after fixes
5. Document all changes

==============================================================================
EOF

    cat "$SUMMARY_FILE"
    print_success "Summary saved to: $SUMMARY_FILE"
}

################################################################################
# Main Test Runner
################################################################################

main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║        PhiGEN Security Testing Suite (Kali Linux)           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}\n"

    TEST_NAME="${1:-all}"

    case "$TEST_NAME" in
        secrets)
            test_secrets
            ;;
        static)
            test_static_analysis
            ;;
        dependencies|deps)
            test_dependencies
            ;;
        crypto|encryption)
            test_cryptography
            ;;
        sql)
            test_sql_injection
            ;;
        command|cmdinject)
            test_command_injection
            ;;
        path|traversal)
            test_path_traversal
            ;;
        password|crack)
            test_password_cracking
            ;;
        all)
            test_secrets
            test_static_analysis
            test_dependencies
            test_cryptography
            test_sql_injection
            test_command_injection
            test_path_traversal
            test_password_cracking
            generate_summary
            ;;
        *)
            echo "Usage: $0 [test_name]"
            echo ""
            echo "Available tests:"
            echo "  secrets      - Secret detection (TruffleHog, Gitleaks)"
            echo "  static       - Static analysis (Bandit, Semgrep)"
            echo "  dependencies - Dependency vulnerabilities (Safety)"
            echo "  crypto       - Cryptographic testing"
            echo "  sql          - SQL injection testing"
            echo "  command      - Command injection testing"
            echo "  path         - Path traversal testing"
            echo "  password     - Password cracking simulation"
            echo "  all          - Run all tests (default)"
            exit 1
            ;;
    esac

    echo ""
    print_success "Testing complete! Reports saved to: $REPORT_DIR"
}

# Run main
main "$@"
