# Send message to Claude Code (DC) via automation
# Usage: .\send_to_dc.ps1 "Your message here"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,

    [Parameter(Mandatory=$false)]
    [string]$Author = "Discord Bot"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Sending Message to Claude Code" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "From: $Author" -ForegroundColor Yellow
Write-Host "Message: $Message" -ForegroundColor Yellow
Write-Host ""

# Path to Python script
$ScriptPath = Join-Path $PSScriptRoot "BotFILES\send_to_claude_code.py"
$PythonPath = "E:\PythonProjects\PhiGEN\.venv\Scripts\python.exe"

# Check if script exists
if (-Not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

# Execute Python script to queue message
& $PythonPath $ScriptPath $Message $Author

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Message queued successfully!" -ForegroundColor Green
    Write-Host "The type_to_claude_desktop.py monitor will send it to Claude Code's window" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Failed to queue message" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Note: Make sure type_to_claude_desktop.py is running on Windows" -ForegroundColor Cyan
