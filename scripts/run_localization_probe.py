"""Synthetic localization probe. This is not a Kaggle solve rate."""

from __future__ import annotations

import json
from pathlib import Path

from hegemon.localization.rank import rank_files
from hegemon.paths import ROOT
from hegemon.telemetry.record import append_record

FIXTURES = ROOT / "tests" / "fixtures"
CASES = (
    {
        "id": "coercion",
        "workspace": FIXTURES / "coercion",
        "problem": "parse_value raises ValueError on the string nan. Non-integers should return None.",
        "expected": "pkg/parse.py",
    },
    {
        "id": "traceback",
        "workspace": FIXTURES / "traceback",
        "problem": 'File "pkg/io_adapter.py", line 3, in load\nValueError: bad handle',
        "expected": "pkg/io_adapter.py",
    },
)


def main() -> None:
    rows = []
    hits = 0
    for case in CASES:
        ranked = rank_files(case["workspace"], case["problem"])
        top = (ranked.get("files") or [{}])[0].get("file")
        hit = top == case["expected"]
        hits += int(hit)
        rows.append({"id": case["id"], "top": top, "expected": case["expected"], "hit": hit, "confidence": ranked.get("confidence")})
    result = {
        "experiment_id": "E_LOC001",
        "status": "MEASURED",
        "dataset": "synthetic_fixtures",
        "tasks_attempted": len(CASES),
        "top1_hits": hits,
        "top1_recall": hits / len(CASES),
        "cases": rows,
        "official_harness": "NOT_RUN",
        "solve_rate": None,
        "note": "Localization recall on two synthetic repositories. Not a leaderboard score.",
    }
    destination = ROOT / "experiments" / "E_LOC001.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    append_record(ROOT / "experiments" / "registry.jsonl", result)
    print(json.dumps({"top1_hits": hits, "tasks": len(CASES)}))


if __name__ == "__main__":
    main()
