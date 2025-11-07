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
REM STEP 4: Launch Status Monitor GUI
REM ============================================================
echo [4/4] Launching PhiGEN Status Monitor...
echo.

color 0A
echo.
echo  *** PHIGEN SYSTEM IS NOW RUNNING! ***
echo.
echo ============================================================
echo  Opening Status Monitor GUI...
echo ============================================================
echo.
echo  The Status Monitor will show:
echo    - Real-time module status (green = active, grey = offline)
echo    - System logs and events
echo    - Active/Inactive count
echo.
echo  Keep the Status Monitor window open to track system health.
echo.
echo ============================================================
echo.

REM Launch the status monitor GUI
start "PhiGEN Status Monitor" /MIN cmd /c ".\.venv\Scripts\python.exe src\phigen\status_monitor.py"

echo Status Monitor launched!
echo.
echo ============================================================
echo  TO STOP SYSTEM:
echo ============================================================
echo.
echo  Run: STOP_PHIGEN_SYSTEM.bat
echo  Or:  Close Status Monitor and DC Bridge windows
echo       docker-compose -f config\docker\docker-compose.yml down
echo.
echo ============================================================
echo.
echo This launcher window will now close...
echo Services continue running in background.
echo.
timeout /t 3 /nobreak >nul
