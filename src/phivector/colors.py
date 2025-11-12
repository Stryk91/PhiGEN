"""
PhiVector Color Palette - Eye Strain Reduction
Soft fade system with lifted blacks and warmer greens
"""

# Soft Fade Color Palette (NOT pure black/green)
COLORS = {
    # Base colors (lifted blacks for reduced eye strain)
    'bg_base': '#0D0D0D',           # Soft black (not pure #000)
    'bg_panel': '#151515',          # Panels slightly lighter
    'bg_card': '#1A1A1A',           # Cards/surfaces
    'bg_input': '#0A0A0A',          # Input fields (darkest)

    # Primary greens (softer than neon)
    'primary': '#00EE00',           # Main green (95% brightness, not 100%)
    'primary_bright': '#00FF00',    # Bright accents (sparingly)
    'primary_dim': '#00AA00',       # Dimmed green
    'primary_dark': '#007700',      # Dark green

    # Accent colors
    'accent_teal': '#00FFAA',       # Teal-green (easier on eyes)
    'accent_cyan': '#00DDDD',       # Cyan highlights

    # Text colors (soft whites, not pure)
    'text_primary': '#CCCCCC',      # Main text (soft white)
    'text_secondary': '#999999',    # Secondary text
    'text_dim': '#666666',          # Dimmed text

    # Status colors
    'success': '#00DD00',           # Success green
    'warning': '#FFAA00',           # Warning orange
    'error': '#FF4444',             # Error red
    'info': '#00DDFF',              # Info cyan

    # Chrome/metal highlights
    'chrome_bright': '#FFFFFF',     # Pure white (only for highlights)
    'chrome_mid': '#C9CDD1',        # Mid chrome
    'chrome_dark': '#8A9196',       # Dark chrome

    # Borders and separators
    'border_bright': 'rgba(0, 255, 0, 0.4)',    # Bright green border
    'border_dim': 'rgba(0, 255, 0, 0.2)',       # Dim green border
    'separator': 'rgba(0, 255, 0, 0.15)',       # Subtle separator
}

# Texture overlay opacities
TEXTURE_OPACITIES = {
    'carbon_fibre': 0.08,       # Base structure
    'graphene_mesh': 0.04,      # Detail layer
    'snake_scale': 0.03,        # Organic warmth
    'circuit': 0.10,            # Circuit background
}

# Interaction state colors
INTERACTION_STATES = {
    'normal': COLORS['primary_dim'],                      # #00AA00
    'hover': COLORS['primary'],                           # #00EE00
    'selected': COLORS['primary_bright'],                 # #00FF00
    'selected_bg': 'rgba(0, 238, 0, 0.20)',              # Selected background
    'hover_bg': 'rgba(0, 238, 0, 0.12)',                 # Hover background
    'border_selected': 'rgba(0, 255, 0, 1.0)',           # Selected border
    'border_hover': 'rgba(0, 238, 0, 0.5)',              # Hover border
}
