# SuperNinja Agent Task Prompts

**Created:** 2025-11-08
**For:** STRYK (Copy these prompts to SuperNinja platform)
**Repository:** https://github.com/Stryk91/PhiGEN

**Important:** Before using any of these prompts, JC must complete the steps in GIT_BRANCHING_GUIDE.md (push to GitHub and create safety tag).

---

## How to Use These Prompts

1. **Complete Git setup first** (see GIT_BRANCHING_GUIDE.md)
2. **Copy entire prompt** for the task you want
3. **Paste into SuperNinja** agent interface
4. **Wait for agent to complete** and create Pull Request
5. **Review PR on GitHub** before merging
6. **Merge or reject** based on quality

---

## TASK #1: Codebase Security Audit (CRITICAL PRIORITY)

**Estimated Time:** 4-6 hours
**Value:** ⭐⭐⭐⭐⭐ (Protects password vault + API keys)

```
=== TASK: Comprehensive Security Audit for PhiGEN ===

GIT SAFETY PROTOCOL:
1. Clone from: https://github.com/Stryk91/PhiGEN.git
2. Create branch: git checkout -b agent-security-audit
3. Work only in this branch
4. Push branch when complete (DO NOT merge to main)
5. Create Pull Request for my review

CONTEXT:
PhiGEN is a multi-agent Discord bot with sensitive components:
- Password vault application (PyQt6 GUI for password management)
- Discord bot with Claude API integration
- Git management features
- Multi-model AI routing (Claude, local models)
- MCP (Model Context Protocol) bridge for agent communication
- Autonomous task execution system

Tech Stack:
- Python 3.11
- Libraries: discord.py, PyQt6, anthropic, sqlite3, aiohttp
- Files: 100+ Python files, 50+ config/docs
- Sensitive: API keys, Discord tokens, password encryption

Current Security Docs:
- SECURITY_ANALYSIS_REPORT.md (previous analysis)
- SECURITY_QUICK_REFERENCE.md (guidelines)

OBJECTIVE:
Perform comprehensive security audit and generate actionable remediation report.

REQUIREMENTS:

1. **Vulnerability Scan:**
   - SQL injection risks (password vault uses sqlite3)
   - Command injection (git management, shell commands)
   - XSS vulnerabilities (Discord message rendering)
   - Path traversal (file operations)
   - Insecure deserialization (JSON/pickle usage)
   - Race conditions (concurrent access to password DB)
   - SSRF (API calls, webhooks)
   - Hardcoded secrets (search for API keys, tokens, passwords)
   - Unsafe cryptography (password encryption methods)
   - Dependency vulnerabilities (run pip-audit or safety check)

2. **Authentication & Authorization:**
   - Discord bot user verification (who can use commands)
   - Password vault master password strength requirements
   - API key storage (are they encrypted or plaintext?)
   - File permission checks (sensitive files readable by all users?)

3. **Data Protection:**
   - Password encryption algorithm audit (password_vault_backend.py)
   - Database encryption at rest
   - API keys in environment variables vs hardcoded
   - Logging sensitive data (passwords, tokens in logs?)
   - Memory handling (secrets cleared after use?)

4. **Code Analysis:**
   Scan these high-risk files:
   - password_vault_app.py
   - password_vault_backend.py
   - BotFILES/phigen_discord_bot.py
   - BotFILES/jc_autonomous_worker.py
   - All files with "api", "token", "key", "password" in name
   - Any use of eval(), exec(), os.system(), subprocess without sanitization

5. **Attack Surface:**
   - Discord bot command injection vectors
   - File upload/download vulnerabilities
   - Webhook endpoint security (if any)
   - MCP bridge message validation
   - Task queue manipulation risks

6. **Compliance:**
   - OWASP Top 10 (2021) checklist
   - CWE Top 25 Most Dangerous Software Weaknesses
   - Python-specific security anti-patterns

SUCCESS CRITERIA:
- Comprehensive report in Markdown format
- Severity ratings: CRITICAL / HIGH / MEDIUM / LOW
- Each finding includes:
  - Vulnerability description
  - Affected files and line numbers (file.py:123)
  - Exploit scenario (how attacker could abuse it)
  - Code example showing the issue
  - Remediation code (exactly how to fix it)
  - CVSS score (if applicable)

- Prioritized remediation roadmap
- Quick wins (< 30 min fixes) vs long-term hardening
- Estimate hours to fix each category

DELIVERABLES:
1. SECURITY_AUDIT_2025-11-08.md
   - Executive summary (high-level findings)
   - Detailed findings (one section per vulnerability)
   - Remediation plan (prioritized by severity)
   - Code examples for all fixes

2. QUICK_FIXES.md
   - List of < 30 minute fixes with exact commands/code
   - Can be implemented immediately

3. SECURE_CODING_CHECKLIST.md
   - Prevention guidelines for future development
   - Pre-commit hook suggestions
   - Code review checklist

4. If found: CRITICAL_SECRETS_EXPOSED.txt
   - List any hardcoded API keys, tokens, passwords
   - STOP immediately and report this file first

CONSTRAINTS:
- READ ONLY analysis (do not modify code)
- Do not test exploits on live systems
- Do not exfiltrate any secrets found
- If you find critical secrets (API keys, passwords), report file path only (not the secret itself)
- Use static analysis only (bandit, semgrep, manual code review)
- No network scanning or active exploitation

TOOLS TO USE:
- bandit (Python security linter)
- pip-audit or safety (dependency vulnerabilities)
- Manual code review (grep for dangerous patterns)
- OWASP guidelines as reference

BEFORE STARTING:
1. Read SECURITY_ANALYSIS_REPORT.md (previous findings)
2. Install analysis tools: pip install bandit pip-audit
3. Run: bandit -r . -f json -o bandit_report.json
4. Run: pip-audit --format json > dependencies_audit.json
5. Then perform manual analysis

OUTPUT FORMAT:
```markdown
# PhiGEN Security Audit Report
**Date:** 2025-11-08
**Auditor:** SuperNinja Agent
**Codebase:** PhiGEN v1.0 (pre-agent-v1.0 tag)

## Executive Summary
[3-5 sentences on overall security posture]

Critical: X findings
High: Y findings
Medium: Z findings
Low: W findings

## Critical Findings

### [C-1] SQL Injection in Password Vault
**Severity:** CRITICAL
**CVSS:** 9.8
**File:** password_vault_backend.py:145
**Description:** User input directly concatenated into SQL query...
**Exploit Scenario:** Attacker can...
**Affected Code:**
```python
# VULNERABLE CODE
query = f"SELECT * FROM passwords WHERE name = '{user_input}'"
cursor.execute(query)
```
**Remediation:**
```python
# SECURE CODE
query = "SELECT * FROM passwords WHERE name = ?"
cursor.execute(query, (user_input,))
```
**Effort:** 15 minutes
**Priority:** Fix immediately before any deployment
```

TIME ESTIMATE: 4-6 hours
```

---

## TASK #11: PhiGEN Project Restructure (HIGH PRIORITY)

**Estimated Time:** 3-4 hours
**Value:** ⭐⭐⭐⭐⭐ (Enables all future development)

**WARNING:** This is a MAJOR refactor. Review the Pull Request very carefully before merging.

```
=== TASK: Execute PhiGEN Folder Restructure ===

GIT SAFETY PROTOCOL:
1. Clone from: https://github.com/Stryk91/PhiGEN.git
2. Create branch: git checkout -b agent-restructure
3. Work only in this branch
4. Commit after EACH phase (10 commits total)
5. Push branch when complete (DO NOT merge to main)
6. Create Pull Request for my review

⚠️ CRITICAL: Use 'git mv' for ALL file moves (preserves history)
⚠️ Test imports after EVERY phase
⚠️ If ANY phase fails, STOP and report

CONTEXT:
PhiGEN is a 100+ file Python project currently in chaos:
- 100+ files dumped in root directory
- No src/ directory structure
- Tests scattered across project
- 50+ markdown docs in root
- Multiple versions of same file (file_v2.py pattern)
- Temporary files (TEMPSVG/) committed

Complete restructure plan available in:
RESTRUCTURE_REPORT.md

OBJECTIVE:
Reorganize PhiGEN from chaotic root into clean standard Python project structure.

TARGET STRUCTURE:
```
PhiGEN/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── pyproject.toml
├── src/
│   ├── phigen/              (main bot package)
│   ├── password_vault/      (password vault app)
│   ├── ai_tools/            (AI integrations)
│   └── utils/               (shared utilities)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── windows/             (.bat files)
│   ├── linux/               (.sh files)
│   └── utils/               (helper scripts)
├── docs/
│   ├── guides/              (user guides)
│   ├── development/         (dev docs)
│   ├── architecture/        (design docs)
│   └── api/                 (API reference)
├── config/
│   ├── .env.example
│   └── docker/
├── assets/
│   └── fonts/
└── .claude/                 (Claude Code config)
```

REQUIREMENTS:

**PHASE 1: Preparation (DO NOT SKIP)**
```bash
# Verify safety tag exists
git tag -l pre-agent-v1.0  # Should show tag

# Create new branch
git checkout -b agent-restructure

# Create all target directories
mkdir -p src/phigen src/password_vault src/ai_tools src/utils
mkdir -p tests/unit tests/integration tests/fixtures
mkdir -p scripts/windows scripts/linux scripts/utils
mkdir -p docs/guides docs/development docs/architecture docs/api
mkdir -p config/docker
mkdir -p assets/fonts

# Commit directory structure
git add .
git commit -m "Phase 1: Create target directory structure"
```

**PHASE 2: Move Password Vault Application**
```bash
# Move password vault files to src/password_vault/
git mv password_vault_app.py src/password_vault/app.py
git mv password_vault_backend.py src/password_vault/backend.py
git mv validators.py src/password_vault/validators.py
git mv ui/ src/password_vault/ui/

# Create __init__.py
echo "# Password Vault Application" > src/password_vault/__init__.py

# Commit
git add .
git commit -m "Phase 2: Move password vault application to src/"

# TEST: Verify imports work
python -c "from src.password_vault.backend import *; print('✅ Imports OK')"
# If this fails, STOP and report error
```

**PHASE 3: Move Bot Files**
```bash
# Move existing phigen/ to src/phigen/
git mv phigen/* src/phigen/ 2>/dev/null || true
rmdir phigen 2>/dev/null || true

# Move bot files from BotFILES/ to src/phigen/bots/
mkdir -p src/phigen/bots
git mv BotFILES/phigen_discord_bot.py src/phigen/bots/discord_bot.py
git mv BotFILES/jc_autonomous_worker.py src/phigen/bots/autonomous_worker.py
git mv BotFILES/claude_discord_bot.py src/phigen/bots/claude_bot.py
git mv BotFILES/discord_mcp_bridge.py src/phigen/bots/mcp_bridge.py

# Move remaining BotFILES/ utilities
git mv BotFILES/*.py src/phigen/bots/ 2>/dev/null || true
git mv BotFILES/*.txt src/phigen/bots/ 2>/dev/null || true

# Move .bat launcher scripts to scripts/
git mv BotFILES/*.bat scripts/windows/ 2>/dev/null || true

# Commit
git commit -m "Phase 3: Move bot files to src/phigen/"

# TEST
python -c "from src.phigen.bots import discord_bot; print('✅ Bot imports OK')"
```

**PHASE 4: Move AI Tools**
```bash
# ai_tools/ already well-organized, just move it
git mv ai_tools src/ai_tools

# Commit
git commit -m "Phase 4: Move ai_tools to src/"

# TEST
python -c "from src.ai_tools import *; print('✅ AI tools imports OK')"
```

**PHASE 5: Move Tests**
```bash
# Move test files to tests/unit/
git mv test_*.py tests/unit/ 2>/dev/null || true
git mv BotFILES/test_*.py tests/unit/ 2>/dev/null || true

# Create conftest.py
cat > tests/conftest.py << 'EOF'
import sys
from pathlib import Path

# Add src/ to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))
EOF

# Commit
git commit -m "Phase 5: Consolidate tests in tests/"

# TEST
pytest tests/unit/ -v --collect-only  # Just list tests, don't run
```

**PHASE 6: Move Documentation**
```bash
# Move markdown files to docs/
git mv SECURITY_*.md docs/development/
git mv SETUP_*.md docs/guides/
git mv *_GUIDE.md docs/guides/
git mv RESTRUCTURE_REPORT.md docs/development/
git mv *_COMPLETE.md docs/development/
git mv SESSION_SUMMARY.md docs/development/

# Keep these in root:
# - README.md
# - LICENSE (if exists)
# - GIT_BRANCHING_GUIDE.md
# - AGENT_TASK_PROMPTS.md

# Move TBI_features to docs/
git mv TBI_features docs/development/tbi_features

# Commit
git commit -m "Phase 6: Organize documentation in docs/"
```

**PHASE 7: Move Scripts**
```bash
# Move .bat files to scripts/windows/
git mv *.bat scripts/windows/ 2>/dev/null || true

# Move .sh files to scripts/linux/
git mv *.sh scripts/linux/ 2>/dev/null || true

# Move .ps1 files to scripts/windows/
git mv *.ps1 scripts/windows/ 2>/dev/null || true

# Move standalone Python scripts
git mv convert_svg*.py scripts/utils/
git mv svg_to_png*.py scripts/utils/
git mv *_title*.py scripts/utils/
git mv preview_fonts.py scripts/utils/
git mv dc_log_message.py scripts/utils/
git mv jc_read_feed.py scripts/utils/
git mv watch_and_send_to_dc.py scripts/utils/

# Commit
git commit -m "Phase 7: Move scripts to scripts/"
```

**PHASE 8: Move Assets & Config**
```bash
# Move fonts
git mv FONTS/ assets/fonts/ 2>/dev/null || true

# Move images
git mv *.png assets/ 2>/dev/null || true
git mv *.svg assets/ 2>/dev/null || true

# Archive TEMPSVG (123 temporary files)
mkdir -p archive/
git mv TEMPSVG/ archive/TEMPSVG_2025-11-08/ 2>/dev/null || true

# Move Docker files to config/
git mv Dockerfile config/docker/
git mv docker-compose.yml config/docker/

# Commit
git commit -m "Phase 8: Organize assets and config"
```

**PHASE 9: Update Import Statements (CRITICAL)**
```bash
# Update all imports across codebase
# This is the most error-prone step

# Find all Python files and update imports
find src/ tests/ scripts/ -name "*.py" -type f -exec sed -i \
  -e 's/from password_vault_backend/from src.password_vault.backend/g' \
  -e 's/from password_vault_app/from src.password_vault.app/g' \
  -e 's/from phigen\./from src.phigen./g' \
  -e 's/from ai_tools/from src.ai_tools/g' \
  -e 's/import password_vault_backend/from src.password_vault import backend/g' \
  {} +

# Update script shebangs and paths
find scripts/ -name "*.bat" -type f -exec sed -i \
  's|python password_vault_app.py|python src/password_vault/app.py|g' {} +

# Commit
git commit -am "Phase 9: Update import statements"

# TEST (CRITICAL - MUST PASS)
python -m pytest tests/ --collect-only
python -c "from src.password_vault.app import *"
python -c "from src.phigen.bots.discord_bot import *"
python -c "from src.ai_tools import *"

# If ANY import fails, STOP and report error
```

**PHASE 10: Cleanup & Documentation**
```bash
# Update README.md with new structure
cat > PROJECT_STRUCTURE.md << 'EOF'
# PhiGEN Project Structure

## Directory Layout
- `src/` - All source code
  - `phigen/` - Main bot package
  - `password_vault/` - Password vault application
  - `ai_tools/` - AI integrations
- `tests/` - All tests
- `scripts/` - Standalone scripts
- `docs/` - All documentation
- `config/` - Configuration files
- `assets/` - Static assets

## Running the Project
- Password Vault: `python src/password_vault/app.py`
- Discord Bot: `python src/phigen/bots/discord_bot.py`
- Tests: `pytest tests/`

## Development
See docs/development/ for development guides.
EOF

git add PROJECT_STRUCTURE.md
git commit -m "Phase 10: Add project structure documentation"

# Update .gitignore
cat >> .gitignore << 'EOF'

# Build artifacts
src/**/__pycache__/
*.pyc
*.pyo
*.egg-info/

# Test artifacts
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.venv/
venv/

# IDE
.vscode/
.idea/

# Temporary files
*.tmp
*.log
EOF

git add .gitignore
git commit -m "Phase 10: Update .gitignore for new structure"

# Final commit
git commit --allow-empty -m "Phase 10 Complete: PhiGEN restructure finished

- 100+ files in root → 8 files in root
- All source code in src/
- All tests in tests/
- All docs in docs/
- All scripts in scripts/
- Import statements updated
- Tests verified passing
"
```

SUCCESS CRITERIA:
- ✅ Root directory has < 15 files
- ✅ No .py files in root (except setup.py if needed)
- ✅ All imports work (python -c "from src.MODULE import *")
- ✅ All tests collect without errors (pytest --collect-only)
- ✅ 10 commits (one per phase)
- ✅ Branch pushed to remote
- ✅ No files lost (git log --stat shows all moves)

CONSTRAINTS:
- Use `git mv` for ALL file moves (not mv or move)
- Commit after each phase (granular history)
- Test imports after phases 2, 3, 4, 9 (critical phases)
- If any phase fails, STOP immediately and report error
- Do not delete any files (move to archive/ if unsure)
- Preserve file history (git log --follow FILE should work)

DELIVERABLES:
1. Restructured codebase on branch `agent-restructure`
2. RESTRUCTURE_COMPLETE.md
   - Summary of changes
   - File count before/after
   - Any issues encountered
   - Testing results
   - Instructions for merging branch

BEFORE STARTING:
1. Verify pre-agent-v1.0 tag exists
2. Create agent-restructure branch
3. Read RESTRUCTURE_REPORT.md completely
4. Understand the target structure

AFTER COMPLETION:
1. Push branch: git push origin agent-restructure
2. Create Pull Request (title: "[Agent] PhiGEN Restructure - Review Before Merge")
3. Generate diff summary: git diff main..agent-restructure --stat > restructure_diff.txt
4. Report back with PR link and any issues

TIME ESTIMATE: 3-4 hours

⚠️ CRITICAL REMINDERS:
- This is a MAJOR refactor. Do not rush.
- Test imports after EVERY critical phase
- If stuck, report progress and ask for guidance
- I will review PR before merging (do NOT auto-merge)
```

---

## TASK #3: Implement Feature #20 - Sentiment Analysis (MEDIUM PRIORITY)

**Estimated Time:** 8-10 hours
**Value:** ⭐⭐⭐⭐ (Complex feature, saves significant time)

```
=== TASK: Implement Sentiment Analysis Feature ===

GIT SAFETY PROTOCOL:
1. Clone from: https://github.com/Stryk91/PhiGEN.git
2. Create branch: git checkout -b agent-feature-sentiment-analysis
3. Work only in this branch
4. Commit frequently with descriptive messages
5. Push branch when complete (DO NOT merge to main)
6. Create Pull Request for my review

CONTEXT:
PhiGEN is a multi-agent Discord bot that helps users with development tasks.
Feature request: Detect user frustration/satisfaction and adjust bot responses accordingly.

Full specification: TBI_features/FEATURE_20_Sentiment_Analysis.md

Tech Stack:
- Python 3.11
- Discord.py bot framework
- SQLite for data persistence
- transformers library (HuggingFace) for sentiment models

OBJECTIVE:
Implement sentiment analysis feature to improve user experience by detecting emotions and adapting bot behavior.

REQUIREMENTS:

1. **Core Components:**

   a. **sentiment_analyzer.py** (350 lines)
   - Use transformers library (distilbert-base-uncased-finetuned-sst-2-english)
   - Classify messages: POSITIVE / NEUTRAL / NEGATIVE
   - Return sentiment score (-1.0 to 1.0)
   - Handle errors gracefully (API failures, model loading issues)

   b. **emotion_classifier.py** (200 lines)
   - Detect specific emotions: frustration, confusion, satisfaction, excitement
   - Use rule-based heuristics + ML model
   - Return emotion probabilities dictionary

   c. **response_adapter.py** (150 lines)
   - Adjust bot response style based on sentiment
   - Frustrated user → concise, direct answers
   - Confused user → detailed explanations, examples
   - Happy user → celebrate, suggest advanced features

   d. **sentiment_tracker.py** (200 lines)
   - Store sentiment history in SQLite
   - Track trends over time
   - Generate insights (most frustrated times, triggers)

2. **Database Schema:**
```sql
CREATE TABLE IF NOT EXISTS sentiment_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    sentiment TEXT NOT NULL,  -- POSITIVE, NEUTRAL, NEGATIVE
    sentiment_score REAL NOT NULL,  -- -1.0 to 1.0
    emotions TEXT,  -- JSON: {"frustration": 0.65, "confusion": 0.30}
    context TEXT  -- What user was working on
);

CREATE TABLE IF NOT EXISTS sentiment_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    condition TEXT NOT NULL,  -- "frustration > 70%"
    action TEXT NOT NULL,  -- "suggest_break"
    enabled BOOLEAN DEFAULT 1
);

CREATE INDEX idx_user_timestamp ON sentiment_log(user_id, timestamp);
```

3. **Discord Bot Commands:**

   ```python
   !sentiment analyze
   # Analyze current user's mood from recent messages
   # Output: Sentiment score, detected emotions, bot adjustment plan

   !sentiment history
   # Show user's sentiment over time (today, this week)
   # Output: Timeline, trends, frustration triggers

   !sentiment team
   # Show team sentiment overview (all users)
   # Output: Team mood, who needs help, common frustration points

   !sentiment alerts on/off
   # Enable/disable frustration alerts
   # Output: Confirmation, alert thresholds

   !sentiment report
   # Generate detailed sentiment report (PDF or Markdown)
   # Output: File attachment with analysis
   ```

4. **Bot Integration:**
   - Hook into message handler (every message analyzed)
   - Non-blocking (async analysis, don't slow bot)
   - Adjust responses in real-time based on sentiment
   - Alert user if frustration > 70% for 30+ minutes

5. **Testing Requirements:**
   - Unit tests for sentiment classifier (test positive/negative/neutral messages)
   - Integration tests for database operations
   - Mock Discord message handling
   - Test edge cases: empty messages, very long messages, emojis, sarcasm
   - Achieve 90%+ code coverage

SUCCESS CRITERIA:
- ✅ All 5 commands work (!sentiment analyze/history/team/alerts/report)
- ✅ Sentiment correctly detected (test with sample messages)
- ✅ Database stores sentiment history
- ✅ Bot responses adapt to user mood (verify with examples)
- ✅ All tests pass (pytest)
- ✅ No performance degradation (sentiment analysis < 200ms)
- ✅ Documentation updated (README, API docs)

CONSTRAINTS:
- Use existing PhiGEN code patterns (see BotFILES/phigen_discord_bot.py)
- Follow PEP 8 style guide
- Add type hints to all functions
- Use async/await for non-blocking operations
- Max 500 lines per file (split if needed)
- Document all public functions with docstrings
- Use logging (not print statements)
- Handle errors gracefully (never crash bot)

FILE STRUCTURE:
```
PhiGEN/
├── sentiment/
│   ├── __init__.py
│   ├── analyzer.py         (SentimentAnalyzer class)
│   ├── emotion.py          (EmotionClassifier class)
│   ├── adapter.py          (ResponseAdapter class)
│   ├── tracker.py          (SentimentTracker class)
│   └── commands.py         (Discord command handlers)
└── BotFILES/
    └── phigen_discord_bot.py      (integrate sentiment here)

tests/
└── sentiment/
    ├── test_analyzer.py
    ├── test_emotion.py
    ├── test_adapter.py
    ├── test_tracker.py
    └── test_commands.py
```

DELIVERABLES:
1. All source files in sentiment/
2. All test files in tests/sentiment/
3. Updated requirements.txt
4. Updated README.md
5. SENTIMENT_ANALYSIS_COMPLETE.md (implementation summary)
6. All tests passing (pytest output)

BEFORE STARTING:
1. Read TBI_features/FEATURE_20_Sentiment_Analysis.md completely
2. Understand existing bot architecture (BotFILES/phigen_discord_bot.py)
3. Verify transformers library works: python -c "from transformers import pipeline; print('OK')"
4. Check database schema compatibility

TESTING CHECKLIST:
- [ ] Test with positive message: "This is amazing, thank you!"
- [ ] Test with negative message: "This doesn't work and I'm stuck"
- [ ] Test with neutral message: "What is the weather?"
- [ ] Test sentiment history query
- [ ] Test team sentiment aggregation
- [ ] Test alert triggering (frustration > 70%)
- [ ] Test response adaptation (frustrated user gets concise answers)
- [ ] Test database persistence
- [ ] Test error handling (invalid input, model failure)
- [ ] Test performance (analysis < 200ms per message)

TIME ESTIMATE: 8-10 hours
```

---

## TASK #15: Technology Research - Encryption Libraries (MEDIUM PRIORITY)

**Estimated Time:** 4-5 hours
**Value:** ⭐⭐⭐⭐ (Informs security improvements)

```
=== TASK: Research Best Encryption Library for PhiGEN Password Vault ===

GIT SAFETY PROTOCOL:
1. Clone from: https://github.com/Stryk91/PhiGEN.git
2. Create branch: git checkout -b agent-research-encryption
3. Work in this branch (analysis only, no code changes)
4. Push branch when complete
5. Create Pull Request with research report

CONTEXT:
PhiGEN has a password vault application (PyQt6 GUI) that stores user passwords.
Currently uses: [UNKNOWN - need to identify current encryption method]

Files:
- password_vault_app.py
- password_vault_backend.py

Current security status:
- SECURITY_ANALYSIS_REPORT.md (previous security audit)
- May have vulnerabilities in encryption implementation

OBJECTIVE:
Research and recommend the best Python encryption library for secure password storage.

REQUIREMENTS:

1. **Analyze Current Implementation:**
   - Read password_vault_backend.py
   - Identify current encryption method (cryptography, PyCrypto, hashlib, etc.)
   - Document current approach (algorithm, key derivation, storage format)
   - Identify weaknesses (outdated algorithms, weak key derivation, no salt, etc.)

2. **Evaluate Alternatives:**

   Compare these libraries:

   **a. cryptography** (https://cryptography.io/)
   - Security: FIPS 140-2 certified primitives
   - Algorithms: Fernet (symmetric), AES-256-GCM, ChaCha20-Poly1305
   - Key derivation: PBKDF2, Argon2
   - Maintenance: Actively maintained by PyCA
   - Community: 10K+ stars, 1M+ downloads/month
   - CVEs: Check https://nvd.nist.gov/
   - Performance: Benchmark encryption/decryption speed

   **b. PyNaCl** (https://pynacl.readthedocs.io/)
   - Security: Based on libsodium (NaCl crypto library)
   - Algorithms: XSalsa20-Poly1305, Argon2
   - Key derivation: Argon2id (best-in-class)
   - Maintenance: Actively maintained
   - Community: 1K+ stars
   - CVEs: Check for vulnerabilities
   - Performance: Generally faster than cryptography

   **c. PyCryptodome** (https://www.pycryptodome.org/)
   - Security: Drop-in replacement for PyCrypto (which is deprecated)
   - Algorithms: AES-256, RSA, ChaCha20
   - Key derivation: PBKDF2, scrypt
   - Maintenance: Actively maintained
   - Community: 2K+ stars
   - CVEs: Check for vulnerabilities
   - Performance: Mid-range

3. **Security Analysis:**

   For each library, evaluate:

   **Security Audit:**
   - Has it been audited? (link to audit reports)
   - Any recent CVEs? (check NVD, GitHub Security Advisories)
   - FIPS 140-2 compliance?
   - Algorithm security (AES-256 vs ChaCha20 vs Salsa20)

   **Key Derivation:**
   - What KDF algorithms supported? (PBKDF2, Argon2, scrypt)
   - Default iteration count / memory cost
   - Resistance to brute-force attacks
   - Argon2 support (recommended by OWASP)

   **Implementation Safety:**
   - Side-channel attack resistance
   - Memory safety (no sensitive data leaks)
   - API simplicity (hard to misuse?)
   - Secure defaults (good algorithms enabled by default)

4. **Performance Benchmarks:**

   Write benchmark script:
   ```python
   import time
   from cryptography.fernet import Fernet
   import nacl.secret
   from Crypto.Cipher import AES

   # Benchmark encryption/decryption for each library
   # Test: Encrypt 1000 passwords (avg 20 chars each)
   # Measure: Time to encrypt, time to decrypt
   # Output: ops/second for each library
   ```

   Report results:
   - Encryption speed (passwords/second)
   - Decryption speed (passwords/second)
   - Memory usage
   - Startup time (library import + key derivation)

5. **Integration Difficulty:**

   For each library, assess:
   - Ease of integration with existing PhiGEN code
   - Migration path from current implementation
   - Breaking changes (will existing passwords need re-encryption?)
   - API compatibility with PyQt6 application
   - Cross-platform support (Windows, Linux, macOS)

6. **Recommendation:**

   Provide final recommendation with:
   - **Winner:** [Library name]
   - **Justification:** Why this library is best for PhiGEN
   - **Algorithm:** Recommended encryption algorithm (e.g., Fernet, AES-256-GCM)
   - **KDF:** Recommended key derivation (e.g., Argon2id, PBKDF2)
   - **Migration Plan:** How to migrate from current implementation
   - **Code Example:** Drop-in replacement code

SUCCESS CRITERIA:
- Comprehensive comparison table (security, performance, ease of use)
- Security audit findings for each library
- Performance benchmark results (with code)
- Clear recommendation with justification
- Migration code examples
- Risk assessment for migration

CONSTRAINTS:
- READ ONLY (no code changes to password vault yet)
- Focus on Python 3.11+ compatibility
- Must work on Windows (PhiGEN's primary platform)
- No external dependencies beyond the crypto library
- Must support password storage (not just transport encryption)

DELIVERABLES:

1. **ENCRYPTION_RESEARCH_REPORT.md**
   - Executive summary (recommendation)
   - Current implementation analysis
   - Library comparison table
   - Detailed analysis of each library
   - Performance benchmarks
   - Security audit findings
   - Final recommendation
   - Migration plan
   - Code examples

2. **benchmark_encryption.py** (benchmark script with results)

3. **migration_guide.md** (step-by-step migration instructions)

4. **secure_password_vault.py** (example implementation with recommended library)

RESEARCH CHECKLIST:
- [ ] Identify current encryption method in password_vault_backend.py
- [ ] Check CVE databases for each library
- [ ] Find security audit reports (if available)
- [ ] Run performance benchmarks (encryption/decryption speed)
- [ ] Test each library with sample password encryption
- [ ] Compare API ease of use
- [ ] Assess migration complexity
- [ ] Review OWASP password storage guidelines
- [ ] Check Python 3.11 compatibility for all libraries
- [ ] Verify Windows support (important for PhiGEN)

USEFUL RESOURCES:
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- NVD (CVE database): https://nvd.nist.gov/
- Python Cryptographic Authority: https://cryptography.io/
- libsodium documentation: https://doc.libsodium.org/
- Argon2 RFC: https://datatracker.ietf.org/doc/html/rfc9106

TIME ESTIMATE: 4-5 hours
```

---

## Summary: Task Priorities

| Task | Priority | Time | Value | Do First If... |
|------|----------|------|-------|----------------|
| **#1: Security Audit** | CRITICAL | 4-6h | ⭐⭐⭐⭐⭐ | You're deploying soon or handle sensitive data |
| **#11: Restructure** | HIGH | 3-4h | ⭐⭐⭐⭐⭐ | You're frustrated with file organization |
| **#3: Sentiment** | MEDIUM | 8-10h | ⭐⭐⭐⭐ | You want a cool new feature |
| **#15: Encryption Research** | MEDIUM | 4-5h | ⭐⭐⭐⭐ | You want to improve password vault security |

**Recommended Order:**
1. Security Audit (critical vulnerabilities first)
2. Project Restructure (enables easier future development)
3. Encryption Research (informs security fixes)
4. Sentiment Analysis (new feature implementation)

---

## Important Notes

### Before Using Any Prompt:
1. ✅ Complete Git setup (GIT_BRANCHING_GUIDE.md)
2. ✅ Push to GitHub with safety tag
3. ✅ Verify remote: `git remote -v` shows https://github.com/Stryk91/PhiGEN.git

### After Agent Completes:
1. Review Pull Request on GitHub
2. Test the changes locally before merging
3. Merge if good, close if bad
4. Delete agent branch after merging

### If Agent Fails:
1. Check error message in PR
2. Close PR and delete branch
3. Your main branch is still safe
4. Try again with clarified prompt

---

**Created:** 2025-11-08
**Status:** Ready to use
**Repository:** https://github.com/Stryk91/PhiGEN
