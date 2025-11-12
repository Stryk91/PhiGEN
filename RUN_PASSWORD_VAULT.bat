@echo off
REM Launch PhiGEN Password Vault GUI
REM Usage: Double-click or run from cmd.exe

cd /d "%~dp0"

echo [PhiGEN Password Vault]
echo Launching Password Vault GUI...
echo.

REM Activate virtual environment and run
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m src.password_vault.app
) else (
    echo Error: Virtual environment not found at .venv
    pause
    exit /b 1
)
