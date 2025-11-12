# PXE Server Quick Start - MacBook Pro 2007

## Step-by-Step Checklist

### [ ] Phase 1: Downloads (30 mins)
1. [ ] Download Tiny PXE Server (~500 KB)
2. [ ] Download SYSLINUX 6.03 (~20 MB)
3. [ ] Download Linux Mint 21.3 MATE (~2.4 GB)
4. [ ] (Optional) Download Clonezilla (~400 MB)

**Quick command**: Run PowerShell script from `DOWNLOAD_LINKS.md`

---

### [ ] Phase 2: Extract & Setup Files (10 mins)

1. [ ] Extract Tiny PXE Server
   ```
   Extract: tftpd64.zip → E:\PythonProjects\PhiGEN\pxe_server\tftpd64\
   ```

2. [ ] Extract SYSLINUX boot files
   ```
   From syslinux-6.03.zip, copy to tftp/:
   - bios/core/pxelinux.0
   - bios/com32/elflink/ldlinux/ldlinux.c32
   - bios/com32/lib/libcom32.c32
   - bios/com32/libutil/libutil.c32
   - bios/com32/menu/vesamenu.c32
   - bios/com32/menu/menu.c32
   - bios/com32/modules/reboot.c32
   - bios/com32/modules/poweroff.c32
   ```

3. [ ] Mount Linux Mint ISO (right-click → Mount in Windows)

4. [ ] Copy boot files from mounted ISO
   ```
   From ISO drive letter (e.g., D:\):
   D:\casper\vmlinuz → E:\PythonProjects\PhiGEN\pxe_server\tftp\images\mint\vmlinuz
   D:\casper\initrd.lz → E:\PythonProjects\PhiGEN\pxe_server\tftp\images\mint\initrd.lz
   ```

5. [ ] Copy entire ISO contents for HTTP serving
   ```
   Copy everything from ISO → E:\PythonProjects\PhiGEN\pxe_server\http\mint\
   ```

---

### [ ] Phase 3: Network Configuration (5 mins)

1. [ ] Set static IP on Windows PC
   ```
   Control Panel → Network → Adapter Properties → IPv4
   IP Address: 192.168.1.10
   Subnet Mask: 255.255.255.0
   Default Gateway: 192.168.1.1
   DNS: 192.168.1.1
   ```

2. [ ] Disable Windows Firewall (temporarily) or allow:
   - UDP Port 67 (DHCP)
   - UDP Port 68 (DHCP)
   - UDP Port 69 (TFTP)
   - TCP Port 80 (HTTP - if using)

---

### [ ] Phase 4: Configure Tiny PXE Server (5 mins)

1. [ ] Run `tftpd64.exe` as Administrator

2. [ ] Configure DHCP tab:
   ```
   IP pool start address: 192.168.1.100
   Size of pool: 50
   Boot File: pxelinux.0
   WINS/DNS Server: 192.168.1.1
   Default router: 192.168.1.1
   Mask: 255.255.255.0
   ```

3. [ ] Configure TFTP tab:
   ```
   Current Directory: E:\PythonProjects\PhiGEN\pxe_server\tftp
   Server interfaces: [Select your Ethernet adapter]
   TFTP Security: None
   ```

4. [ ] Enable services (checkboxes):
   - [x] DHCP Server
   - [x] TFTP Server
   - [ ] DNS Server (leave unchecked)

5. [ ] Click "Save" in Tiny PXE

---

### [ ] Phase 5: Create PXE Menu (2 mins)

1. [ ] Create directory: `tftp\pxelinux.cfg\`

2. [ ] Create file: `tftp\pxelinux.cfg\default`

3. [ ] Paste this content:
   ```
   DEFAULT vesamenu.c32
   TIMEOUT 300
   PROMPT 0
   
   MENU TITLE PhiGEN PXE Boot - MacBook Pro Installer
   
   LABEL mint_live
       MENU LABEL Linux Mint Live
       KERNEL images/mint/vmlinuz
       APPEND initrd=images/mint/initrd.lz boot=casper fetch=http://192.168.1.10/mint/casper/filesystem.squashfs quiet splash --
   
   LABEL mint_install
       MENU LABEL Install Linux Mint
       KERNEL images/mint/vmlinuz
       APPEND initrd=images/mint/initrd.lz boot=casper fetch=http://192.168.1.10/mint/casper/filesystem.squashfs only-ubiquity quiet splash --
   
   LABEL boot_hdd
       MENU LABEL Boot from Hard Drive
       LOCALBOOT 0
   ```

---

### [ ] Phase 6: Test PXE Server (2 mins)

1. [ ] Check Tiny PXE log window shows:
   ```
   DHCP Server: Started
   TFTP Server: Started
   ```

2. [ ] Verify files exist:
   ```
   E:\PythonProjects\PhiGEN\pxe_server\tftp\pxelinux.0 ✓
   E:\PythonProjects\PhiGEN\pxe_server\tftp\images\mint\vmlinuz ✓
   E:\PythonProjects\PhiGEN\pxe_server\tftp\images\mint\initrd.lz ✓
   E:\PythonProjects\PhiGEN\pxe_server\http\mint\casper\filesystem.squashfs ✓
   ```

---

### [ ] Phase 7: Connect MacBook Pro (Physical Setup)

1. [ ] Connect Ethernet cable:
   - MacBook Pro Ethernet port → Router/Switch
   - Windows PC Ethernet port → Same Router/Switch
   - (Or direct cable if you configured crossover/auto-MDI)

2. [ ] Power on MacBook Pro

3. [ ] Immediately hold `Option (⌥)` key

4. [ ] Wait for boot options screen

5. [ ] Select **"Network"** (globe icon)

6. [ ] Watch PXE boot!

---

### [ ] Phase 8: Boot & Install (Variable time)

**If PXE boots successfully:**
1. [ ] You'll see PhiGEN PXE Boot menu
2. [ ] Select "Linux Mint Live" first (test)
3. [ ] Once in Live mode, verify everything works:
   - WiFi drivers
   - Graphics
   - Sound
   - Keyboard/trackpad

**To backup macOS first (RECOMMENDED):**
1. [ ] From PXE menu, boot Clonezilla (if you added it)
2. [ ] Create full disk image to external drive
3. [ ] Reboot to PXE menu

**To install Linux Mint:**
1. [ ] Select "Install Linux Mint" from PXE menu
2. [ ] Follow installer prompts
3. [ ] Choose installation type:
   - **Erase disk** (removes macOS)
   - **Something else** (manual partitioning, keep macOS dual-boot)

---

## Troubleshooting Quick Fixes

### MacBook Won't See Network Boot
```
1. Reset NVRAM: Hold Cmd+Opt+P+R during boot (4 chimes)
2. Check Ethernet cable is firmly connected
3. Try rebooting router
4. Verify Windows PC firewall is OFF
```

### PXE Menu Doesn't Appear
```
1. Check Tiny PXE log for errors
2. Verify pxelinux.0 exists in tftp/ folder
3. Check tftp/pxelinux.cfg/default exists
4. Restart Tiny PXE Server
```

### "Missing Operating System" Error
```
1. Check DHCP is giving correct "Boot File: pxelinux.0"
2. Verify TFTP base directory path is correct
3. Check files aren't blocked (Right-click → Properties → Unblock)
```

### Kernel Panic / Can't Find Root
```
1. Verify filesystem.squashfs path in menu
2. Check HTTP server is enabled if using http://
3. Try adding "toram" to kernel parameters
4. Use simpler fetch method: copy to TFTP instead of HTTP
```

---

## Success Indicators

✓ **Tiny PXE Server log shows**:
```
DHCP Discover from MAC:XX:XX:XX:XX:XX:XX
DHCP Offer to 192.168.1.100
TFTP Read Request: pxelinux.0
```

✓ **MacBook screen shows**:
```
PXE Boot Menu with green PhiGEN title
Options for Linux Mint Live/Install
```

✓ **After selecting Linux Mint**:
```
Linux kernel loading messages
"Loading initial ramdisk"
Linux Mint desktop appears
```

---

## Time Estimates

| Phase | Time |
|-------|------|
| Downloads | 30 mins |
| Setup | 15 mins |
| Testing | 5 mins |
| **First Boot** | **2-5 mins** |
| **Install** | **20-40 mins** |

**Total**: ~1.5 hours from zero to installed Linux Mint

---

**Ready to go?** Start with Phase 1! 🚀
