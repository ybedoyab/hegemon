from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from hegemon.budgets.allocator import per_task_seconds
from hegemon.packaging.build import build_zip, verify_zip
from hegemon.paths import DIST, ROOT, SUBMISSION
from hegemon.prompts.render import write_system_prompt
from hegemon.skills_runtime.loader import load_script


def _env_report() -> dict:
    gpu = "unavailable"
    try:
        completed = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if completed.returncode == 0:
            gpu = completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        gpu = "unavailable"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "gpu": gpu,
        "kaggle_credentials": Path.home().joinpath(".kaggle", "kaggle.json").is_file(),
        "docker": shutil.which("docker") is not None,
        "git": shutil.which("git") is not None,
        "workspace": str(ROOT),
        "real_model_eval": "NOT_RUN",
        "reason": "Local GPU is 4 GB. Official Gemma QAT checkpoints are not loaded. Kaggle dataset is not present.",
    }


def _cmd_pack(args: argparse.Namespace) -> int:
    write_system_prompt()
    DIST.mkdir(parents=True, exist_ok=True)
    info = build_zip(SUBMISSION, DIST / "submission.zip")
    errors = verify_zip(DIST / "submission.zip")
    if errors:
        print(json.dumps({"errors": errors}))
        return 1
    (DIST / "SHA256SUMS").write_text(f"{info['sha256']}  submission.zip\n", encoding="utf-8")
    (DIST / "submission_manifest.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(info))
    return 0


def _cmd_localize(args: argparse.Namespace) -> int:
    os.environ["HEGEMON_WORKSPACE"] = str(Path(args.workspace).resolve())
    os.environ["HEGEMON_STATE_DIR"] = str(Path(args.state_dir).resolve())
    sys.argv = ["localize.py", "--problem", args.problem, "--workspace", args.workspace]
    load_script("localize").main()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hegemon")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("env")
    pack = sub.add_parser("pack")
    pack.set_defaults(func=_cmd_pack)
    locate = sub.add_parser("localize")
    locate.add_argument("--workspace", required=True)
    locate.add_argument("--problem", required=True)
    locate.add_argument("--state-dir", required=True)
    locate.set_defaults(func=_cmd_localize)
    budget = sub.add_parser("budget")
    budget.add_argument("--tasks", type=int, default=120)
    budget.add_argument("--hours", type=float, default=12)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "env":
        print(json.dumps(_env_report(), indent=2))
        return 0
    if args.command == "budget":
        seconds = per_task_seconds(
            args.tasks,
            int(args.hours * 3600),
            reserve_seconds=20 * 60,
            setup_seconds_each=45,
        )
        print(json.dumps({"per_task_seconds": seconds, "per_task_minutes": round(seconds / 60, 2)}))
        return 0
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
