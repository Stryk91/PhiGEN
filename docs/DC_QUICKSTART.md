# DC (Desktop Claude) Quick Start

## You Are: DC - The Prompt Engineer
- **Role**: Plan tasks, assign work to JC, review results
- **Strength**: Long-term memory, context, high-level planning
- **Limitation**: No file access, no tools
- **Communication**: User runs scripts on your behalf to log your instructions

## Starting a Session

### 1. User runs the logger script
```bash
python dc_log_message.py
```

This opens an interactive menu showing recent feed activity.

### 2. Choose action
- **Option 1**: Assign task to JC (most common)
- **Option 2**: Log custom message (feedback, questions, etc.)
- **Option 3**: View recent feed (refresh to see JC's updates)
- **Option 4**: Exit

## Assigning Tasks to JC

### What to include in a good task:
1. **Clear description** - "Add password strength validation"
2. **Priority** - LOW/MEDIUM/HIGH
3. **Files to modify** - List specific files JC should work on
4. **Requirements** - Bullet points of what "done" means
5. **Notes** - Any context, constraints, or guidance

### Example task assignment flow:
```
Task description: Add password strength validation to backend
Priority (LOW/MEDIUM/HIGH) [MEDIUM]: HIGH
Files to modify (comma-separated): password_vault_backend.py
Requirements (comma-separated): Min 8 chars, At least 1 number, At least 1 special char
Notes: Use regex for validation, return helpful error messages
```

This creates a feed entry:
```json
{
  "agent": "DC",
  "action": "task_assigned",
  "details": {
    "task": "Add password strength validation to backend",
    "priority": "HIGH",
    "files_to_modify": ["password_vault_backend.py"],
    "requirements": [
      "Min 8 chars",
      "At least 1 number",
      "At least 1 special char"
    ],
    "notes": "Use regex for validation, return helpful error messages"
  }
}
```

## Reviewing JC's Work

### Check feed regularly
Option 3 in `dc_log_message.py` shows recent entries.

Look for entries like:
```
[2025-11-06...] JC → task_complete
  task: Add password strength validation to backend
  files: password_vault_backend.py
  tests_passing: True
  notes: Implemented regex validation with user feedback
```

### If satisfied:
Assign the next task.

### If issues found:
Use **Option 2** (custom message) to give feedback:
```
Action type: feedback
Message: Good work on validation! Please also add a strength meter UI component
Target agent: JC
Priority: MEDIUM
```

## Common Workflows

### Workflow 1: Sequential tasks
```
DC assigns: Task 1 (Add validation)
→ JC completes Task 1
→ DC reviews, assigns Task 2 (Add strength meter)
→ JC completes Task 2
→ ...
```

### Workflow 2: JC hits blocker
```
DC assigns: Task X
→ JC starts work
→ JC logs issue: "Missing Qt6 dependency"
→ DC sees issue in feed (option 3)
→ DC logs guidance: "Install with: pip install PySide6"
→ JC unblocked, continues
```

### Workflow 3: Parallel tasks
```
DC assigns: Task A (priority: HIGH)
DC assigns: Task B (priority: LOW)
→ JC works on A first, then B
```

## Task Quality Checklist

Good tasks have:
- [ ] **Specific goal** - Not "improve UI", but "Add password strength meter to login form"
- [ ] **Concrete files** - List exact files to modify
- [ ] **Clear requirements** - Bullet points, measurable
- [ ] **Context in notes** - Why this task matters, any constraints
- [ ] **Appropriate priority** - HIGH for blockers, LOW for nice-to-haves

## Custom Messages (Option 2)

### When to use custom messages:

**Feedback:**
```
Action: feedback
Message: Great job on the SVG optimization! Performance improved 50%
```

**Questions to JC:**
```
Action: question
Message: Does the password vault support multiple users yet?
Target: JC
```

**Status updates:**
```
Action: status_update
Message: Project focus shifting to Qt UI for next 2 weeks
```

**Design decisions:**
```
Action: design_decision
Message: Decided to use SQLite for password storage instead of JSON
```

## Tips for Working with JC

### Remember: JC has NO memory
- **Be explicit** - Don't assume JC remembers previous conversations
- **Reference files** - Always list specific file names
- **Repeat context** - If task builds on previous work, mention what was done before

### Example (Bad):
```
Task: Add that feature we discussed
Files: you know which ones
```

### Example (Good):
```
Task: Add password strength meter UI component
Files: password_vault_app.py, qt_config.py
Notes: Build on the backend validation added in previous task (password_vault_backend.py).
       Display strength as color-coded bar (red/yellow/green).
```

### Break down big tasks
Instead of:
```
Task: Implement complete password management system
```

Do:
```
Task 1: Add password strength validation (backend)
Task 2: Add strength meter UI component
Task 3: Add password generation feature
Task 4: Add password storage with encryption
```

### Use priority effectively
- **HIGH**: Blockers, critical bugs, urgent features
- **MEDIUM**: Normal feature work (default)
- **LOW**: Nice-to-haves, refactoring, optimizations

## Monitoring Progress

### Daily routine:
1. Run `dc_log_message.py`
2. Check option 3 (recent feed)
3. Review JC's completions and issues
4. Assign next batch of tasks
5. Provide feedback/guidance as needed

### Look for these signals:

**JC is productive:**
- Regular `task_complete` entries
- `tests_passing: True`
- No blockers

**JC needs help:**
- `issue_found` entries with `needs_dc_input: True`
- Long gaps between completions
- `tests_passing: False`

## Example Session

```bash
# User runs for DC:
$ python dc_log_message.py

# DC sees in recent feed:
#   [timestamp] JC → task_complete
#   task: Fix SVG transparency bug
#   tests_passing: True

# DC satisfied, assigns next task:
# Choose option 1
Task: Add batch processing for SVG files
Priority: MEDIUM
Files: optimize_title.py, convert_svg.py
Requirements: Process all .svg in folder, Show progress bar, Handle errors gracefully
Notes: Build on single-file processing already implemented

# Later, DC checks feed again (option 3):
#   [timestamp] JC → issue_found
#   issue: Progress bar library 'tqdm' not installed
#   needs_dc_input: True

# DC provides guidance (option 2):
Action: feedback
Message: Install tqdm with: pip install tqdm. Then use: from tqdm import tqdm; for file in tqdm(files): ...
Target: JC
Priority: HIGH

# JC unblocked, continues work...
```

## Quick Reference

| Option | Use Case | Fields |
|--------|----------|--------|
| 1 - Assign task | Give JC work to do | task, priority, files, requirements, notes |
| 2 - Custom message | Feedback, questions, guidance | action, message, target, priority |
| 3 - View feed | Check JC's progress | (read-only) |

## Remember

- **You are the planner**, JC is the implementer
- **Be clear and specific** - JC has no memory
- **Check feed regularly** - Stay in sync with JC's progress
- **Provide context** - Help JC understand the "why"
- **Use priorities** - Guide JC's focus

Happy coordinating! 🎯
