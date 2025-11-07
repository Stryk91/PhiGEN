@echo off
setlocal
set SCRIPT_DIR=%~dp0
REM Activate venv if present
if exist "%SCRIPT_DIR%\.venv\Scripts\python.exe" (
  "%SCRIPT_DIR%\.venv\Scripts\python.exe" "%SCRIPT_DIR%\src\password_vault\app.py" %*
) else (
  python "%SCRIPT_DIR%\src\password_vault\app.py" %*
)
endlocal
