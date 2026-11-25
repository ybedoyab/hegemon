from __future__ import annotations

from pathlib import Path

from hegemon.skills_runtime.loader import load_script


def rank_files(workspace: Path, problem: str) -> dict:
    """File and symbol ranking used by scripts/localize.py."""
    return dict(load_script("localize").score_repository(workspace, problem))
