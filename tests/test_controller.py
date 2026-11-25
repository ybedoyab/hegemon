from __future__ import annotations

from pathlib import Path

from hegemon.controller.policy import decide_next_action
from hegemon.localization.rank import rank_files


def test_controller_matches_skill_policy() -> None:
    assert decide_next_action({}, "read_done", "unknown", False) == "edit"
    assert decide_next_action({"attempts": 1, "has_patch": False}, "failure", "assertion", True) == "graph_expand"


def test_rank_wrapper_finds_parse_value() -> None:
    root = Path(__file__).parent / "fixtures" / "coercion"
    ranked = rank_files(root, "parse_value fails when given nan")
    assert ranked["files"][0]["file"] == "pkg/parse.py"
