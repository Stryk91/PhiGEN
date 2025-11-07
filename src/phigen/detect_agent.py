"""
Agent Identity Detection for PhiGEN

Allows Claude instances to identify themselves and verify they're reading
the correct guideline files.

Usage:
    from phigen.detect_agent import get_agent_id, verify_agent_access

    agent_id = get_agent_id()
    print(f"I am: {agent_id}")

    if not verify_agent_access("JC"):
        print("This file is not for me, exiting...")
        exit(0)
"""
import os
import sys
from pathlib import Path
from typing import Optional


def get_agent_id() -> str:
    """
    Detect which Claude agent is running.

    Returns:
        "JC" - Jetbrains Claude (PyCharm)
        "DC" - Desktop Claude (Windows app)
        "TC" - Terminal Claude (Claude Code CLI)
        "UNKNOWN" - Cannot determine
    """
    # Check environment variables first
    agent_id_env = os.getenv("PHIGEN_AGENT_ID")
    if agent_id_env:
        return agent_id_env.upper()

    # Check process/executable paths
    executable = sys.executable.lower()
    argv = " ".join(sys.argv).lower()

    # Terminal Claude Code (node.exe running claude-code/cli.js)
    if "claude-code" in argv or "cli.js" in argv:
        return "TC"

    # Desktop Claude (Electron app)
    if "anthropicclaude" in executable or "claude.exe" in executable:
        # Desktop Claude runs from AppData\Local\AnthropicClaude
        return "DC"

    # PyCharm/Jetbrains (might have pycharm in path or specific env vars)
    pycharm_markers = [
        os.getenv("PYCHARM_HOSTED"),
        os.getenv("JETBRAINS_IDE"),
        "pycharm" in os.getenv("PATH", "").lower(),
    ]
    if any(pycharm_markers):
        return "JC"

    # Check working directory patterns
    cwd = os.getcwd().lower()
    if "pycharm" in cwd or ".idea" in cwd:
        return "JC"

    return "UNKNOWN"


def verify_agent_access(required_agent: str, exit_on_fail: bool = False) -> bool:
    """
    Verify the current agent is authorized to access a resource.

    Args:
        required_agent: Required agent ID ("JC", "DC", "TC")
        exit_on_fail: If True, exit the program if verification fails

    Returns:
        True if agent is authorized, False otherwise
    """
    current = get_agent_id()

    # Normalize
    required = required_agent.upper()

    if current == required:
        return True

    if exit_on_fail:
        print(f"[AGENT VERIFICATION FAILED]")
        print(f"  This resource is for: {required}")
        print(f"  You are: {current}")
        print(f"  Exiting to prevent confusion...")
        sys.exit(1)

    return False


def get_agent_name(agent_id: str) -> str:
    """Get human-readable agent name"""
    names = {
        "JC": "Jetbrains Claude (PyCharm)",
        "DC": "Desktop Claude (Windows App)",
        "TC": "Terminal Claude (Claude Code CLI)",
        "UNKNOWN": "Unknown Agent"
    }
    return names.get(agent_id.upper(), "Unknown Agent")


def set_agent_id(agent_id: str):
    """
    Manually set agent ID via environment variable.
    Useful when auto-detection fails.

    Usage:
        from phigen.detect_agent import set_agent_id
        set_agent_id("JC")  # Force identify as Jetbrains Claude
    """
    os.environ["PHIGEN_AGENT_ID"] = agent_id.upper()


def create_agent_guard(agent_id: str, context: str = "this resource") -> str:
    """
    Create a Python code snippet that guards a resource.

    Args:
        agent_id: Required agent ("JC", "DC", "TC")
        context: Description of what's being protected

    Returns:
        Python code string to insert at top of file
    """
    return f'''# AGENT VERIFICATION GUARD
# This file is for: {agent_id} - {get_agent_name(agent_id)}
try:
    from phigen.detect_agent import verify_agent_access
    if not verify_agent_access("{agent_id}"):
        print(f"[WARNING] {context} is not for this agent")
        import sys
        sys.exit(0)
except ImportError:
    # detect_agent not available, skip verification
    pass
# END AGENT VERIFICATION GUARD

'''


# Self-test when run directly
if __name__ == "__main__":
    agent = get_agent_id()
    name = get_agent_name(agent)

    print("="*60)
    print("PhiGEN Agent Identity Detection")
    print("="*60)
    print(f"\nYour Agent ID: {agent}")
    print(f"Full Name: {name}")
    print(f"\nExecutable: {sys.executable}")
    print(f"Command: {' '.join(sys.argv)}")
    print(f"CWD: {os.getcwd()}")
    print(f"\nEnvironment Hints:")
    print(f"  PHIGEN_AGENT_ID: {os.getenv('PHIGEN_AGENT_ID', '(not set)')}")
    print(f"  PYCHARM_HOSTED: {os.getenv('PYCHARM_HOSTED', '(not set)')}")
    print(f"  JETBRAINS_IDE: {os.getenv('JETBRAINS_IDE', '(not set)')}")
    print("="*60)

    # Test verification
    print("\nTesting verification:")
    print(f"  Am I JC? {verify_agent_access('JC')}")
    print(f"  Am I DC? {verify_agent_access('DC')}")
    print(f"  Am I TC? {verify_agent_access('TC')}")
    print()
