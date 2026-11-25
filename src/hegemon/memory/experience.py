from __future__ import annotations

import json
from pathlib import Path


def compile_experiences(trajectories: list[dict]) -> list[dict]:
    """Turn tagged trajectories into generic repair lessons.

    Lessons never store a repository name, issue id, or patch body.
    """
    grouped: dict[str, int] = {}
    for item in trajectories:
        category = str(item.get("category") or "unknown")
        grouped[category] = grouped.get(category, 0) + 1
    lessons: list[dict] = []
    catalog = {
        "assertion": "When a patch fixes one path and another assertion fails, inspect the shared invariant before editing again.",
        "env_error": "When a test fails because a module is missing, treat it as an environment failure and do not rewrite the patch to satisfy the import.",
        "syntax": "When the edited file no longer parses, restore a syntactically valid edit before running tests again.",
        "tests_only": "When the diff only changes tests, discard it. The grader resets test files.",
        "repeated": "When the same edit fails twice, reject that hypothesis and read a different symbol.",
        "localization_miss": "When the first file does not contain the failing behavior, expand to neighbors instead of editing it.",
    }
    for category, count in sorted(grouped.items()):
        if category not in catalog:
            continue
        lessons.append(
            {
                "category": category,
                "support": count,
                "lesson": catalog[category],
            }
        )
    return lessons


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows
