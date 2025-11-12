#!/bin/bash
#
# PhiGEN MacBook Pro 2007 Post-Installation Setup
# Optimizes Linux Mint for 2007 MacBook Pro hardware
# Run this after installing Linux Mint
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "════════════════════════════════════════════════════════"
echo "  PhiGEN MacBook Pro 2007 - Post-Installation Setup"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please run as normal user, not root (script will use sudo when needed)"
    exit 1
fi

# Update package lists
print_status "Updating package lists..."
sudo apt update

# ============================================================
# SECTION 1: Essential System Tools
# ============================================================
echo ""
echo -e "${YELLOW}Installing essential system tools...${NC}"

sudo apt install -y \
    build-essential \
    linux-headers-$(uname -r) \
    dkms \
    git \
    curl \
    wget \
    htop \
    neofetch \
    tlp \
    tlp-rdw \
    powertop \
    laptop-mode-tools \
    cpufrequtils \
    thermald

print_status "Essential system tools installed"

# ============================================================
# SECTION 2: MacBook-Specific Drivers & Firmware
# ============================================================
echo ""
echo -e "${YELLOW}Installing MacBook-specific drivers...${NC}"

# Broadcom WiFi drivers (most common in 2007 MacBook Pro)
sudo apt install -y \
    bcmwl-kernel-source \
    broadcom-sta-dkms \
    firmware-b43-installer \
    b43-fwcutter

# Touchpad drivers (better multitouch support)
sudo apt install -y \
    xserver-xorg-input-synaptics \
    xserver-xorg-input-libinput

# Webcam support (iSight camera)
sudo apt install -y \
    isight-firmware-tools

# Apple sensors
sudo apt install -y \
    macfanctld \
    pommed

print_status "MacBook-specific drivers installed"

# ============================================================
# SECTION 3: Graphics & Display
# ============================================================
echo ""
echo -e "${YELLOW}Installing graphics and display tools...${NC}"

# Intel/NVIDIA graphics support
sudo apt install -y \
    mesa-utils \
    vulkan-tools \
    xserver-xorg-video-intel \
    xbacklight \
    brightnessctl

# For NVIDIA models (GeForce 8600M GT)
print_warning "If you have NVIDIA graphics, consider installing nvidia-340 driver"
print_warning "Run: sudo apt install nvidia-340"

print_status "Graphics tools installed"

# ============================================================
# SECTION 4: Audio
# ============================================================
echo ""
echo -e "${YELLOW}Installing audio tools...${NC}"

sudo apt install -y \
    pulseaudio \
    pavucontrol \
    alsa-utils \
    pulseaudio-module-bluetooth

# Fix MacBook audio quirks
print_status "Configuring audio for MacBook..."
sudo tee /etc/modprobe.d/alsa-base.conf > /dev/null << 'AUDIO'
# MacBook Pro audio fix
options snd-hda-intel model=mbp3
AUDIO

print_status "Audio tools installed and configured"

# ============================================================
# SECTION 5: Power Management & Battery
# ============================================================
echo ""
echo -e "${YELLOW}Configuring power management...${NC}"

# Enable TLP for better battery life
sudo systemctl enable tlp
sudo systemctl start tlp

# Configure laptop-mode-tools
sudo tee /etc/laptop-mode/laptop-mode.conf > /dev/null << 'POWER'
ENABLE_LAPTOP_MODE_ON_BATTERY=1
ENABLE_LAPTOP_MODE_ON_AC=0
ENABLE_LAPTOP_MODE_WHEN_LID_CLOSED=1
CONTROL_BACKLIGHT=1
BATT_HD_POWERMGMT=128
LM_AC_HD_POWERMGMT=254
POWER

sudo systemctl enable laptop-mode
sudo systemctl start laptop-mode

print_status "Power management configured for maximum battery life"

# ============================================================
# SECTION 6: Development Tools
# ============================================================
echo ""
echo -e "${YELLOW}Installing development tools...${NC}"

sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    nodejs \
    npm \
    vim \
    nano \
    code \
    git-gui \
    meld

print_status "Development tools installed"

# ============================================================
# SECTION 7: Multimedia & Codecs
# ============================================================
echo ""
echo -e "${YELLOW}Installing multimedia codecs...${NC}"

sudo apt install -y \
    ubuntu-restricted-extras \
    mint-meta-codecs \
    ffmpeg \
    vlc \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libdvd-pkg

# Configure libdvd-pkg
sudo dpkg-reconfigure libdvd-pkg

print_status "Multimedia codecs installed"

# ============================================================
# SECTION 8: Useful Applications
# ============================================================
echo ""
echo -e "${YELLOW}Installing useful applications...${NC}"

sudo apt install -y \
    timeshift \
    bleachbit \
    gparted \
    synaptic \
    gnome-disk-utility \
    baobab \
    gimp \
    inkscape \
    audacity \
    transmission-gtk \
    firefox \
    thunderbird \
    libreoffice \
    gnome-tweaks

print_status "Applications installed"

# ============================================================
# SECTION 9: Mac-like Tweaks & Fonts
# ============================================================
echo ""
echo -e "${YELLOW}Installing Mac-like fonts and tweaks...${NC}"

sudo apt install -y \
    fonts-apple-emoji \
    fonts-noto \
    fonts-noto-color-emoji \
    fonts-liberation \
    ttf-mscorefonts-installer

# Install SF Pro font (Mac system font) if available
print_warning "For Mac-like appearance, consider installing SF Pro font manually"

print_status "Fonts installed"

# ============================================================
# SECTION 10: Optimize for Old Hardware
# ============================================================
echo ""
echo -e "${YELLOW}Optimizing for 2007 hardware...${NC}"

# Disable unnecessary services
sudo systemctl disable bluetooth.service || true
sudo systemctl disable cups-browsed.service || true

# Reduce swappiness for better performance with limited RAM
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf > /dev/null

# Preload for faster app launches
sudo apt install -y preload
sudo systemctl enable preload

print_status "System optimized for old hardware"

# ============================================================
# SECTION 11: Networking Tools
# ============================================================
echo ""
echo -e "${YELLOW}Installing networking tools...${NC}"

sudo apt install -y \
    network-manager \
    network-manager-gnome \
    nmap \
    net-tools \
    openssh-server \
    samba \
    cifs-utils \
    avahi-daemon

# Enable SSH server
sudo systemctl enable ssh
sudo systemctl start ssh

print_status "Networking tools installed"

# ============================================================
# SECTION 12: Cleanup & Optimization
# ============================================================
echo ""
echo -e "${YELLOW}Cleaning up...${NC}"

sudo apt autoremove -y
sudo apt autoclean
sudo apt clean

print_status "System cleaned up"

# ============================================================
# SECTION 13: MacBook-Specific Fixes
# ============================================================
echo ""
echo -e "${YELLOW}Applying MacBook-specific fixes...${NC}"

# Fix keyboard layout (Mac keyboard quirks)
sudo tee /etc/default/keyboard > /dev/null << 'KEYBOARD'
XKBMODEL="macintosh"
XKBLAYOUT="us"
XKBVARIANT="mac"
XKBOPTIONS="terminate:ctrl_alt_bksp"
KEYBOARD

# Enable tap-to-click for trackpad
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/trackpad-tap.desktop << 'TRACKPAD'
[Desktop Entry]
Type=Application
Name=Enable Tap to Click
Exec=synclient TapButton1=1 TapButton2=3 TapButton3=2
X-GNOME-Autostart-enabled=true
TRACKPAD

# Fix function keys (F1-F12 behavior)
echo "options hid_apple fnmode=2" | sudo tee /etc/modprobe.d/hid_apple.conf > /dev/null

print_status "MacBook-specific fixes applied"

# ============================================================
# SECTION 14: Create System Info Script
# ============================================================
echo ""
echo -e "${YELLOW}Creating system info script...${NC}"

cat > ~/macbook_info.sh << 'SYSINFO'
#!/bin/bash
echo "╔════════════════════════════════════════════════════════╗"
echo "║         MacBook Pro 2007 - System Information          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "CPU:"
lscpu | grep "Model name" | sed 's/Model name://g'
echo ""
echo "Memory:"
free -h | grep "Mem:"
echo ""
echo "Graphics:"
lspci | grep VGA
echo ""
echo "WiFi:"
lspci | grep Network
echo ""
echo "Battery:"
upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "state|percentage|time to"
echo ""
echo "Temperature:"
sensors 2>/dev/null || echo "Install lm-sensors: sudo apt install lm-sensors"
SYSINFO

chmod +x ~/macbook_info.sh

print_status "System info script created at ~/macbook_info.sh"

# ============================================================
# FINAL REPORT
# ============================================================
echo ""
echo -e "${GREEN}"
echo "════════════════════════════════════════════════════════"
echo "  Installation Complete!"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}"
echo ""
echo "Summary of installed components:"
echo "  ✓ Essential system tools (build tools, git, etc.)"
echo "  ✓ MacBook drivers (WiFi, touchpad, webcam, sensors)"
echo "  ✓ Graphics drivers (Intel/Mesa)"
echo "  ✓ Audio configuration"
echo "  ✓ Power management (TLP, laptop-mode)"
echo "  ✓ Development tools (Python, Node.js, VS Code)"
echo "  ✓ Multimedia codecs (all formats supported)"
echo "  ✓ Useful applications (GIMP, LibreOffice, VLC, etc.)"
echo "  ✓ Mac-like fonts and tweaks"
echo "  ✓ System optimizations for old hardware"
echo "  ✓ Networking tools"
echo "  ✓ MacBook-specific fixes"
echo ""
echo -e "${YELLOW}Important Next Steps:${NC}"
echo "  1. Reboot your system: sudo reboot"
echo "  2. Test WiFi connectivity"
echo "  3. Test webcam: cheese"
echo "  4. Check battery status: ~/macbook_info.sh"
echo "  5. Adjust brightness with Fn keys"
echo ""
echo -e "${YELLOW}Optional Enhancements:${NC}"
echo "  • Install NVIDIA driver (if applicable): sudo apt install nvidia-340"
echo "  • Configure backups: timeshift-gtk"
echo "  • Customize appearance: gnome-tweaks"
echo ""
echo -e "${GREEN}Your MacBook Pro is ready! Enjoy Linux Mint!${NC}"
echo ""
