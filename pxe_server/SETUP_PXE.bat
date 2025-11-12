@echo off
REM PhiGEN PXE Server - Quick Setup Launcher
REM Automated setup for MacBook Pro 2007 Linux Mint installation

color 0A
title PhiGEN PXE Server - Setup Launcher

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  PhiGEN PXE Server - Quick Setup Launcher             ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

:MENU
echo.
echo Main Menu:
echo ─────────────────────────────────────────────────────────
echo  1. Download all required files (ISOs, SYSLINUX, etc.)
echo  2. Extract boot files from ISOs
echo  3. Verify PXE server configuration
echo  4. Start Tiny PXE Server
echo  5. Open network adapter settings
echo  6. View documentation (QUICK_START.md)
echo  7. View comprehensive guide (SETUP_GUIDE.md)
echo  8. Exit
echo ─────────────────────────────────────────────────────────
echo.

set /p choice="Select option (1-8): "

if "%choice%"=="1" goto DOWNLOAD
if "%choice%"=="2" goto EXTRACT
if "%choice%"=="3" goto VERIFY
if "%choice%"=="4" goto START_SERVER
if "%choice%"=="5" goto NETWORK
if "%choice%"=="6" goto VIEW_QUICK
if "%choice%"=="7" goto VIEW_GUIDE
if "%choice%"=="8" goto EXIT

echo Invalid choice. Please try again.
goto MENU

:DOWNLOAD
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║           Downloading Required Files...               ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo This will download:
echo  - Tiny PXE Server (500 KB)
echo  - SYSLINUX 6.03 (20 MB)
echo  - Linux Mint 21.3 MATE ISO (2.4 GB)
echo  - Clonezilla Live ISO (400 MB, optional)
echo.
echo Total size: ~2.8 GB
echo Estimated time: 10-30 minutes (depends on internet speed)
echo.
pause
powershell.exe -ExecutionPolicy Bypass -File "%~dp0download_isos.ps1"
echo.
echo [Done] Press any key to return to menu...
pause >nul
goto MENU

:EXTRACT
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║         Extracting Boot Files from ISOs...            ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo This will:
echo  - Mount Linux Mint ISO
echo  - Extract vmlinuz and initrd
echo  - Copy root filesystem
echo  - Create PXE boot menu
echo.
echo Estimated time: 5-10 minutes
echo.
pause
powershell.exe -ExecutionPolicy Bypass -File "%~dp0extract_boot_files.ps1"
echo.
echo [Done] Press any key to return to menu...
pause >nul
goto MENU

:VERIFY
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║       Verifying PXE Server Configuration...           ║
echo ╚════════════════════════════════════════════════════════╝
echo.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0verify_setup.ps1"
echo.
echo [Done] Press any key to return to menu...
pause >nul
goto MENU

:START_SERVER
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║           Starting Tiny PXE Server...                 ║
echo ╚════════════════════════════════════════════════════════╝
echo.

if not exist "%~dp0tftpd64\tftpd64.exe" (
    echo [ERROR] Tiny PXE Server not found!
    echo.
    echo Please run Option 1 to download required files first.
    echo.
    pause
    goto MENU
)

echo Starting Tiny PXE Server...
echo.
echo Configure Tiny PXE Server:
echo ─────────────────────────────────────────────────────────
echo DHCP Tab:
echo   - IP pool starting address: 192.168.1.100
echo   - Size of pool: 50
echo   - Boot File: pxelinux.0
echo   - Mask: 255.255.255.0
echo   - Default Gateway: 192.168.1.1
echo   - DNS Server: 192.168.1.1
echo.
echo TFTP Tab:
echo   - TFTP Server: Enabled
echo   - Base Directory: %~dp0tftp
echo.
echo Click "Start" on both DHCP and TFTP tabs
echo ─────────────────────────────────────────────────────────
echo.
start "" "%~dp0tftpd64\tftpd64.exe"
echo.
echo Tiny PXE Server launched!
echo.
pause
goto MENU

:NETWORK
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║        Opening Network Adapter Settings...            ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Configure network adapter:
echo ─────────────────────────────────────────────────────────
echo 1. Right-click your Ethernet adapter
echo 2. Click "Properties"
echo 3. Select "Internet Protocol Version 4 (TCP/IPv4)"
echo 4. Click "Properties"
echo 5. Select "Use the following IP address"
echo 6. Enter:
echo    - IP Address: 192.168.1.10
echo    - Subnet Mask: 255.255.255.0
echo    - Default Gateway: 192.168.1.1
echo    - Preferred DNS: 192.168.1.1
echo 7. Click "OK" to save
echo ─────────────────────────────────────────────────────────
echo.
pause
control.exe ncpa.cpl
goto MENU

:VIEW_QUICK
cls
echo.
echo Opening QUICK_START.md...
echo.
if exist "%~dp0QUICK_START.md" (
    start "" "%~dp0QUICK_START.md"
) else (
    echo [ERROR] QUICK_START.md not found!
    pause
)
goto MENU

:VIEW_GUIDE
cls
echo.
echo Opening SETUP_GUIDE.md...
echo.
if exist "%~dp0SETUP_GUIDE.md" (
    start "" "%~dp0SETUP_GUIDE.md"
) else (
    echo [ERROR] SETUP_GUIDE.md not found!
    pause
)
goto MENU

:EXIT
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              Thank you for using PhiGEN!              ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo  1. Ensure Tiny PXE Server is running
echo  2. Connect MacBook Pro to network (Ethernet)
echo  3. Boot MacBook holding Option key
echo  4. Select "Network Boot" (globe icon)
echo  5. Choose Linux Mint from PXE menu
echo.
echo After installation, run macbook_setup.sh on the MacBook
echo to configure all hardware drivers and optimizations.
echo.
echo Documentation: PACKAGE_README.md
echo.
pause
exit
