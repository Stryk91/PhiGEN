# PhiGEN PXE Server - ISO Download Script
# Downloads all required files for MacBook Pro 2007 Linux Mint installation
# Run in PowerShell as Administrator

$ErrorActionPreference = "Stop"

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  PhiGEN PXE Server - ISO Download Script              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Define base directory
$baseDir = "E:\PythonProjects\PhiGEN\pxe_server"
$isoDir = "$baseDir\isos"
$tftpDir = "$baseDir\tftp"
$tftpdDir = "$baseDir\tftpd64"
$winnfsdDir = "$baseDir\winnfsd"

# Create directories
Write-Host "[*] Creating directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $isoDir | Out-Null
New-Item -ItemType Directory -Force -Path $tftpDir | Out-Null
New-Item -ItemType Directory -Force -Path "$tftpDir\pxelinux.cfg" | Out-Null
New-Item -ItemType Directory -Force -Path "$tftpDir\images\mint" | Out-Null
New-Item -ItemType Directory -Force -Path "$tftpDir\images\clonezilla" | Out-Null
New-Item -ItemType Directory -Force -Path $tftpdDir | Out-Null
New-Item -ItemType Directory -Force -Path $winnfsdDir | Out-Null
Write-Host "[✓] Directories created" -ForegroundColor Green

# Download function with progress
function Download-File {
    param (
        [string]$url,
        [string]$output,
        [string]$name
    )

    Write-Host ""
    Write-Host "[*] Downloading: $name" -ForegroundColor Cyan
    Write-Host "    URL: $url" -ForegroundColor Gray
    Write-Host "    Destination: $output" -ForegroundColor Gray

    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($url, $output)
        Write-Host "[✓] Downloaded: $name" -ForegroundColor Green

        # Show file size
        $fileSize = (Get-Item $output).Length / 1MB
        Write-Host "    Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray

        return $true
    }
    catch {
        Write-Host "[✗] Failed to download: $name" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================
# DOWNLOAD 1: Tiny PXE Server (tftpd64)
# ============================================================
$tftpdUrl = "https://download.sourceforge.net/project/tftpd64/tftpd64_se/tftpd64_se_464.zip"
$tftpdFile = "$tftpdDir\tftpd64.zip"

if (Test-Path $tftpdFile) {
    Write-Host "[!] Tiny PXE Server already downloaded: $tftpdFile" -ForegroundColor Yellow
} else {
    Download-File -url $tftpdUrl -output $tftpdFile -name "Tiny PXE Server"

    # Extract
    if (Test-Path $tftpdFile) {
        Write-Host "[*] Extracting Tiny PXE Server..." -ForegroundColor Yellow
        Expand-Archive -Path $tftpdFile -DestinationPath $tftpdDir -Force
        Write-Host "[✓] Extracted to: $tftpdDir" -ForegroundColor Green
    }
}

# ============================================================
# DOWNLOAD 2: SYSLINUX 6.03
# ============================================================
$syslinuxUrl = "https://mirrors.edge.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.03.zip"
$syslinuxFile = "$baseDir\syslinux-6.03.zip"

if (Test-Path $syslinuxFile) {
    Write-Host "[!] SYSLINUX already downloaded: $syslinuxFile" -ForegroundColor Yellow
} else {
    Download-File -url $syslinuxUrl -output $syslinuxFile -name "SYSLINUX 6.03"

    # Extract
    if (Test-Path $syslinuxFile) {
        Write-Host "[*] Extracting SYSLINUX..." -ForegroundColor Yellow
        Expand-Archive -Path $syslinuxFile -DestinationPath "$baseDir\syslinux" -Force

        # Copy required files to TFTP directory
        Write-Host "[*] Copying PXE boot files to TFTP directory..." -ForegroundColor Yellow
        Copy-Item "$baseDir\syslinux\syslinux-6.03\bios\core\pxelinux.0" -Destination $tftpDir
        Copy-Item "$baseDir\syslinux\syslinux-6.03\bios\com32\elflink\ldlinux\ldlinux.c32" -Destination $tftpDir
        Copy-Item "$baseDir\syslinux\syslinux-6.03\bios\com32\libutil\libutil.c32" -Destination $tftpDir
        Copy-Item "$baseDir\syslinux\syslinux-6.03\bios\com32\menu\vesamenu.c32" -Destination $tftpDir
        Copy-Item "$baseDir\syslinux\syslinux-6.03\bios\com32\lib\libcom32.c32" -Destination $tftpDir

        Write-Host "[✓] SYSLINUX files copied to TFTP directory" -ForegroundColor Green
    }
}

# ============================================================
# DOWNLOAD 3: Linux Mint 21.3 MATE (2.4 GB)
# ============================================================
$mintUrl = "https://mirrors.layeronline.com/linuxmint/stable/21.3/linuxmint-21.3-mate-64bit.iso"
$mintFile = "$isoDir\linuxmint-21.3-mate-64bit.iso"

if (Test-Path $mintFile) {
    Write-Host "[!] Linux Mint already downloaded: $mintFile" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " WARNING: This is a 2.4 GB download - may take 10-30 min" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan

    $continue = Read-Host "Continue with Linux Mint download? (Y/N)"
    if ($continue -eq "Y" -or $continue -eq "y") {
        Download-File -url $mintUrl -output $mintFile -name "Linux Mint 21.3 MATE"
    } else {
        Write-Host "[!] Skipped Linux Mint download" -ForegroundColor Yellow
    }
}

# ============================================================
# DOWNLOAD 4: Clonezilla Live (Optional - 400 MB)
# ============================================================
$clonezillaUrl = "https://sourceforge.net/projects/clonezilla/files/clonezilla_live_stable/3.1.3-5/clonezilla-live-3.1.3-5-amd64.iso/download"
$clonezillaFile = "$isoDir\clonezilla-live-3.1.3-5-amd64.iso"

Write-Host ""
$downloadClonezilla = Read-Host "Download Clonezilla (for backing up macOS)? (Y/N)"

if ($downloadClonezilla -eq "Y" -or $downloadClonezilla -eq "y") {
    if (Test-Path $clonezillaFile) {
        Write-Host "[!] Clonezilla already downloaded: $clonezillaFile" -ForegroundColor Yellow
    } else {
        Download-File -url $clonezillaUrl -output $clonezillaFile -name "Clonezilla Live"
    }
} else {
    Write-Host "[!] Skipped Clonezilla download" -ForegroundColor Yellow
}

# ============================================================
# DOWNLOAD 5: WinNFSd (Optional - for NFS support)
# ============================================================
$winnfsdUrl = "https://github.com/winnfsd/winnfsd/releases/download/2.4.0/WinNFSd.exe"
$winnfsdFile = "$winnfsdDir\WinNFSd.exe"

Write-Host ""
$downloadWinNFSd = Read-Host "Download WinNFSd (NFS server for Windows)? (Y/N)"

if ($downloadWinNFSd -eq "Y" -or $downloadWinNFSd -eq "y") {
    if (Test-Path $winnfsdFile) {
        Write-Host "[!] WinNFSd already downloaded: $winnfsdFile" -ForegroundColor Yellow
    } else {
        Download-File -url $winnfsdUrl -output $winnfsdFile -name "WinNFSd"
    }
} else {
    Write-Host "[!] Skipped WinNFSd download" -ForegroundColor Yellow
}

# ============================================================
# FINAL SUMMARY
# ============================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              Download Complete!                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Downloaded files:" -ForegroundColor Cyan
Write-Host ""

# Check what was downloaded
if (Test-Path $tftpdFile) { Write-Host "  [✓] Tiny PXE Server" -ForegroundColor Green } else { Write-Host "  [✗] Tiny PXE Server" -ForegroundColor Red }
if (Test-Path $syslinuxFile) { Write-Host "  [✓] SYSLINUX 6.03" -ForegroundColor Green } else { Write-Host "  [✗] SYSLINUX 6.03" -ForegroundColor Red }
if (Test-Path $mintFile) { Write-Host "  [✓] Linux Mint 21.3 MATE" -ForegroundColor Green } else { Write-Host "  [✗] Linux Mint 21.3 MATE" -ForegroundColor Red }
if (Test-Path $clonezillaFile) { Write-Host "  [✓] Clonezilla Live" -ForegroundColor Green } else { Write-Host "  [!] Clonezilla Live (optional)" -ForegroundColor Yellow }
if (Test-Path $winnfsdFile) { Write-Host "  [✓] WinNFSd" -ForegroundColor Green } else { Write-Host "  [!] WinNFSd (optional)" -ForegroundColor Yellow }

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Run extract_boot_files.ps1 to extract boot files from ISOs"
Write-Host "  2. Follow QUICK_START.md for PXE server setup"
Write-Host "  3. Configure network adapter to 192.168.1.10"
Write-Host ""
Write-Host "Files location: $baseDir" -ForegroundColor Gray
Write-Host ""
