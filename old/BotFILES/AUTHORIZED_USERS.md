# Authorized Task Assigners

This document lists all users authorized to assign tasks to JC via the autonomous worker system.

## Current Authorized Users

### Stryk (Owner)
- **Discord Username:** Stryk#8167
- **Discord User ID:** 1390653822535340162
- **Display Names:** lordcain, Stryk
- **Permissions:** Full access (can assign any task)

### DC Bot
- **Agent Name:** DC
- **Purpose:** Discord Command bot that relays user commands
- **Permissions:** Full access (task relay)

## How Authorization Works

The autonomous worker checks incoming tasks against the `AUTHORIZED_ASSIGNERS` list in `jc_autonomous_worker.py`.

Tasks are accepted if:
1. The `agent` field matches an authorized user, OR
2. The `assigned_by` field in task details matches an authorized user

## Adding New Authorized Users

### Method 1: Edit the Worker Script
1. Open `BotFILES/jc_autonomous_worker.py`
2. Find the `AUTHORIZED_ASSIGNERS` list (around line 30)
3. Add the new user's identifiers:
   ```python
   AUTHORIZED_ASSIGNERS = [
       'DC',
       'Stryk',
       'Stryk#8167',
       '1390653822535340162',
       'lordcain',
       'NewUser#1234',          # Add new user
       'new_user_discord_id',   # Add user ID
   ]
   ```
4. Save and restart the worker

### Method 2: Environment Variable (Future Enhancement)
In a future version, you could load authorized users from an environment variable or config file:
```python
import os
AUTHORIZED_ASSIGNERS = os.getenv('JC_AUTHORIZED_USERS', 'DC,Stryk').split(',')
```

## Security Considerations

### Why Authorization Matters
- Prevents unauthorized task execution
- Ensures only trusted users can control JC
- Protects against malicious commands from Discord

### Best Practices
1. **Limit Access:** Only add users you trust
2. **Use Specific IDs:** Discord user IDs are more secure than usernames
3. **Review Regularly:** Audit the authorized list periodically
4. **Monitor Logs:** Check `worker.log` for suspicious activity
5. **Restart Worker:** Always restart after adding/removing users

## Task Assignment Format

### From Discord (via DC Bot)
```
!assign_task HIGH Create config.py file
```

DC Bot converts this to:
```json
{
  "timestamp": "2025-11-06T...",
  "agent": "DC",
  "action": "task_assigned",
  "details": {
    "task": "Create config.py file",
    "priority": "HIGH",
    "assigned_by": "lordcain",
    "assigned_via": "Discord"
  }
}
```

### Direct to Agent Feed (Manual)
```json
{
  "timestamp": "2025-11-06T...",
  "agent": "Stryk",
  "action": "task_assigned",
  "details": {
    "task": "Create config.py file",
    "priority": "HIGH"
  }
}
```

Both formats are accepted if the `agent` or `assigned_by` is in the authorized list.

## Revoking Access

To revoke a user's access:
1. Open `jc_autonomous_worker.py`
2. Remove their entries from `AUTHORIZED_ASSIGNERS`
3. Restart the worker
4. Their pending tasks will be ignored (not executed)

## Troubleshooting

### "Task not being picked up"
**Cause:** User not in authorized list
**Solution:** Add user to `AUTHORIZED_ASSIGNERS` and restart worker

### "Worker executing tasks from wrong user"
**Cause:** Multiple users with similar names in authorized list
**Solution:** Use Discord user IDs instead of usernames

### "Need to add user temporarily"
**Solution:** Add to list, restart worker, complete tasks, remove, restart again

## Logging

The worker logs who assigned each task:
```
[2025-11-06 13:25:33] [TASK] EXECUTING TASK
[2025-11-06 13:25:33] Assigned by: lordcain
[2025-11-06 13:25:33] Priority: HIGH
[2025-11-06 13:25:33] Task: Create config.py
```

This helps track task origins and audit activity.

## Future Enhancements

Planned improvements to the authorization system:

1. **Config File:** Load authorized users from `authorized_users.json`
2. **Role-Based Access:** Different permission levels (read-only, execute, admin)
3. **Temporary Access:** Time-limited authorization with auto-expiry
4. **Audit Trail:** Detailed logging of all authorization checks
5. **Web Dashboard:** Manage authorized users via web interface

## Related Files

- `jc_autonomous_worker.py` - Contains authorization logic
- `worker.log` - Shows who assigned each task
- `agent-feed.jsonl` - Task queue with assigner info

---

**Last Updated:** 2025-11-06
**Maintained By:** JC Autonomous Worker System
