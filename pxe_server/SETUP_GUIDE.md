# Tiny PXE Server Setup - 2007 MacBook Pro Intel to Linux Mint

## Target Hardware
- **Device**: 2007 MacBook Pro (Intel Core 2 Duo)
- **Current OS**: macOS 10.4.5 Tiger
- **Target OS**: Linux Mint (latest compatible version)
- **Boot Type**: EFI/BIOS hybrid (Intel Mac supports both)

---

## Prerequisites

### 1. Download Tiny PXE Server
- URL: https://erwan.labalec.fr/tinypxeserver/
- Download: `tftpd64.464.zip` (64-bit Windows version)
- Extract to: `E:\PythonProjects\PhiGEN\pxe_server\tftpd64\`

### 2. Download Linux Mint ISO
For 2007 MacBook Pro, use **Linux Mint 32-bit or 64-bit** depending on model:
- **Most 2007 MacBook Pros**: Core 2 Duo (64-bit capable)
- **Recommended**: Linux Mint 21.x MATE or Xfce (lighter for old hardware)
- Download from: https://linuxmint.com/download.php
- Place ISO in: `E:\PythonProjects\PhiGEN\pxe_server\isos\`

### 3. Extract Boot Files from ISO
You'll need:
- `vmlinuz` (Linux kernel)
- `initrd.lz` or `initrd.img` (initial ramdisk)
- `filesystem.squashfs` (root filesystem)

---

## Step-by-Step Setup

### Step 1: Install/Extract Tiny PXE Server

1. Extract `tftpd64.464.zip` to `pxe_server\tftpd64\`
2. Run `tftpd64.exe` as Administrator

### Step 2: Configure Tiny PXE Server

**DHCP Settings:**
```
IP pool start address: 192.168.1.100
Size of pool: 50
Boot File: pxelinux.0
WINS/DNS Server: 192.168.1.1 (your router)
Default router: 192.168.1.1
Mask: 255.255.255.0
```

**TFTP Settings:**
```
Base Directory: E:\PythonProjects\PhiGEN\pxe_server\tftp
Server interfaces: [Your network adapter]
TFTP Security: None
```

**Enable Services:**
- [x] DHCP Server
- [x] TFTP Server
- [ ] DNS Server (optional)
- [x] HTTP Server (for serving ISO files)

### Step 3: Get PXE Boot Files

Download SYSLINUX (provides pxelinux.0):
```bash
# Download from: https://kernel.org/pub/linux/utils/boot/syslinux/
# Or use these files:
```

You need these files in `tftp/`:
- `pxelinux.0` (PXE bootloader)
- `ldlinux.c32` (core library)
- `libcom32.c32`
- `libutil.c32`
- `vesamenu.c32` (for graphical menu)
- `menu.c32` (for text menu)

### Step 4: Extract Linux Mint Boot Files

Mount the ISO and copy:
```
From ISO: /casper/vmlinuz → tftp/images/mint/vmlinuz
From ISO: /casper/initrd.lz → tftp/images/mint/initrd.lz
```

### Step 5: Create PXE Menu Configuration

Create `tftp/pxelinux.cfg/default`:
```
DEFAULT vesamenu.c32
TIMEOUT 300
ONTIMEOUT mint_live
PROMPT 0

MENU TITLE PhiGEN PXE Boot - MacBook Pro Linux Mint Installer
MENU BACKGROUND pxelinux.cfg/splash.png
MENU COLOR screen 37;40 #80ffffff #00000000 std
MENU COLOR border 30;44 #40000000 #00000000 std
MENU COLOR title 1;36;44 #c00090f0 #00000000 std
MENU COLOR unsel 37;44 #90ffffff #00000000 std
MENU COLOR hotkey 1;37;44 #ffffffff #00000000 std
MENU COLOR sel 7;37;40 #e0000000 #20ff8000 all
MENU COLOR hotsel 1;7;37;40 #e0400000 #20ff8000 all
MENU COLOR scrollbar 30;44 #40000000 #00000000 std

LABEL mint_live
    MENU LABEL ^1) Linux Mint Live (Default)
    KERNEL images/mint/vmlinuz
    APPEND initrd=images/mint/initrd.lz boot=casper netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint quiet splash --

LABEL mint_install
    MENU LABEL ^2) Linux Mint Install to Hard Drive
    KERNEL images/mint/vmlinuz
    APPEND initrd=images/mint/initrd.lz boot=casper netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint only-ubiquity quiet splash --

LABEL clonezilla
    MENU LABEL ^3) Clonezilla (Backup macOS First!)
    KERNEL images/clonezilla/vmlinuz
    APPEND initrd=images/clonezilla/initrd.img boot=live union=overlay username=user config components quiet noswap edd=on nomodeset nodmraid noeject locales= keyboard-layouts= ocs_live_run="ocs-live-general" ocs_live_extra_param="" ocs_live_batch=no net.ifnames=0 nosplash noprompt fetch=tftp://192.168.1.10/images/clonezilla/filesystem.squashfs

LABEL boot_hdd
    MENU LABEL ^4) Boot from Hard Drive
    LOCALBOOT 0

LABEL reboot
    MENU LABEL ^5) Reboot
    COM32 reboot.c32

LABEL poweroff
    MENU LABEL ^6) Power Off
    COM32 poweroff.c32
```

### Step 6: Set Up HTTP/NFS for Filesystem

**Option A: Use Tiny PXE HTTP Server**
1. Copy entire ISO contents to `http/mint/`
2. In PXE config, use: `fetch=http://192.168.1.10:69/mint/casper/filesystem.squashfs`

**Option B: Use NFS (Better for Mac)**
1. Install WinNFSd: https://github.com/winnfsd/winnfsd
2. Share `http/mint/` via NFS
3. Use `nfsroot=` in kernel parameters

---

## MacBook Pro Boot Process

### Boot to Network on MacBook Pro:

1. **Power on** while holding `Option (⌥)` key
2. You should see boot options including **Network**
3. Select **Network** (globe icon)
4. Mac will attempt PXE boot
5. Should load PXE menu

### If Network Boot Doesn't Appear:

**Enable Network Boot in Firmware:**
1. Boot into macOS 10.4.5
2. Open **System Preferences** → **Startup Disk**
3. Click **Network Startup** (if available)
4. Or use **Open Firmware**:
   - Restart, hold `Command+Option+O+F`
   - Type: `setenv boot-device enet:bootp`
   - Type: `boot`

---

## Backup Strategy (CRITICAL!)

### Before Installing Linux Mint:

**Option 1: Clonezilla via PXE**
1. Boot Clonezilla from PXE menu
2. Create full disk image to network share
3. Save to external drive

**Option 2: Time Machine Backup**
1. Boot into macOS 10.4.5
2. Connect external FireWire/USB drive
3. Use built-in backup or `dd` command

**Option 3: Manual Backup**
1. Boot from Linux Mint Live
2. Use `dd` to clone entire disk:
   ```bash
   sudo dd if=/dev/sda of=/mnt/backup/macbook_2007.img bs=4M status=progress
   ```

---

## Network Configuration

**Your Server (Windows PC running PXE):**
- IP: `192.168.1.10` (static, set this in Windows)
- Subnet: `255.255.255.0`
- Gateway: `192.168.1.1`

**DHCP Pool for Clients:**
- Range: `192.168.1.100` - `192.168.1.150`

**MacBook Pro (will get from DHCP):**
- Will receive IP in range `192.168.1.100-150`

---

## Troubleshooting

### PXE Boot Fails:
- Check firewall (allow UDP 67, 68, 69)
- Verify DHCP not conflicting with router
- Try direct Ethernet connection
- Check MAC is in EFI mode, not BIOS

### Kernel Panic / Can't Find Filesystem:
- Verify `filesystem.squashfs` path
- Check HTTP/NFS server is running
- Try `toram` kernel parameter to load entirely to RAM

### Mac Won't See Network Boot:
- Reset NVRAM: Hold `Command+Option+P+R` during boot
- Check Ethernet cable is connected
- Try different Ethernet port on Mac (if applicable)

---

## Quick Reference Commands

**Mount ISO in Linux/WSL:**
```bash
sudo mkdir /mnt/iso
sudo mount -o loop linuxmint.iso /mnt/iso
cp /mnt/iso/casper/vmlinuz pxe_server/tftp/images/mint/
cp /mnt/iso/casper/initrd.lz pxe_server/tftp/images/mint/
sudo umount /mnt/iso
```

**Test PXE Server:**
```bash
# From another Linux machine
sudo nmap -sU -p 67,68,69 192.168.1.10
```

**Set Static IP on Windows:**
```
Control Panel → Network → Adapter Settings → IPv4 Properties
IP: 192.168.1.10
Subnet: 255.255.255.0
Gateway: 192.168.1.1
DNS: 192.168.1.1
```

---

## Recommended Linux Mint Version

For 2007 MacBook Pro (Core 2 Duo):
- **Best**: Linux Mint 21.x MATE Edition (lightweight)
- **Alternative**: Linux Mint Xfce (even lighter)
- **Not Recommended**: Cinnamon (too heavy for 2007 hardware)

**Specs to Consider:**
- RAM: Likely 2GB (upgrade to 4GB if possible!)
- GPU: Intel GMA X3100 or NVIDIA GeForce (works well with Linux)
- WiFi: Broadcom (may need proprietary drivers)

---

**Created by**: PhiGEN PXE Boot System
**Target**: 2007 MacBook Pro Intel → Linux Mint
**Status**: Ready for deployment
