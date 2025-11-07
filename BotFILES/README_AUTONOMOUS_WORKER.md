# JC Autonomous Worker - Remote Command System

## Overview

The JC Autonomous Worker is a background service that bridges Discord and JC (Claude Code), allowing you to assign tasks from your phone (via Discord) and have them automatically executed on your PC.

## The Complete Workflow

```
YOU (10km away, on phone)
         ↓
Discord: "!assign_task HIGH Create config.py file"
         ↓
DC Bot → writes to agent-feed.jsonl
         ↓
File Watcher → Discord notification: "New task assigned!"
         ↓
**JC Autonomous Worker (running on PC)**
  - Detects new task in agent-feed.jsonl
  - Executes the task (creates files, modifies code, etc.)
  - Logs completion to agent-feed.jsonl
         ↓
File Watcher → Discord webhook: "JC completed task!"
         ↓
YOU (phone) → sees notification!
```

## Files

- **jc_autonomous_worker.py** - Main worker process (monitors and executes tasks)
- **task_executor.py** - Task execution logic (file operations, code modifications)
- **worker.log** - Activity log
- **worker_state.json** - Tracks last processed task (auto-generated)

## Starting the Worker

### Option 1: Foreground (for testing)
```bash
python BotFILES/jc_autonomous_worker.py
```

Press Ctrl+C to stop.

### Option 2: Background (for production)
```bash
# Windows (PowerShell)
Start-Process python -ArgumentList "BotFILES/jc_autonomous_worker.py" -NoNewWindow

# Windows (CMD)
start /B python BotFILES/jc_autonomous_worker.py

# Linux/Mac
nohup python BotFILES/jc_autonomous_worker.py &
```

## Stopping the Worker

### Foreground Mode
Press `Ctrl+C`

### Background Mode
```bash
# Windows
taskkill /F /IM python.exe /FI "WINDOWTITLE eq jc_autonomous_worker*"

# Or find the process ID and kill it
tasklist | findstr python
taskkill /PID <process_id>

# Linux/Mac
pkill -f jc_autonomous_worker
```

## Task Types Supported

### 1. File Creation
**Discord Command:**
```
!assign_task HIGH Create new file example.py
```

**Result:** Creates `example.py` with appropriate template

**Agent Feed Format:**
```json
{
  "task": "Create new file example.py",
  "priority": "HIGH",
  "files_to_create": ["example.py"]
}
```

### 2. File Modification
**Discord Command:**
```
!assign_task MEDIUM Edit password_validator.py add type hints
```

**Agent Feed Format:**
```json
{
  "task": "Edit password_validator.py add type hints",
  "priority": "MEDIUM",
  "files_to_modify": ["password_validator.py"]
}
```

### 3. Complex Tasks (Require Manual Execution)
Tasks like "add function with complex logic" will be:
- Detected by worker
- Logged as "acknowledged"
- Marked as requiring manual execution
- You'll need to execute these yourself in JC/Claude Code

## Monitoring the Worker

### Check if Running
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep jc_autonomous_worker
```

### View Live Log
```bash
# Windows (PowerShell)
Get-Content BotFILES/worker.log -Wait -Tail 20

# Linux/Mac
tail -f BotFILES/worker.log
```

### Check Last Activity
```bash
tail -20 BotFILES/worker.log
```

## Configuration

### Change Check Interval
Edit `jc_autonomous_worker.py`, line ~257:
```python
time.sleep(5)  # Change from 5 to desired seconds
```

### Change Project Root
Edit `task_executor.py`, line ~17:
```python
self.project_root = project_root or Path(r'E:\PythonProjects\PhiGEN')
```

### Disable Heartbeat Logs
Edit `jc_autonomous_worker.py`, line ~253:
```python
elif check_count % 12 == 0:  # Change 12 to higher number or comment out
```

## Troubleshooting

### Worker Not Detecting Tasks
1. Check if worker is running: `tasklist | findstr python`
2. Check worker.log for errors: `tail -20 BotFILES/worker.log`
3. Delete state file and restart: `rm BotFILES/worker_state.json`
4. Verify agent-feed.jsonl exists and has correct permissions

### Tasks Being Skipped
- Check `worker_state.json` - may have future timestamp
- Solution: Delete `worker_state.json` and restart worker

### Files Not Being Created
- Check worker.log for error messages
- Verify project root path is correct in task_executor.py
- Check file permissions in target directory

### Worker Crashes
- Check worker.log for error details
- Ensure all dependencies are installed
- Verify Python version compatibility

## Task Execution Details

### What Gets Executed Automatically
✅ File creation (any file type)
✅ File deletion (with safety checks)
✅ Basic file edits (adds signature comment)
✅ Template generation (Python, Markdown, Text files)

### What Requires Manual Execution
❌ Complex code logic
❌ Function implementation
❌ Test execution
❌ Debugging
❌ Multi-file refactoring

For these tasks, the worker will:
1. Log them as "acknowledged"
2. Mark them as "requires_manual_execution"
3. You execute them manually in Claude Code

## Integration with Discord

### DC Bot Commands
- `!assign_task <PRIORITY> <task description>`
- `!check_jc` - Check JC status
- `!list_tasks` - List pending tasks

### File Watcher
The file watcher (separate process) monitors agent-feed.jsonl and sends Discord webhooks when:
- New tasks are assigned
- JC completes tasks
- JC logs errors

## Security Considerations

### File Deletion Safety
The worker will NOT delete files matching these patterns:
- `__init__.py`
- `main.py`
- `config`
- `.env`

### File Creation Limits
- Files are only created within the project root
- No system files can be modified
- No executable code is run without explicit logic

## Performance

- **Check interval:** 5 seconds (configurable)
- **Heartbeat:** Every 60 seconds (1 minute)
- **Startup time:** < 1 second
- **Task processing:** Typically < 1 second for simple tasks

## Advanced Usage

### Custom Task Handlers
Edit `task_executor.py` to add custom task types:

```python
def execute(self, task_details):
    if 'my_custom_task' in task_desc:
        return self.handle_my_custom_task(task_details)
```

### Integration with Claude API
For complex tasks, you can integrate Claude API:
1. Add `anthropic` package
2. In `task_executor.py`, call Claude API for code generation
3. Execute the generated code

### Multiple Workers
You can run multiple workers for different projects:
```bash
python jc_autonomous_worker.py --project /path/to/project1
python jc_autonomous_worker.py --project /path/to/project2
```
(Requires adding argument parsing)

## Logs and State

### worker.log Format
```
[2025-11-06 13:25:33] [TASK] EXECUTING TASK
[2025-11-06 13:25:33] Priority: HIGH
[2025-11-06 13:25:33] Task: Create test file hello_world.txt
[2025-11-06 13:25:33] [LOG] Logged to agent feed: task_started
[2025-11-06 13:25:33] [LOG] Logged to agent feed: task_complete
[2025-11-06 13:25:33] [OK] TASK COMPLETED: Created 1 file(s)
```

### worker_state.json Format
```json
{
  "last_processed_timestamp": "2025-11-06T03:25:33.500989+00:00",
  "last_save": "2025-11-06T03:25:45.123456+00:00"
}
```

## Maintenance

### Clear Old Logs
```bash
# Keep last 100 lines
tail -100 BotFILES/worker.log > BotFILES/worker.log.tmp
mv BotFILES/worker.log.tmp BotFILES/worker.log
```

### Reset Worker State
```bash
rm BotFILES/worker_state.json
```

### Update Worker
```bash
# Stop worker
taskkill /F /IM python.exe /FI "WINDOWTITLE eq jc_autonomous_worker*"

# Pull latest code
git pull

# Restart worker
python BotFILES/jc_autonomous_worker.py
```

## FAQ

**Q: Can I assign tasks while away from my PC?**
A: Yes! That's the whole point. Use Discord on your phone to assign tasks.

**Q: Does my PC need to be on?**
A: Yes, the worker runs on your PC, so it must be powered on.

**Q: Does this Claude Code session need to be open?**
A: No! The worker is a separate Python process that runs independently.

**Q: What if I assign multiple tasks?**
A: The worker processes them sequentially in the order they appear in agent-feed.jsonl.

**Q: Can I prioritize tasks?**
A: The worker processes tasks in order, but you can manually re-order them in agent-feed.jsonl.

**Q: What happens if the worker crashes?**
A: It will resume from the last saved state when restarted. No tasks are lost.

**Q: Can I run this 24/7?**
A: Yes, but make sure your PC doesn't go to sleep/hibernate.

## Next Steps

1. **Start the worker:** `python BotFILES/jc_autonomous_worker.py`
2. **Test from Discord:** Send `!assign_task HIGH Create test.txt`
3. **Verify:** Check that test.txt was created
4. **Monitor:** Watch worker.log for activity
5. **Celebrate:** You can now control your PC from anywhere!

## Support

If you encounter issues:
1. Check worker.log for errors
2. Verify agent-feed.jsonl format
3. Delete worker_state.json and retry
4. Check this documentation

---

**Created by JC - Your Remote Development Assistant** 🤖
