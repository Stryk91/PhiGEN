# PhiGEN Project - Folder Restructure Report

**Generated:** 2025-11-08
**Analyst:** Claude Code
**For:** JC (Implementation)
**Status:** Analysis Only - No Changes Made

---

## Executive Summary

PhiGEN project has **100+ files in root directory** causing navigation and maintenance issues. The codebase is functional but severely disorganized. Major restructure recommended to improve:
- Developer productivity (easier to find files)
- Onboarding speed (clear structure)
- Maintainability (logical grouping)
- Build processes (standardized locations)

**Critical Issues:**
1. Root directory pollution (100+ files)
2. No src/ directory for source code
3. Scattered related files across multiple locations
4. Temporary/generated files committed to repo
5. Multiple versions of same file (should use git)

---

## Current State Assessment

### Severity: HIGH

**Files in Root:** 100+
**Scattered Test Files:** 10+
**Documentation Files in Root:** 50+
**Duplicate/Version Files:** 15+

**Impact:**
- Hard to find specific files
- Unclear project entry points
- Difficult for new developers
- Risk of accidentally editing wrong version
- Build scripts unclear

---

## Current Structure Overview

```
PhiGEN/
├── 100+ files in root (❌ MAJOR PROBLEM)
├── ai_tools/ (✅ WELL ORGANIZED)
├── BotFILES/ (⚠️ FUNCTIONAL BUT MESSY)
├── TEMPSVG/ (❌ 123 FILES, SHOULD BE ARCHIVED)
├── FONTS/ (⚠️ OK BUT INCONSISTENT)
├── phigen/ (✅ MINIMAL, CLEAN)
├── docs/ (⚠️ ONLY 7 FILES, 50+ MORE IN ROOT)
├── ui/ (✅ APPROPRIATE)
└── TBI_features/ (✅ WELL ORGANIZED)
```

### Best Organized Folder
**ai_tools/** - Excellent example of proper module organization
- Clear purpose
- Self-contained
- Logical file grouping
- Proper __init__.py
- Tests with code
- Own requirements.txt

### Worst Organized Area
**Root Directory** - Complete chaos
- 100+ files with no organization
- Mixes code, docs, configs, assets, tests, scripts
- Impossible to navigate
- No clear entry points

---

## Problem Categories

### 1. ROOT DIRECTORY POLLUTION (Critical)

**Current State:** 100+ files dumped in root

**Problem Files:**

**Python Source (15+ files):**
```
password_vault_app.py
password_vault_backend.py
run_qt_ui.py, run_qt_ui_IMPROVED.py, run_qt_ui_LAYOUTS.py
validators.py
convert_svg.py, convert_svg_transparent.py
svg_to_png.py, svg_to_png_clean.py
setup_qt.py, qt_config.py
preview_fonts.py
test_agent_feed.py
jc_read_feed.py
dc_log_message.py
watch_and_send_to_dc.py
... and more
```

**Documentation (50+ .md files):**
```
README.md
ARCHITECTURE.md
API_DOCUMENTATION.md
AGENT_GUIDELINES.md
COLLABORATION_GUIDE.md
DEPLOYMENT_GUIDE.md
DOCKER_GUIDE.md
... 40+ more markdown files
```

**Scripts (15+ files):**
```
*.bat (9 files)
*.ps1 (3 files)
*.sh (3 files)
```

**Test Files:**
```
test.txt, test2.txt, test3.txt, test4.txt
test_password_validation.py
dc_message_trigger.txt
```

**Data/Logs:**
```
2025-11-08-00-34am-first-kali-session.txt
*.log files
```

**Impact:**
- Takes 30+ seconds to find specific file
- Risk of editing wrong version
- Unclear what's production vs experimental
- Makes git status output unreadable

---

### 2. SCATTERED RELATED FILES (Critical)

**Password Vault Application:**
- Root: `password_vault_app.py`, `password_vault_backend.py`
- Root: `run_qt_ui.py` (+ 2 improved versions)
- Root: `validators.py`
- TEMPSVG: `password_vault_complete.py`, `password_vault_complete_IMPROVED.py`
- ui/: `password_vault.ui` (+ 2 improved versions)

**Result:** One feature spread across 3 directories, 8+ files

**SVG/Graphics Utilities (12+ files):**
- Root: 8 SVG utility scripts
- TEMPSVG: 29 generation scripts
- TEMPSVG: 40+ source SVGs
- TEMPSVG: 83+ generated PNGs

**Result:** Graphics pipeline impossible to understand

**Discord Bots:**
- BotFILES: 6 different bot implementations
- ai_tools: 2 more bot implementations

**Result:** Unclear which bot is production

**Test Files:**
- Root: test_password_validation.py
- ai_tools: test_ai_integration.py, test_multimodel.py
- BotFILES: test_*.py (6 files)

**Result:** No centralized test runner

---

### 3. TEMPSVG FOLDER (High Priority)

**Current State:** 123 files, 29 Python scripts

**Contents:**
- 29 Python generation scripts (one-off utilities)
- 40+ SVG source files
- 83+ PNG rendered files
- 1.4MB buttons_rc.py (compiled Qt resources)
- 2 password vault implementations (wrong location!)

**Problems:**
- Name says "TEMP" but committed to repo
- Mix of source, generated, and production files
- Should be archived or properly organized
- Generated files shouldn't be in repo
- Password vault apps in wrong location

**Impact:**
- 30% of project files are in this mess
- Unclear what's source vs generated
- Massive git history from binary PNGs

---

### 4. MULTIPLE FILE VERSIONS (Medium Priority)

**Instead of using git for versions:**

```
password_vault_app.py
password_vault_complete.py
password_vault_complete_IMPROVED.py

run_qt_ui.py
run_qt_ui_IMPROVED.py
run_qt_ui_LAYOUTS.py

password_vault.ui
password_vault_IMPROVED.ui
password_vault_LAYOUTS.ui

convert_svg.py
convert_svg_transparent.py

svg_to_png.py
svg_to_png_clean.py
```

**Problem:** Unclear which is production, which is experimental
**Solution:** Use git branches or archive old versions

---

### 5. BUILD ARTIFACTS COMMITTED (Medium Priority)

```
__pycache__/ (in root - should be gitignored)
__pycache__/ (in multiple folders)
buttons_rc.py (1.4MB compiled Qt resources)
Generated PNG files (80+ files)
*.pyc files
```

**Impact:**
- Bloated git history
- Merge conflicts on generated files
- Slower clone times

---

### 6. NO STANDARD STRUCTURE (High Priority)

**Missing:**
- ❌ No `src/` directory (source code scattered)
- ❌ No `tests/` directory (tests everywhere)
- ❌ No `scripts/` directory (utilities in root)
- ❌ No `assets/` directory (images scattered)
- ❌ No `config/` directory (configs in root)
- ❌ No `data/` directory (logs/feeds in various places)

**Impact:**
- Non-standard project layout
- Hard for new devs to understand
- Build tools can't find files predictably
- CI/CD scripts fragile

---

## Proposed Structure

### Clean, Standard Python Project Layout

```
PhiGEN/
├── .github/                          # CI/CD workflows
│   └── workflows/
│
├── src/                              # ALL SOURCE CODE
│   ├── phigen/                      # Core package
│   │   ├── __init__.py
│   │   ├── agent_feed.py
│   │   └── detect_agent.py
│   │
│   ├── password_vault/              # Password vault application
│   │   ├── __init__.py
│   │   ├── app.py                   # From: password_vault_app.py
│   │   ├── backend.py               # From: password_vault_backend.py
│   │   ├── validators.py            # From: validators.py
│   │   ├── runners/
│   │   │   ├── main.py             # From: run_qt_ui.py (production version)
│   │   │   └── layouts.py          # From: run_qt_ui_LAYOUTS.py (if needed)
│   │   └── ui/
│   │       ├── main_window.ui       # From: ui/password_vault.ui (production)
│   │       └── resources/
│   │           └── buttons_rc.py    # From: TEMPSVG/buttons_rc.py
│   │
│   ├── ai_tools/                    # Move from root (already well organized)
│   │   ├── __init__.py
│   │   ├── api_server.py
│   │   ├── code_reviewer.py
│   │   ├── conversation_logger.py
│   │   ├── conversation_rag.py
│   │   ├── model_router.py
│   │   ├── ollama_client.py
│   │   └── ... (rest of ai_tools/)
│   │
│   ├── bots/                        # Discord bots (from BotFILES/)
│   │   ├── __init__.py
│   │   ├── discord_ai/
│   │   │   ├── single_model_bot.py # From: ai_tools/discord_ai_bot.py
│   │   │   └── multimodel_bot.py   # From: ai_tools/discord_multimodel_bot.py
│   │   ├── jc_bot/
│   │   │   ├── main.py             # From: BotFILES/jc_discord_bot.py
│   │   │   ├── autonomous_worker.py
│   │   │   └── feed_watcher.py
│   │   ├── claude_bot/
│   │   │   └── main.py             # From: BotFILES/claude_discord_bot.py
│   │   └── phigen_bot/
│   │       └── main.py             # From: BotFILES/phigen_discord_bot.py
│   │
│   ├── automation/                  # Task automation
│   │   ├── task_executor.py        # From: BotFILES/
│   │   ├── desktop_integration.py  # From: BotFILES/type_to_claude_desktop.py
│   │   └── monitors/
│   │       └── claude_code.py      # From: BotFILES/claude_code_monitor.py
│   │
│   ├── mcp/                         # MCP integration
│   │   ├── __init__.py
│   │   ├── bridge.py               # From: BotFILES/discord_mcp_bridge.py
│   │   └── enhanced_bot.py         # From: BotFILES/discord_bot_mcp_enhanced.py
│   │
│   └── utils/                       # Shared utilities
│       ├── qt_setup.py             # From: setup_qt.py
│       └── qt_config.py            # From: qt_config.py
│
├── scripts/                         # Standalone scripts (not imported)
│   ├── setup/
│   │   └── install_dependencies.sh
│   ├── graphics/                    # SVG/PNG utilities
│   │   ├── convert_svg.py          # From: root
│   │   ├── svg_to_png.py           # From: root (production version)
│   │   ├── crop_title.py
│   │   ├── optimize_title.py
│   │   └── ... (graphics utilities)
│   ├── development/
│   │   └── preview_fonts.py        # From: root
│   ├── agent_coordination/
│   │   ├── read_feed.py            # From: jc_read_feed.py
│   │   ├── log_message.py          # From: dc_log_message.py
│   │   └── watch_and_send.py       # From: watch_and_send_to_dc.py
│   ├── windows/                     # Windows-specific
│   │   ├── *.bat                   # From: root
│   │   └── *.ps1                   # From: root
│   └── linux/                       # Linux-specific
│       └── *.sh                    # From: root
│
├── tests/                           # ALL TESTS
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_password_validation.py  # From: root
│   │   ├── test_ai_integration.py       # From: ai_tools/
│   │   └── test_multimodel.py           # From: ai_tools/
│   ├── integration/
│   │   └── test_*.py                    # From: BotFILES/test_*.py
│   └── fixtures/
│       └── test_data.json
│
├── docs/                            # ALL DOCUMENTATION
│   ├── README.md                    # Project overview
│   ├── guides/
│   │   ├── QUICK_START.md          # From: QUICK_START_GUIDE.txt
│   │   ├── JC_QUICKSTART.md        # From: docs/
│   │   ├── DC_QUICKSTART.md        # From: docs/
│   │   ├── DEPLOYMENT_GUIDE.md     # From: root
│   │   └── DOCKER_GUIDE.md         # From: root
│   ├── api/
│   │   └── API_DOCUMENTATION.md    # From: root
│   ├── architecture/
│   │   ├── ARCHITECTURE.md         # From: root
│   │   ├── AGENT_COORDINATION.md   # From: docs/
│   │   └── ... (architecture docs)
│   ├── development/
│   │   ├── COLLABORATION_GUIDE.md  # From: root
│   │   ├── JC_GUIDELINES.md        # From: docs/
│   │   └── ... (50+ .md files from root)
│   └── features/
│       └── TBI_features/            # Move from root
│
├── assets/                          # Static assets
│   ├── fonts/                       # From: FONTS/
│   │   ├── bedstead/
│   │   ├── drafting-mono/
│   │   └── ... (organized fonts)
│   ├── images/
│   │   ├── icons/                  # From: scattered PNGs
│   │   └── ui/
│   │       └── buttons/            # From: TEMPSVG/buttons_*.png
│   └── svg/
│       └── sources/                # From: TEMPSVG/*.svg
│
├── design/                          # Design & generation (archive old TEMPSVG)
│   ├── svg_generation/
│   │   └── scripts/                # From: TEMPSVG/*.py (29 scripts)
│   ├── archived/
│   │   └── old_implementations/    # Old versions of password vault
│   └── README.md                   # Document what's here
│
├── data/                            # Runtime data (gitignored)
│   ├── logs/                       # *.log files
│   ├── feeds/
│   │   └── agent-feed.jsonl       # From: docs/agent-feed.jsonl
│   ├── temp/                       # Temporary files
│   └── passwords/                  # From: TMPPASSWORDS/
│       └── passwords.json
│
├── config/                          # Configuration files
│   ├── .env.example                # From: root
│   ├── docker/
│   │   ├── docker-compose.yml     # From: root
│   │   ├── Dockerfile             # From: root
│   │   └── .dockerignore          # From: root
│   ├── claude/
│   │   └── .claude/               # From: root .claude/
│   └── mcp/
│       └── .mcp.json              # From: root
│
├── .github/
│   └── workflows/
├── .venv/                          # Virtual environment (gitignored)
├── .gitignore                      # Enhanced
├── pyproject.toml                  # Modern Python config (NEW)
├── requirements.txt
├── Makefile                        # From: root
└── README.md                       # From: root (main project README)
```

---

## Migration Plan

### Phase 1: Preparation (No Code Changes)
**Duration:** 30 minutes

1. **Backup current state**
   ```bash
   git tag pre-restructure
   git push origin pre-restructure
   ```

2. **Create migration branch**
   ```bash
   git checkout -b restructure
   ```

3. **Update .gitignore**
   ```
   # Add
   __pycache__/
   *.pyc
   *.pyo
   .venv/
   data/logs/
   data/temp/
   data/passwords/
   *.log
   ```

### Phase 2: Create Directory Structure
**Duration:** 10 minutes

```bash
mkdir -p src/{phigen,password_vault/{runners,ui/resources},ai_tools,bots/{discord_ai,jc_bot,claude_bot,phigen_bot},automation/monitors,mcp,utils}
mkdir -p scripts/{setup,graphics,development,agent_coordination,windows,linux}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{guides,api,architecture,development,features}
mkdir -p assets/{fonts,images/{icons,ui/buttons},svg/sources}
mkdir -p design/{svg_generation/scripts,archived/old_implementations}
mkdir -p data/{logs,feeds,temp,passwords}
mkdir -p config/{docker,claude,mcp}
```

### Phase 3: Move Source Files
**Duration:** 1-2 hours

**Critical Order (to maintain working code):**

1. **Core package (phigen/)**
   ```bash
   git mv phigen/ src/phigen/
   ```

2. **AI Tools (already well organized)**
   ```bash
   git mv ai_tools/ src/ai_tools/
   ```

3. **Password Vault files**
   ```bash
   git mv password_vault_app.py src/password_vault/app.py
   git mv password_vault_backend.py src/password_vault/backend.py
   git mv validators.py src/password_vault/validators.py
   git mv run_qt_ui.py src/password_vault/runners/main.py
   git mv ui/*.ui src/password_vault/ui/
   git mv TEMPSVG/buttons_rc.py src/password_vault/ui/resources/
   ```

4. **Bot files from BotFILES/**
   ```bash
   git mv BotFILES/jc_discord_bot.py src/bots/jc_bot/main.py
   git mv BotFILES/jc_autonomous_worker.py src/bots/jc_bot/
   git mv BotFILES/jc_feed_watcher.py src/bots/jc_bot/
   # ... (continue for each bot)
   ```

5. **Documentation (50+ files)**
   ```bash
   git mv *.md docs/development/
   # Keep only README.md in root
   git mv README.md .
   ```

6. **Scripts**
   ```bash
   git mv *.bat scripts/windows/
   git mv *.ps1 scripts/windows/
   git mv *.sh scripts/linux/
   git mv convert_*.py svg_to_*.py scripts/graphics/
   ```

7. **Test files**
   ```bash
   git mv test_*.py tests/unit/
   # Move BotFILES tests too
   ```

8. **Assets**
   ```bash
   git mv FONTS/ assets/fonts/
   git mv TEMPSVG/*.svg assets/svg/sources/
   git mv TEMPSVG/*button*.png assets/images/ui/buttons/
   ```

9. **Archive TEMPSVG**
   ```bash
   git mv TEMPSVG/*.py design/svg_generation/scripts/
   git mv TEMPSVG/password_vault_*.py design/archived/old_implementations/
   ```

10. **Configuration**
    ```bash
    git mv docker-compose.yml config/docker/
    git mv Dockerfile config/docker/
    git mv .dockerignore config/docker/
    git mv .claude/ config/claude/
    git mv .mcp.json config/mcp/
    ```

### Phase 4: Update Imports
**Duration:** 2-3 hours

**Search & replace imports throughout codebase:**

```python
# Old
from phigen import agent_feed
import password_vault_app
from ai_tools import model_router

# New
from src.phigen import agent_feed
from src.password_vault import app
from src.ai_tools import model_router
```

**Files to update:**
- All Python files in src/
- All test files
- All scripts
- Configuration files

**Tool:** Use IDE refactoring or:
```bash
find src/ -name "*.py" -exec sed -i 's/from phigen/from src.phigen/g' {} \;
```

### Phase 5: Update Entry Points
**Duration:** 30 minutes

**Update how applications are launched:**

```python
# Old: python password_vault_app.py
# New: python -m src.password_vault.app

# Old: python BotFILES/jc_discord_bot.py
# New: python -m src.bots.jc_bot.main
```

**Create convenience scripts:**
```bash
# scripts/run_vault.sh
python -m src.password_vault.app

# scripts/run_jc_bot.sh
python -m src.bots.jc_bot.main
```

### Phase 6: Update Configuration Files
**Duration:** 1 hour

**docker-compose.yml:**
```yaml
# Update paths
volumes:
  - ./src:/app/src
  - ./data:/app/data
  - ./config:/app/config
```

**Makefile:**
```makefile
# Update targets
test:
	python -m pytest tests/

run-vault:
	python -m src.password_vault.app
```

**pyproject.toml (NEW):**
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "phigen"
version = "0.1.0"
dependencies = [
    "discord.py>=2.3.0",
    # ... (from requirements.txt)
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### Phase 7: Testing
**Duration:** 1-2 hours

**Test each component:**

1. **Password Vault:**
   ```bash
   python -m src.password_vault.app
   # Verify: Launches, UI loads, encryption works
   ```

2. **Bots:**
   ```bash
   python -m src.bots.jc_bot.main
   # Verify: Connects to Discord, responds to commands
   ```

3. **AI Tools:**
   ```bash
   python -m src.ai_tools.api_server
   # Verify: API starts, model routing works
   ```

4. **Tests:**
   ```bash
   python -m pytest tests/
   # All tests should pass
   ```

### Phase 8: Cleanup
**Duration:** 30 minutes

1. **Remove empty directories:**
   ```bash
   find . -type d -empty -delete
   ```

2. **Remove duplicates/old versions:**
   ```bash
   # Move to design/archived/ instead of deleting
   git mv run_qt_ui_IMPROVED.py design/archived/
   git mv password_vault_complete.py design/archived/
   ```

3. **Clean up test files:**
   ```bash
   # Remove or move temporary test files
   git rm test.txt test2.txt test3.txt test4.txt
   ```

4. **Update documentation:**
   - Update README.md with new structure
   - Update all docs to reflect new paths

### Phase 9: Commit & Review
**Duration:** 30 minutes

```bash
git add .
git commit -m "Restructure: Organize into standard Python project layout

- Move source to src/
- Consolidate tests in tests/
- Organize docs in docs/
- Create scripts/ for utilities
- Move assets to assets/
- Archive TEMPSVG to design/
- Create data/ for runtime files
- Organize config/ files

See RESTRUCTURE_REPORT.md for full details"

git push origin restructure
```

### Phase 10: Merge to Main
**Duration:** Variable (depends on review)

1. Create pull request
2. Review changes
3. Run CI/CD tests
4. Merge to main
5. Update all developers

---

## Benefits After Restructure

### Developer Experience
- ✅ Find files in 5 seconds instead of 30+
- ✅ Clear entry points for each component
- ✅ Standard Python project structure (familiar)
- ✅ Easier to onboard new developers

### Maintenance
- ✅ Easier to locate bugs (know where to look)
- ✅ Clear separation of concerns
- ✅ Reduced risk of editing wrong file
- ✅ Git history cleaner (no binary PNGs)

### Build & Deploy
- ✅ Standard paths for CI/CD
- ✅ Easier Docker builds
- ✅ Clear test runner paths
- ✅ Proper package structure

### Code Quality
- ✅ Easier to enforce code standards
- ✅ Import paths make sense
- ✅ Test organization clear
- ✅ Documentation accessible

---

## Risks & Mitigations

### Risk 1: Breaking Imports
**Likelihood:** High
**Impact:** High
**Mitigation:**
- Tag pre-restructure state for rollback
- Update imports methodically
- Test each component after moving
- Use IDE refactoring tools

### Risk 2: Broken Scripts
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Update batch/shell scripts with new paths
- Create convenience wrapper scripts
- Document new run commands

### Risk 3: Configuration Issues
**Likelihood:** Medium
**Impact:** Medium
**Mitigation:**
- Update Docker configs carefully
- Test in containers before deploying
- Keep .env in root for simplicity

### Risk 4: Git History Loss
**Likelihood:** Low
**Impact:** Low
**Mitigation:**
- Use `git mv` (preserves history)
- Don't delete, move to archived/
- Tag important commits

### Risk 5: Team Disruption
**Likelihood:** High (if active dev)
**Impact:** High
**Mitigation:**
- Coordinate with team (freeze dev)
- Merge quickly after restructure
- Update all documentation
- Post-merge: Help team update local envs

---

## Estimated Timeline

**Total:** 8-12 hours (one full day)

| Phase | Duration | Can Parallelize |
|-------|----------|-----------------|
| 1. Preparation | 30min | No |
| 2. Create directories | 10min | No |
| 3. Move files | 1-2h | No |
| 4. Update imports | 2-3h | Partially |
| 5. Update entry points | 30min | Yes |
| 6. Update configs | 1h | Yes |
| 7. Testing | 1-2h | No |
| 8. Cleanup | 30min | Yes |
| 9. Commit | 30min | No |
| 10. Merge | Variable | No |

**Recommendation:** Block full day, start Friday afternoon or Monday morning

---

## Success Criteria

### Must Have (Before Merge)
- ✅ All imports working
- ✅ All applications launch
- ✅ All tests pass
- ✅ Docker builds successfully
- ✅ Documentation updated

### Nice to Have (Can do after)
- ⚪ pyproject.toml fully configured
- ⚪ CI/CD updated with new paths
- ⚪ Old versions archived (not deleted)
- ⚪ Team trained on new structure

---

## Maintenance After Restructure

### File Placement Guidelines

**When adding new files, use this decision tree:**

```
Is it source code that's imported?
├─ Yes → src/
│  ├─ Is it a core library? → src/phigen/
│  ├─ Is it a bot? → src/bots/
│  ├─ Is it AI-related? → src/ai_tools/
│  └─ Is it shared utility? → src/utils/
│
├─ Is it a standalone script?
│  └─ Yes → scripts/
│     ├─ Windows-specific? → scripts/windows/
│     └─ Graphics utility? → scripts/graphics/
│
├─ Is it a test?
│  └─ Yes → tests/
│     ├─ Unit test? → tests/unit/
│     └─ Integration test? → tests/integration/
│
├─ Is it documentation?
│  └─ Yes → docs/
│     ├─ Guide? → docs/guides/
│     └─ API docs? → docs/api/
│
├─ Is it an asset (image, font)?
│  └─ Yes → assets/
│     ├─ Font? → assets/fonts/
│     └─ Image? → assets/images/
│
└─ Is it configuration?
   └─ Yes → config/
      ├─ Docker? → config/docker/
      └─ Claude? → config/claude/
```

### Prevent Re-Pollution

**Rules:**
1. **Never** put .py files in root (except setup.py if needed)
2. **Never** commit __pycache__ or *.pyc
3. **Never** commit logs or temp files
4. **Never** commit multiple versions (use git branches)
5. **Always** put tests in tests/
6. **Always** put docs in docs/
7. **Always** put scripts in scripts/

**Enforce with:**
- Pre-commit hooks
- Code review checklist
- CI/CD checks

---

## Appendix: File Mapping

### Complete list of files to move

**Password Vault (8 files):**
```
ROOT/password_vault_app.py           → src/password_vault/app.py
ROOT/password_vault_backend.py       → src/password_vault/backend.py
ROOT/validators.py                   → src/password_vault/validators.py
ROOT/run_qt_ui.py                    → src/password_vault/runners/main.py
ROOT/run_qt_ui_IMPROVED.py           → design/archived/
ROOT/run_qt_ui_LAYOUTS.py            → design/archived/
ui/password_vault.ui                 → src/password_vault/ui/main_window.ui
TEMPSVG/buttons_rc.py                → src/password_vault/ui/resources/
```

**Bots (10+ files):**
```
BotFILES/jc_discord_bot.py           → src/bots/jc_bot/main.py
BotFILES/jc_autonomous_worker.py     → src/bots/jc_bot/
BotFILES/jc_feed_watcher.py          → src/bots/jc_bot/
BotFILES/claude_discord_bot.py       → src/bots/claude_bot/main.py
BotFILES/phigen_discord_bot.py       → src/bots/phigen_bot/main.py
BotFILES/discord_mcp_bridge.py       → src/mcp/bridge.py
BotFILES/discord_bot_mcp_enhanced.py → src/mcp/enhanced_bot.py
ai_tools/discord_ai_bot.py           → src/bots/discord_ai/single_model.py
ai_tools/discord_multimodel_bot.py   → src/bots/discord_ai/multimodel.py
```

**Scripts (30+ files):**
```
ROOT/*.bat (9 files)                 → scripts/windows/
ROOT/*.ps1 (3 files)                 → scripts/windows/
ROOT/*.sh (3 files)                  → scripts/linux/
ROOT/convert_svg*.py                 → scripts/graphics/
ROOT/svg_to_png*.py                  → scripts/graphics/
ROOT/crop_title.py                   → scripts/graphics/
ROOT/optimize_title.py               → scripts/graphics/
ROOT/preview_fonts.py                → scripts/development/
ROOT/setup_qt.py                     → src/utils/
ROOT/qt_config.py                    → src/utils/
```

**Documentation (50+ .md files):**
```
ROOT/*.md (except README.md)         → docs/development/
docs/JC_QUICKSTART.md                → docs/guides/
docs/DC_QUICKSTART.md                → docs/guides/
docs/AGENT_COORDINATION.md           → docs/architecture/
```

**Tests (10+ files):**
```
ROOT/test_password_validation.py     → tests/unit/
ai_tools/test_*.py                   → tests/unit/
BotFILES/test_*.py                   → tests/integration/
```

**Assets:**
```
FONTS/                               → assets/fonts/
TEMPSVG/*.svg                        → assets/svg/sources/
TEMPSVG/*button*.png                 → assets/images/ui/buttons/
```

**Configuration:**
```
ROOT/.claude/                        → config/claude/
ROOT/.mcp.json                       → config/mcp/
ROOT/docker-compose.yml              → config/docker/
ROOT/Dockerfile                      → config/docker/
ROOT/.dockerignore                   → config/docker/
```

**Archive:**
```
TEMPSVG/*.py (29 scripts)            → design/svg_generation/scripts/
TEMPSVG/password_vault_complete*.py  → design/archived/old_implementations/
ROOT/run_qt_ui_IMPROVED.py           → design/archived/
ROOT/run_qt_ui_LAYOUTS.py            → design/archived/
```

**Data (gitignored):**
```
docs/agent-feed.jsonl                → data/feeds/
TMPPASSWORDS/passwords.json          → data/passwords/
ROOT/*.log                           → data/logs/ (gitignore)
ROOT/test*.txt                       → DELETE or tests/fixtures/
```

---

## Questions for JC

**Before starting migration:**

1. **Active Development?**
   - Is anyone actively working on feature branches?
   - Should we freeze development during restructure?

2. **Production Usage?**
   - Are any bots running in production?
   - Do we need zero-downtime migration?

3. **Priority Components?**
   - Which components are most critical?
   - Test these first after migration

4. **Deployment Impact?**
   - Are there deployed instances that need updating?
   - Docker containers to rebuild?

5. **Team Size?**
   - How many developers to coordinate with?
   - Training needed after migration?

6. **File Versions:**
   - Which version is production?
     - run_qt_ui.py vs IMPROVED vs LAYOUTS?
     - password_vault_app.py vs complete.py?
   - Archive old or delete?

7. **TEMPSVG Decision:**
   - Archive all 123 files?
   - Keep any scripts as production tools?
   - Delete generated PNGs or keep for reference?

---

## Conclusion

**Current State:** Functional but chaotic (100+ files in root)
**Proposed State:** Clean, standard Python structure
**Effort:** 8-12 hours (one full day)
**Risk:** Medium (imports will break, but recoverable)
**Benefit:** High (much easier to maintain long-term)

**Recommendation:** PROCEED with restructure

**Timing:** Block one full day when:
- No active feature development
- Team can coordinate
- Time for testing after migration

**Rollback Plan:** `git reset --hard pre-restructure` if issues

---

**Report Prepared By:** Claude Code
**Date:** 2025-11-08
**For:** JC (Implementation)
**Status:** Ready for Review
