#!/usr/bin/env python3
"""
JC Task Monitor
Run this in Claude Code (JC) - it will monitor for new tasks and tell JC what to do
"""

import json
import time
from pathlib import Path
from datetime import datetime

AGENT_FEED_PATH = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')
CHECK_INTERVAL = 2  # seconds

def get_last_task():
    """Get the most recent task assignment"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find latest task_assigned from DC
        for line in reversed(lines):
            entry = json.loads(line)
            if entry.get('agent') == 'DC' and entry.get('action') == 'task_assigned':
                return entry
        return None
    except:
        return None

def check_if_completed(task_timestamp):
    """Check if this task has been completed"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Look for task_complete from JC after this timestamp
        for line in reversed(lines):
            entry = json.loads(line)
            if (entry.get('agent') == 'JC' and 
                entry.get('action') == 'task_complete' and
                entry.get('timestamp') > task_timestamp):
                return True
        return False
    except:
        return False

def main():
    print("🤖 JC Task Monitor")
    print("=" * 60)
    print("Monitoring agent feed for new tasks...")
    print("When a task appears, I'll tell you what to do!")
    print("=" * 60)
    print()
    
    last_processed = None
    
    while True:
        task = get_last_task()
        
        if task and task.get('timestamp') != last_processed:
            timestamp = task.get('timestamp')
            
            # Check if already completed
            if not check_if_completed(timestamp):
                details = task.get('details', {})
                task_desc = details.get('task', '')
                priority = details.get('priority', 'MEDIUM')
                
                print("\n" + "=" * 60)
                print(f"🎯 NEW TASK DETECTED!")
                print("=" * 60)
                print(f"Priority: {priority}")
                print(f"Task: {task_desc}")
                print(f"Assigned: {timestamp}")
                print("=" * 60)
                print()
                print("📋 INSTRUCTIONS FOR JC:")
                print(f"Please execute this task: {task_desc}")
                print()
                print("Steps:")
                print("1. Analyze what needs to be done")
                print("2. Use JetBrains MCP tools to implement")
                print("3. Create/modify files as needed")
                print("4. Run tests if applicable")
                print("5. When complete, log to agent feed:")
                print()
                print("   Use this command to log completion:")
                print(f'   echo \'{{"timestamp":"{datetime.utcnow().isoformat()}Z","agent":"JC","action":"task_complete","details":{{"task":"{task_desc}","result":"[what you did]"}}}}\' >> {AGENT_FEED_PATH}')
                print()
                print("🚀 START WORKING NOW!")
                print("=" * 60)
                print()
                
                last_processed = timestamp
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped")
