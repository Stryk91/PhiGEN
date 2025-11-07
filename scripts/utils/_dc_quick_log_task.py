#!/usr/bin/env python3
"""Direct append to agent feed - no imports needed"""
import json
from datetime import datetime, timezone
from pathlib import Path

# Path to agent feed
feed_path = Path(r"E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl")

# Create the task entry
entry = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "agent": "DC",
    "action": "task_assigned",
    "details": {
        "task": "Add minimum password length validation function to backend",
        "priority": "MEDIUM",
        "files_to_modify": ["password_vault_backend.py"],
        "requirements": [
            "Create function: validate_min_length(password: str, min_length: int = 8) -> tuple[bool, str]",
            "Returns (True, 'Valid') if password meets length requirement",
            "Returns (False, 'Password must be at least 8 characters') if too short",
            "Add basic unit test for this function",
            "Use type hints and docstrings with examples"
        ],
        "notes": "This is foundational - other validation functions will follow this same pattern. Keep it simple - just length checking, no regex or complexity checks yet. This is Task 1 of the password security series."
    }
}

# Append to feed
with open(feed_path, 'a', encoding='utf-8') as f:
    f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")

print('✅ Task assigned to JC successfully!')
print(f'✅ Task logged at: {entry["timestamp"]}')
print('\nJC can now check the agent feed for this task.')
