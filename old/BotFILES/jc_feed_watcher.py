#!/usr/bin/env python3
"""
JC Agent Feed Watcher
Monitors agent-feed.jsonl for new tasks assigned to JC
Shows notifications and can auto-respond via Discord
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1435814674242338847/gC1Lkq49pr8aOyxRnSRia8K-b5E7fLJqRMa8REAspOOjGUTzMgLVqRK-O8BhPiUXSIYu"
CHECK_INTERVAL = 1  # seconds

class AgentFeedWatcher(FileSystemEventHandler):
    """Watches agent-feed.jsonl for changes"""
    
    def __init__(self):
        self.last_position = 0
        self.last_entry_timestamp = None
        
        # Read existing entries to set baseline
        self.initialize_position()
    
    def initialize_position(self):
        """Set initial position to end of file"""
        try:
            with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.last_position = sum(len(line.encode('utf-8')) for line in lines)
                
                # Get last entry timestamp
                if lines:
                    last_entry = json.loads(lines[-1])
                    self.last_entry_timestamp = last_entry.get('timestamp')
                    print(f"✅ Initialized. Last entry: {self.last_entry_timestamp}")
        except Exception as e:
            print(f"⚠️ Could not initialize: {e}")
    
    def on_modified(self, event):
        """Called when agent-feed.jsonl is modified"""
        if event.src_path.endswith('agent-feed.jsonl'):
            self.check_new_entries()
    
    def check_new_entries(self):
        """Check for new entries in the feed"""
        try:
            with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
                # Seek to last known position
                f.seek(self.last_position)
                
                # Read new content
                new_lines = f.readlines()
                
                if not new_lines:
                    return
                
                # Update position
                self.last_position = f.tell()
                
                # Process each new entry
                for line in new_lines:
                    if line.strip():
                        entry = json.loads(line)
                        self.process_entry(entry)
        
        except Exception as e:
            print(f"❌ Error checking entries: {e}")
    
    def process_entry(self, entry):
        """Process a new entry from the feed"""
        agent = entry.get('agent')
        action = entry.get('action')
        timestamp = entry.get('timestamp')
        details = entry.get('details', {})
        
        print(f"\n{'='*60}")
        print(f"📋 New Entry Detected!")
        print(f"Agent: {agent}")
        print(f"Action: {action}")
        print(f"Time: {timestamp}")
        
        # Check if it's a task for JC
        if agent == 'DC' and action == 'task_assigned':
            self.handle_task_assignment(entry)

        # Check if it's a message for JC
        elif agent == 'DC' and action == 'message_to_jc':
            self.handle_message(entry)

        # Check if JC completed a task
        elif agent == 'JC' and action == 'task_complete':
            self.handle_task_completion(entry)

        # Check if JC started a task
        elif agent == 'JC' and action == 'task_started':
            self.handle_task_started(entry)

        print(f"{'='*60}\n")
    
    def handle_task_assignment(self, entry):
        """Handle new task assignment"""
        details = entry.get('details', {})
        task = details.get('task', 'Unknown task')
        priority = details.get('priority', 'MEDIUM')
        
        print(f"🎯 NEW TASK ASSIGNED TO JC!")
        print(f"Priority: {priority}")
        print(f"Task: {task}")
        
        # Send to Discord
        self.notify_discord(
            title="🎯 New Task Assigned",
            description=f"**Priority:** {priority}\n**Task:** {task}",
            color=0xFF5555 if priority == 'HIGH' else 0x5555FF
        )
        
        # Show system notification (Windows)
        self.show_windows_notification(
            "JC - New Task Assigned",
            f"{priority}: {task}"
        )
    
    def handle_message(self, entry):
        """Handle message to JC"""
        details = entry.get('details', {})
        message = details.get('message', 'No message')
        from_user = details.get('from', 'Unknown')

        print(f"💬 MESSAGE FOR JC!")
        print(f"From: {from_user}")
        print(f"Message: {message}")

        # Send to Discord
        self.notify_discord(
            title="💬 Message for JC",
            description=f"From: {from_user}\n\n{message}",
            color=0x55FF55
        )

    def handle_task_started(self, entry):
        """Handle JC starting a task"""
        details = entry.get('details', {})
        task = details.get('task', 'Unknown task')
        priority = details.get('priority', 'MEDIUM')
        assigned_by = details.get('assigned_by', 'Unknown')

        print(f"🔨 JC STARTED TASK!")
        print(f"Priority: {priority}")
        print(f"Task: {task}")
        print(f"Assigned by: {assigned_by}")

        # Send to Discord
        self.notify_discord(
            title="🔨 JC Started Working",
            description=f"**Task:** {task}\n**Priority:** {priority}\n**Assigned by:** {assigned_by}",
            color=0xFFAA00
        )

    def handle_task_completion(self, entry):
        """Handle JC completing a task"""
        details = entry.get('details', {})
        task = details.get('task', 'Unknown task')
        result = details.get('result', 'No details')
        files_modified = details.get('files_modified', [])
        success = details.get('success', True)
        assigned_by = details.get('assigned_by', 'Unknown')

        print(f"✅ JC COMPLETED TASK!")
        print(f"Task: {task}")
        print(f"Result: {result}")
        print(f"Files: {len(files_modified)}")
        print(f"Success: {success}")

        # Build description
        desc = f"**Task:** {task}\n**Result:** {result}\n**Assigned by:** {assigned_by}"

        if files_modified:
            desc += f"\n\n**Files Modified:** ({len(files_modified)})"
            for f in files_modified[:5]:  # Show max 5 files
                desc += f"\n• `{Path(f).name}`"
            if len(files_modified) > 5:
                desc += f"\n• ... and {len(files_modified) - 5} more"

        # Send to Discord
        self.notify_discord(
            title="✅ JC Task Complete!" if success else "❌ JC Task Failed",
            description=desc,
            color=0x00FF00 if success else 0xFF0000
        )

        # Show system notification
        self.show_windows_notification(
            "JC - Task Complete!",
            f"{task}"
        )
    
    def notify_discord(self, title, description, color=0x5555FF):
        """Send notification to Discord via webhook"""
        if DISCORD_WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
            print("⚠️ Discord webhook not configured")
            return
        
        try:
            embed = {
                "embeds": [{
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": datetime.utcnow().isoformat(),
                    "footer": {
                        "text": "JC Agent Feed Watcher"
                    }
                }]
            }
            
            response = requests.post(DISCORD_WEBHOOK_URL, json=embed)
            
            if response.status_code == 204:
                print("✅ Notification sent to Discord")
            else:
                print(f"⚠️ Discord webhook failed: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Failed to send Discord notification: {e}")
    
    def show_windows_notification(self, title, message):
        """Show Windows notification"""
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name="JC Agent Feed Watcher",
                timeout=10
            )
        except ImportError:
            print("⚠️ plyer not installed - skipping Windows notification")
        except Exception as e:
            print(f"⚠️ Could not show notification: {e}")

def main():
    """Main function to start the watcher"""
    print("="*60)
    print("🤖 JC Agent Feed Watcher Starting...")
    print("="*60)
    print(f"📁 Watching: {AGENT_FEED_PATH}")
    print(f"🔔 Discord webhook: {'Configured' if DISCORD_WEBHOOK_URL != 'YOUR_WEBHOOK_URL_HERE' else 'NOT CONFIGURED'}")
    print()
    print("👀 Monitoring for new entries...")
    print("Press Ctrl+C to stop")
    print("="*60)
    print()
    
    # Create event handler
    event_handler = AgentFeedWatcher()
    
    # Create observer
    observer = Observer()
    watch_dir = str(Path(AGENT_FEED_PATH).parent)
    observer.schedule(event_handler, watch_dir, recursive=False)
    
    # Start observer
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping watcher...")
        observer.stop()
    
    observer.join()
    print("✅ Watcher stopped")

if __name__ == '__main__':
    main()
