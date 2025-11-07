# PhiGEN Agent Coordination System

**Status**: ✅ Fully operational

Multi-agent coordination system for JC (Jetbrains Claude) and DC (Desktop Claude) to collaborate on PhiGEN project.

## Quick Start

### For JC (in PyCharm):
```bash
# Check for tasks from DC
python jc_read_feed.py

# After completing work, log it:
python
>>> from phigen.agent_feed import jc_task_complete
>>> jc_task_complete("Task description", files=["file.py"], tests_passing=True)
```

### For DC (user runs on behalf):
```bash
# Assign tasks to JC
python dc_log_message.py
# Choose option 1, fill in task details
```

## What Got Installed

```
PhiGEN/
├── phigen/                      # Package
│   ├── __init__.py
│   └── agent_feed.py           # Core logging utilities (240 lines)
├── docs/
│   ├── agent-feed.jsonl        # Event feed (append-only log)
│   ├── AGENT_COORDINATION.md   # Full guide (350+ lines)
│   ├── JC_QUICKSTART.md        # Quick start for JC
│   └── DC_QUICKSTART.md        # Quick start for DC
├── dc_log_message.py           # Interactive logger for DC (120 lines)
├── jc_read_feed.py             # Feed reader for JC (95 lines)
└── test_agent_feed.py          # Test suite (150 lines)
```

## How It Works

1. **DC plans** → Assigns task via `dc_log_message.py` → Logged to `agent-feed.jsonl`
2. **JC reads** → Runs `jc_read_feed.py` → Sees task
3. **JC implements** → Codes solution in PyCharm
4. **JC logs** → Uses `jc_task_complete()` → Logged to `agent-feed.jsonl`
5. **DC reviews** → Sees completion → Plans next task → Repeat

## Key Features

- **JSONL feed**: Append-only event log, human-readable
- **No dependencies**: Uses only Python stdlib (json, datetime, pathlib)
- **Simple API**: 3 main functions cover 90% of use cases
- **Tested**: All components verified and working
- **Documented**: 3 comprehensive guides included

## API Reference

### For JC:
```python
from phigen.agent_feed import jc_task_complete, jc_found_issue, log_action

# Log task completion
jc_task_complete(task, files, tests_passing=True, notes=None)

# Log blocker/issue
jc_found_issue(issue, severity, file=None, line=None, needs_dc_input=False)

# Custom action
log_action(action, details, agent="JC")
```

### For DC (via script):
- Run `dc_log_message.py` → Interactive menu
- Option 1: Assign task
- Option 2: Custom message
- Option 3: View recent feed

## Testing

All tests passed:
```bash
$ python test_agent_feed.py

============================================================
ALL TESTS PASSED
============================================================
```

Tests verify:
- ✅ Basic logging works
- ✅ DC can assign tasks
- ✅ JC can log completions
- ✅ JC can log issues
- ✅ Feed can be read
- ✅ Custom actions work

## Time to Implement

**Total: ~20 minutes**
- Core module: 5 min
- Helper scripts: 5 min
- Documentation: 8 min
- Testing: 2 min

## Compared to PhiWave System

**What's included:**
- ✅ JSONL feed (same as PhiWave)
- ✅ Append-only log (same)
- ✅ Agent coordination (same)
- ✅ Helper utilities (adapted for PhiGEN)

**What's excluded:**
- ❌ MCP Hub (not needed - DC has no tools)
- ❌ SQLite database (feed-only is simpler)
- ❌ Real-time messaging (async via feed is sufficient)

**Result:** Simpler, lighter, perfect for JC ↔ DC workflow.

## Next Steps

1. **JC**: Read `docs/JC_QUICKSTART.md` (5 min)
2. **DC**: Read `docs/DC_QUICKSTART.md` (5 min)
3. **Try it**: DC assigns first task, JC completes it (10 min)
4. **Iterate**: Improve workflow based on actual usage

## Support

- **Full guide**: `docs/AGENT_COORDINATION.md`
- **JC guide**: `docs/JC_QUICKSTART.md`
- **DC guide**: `docs/DC_QUICKSTART.md`
- **Feed format**: See `docs/AGENT_COORDINATION.md` section "Feed Entry Format"

---

**Ready to use!** Start with DC assigning the first task.
