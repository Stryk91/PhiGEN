.PHONY: help build dev shell test lint scan clean install run format security docker-clean discord-mcp discord-stop

# Default target
help:
	@echo "PhiGEN Development Commands"
	@echo "============================"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build        - Build Docker images"
	@echo "  make dev          - Start development container"
	@echo "  make shell        - Open interactive shell in container"
	@echo "  make stop         - Stop all containers"
	@echo ""
	@echo "Discord MCP:"
	@echo "  make discord-mcp  - Start Discord MCP server"
	@echo "  make discord-stop - Stop Discord MCP server"
	@echo ""
	@echo "Code Quality:"
	@echo "  make test         - Run tests in Docker"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black"
	@echo "  make scan         - Run security scan (Bandit)"
	@echo "  make security     - Full security audit"
	@echo ""
	@echo "Local Development:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make run          - Run the password vault app"
	@echo "  make clean        - Clean temporary files"
	@echo ""
	@echo "Git:"
	@echo "  make hooks        - Verify git hooks are installed"
	@echo "  make commit       - Interactive commit helper"
	@echo ""
	@echo "Maintenance:"
	@echo "  make docker-clean - Remove all Docker containers and images"
	@echo "  make full-clean   - Clean everything (Docker + temp files)"

# Docker commands
build:
	@echo "🐳 Building Docker images..."
	docker-compose build

dev:
	@echo "🚀 Starting development container..."
	docker-compose up -d phigen-dev
	@echo "✅ Container running. Use 'make shell' to access it."

shell:
	@echo "🐚 Opening shell in development container..."
	docker-compose run --rm phigen-dev /bin/bash

stop:
	@echo "🛑 Stopping containers..."
	docker-compose down

# Code quality
test:
	@echo "🧪 Running tests..."
	docker-compose --profile test run --rm phigen-test

lint:
	@echo "🔍 Running linting checks..."
	docker-compose --profile lint run --rm phigen-lint

format:
	@echo "✨ Formatting code with black..."
	docker-compose run --rm phigen-dev black .

scan:
	@echo "🔐 Running security scan..."
	docker-compose --profile scan run --rm phigen-scan

security:
	@echo "🛡️  Running comprehensive security audit..."
	@echo "Running Bandit..."
	docker-compose run --rm phigen-scan sh -c "pip install bandit -q && bandit -ll -r ." || true
	@echo "Checking for known vulnerabilities..."
	docker-compose run --rm phigen-scan sh -c "pip install safety -q && safety check" || true
	@echo "✅ Security scan complete"

# Local development
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt || echo "⚠️  No requirements.txt found"
	pip install PyQt6 cryptography bandit pylint black pytest

run:
	@echo "🚀 Running PhiGEN Password Vault..."
	python password_vault_app.py

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.tmp" -delete 2>/dev/null || true
	rm -f nul temp_*.png 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Git helpers
hooks:
	@echo "🪝 Verifying git hooks..."
	@test -f .git/hooks/pre-commit && echo "✅ pre-commit hook installed" || echo "❌ pre-commit hook missing"
	@test -f .git/hooks/commit-msg && echo "✅ commit-msg hook installed" || echo "❌ commit-msg hook missing"
	@test -f .git/hooks/pre-push && echo "✅ pre-push hook installed" || echo "❌ pre-push hook missing"
	@test -f .git/hooks/post-commit && echo "✅ post-commit hook installed" || echo "❌ post-commit hook missing"

commit:
	@echo "📝 Commit Helper"
	@echo "==============="
	@echo "Choose commit type:"
	@echo "  1) feat     - New feature"
	@echo "  2) fix      - Bug fix"
	@echo "  3) docs     - Documentation"
	@echo "  4) refactor - Code refactoring"
	@echo "  5) test     - Tests"
	@echo "  6) chore    - Maintenance"
	@read -p "Enter number (1-6): " choice; \
	case $$choice in \
		1) type="feat";; \
		2) type="fix";; \
		3) type="docs";; \
		4) type="refactor";; \
		5) type="test";; \
		6) type="chore";; \
		*) echo "Invalid choice"; exit 1;; \
	esac; \
	read -p "Scope (optional, press enter to skip): " scope; \
	read -p "Description: " desc; \
	if [ -z "$$scope" ]; then \
		msg="$$type: $$desc"; \
	else \
		msg="$$type($$scope): $$desc"; \
	fi; \
	git commit -m "$$msg"

# Discord MCP commands
discord-mcp:
	@echo "🤖 Starting Discord MCP server..."
	docker-compose --profile mcp up -d discord-mcp
	@echo "✅ Discord MCP running on port 3000"
	@echo "Bot should now be online in your Discord server!"

discord-stop:
	@echo "🛑 Stopping Discord MCP server..."
	docker-compose stop discord-mcp
	docker-compose rm -f discord-mcp
	@echo "✅ Discord MCP stopped"

# Docker cleanup
docker-clean:
	@echo "🗑️  Removing Docker containers and images..."
	docker-compose down -v
	docker images | grep phigen | awk '{print $$3}' | xargs docker rmi -f 2>/dev/null || true
	@echo "✅ Docker cleanup complete"

full-clean: clean docker-clean
	@echo "🧹 Full cleanup complete"

# Quick shortcuts
s: shell
b: build
t: test
l: lint
r: run
c: clean
d: discord-mcp
