@echo off
REM Send message to Claude Code (DC) via macro
REM Usage: send_message_to_dc.bat "Your message here"

if "%~1"=="" (
    echo Error: No message provided
    echo Usage: send_message_to_dc.bat "Your message here"
    exit /b 1
)

cd /d E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe -c "import time; import pyautogui; pyautogui.hotkey('win', 'r'); time.sleep(0.5); pyautogui.typewrite('DC(DESKC)', interval=0.05); pyautogui.press('enter'); time.sleep(7.5); pyautogui.write(r'%~1', interval=0.01); time.sleep(0.3); pyautogui.press('enter')"

exit /b 0
