#!/usr/bin/env python3
"""Extract pending tasks from agent feed"""
import json
from pathlib import Path

FEED = Path(r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl')
OUTPUT = Path(r'E:\PythonProjects\PhiGEN\BotFILES\pending.txt')

completed = set()
pending = []

with open(FEED, 'r', encoding='utf-8') as f:
    for line in f:
        entry = json.loads(line)
        agent = entry.get('agent')
        action = entry.get('action')
        
        if agent == 'JC' and action in ['task_complete', 'task_started']:
            task = entry.get('details', {}).get('task', '')
            completed.add(task)
        
        elif agent == 'DC' and action == 'task_assigned':
            task = entry.get('details', {}).get('task', '')
            if task not in completed:
                priority = entry.get('details', {}).get('priority', 'MEDIUM')
                pending.append(f"[{priority}] {task}")

if pending:
    numbered = [f"{i+1}. {t}" for i, t in enumerate(pending)]
    OUTPUT.write_text('\n'.join(numbered))
    print(f"✅ {len(pending)} pending tasks:")
    for t in numbered:
        print(f"  {t}")
    print("\nTell DC: execute task 1,3,5 (or 'all')")
else:
    OUTPUT.write_text("")
    print("No pending tasks")
