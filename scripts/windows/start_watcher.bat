@echo off
REM JC Agent Feed Watcher - Start Script
REM Monitors agent feed and sends Discord notifications

echo ============================================================
echo   JC AGENT FEED WATCHER - Starting...
echo ============================================================
echo.

cd /d "%~dp0\.."

echo Project Root: %CD%
echo Watcher Script: %CD%\BotFILES\jc_feed_watcher.py
echo.

echo.
echo ============================================================
echo   WATCHER RUNNING - Press Ctrl+C to stop
echo ============================================================
echo.

.venv\Scripts\python.exe BotFILES\jc_feed_watcher.py

echo.
echo ============================================================
echo   Watcher stopped
echo ============================================================
pause
