# PhiGEN PXE Server - Setup Verification Script
# Verifies all files are in place for PXE boot
# Run in PowerShell

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  PhiGEN PXE Server - Setup Verification               ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

$baseDir = "E:\PythonProjects\PhiGEN\pxe_server"
$errorCount = 0
$warningCount = 0

function Test-FileExists {
    param (
        [string]$path,
        [string]$name,
        [bool]$optional = $false
    )

    if (Test-Path $path) {
        $size = (Get-Item $path).Length / 1MB
        Write-Host "  [✓] $name" -ForegroundColor Green
        Write-Host "      $path" -ForegroundColor Gray
        Write-Host "      Size: $([math]::Round($size, 2)) MB" -ForegroundColor Gray
        return $true
    } else {
        if ($optional) {
            Write-Host "  [!] $name (optional)" -ForegroundColor Yellow
            $script:warningCount++
        } else {
            Write-Host "  [✗] $name" -ForegroundColor Red
            Write-Host "      Missing: $path" -ForegroundColor Red
            $script:errorCount++
        }
        return $false
    }
}

function Test-NetworkConfig {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " Network Configuration Check" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""

    $adapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -eq "192.168.1.10" }

    if ($adapters) {
        Write-Host "  [✓] Network adapter configured with 192.168.1.10" -ForegroundColor Green
        foreach ($adapter in $adapters) {
            $interface = Get-NetAdapter -InterfaceIndex $adapter.InterfaceIndex
            Write-Host "      Interface: $($interface.Name)" -ForegroundColor Gray
            Write-Host "      Status: $($interface.Status)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [✗] No adapter found with IP 192.168.1.10" -ForegroundColor Red
        Write-Host "      Configure network adapter:" -ForegroundColor Yellow
        Write-Host "      Control Panel → Network → Adapter Properties → IPv4" -ForegroundColor Yellow
        Write-Host "      IP: 192.168.1.10" -ForegroundColor Yellow
        Write-Host "      Subnet: 255.255.255.0" -ForegroundColor Yellow
        Write-Host "      Gateway: 192.168.1.1" -ForegroundColor Yellow
        $script:errorCount++
    }
}

function Test-FirewallRules {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " Firewall Rules Check" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""

    # Check if TFTP (UDP 69) is allowed
    $tftpRule = Get-NetFirewallPortFilter | Where-Object { $_.LocalPort -eq 69 }
    if ($tftpRule) {
        Write-Host "  [✓] Firewall rule for TFTP (UDP 69) exists" -ForegroundColor Green
    } else {
        Write-Host "  [!] No firewall rule for TFTP (UDP 69)" -ForegroundColor Yellow
        Write-Host "      You may need to allow TFTP in Windows Firewall" -ForegroundColor Yellow
        $script:warningCount++
    }

    # Check if DHCP (UDP 67-68) is allowed
    $dhcpRule = Get-NetFirewallPortFilter | Where-Object { $_.LocalPort -eq 67 -or $_.LocalPort -eq 68 }
    if ($dhcpRule) {
        Write-Host "  [✓] Firewall rule for DHCP (UDP 67-68) exists" -ForegroundColor Green
    } else {
        Write-Host "  [!] No firewall rule for DHCP (UDP 67-68)" -ForegroundColor Yellow
        Write-Host "      You may need to allow DHCP in Windows Firewall" -ForegroundColor Yellow
        $script:warningCount++
    }
}

# ============================================================
# CHECK 1: TFTP Boot Files
# ============================================================
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " TFTP Boot Files" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\tftp\pxelinux.0" "PXE bootloader (pxelinux.0)"
Test-FileExists "$baseDir\tftp\ldlinux.c32" "SYSLINUX library (ldlinux.c32)"
Test-FileExists "$baseDir\tftp\libutil.c32" "SYSLINUX utility library (libutil.c32)"
Test-FileExists "$baseDir\tftp\vesamenu.c32" "VESA menu module (vesamenu.c32)"
Test-FileExists "$baseDir\tftp\libcom32.c32" "COM32 library (libcom32.c32)"
Test-FileExists "$baseDir\tftp\pxelinux.cfg\default" "PXE menu configuration"

# ============================================================
# CHECK 2: Linux Mint Boot Files
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Linux Mint Boot Files" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\tftp\images\mint\vmlinuz" "Linux Mint kernel (vmlinuz)"
Test-FileExists "$baseDir\tftp\images\mint\initrd.lz" "Linux Mint initrd (initrd.lz)"
Test-FileExists "$baseDir\http\mint\casper\filesystem.squashfs" "Linux Mint root filesystem"

# ============================================================
# CHECK 3: Clonezilla Boot Files (Optional)
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Clonezilla Boot Files (Optional)" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\tftp\images\clonezilla\vmlinuz" "Clonezilla kernel" $true
Test-FileExists "$baseDir\tftp\images\clonezilla\initrd.img" "Clonezilla initrd" $true
Test-FileExists "$baseDir\tftp\images\clonezilla\filesystem.squashfs" "Clonezilla filesystem" $true

# ============================================================
# CHECK 4: Tiny PXE Server
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Tiny PXE Server" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\tftpd64\tftpd64.exe" "Tiny PXE Server executable"

# Check if tftpd64 is running
$process = Get-Process -Name "tftpd64" -ErrorAction SilentlyContinue
if ($process) {
    Write-Host "  [✓] Tiny PXE Server is running" -ForegroundColor Green
    Write-Host "      PID: $($process.Id)" -ForegroundColor Gray
} else {
    Write-Host "  [!] Tiny PXE Server is not running" -ForegroundColor Yellow
    Write-Host "      Start it from: $baseDir\tftpd64\tftpd64.exe" -ForegroundColor Yellow
    $warningCount++
}

# ============================================================
# CHECK 5: ISOs
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " ISO Files" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\isos\linuxmint-21.3-mate-64bit.iso" "Linux Mint ISO"
Test-FileExists "$baseDir\isos\clonezilla-live-3.1.3-5-amd64.iso" "Clonezilla ISO" $true

# ============================================================
# CHECK 6: Post-Installation Scripts
# ============================================================
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " Post-Installation Scripts" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Test-FileExists "$baseDir\post_install_scripts\macbook_setup.sh" "MacBook setup script"

# ============================================================
# CHECK 7: Network Configuration
# ============================================================
Test-NetworkConfig

# ============================================================
# CHECK 8: Firewall Rules
# ============================================================
Test-FirewallRules

# ============================================================
# FINAL SUMMARY
# ============================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              Verification Complete!                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

if ($errorCount -eq 0 -and $warningCount -eq 0) {
    Write-Host "  ✓ All checks passed! PXE server is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Ensure Tiny PXE Server is running" -ForegroundColor White
    Write-Host "  2. Connect MacBook Pro to same network (Ethernet cable)" -ForegroundColor White
    Write-Host "  3. Boot MacBook holding Option key" -ForegroundColor White
    Write-Host "  4. Select 'Network Boot' (globe icon)" -ForegroundColor White
    Write-Host "  5. Select Linux Mint from PXE menu" -ForegroundColor White
} elseif ($errorCount -eq 0) {
    Write-Host "  ✓ Critical checks passed (with $warningCount warnings)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can proceed, but review the warnings above." -ForegroundColor Yellow
} else {
    Write-Host "  ✗ Found $errorCount critical errors and $warningCount warnings" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the errors before proceeding:" -ForegroundColor Red
    Write-Host "  1. Run download_isos.ps1 to download missing files" -ForegroundColor White
    Write-Host "  2. Run extract_boot_files.ps1 to extract boot files" -ForegroundColor White
    Write-Host "  3. Configure network adapter to 192.168.1.10" -ForegroundColor White
}

Write-Host ""
Write-Host "Documentation: $baseDir\QUICK_START.md" -ForegroundColor Gray
Write-Host ""

# Return exit code
exit $errorCount
