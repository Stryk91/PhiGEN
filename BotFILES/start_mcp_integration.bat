@echo off
REM Start Discord Bot with MCP Integration

echo ========================================
echo PhiGEN Discord Bot - MCP Integration
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting MCP Bridge on port 5000...
start "MCP Bridge" cmd /k python "%~dp0discord_mcp_bridge.py"

timeout /t 3 /nobreak >nul

echo Starting Discord Bot with MCP support...
start "Discord Bot" cmd /k python "%~dp0discord_bot_mcp_enhanced.py"

echo.
echo ========================================
echo Both services started!
echo ========================================
echo MCP Bridge: http://localhost:5000
echo Discord Bot: Connected to Discord
echo.
echo Press any key to exit (services will continue running)
pause >nul
