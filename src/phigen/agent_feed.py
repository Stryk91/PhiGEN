"""
Agent Feed Logging for PhiGEN
Multi-agent coordination between JC (Jetbrains Claude) and DC (Desktop Claude)

Usage:
    from phigen.agent_feed import log_action, read_tail

    # JC logs completed work
    log_action("task_complete", {
        "task": "Add password validation",
        "files": ["password_vault_backend.py"],
        "tests_passing": True
    }, agent="JC")

    # DC's messages (logged manually or via helper script)
    log_action("task_assigned", {
        "task": "Implement SVG optimization pipeline",
        "priority": "HIGH",
        "files_to_modify": ["optimize_title.py"]
    }, agent="DC")
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

# PhiGEN-specific paths
_DEFAULT_ABS = Path(r"E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl")
_REPO_REL = Path("docs") / "agent-feed.jsonl"
_ENV_VAR = "PHIGEN_AGENT_FEED"


def _repo_root_from_here() -> Path:
    """Find PhiGEN repo root by walking up to find known files"""
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        # Look for PhiGEN-specific markers
        if (parent / ".git").exists() or (parent / "password_vault_app.py").exists():
            return parent
    return here.parent.parent


def get_default_feed_path() -> Path:
    """Get the agent feed path (env var > absolute default > repo-relative)"""
    env = os.getenv(_ENV_VAR)
    if env:
        return Path(env).expanduser().resolve()
    try:
        return _DEFAULT_ABS
    except Exception:
        pass
    return (_repo_root_from_here() / _REPO_REL).resolve()


@dataclass
class FeedEntry:
    timestamp: str
    agent: str
    action: str
    details: Dict[str, Any]

    def to_json_line(self) -> str:
        return json.dumps(
            {
                "timestamp": self.timestamp,
                "agent": self.agent,
                "action": self.action,
                "details": self.details,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )


def _iso_now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_feed(path: Optional[Path] = None) -> Path:
    """Ensure the feed file exists, creating it if necessary"""
    p = Path(path) if path else get_default_feed_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("", encoding="utf-8")
    return p


def log_action(
    action: str,
    details: Dict[str, Any],
    agent: str = "JC",
    feed_path: Optional[Path] = None
) -> Path:
    """Append a JSONL entry to the agent feed.

    Args:
        action: Action type (e.g., "task_complete", "task_assigned", "bug_found")
        details: Dictionary with action-specific data
        agent: Agent name ("JC" or "DC")
        feed_path: Optional override path

    Returns:
        Path to the feed file
    """
    if not isinstance(details, dict):
        raise TypeError("details must be a dict")

    path = ensure_feed(feed_path)
    entry = FeedEntry(
        timestamp=_iso_now_utc(),
        agent=agent,
        action=action,
        details=details
    )
    line = entry.to_json_line() + "\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
    return path


def read_tail(n: int = 50, feed_path: Optional[Path] = None) -> list[dict]:
    """Read last n entries from the feed

    Args:
        n: Number of entries to return (default 50)
        feed_path: Optional override path

    Returns:
        List of feed entries as dicts
    """
    path = ensure_feed(feed_path)
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return []

    tail = lines[-n:] if n and len(lines) > n else lines
    out: list[dict] = []
    for ln in tail:
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def read_all(feed_path: Optional[Path] = None) -> list[dict]:
    """Read all entries from the feed"""
    return read_tail(n=0, feed_path=feed_path)


# Convenience helpers for common actions

def jc_task_complete(
    task: str,
    files: Optional[Sequence[str]] = None,
    tests_passing: bool = True,
    notes: Optional[str] = None,
    commit_hash: Optional[str] = None,
    feed_path: Optional[Path] = None,
) -> Path:
    """JC logs task completion

    Args:
        task: Description of completed task
        files: Files modified
        tests_passing: Whether tests pass
        notes: Optional notes
        commit_hash: Optional git commit
        feed_path: Optional override path
    """
    details: Dict[str, Any] = {
        "task": task,
        "tests_passing": tests_passing,
    }
    if files:
        details["files"] = list(files)
    if notes:
        details["notes"] = notes
    if commit_hash:
        details["commit_hash"] = commit_hash

    return log_action("task_complete", details, agent="JC", feed_path=feed_path)


def dc_assign_task(
    task: str,
    priority: str = "MEDIUM",
    files_to_modify: Optional[Sequence[str]] = None,
    requirements: Optional[Sequence[str]] = None,
    notes: Optional[str] = None,
    feed_path: Optional[Path] = None,
) -> Path:
    """DC assigns a task to JC

    Args:
        task: Task description
        priority: LOW, MEDIUM, HIGH
        files_to_modify: Expected files to change
        requirements: List of requirements/acceptance criteria
        notes: Additional context
        feed_path: Optional override path
    """
    details: Dict[str, Any] = {
        "task": task,
        "priority": priority,
    }
    if files_to_modify:
        details["files_to_modify"] = list(files_to_modify)
    if requirements:
        details["requirements"] = list(requirements)
    if notes:
        details["notes"] = notes

    return log_action("task_assigned", details, agent="DC", feed_path=feed_path)


def jc_found_issue(
    issue: str,
    severity: str = "MEDIUM",
    file: Optional[str] = None,
    line: Optional[int] = None,
    needs_dc_input: bool = False,
    feed_path: Optional[Path] = None,
) -> Path:
    """JC reports an issue/blocker

    Args:
        issue: Issue description
        severity: LOW, MEDIUM, HIGH, CRITICAL
        file: File where issue was found
        line: Line number
        needs_dc_input: Whether DC needs to provide guidance
        feed_path: Optional override path
    """
    details: Dict[str, Any] = {
        "issue": issue,
        "severity": severity,
        "needs_dc_input": needs_dc_input,
    }
    if file:
        details["file"] = file
    if line:
        details["line"] = line

    return log_action("issue_found", details, agent="JC", feed_path=feed_path)
