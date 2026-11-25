"""Inspect the current git diff before submission. Does not modify the tree."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common


def git_lines(workspace: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(workspace), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def main() -> None:
    args = common.argv_map()
    workspace = common.resolve_workspace(args.get("workspace"))
    names = git_lines(workspace, "diff", "--name-only", "HEAD")
    numstat = git_lines(workspace, "diff", "--numstat", "HEAD")
    added = removed = 0
    for line in numstat:
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            added += int(parts[0])
            removed += int(parts[1])
    unsafe = [name for name in names if common.is_test_path(name)]
    source = [name for name in names if not common.is_test_path(name)]
    if not names:
        action = "stop"
        verdict = "empty"
    elif unsafe and not source:
        action = "revise"
        verdict = "tests_only"
    elif unsafe:
        action = "revise"
        verdict = "touches_tests"
    elif len(source) > 6:
        action = "revise"
        verdict = "too_broad"
    else:
        action = "submit"
        verdict = "ok"
    state = common.load_state()
    state["has_patch"] = bool(source)
    state["diff_verdict"] = verdict
    state["next_action"] = action
    events = list(state.get("events") or [])
    events.append(f"guard:{verdict}")
    state["events"] = events[-30:]
    common.save_state(state)
    common.emit(
        {
            "next_action": action,
            "verdict": verdict,
            "files": source[:8],
            "unsafe_files": unsafe[:8],
            "added": added,
            "removed": removed,
            "note": "Patch size is only a warning. Submit when the edit matches the issue and tests were not rewritten.",
        }
    )


if __name__ == "__main__":
    main()
