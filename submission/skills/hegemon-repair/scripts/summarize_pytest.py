"""Run one targeted pytest path, or summarize an existing output file."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common


def classify_output(text: str, returncode: int | None) -> str:
    lowered = text.lower()
    if "modulenotfounderror" in lowered or "no module named" in lowered:
        return "env_error"
    if "syntaxerror" in lowered:
        return "syntax"
    if returncode == 0 and "failed" not in lowered:
        return "pass"
    if "assertionerror" in lowered or "failed" in lowered:
        return "assertion"
    if returncode not in (0, None):
        return "error"
    return "unknown"


def allowed_target(workspace: Path, raw: str) -> Path | None:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = workspace / candidate
    resolved = candidate.resolve()
    state_root = common.state_dir().resolve()
    if common.within(workspace, resolved) or common.within(state_root, resolved):
        return resolved
    return None


def main() -> None:
    args = common.argv_map()
    workspace = common.resolve_workspace(args.get("workspace"))
    output_file = args.get("output_file")
    if output_file:
        path = allowed_target(workspace, output_file)
        if path is None or not path.is_file():
            common.emit({"error": "output_file_rejected", "next_action": "revise", "category": "env_error"})
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        category = classify_output(text, 0 if "passed" in text.lower() and "failed" not in text.lower() else 1)
        event = "success" if category == "pass" else "failure"
        common.emit(
            {
                "next_action": "submit" if category == "pass" else "revise",
                "category": category,
                "event": event,
                "tail": "\n".join(text.splitlines()[-25:])[:1200],
            }
        )
        return

    target = args.get("target")
    if not target:
        common.emit({"error": "target_required", "next_action": "revise"})
        return
    path = allowed_target(workspace, target)
    if path is None:
        common.emit({"error": "target_outside_workspace", "next_action": "revise"})
        return
    try:
        relative = path.resolve().relative_to(workspace.resolve()).as_posix()
    except ValueError:
        relative = str(path)
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--tb=line",
                "-p",
                "no:anyio",
                relative,
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        common.emit({"next_action": "revise", "category": "timeout", "event": "failure"})
        return
    except OSError as exc:
        common.emit({"next_action": "revise", "category": "env_error", "event": "failure", "detail": str(exc)[:200]})
        return
    combined = (completed.stdout or "") + "\n" + (completed.stderr or "")
    category = classify_output(combined, completed.returncode)
    if "No module named pytest" in combined or completed.returncode == 2 and "pytest" in combined.lower():
        category = "env_error"
    common.emit(
        {
            "next_action": "submit" if category == "pass" else "revise",
            "category": category,
            "returncode": completed.returncode,
            "event": "success" if category == "pass" else "failure",
            "tail": "\n".join(combined.splitlines()[-25:])[:1200],
        }
    )


if __name__ == "__main__":
    main()
