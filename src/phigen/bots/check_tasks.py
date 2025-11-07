#!/usr/bin/env python3
"""
JC Auto-Task Monitor
Watches agent feed and creates task notifications for JC to pick up
"""

import json
import time
from pathlib import Path
from datetime import datetime

AGENT_FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')
TASK_FILE = Path(r'E:\PythonProjects\PhiGEN\BotFILES\current_task.txt')

def get_latest_task():
    try:
        with open(AGENT_FEED, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            entry = json.loads(line)
            if entry.get('agent') == 'DC' and entry.get('action') == 'task_assigned':
                return entry
        return None
    except:
        return None

def check_if_started(task_timestamp):
    try:
        with open(AGENT_FEED, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            entry = json.loads(line)
            if (entry.get('agent') == 'JC' and 
                entry.get('action') in ['task_started', 'task_complete'] and
                entry.get('timestamp') > task_timestamp):
                return True
        return False
    except:
        return False

# Check for new task
task = get_latest_task()
if task:
    timestamp = task.get('timestamp')
    
    if not check_if_started(timestamp):
        details = task.get('details', {})
        task_desc = details.get('task', '')
        priority = details.get('priority', 'MEDIUM')
        
        # Write task file for JC to find
        TASK_FILE.write_text(
            f"PENDING TASK [{priority}]\n"
            f"Assigned: {timestamp}\n"
            f"Task: {task_desc}\n\n"
            f"Execute this task using JetBrains MCP tools, then log completion to:\n"
            f"{AGENT_FEED}\n"
        )
        
        print(f"✅ New task detected and queued for JC!")
        print(f"Priority: {priority}")
        print(f"Task: {task_desc}")
