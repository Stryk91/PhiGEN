# Feature #7: Smart Notifications

**Status:** TBI (To Be Implemented)
**Priority:** Medium-High
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Monitor file changes, build status, test results, errors. Get notified only when important events happen.

**Commands:**
```
!watch-file <path>                   # Notify on file changes
!watch-build                         # Notify when build completes
!watch-tests                         # Notify on test failures
!watch-errors                        # Notify on error patterns in logs
!watch-dir <path>                    # Monitor directory
!alert-when "condition"              # Custom condition alerts
!watch list                          # List all watchers
!watch delete <id>                   # Remove watcher
!watch pause <id>                    # Pause notifications
```

---

## Architecture

```
File System Watcher (watchdog)
        ↓
Event Detection
        ↓
Condition Evaluation
        ↓
Notification Trigger
        ↓
Discord Message (with context)
```

---

## Tech Stack

- `watchdog` - File system monitoring
- `psutil` - Process monitoring
- Pattern matching for conditions
- Log file parsing

---

## Usage Examples

### Watch File Changes

```
User: !watch-file src/config.py
Bot: 👁️ Watching: src/config.py
     Watcher ID: 1
     Will notify on: modify, create, delete

[File modified]
Bot: 📝 **File Changed: src/config.py**
     Event: modified
     Time: 3:45 PM
     By: STRYK (git blame)

     Recent changes:
     ```diff
     - DEBUG = True
     + DEBUG = False
     ```
```

### Watch Build

```
User: !watch-build
Bot: 🔨 Watching: Build process
     Monitoring: docker-compose.log
     Watcher ID: 2

[Build completes]
Bot: ✅ **Build Complete**
     Duration: 2m 34s
     Status: SUCCESS
     Output: No errors

[Build fails]
Bot: ❌ **Build Failed**
     Duration: 1m 12s
     Status: FAILED
     Error: ModuleNotFoundError: discord.py
     Line: 45 in bot.py
```

### Watch Tests

```
User: !watch-tests
Bot: 🧪 Watching: Test suite
     Monitoring: pytest output
     Watcher ID: 3

[Tests fail]
Bot: ❌ **Tests Failed**
     Passed: 45/48
     Failed: 3

     **Failures:**
     - test_encryption_persistence (KeyError)
     - test_auth_flow (AssertionError)
     - test_api_integration (ConnectionError)

     View full output: !tests-output
```

### Watch Errors

```
User: !watch-errors
Bot: 🚨 Watching: Error logs
     Monitoring: app.log
     Patterns: ERROR, CRITICAL, Exception
     Watcher ID: 4

[Error detected]
Bot: 🚨 **Error Detected**
     Level: CRITICAL
     File: src/encryption.py:125
     Message: KeyError: 'derived_key'
     Time: 3:47 PM

     Stack trace:
     ```
     File "src/encryption.py", line 125, in encrypt
         cipher = Fernet(self._keys['derived_key'])
     KeyError: 'derived_key'
     ```
```

### Custom Conditions

```
User: !alert-when "deploy succeeds"
Bot: 🔔 Alert created
     Condition: deploy succeeds
     Monitoring: deploy.log
     Watcher ID: 5

[Deploy completes]
Bot: 🎉 **Deploy Succeeded**
     Environment: production
     Version: v2.1.0
     Time: 4:00 PM
     URL: https://phigen.app
```

### Directory Watch

```
User: !watch-dir src/ --pattern "*.py"
Bot: 👁️ Watching: src/
     Pattern: *.py
     Watcher ID: 6

[New file created]
Bot: ✨ **New File: src/oauth.py**
     Created by: STRYK
     Size: 234 lines

[File deleted]
Bot: 🗑️ **File Deleted: src/old_auth.py**
     Last modified: 2 days ago
     Size: 180 lines
```

---

## Management

### List Watchers

```
User: !watch list
Bot: **Active Watchers:**

     #1 | File: src/config.py
     #2 | Build process
     #3 | Test suite
     #4 | Error logs
     #5 (PAUSED) | Deploy status
     #6 | Directory: src/

     Total: 6 active, 1 paused
```

### Pause/Resume

```
User: !watch pause 4
Bot: ⏸️ Paused watcher #4 (Error logs)

User: !watch resume 4
Bot: ▶️ Resumed watcher #4 (Error logs)
```

### Delete

```
User: !watch delete 2
Bot: ✅ Deleted watcher #2 (Build process)
```

---

## Implementation Components

**Files Created:**
- `file_watcher.py` - Watchdog integration (400 lines)
- `build_monitor.py` - Build process tracking
- `log_parser.py` - Parse and filter logs
- `notification_manager.py` - Handle notification logic
- Bot integration (~200 lines)

**Key Classes:**
- `FileWatcher` - Monitor file system events
- `BuildMonitor` - Track build processes
- `LogParser` - Parse and filter log files
- `NotificationManager` - Handle alerts and rate limiting

---

## Advanced Features

### Smart Filtering

```
User: !watch-errors --exclude "DeprecationWarning"
Bot: 🚨 Watching errors (excluding DeprecationWarning)
```

### Aggregation

```
User: !watch-errors --aggregate 5m
Bot: 🚨 Watching errors (aggregated every 5 minutes)

[After 5 minutes]
Bot: 📊 **Error Summary (last 5 min):**
     Total: 12 errors
     CRITICAL: 1
     ERROR: 8
     WARNING: 3

     Most common: KeyError (6 occurrences)
```

### Conditional Alerts

```
User: !alert-when "test coverage < 80%"
Bot: 🔔 Alert created
     Condition: coverage below 80%

[Tests run with 75% coverage]
Bot: ⚠️ **Coverage Alert**
     Current: 75%
     Threshold: 80%
     Missing coverage in: src/oauth.py
```

### Threshold Alerts

```
User: !watch-file src/main.py --threshold 5
Bot: 👁️ Watching: src/main.py
     Will notify after 5 changes (prevents spam)

[After 5 modifications]
Bot: 📝 **src/main.py changed 5 times in last 10 minutes**
     Last change: 2 min ago
     Total lines changed: +45, -12
```

---

## Database Schema

```sql
CREATE TABLE watchers (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    channel_id TEXT,
    type TEXT,  -- file, build, test, error, custom
    target TEXT,  -- path or condition
    pattern TEXT,
    enabled BOOLEAN,
    created_at TIMESTAMP
);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    watcher_id INTEGER,
    triggered_at TIMESTAMP,
    message TEXT,
    acknowledged BOOLEAN
);
```

---

## Security

- Whitelist watched paths (no system files)
- Rate limiting (max 1 notification per watcher per minute)
- User can only watch their own files/processes
- Admin can view all watchers
- No execution of commands on events
- Sanitize file paths to prevent directory traversal

---

## Resource Usage

- Low CPU (event-driven, not polling)
- Memory: ~50MB per 10 active watchers
- Disk: Minimal (only stores metadata)

**Performance:**
- Event detection: <100ms
- Notification delivery: <500ms
- No impact when no events occurring
- Watchdog is efficient (OS-level events)

---

## Notification Types

| Type | Trigger | Use Case |
|------|---------|----------|
| **File Change** | File modified/created/deleted | Config changes, code updates |
| **Build Status** | Build complete/failed | CI/CD monitoring |
| **Test Failures** | Tests fail | Quality assurance |
| **Error Logs** | Error patterns in logs | Production monitoring |
| **Deploy Status** | Deployment events | Release tracking |
| **Coverage Drop** | Test coverage decreases | Code quality |
| **Performance** | Slow queries, high CPU | Performance issues |

---

## Limitations

1. **Local files only** - Can't watch remote servers
2. **Polling for logs** - Log watching uses polling (1s interval)
3. **No network monitoring** - Only file/process events
4. **Discord rate limits** - Max 50 messages per channel per minute
5. **Windows limitations** - Some events not supported on Windows
6. **No historical data** - Only current events (no time-series analysis)

---

## Future Enhancements

- Remote server monitoring (SSH)
- Network request monitoring
- Database query monitoring
- Performance metric alerts (CPU, memory, disk)
- Webhook integrations (external services)
- Email/SMS notifications
- Alert escalation (if not acknowledged)
- Alert grouping (multiple events → single notification)
- Anomaly detection (ML-based)
- Integration with monitoring tools (Prometheus, Grafana)

---

## Dependencies

```
watchdog>=3.0.0
psutil>=5.9.0
```

---

## Use Cases

1. **Development** - Monitor file changes during coding
2. **CI/CD** - Track build and deployment status
3. **Testing** - Get notified of test failures immediately
4. **Production** - Monitor error logs in real-time
5. **Security** - Alert on suspicious file modifications
6. **Performance** - Track resource usage spikes
7. **Team Coordination** - Shared visibility into system events

---

## Pros & Cons

### Pros
- Stay informed without constant checking
- Instant notifications for important events
- Customizable conditions
- Low resource overhead
- No manual monitoring needed
- Event-driven (efficient)

### Cons
- Local only (no remote monitoring)
- Can be noisy if not filtered properly
- Requires bot running continuously
- Limited to file/process events
- Discord rate limits apply

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**Implementation Complexity:** Medium (Watchdog + event handling)
**ROI:** High (saves constant manual checking)
