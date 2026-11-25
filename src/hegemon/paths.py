from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"
SKILL_SCRIPTS = SUBMISSION / "skills" / "hegemon-repair" / "scripts"
PROMPT_PARTS = SUBMISSION / "prompts" / "parts"
SYSTEM_PROMPT = SUBMISSION / "prompts" / "system.md"
EXPERIMENTS = ROOT / "experiments"
DIST = ROOT / "dist"
