@echo off
setlocal
set SCRIPT_DIR=%~dp0
REM Activate venv if present
if exist "%SCRIPT_DIR%\.venv\Scripts\python.exe" (
  "%SCRIPT_DIR%\.venv\Scripts\python.exe" "%SCRIPT_DIR%\password_vault_app.py" %*
) else (
  python "%SCRIPT_DIR%\password_vault_app.py" %*
)
endlocal
