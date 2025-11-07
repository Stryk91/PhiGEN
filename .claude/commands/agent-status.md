---
description: Check status of agent feed and autonomous workers
allowed-tools: [Read, Bash, Grep]
---

# Agent Status Check

Check the status of multi-agent coordination system.

## Check:

1. **Agent Feed**
   - Read last 10 entries from `docs/agent-feed.jsonl`
   - Show recent task assignments and completions
   - Identify pending tasks

2. **Autonomous Worker**
   - Check if `jc_autonomous_worker.py` is running
   - Read `BotFILES/worker.log` (last 20 lines)
   - Check `BotFILES/worker_state.json` for last processed timestamp

3. **Discord Bot**
   - Check if `phigen_discord_bot.py` is running
   - Verify bot token is in environment variables (not hardcoded)

4. **Summary**
   - Active agents
   - Recent activity
   - Pending tasks
   - Health status

Generate the status report now.
