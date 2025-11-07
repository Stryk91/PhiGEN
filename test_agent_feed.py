#!/usr/bin/env python3
"""
Test script to verify agent feed system works correctly
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from phigen.agent_feed import (
    log_action,
    jc_task_complete,
    dc_assign_task,
    jc_found_issue,
    read_tail
)


def test_basic_logging():
    """Test basic log_action functionality"""
    print("Testing basic logging...")

    path = log_action("test_action", {
        "message": "This is a test entry",
        "test_number": 1
    }, agent="System")

    assert path.exists(), "Feed file should exist"
    print(f"[OK] Feed file created: {path}")


def test_dc_assign_task():
    """Test DC assigning a task"""
    print("\nTesting DC task assignment...")

    dc_assign_task(
        task="Add SVG transparency fix",
        priority="HIGH",
        files_to_modify=["convert_svg_transparent.py", "optimize_title.py"],
        requirements=[
            "Remove white backgrounds",
            "Preserve original quality",
            "Add batch processing"
        ],
        notes="This is part of the UI polish sprint"
    )

    print("[OK] DC task assigned")


def test_jc_task_complete():
    """Test JC completing a task"""
    print("\nTesting JC task completion...")

    jc_task_complete(
        task="Add SVG transparency fix",
        files=["convert_svg_transparent.py", "optimize_title.py"],
        tests_passing=True,
        notes="Implemented using PIL ImageOps, batch processing working"
    )

    print("[OK] JC task completed")


def test_jc_found_issue():
    """Test JC logging an issue"""
    print("\nTesting JC issue logging...")

    jc_found_issue(
        issue="Missing PySide6 dependency for Qt UI",
        severity="HIGH",
        file="run_qt_ui.py",
        line=15,
        needs_dc_input=True
    )

    print("[OK] JC issue logged")


def test_read_feed():
    """Test reading the feed"""
    print("\nTesting feed reading...")

    entries = read_tail(10)

    assert len(entries) > 0, "Should have entries in feed"
    print(f"[OK] Read {len(entries)} entries from feed")

    print("\nRecent entries:")
    print("-" * 60)
    for entry in entries[-5:]:
        agent = entry.get("agent", "?")
        action = entry.get("action", "?")
        timestamp = entry.get("timestamp", "")[:19]
        print(f"[{timestamp}] {agent} -> {action}")


def test_custom_actions():
    """Test custom action logging"""
    print("\nTesting custom actions...")

    # JC refactoring
    log_action("code_refactor", {
        "file": "password_vault_backend.py",
        "description": "Extracted validation logic to separate module",
        "functions_added": ["validate_password", "check_strength"]
    }, agent="JC")

    # DC design decision
    log_action("design_decision", {
        "decision": "Use SQLite for password storage",
        "rationale": "Better performance and ACID compliance",
        "affected_files": ["password_vault_backend.py"]
    }, agent="DC")

    print("[OK] Custom actions logged")


def main():
    print("="*60)
    print("PhiGEN Agent Feed System Test")
    print("="*60)

    try:
        test_basic_logging()
        test_dc_assign_task()
        test_jc_task_complete()
        test_jc_found_issue()
        test_custom_actions()
        test_read_feed()

        print("\n" + "="*60)
        print("ALL TESTS PASSED")
        print("="*60)
        print("\nAgent coordination system is ready to use!")
        print("\nNext steps:")
        print("  - JC: run 'python jc_read_feed.py' to see tasks")
        print("  - DC: run 'python dc_log_message.py' to assign tasks")
        print("  - Read docs/AGENT_COORDINATION.md for full guide")
        print()

    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
