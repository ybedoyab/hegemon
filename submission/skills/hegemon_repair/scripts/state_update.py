"""Record one observation and choose the next repair action."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common


def classify(detail: str, category: str) -> str:
    if category and category != "auto":
        return category
    lowered = detail.lower()
    if "modulenotfounderror" in lowered or "no module named" in lowered:
        return "env_error"
    if "syntaxerror" in lowered:
        return "syntax"
    if "assertionerror" in lowered or "failed" in lowered:
        return "assertion"
    if not detail.strip():
        return "empty"
    return "unknown"


def decide(state: dict, event: str, category: str, repeated: bool) -> str:
    attempts = int(state.get("attempts") or 0)
    if event == "read_done":
        return "edit"
    if event == "edit_done":
        return "rerun"
    if event == "repro_written":
        return "rerun"
    if event == "guard_ok":
        return "submit"
    if event == "guard_bad":
        return "revise"
    if repeated or event == "repeated":
        if attempts >= 3:
            return "submit" if state.get("has_patch") else "stop"
        return "graph_expand"
    if category == "env_error":
        return "revise"
    if event == "failure":
        if attempts >= 2:
            return "submit" if state.get("has_patch") else "stop"
        return "revise"
    if event == "success":
        return "submit"
    return "revise"


def main() -> None:
    args = common.argv_map()
    event = args.get("event", "failure")
    detail = args.get("detail", "")[:800]
    category = classify(detail, args.get("category", "auto"))
    fingerprint = args.get("fingerprint") or common.fingerprint(detail or event)
    state = common.load_state()
    rejected = list(state.get("rejected_fingerprints") or [])
    repeated = fingerprint in rejected and event in {"failure", "edit_done", "repeated"}
    if event == "failure":
        rejected.append(fingerprint)
        state["attempts"] = int(state.get("attempts") or 0) + 1
        hypotheses = list(state.get("hypotheses") or [])
        if hypotheses and repeated:
            hypotheses[0]["status"] = "rejected"
            hypotheses[0].setdefault("evidence_against", []).append(detail[:180])
        elif hypotheses and category == "assertion":
            hypotheses[0].setdefault("evidence_against", []).append(detail[:180])
        state["hypotheses"] = hypotheses
    if event == "success":
        hypotheses = list(state.get("hypotheses") or [])
        if hypotheses:
            hypotheses[0]["status"] = "supported"
            hypotheses[0].setdefault("evidence_for", []).append("targeted check passed")
        state["hypotheses"] = hypotheses
        state["has_patch"] = True
    if event == "edit_done":
        state["has_patch"] = True
    state["rejected_fingerprints"] = rejected[-20:]
    state["last_category"] = category
    state["last_event"] = event
    events = list(state.get("events") or [])
    events.append(event)
    state["events"] = events[-30:]
    action = decide(state, event, category, repeated)
    state["next_action"] = action
    common.save_state(state)
    common.emit(
        {
            "next_action": action,
            "category": category,
            "repeated": repeated,
            "attempts": state.get("attempts", 0),
            "hypothesis_status": (state.get("hypotheses") or [{}])[0].get("status", "none"),
            "open_hypotheses": [
                item.get("id")
                for item in state.get("hypotheses") or []
                if item.get("status") == "open"
            ],
        }
    )


if __name__ == "__main__":
    main()
