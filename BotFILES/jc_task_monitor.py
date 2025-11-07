#!/usr/bin/env python3
"""
JC Continuous Task Monitor
Runs alongside JC and automatically feeds it tasks
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

AGENT_FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')
JC_PROMPT_FILE = Path(r'E:\PythonProjects\PhiGEN\BotFILES\jc_auto_prompt.txt')

class TaskMonitor:
    def __init__(self):
        self.last_task_timestamp = None
        self.load_state()
    
    def load_state(self):
        """Load last processed task"""
        try:
            task = self.get_latest_task()
            if task:
                self.last_task_timestamp = task.get('timestamp')
        except:
            pass
    
    def get_latest_task(self):
        """Get most recent task from DC"""
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
    
    def check_if_started(self, task_timestamp):
        """Check if JC already started this task"""
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
    
    def create_jc_prompt(self, task_desc, priority, timestamp):
        """Create a prompt file that JC should execute"""
        prompt = f"""NEW TASK AUTO-ASSIGNED:

Priority: {priority}
Task: {task_desc}
Assigned: {timestamp}

INSTRUCTIONS:
1. First, log task start to {AGENT_FEED}:
   {{"timestamp": "{datetime.utcnow().isoformat()}Z", "agent": "JC", "action": "task_started", "details": {{"task": "{task_desc}"}}}}

2. Execute the task using JetBrains MCP tools

3. When complete, log to {AGENT_FEED}:
   {{"timestamp": "{datetime.utcnow().isoformat()}Z", "agent": "JC", "action": "task_complete", "details": {{"task": "{task_desc}", "result": "what you did"}}}}

START WORKING NOW.
"""
        JC_PROMPT_FILE.write_text(prompt)
        print(f"\n📋 Prompt file created for JC at: {JC_PROMPT_FILE}")
        print(f"✅ JC should now execute: {task_desc}")
    
    def monitor(self):
        """Continuously monitor for new tasks"""
        print("🤖 JC Task Monitor Running...")
        print("="*60)
        print(f"Watching: {AGENT_FEED}")
        print(f"Prompt file: {JC_PROMPT_FILE}")
        print()
        print("When new tasks appear, a prompt file will be created")
        print("JC needs to check this file periodically and execute tasks")
        print()
        print("Press Ctrl+C to stop")
        print("="*60)
        print()
        
        while True:
            task = self.get_latest_task()
            
            if task:
                timestamp = task.get('timestamp')
                
                # Check if this is a new task we haven't processed
                if timestamp != self.last_task_timestamp:
                    # Check if JC already started it
                    if not self.check_if_started(timestamp):
                        details = task.get('details', {})
                        task_desc = details.get('task', '')
                        priority = details.get('priority', 'MEDIUM')
                        
                        print(f"\n🎯 NEW TASK DETECTED!")
                        print(f"Priority: {priority}")
                        print(f"Task: {task_desc}")
                        
                        # Create prompt for JC
                        self.create_jc_prompt(task_desc, priority, timestamp)
                        
                        self.last_task_timestamp = timestamp
            
            time.sleep(2)  # Check every 2 seconds

if __name__ == '__main__':
    try:
        monitor = TaskMonitor()
        monitor.monitor()
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped")
