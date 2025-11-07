@echo off
echo ================================================
echo Claude Desktop Macro Test
echo ================================================
echo.
echo This will test the Win+R -^> DC(DESKC) macro.
echo.
echo Make sure:
echo   1. You have saved any work in Claude Desktop
echo   2. You are ready for the window to take focus
echo.
echo ================================================
echo.

cd /d E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\test_claude_macro.py

echo.
pause
