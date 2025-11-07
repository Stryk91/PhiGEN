# Feature #4: Scheduled Tasks

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Automate recurring tasks and reminders. Set up daily standups, periodic checks, or time-based notifications.

**Commands:**
```
!schedule 9am "!dc good morning, daily standup"
!schedule every-hour "!stats"
!schedule friday-5pm "!dc weekly summary"
!schedule daily-9am "!git status"
!remind 30m "check build status"
!schedule list
!schedule delete <id>
!schedule pause <id>
!schedule resume <id>
!timezone <tz>
```

---

## Architecture

```
Schedule Parser (cron-like syntax)
        ↓
Task Queue (APScheduler)
        ↓
Task Executor (runs command at scheduled time)
        ↓
Notification (sends to Discord channel)
        ↓
Persistence (SQLite for task storage)
```

---

## Tech Stack

- `APScheduler` - Advanced scheduling
- `dateparser` - Natural language time parsing
- `pytz` - Timezone support
- SQLite - Persistent task storage

---

## Schedule Formats

### Time-based
- `9am`, `14:30`, `5pm`
- `tomorrow-9am`
- `monday-10am`

### Interval-based
- `every-hour`
- `every-30m`
- `every-day`
- `every-monday`

### Relative
- `30m` (in 30 minutes)
- `2h` (in 2 hours)
- `1d` (in 1 day)

---

## Usage Examples

### Daily Standup
```
User: !schedule daily-9am "!dc Good morning team, daily standup time"
Bot: ✅ Scheduled task #1
     Runs: Every day at 9:00 AM
     Command: !dc Good morning team, daily standup time

[Next day at 9:00 AM]
Bot: 🔔 Scheduled Task #1
     (executes: !dc Good morning team, daily standup time)
```

### Hourly Stats
```
User: !schedule every-hour "!stats"
Bot: ✅ Scheduled task #2
     Runs: Every hour at :00
     Command: !stats

[Every hour]
Bot: 🔔 Scheduled Task #2
     📊 Model Usage Statistics
     Local queries: 47
     API queries: 12
     Cost saved: $2.34
```

### One-Time Reminder
```
User: !remind 30m "Check if deploy completed"
Bot: ✅ Reminder set
     Time: 2:45 PM (in 30 minutes)
     Message: Check if deploy completed

[30 minutes later]
Bot: 🔔 REMINDER
     Check if deploy completed
```

### Weekly Summary
```
User: !schedule friday-5pm "!dc Weekly summary: !stats week"
Bot: ✅ Scheduled task #3
     Runs: Every Friday at 5:00 PM
     Command: !dc Weekly summary: !stats week

[Friday at 5 PM]
Bot: 🔔 Scheduled Task #3
     (executes command chain)
```

---

## Management Commands

### List all schedules
```
User: !schedule list
Bot: **Active Schedules:**

     #1 | Daily 9:00 AM | !dc Good morning team
     #2 | Every hour | !stats
     #3 | Friday 5:00 PM | !dc Weekly summary

     #4 (PAUSED) | Every 30 min | !git status
```

### Delete schedule
```
User: !schedule delete 2
Bot: ✅ Deleted schedule #2 (Every hour | !stats)
```

### Pause/Resume
```
User: !schedule pause 1
Bot: ⏸️ Paused schedule #1

User: !schedule resume 1
Bot: ▶️ Resumed schedule #1
```

---

## Implementation Components

**Files Created:**
- `task_scheduler.py` - APScheduler wrapper (350 lines)
- `schedule_parser.py` - Parse natural language schedules
- `task_storage.py` - SQLite persistence
- Bot integration (~150 lines)

**Key Classes:**
- `TaskScheduler` - Manage scheduled tasks
- `ScheduleParser` - Parse time expressions
- `TaskStorage` - Persistent storage

---

## Database Schema

```sql
CREATE TABLE scheduled_tasks (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    schedule TEXT NOT NULL,  -- cron or interval
    command TEXT NOT NULL,
    created_at TIMESTAMP,
    next_run TIMESTAMP,
    enabled BOOLEAN DEFAULT 1,
    runs_count INTEGER DEFAULT 0
);
```

---

## Timezone Handling

**Set user timezone:**
```
User: !timezone Australia/Sydney
Bot: ✅ Timezone set to Australia/Sydney (UTC+11)

User: !schedule 9am "morning"
Bot: ✅ Scheduled for 9:00 AM Australia/Sydney
```

---

## Advanced Features

### Command Chaining
```
!schedule daily-9am "!stats + !git commits 5 + !dc Daily report"
```

### Conditional Execution
```
!schedule every-hour "!git status && if-changes !dc Code updated"
```

### Recurring with Limit
```
!schedule every-day "!remind standup" --until 2025-12-31
```

### Execution Windows
```
!schedule weekdays-9am "!dc Start work" --only-weekdays
!schedule business-hours "!check-builds" --between 9am-5pm
```

---

## Security

- Only schedule owner can delete/modify
- Rate limit: Max 10 active schedules per user
- Command whitelist (can't schedule dangerous commands)
- Timeout per scheduled task (30s max)
- No arbitrary code execution
- Admin can view/delete all schedules

---

## Resource Usage

- Minimal CPU when idle
- ~10MB memory overhead
- SQLite database: <1MB for 100 tasks
- Network: Only when task executes

**Performance:**
- Can handle 100+ concurrent schedules
- Subsecond execution accuracy
- Persistent across bot restarts

---

## Error Handling

**Bot Offline During Scheduled Time:**
```
[Bot restarts]
Bot: ⚠️ Missed 3 scheduled tasks while offline:
     #1 - Daily standup (missed 9:00 AM)
     #2 - Hourly stats (missed 2:00 PM, 3:00 PM)

     Running missed tasks now? (react ✅/❌)
```

**Invalid Schedule:**
```
User: !schedule invalid-time "test"
Bot: ❌ Could not parse schedule: "invalid-time"
     Examples:
     - 9am, 2:30pm
     - every-hour, every-day
     - 30m, 2h (relative)
```

**Command Execution Failed:**
```
[Scheduled task runs]
Bot: ❌ Task #5 failed to execute: !nonexistent-command
     Error: Command not found
     Task has been disabled. Fix and use !schedule resume 5
```

---

## Limitations

1. **No task history** - Only stores next run, not full execution history
2. **Single channel** - Task executes in channel where created
3. **Bot restart** - Tasks reload from DB but may miss runs during downtime
4. **No distributed** - Won't work across multiple bot instances
5. **Timezone dependent** - User must set correct timezone

---

## Future Enhancements

- Task execution history/logs
- Task dependencies ("Run B after A completes")
- Webhook triggers (GitHub push → run task)
- Conditional schedules (only if tests pass)
- Task templates/presets
- Execution statistics per task
- Distributed scheduling (multi-bot)
- Cron expression support
- Recurring task with retries

---

## Dependencies

```
APScheduler>=3.10.0
dateparser>=1.1.0
pytz>=2023.3
```

---

## Use Cases

1. **Daily Standups** - Automated team reminders
2. **Build Monitoring** - Periodic build status checks
3. **Stats Reporting** - Hourly/daily usage stats
4. **Code Review Reminders** - Friday afternoon PR review reminder
5. **Deadline Alerts** - Project milestone reminders
6. **Health Checks** - Regular system status verification
7. **Log Rotation** - Periodic log cleanup
8. **Backup Reminders** - Weekly backup notifications

---

## Pros & Cons

### Pros
- Set and forget automation
- Never miss recurring tasks
- Natural language scheduling
- Persistent across restarts
- Per-user timezone support
- Easy to manage (pause/resume/delete)

### Cons
- Limited to bot commands (can't run arbitrary code)
- Single bot instance only
- May miss executions if bot offline
- Timezone confusion for global teams
- No conditional execution (yet)

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**Implementation Complexity:** Medium (APScheduler + time parsing)
**ROI:** High for teams with recurring workflows
