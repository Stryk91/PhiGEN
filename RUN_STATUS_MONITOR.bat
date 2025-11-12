@echo off
REM Launch PhiGEN Status Monitor GUI
REM Usage: Double-click or run from cmd.exe

cd /d "%~dp0"

echo [PhiGEN Status Monitor]
echo Launching Status Monitor GUI...
echo.

REM Activate virtual environment and run
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m src.phigen.status_monitor
) else (
    echo Error: Virtual environment not found at .venv
    pause
    exit /b 1
)
