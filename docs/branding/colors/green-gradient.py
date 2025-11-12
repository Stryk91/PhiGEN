"""
PhiVector Green Gradient
25-shade gradient from neon green to black
Primary brand color palette
"""

# Hex colors (with #)
PHIVECTOR_GREEN = [
    "#00FF2A",  # Green - Primary neon
    "#00F428",  # Erin - Bright success
    "#00EA27",  # SGBUS green - Headers
    "#00DF25",  # SGBUS green 2 - Borders
    "#00D523",  # Lime green - Default
    "#00CA21",  # Lime green 2 - Links
    "#00BF20",  # Dark pastel green - Hover
    "#00B51E",  # Dark pastel green 2 - Code
    "#00AA1C",  # Dark pastel green 3 - Badges
    "#009F1A",  # Pigment green - Icons
    "#009519",  # Forest green - Dividers
    "#008A17",  # India green - Disabled
    "#008015",  # Office green - Tertiary
    "#007513",  # Office green 2 - BG accent
    "#006A12",  # Office green 3 - Borders
    "#006010",  # Dartmouth green - Text
    "#00550E",  # Cal Poly green - BG tint
    "#004A0C",  # Pakistan green - Very dark
    "#00400B",  # Pakistan green 2 - Shadow
    "#003509",  # Pakistan green 3 - Near-black
    "#002B07",  # Dark green - Terminal BG
    "#002005",  # Dark green 2 - Deep shadow
    "#001504",  # Night - Almost black
    "#000B02",  # Black - Near-black base
    "#000000",  # Pure black
]

# RGB tuples
PHIVECTOR_GREEN_RGB = [
    (0, 255, 42),   # Green
    (0, 244, 40),   # Erin
    (0, 234, 39),   # SGBUS green
    (0, 223, 37),   # SGBUS green 2
    (0, 213, 35),   # Lime green
    (0, 202, 33),   # Lime green 2
    (0, 191, 32),   # Dark pastel green
    (0, 181, 30),   # Dark pastel green 2
    (0, 170, 28),   # Dark pastel green 3
    (0, 159, 26),   # Pigment green
    (0, 149, 25),   # Forest green
    (0, 138, 23),   # India green
    (0, 128, 21),   # Office green
    (0, 117, 19),   # Office green 2
    (0, 106, 18),   # Office green 3
    (0, 96, 16),    # Dartmouth green
    (0, 85, 14),    # Cal Poly green
    (0, 74, 12),    # Pakistan green
    (0, 64, 11),    # Pakistan green 2
    (0, 53, 9),     # Pakistan green 3
    (0, 43, 7),     # Dark green
    (0, 32, 5),     # Dark green 2
    (0, 21, 4),     # Night
    (0, 11, 2),     # Black
    (0, 0, 0),      # Pure black
]

# Named colors dictionary
PHIVECTOR_COLORS = {
    "neon": "#00FF2A",          # Brightest - Primary accent
    "bright": "#00EA27",        # Headers, primary text
    "primary": "#00D523",       # Default green
    "link": "#00CA21",          # Interactive elements
    "hover": "#00BF20",         # Hover states
    "code": "#00B51E",          # Syntax highlighting
    "icon": "#009F1A",          # Icons, glyphs
    "divider": "#009519",       # Borders, dividers
    "muted": "#008A17",         # Disabled states
    "dark_text": "#006010",     # Dark mode text
    "bg_tint": "#00550E",       # Background with green tint
    "terminal_bg": "#002B07",   # Terminal background
    "near_black": "#000B02",    # Near-black base
    "black": "#000000",         # Pure black
}

# PowerShell color mappings (for console scripts)
POWERSHELL_COLORS = {
    "NeonGreen": "#00FF2A",     # Maps to Green in PowerShell
    "DarkGreen": "#009519",     # Maps to DarkGreen in PowerShell
    "Black": "#000000",         # Maps to Black in PowerShell
}

# ANSI color codes for terminal output
ANSI_COLORS = {
    "neon_green": "\033[38;2;0;255;42m",
    "bright_green": "\033[38;2;0;234;39m",
    "primary_green": "\033[38;2;0;213;35m",
    "dark_green": "\033[38;2;0;149;25m",
    "reset": "\033[0m",
}


def get_gradient_color(index: int) -> str:
    """Get a color from the gradient by index (0-24)."""
    if 0 <= index < len(PHIVECTOR_GREEN):
        return PHIVECTOR_GREEN[index]
    return PHIVECTOR_GREEN[0]


def get_gradient_rgb(index: int) -> tuple:
    """Get RGB tuple from the gradient by index (0-24)."""
    if 0 <= index < len(PHIVECTOR_GREEN_RGB):
        return PHIVECTOR_GREEN_RGB[index]
    return PHIVECTOR_GREEN_RGB[0]


def get_color(name: str) -> str:
    """Get a named color."""
    return PHIVECTOR_COLORS.get(name, PHIVECTOR_COLORS["primary"])


# Example usage
if __name__ == "__main__":
    print("PhiVector Green Gradient")
    print("=" * 50)
    for i, color in enumerate(PHIVECTOR_GREEN):
        rgb = PHIVECTOR_GREEN_RGB[i]
        print(f"{i:2d}. {color} - RGB{rgb}")
