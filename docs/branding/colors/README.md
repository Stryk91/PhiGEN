# PhiVector Color Palettes

Brand color documentation for PhiVector systems.

---

## 📁 Files

### Green Gradient (Primary Brand)

- **green-gradient.json** - Complete color data with metadata
- **green-gradient.css** - CSS variables for web/UI
- **green-gradient.py** - Python constants for scripts
- **green-gradient.ps1** - PowerShell hashtable (coming next)

---

## 🎨 Color Palettes

### 1. Green Gradient (25 shades)

**Range:** Neon green (#00FF2A) → Pure black (#000000)

**Primary colors:**
- **Neon (#00FF2A)** - Brightest accent, CTAs, highlights
- **Bright (#00EA27)** - Headers, primary text on dark
- **Primary (#00D523)** - Default brand green
- **Link (#00CA21)** - Interactive elements, links
- **Hover (#00BF20)** - Hover states, secondary buttons
- **Code (#00B51E)** - Syntax highlighting, code blocks
- **Icon (#009F1A)** - Icons, glyphs, small UI
- **Divider (#009519)** - Borders, dividers, separators
- **Muted (#008A17)** - Disabled states, subtle elements
- **Dark Text (#006010)** - Dark mode text
- **BG Tint (#00550E)** - Backgrounds with green hint
- **Terminal BG (#002B07)** - Terminal/console background
- **Near Black (#000B02)** - Near-black base
- **Black (#000000)** - Pure black

---

## 🔧 Usage Examples

### CSS/HTML

```css
@import url('green-gradient.css');

.primary-button {
    background: var(--phivector-primary);
    color: var(--phivector-bg-primary);
    border: 1px solid var(--phivector-accent);
}

.primary-button:hover {
    background: var(--phivector-hover);
}
```

### Python

```python
from docs.branding.colors.green_gradient import PHIVECTOR_COLORS, ANSI_COLORS

# Print colored text
print(f"{ANSI_COLORS['neon_green']}PhiVector{ANSI_COLORS['reset']} - Direction for every signal")

# Get named color
primary = PHIVECTOR_COLORS["primary"]  # #00D523

# Get gradient color by index
from docs.branding.colors.green_gradient import get_gradient_color
header_color = get_gradient_color(2)  # #00EA27
```

### PowerShell (coming next)

```powershell
. .\green-gradient.ps1

Write-Host "PhiVector" -ForegroundColor $PhiVectorColors.NeonGreen
Write-Host "Direction for every signal" -ForegroundColor $PhiVectorColors.Primary
```

---

## 🎯 Semantic Color Usage

### UI Elements

| Element | Color | Hex |
|---------|-------|-----|
| **Headers** | Bright | #00EA27 |
| **Body text** | Dark Text | #006010 |
| **Links** | Link | #00CA21 |
| **Buttons (primary)** | Primary | #00D523 |
| **Buttons (hover)** | Hover | #00BF20 |
| **Success states** | Bright | #00F428 |
| **Borders** | Divider | #009519 |
| **Disabled** | Muted | #008A17 |
| **Background** | Black | #000000 |
| **Terminal BG** | Terminal BG | #002B07 |

### Code/Terminal

| Element | Color | Hex |
|---------|-------|-----|
| **Syntax keywords** | Code | #00B51E |
| **Strings** | Primary | #00D523 |
| **Comments** | Muted | #008A17 |
| **Function names** | Link | #00CA21 |
| **Operators** | Icon | #009F1A |
| **Terminal prompt** | Neon | #00FF2A |
| **Terminal BG** | Terminal BG | #002B07 |

---

## 🌈 Gradient Visualization

```
#00FF2A ████████ Neon (brightest)
#00F428 ████████
#00EA27 ████████ Bright
#00DF25 ████████
#00D523 ████████ Primary
#00CA21 ████████ Link
#00BF20 ████████ Hover
#00B51E ████████ Code
#00AA1C ████████
#009F1A ████████ Icon
#009519 ████████ Divider
#008A17 ████████ Muted
#008015 ████████
#007513 ████████
#006A12 ████████
#006010 ████████ Dark Text
#00550E ████████ BG Tint
#004A0C ████████
#00400B ████████
#003509 ████████
#002B07 ████████ Terminal BG
#002005 ████████
#001504 ████████
#000B02 ████████ Near Black
#000000 ████████ Black (darkest)
```

---

## 📊 Color Properties

### Accessibility

**WCAG AA Compliance:**
- Neon (#00FF2A) on Black (#000000): ✅ AAA (14.2:1)
- Primary (#00D523) on Black (#000000): ✅ AAA (11.8:1)
- Dark Text (#006010) on Black (#000000): ❌ Fails (2.8:1) - Use for dark mode only

**Recommended combinations:**
- Light text on dark: Use shades 0-11 (#00FF2A - #008A17)
- Dark backgrounds: Use shades 18-24 (#00400B - #000000)

### Color Theory

**Hue:** 130° (pure green)
**Saturation:** 100% (all shades except black)
**Lightness:** 50% (primary) → 0% (black)

**Complementary:** Magenta (#FF00D5)
**Analogous:** Yellow-green (#80FF00), Blue-green (#00FF80)

---

## 🔄 Upcoming Palettes

- **Chrome gradient** (whites/grays)
- **Gunmetal gradient** (dark grays)
- **Cyan accent gradient** (blue-greens)
- **Full PhiVector palette** (combined system)

---

**Last Updated:** 2025-11-08
