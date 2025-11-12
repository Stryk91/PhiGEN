# PhiGEN PXE Server - Installation Summary

Complete package for installing Linux Mint 21.3 MATE on 2007 MacBook Pro Intel via PXE network boot.

## 📦 Complete Package Contents

### ✅ Documentation (6 files)
- [README.md](README.md) - Quick overview and navigation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive 7,400+ word technical guide
- [QUICK_START.md](QUICK_START.md) - Step-by-step checklist (8 phases)
- [DOWNLOAD_LINKS.md](DOWNLOAD_LINKS.md) - All download URLs with checksums
- [PACKAGE_README.md](PACKAGE_README.md) - Complete package documentation
- [INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md) - This file

### ✅ Automated Scripts (4 files)

#### Windows PowerShell Scripts
1. **download_isos.ps1** (9.6 KB)
   - Downloads Tiny PXE Server (500 KB)
   - Downloads SYSLINUX 6.03 (20 MB)
   - Downloads Linux Mint 21.3 MATE ISO (2.4 GB)
   - Downloads Clonezilla Live (400 MB, optional)
   - Downloads WinNFSd (200 KB, optional)
   - Auto-extracts and organizes all files
   - Estimated time: 10-30 minutes

2. **extract_boot_files.ps1** (14 KB)
   - Mounts ISOs automatically
   - Extracts vmlinuz and initrd from Linux Mint
   - Extracts Clonezilla boot files (optional)
   - Copies root filesystem to HTTP directory
   - Creates PXE boot menu automatically
   - Estimated time: 5-10 minutes

3. **verify_setup.ps1** (13 KB)
   - Verifies all required files exist
   - Checks network configuration (192.168.1.10)
   - Checks if Tiny PXE Server is running
   - Validates firewall rules for TFTP/DHCP
   - Provides detailed error/warning messages
   - Estimated time: 1 minute

4. **SETUP_PXE.bat** (8.1 KB)
   - Interactive menu launcher
   - One-click access to all scripts
   - Opens network adapter settings
   - Starts Tiny PXE Server
   - Quick access to documentation

#### Linux Post-Installation Script
1. **macbook_setup.sh** (11.8 KB)
   - Installs MacBook-specific drivers (WiFi, touchpad, webcam)
   - Configures audio for MacBook chipset
   - Sets up power management (TLP, laptop-mode)
   - Installs development tools (Python, Node.js, VS Code)
   - Installs multimedia codecs (all formats)
   - Applies MacBook-specific fixes (keyboard, trackpad, function keys)
   - Optimizes for 2007 hardware
   - Creates system info script
   - Estimated time: 20-30 minutes

## 🚀 Usage Instructions

### Method 1: Interactive Launcher (Recommended)
```batch
E:\PythonProjects\PhiGEN\pxe_server\SETUP_PXE.bat
```
Follow the on-screen menu to:
1. Download all required files
2. Extract boot files
3. Verify configuration
4. Start PXE server
5. Configure network

### Method 2: Manual PowerShell Commands
```powershell
# Step 1: Download everything
cd E:\PythonProjects\PhiGEN\pxe_server
.\download_isos.ps1

# Step 2: Extract boot files
.\extract_boot_files.ps1

# Step 3: Verify setup
.\verify_setup.ps1

# Step 4: Configure network (manually)
# Control Panel → Network → Adapter Properties → IPv4
# IP: 192.168.1.10, Mask: 255.255.255.0, Gateway: 192.168.1.1

# Step 5: Start PXE server
.\tftpd64\tftpd64.exe
```

## 📋 Complete Workflow

### Phase 1: Prepare PXE Server (Windows PC)
**Time: 15-45 minutes**

1. Run `SETUP_PXE.bat` or `download_isos.ps1`
2. Run `extract_boot_files.ps1`
3. Run `verify_setup.ps1` to check everything
4. Configure network adapter to 192.168.1.10
5. Start Tiny PXE Server (`tftpd64.exe`)
6. Verify DHCP and TFTP are running

**Result:** PXE server ready to boot MacBook Pro

### Phase 2: Boot MacBook Pro
**Time: 5-10 minutes**

1. Connect MacBook Pro to network (Ethernet cable)
2. Power on MacBook Pro
3. Hold **Option (⌥) key** immediately
4. Wait for boot menu
5. Select **Network Boot** (globe icon)
6. Wait for PXE menu to load

**Result:** MacBook boots to PXE menu

### Phase 3: Choose Installation Method
**Time: Variable**

**Option A: Try Before Installing (Recommended)**
- Select **Option 1: Linux Mint Live Session**
- Test WiFi, audio, trackpad, display
- Run installer from desktop when ready
- Time: 10-60 minutes

**Option B: Direct Installation**
- Select **Option 2: Linux Mint Install to Hard Drive**
- Follow installation wizard
- Time: 20-40 minutes

**Option C: Backup macOS First**
- Select **Option 4: Clonezilla Live**
- Create full disk backup to external drive
- Reboot and try Option A or B
- Time: 30-90 minutes (depends on disk size)

**Result:** Linux Mint installed on MacBook Pro

### Phase 4: Post-Installation Setup
**Time: 20-30 minutes**

1. Transfer `macbook_setup.sh` to MacBook Pro:
   ```bash
   # Using USB drive (easiest)
   cp /media/usb/macbook_setup.sh ~/

   # Or using SCP
   scp user@192.168.1.10:E:/PythonProjects/PhiGEN/pxe_server/post_install_scripts/macbook_setup.sh ~/
   ```

2. Run the setup script:
   ```bash
   chmod +x ~/macbook_setup.sh
   ./macbook_setup.sh
   ```

3. Reboot:
   ```bash
   sudo reboot
   ```

**Result:** MacBook Pro fully configured and optimized for Linux Mint

## 📊 What Gets Installed by macbook_setup.sh

### Section 1: Essential System Tools
- build-essential, linux-headers, DKMS
- git, curl, wget, htop, neofetch
- TLP, powertop, laptop-mode-tools
- cpufrequtils, thermald

### Section 2: MacBook-Specific Drivers
- **WiFi:** bcmwl-kernel-source, broadcom-sta-dkms, b43-fwcutter
- **Touchpad:** xserver-xorg-input-synaptics, libinput
- **Webcam:** isight-firmware-tools
- **Sensors:** macfanctld, pommed

### Section 3: Graphics & Display
- Intel: mesa-utils, xserver-xorg-video-intel
- NVIDIA: nvidia-340 (optional, for GeForce 8600M GT)
- Brightness control: xbacklight, brightnessctl

### Section 4: Audio
- PulseAudio, pavucontrol, alsa-utils
- Bluetooth audio support
- MacBook audio quirk fixes (model=mbp3)

### Section 5: Power Management
- TLP (battery optimization)
- laptop-mode-tools (power saving)
- CPU frequency scaling
- Thermal management

### Section 6: Development Tools
- Python 3 (with pip and venv)
- Node.js and npm
- VS Code
- Vim, nano, git-gui, meld

### Section 7: Multimedia & Codecs
- ubuntu-restricted-extras
- mint-meta-codecs
- FFmpeg, VLC
- DVD playback support

### Section 8: Useful Applications
- Timeshift (system snapshots)
- GParted (disk management)
- GIMP (image editing)
- Inkscape (vector graphics)
- Audacity (audio editing)
- LibreOffice (office suite)
- Firefox, Thunderbird

### Section 9: Mac-like Tweaks
- Apple emoji fonts
- Noto fonts
- Microsoft core fonts
- Liberation fonts

### Section 10: Hardware Optimizations
- Reduce swappiness (vm.swappiness=10)
- Disable unnecessary services (Bluetooth, CUPS)
- Preload for faster app launches

### Section 11: Networking
- OpenSSH server
- Samba (Windows file sharing)
- Avahi (Bonjour equivalent)
- Network Manager

### Section 12: Cleanup
- Remove unnecessary packages
- Clean package cache

### Section 13: MacBook-Specific Fixes
- Keyboard layout (Mac keyboard model)
- Tap-to-click trackpad configuration
- Function keys (F1-F12 work as F-keys, not special functions)
- Three-finger tap for middle click

### Section 14: System Info Script
- Creates `~/macbook_info.sh` for quick hardware status
- Shows CPU, RAM, graphics, WiFi, battery, temperature

## 🎯 Expected Results

### After PXE Boot
- MacBook Pro boots to PXE menu in ~30 seconds
- Network boot icon appears in boot menu
- PXE menu shows Linux Mint and Clonezilla options
- Live session boots in 2-3 minutes

### After Linux Mint Installation
- Clean Linux Mint 21.3 MATE installation
- All partitions properly configured
- GRUB bootloader installed
- System boots in 30-60 seconds

### After Post-Installation Script
- ✅ WiFi working (Broadcom driver installed)
- ✅ Trackpad working (multitouch gestures)
- ✅ Webcam working (iSight firmware loaded)
- ✅ Audio working (speakers, headphones, microphone)
- ✅ Brightness control working (Fn+F1/F2)
- ✅ Battery reporting working (TLP configured)
- ✅ Function keys working (Fn+F1-F12)
- ✅ Keyboard layout correct (Mac keyboard)
- ✅ Power management optimized (3-4 hours battery)
- ✅ System responsive (optimized for Core 2 Duo)

## 🔧 Troubleshooting Quick Reference

### Problem: MacBook won't network boot
**Solution:** Reset NVRAM (Cmd+Opt+P+R during boot)

### Problem: PXE menu hangs on boot
**Solution:** Check NFS/HTTP server is accessible, try HTTP boot instead

### Problem: WiFi not working after install
**Solution:** Run `macbook_setup.sh` (installs Broadcom drivers)

### Problem: Brightness not adjustable
**Solution:** Run `macbook_setup.sh` (fixes function keys)

### Problem: Trackpad not sensitive enough
**Solution:** Run `macbook_setup.sh` (configures Synaptics)

### Problem: No audio
**Solution:** Run `macbook_setup.sh` (fixes MacBook audio model)

### Problem: Poor battery life
**Solution:** Run `macbook_setup.sh` (installs TLP + laptop-mode)

### Problem: System slow
**Solution:** Run `macbook_setup.sh` (optimizes for old hardware)

## 📚 Documentation Reference

| Document | Purpose | Length | When to Use |
|----------|---------|--------|-------------|
| README.md | Quick overview | 1 page | First read |
| QUICK_START.md | Step-by-step checklist | 3 pages | During setup |
| SETUP_GUIDE.md | Technical details | 30 pages | Troubleshooting |
| DOWNLOAD_LINKS.md | Download URLs | 2 pages | Manual downloads |
| PACKAGE_README.md | Complete guide | 12 pages | Reference |
| INSTALLATION_SUMMARY.md | Overview | This file | Planning |

## 🎓 Key Technical Concepts

### PXE Boot Process
1. MacBook sends DHCP discover
2. PXE server responds with IP + boot file
3. MacBook downloads pxelinux.0 via TFTP
4. pxelinux.0 loads menu (vesamenu.c32)
5. Menu loads kernel (vmlinuz) and initrd
6. Kernel boots with root filesystem over NFS/HTTP

### Network Configuration
- **PXE Server IP:** 192.168.1.10 (static)
- **DHCP Pool:** 192.168.1.100-150
- **Subnet:** 255.255.255.0
- **Gateway:** 192.168.1.1
- **Protocols:** DHCP (67-68), TFTP (69), NFS (2049), HTTP (80)

### MacBook Hardware (2007 Model)
- **CPU:** Intel Core 2 Duo (2.2-2.4 GHz, 64-bit)
- **RAM:** 2-4 GB DDR2
- **Graphics:** Intel GMA X3100 or NVIDIA GeForce 8600M GT
- **WiFi:** Broadcom BCM4328 (requires proprietary driver)
- **Display:** 15" or 17" (1440x900 or 1680x1050)
- **Ports:** 2-3 USB 2.0, FireWire 400/800, Ethernet, Audio

### Linux Mint 21.3 MATE
- **Base:** Ubuntu 22.04 LTS
- **Kernel:** 5.15 LTS
- **Desktop:** MATE 1.26 (lightweight, good for old hardware)
- **Support:** Until 2027 (5 years)
- **Size:** 2.4 GB ISO, ~8 GB installed

## 🏁 Success Checklist

### PXE Server Setup ✅
- [ ] Downloaded all files (Tiny PXE, SYSLINUX, Linux Mint)
- [ ] Extracted boot files to TFTP directory
- [ ] Created PXE menu (pxelinux.cfg/default)
- [ ] Configured network adapter (192.168.1.10)
- [ ] Started Tiny PXE Server (DHCP + TFTP)
- [ ] Verified setup with verify_setup.ps1

### MacBook Boot ✅
- [ ] Connected MacBook to network (Ethernet)
- [ ] Booted MacBook holding Option key
- [ ] Selected Network Boot (globe icon)
- [ ] PXE menu loaded successfully
- [ ] Selected Linux Mint option

### Linux Mint Installation ✅
- [ ] Booted to live session
- [ ] Tested hardware (WiFi, audio, display)
- [ ] Ran installer from desktop
- [ ] Partitioned disk (auto or manual)
- [ ] Completed installation
- [ ] Removed installation media
- [ ] Rebooted into Linux Mint

### Post-Installation Setup ✅
- [ ] Transferred macbook_setup.sh to MacBook
- [ ] Made script executable (chmod +x)
- [ ] Ran macbook_setup.sh
- [ ] Rebooted MacBook
- [ ] Verified WiFi working
- [ ] Verified audio working
- [ ] Verified trackpad working
- [ ] Verified brightness control working
- [ ] Verified battery reporting
- [ ] Updated system (apt update && apt upgrade)
- [ ] Created backup with Timeshift

## 🎉 Final Result

**You now have:**
- 2007 MacBook Pro running Linux Mint 21.3 MATE
- All hardware fully functional (WiFi, audio, webcam, sensors)
- Optimized for old hardware (battery life, performance)
- Modern software (Python, Node.js, VS Code, LibreOffice)
- Supported until 2027 (5 more years of updates)
- Mac-like experience (keyboard, trackpad, fonts)

**Performance expectations:**
- Boot time: 30-60 seconds
- Login time: 5-10 seconds
- App launch: 2-5 seconds
- Battery life: 3-4 hours (depends on usage)
- RAM usage: 800 MB idle (out of 2-4 GB)
- Disk usage: 8-10 GB (out of 120-250 GB)

**Enjoy your refreshed MacBook Pro! 🚀**

---

**Package created by:** PhiGEN Project
**Target hardware:** 2007 MacBook Pro Intel (macOS 10.4.5 Tiger)
**Target OS:** Linux Mint 21.3 MATE Edition (64-bit)
**Package version:** 1.0
**Last updated:** November 2025

**Questions?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.
