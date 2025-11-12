@echo off
REM Launch PhiVector Control Bridge
REM Usage: Double-click or run from cmd.exe

cd /d "%~dp0"

echo [PhiVector Control Bridge]
echo Launching System Management Hub...
echo.

REM Activate virtual environment and run
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m src.phivector.control_bridge
) else (
    echo Error: Virtual environment not found at .venv
    pause
    exit /b 1
)
