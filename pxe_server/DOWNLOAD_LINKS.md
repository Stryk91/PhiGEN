# PXE Server Required Downloads

## 1. Tiny PXE Server (REQUIRED)
**What**: Lightweight PXE/TFTP/DHCP server for Windows
**URL**: https://erwan.labalec.fr/tinypxeserver/
**File**: `tftpd64.464.zip` (about 500 KB)
**Extract to**: `E:\PythonProjects\PhiGEN\pxe_server\tftpd64\`

Direct download: https://download.sourceforge.net/project/tftpd64/tftpd64_se/tftpd64_se_464.zip

---

## 2. SYSLINUX (PXE Bootloader Files)
**What**: PXE bootloader (pxelinux.0 and libraries)
**URL**: https://kernel.org/pub/linux/utils/boot/syslinux/
**Version**: 6.03 (stable)
**File**: `syslinux-6.03.zip`

Direct download: https://kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.zip

**Files you need from the ZIP** (extract to `tftp/`):
```
bios/core/pxelinux.0
bios/com32/elflink/ldlinux/ldlinux.c32
bios/com32/lib/libcom32.c32
bios/com32/libutil/libutil.c32
bios/com32/menu/vesamenu.c32
bios/com32/menu/menu.c32
bios/com32/modules/reboot.c32
bios/com32/modules/poweroff.c32
```

---

## 3. Linux Mint ISO
**What**: Operating system to install on MacBook Pro
**URL**: https://linuxmint.com/download.php

### Recommended for 2007 MacBook Pro:
**Linux Mint 21.3 MATE Edition (64-bit)**
- Size: ~2.4 GB
- Desktop: MATE (lightweight, perfect for old hardware)
- Support: Until 2027

Direct link: https://mirrors.layeronline.com/linuxmint/stable/21.3/linuxmint-21.3-mate-64bit.iso

**Alternative (Even Lighter):**
**Linux Mint 21.3 Xfce Edition**
- Direct link: https://mirrors.layeronline.com/linuxmint/stable/21.3/linuxmint-21.3-xfce-64bit.iso

**Save to**: `E:\PythonProjects\PhiGEN\pxe_server\isos\`

---

## 4. Clonezilla (OPTIONAL - For Backup)
**What**: Disk cloning/imaging tool to backup macOS before installing Linux
**URL**: https://clonezilla.org/downloads.php
**Version**: Clonezilla Live (stable)
**Architecture**: amd64 (64-bit)

Direct download: https://sourceforge.net/projects/clonezilla/files/clonezilla_live_stable/

**File**: `clonezilla-live-3.1.0-22-amd64.iso` (about 400 MB)
**Save to**: `E:\PythonProjects\PhiGEN\pxe_server\isos\`

---

## 5. WinNFSd (OPTIONAL - Better performance)
**What**: NFS server for Windows (faster than HTTP for large files)
**URL**: https://github.com/winnfsd/winnfsd/releases
**File**: `WinNFSd.exe` (portable, no install needed)
**Place in**: `E:\PythonProjects\PhiGEN\pxe_server\winnfsd\`

Direct download: https://github.com/winnfsd/winnfsd/releases/download/2.4.0/WinNFSd.exe

---

## Quick Download Script (PowerShell)

Run this in PowerShell to download everything:

```powershell
# Create directories
New-Item -ItemType Directory -Force -Path "E:\PythonProjects\PhiGEN\pxe_server\isos"
New-Item -ItemType Directory -Force -Path "E:\PythonProjects\PhiGEN\pxe_server\tftpd64"
New-Item -ItemType Directory -Force -Path "E:\PythonProjects\PhiGEN\pxe_server\winnfsd"

# Download Tiny PXE Server
Invoke-WebRequest -Uri "https://download.sourceforge.net/project/tftpd64/tftpd64_se/tftpd64_se_464.zip" -OutFile "E:\PythonProjects\PhiGEN\pxe_server\tftpd64.zip"

# Download SYSLINUX
Invoke-WebRequest -Uri "https://kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.zip" -OutFile "E:\PythonProjects\PhiGEN\pxe_server\syslinux.zip"

# Download Linux Mint (this will take a while - 2.4 GB)
Invoke-WebRequest -Uri "https://mirrors.layeronline.com/linuxmint/stable/21.3/linuxmint-21.3-mate-64bit.iso" -OutFile "E:\PythonProjects\PhiGEN\pxe_server\isos\linuxmint-21.3-mate-64bit.iso"

# Download Clonezilla (backup tool)
Invoke-WebRequest -Uri "https://sourceforge.net/projects/clonezilla/files/latest/download" -OutFile "E:\PythonProjects\PhiGEN\pxe_server\isos\clonezilla-live-latest.iso"

# Download WinNFSd
Invoke-WebRequest -Uri "https://github.com/winnfsd/winnfsd/releases/download/2.4.0/WinNFSd.exe" -OutFile "E:\PythonProjects\PhiGEN\pxe_server\winnfsd\WinNFSd.exe"

Write-Host "✓ All downloads complete!"
```

---

## Checksums (Verify Downloads)

**Linux Mint 21.3 MATE (64-bit):**
```
SHA256: 3c9a8e7fe1e371817c32b5f101c0d0db651303fd358c6d6d87a92bfa6281a5f1
```

**Verify in PowerShell:**
```powershell
Get-FileHash -Path "E:\PythonProjects\PhiGEN\pxe_server\isos\linuxmint-21.3-mate-64bit.iso" -Algorithm SHA256
```

---

## What's Next?

After downloading:
1. Extract `tftpd64.zip` to `pxe_server\tftpd64\`
2. Extract SYSLINUX files to `pxe_server\tftp\` (see list above)
3. Mount Linux Mint ISO and copy boot files (see SETUP_GUIDE.md)
4. Configure Tiny PXE Server (see SETUP_GUIDE.md)
5. Boot MacBook Pro and hold Option key!

---

**Total Download Size**: ~3.3 GB (mostly Linux Mint ISO)
**Estimated Time**: 15-30 minutes on fast connection
