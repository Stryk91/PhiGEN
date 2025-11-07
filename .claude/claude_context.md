# PhiGEN Project Context for Claude

## Project Overview
- Password manager called PhiGEN
- PyQt6 GUI application
- Security-focused (AES-256, Zero-Trust, Mil-Spec)

## Key Paths
- Python: E:\PythonProjects\PhiGEN\venv\Scripts\python.exe
- Project Root: E:\PythonProjects\PhiGEN\
- cairosvg: Installed in venv

## Design Decisions
- Font: White Rabbit (custom font)
- Colors: #00FF00 (green), #0d0d0d (black)
- UI Style: Tactical/military/circuit board aesthetic
- Title banner: 1400×200, metallic chrome with circuit traces

## Common Issues & Solutions
- Always use venv Python (not system Python)
- Export SVG: Use Firefox screenshot method (8× super-sampling)
- Shadow blur: stdDeviation="20" (sweet spot)
```

**Then tell Claude Coder:**
```
"Read claude_context.md for project background before starting"