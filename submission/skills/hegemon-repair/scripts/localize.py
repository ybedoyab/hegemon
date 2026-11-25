"""Rank repository files and symbols for one issue. Writes state under /tmp."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common


def traceback_targets(problem: str, root: Path) -> dict[str, int]:
    targets: dict[str, int] = {}
    for raw_path, line in common.TRACE_RE.findall(problem):
        candidate = Path(raw_path)
        if candidate.is_absolute():
            try:
                relative = candidate.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                relative = candidate.name
        else:
            relative = candidate.as_posix()
        targets[relative] = int(line)
    return targets


def score_repository(root: Path, problem: str) -> dict:
    query = common.query_terms(problem)
    traces = traceback_targets(problem, root)
    ranked: list[dict] = []
    symbols: list[dict] = []
    if not query and not traces:
        return {"files": [], "symbols": [], "confidence": 0.0, "strategy": "search_first"}

    for path in common.iter_python_files(root):
        relative = path.relative_to(root).as_posix()
        text = common.read_bounded(path)
        if not text:
            continue
        counts = Counter(common.terms(text))
        name_terms = set(common.terms(relative))
        score = 0.0
        for term, weight in query.items():
            if term in name_terms:
                score += 8.0 * weight
            frequency = counts[term]
            if frequency:
                score += weight * (1.0 + frequency) ** 0.5
        line_hint = traces.get(relative) or traces.get(path.name)
        if line_hint:
            score += 40.0
        test_file = common.is_test_path(relative)
        code_score = score * (0.2 if test_file else 1.0)
        if code_score <= 0 and not line_hint:
            continue
        spans = common.function_spans(text)
        best_symbol = None
        best_symbol_score = 0.0
        for name, line in spans:
            symbol_score = 0.0
            for term in common.terms(name):
                if term in query:
                    symbol_score += 6.0 * query[term]
            if symbol_score > best_symbol_score:
                best_symbol_score = symbol_score
                best_symbol = {"name": name, "line": line}
        if best_symbol and best_symbol_score:
            code_score += best_symbol_score
            symbols.append(
                {
                    "name": best_symbol["name"],
                    "file": relative,
                    "line": best_symbol["line"],
                    "score": round(best_symbol_score, 2),
                }
            )
        start_line = 1
        if line_hint:
            start_line = max(1, line_hint - 15)
        elif best_symbol:
            start_line = max(1, best_symbol["line"] - 5)
        ranked.append(
            {
                "file": relative,
                "score": round(code_score, 2),
                "start_line": start_line,
                "end_line": start_line + 79,
                "is_test": test_file,
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    symbols.sort(key=lambda item: item["score"], reverse=True)
    primary = [item for item in ranked if not item["is_test"]]
    tests = [item for item in ranked if item["is_test"]]
    top = primary[:5]
    top_score = top[0]["score"] if top else 0.0
    second = top[1]["score"] if len(top) > 1 else 0.0
    confidence = 0.0 if top_score <= 0 else top_score / (top_score + second + 1e-6)
    if not top:
        strategy = "search_first"
    elif confidence >= 0.62:
        strategy = "direct_repair"
    elif len(top) >= 3 and confidence < 0.45:
        strategy = "search_first"
    else:
        strategy = "direct_repair"
    if any(not item["is_test"] for item in ranked[:4]) and sum(1 for item in primary[:4] if item["score"] > top_score * 0.75) >= 3:
        strategy = "multi_file"
    return {
        "files": top,
        "related_tests": tests[:3],
        "symbols": symbols[:6],
        "confidence": round(confidence, 3),
        "strategy": strategy,
    }


def is_skill_tree(root: Path) -> bool:
    return (root / "SKILL.md").is_file() and (root / "scripts" / "localize.py").is_file()


def has_repo_marker(root: Path) -> bool:
    return any((root / name).exists() for name in (".git", "pyproject.toml", "setup.py", "setup.cfg"))


def discover_workspace(explicit: str | None, sandbox_root: Path | None = None) -> Path | None:
    """Find the task repository.

    The skill process often cannot see the harness path /workspace. The subprocess
    sandbox keeps the checkout under /tmp/swegemma_sandbox_*/workspace. Scanning the
    skill directory ranks this script and reports a false confidence.
    """
    ordered: list[Path] = []
    if explicit:
        ordered.append(Path(explicit))
    ordered.append(common.default_workspace())
    root = sandbox_root if sandbox_root is not None else Path("/tmp")
    if root.is_dir():
        sandboxes = [path for path in root.glob("swegemma_sandbox_*") if path.is_dir()]
        sandboxes.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        for sandbox in sandboxes[:4]:
            ordered.append(sandbox / "workspace")
            ordered.append(sandbox)
    for candidate in ordered:
        try:
            if candidate.is_dir() and not is_skill_tree(candidate) and has_repo_marker(candidate):
                return candidate.resolve()
        except OSError:
            continue
    for candidate in ordered[:2]:
        try:
            if candidate.is_dir() and not is_skill_tree(candidate):
                return candidate.resolve()
        except OSError:
            continue
    return None


def next_action_for(localization: dict) -> str:
    files = localization.get("files") or []
    if not files:
        return "graph_expand"
    if localization.get("strategy") == "search_first" and localization.get("confidence", 0) < 0.45:
        return "graph_expand"
    return "read_top_file"


def main() -> None:
    args = common.argv_map()
    problem = args.get("problem", "")
    problem_file = args.get("problem_file")
    if problem_file:
        path = Path(problem_file)
        if path.is_file():
            problem = path.read_text(encoding="utf-8", errors="replace")
    workspace = discover_workspace(args.get("workspace"))
    if workspace is None:
        common.emit(
            {
                "error": "workspace_not_visible",
                "next_action": "graph_expand",
                "note": "The skill cannot see the repository. Call search_similar_code with a symbol copied from the issue, then read_file.",
            }
        )
        return
    if not problem.strip():
        common.emit({"error": "problem_required", "next_action": "stop"})
        return
    # A title paraphrase produced confidence 0 on the first real task and the
    # model then searched unrelated scripts. A query with a function name,
    # exception, or path is still accepted.
    codeish = re.compile(r"[A-Za-z_][A-Za-z0-9]*_[A-Za-z0-9_]+|[A-Z][a-z0-9]+[A-Z][A-Za-z0-9]+")
    if (
        len(problem.strip()) < 80
        and not common.TRACE_RE.search(problem)
        and not common.PATH_RE.search(problem)
        and not codeish.search(problem)
    ):
        common.emit(
            {
                "error": "problem_too_short",
                "next_action": "graph_expand",
                "note": "Copy exception names and file paths from the issue. Do not pass a title.",
            }
        )
        return

    localization = score_repository(workspace, problem)
    action = next_action_for(localization)
    state = {
        "problem_hash": common.problem_hash(problem),
        "localization": localization,
        "hypotheses": [],
        "rejected_fingerprints": [],
        "events": ["localize"],
        "attempts": 0,
        "next_action": action,
    }
    if localization["files"]:
        top = localization["files"][0]
        state["hypotheses"].append(
            {
                "id": "H1",
                "cause": f"Defect is in {top['file']} near line {top['start_line']}",
                "files": [top["file"]],
                "status": "open",
                "evidence_for": ["lexical overlap with the issue"],
                "evidence_against": [],
            }
        )
    common.save_state(state)
    common.emit(
        {
            "next_action": action,
            "strategy": localization["strategy"],
            "confidence": localization["confidence"],
            "files": localization["files"],
            "symbols": localization["symbols"],
            "related_tests": localization["related_tests"],
            "state_dir": str(common.state_dir()),
            "note": (
                f"Next call is read_file on {localization['files'][0]['file']}. "
                "If that read is not truncated, the following call is edit_file. Do not grep."
                if localization["files"]
                else "No file ranked. Call search_similar_code with a symbol copied from the issue."
            ),
        }
    )


if __name__ == "__main__":
    main()
