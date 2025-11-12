# PhiGEN PXE Boot Server
## Network Boot System for 2007 MacBook Pro Intel

**Purpose**: Install Linux Mint on 2007 MacBook Pro via network boot (PXE)

---

## Quick Start

**New to PXE?** Start here: [QUICK_START.md](QUICK_START.md)

**Downloads needed**: [DOWNLOAD_LINKS.md](DOWNLOAD_LINKS.md)

**Full guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## What This Does

Transform a **2007 MacBook Pro running macOS 10.4.5 Tiger** into a modern **Linux Mint** machine by:
1. Booting over the network (no USB/CD required)
2. Optionally backing up macOS first (Clonezilla)
3. Installing Linux Mint MATE Edition (lightweight, perfect for old hardware)

---

## Directory Structure

```
pxe_server/
├── README.md              ← You are here
├── QUICK_START.md         ← Step-by-step checklist
├── SETUP_GUIDE.md         ← Detailed technical guide
├── DOWNLOAD_LINKS.md      ← What to download and where
│
├── tftp/                  ← TFTP boot files (PXE)
│   ├── pxelinux.0        ← PXE bootloader
│   ├── *.c32             ← SYSLINUX libraries
│   ├── pxelinux.cfg/     ← Boot menu configuration
│   │   └── default       ← Menu config file
│   └── images/           ← OS boot kernels
│       ├── mint/         ← Linux Mint
│       │   ├── vmlinuz
│       │   └── initrd.lz
│       └── clonezilla/   ← Backup tool (optional)
│
├── http/                  ← HTTP/NFS filesystem serving
│   └── mint/             ← Full Linux Mint ISO contents
│       └── casper/
│           └── filesystem.squashfs
│
├── isos/                  ← Downloaded ISOs
│   ├── linuxmint-21.3-mate-64bit.iso
│   └── clonezilla-live-latest.iso
│
├── tftpd64/              ← Tiny PXE Server (extract here)
│   └── tftpd64.exe
│
└── winnfsd/              ← Optional NFS server
    └── WinNFSd.exe
```

---

## System Requirements

### Server (Your Windows PC):
- Windows 10/11
- Ethernet port
- 4+ GB free disk space
- Network access to MacBook

### Target (2007 MacBook Pro):
- Intel Core 2 Duo (64-bit)
- Currently running macOS 10.4.5 Tiger
- Ethernet port (or Thunderbolt adapter)
- 2+ GB RAM (4GB recommended)

---

## Key Features

✓ **No USB/CD required** - Everything over network  
✓ **Backup macOS first** - Clonezilla included  
✓ **Live mode test** - Try before installing  
✓ **Multiple OS options** - Easy to add more  
✓ **Fast deployment** - Gigabit Ethernet speeds  

---

## Boot Process Overview

```
1. MacBook powers on → Hold Option key
2. Select "Network" boot option (globe icon)
3. MacBook gets IP from DHCP (192.168.1.100-150)
4. Downloads pxelinux.0 via TFTP
5. Displays PhiGEN PXE Boot Menu
6. User selects "Linux Mint Live" or "Install"
7. Kernel + initrd load via TFTP
8. Filesystem loads via HTTP/NFS
9. Linux Mint boots!
```

---

## Network Configuration

**Server IP** (Your Windows PC):
```
IP: 192.168.1.10 (static)
Subnet: 255.255.255.0
Gateway: 192.168.1.1
```

**DHCP Pool** (MacBook will get):
```
Range: 192.168.1.100 - 192.168.1.150
```

**Required Firewall Rules**:
```
UDP 67/68  → DHCP
UDP 69     → TFTP
TCP 80     → HTTP (if using)
TCP 2049   → NFS (if using WinNFSd)
```

---

## PXE Menu Options

When MacBook boots, you'll see:

```
╔══════════════════════════════════════╗
║  PhiGEN PXE Boot - MacBook Pro       ║
╠══════════════════════════════════════╣
║  1) Linux Mint Live (Default)        ║
║  2) Linux Mint Install to Hard Drive ║
║  3) Clonezilla (Backup macOS First!) ║
║  4) Boot from Hard Drive             ║
║  5) Reboot                           ║
║  6) Power Off                        ║
╚══════════════════════════════════════╝
```

---

## Important Notes

### Before Installing Linux:
1. **BACKUP MACBOOK DATA** (use Clonezilla option)
2. Test Linux Mint in Live mode first
3. Verify WiFi/graphics/sound work
4. Decide: Erase macOS or dual-boot?

### Recommended Linux Mint Version:
- **Linux Mint 21.3 MATE** (best for 2007 hardware)
- NOT Cinnamon (too heavy)
- Xfce also good (lighter than MATE)

### MacBook Considerations:
- **WiFi**: Broadcom - may need drivers post-install
- **Graphics**: Intel GMA X3100 or NVIDIA - works great
- **Sound**: Usually works out-of-box
- **Battery**: May not report correctly (known Intel Mac issue)

---

## Troubleshooting

**Can't find downloads?**
→ See [DOWNLOAD_LINKS.md](DOWNLOAD_LINKS.md)

**MacBook won't network boot?**
→ Reset NVRAM (Cmd+Opt+P+R during boot)

**PXE menu doesn't show?**
→ Check Tiny PXE logs, verify pxelinux.0 exists

**Kernel panic?**
→ Verify filesystem.squashfs path in menu config

**Full troubleshooting**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## Support

**Created by**: PhiGEN System Tools  
**Tested on**: 2007 MacBook Pro (Core 2 Duo)  
**Target OS**: Linux Mint 21.3 MATE/Xfce  
**Last Updated**: November 2025  

---

## Quick Links

- **Tiny PXE Server**: https://erwan.labalec.fr/tinypxeserver/
- **Linux Mint**: https://linuxmint.com/download.php
- **Clonezilla**: https://clonezilla.org/downloads.php
- **SYSLINUX**: https://kernel.org/pub/linux/utils/boot/syslinux/

---

**Ready to begin?**  
→ Open [QUICK_START.md](QUICK_START.md) and follow the checklist! 🚀
