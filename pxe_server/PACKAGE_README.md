# PhiGEN PXE Server - Complete Package

Complete PXE network boot solution for installing Linux Mint 21.3 MATE on a 2007 MacBook Pro Intel running macOS 10.4.5 Tiger.

## 📦 Package Contents

This package includes everything needed for a successful PXE boot installation:

### Documentation (4 files)
- **README.md** - Quick overview and navigation
- **SETUP_GUIDE.md** - Comprehensive technical guide (7,400+ words)
- **QUICK_START.md** - Step-by-step checklist format
- **DOWNLOAD_LINKS.md** - Download URLs and checksums
- **PACKAGE_README.md** - This file

### PowerShell Scripts (3 files)
- **download_isos.ps1** - Automated download of all required files
- **extract_boot_files.ps1** - Extracts boot files from ISOs
- **verify_setup.ps1** - Verifies PXE server configuration

### Post-Installation Scripts (1 file)
- **macbook_setup.sh** - Automated MacBook Pro hardware configuration

### Directory Structure
```
pxe_server/
├── README.md                       # Main overview
├── SETUP_GUIDE.md                  # Technical guide
├── QUICK_START.md                  # Step-by-step checklist
├── DOWNLOAD_LINKS.md               # Download URLs
├── PACKAGE_README.md               # This file
├── download_isos.ps1               # Download script
├── extract_boot_files.ps1          # Extraction script
├── verify_setup.ps1                # Verification script
├── tftp/                           # TFTP boot files
│   ├── pxelinux.0                  # PXE bootloader
│   ├── ldlinux.c32                 # SYSLINUX library
│   ├── libutil.c32                 # Utility library
│   ├── vesamenu.c32                # Menu module
│   ├── libcom32.c32                # COM32 library
│   ├── pxelinux.cfg/
│   │   └── default                 # PXE menu config
│   └── images/
│       ├── mint/                   # Linux Mint boot files
│       │   ├── vmlinuz             # Kernel
│       │   └── initrd.lz           # Initial ramdisk
│       └── clonezilla/             # Clonezilla boot files (optional)
│           ├── vmlinuz
│           ├── initrd.img
│           └── filesystem.squashfs
├── http/                           # HTTP/NFS root filesystem
│   └── mint/                       # Linux Mint root filesystem
│       └── casper/
│           └── filesystem.squashfs
├── isos/                           # Downloaded ISO files
│   ├── linuxmint-21.3-mate-64bit.iso
│   └── clonezilla-live-3.1.3-5-amd64.iso (optional)
├── tftpd64/                        # Tiny PXE Server
│   ├── tftpd64.exe
│   └── [extracted files]
├── winnfsd/                        # WinNFSd (optional)
│   └── WinNFSd.exe
├── syslinux/                       # SYSLINUX (extracted)
│   └── syslinux-6.03/
└── post_install_scripts/           # Post-installation
    └── macbook_setup.sh            # MacBook hardware setup
```

## 🚀 Quick Start (5 Steps)

### Step 1: Run Download Script
```powershell
cd E:\PythonProjects\PhiGEN\pxe_server
.\download_isos.ps1
```
Downloads all required files (Tiny PXE Server, SYSLINUX, Linux Mint ISO, optional Clonezilla)

**Time:** 10-30 minutes (depends on internet speed)

### Step 2: Extract Boot Files
```powershell
.\extract_boot_files.ps1
```
Extracts boot files from ISOs and creates PXE menu

**Time:** 5-10 minutes

### Step 3: Verify Setup
```powershell
.\verify_setup.ps1
```
Verifies all files are in place and checks network configuration

**Time:** 1 minute

### Step 4: Configure Network
```
Control Panel → Network → Adapter Properties → IPv4
├── IP Address: 192.168.1.10
├── Subnet Mask: 255.255.255.0
├── Default Gateway: 192.168.1.1
└── DNS: 192.168.1.1
```

### Step 5: Start PXE Server
```
Run: E:\PythonProjects\PhiGEN\pxe_server\tftpd64\tftpd64.exe

Configure Tiny PXE Server:
├── DHCP Tab:
│   ├── IP pool starting address: 192.168.1.100
│   ├── Size of pool: 50
│   ├── Boot File: pxelinux.0
│   ├── Mask: 255.255.255.0
│   ├── Default Gateway: 192.168.1.1
│   └── DNS Server: 192.168.1.1
├── TFTP Tab:
│   ├── TFTP Server: Enabled
│   └── Base Directory: E:\PythonProjects\PhiGEN\pxe_server\tftp
└── Click "Start" on both DHCP and TFTP
```

## 🖥️ Boot MacBook Pro

### Physical Setup
1. Connect MacBook Pro to same network as PXE server (Ethernet cable)
2. Power on MacBook Pro
3. Immediately hold **Option (⌥) key** during boot
4. Wait for boot menu (shows available boot devices)
5. Select **Network Boot** (globe icon with arrows)
6. Wait for PXE menu to load

### PXE Menu Options
- **Option 1:** Linux Mint Live Session (try before installing)
- **Option 2:** Linux Mint Install to Hard Drive (direct install)
- **Option 3:** Linux Mint Safe Graphics Mode (if display issues)
- **Option 4:** Clonezilla Live (backup macOS first)
- **Option 9:** Boot from Local Hard Drive (cancel)

## 📋 Post-Installation Setup

After installing Linux Mint on MacBook Pro:

### Transfer Setup Script
```bash
# From MacBook Pro (after Linux Mint installation)
scp user@192.168.1.10:E:/PythonProjects/PhiGEN/pxe_server/post_install_scripts/macbook_setup.sh ~/

# Or use USB drive to copy the file
```

### Run Setup Script
```bash
chmod +x ~/macbook_setup.sh
./macbook_setup.sh
```

This script automatically installs and configures:
- ✓ MacBook-specific drivers (WiFi, touchpad, webcam, sensors)
- ✓ Graphics drivers (Intel/NVIDIA)
- ✓ Audio configuration (fixes MacBook audio quirks)
- ✓ Power management (TLP, laptop-mode for battery life)
- ✓ Development tools (Python, Node.js, VS Code)
- ✓ Multimedia codecs (all formats supported)
- ✓ Useful applications (GIMP, LibreOffice, VLC, etc.)
- ✓ Mac-like fonts and tweaks
- ✓ System optimizations for 2007 hardware
- ✓ Networking tools (SSH, Samba, Avahi)
- ✓ MacBook-specific fixes (keyboard, trackpad, function keys)

**Time:** 20-30 minutes

### Reboot
```bash
sudo reboot
```

## 🔧 Troubleshooting

### MacBook Won't Network Boot

**Solution 1: Reset NVRAM**
```
1. Power off MacBook
2. Hold: Command (⌘) + Option (⌥) + P + R
3. Power on while holding keys
4. Wait for startup sound (2-3 times)
5. Release keys
6. Try booting again with Option key
```

**Solution 2: Check Network Cable**
- Ensure Ethernet cable is properly connected
- Try different Ethernet cable if available
- Check network switch/router is powered on

**Solution 3: Verify PXE Server**
```powershell
# Run verification script
.\verify_setup.ps1

# Check if tftpd64 is running
Get-Process -Name "tftpd64"

# Check network configuration
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -eq "192.168.1.10" }
```

### PXE Menu Loads But Hangs

**Cause:** NFS root filesystem not accessible

**Solution:**
```
Option 1: Use WinNFSd
1. Download WinNFSd: .\download_isos.ps1
2. Run: E:\PythonProjects\PhiGEN\pxe_server\winnfsd\WinNFSd.exe
3. Export: E:\PythonProjects\PhiGEN\pxe_server\http\mint

Option 2: Use HTTP Boot (edit pxelinux.cfg/default)
Replace: netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint
With: netboot=url url=http://192.168.1.10/mint
```

### WiFi Not Working After Install

**Cause:** Broadcom WiFi drivers need installation

**Solution:**
```bash
# The macbook_setup.sh script handles this, but if manual install needed:
sudo apt update
sudo apt install bcmwl-kernel-source broadcom-sta-dkms
sudo modprobe -r b43 ssb wl
sudo modprobe wl
sudo reboot
```

### Screen Brightness Not Adjustable

**Cause:** Function keys need configuration

**Solution:**
```bash
# Already fixed in macbook_setup.sh, but if manual fix needed:
echo "options hid_apple fnmode=2" | sudo tee /etc/modprobe.d/hid_apple.conf
sudo update-initramfs -u
sudo reboot
```

### Battery Not Detected

**Cause:** Battery is old or ACPI issue

**Solution:**
```bash
# Check battery status
upower -i /org/freedesktop/UPower/devices/battery_BAT0

# If no battery found, try:
sudo apt install acpi-support laptop-mode-tools
sudo systemctl enable laptop-mode
sudo reboot
```

## 📊 File Size Reference

| File | Size | Download Time (10 Mbps) |
|------|------|------------------------|
| Tiny PXE Server | 500 KB | 5 seconds |
| SYSLINUX 6.03 | 20 MB | 15 seconds |
| Linux Mint 21.3 MATE ISO | 2.4 GB | 30 minutes |
| Clonezilla Live ISO | 400 MB | 5 minutes |
| WinNFSd | 200 KB | 2 seconds |

**Total download:** ~2.8 GB

## 🔐 Security Notes

### Backup macOS Before Installing
1. Boot Clonezilla from PXE menu (Option 4)
2. Create full disk image to external drive
3. Verify backup before proceeding with Linux Mint install

### Post-Installation Security
```bash
# Enable firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow from 192.168.1.0/24

# Keep system updated
sudo apt update && sudo apt upgrade

# Create backups with Timeshift (installed by macbook_setup.sh)
sudo timeshift --create --comments "Initial Linux Mint install"
```

## 📚 Additional Resources

### Official Documentation
- Linux Mint: https://linuxmint.com/documentation.php
- PXE Boot: https://wiki.syslinux.org/wiki/index.php?title=PXELINUX
- MacBook Linux: https://help.ubuntu.com/community/MacBookPro

### Troubleshooting Guides
- See SETUP_GUIDE.md Section 8: Troubleshooting
- See QUICK_START.md Phase 8: Common Issues

### Community Support
- Linux Mint Forums: https://forums.linuxmint.com/
- MacBook Linux Wiki: https://wiki.archlinux.org/title/MacBookPro

## 📝 License

This package is part of the PhiGEN project and is provided as-is for educational and personal use.

## ✨ Credits

**PhiGEN PXE Server Package**
- Created for 2007 MacBook Pro Intel (macOS 10.4.5 Tiger → Linux Mint 21.3 MATE)
- Includes automated setup scripts and comprehensive documentation
- Optimized for old hardware with power management and performance tweaks

---

**Need help?** See SETUP_GUIDE.md for detailed instructions or QUICK_START.md for step-by-step checklist.
