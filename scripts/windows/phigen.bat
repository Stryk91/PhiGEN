@echo off
REM PhiGEN Development Helper for Windows
REM Usage: phigen.bat [command]

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="build" goto build
if "%1"=="dev" goto dev
if "%1"=="shell" goto shell
if "%1"=="stop" goto stop
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="scan" goto scan
if "%1"=="security" goto security
if "%1"=="run" goto run
if "%1"=="clean" goto clean
if "%1"=="hooks" goto hooks
if "%1"=="format" goto format
goto invalid

:help
echo.
echo PhiGEN Development Commands
echo ============================
echo.
echo Docker Commands:
echo   phigen build        - Build Docker images
echo   phigen dev          - Start development container
echo   phigen shell        - Open interactive shell in container
echo   phigen stop         - Stop all containers
echo.
echo Code Quality:
echo   phigen test         - Run tests in Docker
echo   phigen lint         - Run linting checks
echo   phigen format       - Format code with black
echo   phigen scan         - Run security scan
echo   phigen security     - Full security audit
echo.
echo Local Development:
echo   phigen run          - Run the password vault app
echo   phigen clean        - Clean temporary files
echo.
echo Git:
echo   phigen hooks        - Verify git hooks are installed
echo.
goto end

:build
echo Building Docker images...
docker-compose build
goto end

:dev
echo Starting development container...
docker-compose up -d phigen-dev
echo Container running. Use 'phigen shell' to access it.
goto end

:shell
echo Opening shell in development container...
docker-compose run --rm phigen-dev /bin/bash
goto end

:stop
echo Stopping containers...
docker-compose down
goto end

:test
echo Running tests...
docker-compose --profile test run --rm phigen-test
goto end

:lint
echo Running linting checks...
docker-compose --profile lint run --rm phigen-lint
goto end

:format
echo Formatting code with black...
docker-compose run --rm phigen-dev black .
goto end

:scan
echo Running security scan...
docker-compose --profile scan run --rm phigen-scan
goto end

:security
echo Running comprehensive security audit...
docker-compose run --rm phigen-scan sh -c "pip install bandit safety -q && bandit -ll -r . && safety check"
goto end

:run
echo Running PhiGEN Password Vault...
python password_vault_app.py
goto end

:clean
echo Cleaning temporary files...
powershell -Command "Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo,*.tmp -Recurse | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue"
if exist nul del /f nul
if exist temp_*.png del /f temp_*.png
echo Cleanup complete
goto end

:hooks
echo Verifying git hooks...
if exist .git\hooks\pre-commit (echo [OK] pre-commit hook installed) else (echo [X] pre-commit hook missing)
if exist .git\hooks\commit-msg (echo [OK] commit-msg hook installed) else (echo [X] commit-msg hook missing)
if exist .git\hooks\pre-push (echo [OK] pre-push hook installed) else (echo [X] pre-push hook missing)
if exist .git\hooks\post-commit (echo [OK] post-commit hook installed) else (echo [X] post-commit hook missing)
goto end

:invalid
echo Invalid command: %1
echo Run 'phigen help' for available commands
goto end

:end
