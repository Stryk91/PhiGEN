#!/usr/bin/env python3
"""
Test authorization system for JC Autonomous Worker
Adds test tasks from different users to verify authorization
"""

import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')


def add_task_from_stryk():
    """Add a task assigned by Stryk (should be accepted)"""
    task = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'agent': 'Stryk',
        'action': 'task_assigned',
        'details': {
            'task': 'Create auth_test_stryk.txt',
            'priority': 'HIGH',
            'files_to_create': ['auth_test_stryk.txt'],
            'notes': 'Testing authorization - task from Stryk'
        }
    }

    with open(AGENT_FEED, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task) + '\n')

    print("[OK] Added task from Stryk (agent='Stryk')")
    print(f"    Task: {task['details']['task']}")
    print()


def add_task_from_stryk_via_dc():
    """Add a task via DC bot but assigned by Stryk (should be accepted)"""
    task = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'agent': 'DC',
        'action': 'task_assigned',
        'details': {
            'task': 'Create auth_test_stryk_via_dc.txt',
            'priority': 'HIGH',
            'assigned_by': 'lordcain',  # Stryk's Discord username
            'assigned_via': 'Discord',
            'files_to_create': ['auth_test_stryk_via_dc.txt'],
            'notes': 'Testing authorization - task via DC from lordcain'
        }
    }

    with open(AGENT_FEED, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task) + '\n')

    print("[OK] Added task from DC Bot (assigned_by='lordcain')")
    print(f"    Task: {task['details']['task']}")
    print()


def add_task_from_stryk_with_user_id():
    """Add a task with Stryk's Discord user ID (should be accepted)"""
    task = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'agent': '1390653822535340162',  # Stryk's Discord ID
        'action': 'task_assigned',
        'details': {
            'task': 'Create auth_test_stryk_user_id.txt',
            'priority': 'HIGH',
            'files_to_create': ['auth_test_stryk_user_id.txt'],
            'notes': 'Testing authorization - task with Discord user ID'
        }
    }

    with open(AGENT_FEED, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task) + '\n')

    print("[OK] Added task with Discord user ID (agent='1390653822535340162')")
    print(f"    Task: {task['details']['task']}")
    print()


def add_task_from_unauthorized_user():
    """Add a task from unauthorized user (should be IGNORED)"""
    task = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'agent': 'UnauthorizedUser',
        'action': 'task_assigned',
        'details': {
            'task': 'Create auth_test_unauthorized.txt',
            'priority': 'HIGH',
            'files_to_create': ['auth_test_unauthorized.txt'],
            'notes': 'Testing authorization - should be IGNORED'
        }
    }

    with open(AGENT_FEED, 'a', encoding='utf-8') as f:
        f.write(json.dumps(task) + '\n')

    print("[WARN] Added task from unauthorized user (agent='UnauthorizedUser')")
    print(f"      Task: {task['details']['task']}")
    print(f"      Expected: IGNORED by worker")
    print()


if __name__ == '__main__':
    print("="*60)
    print("  AUTHORIZATION TEST - Adding Test Tasks")
    print("="*60)
    print()

    print("Adding 4 test tasks to agent feed:")
    print()

    add_task_from_stryk()
    add_task_from_stryk_via_dc()
    add_task_from_stryk_with_user_id()
    add_task_from_unauthorized_user()

    print("="*60)
    print("  Test tasks added!")
    print("="*60)
    print()
    print("Now run the worker:")
    print("  python BotFILES/jc_autonomous_worker.py")
    print()
    print("Expected results:")
    print("  [OK] auth_test_stryk.txt created")
    print("  [OK] auth_test_stryk_via_dc.txt created")
    print("  [OK] auth_test_stryk_user_id.txt created")
    print("  [SKIP] auth_test_unauthorized.txt NOT created")
    print()
    print("Check worker.log to see which tasks were processed!")
    print()
