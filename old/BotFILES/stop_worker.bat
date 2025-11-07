@echo off
REM JC Autonomous Worker - Stop Script
REM Stops the running autonomous worker process

echo ============================================================
echo   JC AUTONOMOUS WORKER - Stopping...
echo ============================================================
echo.

echo Searching for worker process...
tasklist | findstr /I "python.exe" >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Found Python processes. Attempting to stop worker...
    echo.

    REM Note: This will kill ALL python processes
    REM In production, you'd want to be more selective

    echo WARNING: This will stop ALL Python processes!
    echo Press Ctrl+C to cancel, or
    pause

    taskkill /F /IM python.exe /FI "WINDOWTITLE eq *"

    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ============================================================
        echo   Worker stopped successfully
        echo ============================================================
    ) else (
        echo.
        echo ============================================================
        echo   Error stopping worker
        echo ============================================================
    )
) else (
    echo.
    echo No Python processes found. Worker may not be running.
    echo.
    echo ============================================================
    echo   Nothing to stop
    echo ============================================================
)

echo.
pause
