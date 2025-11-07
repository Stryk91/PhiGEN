#!/usr/bin/env python3
"""
DC Message Logger - Interactive script for logging Desktop Claude's messages

Since DC (Desktop Claude) has no file access, use this script to manually
log DC's tasks, feedback, and instructions into the agent feed.

Usage:
    python dc_log_message.py
"""
import sys
from pathlib import Path

# Add phigen package to path
sys.path.insert(0, str(Path(__file__).parent))

from phigen.agent_feed import log_action, dc_assign_task, read_tail


def print_recent_feed(n=5):
    """Show recent feed entries"""
    print("\n" + "="*60)
    print(f"RECENT FEED (last {n} entries):")
    print("="*60)
    entries = read_tail(n)
    if not entries:
        print("(no entries yet)")
        return

    for entry in entries:
        agent = entry.get("agent", "?")
        action = entry.get("action", "?")
        timestamp = entry.get("timestamp", "")[:19]  # Truncate timestamp
        details = entry.get("details", {})

        print(f"\n[{timestamp}] {agent} → {action}")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {value}")
    print("="*60 + "\n")


def log_task_assignment():
    """Quick task assignment interface"""
    print("\n[DC TASK ASSIGNMENT]")
    print("-" * 40)

    task = input("Task description: ").strip()
    if not task:
        print("[ERROR] Task cannot be empty")
        return

    priority = input("Priority (LOW/MEDIUM/HIGH) [MEDIUM]: ").strip().upper() or "MEDIUM"
    if priority not in ["LOW", "MEDIUM", "HIGH"]:
        priority = "MEDIUM"

    files_input = input("Files to modify (comma-separated, optional): ").strip()
    files = [f.strip() for f in files_input.split(",")] if files_input else None

    requirements_input = input("Requirements (comma-separated, optional): ").strip()
    requirements = [r.strip() for r in requirements_input.split(",")] if requirements_input else None

    notes = input("Notes (optional): ").strip() or None

    # Log it
    dc_assign_task(
        task=task,
        priority=priority,
        files_to_modify=files,
        requirements=requirements,
        notes=notes
    )

    print(f"\n[OK] Task logged successfully!")


def log_custom_message():
    """Custom message interface"""
    print("\n[DC CUSTOM MESSAGE]")
    print("-" * 40)

    action = input("Action type (e.g., feedback, question, status_update): ").strip()
    if not action:
        print("[ERROR] Action cannot be empty")
        return

    message = input("Message: ").strip()
    if not message:
        print("[ERROR] Message cannot be empty")
        return

    details = {"message": message}

    # Optional fields
    target = input("Target agent (JC/all) [all]: ").strip() or "all"
    if target:
        details["target"] = target

    priority = input("Priority (LOW/MEDIUM/HIGH) [MEDIUM]: ").strip().upper() or "MEDIUM"
    details["priority"] = priority

    # Log it
    log_action(action, details, agent="DC")

    print(f"\n[OK] Message logged successfully!")


def main_menu():
    """Main interactive menu"""
    while True:
        print_recent_feed(5)

        print("DC MESSAGE LOGGER")
        print("-" * 40)
        print("1. Assign task to JC")
        print("2. Log custom message")
        print("3. View recent feed (refresh)")
        print("4. Exit")
        print()

        choice = input("Choose option (1-4): ").strip()

        if choice == "1":
            log_task_assignment()
        elif choice == "2":
            log_custom_message()
        elif choice == "3":
            continue  # Refresh (loop will show recent feed again)
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("[ERROR] Invalid choice, try again")


if __name__ == "__main__":
    print("="*60)
    print("PhiGEN - DC Message Logger")
    print("Logging messages from DC (Desktop Claude)")
    print("="*60)

    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user, goodbye!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
