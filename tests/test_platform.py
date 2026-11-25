from __future__ import annotations

import json
from pathlib import Path

import pytest

from hegemon.budgets.allocator import per_task_seconds, should_stop_early
from hegemon.evolution.engine import Candidate, apply_mutation, promote
from hegemon.memory.experience import compile_experiences
from hegemon.packaging.build import PackageError, build_zip, validate_tree, verify_zip
from hegemon.paths import SUBMISSION
from hegemon.prompts.render import render_system_prompt, write_system_prompt


def test_prompt_contains_policy_actions() -> None:
    text = render_system_prompt()
    assert "edit_file" in text
    assert "submit_patch" in text
    assert "git grep -n" in text
    assert "run_skill_script" not in text
    assert "exactly one tool" not in text
    assert len(text) < 3500


def test_rendered_prompt_matches_checked_in_file() -> None:
    rendered = write_system_prompt()
    assert rendered == (SUBMISSION / "prompts" / "system.md").read_text(encoding="utf-8")


def test_budget_leaves_reserve() -> None:
    seconds = per_task_seconds(120, 12 * 3600, reserve_seconds=20 * 60, setup_seconds_each=45)
    assert seconds * 120 < 12 * 3600
    assert seconds <= 360
    assert should_stop_early(has_verified_patch=True, attempts=1, remaining_tool_calls=2, repeated=False)


def test_evolution_rejects_unmeasured_and_regressions() -> None:
    champion = Candidate("base", "prompt", 0.2, 2, 10, "MEASURED")
    unmeasured = Candidate("new", "prompt2", None, None, None, "NOT_RUN")
    kept, reason = promote(champion, unmeasured)
    assert kept.name == "base"
    assert reason == "rejected_unmeasured"
    worse = Candidate("worse", "prompt3", 0.1, 1, 10, "MEASURED")
    kept, reason = promote(champion, worse)
    assert reason == "rejected_no_improvement"
    better = Candidate("better", "prompt4", 0.3, 3, 10, "MEASURED")
    kept, reason = promote(champion, better)
    assert reason == "promoted"
    mutated = apply_mutation("base\n", "Read the boundary function.")
    assert "Read the boundary function." in mutated
    assert apply_mutation(mutated, "Read the boundary function.") == mutated


def test_experience_compiler_drops_task_identity() -> None:
    lessons = compile_experiences(
        [
            {
                "category": "env_error",
                "repo": "fastapi/fastapi",
                "instance_id": "secret-task",
                "patch": "diff --git a/app.py",
            },
            {"category": "assertion", "repo": "encode/httpx"},
        ]
    )
    blob = json.dumps(lessons)
    assert "fastapi" not in blob
    assert "httpx" not in blob
    assert "secret-task" not in blob
    assert "diff --git" not in blob
    assert any(item["category"] == "env_error" for item in lessons)


def test_official_submission_shape() -> None:
    agent = (SUBMISSION / "agent.yaml").read_text(encoding="utf-8")
    eval_config = (SUBMISSION / "eval_config.yaml").read_text(encoding="utf-8")
    sampling = (SUBMISSION / "configs" / "sampling.yaml").read_text(encoding="utf-8")
    assert "skills:" not in agent
    assert "hegemon_repair" not in agent
    assert "- name:" not in agent
    assert "evaluation:" in eval_config
    assert "max_tool_calls:" in eval_config
    assert "thinking_level" not in sampling
    assert "thinking_budget: 1024" in sampling
    assert "max_output_tokens: 4096" in sampling


def test_submission_tree_and_zip(tmp_path: Path) -> None:
    write_system_prompt()
    errors = validate_tree(SUBMISSION)
    assert errors == []
    info = build_zip(SUBMISSION, tmp_path / "submission.zip")
    assert verify_zip(tmp_path / "submission.zip") == []
    assert info["sha256"]
    import zipfile

    with zipfile.ZipFile(tmp_path / "submission.zip") as archive:
        names = archive.namelist()
    assert "agent.yaml" in names
    assert "prompts/system.md" in names
    assert all(not name.startswith("prompts/parts/") for name in names)
    assert all("tasks.jsonl" not in name for name in names)


def test_package_rejects_secret_file(tmp_path: Path) -> None:
    root = tmp_path / "submission"
    root.mkdir()
    (root / "agent.yaml").write_text(
        "agent_class: LlmAgent\nmodel: gemma-4-31b-it-qat-w4a16-ct\ninstruction: !include prompts/system.md\n",
        encoding="utf-8",
    )
    (root / "prompts").mkdir()
    (root / "prompts" / "system.md").write_text("repair\n", encoding="utf-8")
    skills = root / "skills" / "hegemon_repair"
    skills.mkdir(parents=True)
    (skills / "SKILL.md").write_text("---\nname: hegemon_repair\ndescription: test\n---\n", encoding="utf-8")
    (root / "kaggle.json").write_text('{"key":"secret"}\n', encoding="utf-8")
    with pytest.raises(PackageError):
        build_zip(root, tmp_path / "bad.zip")
