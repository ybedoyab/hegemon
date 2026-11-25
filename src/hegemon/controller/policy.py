from __future__ import annotations

from hegemon.skills_runtime.loader import load_script


def decide_next_action(state: dict, event: str, category: str, repeated: bool) -> str:
    """Same decision function the sandbox skill uses."""
    return str(load_script("state_update").decide(state, event, category, repeated))
