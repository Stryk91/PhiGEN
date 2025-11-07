# PhiGEN

A comprehensive Python application suite featuring Discord bots, password vault management, and AI integration tools.

## Overview

PhiGEN is a multi-component system that provides:
- **Discord Bot Infrastructure**: Multiple Discord bots with MCP integration
- **Password Vault**: Secure password management with GUI interface
- **AI Tools**: Integration with various AI models and conversation analysis
- **Automation**: Task execution and workflow automation

## Quick Start

### Prerequisites

- Python 3.8+
- PyQt6 (for password vault GUI)
- discord.py (for Discord bots)
- cryptography (for password encryption)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd PhiGEN

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp config/.env.example .env
# Edit .env with your configuration
```

### Running Applications

#### Password Vault
```bash
# Windows
scripts\windows\RUN_PASSWORD_VAULT.bat

# Linux/Mac
python -m src.password_vault.app
```

#### Discord Bots
```bash
# Start main bot
scripts\windows\START_PHIGEN_SYSTEM.bat

# Or run directly
python -m src.phigen.bots.discord_bot
```

#### AI Tools
```bash
# Start AI integration
./scripts/linux/start_ai.sh

# Or run directly
python -m src.ai_tools.api_server
```

## Project Structure

This project follows a standard Python package structure:

```
src/
├── phigen/           # Discord bot functionality
├── password_vault/   # Password management application
├── ai_tools/         # AI integration tools
└── utils/            # Shared utilities

tests/                # Test suite
scripts/              # Utility scripts
docs/                 # Documentation
config/               # Configuration files
assets/               # Static assets
```

For detailed structure information, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

## Features

### Discord Bots
- Multi-model AI integration
- MCP (Model Context Protocol) support
- Autonomous task execution
- Conversation logging and analysis
- Custom command system

### Password Vault
- Secure password storage with encryption
- Password generation and validation
- Cross-platform GUI (Qt6)
- Import/export functionality

### AI Tools
- Multiple AI model support
- Conversation analysis and RAG
- Personality integration
- Code review assistance
- Knowledge base management

## Documentation

- [Project Structure](PROJECT_STRUCTURE.md) - Detailed project layout
- [Git Branching Guide](GIT_BRANCHING_GUIDE.md) - Development workflow
- [User Guides](docs/guides/) - Usage documentation
- [Development Docs](docs/development/) - Developer resources

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the [documentation](docs/)
- Review [guides](docs/guides/)
- Open an issue for bug reports or feature requests

## Recent Changes

The repository has undergone a comprehensive restructure to improve organization and maintainability. All file moves were performed using `git mv` to preserve history. See [RESTRUCTURE_REPORT.md](docs/development/RESTRUCTURE_REPORT.md) for detailed information about the changes.