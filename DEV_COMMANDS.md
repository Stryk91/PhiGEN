# PhiGEN Development Commands

Quick reference guide for development workflow.

## Quick Start

### Windows (CMD)
```cmd
phigen help          # Show all commands
phigen dev           # Start development environment
phigen run           # Run the app
```

### Windows (PowerShell)
```powershell
.\phigen.ps1 help    # Show all commands
.\phigen.ps1 dev     # Start development environment
.\phigen.ps1 run     # Run the app
```

### Linux/WSL/Make
```bash
make help            # Show all commands
make dev             # Start development environment
make run             # Run the app
```

## Docker Commands

| Command | Windows CMD | PowerShell | Make |
|---------|------------|------------|------|
| Build images | `phigen build` | `.\phigen.ps1 build` | `make build` |
| Start dev container | `phigen dev` | `.\phigen.ps1 dev` | `make dev` |
| Open shell | `phigen shell` | `.\phigen.ps1 shell` | `make shell` |
| Stop containers | `phigen stop` | `.\phigen.ps1 stop` | `make stop` |

## Code Quality

| Command | Windows CMD | PowerShell | Make |
|---------|------------|------------|------|
| Run tests | `phigen test` | `.\phigen.ps1 test` | `make test` |
| Lint code | `phigen lint` | `.\phigen.ps1 lint` | `make lint` |
| Format code | `phigen format` | `.\phigen.ps1 format` | `make format` |
| Security scan | `phigen scan` | `.\phigen.ps1 scan` | `make scan` |
| Full security audit | `phigen security` | `.\phigen.ps1 security` | `make security` |

## Local Development

| Command | Windows CMD | PowerShell | Make |
|---------|------------|------------|------|
| Run app | `phigen run` | `.\phigen.ps1 run` | `make run` |
| Clean temp files | `phigen clean` | `.\phigen.ps1 clean` | `make clean` |

## Git Workflow

| Command | Windows CMD | PowerShell | Make |
|---------|------------|------------|------|
| Check hooks | `phigen hooks` | `.\phigen.ps1 hooks` | `make hooks` |
| Interactive commit | N/A | `.\phigen.ps1 commit` | `make commit` |

## Git Hooks (Automatic)

These run automatically during git operations:

### pre-commit
Runs before each commit:
- Python syntax checking
- Hardcoded credential detection
- Dangerous function detection (eval, exec)
- Large file warnings (>1MB)

### commit-msg
Enforces commit message format:
```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
```

Examples:
- `feat: add password strength indicator`
- `fix(ui): resolve button alignment`
- `docs: update README`

### pre-push
Runs before pushing to remote:
- Blocks sensitive files (.pem, .key, .env)
- Detects large files (>10MB)
- Scans for hardcoded secrets
- Docker-based security scan (if available)

### post-commit
Sends notification to Discord webhook with:
- Commit message and hash
- Author and branch
- Files changed
- Timestamp

## Docker Compose Profiles

Run specific services:

```bash
# Security scan
docker-compose --profile scan up phigen-scan

# Run tests
docker-compose --profile test up phigen-test

# Linting
docker-compose --profile lint up phigen-lint
```

## Bypassing Checks

### Skip pre-commit hook
```bash
git commit --no-verify -m "your message"
```

### Skip security warnings
Add `# nosec` comment to the line:
```python
password = "test123"  # nosec - example only
```

## Common Workflows

### Making a Commit
```bash
# 1. Stage your changes
git add .

# 2. Commit (hooks run automatically)
git commit -m "feat: add new feature"

# 3. Check Discord for notification
```

### Before Pushing
```bash
# 1. Run security scan
phigen scan

# 2. Run tests
phigen test

# 3. Push (pre-push hook runs automatically)
git push
```

### Development Session
```bash
# 1. Start Docker environment
phigen dev

# 2. Open shell in container
phigen shell

# 3. Make changes, test, commit
# 4. Clean up when done
phigen stop
```

## Troubleshooting

### Hooks not running
```bash
phigen hooks  # Check if hooks are installed
chmod +x .git/hooks/*  # Make hooks executable (Linux/WSL)
```

### Docker build fails
```bash
phigen clean          # Clean temp files
docker-compose down   # Stop containers
phigen build          # Rebuild
```

### Commit message rejected
Make sure your commit follows the format:
```
type: description at least 10 chars long
```

### Pre-commit blocking you
If checks are incorrect, you can bypass:
```bash
git commit --no-verify -m "your message"
```

## Tips

1. Use `phigen commit` (PowerShell) or `make commit` for interactive commit helper
2. Run `phigen security` before important pushes
3. Check `phigen hooks` regularly to ensure hooks are working
4. Use Docker for consistent testing environment
5. Discord notifications keep your team informed automatically
