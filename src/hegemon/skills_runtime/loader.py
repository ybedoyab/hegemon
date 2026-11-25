from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from hegemon.paths import SKILL_SCRIPTS


def load_script(name: str) -> ModuleType:
    path = SKILL_SCRIPTS / f"{name}.py"
    if not path.is_file():
        raise FileNotFoundError(path)
    spec = importlib.util.spec_from_file_location(f"hegemon_skill_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def script_path(name: str) -> Path:
    return SKILL_SCRIPTS / f"{name}.py"
