"""Stdlib helpers for HEGEMON skill scripts.

These files run inside the competition sandbox. They must not import third-party
packages, open a network connection, or execute text taken from the issue.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

def state_dir() -> Path:
    return Path(os.environ.get("HEGEMON_STATE_DIR", "/tmp/hegemon"))


def default_workspace() -> Path:
    return Path(os.environ.get("HEGEMON_WORKSPACE", "/workspace"))
MAX_OUTPUT_CHARS = 3400
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".tox",
    "dist",
    "build",
    ".eggs",
    ".mypy_cache",
    ".pytest_cache",
}
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "are",
    "was",
    "were",
    "not",
    "but",
    "you",
    "your",
    "when",
    "into",
    "should",
    "would",
    "could",
    "have",
    "has",
    "had",
    "does",
    "did",
    "error",
    "issue",
    "bug",
    "fix",
    "please",
    "using",
    "used",
    "file",
    "line",
    "code",
    "test",
    "tests",
    "none",
    "true",
    "false",
}
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
TRACE_RE = re.compile(r'File "([^"]+\.py)", line (\d+)')
BACKTICK_RE = re.compile(r"`([^`]{2,80})`")
PATH_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]+\.py")

ACTIONS = (
    "read_top_file",
    "graph_expand",
    "edit",
    "reproduce",
    "rerun",
    "revise",
    "submit",
    "stop",
)


def emit(payload: dict) -> None:
    text = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    if len(text) > MAX_OUTPUT_CHARS:
        payload = {
            "truncated": True,
            "next_action": payload.get("next_action", "revise"),
            "preview": text[: MAX_OUTPUT_CHARS - 80],
        }
        text = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    sys.stdout.write(text + "\n")


def argv_map(argv: list[str] | None = None) -> dict[str, str]:
    args = list(sys.argv[1:] if argv is None else argv)
    out: dict[str, str] = {}
    index = 0
    while index < len(args):
        token = args[index]
        if token.startswith("--") and index + 1 < len(args) and not args[index + 1].startswith("--"):
            key = token[2:].replace("-", "_")
            out[key] = args[index + 1]
            index += 2
        else:
            index += 1
    return out


def resolve_workspace(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    if default_workspace().is_dir():
        return default_workspace().resolve()
    return Path.cwd().resolve()


def within(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def problem_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def load_state() -> dict:
    path = state_dir() / "state.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_state(state: dict) -> None:
    root = state_dir()
    root.mkdir(parents=True, exist_ok=True)
    target = root / "state.json"
    temporary = root / "state.json.tmp"
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(target)


def terms(text: str) -> list[str]:
    found: list[str] = []
    for token in IDENT_RE.findall(text):
        lowered = token.lower()
        if lowered in STOPWORDS or len(lowered) < 3:
            continue
        found.append(lowered)
        if "_" in token:
            found.extend(part.lower() for part in token.split("_") if len(part) > 2 and part.lower() not in STOPWORDS)
    return found


def query_terms(problem: str) -> Counter[str]:
    weighted: Counter[str] = Counter()
    for match in BACKTICK_RE.findall(problem):
        weighted.update(terms(match))
        for token in terms(match):
            weighted[token] += 3
    for path in PATH_RE.findall(problem):
        weighted.update(terms(path))
        for token in terms(Path(path).stem):
            weighted[token] += 4
    for path, _line in TRACE_RE.findall(problem):
        weighted.update(terms(Path(path).name))
        for token in terms(Path(path).stem):
            weighted[token] += 5
    weighted.update(terms(problem))
    return weighted


def is_test_path(relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    name = Path(normalized).name
    return (
        name in {"conftest.py", "pytest.ini", "setup.cfg", "tox.ini"}
        or name.startswith("test_")
        or name.endswith("_test.py")
        or "/tests/" in f"/{normalized}"
        or normalized.startswith("tests/")
        or "/testing/" in f"/{normalized}"
    )


def iter_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS and not name.startswith(".git")]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            path = Path(dirpath) / filename
            if path.is_symlink():
                continue
            if not within(root, path):
                continue
            files.append(path)
    return files


def read_bounded(path: Path, limit: int = 200_000) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return data[:limit]


def function_spans(text: str) -> list[tuple[str, int]]:
    spans: list[tuple[str, int]] = []
    for index, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("class ") or stripped.startswith("async def "):
            parts = stripped.split()
            if len(parts) >= 2:
                name = parts[1].split("(")[0].split(":")[0]
                if name.isidentifier():
                    spans.append((name, index))
    return spans


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:12]
