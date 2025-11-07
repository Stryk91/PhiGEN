@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM PhiGEN System Master Launcher
REM Starts all components: Discord Bot, AI Models, DC Bridge
REM ============================================================

color 0A
title PhiGEN System Launcher

echo.
echo ============================================================
echo             PhiGEN SYSTEM LAUNCHER
echo ============================================================
echo.
echo Starting all system components...
echo.
echo ============================================================
echo.

cd /d E:\PythonProjects\PhiGEN

REM ============================================================
REM STEP 1: Check Prerequisites
REM ============================================================
echo [1/4] Checking prerequisites...
echo.

REM Check if Docker is running
echo Checking Docker Desktop...
docker version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)
echo [OK] Docker Desktop is running

REM Check Python venv
echo Checking Python environment...
if not exist ".venv\Scripts\python.exe" (
    color 0C
    echo [ERROR] Python virtual environment not found!
    echo.
    echo Please run: python -m venv .venv
    echo.
    pause
    exit /b 1
)
echo [OK] Python virtual environment found

echo.
echo ============================================================
echo.

REM ============================================================
REM STEP 2: Start Docker Services
REM ============================================================
echo [2/4] Starting Docker services...
echo.
echo This will start:
echo   - Discord Multi-Model Bot
echo   - Ollama (Phi 3.5, Mistral, Granite, BakLLaVA)
echo   - AI REST API
echo.

docker-compose -f config\docker\docker-compose.yml --profile ai up -d

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Failed to start Docker services!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Docker services started
echo.
echo Waiting for services to initialize...
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo.

REM ============================================================
REM STEP 3: Start DC Bridge Watcher
REM ============================================================
echo [3/4] Starting Discord to Claude Code bridge...
echo.

REM Start the bridge in a new window
start "PhiGEN DC Bridge" cmd /k ".\.venv\Scripts\python.exe scripts\utils\watch_and_send_to_dc.py"

echo [OK] DC Bridge watcher started in new window
echo      Keep that window open to process !send_to_dc commands

echo.
echo ============================================================
echo.

REM ============================================================
REM STEP 4: Status Check & Dashboard
REM ============================================================
echo [4/4] Checking system status...
echo.

REM Check Docker containers
docker ps --filter "name=phigen" --format "table {{.Names}}\t{{.Status}}" | findstr "phigen"

echo.
echo ============================================================
echo.

color 0A
echo.
echo  *** PHIGEN SYSTEM IS NOW RUNNING! ***
echo.
echo ============================================================
echo  SYSTEM COMPONENTS:
echo ============================================================
echo.
echo  [Discord Bot]
echo    Status: Running in Docker
echo    Models: Phi 3.5, Mistral 7B, Granite 3B, Claude Sonnet
echo    Commands: !help_ai in Discord
echo.
echo  [DC Bridge]
echo    Status: Running in separate window
echo    Command: !send_to_dc ^<message^>
echo    Purpose: Send messages to Claude Code from Discord
echo.
echo  [AI Services]
echo    Ollama API: http://localhost:11434
echo    REST API: http://localhost:8000
echo.
echo ============================================================
echo  QUICK TESTS:
echo ============================================================
echo.
echo  In Discord:
echo    !status          - Check model availability
echo    !ai Who are you? - Test personality
echo    !send_to_dc Test - Send to Claude Code
echo    !help_ai         - Full command list
echo.
echo ============================================================
echo  TO STOP SYSTEM:
echo ============================================================
echo.
echo  Run: STOP_PHIGEN_SYSTEM.bat
echo  Or:  docker-compose down
echo       Close DC Bridge window
echo.
echo ============================================================
echo.
echo Press any key to exit this launcher...
echo (Services will keep running in background)
echo.
pause >nul
