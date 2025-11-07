#!/usr/bin/env python3
"""
Desktop Claude Task Monitor
Monitors agent feed and creates task notifications
Desktop Claude (in chat) executes them using JetBrains tools
"""

import json
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'
PENDING_TASKS_PATH = r'E:\PythonProjects\PhiGEN\BotFILES\pending_tasks.txt'

class TaskMonitor(FileSystemEventHandler):
    def __init__(self):
        self.last_position = 0
        self.initialize()
    
    def initialize(self):
        try:
            with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.last_position = sum(len(line.encode('utf-8')) for line in lines)
        except:
            pass
    
    def on_modified(self, event):
        if event.src_path.endswith('agent-feed.jsonl'):
            self.check_tasks()
    
    def check_tasks(self):
        try:
            with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                
                if not new_lines:
                    return
                
                self.last_position = f.tell()
                
                for line in new_lines:
                    if line.strip():
                        entry = json.loads(line)
                        
                        if (entry.get('agent') == 'DC' and 
                            entry.get('action') == 'task_assigned'):
                            self.notify_task(entry)
        except Exception as e:
            print(f"Error: {e}")
    
    def notify_task(self, entry):
        details = entry.get('details', {})
        task = details.get('task', '')
        priority = details.get('priority', 'MEDIUM')
        
        print(f"\n🔔 NEW TASK!")
        print(f"Priority: {priority}")
        print(f"Task: {task}")
        print(f"\n👉 Tell Desktop Claude in chat: 'Execute pending tasks'\n")
        
        # Write to pending tasks file
        with open(PENDING_TASKS_PATH, 'a', encoding='utf-8') as f:
            f.write(f"[{priority}] {task}\n")

def main():
    print("🤖 Desktop Claude Task Monitor Running...")
    print("Watching for new tasks...\n")
    
    monitor = TaskMonitor()
    observer = Observer()
    observer.schedule(monitor, str(Path(AGENT_FEED_PATH).parent), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    main()
