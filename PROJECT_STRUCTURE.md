# PhiGEN Project Structure

This document describes the reorganized structure of the PhiGEN repository after the comprehensive restructure.

## Overview

PhiGEN is now organized as a standard Python project with clear separation of concerns, following best practices for package structure and development workflow.

## Directory Structure

```
PhiGEN/
├── README.md                    # Main project documentation
├── GIT_BRANCHING_GUIDE.md        # Git workflow guide
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation setup
├── .gitignore                   # Git ignore patterns
├── pyproject.toml              # Modern Python project configuration
├── Makefile                     # Build and utility commands
├── src/                         # Source code packages
│   ├── phigen/                  # Main Discord bot package
│   │   ├── __init__.py          # Package initialization
│   │   ├── agent_feed.py        # Agent feed functionality
│   │   ├── detect_agent.py      # Agent detection
│   │   ├── bots/                # Bot implementations
│   │   │   ├── __init__.py      # Bots package init
│   │   │   ├── discord_bot.py   # Main Discord bot
│   │   │   ├── claude_discord_bot.py
│   │   │   ├── discord_bot_mcp_enhanced.py
│   │   │   ├── jc_discord_bot.py
│   │   │   ├── discord_mcp_bridge.py
│   │   │   ├── jc_autonomous_worker.py
│   │   │   ├── task_executor.py
│   │   │   └── [other bot files]
│   │   └── core/                # Core bot functionality
│   ├── password_vault/          # Password vault application
│   │   ├── __init__.py          # Package initialization
│   │   ├── app.py               # GUI application main
│   │   ├── backend.py           # Backend logic
│   │   ├── validators.py        # Password validation
│   │   └── ui/                  # UI definition files
│   │       ├── password_vault.ui
│   │       ├── password_vault_IMPROVED.ui
│   │       └── password_vault_LAYOUTS.ui
│   ├── ai_tools/                # AI integrations
│   │   ├── __init__.py          # Package initialization
│   │   ├── README.md            # AI tools documentation
│   │   ├── analyze_conversations.py
│   │   ├── api_server.py
│   │   ├── code_reviewer.py
│   │   ├── conversation_logger.py
│   │   ├── conversation_rag.py
│   │   ├── discord_ai_bot.py
│   │   ├── discord_multimodel_bot.py
│   │   ├── enhanced_personality.py
│   │   ├── log_analyzer.py
│   │   ├── model_router.py
│   │   ├── ollama_client.py
│   │   ├── user_settings.py
│   │   └── [other AI tool files]
│   └── utils/                   # Shared utilities
│       └── __init__.py          # Utils package init
├── tests/                       # Test suite
│   ├── __init__.py              # Tests package init
│   ├── conftest.py              # Pytest configuration
│   ├── unit/                    # Unit tests
│   │   ├── test_agent_feed.py
│   │   ├── test_ai_integration.py
│   │   ├── test_auth.py
│   │   ├── test_autonomous_worker.py
│   │   ├── test_claude_api.py
│   │   ├── test_mcp_bridge.py
│   │   ├── test_multimodel.py
│   │   └── test_password_validation.py
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test fixtures
├── scripts/                     # Utility scripts
│   ├── windows/                 # Windows-specific scripts
│   │   ├── RUN_PASSWORD_VAULT.bat
│   │   ├── START_PHIGEN_SYSTEM.bat
│   │   ├── STATUS_CHECK.bat
│   │   ├── STOP_PHIGEN_SYSTEM.bat
│   │   ├── install_dependencies.bat
│   │   ├── phigen.bat
│   │   ├── phigen.ps1
│   │   ├── passgen2.ps1
│   │   ├── send_message_to_dc.bat
│   │   ├── send_to_dc.ps1
│   │   ├── start_dc_bridge.bat
│   │   └── [other Windows scripts]
│   ├── linux/                   # Linux-specific scripts
│   │   ├── kali_security_tests.sh
│   │   ├── start_ai.sh
│   │   └── start_multimodel_bot.sh
│   └── utils/                   # Cross-platform utility scripts
│       ├── convert_svg.py
│       ├── crop_title.py
│       ├── downsample_title.py
│       ├── fix_title_bg.py
│       ├── preview_fonts.py
│       ├── qt_config.py
│       ├── remove_white_bg.py
│       ├── run_qt_ui.py
│       ├── setup_qt.py
│       ├── svg_to_png.py
│       └── [other utility scripts]
├── docs/                        # Documentation
│   ├── guides/                  # User guides
│   │   ├── AI_INTEGRATION_COMPLETE.md
│   │   ├── BOT_PERSONALITY_CONFIG.md
│   │   ├── CLAUDE.md
│   │   ├── CUSTOM_COMMANDS_GUIDE.md
│   │   ├── DEV_COMMANDS.md
│   │   ├── DISCORD_MCP_COMPLETE_GUIDE.md
│   │   ├── [other guides]
│   ├── development/             # Developer documentation
│   │   ├── AGENT_IDENTITY_SYSTEM.md
│   │   ├── SECURITY_ANALYSIS_REPORT.md
│   │   ├── RESTRUCTURE_REPORT.md
│   │   └── [other dev docs]
│   ├── architecture/            # Design documents
│   ├── api/                     # API reference
│   └── [other documentation]
├── config/                      # Configuration files
│   ├── .env.example             # Environment variables template
│   └── docker/                  # Docker configuration
│       ├── Dockerfile
│       └── docker-compose.yml
├── assets/                      # Static assets
│   └── fonts/                   # Font files
│       ├── Cyberdyne-*.otf
│       ├── Xolonium/
│       ├── drafting-mono/
│       ├── leviathans/
│       └── [other font families]
├── archive/                     # Deprecated/temporary files
└── .claude/                     # Claude Code configuration
```

## Key Changes

### Before Restructure
- 100+ files scattered in root directory
- No proper package structure
- Tests mixed with source code
- Scripts and documentation unorganized
- No clear separation of concerns

### After Restructure
- **Organized Source Code**: All source code in `src/` with proper package structure
- **Separated Concerns**: 
  - `src/phigen/` - Main Discord bot functionality
  - `src/password_vault/` - Password vault application
  - `src/ai_tools/` - AI integrations and tools
  - `src/utils/` - Shared utilities
- **Proper Testing**: All tests in `tests/` with pytest configuration
- **Organized Scripts**: Platform-specific scripts in appropriate subdirectories
- **Structured Documentation**: Separated into guides, development docs, and API docs
- **Asset Management**: All assets (fonts, images) in `assets/`
- **Configuration**: Environment and Docker config in `config/`

## Import Patterns

### Password Vault
```python
from src.password_vault import PasswordVault, PasswordGenerator
from src.password_vault.validators import validate_password
```

### Discord Bots
```python
from src.phigen.bots.discord_bot import PhiGenBot
from src.phigen.bots.jc_autonomous_worker import JCAutonomousWorker
```

### AI Tools
```python
from src.ai_tools import model_router, conversation_analyzer
from src.ai_tools.ollama_client import OllamaClient
```

## Development Workflow

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run unit tests only
python -m pytest tests/unit/

# Run with coverage
python -m pytest --cov=src tests/
```

### Running Applications
```bash
# Password Vault (if PyQt6 available)
python -m src.password_vault.app

# Discord Bot (if discord.py available)
python -m src.phigen.bots.discord_bot

# AI Tools
python -m src.ai_tools.api_server
```

### Using Scripts
```bash
# Windows
scripts\windows\START_PHIGEN_SYSTEM.bat

# Linux
./scripts/linux/start_ai.sh

# Cross-platform utilities
python scripts/utils/preview_fonts.py
```

## Git Safety

The restructure was performed with strict git safety protocols:
- Created `pre-agent-v1.0` safety tag
- Worked in `agent-restructure` branch
- Used `git mv` for all file moves (preserves history)
- Committed after each phase
- All import statements verified

## Next Steps

1. Review and test the new structure
2. Update CI/CD pipelines if needed
3. Update deployment scripts
4. Create requirements.txt files for each package if needed
5. Consider adding type hints and docstrings
6. Set up automated testing in CI/CD

## Benefits

- **Maintainability**: Clear structure makes code easier to navigate and maintain
- **Testing**: Proper test organization enables better test coverage
- **Development**: Standard Python structure follows best practices
- **Deployment**: Organized scripts and config make deployment easier
- **Collaboration**: Clear structure helps new developers understand the project