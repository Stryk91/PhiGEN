@echo off
echo ================================================
echo Discord to Claude Code Bridge
echo ================================================
echo.
echo This script monitors for Discord messages and
echo sends them to Claude Code via macro automation.
echo.
echo Keep this window open to process !send_to_dc commands!
echo.
echo ================================================
echo.

cd /d E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe watch_and_send_to_dc.py

echo.
echo.
echo Bridge stopped.
pause
