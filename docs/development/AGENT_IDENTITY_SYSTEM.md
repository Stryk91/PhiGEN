# PhiGEN Agent Identity System

**Prevents agents from reading each other's guidelines and getting confused.**

---

## Problem Solved

Multiple Claude instances work on PhiGEN:
- **JC** (Jetbrains Claude in PyCharm) - Has tools, implements code
- **DC** (Desktop Claude for Windows) - Has memory, plans work

Each agent has **different instructions** in their guideline files. If JC reads DC's guidelines (or vice versa), they get confused about their role.

**Solution:** Identity headers at the top of each guideline file that check "am I the right agent for this?"

---

## How It Works

### 1. Agent Detection (`phigen/detect_agent.py`)

Python module that detects which Claude is running:

```python
from phigen.detect_agent import get_agent_id

agent = get_agent_id()
# Returns: "JC", "DC", "TC", or "UNKNOWN"
```

**Detection Logic:**
- Checks environment variable: `PHIGEN_AGENT_ID`
- Checks executable path (Desktop Claude at `AppData\Local\AnthropicClaude`)
- Checks command line (Terminal Claude runs `claude-code/cli.js`)
- Checks working directory (PhiGEN project = likely JC)

### 2. Identity Headers in Guideline Files

Each agent-specific guideline has a header:

**`.dc/guidelines.md` (for Desktop Claude):**
```markdown
⚠️  AGENT IDENTITY CHECK ⚠️

REQUIRED AGENT ID: DC (Desktop Claude - Windows App)

IF YOU ARE NOT DESKTOP CLAUDE, STOP READING THIS FILE NOW.

To verify: python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"
Expected output: DC

If you see JC, TC, or UNKNOWN, EXIT IMMEDIATELY.
```

**`.jc/guidelines.md` (for Jetbrains Claude):**
```markdown
⚠️  AGENT IDENTITY CHECK ⚠️

REQUIRED AGENT ID: JC (Jetbrains Claude - PyCharm IDE)

IF YOU ARE NOT JETBRAINS CLAUDE IN PYCHARM, STOP READING THIS FILE NOW.

To verify: python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"
Expected output: JC

If you see DC, TC, or UNKNOWN, EXIT IMMEDIATELY.
```

### 3. Programmatic Verification (Optional)

For Python scripts that should only run for specific agents:

```python
from phigen.detect_agent import verify_agent_access

# Option 1: Check and continue
if not verify_agent_access("JC"):
    print("This script is for JC only, exiting...")
    exit(0)

# Option 2: Auto-exit on failure
verify_agent_access("JC", exit_on_fail=True)  # Exits if not JC
```

---

## File Structure

```
PhiGEN/
├── .dc/
│   └── guidelines.md          # DC (Desktop Claude) instructions
├── .jc/
│   └── guidelines.md          # JC (Jetbrains Claude) instructions
├── phigen/
│   └── detect_agent.py        # Detection module
└── AGENT_IDENTITY_SYSTEM.md   # This file
```

---

## Agent IDs

| ID | Name | Environment | Capabilities |
|----|------|-------------|--------------|
| **JC** | Jetbrains Claude | PyCharm IDE | Tools: ✓ Memory: ✗ Files: ✓ |
| **DC** | Desktop Claude | Windows App | Tools: ✗ Memory: ✓ Files: ✗ |
| **TC** | Terminal Claude | Claude Code CLI | Tools: ✓ Memory: ✗ Files: ✓ |

---

## Usage Guide

### For DC (Desktop Claude)

**Your guideline file:** `.dc/guidelines.md`

**To verify your identity** (ask user to run):
```bash
python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"
```

Expected output: `DC`

**If you see this file and you're NOT DC:**
- **STOP reading immediately**
- This file will confuse you
- Ask user which agent you are
- Read the correct guideline file

### For JC (Jetbrains Claude)

**Your guideline file:** `.jc/guidelines.md`

**To verify your identity** (run in PyCharm terminal):
```bash
python -c "from phigen.detect_agent import get_agent_id; print(get_agent_id())"
```

Expected output: `JC`

**If you see this file and you're NOT JC:**
- **STOP reading immediately**
- This file will confuse you
- Find out which agent you are
- Read the correct guideline file

### For TC (Terminal Claude)

If Terminal Claude needs guidelines in the future, create `.tc/guidelines.md` with:
- Identity header checking for `TC`
- Role-specific instructions

---

## Manual Override

If auto-detection fails, manually set agent ID:

**Option 1: Environment Variable**
```bash
# Windows CMD
set PHIGEN_AGENT_ID=JC

# Windows PowerShell
$env:PHIGEN_AGENT_ID="JC"

# Bash
export PHIGEN_AGENT_ID=JC
```

**Option 2: Python Code**
```python
from phigen.detect_agent import set_agent_id
set_agent_id("JC")  # Force identify as JC
```

---

## Testing the System

### Test Detection
```bash
cd E:\PythonProjects\PhiGEN
python phigen/detect_agent.py
```

Output shows:
- Your detected agent ID
- Full agent name
- Executable path
- Environment hints
- Verification test results

### Test Verification
```python
from phigen.detect_agent import verify_agent_access

# Check without exiting
if verify_agent_access("JC"):
    print("I am JC!")
else:
    print("I am NOT JC")

# Check with auto-exit
verify_agent_access("JC", exit_on_fail=True)
# (exits if not JC)
```

---

## Detection Logic Details

### Priority Order

1. **Environment Variable** (`PHIGEN_AGENT_ID`)
   - Highest priority
   - Manual override
   - Example: `PHIGEN_AGENT_ID=JC`

2. **Process Name/Path**
   - Desktop Claude: `AnthropicClaude\app-*/claude.exe`
   - Terminal Claude: `node.exe` running `claude-code/cli.js`

3. **Environment Markers**
   - PyCharm: `PYCHARM_HOSTED`, `JETBRAINS_IDE` variables

4. **Working Directory**
   - PyCharm projects often have `.idea` folder
   - PhiGEN directory suggests JC

5. **Default**: `UNKNOWN`

### Detection Code

```python
def get_agent_id() -> str:
    # 1. Check env var
    if os.getenv("PHIGEN_AGENT_ID"):
        return os.getenv("PHIGEN_AGENT_ID").upper()

    # 2. Check process paths
    if "claude-code" in sys.argv:
        return "TC"
    if "AnthropicClaude" in sys.executable:
        return "DC"

    # 3. Check PyCharm markers
    if os.getenv("PYCHARM_HOSTED") or "pycharm" in os.getenv("PATH", ""):
        return "JC"

    # 4. Check working directory
    if "pycharm" in os.getcwd().lower() or ".idea" in os.getcwd():
        return "JC"

    return "UNKNOWN"
```

---

## Why This Matters

### Without Identity System
```
DC reads .jc/guidelines.md by accident
  → Thinks it has PyCharm tools
  → Tries to execute code directly
  → Fails, gets confused

JC reads .dc/guidelines.md by accident
  → Thinks it should only plan, not implement
  → Waits for user to assign tasks
  → Doesn't use its tools
```

### With Identity System
```
DC opens .jc/guidelines.md
  → Sees "REQUIRED AGENT ID: JC"
  → Verifies: "I am DC, not JC"
  → Stops reading immediately
  → No confusion!

JC opens .jc/guidelines.md
  → Sees "REQUIRED AGENT ID: JC"
  → Verifies: "I am JC"
  → Reads the file
  → Gets correct instructions
```

---

## Integration with Other Systems

### Agent Feed System

The agent feed uses agent names:
- DC logs as: `agent="DC"`
- JC logs as: `agent="JC"`

These should match the detected agent IDs.

### Can Auto-Set Agent Name

```python
from phigen.detect_agent import get_agent_id
from phigen.agent_feed import log_action

agent = get_agent_id()  # Auto-detect

log_action("hello", {
    "message": "I am active"
}, agent=agent)  # Use detected ID
```

---

## Troubleshooting

### Problem: Detection Returns "UNKNOWN"

**Solution 1:** Set environment variable
```bash
set PHIGEN_AGENT_ID=JC
```

**Solution 2:** Set in Python
```python
from phigen.detect_agent import set_agent_id
set_agent_id("JC")
```

### Problem: Wrong Agent Detected

Run diagnostic:
```bash
python phigen/detect_agent.py
```

Check output for hints about why detection chose that ID.

### Problem: Agent Reads Wrong Guidelines

Make sure identity headers are at the **very top** of guideline files. Agents should read the header before the rest of the file.

---

## Best Practices

1. **Always check identity** before reading agent-specific files
2. **Run detection test** at start of session: `python phigen/detect_agent.py`
3. **Use verification in scripts** that are agent-specific
4. **Keep headers prominent** - bold, warnings, can't miss them
5. **Exit immediately** if identity doesn't match

---

## Future Enhancements

### Possible Additions

1. **Config file detection** - Check `.phigen_config.json` for agent ID
2. **Git branch heuristics** - Different agents work on different branches?
3. **Stricter enforcement** - Make detection module required for all tools
4. **Identity cache** - Remember detected ID for session duration
5. **Multiple roles** - Agent can have multiple roles (JC+DC for super-user)

### Extensibility

Easy to add new agent types:

1. Add ID to detection logic in `detect_agent.py`:
```python
# Add detection for new agent type
if "my_new_ide" in sys.executable:
    return "NEW_AGENT"
```

2. Create guideline file: `.new_agent/guidelines.md`

3. Add header with identity check

Done!

---

## Summary

**What:** Identity system prevents agents from reading wrong guidelines
**How:** Detection module + identity headers in guideline files
**Why:** Prevents confusion, ensures correct role behavior
**Who:** JC (PyCharm coder), DC (Desktop planner), TC (Terminal helper)

**Files:**
- Detection: `phigen/detect_agent.py`
- DC Guidelines: `.dc/guidelines.md`
- JC Guidelines: `.jc/guidelines.md`

**Test It:**
```bash
python phigen/detect_agent.py
```

**Verify in Code:**
```python
from phigen.detect_agent import get_agent_id, verify_agent_access
print(f"I am: {get_agent_id()}")
verify_agent_access("JC", exit_on_fail=True)
```

---

**Identity system is production-ready!** 🎭
