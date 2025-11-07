# JC Guidelines - PhiGEN Project

**Last Updated**: 2025-11-06
**Agent**: JC (Jetbrains Claude - PyCharm IDE Agent)

## Project Overview
PhiGEN is a password vault application with a tactical cyberpunk UI aesthetic featuring:
- AES-256 encryption for password storage
- PyQt6/PySide6 based GUI with custom graphics
- SVG-based UI elements with chrome/metallic styling
- Green circuit board theme (#39ff14 accent color)

**Project Location**: `E:\PythonProjects\PhiGEN\`

## Project Structure

```
PhiGEN/
├── docs/                           # Documentation and coordination
│   ├── agent-feed.jsonl           # JC ↔ DC communication log
│   ├── JC_GUIDELINES.md           # This file
│   └── JC_KNOWLEDGE_BASE.md       # Problem solutions index
├── phigen/                        # Core package
│   └── agent_feed.py             # Feed utilities
├── TEMPSVG/                       # UI assets and working files
│   ├── *.svg                     # Source graphics
│   ├── *.png                     # Rendered UI elements
│   └── password_vault_complete_IMPROVED.py  # MAIN WORKING UI
├── ui/                            # Qt Designer files
│   └── password_vault_IMPROVED.ui
├── password_vault_backend.py      # Core vault logic
└── *.py                          # Various utilities

```

## Key Files

### Main Application
- **`TEMPSVG/password_vault_complete_IMPROVED.py`** - PRIMARY working UI (1125×740px window)
- **`password_vault_backend.py`** - PasswordVault class, encryption, storage
- **`phigen/agent_feed.py`** - Agent coordination utilities

### UI Assets
- **`TEMPSVG/PHIGEN_TITLE_FINAL.png`** - High-res title (7144×1224) - DO NOT RESIZE
- **`TEMPSVG/circuit_background_opacity_15.png`** - Background texture
- **`TEMPSVG/buttons.qrc`** - Qt resource file
- **`TEMPSVG/buttons_rc.py`** - Compiled Qt resources

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where beneficial
- Docstrings for public methods
- Keep functions under 50 lines when possible

### Qt/GUI Code
- PyQt6 for main UI (not PySide6 unless specified)
- Use `QPixmap.scaled()` with `Qt.TransformationMode.SmoothTransformation` for high-quality image scaling
- **CRITICAL**: Never resize high-res images on disk - always scale in Qt at display time
- Color scheme: Dark (#0a0a0a) background, neon green (#39ff14) accents
- Monospace fonts: 'Xolonium', 'Courier New'

### Image Handling Rules
1. **High-res sources stay high-res** - Never downscale PNG files
2. **Qt handles display scaling** - Use `QPixmap.scaled()` for display
3. **Compression only** - If optimizing file size, use PNG compression (`optimize=True, compress_level=9`)
4. **Aspect ratio preservation** - Always use `Qt.AspectRatioMode.KeepAspectRatio`

### File Operations
- Use `Path` from `pathlib` for cross-platform paths
- Use forward slashes in stylesheets: `str(path).replace("\\", "/")`
- Check file existence before loading resources

## Testing Requirements
- Manual UI testing required (no automated tests yet)
- Test on Windows (primary platform)
- Verify window size: 1125×740 minimum
- Check all buttons load graphics correctly

## Common Patterns

### Loading High-Res Images in Qt
```python
from pathlib import Path
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Load high-res source
high_res_pixmap = QPixmap(str(Path("TEMPSVG/PHIGEN_TITLE_FINAL.png")))

# Scale for display
display_height = 100
aspect_ratio = high_res_pixmap.width() / high_res_pixmap.height()
display_width = int(display_height * aspect_ratio)

display_pixmap = high_res_pixmap.scaled(
    display_width,
    display_height,
    Qt.AspectRatioMode.KeepAspectRatio,
    Qt.TransformationMode.SmoothTransformation
)

label.setPixmap(display_pixmap)
```

### Using Agent Feed
```python
from phigen.agent_feed import jc_task_complete, jc_found_issue, read_tail

# Check recent entries
recent = read_tail(20)

# Log completion
jc_task_complete(
    task="Description of work",
    files=["file1.py", "file2.py"],
    tests_passing=True,
    notes="Additional context"
)

# Log blocker
jc_found_issue(
    issue="Problem description",
    severity="HIGH",
    needs_dc_input=True
)
```

## Session Start Checklist
1. ✓ **Verify identity**: `python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"` (expect: JC)
2. ✓ **Read agent-specific guidelines**: `.jc/guidelines.md` (my role instructions)
3. ✓ **Read this guidelines file**: `docs/JC_GUIDELINES.md` (project-specific)
4. ✓ **Read knowledge base**: `docs/JC_KNOWLEDGE_BASE.md` (historical solutions)
5. ✓ **Read agent feed**: `from phigen.agent_feed import read_tail; read_tail(20)` (check for tasks)
6. ✓ Check git status if applicable
7. ✓ Review open files in IDE

### Agent Identity Verification
**CRITICAL**: Always verify I'm JC before reading guidelines:
```python
from phigen.detect_agent import verify_agent_access
verify_agent_access("JC", exit_on_fail=True)
```

**My Files**:
- ✓ `.jc/guidelines.md` - Read this
- ✗ `.dc/guidelines.md` - NEVER read (DC's instructions will confuse me)

## Don't Forget
- Update knowledge base after solving new problems
- Log all completed tasks to agent feed
- Ask DC for clarification via `jc_found_issue()` when blocked
- Keep this guidelines file updated with new patterns
