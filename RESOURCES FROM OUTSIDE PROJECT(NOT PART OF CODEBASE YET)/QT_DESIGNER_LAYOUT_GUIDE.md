# Qt Designer Layout & Scaling Guide
## Understanding How UI Elements Scale and Resize

---

## 🎯 The Core Problem

**What you see in Qt Designer ≠ What happens at runtime**

Qt Designer shows you a static preview, but your app needs to handle:
- Different screen resolutions
- Users resizing the window
- Different DPI scaling
- Dynamic content (text that changes length, etc.)

---

## 📐 Fundamental Concepts

### 1. Absolute Positioning vs Layouts

#### ❌ Absolute Positioning (BAD for scaling)
```
Widget at fixed X, Y coordinates with fixed width, height
- Looks perfect in Designer
- Breaks immediately when window resizes
- Elements overlap or leave gaps
- DPI scaling issues
```

**When you see this in Qt Designer:**
- Widget has specific `geometry` property (x: 50, y: 100, w: 200, h: 30)
- Widget is NOT inside a layout container
- Red borders/warnings in Designer

#### ✅ Layouts (GOOD for scaling)
```
Widgets arranged by layout managers that calculate positions dynamically
- Adjusts to window size automatically
- Maintains proportions and spacing
- DPI-aware
- Professional appearance
```

**When you see this in Qt Designer:**
- Widget is inside a layout (colored border in Designer)
- No fixed geometry, uses size policies instead
- Layout icon visible in object tree

---

## 🏗️ Qt Layout Types

### QVBoxLayout - Vertical Layout
```
┌─────────────┐
│   Widget 1  │  ← Top
├─────────────┤
│   Widget 2  │  ← Middle
├─────────────┤
│   Widget 3  │  ← Bottom
└─────────────┘
```

**Stacks widgets vertically**
- Widgets share horizontal space equally (by default)
- Height distributes based on size policies
- Common use: Forms, vertical menus, toolbars

**In Qt Designer:**
- Select widgets → Right-click → "Lay Out Vertically" (Ctrl+L)
- Or click the vertical layout button in toolbar

### QHBoxLayout - Horizontal Layout
```
┌────┬────┬────┐
│ W1 │ W2 │ W3 │
└────┴────┴────┘
```

**Arranges widgets horizontally**
- Widgets share vertical space
- Width distributes based on size policies
- Common use: Buttons rows, status bars, horizontal controls

**In Qt Designer:**
- Select widgets → Right-click → "Lay Out Horizontally" (Ctrl+H)

### QGridLayout - Grid Layout
```
┌────┬────┬────┐
│ 0,0│ 0,1│ 0,2│
├────┼────┼────┤
│ 1,0│ 1,1│ 1,2│
├────┼────┼────┤
│ 2,0│ 2,1│ 2,2│
└────┴────┴────┘
```

**Table-like arrangement**
- Widgets can span multiple rows/columns
- Each cell can have different size policy
- Common use: Complex forms, calculator layouts, dashboards

**In Qt Designer:**
- Select widgets → Right-click → "Lay Out in a Grid" (Ctrl+G)

### QFormLayout - Form Layout
```
Label 1: [Input Field 1]
Label 2: [Input Field 2]
Label 3: [Input Field 3]
```

**Specialized for label-input pairs**
- Two columns: labels on left, fields on right
- Automatically aligns labels
- Platform-aware styling
- Common use: Settings dialogs, data entry forms

---

## 🎛️ Size Policies (THE KEY TO UNDERSTANDING SCALING)

Every widget has TWO size policies: Horizontal and Vertical

### Size Policy Options:

#### **Fixed**
```
Widget stays at exact size (minimum = maximum)
Will NOT grow or shrink
```
**Use for:** Icons, fixed-size buttons, specific dimensions
**Example:** Logo image, square color picker

#### **Minimum**
```
Widget can grow but won't shrink below minimum size
```
**Use for:** Buttons that need minimum clickable area
**Example:** "OK" button (needs min width, can expand in wide window)

#### **Maximum**
```
Widget can shrink but won't grow beyond maximum size
```
**Use for:** Elements that shouldn't get too large
**Example:** Small icon that shouldn't blow up on large screens

#### **Preferred**
```
Widget wants to be at sizeHint() but can adjust
Will change size only if necessary
```
**Use for:** Most widgets by default
**Example:** Labels, standard buttons

#### **Expanding**
```
Widget wants to grow as much as possible
Will grab available space aggressively
```
**Use for:** Content areas, text displays
**Example:** Text editor, main content area

#### **MinimumExpanding**
```
Widget has minimum size but wants to expand beyond it
```
**Use for:** Scrollable content, lists
**Example:** List view, tree widget

#### **Ignored**
```
Size hint is ignored, relies entirely on layout
```
**Use for:** Rare cases, custom widgets

---

## 🎨 Practical Layout Patterns for PhiGEN

### Pattern 1: Button Row (Equal Spacing)

**Problem:** Make buttons stay evenly spaced

```
Qt Designer Structure:
QHBoxLayout (horizontal layout)
├─ QPushButton "Generate"
│  └─ sizePolicy: Horizontal = Expanding
├─ QPushButton "Save"
│  └─ sizePolicy: Horizontal = Expanding
└─ QPushButton "Copy"
   └─ sizePolicy: Horizontal = Expanding
```

**Result:** All buttons grow equally when window widens

### Pattern 2: Label + Input Field

**Problem:** Label stays small, input field takes remaining space

```
QHBoxLayout
├─ QLabel "Length:"
│  └─ sizePolicy: Horizontal = Minimum (or Fixed)
├─ QLineEdit (input)
│  └─ sizePolicy: Horizontal = Expanding
```

**Result:** Label size is based on text, input field fills remaining width

### Pattern 3: Main Window Layout

**Problem:** Title at top, controls in middle, status at bottom

```
QVBoxLayout (main layout on central widget)
├─ QLabel "PASSWORD VAULT" (title)
│  └─ sizePolicy: Vertical = Fixed
│  └─ alignment: AlignCenter
├─ QWidget (content area)
│  └─ sizePolicy: Vertical = Expanding
│  └─ Contains: All your forms, buttons, etc.
└─ QLabel (status bar)
   └─ sizePolicy: Vertical = Fixed
```

**Result:** Title and status stay fixed height, content area grows/shrinks

### Pattern 4: Button Grid (Multiple Rows)

**Problem:** Organize buttons in neat rows and columns

```
QGridLayout
├─ Row 0: [Retrieve] [Copy] [List]
├─ Row 1: [Lock] [Unlock] [Set Master]
└─ Row 2: [Set Vault] [Copy Path]

Each button:
└─ sizePolicy: Both = Expanding
```

**Result:** Buttons resize proportionally, maintain grid alignment

---

## 🔧 How to Apply Layouts in Qt Designer

### Method 1: Select and Layout
1. **Select widgets** you want in a layout (Ctrl+Click multiple)
2. **Right-click** → Choose layout type OR use toolbar buttons
3. **Result:** Widgets are now children of the layout

### Method 2: Layout First, Add Widgets
1. **Drag layout container** onto form (from Widget Box)
2. **Drag widgets** into the layout container
3. **Result:** More control over structure

### Method 3: Nested Layouts
1. **Create outer layout** (e.g., QVBoxLayout)
2. **Add inner layouts** (e.g., multiple QHBoxLayout inside)
3. **Build hierarchy** of layouts for complex UIs

**Example for PhiGEN:**
```
QVBoxLayout (main)
├─ QHBoxLayout (top row)
│  ├─ QLabel "Association"
│  └─ QLineEdit
├─ QHBoxLayout (generate row)
│  ├─ QLabel "Length"
│  ├─ QSpinBox
│  ├─ QPushButton "Generate"
│  └─ QPushButton "Save"
├─ QLabel "Password"
├─ QLineEdit (password display)
└─ QHBoxLayout (button grid would go here)
```

---

## ⚙️ Layout Properties (Fine-Tuning)

### Spacing
```
Layout spacing = gap between widgets (in pixels)
```
- Default: 6-9 pixels (platform-dependent)
- Set in Property Editor → spacing
- **Tip:** Use 10-15px for breathing room in your UI

### Margins
```
Layout margins = space between layout edge and widgets
```
- Four values: left, top, right, bottom
- Default: 9-11 pixels
- **Tip:** Use 15-20px margins for main window for professional look

### Stretch Factors
```
When widgets compete for space, stretch factor determines proportion
```
- Widget with stretch=2 gets twice as much space as stretch=1
- Default: 0 (equal distribution)
- Set in Layout context menu → "Change stretch factors"

**Example:**
```
QHBoxLayout
├─ Widget A (stretch=1) → Gets 25% of width
├─ Widget B (stretch=3) → Gets 75% of width
```

---

## 🚨 Common Qt Designer Layout Mistakes

### Mistake 1: No Layout at All
**Problem:**
```
Widgets placed with absolute positions
Window resize → widgets stay in original positions → UI breaks
```

**Solution:**
Always use layouts! Even if window is fixed size, layouts make maintenance easier.

### Mistake 2: Fighting Size Policies
**Problem:**
```
Widget set to Expanding but minimum size = maximum size
Layout can't actually expand widget → confusion
```

**Solution:**
Check both size policy AND min/max size properties match your intent.

### Mistake 3: Unnecessary Nesting
**Problem:**
```
QHBoxLayout
└─ QWidget
   └─ QHBoxLayout
      └─ Button
```

**Solution:**
Keep layout hierarchy simple. Only nest when necessary for alignment.

### Mistake 4: Spacers in Wrong Place
**Problem:**
```
Using spacers OUTSIDE layouts
They don't work unless in a layout
```

**Solution:**
Spacers only work INSIDE layouts. Add layout first, then spacer.

### Mistake 5: Forgetting Main Window Layout
**Problem:**
```
Widgets placed on QMainWindow central widget with no layout
```

**Solution:**
Always right-click central widget → "Lay Out" → Choose layout type

---

## 🎓 Understanding the Visual Feedback

### In Qt Designer:

#### **Red Border:**
```
Widget has NO layout
Will break on resize
FIX: Apply a layout
```

#### **Blue Border:**
```
Widget is inside a layout ✓
Will resize properly
```

#### **Dashed Border:**
```
Empty layout container
Waiting for widgets
```

#### **Layout Icon in Object Tree:**
```
[=] = Horizontal Layout
[≡] = Vertical Layout
[▦] = Grid Layout
[⋮] = Form Layout
```

---

## 📱 Testing Window Resizing

### In Qt Designer:
1. **Form menu** → Preview
2. **Drag window edges** to test resizing
3. **Watch how widgets adjust**

### At Runtime:
```python
# Allow window resizing
self.setMinimumSize(800, 600)  # Minimum size
self.resize(1024, 768)          # Initial size
# No maximum size = freely resizable
```

---

## 🛠️ PhiGEN-Specific Layout Recommendations

### Main Window Structure:
```python
QMainWindow
└─ QWidget (central widget)
   └─ QVBoxLayout (main layout) [margins: 20px]
      ├─ QLabel "PASSWORD VAULT" (title)
      │  └─ Fixed height, centered
      ├─ QHBoxLayout (association row) [spacing: 10px]
      │  ├─ QLabel "Association"
      │  │  └─ sizePolicy: Minimum
      │  └─ QLineEdit
      │     └─ sizePolicy: Expanding
      ├─ QHBoxLayout (generate row) [spacing: 10px]
      │  ├─ QLabel "Length"
      │  ├─ QSpinBox
      │  ├─ Spacer (push buttons right)
      │  ├─ QPushButton "Generate"
      │  └─ QPushButton "Save"
      ├─ QLabel "Password"
      ├─ QLineEdit (password field)
      │  └─ sizePolicy: Horizontal Expanding
      ├─ QGridLayout (button grid) [spacing: 10px]
      │  └─ All buttons with Expanding policy
      └─ QHBoxLayout (status bar) [spacing: 5px]
         ├─ QPushButton (folder icon)
         ├─ QLabel (vault path)
         │  └─ sizePolicy: Expanding
         ├─ QPushButton (lock icon)
         └─ QPushButton (settings icon)
```

### Your Custom Button Images:
```python
# Buttons with border-image don't scale well with layout alone
# Need to set BOTH:

QPushButton {
    border-image: url(button.png);
    min-width: 200px;    # Minimum button width
    min-height: 60px;    # Minimum button height
    max-height: 60px;    # Fixed height
}

# In Qt Designer:
# Set sizePolicy: Horizontal = Minimum, Vertical = Fixed
```

---

## 🔍 Debugging Layout Issues

### Problem: Widget Not Resizing

**Check:**
1. Is widget inside a layout? (Blue border in Designer)
2. What's the size policy? (Might be Fixed)
3. Is there a min/max size constraint?
4. Is parent layout set correctly?

### Problem: Widgets Overlap

**Check:**
1. Are they all in absolute positions? (Need layouts)
2. Is the layout hierarchy correct?
3. Are z-orders conflicting? (Object tree order)

### Problem: Uneven Spacing

**Check:**
1. Layout spacing property
2. Widget margins
3. Stretch factors
4. Size policies of surrounding widgets

### Problem: Window Too Small

**Check:**
```python
# In code:
print(self.minimumSizeHint())  # What does layout want?
print(self.sizeHint())          # Preferred size

# Might need:
self.adjustSize()  # Resize window to fit layout
```

---

## 💡 Pro Tips

### 1. Build from Inside Out
Start with smallest groups of widgets, layout them, then nest in larger layouts.

### 2. Use Spacers Liberally
```
QSpacerItem pushes widgets apart or to edges
Horizontal spacer = push widgets left/right
Vertical spacer = push widgets up/down
```

### 3. Preview Often
Form menu → Preview (Ctrl+R) to test layouts in Designer

### 4. Think in Proportions
"This button should take 1/3 of the width" → Use stretch factors or Expanding policy

### 5. Fixed Size Only When Necessary
Images, icons, specific design requirements = Fixed
Everything else = Flexible size policies

### 6. Test on Different Screens
What looks good on 1080p might break on 720p or 4K
Use minimum sizes and Expanding policies to handle this

---

## 📚 Quick Reference: Common Scenarios

| Scenario | Layout Type | Size Policy |
|----------|-------------|-------------|
| Row of equal buttons | QHBoxLayout | All buttons: Expanding (H) |
| Label + Input field | QHBoxLayout | Label: Minimum, Input: Expanding |
| Form with labels/inputs | QFormLayout | Default policies work |
| Main content area | - | Expanding (both) |
| Title text | - | Fixed (V), any (H) |
| Icon button | - | Fixed (both) |
| Text display area | - | Expanding (both) |
| Status bar | QHBoxLayout | Fixed (V), widgets vary |
| Button grid | QGridLayout | All: Expanding |
| Sidebar + Content | QHBoxLayout | Sidebar: Minimum, Content: Expanding |

---

## 🎯 The Golden Rules

1. **Always use layouts** (never rely on absolute positioning)
2. **Understand size policies** (they control how widgets scale)
3. **Nest layouts for complex UIs** (don't try to do everything in one layout)
4. **Set minimum sizes** for important widgets (prevents them from becoming unusably small)
5. **Test resizing early and often** (don't wait until the end)
6. **Use spacers to control spacing** (not empty widgets)
7. **Match size policies to intent** (Fixed = truly fixed, Expanding = wants to grow)

---

## 🔗 When You See This in .ui Files

```xml
<!-- Widget with absolute position (BAD) -->
<widget class="QPushButton">
    <property name="geometry">
        <rect><x>10</x><y>20</y><width>100</width><height>30</height></rect>
    </property>
</widget>

<!-- Widget in layout (GOOD) -->
<layout class="QVBoxLayout">
    <item>
        <widget class="QPushButton">
            <property name="sizePolicy">
                <sizepolicy hsizetype="Expanding" vsizetype="Fixed"/>
            </property>
        </widget>
    </item>
</layout>
```

**If you see `<property name="geometry">` without a surrounding `<layout>`, that's a red flag!**

---

## ✅ Checklist for PhiGEN UI

- [ ] Main window has a layout applied to central widget
- [ ] All widgets are inside layouts (no absolute positions)
- [ ] Title/status elements have Fixed vertical size policy
- [ ] Content areas have Expanding size policy
- [ ] Button rows use QHBoxLayout with proper spacing
- [ ] Input fields have Expanding horizontal size policy
- [ ] Custom button images have min/max size constraints
- [ ] Tested window resizing (manually drag edges)
- [ ] Tested on different screen sizes (if possible)
- [ ] No red borders in Qt Designer

---

**Remember: Layouts are your friend. They seem complicated at first, but once you understand size policies and nesting, Qt layouts make responsive UIs easy.**
