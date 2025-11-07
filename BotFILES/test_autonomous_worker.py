#!/usr/bin/env python3
"""
Test script for JC Autonomous Worker
Simulates a task assignment and verifies the worker processes it
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone

AGENT_FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')


def add_test_task():
    """Add a test task to the agent feed"""
    task = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'agent': 'DC',
        'action': 'task_assigned',
        'details': {
            'task': 'Create test file hello_world.txt',
            'priority': 'HIGH',
            'files_to_create': ['hello_world.txt'],
            'notes': 'This is a test task from the autonomous worker test script'
        }
    }

    print("Adding test task to agent feed...")
    print(f"Task: {task['details']['task']}")
    print()

    with open(AGENT_FEED, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task) + '\n')

    print("Test task added!")
    print()
    print("Now run the autonomous worker:")
    print("  python BotFILES\\jc_autonomous_worker.py")
    print()
    print("The worker should:")
    print("  1. Detect the task")
    print("  2. Create hello_world.txt")
    print("  3. Log completion to agent-feed.jsonl")
    print()


if __name__ == '__main__':
    add_test_task()
