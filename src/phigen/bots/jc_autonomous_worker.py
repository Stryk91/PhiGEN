#!/usr/bin/env python3
"""
JC Autonomous Worker
Monitors agent-feed.jsonl and automatically executes tasks assigned to JC
Runs as a background process - the bridge between Discord and JC
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
import traceback

# Add BotFILES to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import task executor
try:
    from task_executor import TaskExecutor
except ImportError:
    TaskExecutor = None

AGENT_FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')
WORKER_LOG = Path(r'E:\PythonProjects\PhiGEN\BotFILES\worker.log')
STATE_FILE = Path(r'E:\PythonProjects\PhiGEN\BotFILES\worker_state.json')

# Authorized task assigners (agents who can assign tasks to JC)
AUTHORIZED_ASSIGNERS = {
    'DC',  # DC Bot (agent name in feed)
    'DC BOT',  # DC BOT
    'Stryk#8167',  # Stryk Discord username
    '1390653822535340162',  # Stryk Discord ID
    'lordcain',  # Stryk display name
    '821263652899782656',  # Stryk alternate ID
    'Stryker',  # Stryk alternate name
    'JC BOT',  # JC Discord Bot
    'JC',  # JC (short form)
    '1435799961202851901',  # JC Bot Discord ID
}
class AutonomousWorker:
    def __init__(self):
        self.running = False
        self.last_processed_timestamp = None
        self.executor = TaskExecutor() if TaskExecutor else None
        self.load_state()

    def load_state(self):
        """Load the last processed task timestamp"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    self.last_processed_timestamp = state.get('last_processed_timestamp')
                    self.log(f"Loaded state: last processed at {self.last_processed_timestamp}")
            except Exception as e:
                self.log(f"Could not load state: {e}")

    def save_state(self):
        """Save the last processed task timestamp"""
        try:
            state = {
                'last_processed_timestamp': self.last_processed_timestamp,
                'last_save': datetime.now(timezone.utc).isoformat()
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            self.log(f"Could not save state: {e}")

    def log(self, message):
        """Log to both console and log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        try:
            with open(WORKER_LOG, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass

    def get_pending_tasks(self):
        """Get all unprocessed tasks assigned to JC"""
        tasks = []

        try:
            if not AGENT_FEED.exists():
                return tasks

            with open(AGENT_FEED, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                try:
                    entry = json.loads(line.strip())

                    # Look for tasks assigned by authorized agents
                    agent = entry.get('agent')
                    action = entry.get('action')

                    # Check if this is a task assignment from an authorized source
                    if action == 'task_assigned' and agent in AUTHORIZED_ASSIGNERS:
                        task_timestamp = entry.get('timestamp')

                        # Only process tasks newer than our last processed timestamp
                        if self.last_processed_timestamp is None or task_timestamp > self.last_processed_timestamp:
                            # Check if this task was already completed by JC
                            if not self.is_task_completed(task_timestamp):
                                tasks.append(entry)

                    # Also check for tasks with assigned_by field (from Discord)
                    elif action == 'task_assigned':
                        details = entry.get('details', {})
                        assigned_by = details.get('assigned_by', '')

                        if assigned_by in AUTHORIZED_ASSIGNERS:
                            task_timestamp = entry.get('timestamp')

                            if self.last_processed_timestamp is None or task_timestamp > self.last_processed_timestamp:
                                if not self.is_task_completed(task_timestamp):
                                    tasks.append(entry)

                except json.JSONDecodeError:
                    continue

        except Exception as e:
            self.log(f"Error reading agent feed: {e}")

        return tasks

    def is_task_completed(self, task_timestamp):
        """Check if JC has already completed this task"""
        try:
            with open(AGENT_FEED, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                try:
                    entry = json.loads(line.strip())

                    # Look for JC completion after this task timestamp
                    if (entry.get('agent') == 'JC' and
                        entry.get('action') in ['task_complete', 'task_started'] and
                        entry.get('timestamp') > task_timestamp):

                        # Check if it's for the same task
                        # (This is a simple check - could be enhanced)
                        return True

                except json.JSONDecodeError:
                    continue

        except Exception as e:
            self.log(f"Error checking task completion: {e}")

        return False

    def execute_task(self, task_entry):
        """Execute a task and return result"""
        details = task_entry.get('details', {})
        task_desc = details.get('task', 'No description')
        priority = details.get('priority', 'MEDIUM')
        agent = task_entry.get('agent', 'Unknown')
        assigned_by = details.get('assigned_by', agent)

        self.log(f"")
        self.log(f"{'='*60}")
        self.log(f"[TASK] EXECUTING TASK")
        self.log(f"Assigned by: {assigned_by}")
        self.log(f"Priority: {priority}")
        self.log(f"Task: {task_desc}")
        self.log(f"{'='*60}")

        try:
            # Log task start
            self.log_to_agent_feed('task_started', {
                'task': task_desc,
                'priority': priority,
                'assigned_by': assigned_by,
                'started_by': 'autonomous_worker'
            })

            # Execute the task based on type
            result = self.execute_task_logic(task_entry)

            # Log task completion
            self.log_to_agent_feed('task_complete', {
                'task': task_desc,
                'priority': priority,
                'assigned_by': assigned_by,
                'result': result.get('message', 'Task completed'),
                'files_modified': result.get('files_modified', []),
                'success': result.get('success', True)
            })

            self.log(f"[OK] TASK COMPLETED: {result.get('message', 'Success')}")

            # Update state
            self.last_processed_timestamp = task_entry.get('timestamp')
            self.save_state()

            return True

        except Exception as e:
            error_msg = f"Error executing task: {str(e)}\n{traceback.format_exc()}"
            self.log(f"[ERROR] {error_msg}")

            # Log failure
            self.log_to_agent_feed('task_failed', {
                'task': task_desc,
                'error': str(e),
                'traceback': traceback.format_exc()
            })

            return False

    def execute_task_logic(self, task_entry):
        """
        Main task execution logic
        This is where we parse the task and decide what to do
        """
        details = task_entry.get('details', {})

        # Use TaskExecutor if available
        if self.executor:
            return self.executor.execute(details)

        # Fallback: Just acknowledge the task
        task_desc = details.get('task', '')
        return {
            'success': True,
            'message': f'Task acknowledged: {task_desc}',
            'files_modified': [],
            'note': 'TaskExecutor not available - task logged but not executed'
        }

    def log_to_agent_feed(self, action, details):
        """Append an entry to the agent feed"""
        try:
            entry = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'agent': 'JC',
                'action': action,
                'details': details
            }

            with open(AGENT_FEED, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')

            self.log(f"[LOG] Logged to agent feed: {action}")

        except Exception as e:
            self.log(f"Error logging to agent feed: {e}")

    def run(self):
        """Main monitoring loop"""
        self.running = True

        self.log("")
        self.log("="*60)
        self.log("[JC WORKER] AUTONOMOUS WORKER STARTED")
        self.log("="*60)
        self.log(f"Monitoring: {AGENT_FEED}")
        self.log(f"Log file: {WORKER_LOG}")
        self.log(f"Checking every 5 seconds for new tasks...")
        self.log("Press Ctrl+C to stop")
        self.log("="*60)
        self.log("")

        check_count = 0

        try:
            while self.running:
                check_count += 1

                # Get pending tasks
                tasks = self.get_pending_tasks()

                if tasks:
                    self.log(f"Found {len(tasks)} pending task(s)")

                    for task in tasks:
                        self.execute_task(task)

                elif check_count % 12 == 0:  # Log heartbeat every minute (12 * 5 seconds)
                    self.log(f"[HEARTBEAT] Worker active - no pending tasks")

                # Wait before next check
                time.sleep(5)

        except KeyboardInterrupt:
            self.log("")
            self.log("="*60)
            self.log("[JC WORKER] AUTONOMOUS WORKER STOPPED (User interrupted)")
            self.log("="*60)

        except Exception as e:
            self.log(f"[FATAL ERROR] {e}")
            self.log(traceback.format_exc())

        finally:
            self.running = False
            self.save_state()


def main():
    """Entry point"""
    worker = AutonomousWorker()
    worker.run()


if __name__ == '__main__':
    main()
