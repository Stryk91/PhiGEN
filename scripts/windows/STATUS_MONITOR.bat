@echo off
setlocal

REM ============================================================
REM PhiGEN Status Monitor Launcher
REM Opens the GUI status monitor window
REM ============================================================

color 0B
title PhiGEN Status Monitor Launcher

echo.
echo ============================================================
echo          PHIGEN STATUS MONITOR
echo ============================================================
echo.
echo Launching Status Monitor GUI...
echo.

cd /d E:\PythonProjects\PhiGEN

REM Check if venv exists
if not exist ".venv\Scripts\python.exe" (
    color 0C
    echo [ERROR] Python virtual environment not found!
    echo.
    echo Please run: python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Launch the status monitor
".\.venv\Scripts\python.exe" src\phigen\status_monitor.py

endlocal
