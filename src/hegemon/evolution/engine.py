from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Candidate:
    name: str
    prompt_text: str
    solve_rate: float | None
    tasks_solved: int | None
    tasks_attempted: int | None
    status: str


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def apply_mutation(prompt_text: str, bullet: str) -> str:
    marker = "<!-- evolve -->"
    line = f"- {bullet.strip()}"
    if marker not in prompt_text:
        return prompt_text.rstrip() + "\n\n" + marker + "\n" + line + "\n"
    head, tail = prompt_text.split(marker, 1)
    if line in tail:
        return prompt_text
    return head + marker + "\n" + line + tail


def promote(champion: Candidate, challenger: Candidate) -> tuple[Candidate, str]:
    """Promote only a measured, non-regressing challenger on the same task count."""
    if challenger.status != "MEASURED":
        return champion, "rejected_unmeasured"
    if challenger.solve_rate is None or challenger.tasks_attempted is None:
        return champion, "rejected_missing_metrics"
    if champion.status == "MEASURED" and champion.tasks_attempted != challenger.tasks_attempted:
        return champion, "rejected_incomparable_split"
    if champion.status == "MEASURED" and champion.solve_rate is not None:
        if challenger.solve_rate <= champion.solve_rate:
            return champion, "rejected_no_improvement"
    return challenger, "promoted"


def write_lineage(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
