@echo off
setlocal

REM ============================================================
REM PhiGEN System Status Checker
REM Quick status check of all components
REM ============================================================

color 0B
title PhiGEN System Status

echo.
echo ============================================================
echo             PHIGEN SYSTEM STATUS
echo ============================================================
echo.

cd /d E:\PythonProjects\PhiGEN

REM Check Docker
echo [Docker Desktop]
docker version >nul 2>&1
if errorlevel 1 (
    echo   Status: NOT RUNNING
    color 0C
) else (
    echo   Status: Running
)
echo.

REM Check Docker Containers
echo [Docker Containers]
docker ps --filter "name=phigen" --format "  {{.Names}}: {{.Status}}" 2>nul
if errorlevel 1 (
    echo   No PhiGEN containers running
)
echo.

REM Check DC Bridge
echo [DC Bridge Watcher]
tasklist /fi "imagename eq python.exe" 2>nul | findstr /i "python.exe" >nul
if errorlevel 1 (
    echo   Status: Not running
) else (
    REM Check if it's specifically our bridge script
    set found=0
    for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr /i "PID"') do (
        wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /i "watch_and_send_to_dc" >nul
        if not errorlevel 1 (
            echo   Status: Running (PID: %%a^)
            set found=1
        )
    )
    if !found!==0 (
        echo   Status: Not running
    )
)
echo.

REM Check Ollama API
echo [Ollama API]
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo   Status: Not responding
) else (
    echo   Status: Running (http://localhost:11434)
)
echo.

REM Check REST API
echo [REST API]
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo   Status: Not responding
) else (
    echo   Status: Running (http://localhost:8000)
)
echo.

echo ============================================================
echo.
echo To start system: START_PHIGEN_SYSTEM.bat
echo To stop system:  STOP_PHIGEN_SYSTEM.bat
echo.
echo ============================================================
echo.
pause
