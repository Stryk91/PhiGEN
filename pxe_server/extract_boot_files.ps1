# PhiGEN PXE Server - Boot Files Extraction Script
# Extracts vmlinuz and initrd from Linux Mint and Clonezilla ISOs
# Run in PowerShell as Administrator

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  PhiGEN PXE Server - Boot Files Extraction            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Define paths
$baseDir = "E:\PythonProjects\PhiGEN\pxe_server"
$isoDir = "$baseDir\isos"
$tftpDir = "$baseDir\tftp"
$httpDir = "$baseDir\http"
$mountDir = "$baseDir\temp_mount"

$mintISO = "$isoDir\linuxmint-21.3-mate-64bit.iso"
$clonezillaISO = "$isoDir\clonezilla-live-3.1.3-5-amd64.iso"

# Create directories
Write-Host "[*] Creating directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$tftpDir\images\mint" | Out-Null
New-Item -ItemType Directory -Force -Path "$tftpDir\images\clonezilla" | Out-Null
New-Item -ItemType Directory -Force -Path "$httpDir\mint" | Out-Null
New-Item -ItemType Directory -Force -Path $mountDir | Out-Null
Write-Host "[✓] Directories created" -ForegroundColor Green

# Function to mount ISO
function Mount-ISO {
    param (
        [string]$isoPath,
        [string]$name
    )

    Write-Host ""
    Write-Host "[*] Mounting $name ISO..." -ForegroundColor Cyan

    if (-not (Test-Path $isoPath)) {
        Write-Host "[✗] ISO not found: $isoPath" -ForegroundColor Red
        return $null
    }

    try {
        $mount = Mount-DiskImage -ImagePath $isoPath -PassThru
        $driveLetter = ($mount | Get-Volume).DriveLetter
        Write-Host "[✓] Mounted at: ${driveLetter}:\" -ForegroundColor Green
        return "${driveLetter}:\"
    }
    catch {
        Write-Host "[✗] Failed to mount ISO: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Function to dismount ISO
function Dismount-ISO {
    param (
        [string]$isoPath,
        [string]$name
    )

    Write-Host "[*] Unmounting $name ISO..." -ForegroundColor Yellow
    Dismount-DiskImage -ImagePath $isoPath | Out-Null
    Write-Host "[✓] Unmounted" -ForegroundColor Green
}

# ============================================================
# EXTRACT 1: Linux Mint Boot Files
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Extracting Linux Mint Boot Files" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan

if (Test-Path $mintISO) {
    $mintMount = Mount-ISO -isoPath $mintISO -name "Linux Mint"

    if ($mintMount) {
        Write-Host "[*] Copying boot files..." -ForegroundColor Yellow

        # Copy vmlinuz and initrd
        Copy-Item "$mintMount\casper\vmlinuz" -Destination "$tftpDir\images\mint\vmlinuz"
        Copy-Item "$mintMount\casper\initrd.lz" -Destination "$tftpDir\images\mint\initrd.lz"

        Write-Host "[✓] Boot files copied to: $tftpDir\images\mint\" -ForegroundColor Green

        # Copy entire casper directory for network boot
        Write-Host "[*] Copying root filesystem (this may take several minutes)..." -ForegroundColor Yellow
        Copy-Item "$mintMount\*" -Destination "$httpDir\mint\" -Recurse -Force

        Write-Host "[✓] Root filesystem copied to: $httpDir\mint\" -ForegroundColor Green

        # Verify files
        if ((Test-Path "$tftpDir\images\mint\vmlinuz") -and (Test-Path "$tftpDir\images\mint\initrd.lz")) {
            Write-Host "[✓] Linux Mint boot files extracted successfully" -ForegroundColor Green

            $vmlinuzSize = (Get-Item "$tftpDir\images\mint\vmlinuz").Length / 1MB
            $initrdSize = (Get-Item "$tftpDir\images\mint\initrd.lz").Length / 1MB
            Write-Host "    vmlinuz: $([math]::Round($vmlinuzSize, 2)) MB" -ForegroundColor Gray
            Write-Host "    initrd.lz: $([math]::Round($initrdSize, 2)) MB" -ForegroundColor Gray
        } else {
            Write-Host "[✗] Failed to extract boot files" -ForegroundColor Red
        }

        Dismount-ISO -isoPath $mintISO -name "Linux Mint"
    }
} else {
    Write-Host "[!] Linux Mint ISO not found: $mintISO" -ForegroundColor Yellow
    Write-Host "    Run download_isos.ps1 first" -ForegroundColor Yellow
}

# ============================================================
# EXTRACT 2: Clonezilla Boot Files (Optional)
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Extracting Clonezilla Boot Files" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan

if (Test-Path $clonezillaISO) {
    $clonezillaMount = Mount-ISO -isoPath $clonezillaISO -name "Clonezilla"

    if ($clonezillaMount) {
        Write-Host "[*] Copying boot files..." -ForegroundColor Yellow

        # Copy vmlinuz and initrd
        Copy-Item "$clonezillaMount\live\vmlinuz" -Destination "$tftpDir\images\clonezilla\vmlinuz"
        Copy-Item "$clonezillaMount\live\initrd.img" -Destination "$tftpDir\images\clonezilla\initrd.img"
        Copy-Item "$clonezillaMount\live\filesystem.squashfs" -Destination "$tftpDir\images\clonezilla\filesystem.squashfs"

        Write-Host "[✓] Boot files copied to: $tftpDir\images\clonezilla\" -ForegroundColor Green

        # Verify files
        if ((Test-Path "$tftpDir\images\clonezilla\vmlinuz") -and (Test-Path "$tftpDir\images\clonezilla\initrd.img")) {
            Write-Host "[✓] Clonezilla boot files extracted successfully" -ForegroundColor Green

            $vmlinuzSize = (Get-Item "$tftpDir\images\clonezilla\vmlinuz").Length / 1MB
            $initrdSize = (Get-Item "$tftpDir\images\clonezilla\initrd.img").Length / 1MB
            $fsSize = (Get-Item "$tftpDir\images\clonezilla\filesystem.squashfs").Length / 1MB
            Write-Host "    vmlinuz: $([math]::Round($vmlinuzSize, 2)) MB" -ForegroundColor Gray
            Write-Host "    initrd.img: $([math]::Round($initrdSize, 2)) MB" -ForegroundColor Gray
            Write-Host "    filesystem.squashfs: $([math]::Round($fsSize, 2)) MB" -ForegroundColor Gray
        } else {
            Write-Host "[✗] Failed to extract boot files" -ForegroundColor Red
        }

        Dismount-ISO -isoPath $clonezillaISO -name "Clonezilla"
    }
} else {
    Write-Host "[!] Clonezilla ISO not found: $clonezillaISO" -ForegroundColor Yellow
    Write-Host "    This is optional - you can skip this" -ForegroundColor Yellow
}

# ============================================================
# CREATE PXE MENU
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Creating PXE Boot Menu" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan

$pxeMenu = @"
DEFAULT vesamenu.c32
TIMEOUT 300
ONTIMEOUT mint_live
PROMPT 0

MENU TITLE PhiGEN PXE Boot - MacBook Pro Linux Mint Installer
MENU BACKGROUND pxelinux.cfg/splash.png
MENU COLOR border 30;44 #40ffffff #a0000000 std
MENU COLOR title  1;36;44 #9033ccff #a0000000 std
MENU COLOR sel    7;37;40 #e0ffffff #20ffffff all
MENU COLOR unsel  37;44 #50ffffff #a0000000 std
MENU COLOR help   37;40 #c0ffffff #a0000000 std
MENU COLOR timeout_msg 37;40 #80ffffff #00000000 std
MENU COLOR timeout 1;37;40 #c0ffffff #00000000 std
MENU COLOR msg07  37;40 #90ffffff #a0000000 std

LABEL mint_live
    MENU LABEL ^1) Linux Mint 21.3 MATE - Live Session (Default)
    MENU DEFAULT
    KERNEL images/mint/vmlinuz
    APPEND initrd=images/mint/initrd.lz boot=casper netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint quiet splash --

LABEL mint_install
    MENU LABEL ^2) Linux Mint 21.3 MATE - Install to Hard Drive
    KERNEL images/mint/vmlinuz
    APPEND initrd=images/mint/initrd.lz boot=casper netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint only-ubiquity quiet splash --

LABEL mint_safe
    MENU LABEL ^3) Linux Mint 21.3 MATE - Safe Graphics Mode
    KERNEL images/mint/vmlinuz
    APPEND initrd=images/mint/initrd.lz boot=casper netboot=nfs nfsroot=192.168.1.10:/mnt/e/PythonProjects/PhiGEN/pxe_server/http/mint nomodeset quiet splash --
"@

if (Test-Path $clonezillaISO) {
    $pxeMenu += @"

MENU SEPARATOR

LABEL clonezilla
    MENU LABEL ^4) Clonezilla Live - Backup/Restore macOS
    KERNEL images/clonezilla/vmlinuz
    APPEND initrd=images/clonezilla/initrd.img boot=live union=overlay username=user config components quiet noswap edd=on nomodeset nodmraid noeject locales= keyboard-layouts= ocs_live_run="ocs-live-general" ocs_live_extra_param="" ocs_live_batch=no net.ifnames=0 nosplash noprompt fetch=tftp://192.168.1.10/images/clonezilla/filesystem.squashfs
"@
}

$pxeMenu += @"

MENU SEPARATOR

LABEL local
    MENU LABEL ^9) Boot from Local Hard Drive
    LOCALBOOT 0
"@

# Save PXE menu
$pxeMenuPath = "$tftpDir\pxelinux.cfg\default"
New-Item -ItemType Directory -Force -Path "$tftpDir\pxelinux.cfg" | Out-Null
$pxeMenu | Out-File -FilePath $pxeMenuPath -Encoding ASCII

Write-Host "[✓] PXE menu created: $pxeMenuPath" -ForegroundColor Green

# ============================================================
# FINAL SUMMARY
# ============================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           Boot Files Extraction Complete!             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Extracted files:" -ForegroundColor Cyan
Write-Host ""

# Check what was extracted
if (Test-Path "$tftpDir\images\mint\vmlinuz") {
    Write-Host "  [✓] Linux Mint boot files" -ForegroundColor Green
} else {
    Write-Host "  [✗] Linux Mint boot files" -ForegroundColor Red
}

if (Test-Path "$tftpDir\images\clonezilla\vmlinuz") {
    Write-Host "  [✓] Clonezilla boot files" -ForegroundColor Green
} else {
    Write-Host "  [!] Clonezilla boot files (optional)" -ForegroundColor Yellow
}

if (Test-Path "$httpDir\mint\casper") {
    Write-Host "  [✓] Linux Mint root filesystem" -ForegroundColor Green
} else {
    Write-Host "  [✗] Linux Mint root filesystem" -ForegroundColor Red
}

if (Test-Path $pxeMenuPath) {
    Write-Host "  [✓] PXE boot menu" -ForegroundColor Green
} else {
    Write-Host "  [✗] PXE boot menu" -ForegroundColor Red
}

Write-Host ""
Write-Host "Directory structure:" -ForegroundColor Cyan
Write-Host "  $tftpDir\" -ForegroundColor Gray
Write-Host "    ├── pxelinux.0" -ForegroundColor Gray
Write-Host "    ├── vesamenu.c32" -ForegroundColor Gray
Write-Host "    ├── pxelinux.cfg\default" -ForegroundColor Gray
Write-Host "    └── images\" -ForegroundColor Gray
Write-Host "        ├── mint\" -ForegroundColor Gray
Write-Host "        │   ├── vmlinuz" -ForegroundColor Gray
Write-Host "        │   └── initrd.lz" -ForegroundColor Gray
Write-Host "        └── clonezilla\" -ForegroundColor Gray
Write-Host "            ├── vmlinuz" -ForegroundColor Gray
Write-Host "            ├── initrd.img" -ForegroundColor Gray
Write-Host "            └── filesystem.squashfs" -ForegroundColor Gray
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Configure network adapter to 192.168.1.10 (static IP)"
Write-Host "  2. Run tftpd64.exe from $baseDir\tftpd64\"
Write-Host "  3. Configure Tiny PXE Server (see SETUP_GUIDE.md)"
Write-Host "  4. Connect MacBook Pro to same network"
Write-Host "  5. Boot MacBook holding Option key, select Network Boot"
Write-Host ""
Write-Host "Documentation: $baseDir\QUICK_START.md" -ForegroundColor Gray
Write-Host ""
