from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = dict(record)
    body.setdefault("recorded_at", datetime.now(timezone.utc).isoformat())
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(body, sort_keys=True) + "\n")
