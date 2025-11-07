@echo off
setlocal

REM ============================================================
REM PhiGEN System Shutdown Script
REM Stops all components gracefully
REM ============================================================

color 0E
title PhiGEN System Shutdown

echo.
echo ============================================================
echo             PHIGEN SYSTEM SHUTDOWN
echo ============================================================
echo.
echo Stopping all system components...
echo.
echo ============================================================
echo.

cd /d E:\PythonProjects\PhiGEN

REM ============================================================
REM STEP 1: Stop Docker Services
REM ============================================================
echo [1/2] Stopping Docker services...
echo.

docker-compose -f config\docker\docker-compose.yml --profile ai down

if errorlevel 1 (
    echo [WARNING] Some Docker services may not have stopped cleanly
) else (
    echo [OK] Docker services stopped
)

echo.
echo ============================================================
echo.

REM ============================================================
REM STEP 2: Stop DC Bridge (if running)
REM ============================================================
echo [2/2] Checking for DC Bridge process...
echo.

REM Try to find and kill the Python process running the bridge
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo list ^| findstr /i "PID"') do (
    set pid=%%a
    wmic process where "ProcessId=!pid!" get CommandLine 2>nul | findstr /i "watch_and_send_to_dc" >nul
    if not errorlevel 1 (
        echo Stopping DC Bridge process (PID: !pid!)...
        taskkill /PID !pid! /F >nul 2>&1
        if not errorlevel 1 (
            echo [OK] DC Bridge stopped
        )
    )
)

echo.
echo ============================================================
echo.

color 0A
echo.
echo  *** PHIGEN SYSTEM STOPPED ***
echo.
echo ============================================================
echo  All components have been shut down:
echo ============================================================
echo.
echo  [x] Discord Bot
echo  [x] AI Models (Ollama)
echo  [x] DC Bridge
echo  [x] REST API
echo.
echo ============================================================
echo.
echo  To restart: Run START_PHIGEN_SYSTEM.bat
echo.
echo ============================================================
echo.
pause
