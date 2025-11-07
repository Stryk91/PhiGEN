@echo off
REM JC Autonomous Worker - Start Script
REM Quick launcher for the autonomous worker

echo ============================================================
echo   JC AUTONOMOUS WORKER - Starting...
echo ============================================================
echo.

cd /d "%~dp0\.."

echo Project Root: %CD%
echo Worker Script: %CD%\BotFILES\jc_autonomous_worker.py
echo.

echo Starting worker in 3 seconds...
echo Press Ctrl+C to cancel
timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo   WORKER RUNNING - Press Ctrl+C to stop
echo ============================================================
echo.

python BotFILES\jc_autonomous_worker.py

echo.
echo ============================================================
echo   Worker stopped
echo ============================================================
pause
