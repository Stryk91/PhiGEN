# Qt Designer Layout Quick Reference
## One-Page Cheat Sheet

---

## 🎯 The Core Rule
**Never use absolute positioning. Always use layouts.**

---

## 📐 Layout Types

| Layout | When to Use | Keyboard Shortcut |
|--------|-------------|-------------------|
| **QVBoxLayout** | Stack vertically (forms, menus) | Ctrl+L |
| **QHBoxLayout** | Arrange horizontally (button rows) | Ctrl+H |
| **QGridLayout** | Table-like (calculator, dashboard) | Ctrl+G |
| **QFormLayout** | Label:Input pairs (settings) | - |

---

## 🎛️ Size Policies (What They Mean)

| Policy | Behavior | Common Use |
|--------|----------|------------|
| **Fixed** | Never changes size | Icons, specific dimensions |
| **Minimum** | Can grow, won't shrink | Buttons with min clickable area |
| **Maximum** | Can shrink, won't grow | Small elements |
| **Preferred** | Wants sizeHint(), flexible | Default for most widgets |
| **Expanding** | Grabs all available space | Content areas, text displays |

---

## 🚨 Common Mistakes & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Red border in Designer | No layout | Right-click → Lay Out |
| Widget won't resize | Fixed size policy | Change to Expanding/Preferred |
| Widgets overlap | Absolute positioning | Put in layout |
| Uneven spacing | Default spacing | Set layout spacing property |
| Widget too small | Wrong size policy | Check min size + size policy |

---

## 🎨 PhiGEN Button Layout Pattern

```
QHBoxLayout or QGridLayout
└─ QPushButton (your custom image button)
   ├─ sizePolicy: H=Minimum, V=Fixed
   ├─ minimumSize: 200x60 (your button image size)
   └─ maximumSize: (none)x60 (fixed height, flexible width)
```

**In stylesheet:**
```css
QPushButton {
    border-image: url(button.png);
    min-width: 200px;
    min-height: 60px;
    max-height: 60px;
}
```

---

## 📱 Testing Your Layout

**In Qt Designer:**
- Form → Preview (Ctrl+R)
- Drag window edges

**In Code:**
```python
# Set resizable window
self.setMinimumSize(800, 600)
self.resize(1024, 768)
```

---

## ✅ PhiGEN Layout Checklist

```
Main Window:
├─ Central Widget
│  └─ QVBoxLayout (margins: 20px, spacing: 10px)
│     ├─ Title Label (V:Fixed, H:Expanding, centered)
│     ├─ Input rows (QHBoxLayout)
│     │  ├─ Labels (H:Minimum)
│     │  └─ Input fields (H:Expanding)
│     ├─ Button area (QGridLayout)
│     │  └─ All buttons (Expanding)
│     └─ Status bar (QHBoxLayout, V:Fixed)
└─ All widgets in layouts, no absolute positioning
```

---

## 🔧 Quick Commands in Designer

| Action | Method |
|--------|--------|
| Add layout | Right-click → Lay Out → [type] |
| Break layout | Right-click → Break Layout |
| Adjust size policy | Property Editor → sizePolicy |
| Set spacing | Property Editor → spacing |
| Set margins | Property Editor → margin |
| Add spacer | Widget Box → Spacers → Drag in |
| Preview | Form → Preview (Ctrl+R) |

---

## 💡 Golden Rules

1. ✅ **Always use layouts** (never absolute positions)
2. ✅ **Set size policies** to match intent (Fixed vs Expanding)
3. ✅ **Nest layouts** for complex UIs
4. ✅ **Use spacers** for spacing (not empty widgets)
5. ✅ **Test resizing** early and often
6. ✅ **Apply layout to central widget** (main window)

---

## 🔍 Debugging Steps

Widget won't resize?
1. Is it in a layout? (Blue border)
2. Check size policy (Fixed = won't change)
3. Check min/max size constraints
4. Check parent layout

Widgets overlap?
1. Not in layouts → Add layouts
2. Wrong z-order → Reorder in object tree

---

## 📏 Recommended Values for PhiGEN

```
Main Layout (QVBoxLayout):
- Margins: 20px all sides
- Spacing: 15px

Button Rows (QHBoxLayout):
- Spacing: 10px

Custom Buttons:
- Min size: 200x60 (match image)
- Size policy: H=Minimum, V=Fixed
- Max height: 60 (prevents vertical stretching)

Input Fields:
- Size policy: H=Expanding, V=Fixed
- Min height: 30-40px

Title:
- Size policy: H=Expanding, V=Fixed
- Alignment: AlignCenter
```

---

## 🛠️ Tools Available

```bash
# Analyze your .ui file structure
python analyze_ui_layout.py your_design.ui

# See detailed guide
# Read: QT_DESIGNER_LAYOUT_GUIDE.md
```

---

**Remember: Layouts = Responsive UI. No layouts = Broken UI.**
