# PhiGEN Agent Coordination System

## Overview

PhiGEN uses a simple JSONL feed system for coordination between:
- **JC (Jetbrains Claude)** - IDE agent in PyCharm, has file access & tools, does coding
- **DC (Desktop Claude)** - Desktop agent, has memory, does planning/tasking

## Architecture

```
┌─────────────────┐
│  DC (Desktop)   │  ← Memory, no tools
│ Prompt Engineer │
└────────┬────────┘
         │ (user runs dc_log_message.py)
         ↓
┌──────────────────────────────┐
│  agent-feed.jsonl (JSONL)    │  ← Shared state
│  E:\...\PhiGEN\docs\         │
└──────────────────────────────┘
         ↑
         │ (direct file access)
┌────────┴────────┐
│   JC (PyCharm)  │  ← Tools, no memory
│     Coder       │
└─────────────────┘
```

## Workflow

### 1. DC assigns a task
User runs:
```bash
python dc_log_message.py
```
Choose option 1 (Assign task), provide:
- Task description
- Priority (LOW/MEDIUM/HIGH)
- Files to modify
- Requirements

This logs to `docs/agent-feed.jsonl`:
```json
{
  "timestamp": "2025-11-06T...",
  "agent": "DC",
  "action": "task_assigned",
  "details": {
    "task": "Add password strength validation",
    "priority": "HIGH",
    "files_to_modify": ["password_vault_backend.py"],
    "requirements": ["Min 8 chars", "At least 1 number", "At least 1 special char"]
  }
}
```

### 2. JC reads tasks
In PyCharm terminal:
```bash
python jc_read_feed.py
```

Shows pending tasks from DC.

### 3. JC implements the task
JC codes the solution using PyCharm tools.

### 4. JC logs completion
**Option A - Python (recommended):**
```python
from phigen.agent_feed import jc_task_complete

jc_task_complete(
    task="Add password strength validation",
    files=["password_vault_backend.py"],
    tests_passing=True,
    notes="Added regex validation and user feedback"
)
```

**Option B - Terminal:**
```python
python -c "from phigen.agent_feed import jc_task_complete; jc_task_complete('Task desc', files=['file.py'])"
```

### 5. DC reviews and assigns next task
User checks feed, DC sees completion, plans next task, repeats cycle.

## File Reference

### Core Module
- **`phigen/agent_feed.py`** - Core logging utilities

### Helper Scripts
- **`dc_log_message.py`** - Interactive script for DC to log messages (run by user)
- **`jc_read_feed.py`** - Quick feed viewer for JC

### Feed File
- **`docs/agent-feed.jsonl`** - Append-only event log (JSONL format)

## Common Actions

### For DC (via user running script)

**Assign task:**
```bash
python dc_log_message.py
# Choose option 1
```

**Log feedback/question:**
```bash
python dc_log_message.py
# Choose option 2
```

### For JC (direct in PyCharm)

**Check tasks:**
```bash
python jc_read_feed.py
```

**Log task completion:**
```python
from phigen.agent_feed import jc_task_complete
jc_task_complete("Task name", files=["file.py"], tests_passing=True)
```

**Log issue/blocker:**
```python
from phigen.agent_feed import jc_found_issue
jc_found_issue(
    "Cannot find import for Qt module",
    severity="HIGH",
    file="run_qt_ui.py",
    line=42,
    needs_dc_input=True
)
```

**Custom log:**
```python
from phigen.agent_feed import log_action
log_action("refactored_code", {
    "file": "optimize_title.py",
    "description": "Extracted SVG processing to separate function"
}, agent="JC")
```

## Feed Entry Format

Every entry follows this structure:
```json
{
  "timestamp": "2025-11-06T12:34:56.789+00:00",  // ISO 8601 UTC
  "agent": "JC" | "DC" | "System",                // Who logged it
  "action": "task_assigned" | "task_complete" | ...,  // What happened
  "details": {                                    // Action-specific data
    ...
  }
}
```

### Common Actions

| Action | Agent | Details Keys |
|--------|-------|-------------|
| `task_assigned` | DC | task, priority, files_to_modify, requirements, notes |
| `task_complete` | JC | task, files, tests_passing, notes, commit_hash |
| `issue_found` | JC | issue, severity, file, line, needs_dc_input |
| `feedback` | DC | message, target, priority |
| `refactored_code` | JC | file, description |
| `question` | JC | question, context, urgency |

## Tips

### For JC
1. **Start each session** by running `python jc_read_feed.py` to see pending tasks
2. **Log frequently** - even small completions or blockers
3. **Use convenience functions** (`jc_task_complete`, `jc_found_issue`) for common actions
4. **Import at top of your test scripts** so you can log easily:
   ```python
   from phigen.agent_feed import jc_task_complete, jc_found_issue
   ```

### For DC (and user)
1. **Keep dc_log_message.py running** in a terminal for quick task assignments
2. **Be specific** in task descriptions - JC has no memory
3. **List requirements as checklist** - makes it clear what "done" means
4. **Check feed regularly** by looking at recent entries (option 3 in script)

### General
- Feed file is **append-only** - never delete entries (keep history)
- Feed file is **human-readable** - you can grep/search it easily
- **One entry per line** - easy to tail, parse, or analyze
- **UTC timestamps** - no timezone confusion

## Troubleshooting

**Q: Can't import phigen.agent_feed**
A: Make sure you're running from `E:\PythonProjects\PhiGEN` directory, or add it to Python path.

**Q: Feed file not found**
A: Run `python dc_log_message.py` once - it will create the file automatically.

**Q: How do I see what JC did last session?**
A: Run `python jc_read_feed.py --all` to see full history.

**Q: Can I edit the feed file manually?**
A: Yes, but be careful - it must remain valid JSONL (one JSON object per line).

**Q: How do I clean old entries?**
A: Archive them to a backup file, or leave them (disk space is cheap, history is valuable).

## Example Session

```bash
# DC (via user):
$ python dc_log_message.py
# Assigns: "Fix SVG transparency bug in optimize_title.py"

# JC (in PyCharm):
$ python jc_read_feed.py
# Sees task, starts working...

# JC implements fix...

# JC logs completion:
>>> from phigen.agent_feed import jc_task_complete
>>> jc_task_complete(
...     "Fix SVG transparency bug",
...     files=["optimize_title.py"],
...     tests_passing=True,
...     notes="Used convert_svg_transparent.py approach"
... )

# DC (via user):
$ python dc_log_message.py
# Sees completion in recent feed (option 3), assigns next task...
```

## Advanced: Programmatic Access

### Read feed programmatically
```python
from phigen.agent_feed import read_tail, read_all

# Last 10 entries
recent = read_tail(10)
for entry in recent:
    print(f"{entry['agent']}: {entry['action']}")

# All entries
all_entries = read_all()
print(f"Total activity: {len(all_entries)} entries")

# Filter by agent
jc_entries = [e for e in all_entries if e['agent'] == 'JC']
```

### Custom action types
```python
from phigen.agent_feed import log_action

# JC logs a refactoring
log_action("code_refactor", {
    "file": "password_vault_app.py",
    "description": "Extracted validation logic to separate module",
    "lines_changed": 150,
    "functions_added": ["validate_password", "check_strength"]
}, agent="JC")

# DC logs a design decision
log_action("design_decision", {
    "decision": "Use Qt6 instead of Qt5",
    "rationale": "Better performance and modern features",
    "affected_files": ["qt_config.py", "run_qt_ui.py"]
}, agent="DC")
```

## Integration with Other Tools

### Git commits
```python
# JC after committing
import subprocess
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()

jc_task_complete(
    "Implement password strength meter",
    files=["password_vault_backend.py", "password_vault_app.py"],
    commit_hash=commit,
    tests_passing=True
)
```

### PyCharm run configurations
Create a run configuration for `jc_read_feed.py` for quick access.

### Terminal aliases (optional)
```bash
# In ~/.bashrc or ~/.bash_profile
alias jc-feed='cd /e/PythonProjects/PhiGEN && python jc_read_feed.py'
alias dc-log='cd /e/PythonProjects/PhiGEN && python dc_log_message.py'
```
