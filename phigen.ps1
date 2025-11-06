# PhiGEN Development Helper for PowerShell
# Usage: .\phigen.ps1 [command]

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "`nPhiGEN Development Commands" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Docker Commands:" -ForegroundColor Yellow
    Write-Host "  .\phigen.ps1 build        - Build Docker images"
    Write-Host "  .\phigen.ps1 dev          - Start development container"
    Write-Host "  .\phigen.ps1 shell        - Open interactive shell in container"
    Write-Host "  .\phigen.ps1 stop         - Stop all containers"
    Write-Host ""
    Write-Host "Code Quality:" -ForegroundColor Yellow
    Write-Host "  .\phigen.ps1 test         - Run tests in Docker"
    Write-Host "  .\phigen.ps1 lint         - Run linting checks"
    Write-Host "  .\phigen.ps1 format       - Format code with black"
    Write-Host "  .\phigen.ps1 scan         - Run security scan"
    Write-Host "  .\phigen.ps1 security     - Full security audit"
    Write-Host ""
    Write-Host "Local Development:" -ForegroundColor Yellow
    Write-Host "  .\phigen.ps1 run          - Run the password vault app"
    Write-Host "  .\phigen.ps1 clean        - Clean temporary files"
    Write-Host ""
    Write-Host "Git:" -ForegroundColor Yellow
    Write-Host "  .\phigen.ps1 hooks        - Verify git hooks are installed"
    Write-Host "  .\phigen.ps1 commit       - Interactive commit helper"
    Write-Host ""
}

function Build-Docker {
    Write-Host "🐳 Building Docker images..." -ForegroundColor Cyan
    docker-compose build
}

function Start-Dev {
    Write-Host "🚀 Starting development container..." -ForegroundColor Cyan
    docker-compose up -d phigen-dev
    Write-Host "✅ Container running. Use '.\phigen.ps1 shell' to access it." -ForegroundColor Green
}

function Open-Shell {
    Write-Host "🐚 Opening shell in development container..." -ForegroundColor Cyan
    docker-compose run --rm phigen-dev /bin/bash
}

function Stop-Containers {
    Write-Host "🛑 Stopping containers..." -ForegroundColor Cyan
    docker-compose down
}

function Run-Tests {
    Write-Host "🧪 Running tests..." -ForegroundColor Cyan
    docker-compose --profile test run --rm phigen-test
}

function Run-Lint {
    Write-Host "🔍 Running linting checks..." -ForegroundColor Cyan
    docker-compose --profile lint run --rm phigen-lint
}

function Run-Format {
    Write-Host "✨ Formatting code with black..." -ForegroundColor Cyan
    docker-compose run --rm phigen-dev black .
}

function Run-Scan {
    Write-Host "🔐 Running security scan..." -ForegroundColor Cyan
    docker-compose --profile scan run --rm phigen-scan
}

function Run-Security {
    Write-Host "🛡️  Running comprehensive security audit..." -ForegroundColor Cyan
    docker-compose run --rm phigen-scan sh -c "pip install bandit safety -q && bandit -ll -r . && safety check"
}

function Run-App {
    Write-Host "🚀 Running PhiGEN Password Vault..." -ForegroundColor Cyan
    python password_vault_app.py
}

function Clean-Files {
    Write-Host "🧹 Cleaning temporary files..." -ForegroundColor Cyan
    Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo,*.tmp -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path nul -ErrorAction SilentlyContinue
    Remove-Item -Path temp_*.png -ErrorAction SilentlyContinue
    Write-Host "✅ Cleanup complete" -ForegroundColor Green
}

function Check-Hooks {
    Write-Host "🪝 Verifying git hooks..." -ForegroundColor Cyan
    $hooks = @("pre-commit", "commit-msg", "pre-push", "post-commit")
    foreach ($hook in $hooks) {
        $path = ".git\hooks\$hook"
        if (Test-Path $path) {
            Write-Host "✅ $hook hook installed" -ForegroundColor Green
        } else {
            Write-Host "❌ $hook hook missing" -ForegroundColor Red
        }
    }
}

function Interactive-Commit {
    Write-Host "`n📝 Commit Helper" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Choose commit type:"
    Write-Host "  1) feat     - New feature"
    Write-Host "  2) fix      - Bug fix"
    Write-Host "  3) docs     - Documentation"
    Write-Host "  4) refactor - Code refactoring"
    Write-Host "  5) test     - Tests"
    Write-Host "  6) chore    - Maintenance"

    $choice = Read-Host "Enter number (1-6)"

    $type = switch ($choice) {
        "1" { "feat" }
        "2" { "fix" }
        "3" { "docs" }
        "4" { "refactor" }
        "5" { "test" }
        "6" { "chore" }
        default {
            Write-Host "Invalid choice" -ForegroundColor Red
            return
        }
    }

    $scope = Read-Host "Scope (optional, press enter to skip)"
    $desc = Read-Host "Description"

    if ([string]::IsNullOrWhiteSpace($scope)) {
        $msg = "$type`: $desc"
    } else {
        $msg = "$type($scope): $desc"
    }

    git commit -m $msg
}

# Main command router
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "build" { Build-Docker }
    "dev" { Start-Dev }
    "shell" { Open-Shell }
    "stop" { Stop-Containers }
    "test" { Run-Tests }
    "lint" { Run-Lint }
    "format" { Run-Format }
    "scan" { Run-Scan }
    "security" { Run-Security }
    "run" { Run-App }
    "clean" { Clean-Files }
    "hooks" { Check-Hooks }
    "commit" { Interactive-Commit }
    default {
        Write-Host "Invalid command: $Command" -ForegroundColor Red
        Write-Host "Run '.\phigen.ps1 help' for available commands" -ForegroundColor Yellow
    }
}
