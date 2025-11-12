# PhiGEN GUI Troubleshooting Guide

## Current Issue: GUIs Running But Not Visible

### Status
- ✅ PyQt6 6.10.0 installed
- ✅ PySide6 6.10.0 installed
- ✅ All XCB dependencies installed
- ✅ WSLg X server running (Microsoft Corporation)
- ✅ Qt applications initialize without errors
- ✅ Python processes running (verified with ps aux)
- ❌ **Windows not appearing on screen**

### Root Cause
WSLg (Windows Subsystem for Linux GUI) is configured but windows are not being forwarded to the Windows desktop properly.

## Solutions

### Solution 1: Restart WSLg (Recommended First Step)

From **Windows PowerShell** (not WSL), run:
```powershell
wsl --shutdown
```

Then restart WSL and try again:
```bash
./status_monitor.sh
```

### Solution 2: Check Windows Task Manager

1. Open Task Manager (Ctrl+Shift+Esc)
2. Look for "python.exe" processes
3. Right-click → "Bring to front" or "Switch to"
4. Windows might be minimized or on another virtual desktop

### Solution 3: Install VcXsrv (Alternative X Server)

If WSLg continues to fail:

1. Download VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Install and launch XLaunch
3. Configure:
   - Display: Multiple windows
   - Start: No client
   - Extra: ✓ Disable access control
4. In WSL, set DISPLAY:
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
   ```
5. Launch GUI:
   ```bash
   ./status_monitor.sh
   ```

### Solution 4: Use Native Windows Python (Best Performance)

Instead of fighting WSL GUI issues, run Python natively on Windows:

1. Install Python 3.11+ on Windows (not WSL)
2. Create Windows virtual environment:
   ```cmd
   cd E:\PythonProjects\PhiGEN
   python -m venv .venv-windows
   .venv-windows\Scripts\activate
   pip install PyQt6 PySide6 cryptography
   ```
3. Use the Windows batch files:
   - `RUN_STATUS_MONITOR.bat`
   - `RUN_PASSWORD_VAULT.bat`

### Solution 5: Check WSL Version

From **Windows PowerShell**:
```powershell
wsl --version
wsl --status
```

WSLg requires:
- Windows 11 or Windows 10 version 21H2+
- WSL version 0.67.6+
- WSLg version 1.0.41+

## Testing X Server Connection

### Test 1: Simple X11 App
```bash
sudo apt-get install x11-apps
xclock
```
If xclock appears, X server works.

### Test 2: Qt Test Window
```bash
source .venv/bin/activate
export QT_QPA_PLATFORM=xcb
python -c "
from PyQt6.QtWidgets import QApplication, QLabel
import sys
app = QApplication(sys.argv)
label = QLabel('PhiGEN Test Window')
label.setGeometry(100, 100, 300, 100)
label.show()
sys.exit(app.exec())
"
```

## Current Launch Scripts

### WSL/Linux (requires working WSLg)
```bash
./status_monitor.sh
./password_vault.sh
```

### From VSCode
Press F5 → Select:
- "PhiGEN Status Monitor"
- "Password Vault"

### Environment Variables Set
Both scripts now export:
```bash
export QT_QPA_PLATFORM=xcb
export DISPLAY=${DISPLAY:-:0}
```

## Known Issues

### Issue: QTextEdit vs QPlainTextEdit
**Fixed** - Changed to QPlainTextEdit for proper API compatibility

### Issue: Qt Platform Plugin Missing
**Fixed** - Added QT_QPA_PLATFORM=xcb export to all launch scripts

### Issue: MinGW Conflicts
**Not applicable** - MinGW not in PATH, no conflicts detected

## Status Monitor Code Fixes Applied

1. Line 16: Added `QPlainTextEdit` to imports
2. Line 194: Changed `QTextEdit()` to `QPlainTextEdit()`
3. Line 221: Changed `.append()` to `.appendPlainText()`

## Next Steps

1. Try Solution 1 (restart WSLg) first
2. If that fails, check Task Manager for hidden windows
3. Consider using native Windows Python for best GUI experience
