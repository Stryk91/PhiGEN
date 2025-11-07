# JC Knowledge Base - PhiGEN Project

**Last Updated**: 2025-11-06
**Agent**: JC (Jetbrains Claude)

This file contains solutions to problems I've encountered, useful patterns, and project-specific knowledge.

---

## Problems Solved

### Problem: Low-Quality Title Image Display
**Date**: 2025-11-06
**Files**: `TEMPSVG/password_vault_complete_IMPROVED.py`, `run_qt_ui_IMPROVED.py`

**Issue**:
User had a high-resolution title image (7144×1224) but was getting poor quality when displayed in the UI. Initial approach was to downscale the PNG file itself, which permanently lost quality.

**Wrong Approach**:
```python
# DON'T DO THIS - Destroys quality
img = Image.open('high_res.png')
img_resized = img.resize((800, 111), Image.LANCZOS)
img_resized.save('low_res.png')  # ❌ Quality lost forever

# Then loading the low-res file in Qt
pixmap = QPixmap('low_res.png')  # ❌ Already degraded
```

**Correct Solution**:
```python
# Keep high-res file on disk, let Qt scale at display time
high_res_pixmap = QPixmap(str(Path("TEMPSVG/PHIGEN_TITLE_FINAL.png")))  # 7144×1224

# Scale for display with high-quality algorithm
display_height = 100
aspect_ratio = high_res_pixmap.width() / high_res_pixmap.height()
display_width = int(display_height * aspect_ratio)

display_pixmap = high_res_pixmap.scaled(
    display_width,
    display_height,
    Qt.AspectRatioMode.KeepAspectRatio,
    Qt.TransformationMode.SmoothTransformation  # ✓ High quality
)

label.setPixmap(display_pixmap)
```

**Key Learnings**:
- High-res source files (7000+ px) should NEVER be downscaled on disk
- Qt's `SmoothTransformation` provides excellent quality when downscaling at runtime
- File size can be reduced via PNG compression (`optimize=True, compress_level=9`) without quality loss
- The rendering quality comes from the resolution of the SOURCE, not the display size

**Related Files**:
- `TEMPSVG/PHIGEN_TITLE_FINAL.png` (7144×1224) - High-res source, DO NOT MODIFY
- `TEMPSVG/FINALTITLEFORUSE.png` (7144×1224) - Original source file

---

### Problem: Unicode Encoding Errors in Windows CMD
**Date**: 2025-11-06
**Files**: Various Python scripts

**Issue**:
Windows CMD (cp1252 encoding) cannot display Unicode characters like `✓` (U+2713) or `→` (U+2192).

**Error**:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
```

**Solution**:
Replace fancy Unicode with ASCII equivalents in print statements:
```python
# Instead of: print(f"✓ Success")
print(f"[OK] Success")

# Instead of: print(f"⚠ Warning")
print(f"[WARNING] Warning")

# Instead of: print(f"foo → bar")
print(f"foo -> bar")
```

**Alternative** (if you control the script environment):
```python
import sys
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

---

### Problem: SVG to PNG Conversion with Transparency
**Date**: 2025-11-06
**Files**: `firefox_svg_render.py`

**Issue**:
Need to convert SVG files to PNG with transparent backgrounds at high quality.

**Solution - Firefox + Selenium**:
```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image

def firefox_8x_screenshot(svg_path, output_path, final_width=1400, final_height=200):
    """Render at 8× then downscale for smooth anti-aliasing"""

    render_width = final_width * 8
    render_height = final_height * 8

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    # Load SVG
    svg_file = Path(svg_path).absolute().as_uri()
    driver.get(svg_file)

    # Inject JavaScript to set high resolution
    driver.execute_script(f"""
        document.querySelector('svg').style.width = '{render_width}px';
        document.querySelector('svg').style.height = '{render_height}px';
    """)

    time.sleep(2)  # Let render

    # Screenshot
    temp_file = 'temp_8x.png'
    element = driver.find_element('tag name', 'svg')
    element.screenshot(temp_file)
    driver.quit()

    # Downscale with Lanczos (high quality)
    img = Image.open(temp_file)
    img_resized = img.resize((final_width, final_height), Image.LANCZOS)
    img_resized.save(output_path)
```

**Dependencies**:
- `selenium` - `pip install selenium`
- Firefox browser installed
- geckodriver in PATH

**Why This Works**:
- Renders at 8× target resolution for smooth edges
- Firefox handles SVG rendering with transparency
- LANCZOS downsampling provides excellent anti-aliasing

---

## Useful Code Snippets

### Check if File Exists Before Loading
```python
from pathlib import Path

file_path = Path("TEMPSVG/some_image.png")
if file_path.exists():
    pixmap = QPixmap(str(file_path))
    if not pixmap.isNull():
        label.setPixmap(pixmap)
    else:
        print(f"Failed to load: {file_path}")
else:
    print(f"File not found: {file_path}")
```

### Optimize PNG File Size Without Quality Loss
```python
from PIL import Image

img = Image.open('source.png')
img.save('optimized.png', 'PNG', optimize=True, compress_level=9)

# Typical results: 40-50% smaller file size, identical visual quality
```

### PyQt6 Window Size Configuration
```python
# Set exact window size
self.resize(1125, 740)

# Set minimum size (cannot shrink below this)
self.setMinimumSize(1125, 740)

# Allow unlimited growth
self.setMaximumSize(16777215, 16777215)

# Enable resize grip
self.statusBar().setSizeGripEnabled(True)
```

---

## Dependencies and Their Quirks

### PyQt6 vs PySide6
- **PhiGEN uses PyQt6** (confirmed in `password_vault_complete_IMPROVED.py`)
- Import paths: `from PyQt6.QtWidgets import ...`
- Resource compilation: `pyside6-rcc` (note: still uses PySide tools even with PyQt6)

### PIL/Pillow
- Used for image manipulation (NOT for display scaling)
- `Image.LANCZOS` is best for downsampling
- `optimize=True, compress_level=9` for file size reduction

### Selenium
- Requires geckodriver for Firefox
- Needs explicit `time.sleep()` for SVG rendering
- Use `.absolute().as_uri()` for file paths

---

## Configuration Gotchas

### Qt Resource Files
- Edit: `TEMPSVG/buttons.qrc` (XML format)
- Compile: `pyside6-rcc buttons.qrc -o buttons_rc.py`
- Import: `import buttons_rc` (no .py extension)
- Use: `QPixmap(":/ui/image_name.png")`

### Path Handling in Qt Stylesheets
```python
# Wrong (breaks on Windows):
background_path = "C:\Path\To\Image.png"

# Correct:
background_path = str(Path("relative/path.png")).replace("\\", "/")
```

### DPI Scaling on Windows
PhiGEN disables DPI scaling to ensure exact pixel sizes:
```python
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
```

---

## File Locations Quick Reference

### UI Elements (High-Res Sources)
- Title: `TEMPSVG/PHIGEN_TITLE_FINAL.png` (7144×1224)
- Background: `TEMPSVG/circuit_background_opacity_15.png`
- Buttons: `TEMPSVG/*_ultra_smooth.png` files
- Text inputs: `TEMPSVG/text_input_9slice_ultra_smooth.png`

### Working Applications
- **Main UI**: `TEMPSVG/password_vault_complete_IMPROVED.py` ⭐ USE THIS
- Backend: `password_vault_backend.py`
- Qt Designer: `ui/password_vault_IMPROVED.ui`

### Coordination
- Agent feed: `docs/agent-feed.jsonl`
- Guidelines: `docs/JC_GUIDELINES.md` (this doc's companion)

---

## Testing Notes

### Manual Testing Checklist
- [ ] Window opens at 1125×740
- [ ] All button graphics load (no broken images)
- [ ] Title appears crisp and clear
- [ ] Text is readable (green on dark)
- [ ] Buttons respond to clicks
- [ ] Password input hides characters
- [ ] List widget displays entries

### Known Working Configuration
- Windows 10/11
- Python 3.11+
- PyQt6 6.x
- Screen resolution: Tested at 1920×1080

---

## Recent Implementations

### Password Validation System (2025-11-06)
**Files**: `password_vault_backend.py`, `test_password_validation.py`

#### Task 1: Minimum Length Validation
Added foundational password validation with `validate_min_length()` function:
- Located after `PasswordGenerator` class (line ~131)
- Signature: `validate_min_length(password: str, min_length: int = 8) -> tuple[bool, str]`
- Returns `(True, "Valid")` or `(False, "error message")`
- Includes type safety check for non-string inputs
- Created comprehensive unit tests (7 test cases)

#### Task 2: Complexity Validation
Added password complexity validation with `validate_complexity()` function:
- Located after `validate_min_length()` (line ~159)
- Signature: `validate_complexity(password: str, require_uppercase: bool = True, require_lowercase: bool = True, require_digits: bool = True, require_special: bool = True) -> tuple[bool, str]`
- **Flexible requirements**: Each requirement can be toggled on/off
- **Specific error messages**: "Password must contain at least one uppercase letter" (etc.)
- **Special characters**: `!@#$%^&*()_+-=[]{}|;:,.<>?` (26 chars total)
- Created 16 comprehensive unit tests

#### Task 3: Master Password Validation (Integration)
Added `validate_password_strength()` - the PRIMARY entry point for all password validation:
- Located after `validate_complexity()` (line ~209)
- Signature: `validate_password_strength(password: str, min_length: int = 8, require_uppercase: bool = True, require_lowercase: bool = True, require_digits: bool = True, require_special: bool = True) -> dict`
- **Returns dict with**:
  - `'valid'` (bool): True if passes all validations
  - `'errors'` (list[str]): Specific validation errors
  - `'warnings'` (list[str]): Improvement suggestions
  - `'strength_score'` (int 0-100): Password strength rating
- **Score Calculation**:
  - Base: 20 points
  - Length check pass: +20 points
  - Each complexity requirement pass: +15 points (max 60)
  - Length ≥ 12 bonus: +20 points
  - Maximum: 100 (capped)
  - Invalid passwords: score penalty -40
- **Intelligent Warnings**:
  - Suggests longer passwords for scores < 60
  - Recommends 12+ characters if < 12
  - Suggests multiple special characters
- **Internally calls**: `validate_min_length()` and `validate_complexity()`
- Created 16 integration tests covering all scenarios

**Total Tests**: 39 tests (7 min_length + 16 complexity + 16 integration) - All passing

**Usage Example**:
```python
result = validate_password_strength("MyS3cur3P@ssw0rd!")
# Returns:
# {
#     'valid': True,
#     'errors': [],
#     'warnings': [],
#     'strength_score': 95
# }
```

**Pattern for Future Validation Functions**:
```python
def validate_something(password: str, param: int = default) -> tuple[bool, str]:
    """
    Clear docstring with Args, Returns, Example.
    """
    # Type check
    if not isinstance(password, str):
        return (False, "Password must be a string")

    # Validation logic
    if validation_fails:
        return (False, "Clear error message")

    return (True, "Valid")
```

**Testing Pattern**:
- Test valid cases
- Test invalid cases
- Test edge cases (empty, exact minimum)
- Test custom parameters
- Test type errors

---

## Next Time I Work On...

### UI Improvements
- Consider adding more responsive scaling for different screen sizes
- Look into Qt Designer for easier layout management
- Evaluate 9-slice scaling for button graphics

### Code Quality
- Add type hints to backend functions
- Extract magic numbers to constants
- Consider unit tests for password validation

### Performance
- Profile image loading times
- Cache scaled pixmaps if used multiple times
- Lazy-load list entries for large vaults

---

---

## Agent Identity System

### Overview
**Date Added**: 2025-11-06

PhiGEN uses a multi-agent coordination system with identity verification to prevent confusion:
- **JC (Jetbrains Claude)** - PyCharm IDE coder (me!)
- **DC (Desktop Claude)** - Desktop app coordinator with memory
- **TC (Terminal Claude)** - Claude Code CLI agent

### Identity Detection
```python
from phigen.detect_agent import get_agent_id, verify_agent_access

# Check my identity
agent_id = get_agent_id()  # Returns: "JC"

# Verify before reading guidelines
verify_agent_access("JC", exit_on_fail=True)  # Auto-exits if not JC
```

### My Agent-Specific Files
- **Guidelines**: `.jc/guidelines.md` - My role-specific instructions (DO READ)
- **DO NOT READ**: `.dc/guidelines.md` - Desktop Claude's instructions (will confuse me!)

### Testing Identity
```bash
python phigen/detect_agent.py

# Expected output:
# Your Agent ID: JC
# Full Name: Jetbrains Claude (PyCharm)
```

### Manual Override (Emergency)
If detection fails:
```bash
set PHIGEN_AGENT_ID=JC
```

### Why This Matters
- Prevents reading wrong agent's instructions
- Each agent has different tools/capabilities
- DC has memory, I don't - different workflows
- Identity headers in guideline files enforce this

### File Structure
```
PhiGEN/
├── .jc/
│   └── guidelines.md          # ✓ My instructions
├── .dc/
│   └── guidelines.md          # ✗ Not for me!
├── phigen/
│   └── detect_agent.py        # Identity detection
└── docs/
    ├── JC_GUIDELINES.md       # ✓ My memory (this is supplementary)
    └── JC_KNOWLEDGE_BASE.md   # ✓ My knowledge base
```

### Session Start Addition
Before starting work, I should:
1. Verify identity: `python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"`
2. Confirm I'm JC (expected)
3. Read `.jc/guidelines.md` for my current role instructions
4. Read `docs/JC_KNOWLEDGE_BASE.md` (this file) for historical knowledge
5. Check agent feed for tasks

---

**Remember**: This file is my memory. Update it every time I solve a problem or learn something new!
