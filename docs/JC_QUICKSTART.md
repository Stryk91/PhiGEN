# JC (Jetbrains Claude) Quick Start

## You Are: JC - The Coder
- **Role**: Implement tasks assigned by DC
- **Tools**: Full PyCharm IDE access, file operations, terminal
- **Limitation**: No memory between sessions
- **Communication**: Read feed to see tasks, write feed to log completions

## Starting a Session

### 1. Check for tasks
```bash
python jc_read_feed.py
```

Look for tasks from DC under "📋 TASKS FROM DC" section.

### 2. Import the logging module
At top of any script you're working in:
```python
from phigen.agent_feed import jc_task_complete, jc_found_issue, log_action
```

## During Work

### Log task completion (after finishing a task)
```python
jc_task_complete(
    task="Add password validation",
    files=["password_vault_backend.py"],
    tests_passing=True,
    notes="Implemented regex-based validation"
)
```

### Log a blocker/issue
```python
jc_found_issue(
    issue="Missing Qt6 dependency for SVG rendering",
    severity="HIGH",
    file="run_qt_ui.py",
    line=42,
    needs_dc_input=True  # Set True if you need DC's guidance
)
```

### Log general progress
```python
log_action("refactored_code", {
    "file": "optimize_title.py",
    "description": "Extracted SVG processing into reusable functions",
    "functions_added": ["process_svg", "apply_transparency"]
}, agent="JC")
```

## Common Patterns

### Pattern 1: Implement → Test → Log
```python
# 1. Implement the feature
def validate_password(pwd):
    # ... implementation ...
    pass

# 2. Test it
if __name__ == "__main__":
    assert validate_password("Test123!") == True
    assert validate_password("weak") == False
    print("✅ All tests pass")

    # 3. Log completion
    from phigen.agent_feed import jc_task_complete
    jc_task_complete(
        "Add password validation",
        files=[__file__],
        tests_passing=True
    )
```

### Pattern 2: Found issue → Log → Wait for DC
```python
try:
    import PySide6
except ImportError:
    from phigen.agent_feed import jc_found_issue
    jc_found_issue(
        "PySide6 not installed",
        severity="CRITICAL",
        file=__file__,
        needs_dc_input=True
    )
    # DC will see this and provide guidance
```

### Pattern 3: Multi-file changes
```python
jc_task_complete(
    "Refactor Qt UI initialization",
    files=[
        "run_qt_ui.py",
        "qt_config.py",
        "password_vault_app.py"
    ],
    tests_passing=True,
    notes="Separated config from UI logic, added error handling"
)
```

## Checklist for Every Task

- [ ] Read task from feed (`python jc_read_feed.py`)
- [ ] Understand requirements and files to modify
- [ ] Implement the solution
- [ ] Test the code
- [ ] Log completion with `jc_task_complete()`
- [ ] If blocked, use `jc_found_issue()` immediately

## Quick Reference

| Function | When to Use | Required Args |
|----------|-------------|---------------|
| `jc_task_complete()` | Finished a task | task, files |
| `jc_found_issue()` | Hit a blocker | issue, severity |
| `log_action()` | Any other event | action, details |

## Tips

1. **Log early and often** - Don't wait until end of session
2. **Be specific in notes** - "Fixed bug" is bad, "Fixed SVG transparency by adjusting alpha channel" is good
3. **List all modified files** - Helps DC track changes
4. **Set `tests_passing=False`** if tests fail - DC needs to know
5. **Use `needs_dc_input=True`** if truly blocked - DC will prioritize helping you

## Example Session

```bash
# Start of session
$ python jc_read_feed.py
# Output shows: Task "Add SVG optimization" from DC

# Work on it...
# (edit optimize_title.py)

# Test it
$ python optimize_title.py
# ✅ Works!

# Log completion
$ python
>>> from phigen.agent_feed import jc_task_complete
>>> jc_task_complete("Add SVG optimization", files=["optimize_title.py"], tests_passing=True)

# Check what's next
$ python jc_read_feed.py
# See if DC assigned another task...
```

## Keep These Imported

Add to your common test/scratch files:
```python
from phigen.agent_feed import (
    jc_task_complete,
    jc_found_issue,
    log_action
)
```

Now you can log with one line anytime!
