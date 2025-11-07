#!/usr/bin/env python3
"""
JC Feed Reader - Quick script for JC to check tasks and log completions

Usage (in PyCharm terminal):
    python jc_read_feed.py           # Show recent tasks
    python jc_read_feed.py --all     # Show all feed entries
"""
import sys
from pathlib import Path

# Add phigen package to path
sys.path.insert(0, str(Path(__file__).parent))

from phigen.agent_feed import read_tail, read_all


def main():
    show_all = "--all" in sys.argv

    print("="*70)
    print("PhiGEN Agent Feed - JC View")
    print("="*70)

    entries = read_all() if show_all else read_tail(20)

    if not entries:
        print("\n(No entries in feed yet)\n")
        return

    # Group by agent
    dc_tasks = []
    jc_completions = []
    other = []

    for entry in entries:
        agent = entry.get("agent", "")
        action = entry.get("action", "")

        if agent == "DC" and "task" in action.lower():
            dc_tasks.append(entry)
        elif agent == "JC":
            jc_completions.append(entry)
        else:
            other.append(entry)

    # Show DC tasks (most important for JC)
    if dc_tasks:
        print("\n[TASKS FROM DC]")
        print("-" * 70)
        for entry in dc_tasks[-10:]:  # Last 10 tasks
            timestamp = entry.get("timestamp", "")[:19]
            action = entry.get("action", "")
            details = entry.get("details", {})

            task = details.get("task", "")
            priority = details.get("priority", "MEDIUM")
            files = details.get("files_to_modify", [])
            requirements = details.get("requirements", [])

            print(f"\n[{timestamp}] Priority: {priority}")
            print(f"  Task: {task}")
            if files:
                print(f"  Files: {', '.join(files)}")
            if requirements:
                print("  Requirements:")
                for req in requirements:
                    print(f"    - {req}")

    # Show recent JC completions (for context)
    if jc_completions:
        print("\n[RECENT JC COMPLETIONS]")
        print("-" * 70)
        for entry in jc_completions[-5:]:  # Last 5 completions
            timestamp = entry.get("timestamp", "")[:19]
            action = entry.get("action", "")
            details = entry.get("details", {})

            print(f"\n[{timestamp}] {action}")
            for key, value in details.items():
                if isinstance(value, list):
                    print(f"  {key}: {', '.join(value)}")
                else:
                    print(f"  {key}: {value}")

    # Show other entries if requested
    if show_all and other:
        print("\n[OTHER ENTRIES]")
        print("-" * 70)
        for entry in other:
            timestamp = entry.get("timestamp", "")[:19]
            agent = entry.get("agent", "")
            action = entry.get("action", "")
            print(f"[{timestamp}] {agent} → {action}")

    print("\n" + "="*70)
    print(f"Total entries: {len(entries)}")
    print("="*70 + "\n")

    print("TIP: To log task completion from Python:")
    print("   from phigen.agent_feed import jc_task_complete")
    print("   jc_task_complete('Task description', files=['file.py'], tests_passing=True)")
    print()


if __name__ == "__main__":
    main()
