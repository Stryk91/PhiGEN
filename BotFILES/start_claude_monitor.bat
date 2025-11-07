@echo off
echo ================================================
echo Starting Claude Code Desktop Monitor
echo ================================================
echo.
echo This script monitors the bulletin board and sends
echo messages to Claude Code's desktop window.
echo.
echo Keep this window open to process Discord messages!
echo.
echo ================================================
echo.

cd /d E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py

echo.
echo.
echo Monitor stopped.
pause
