from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path

ALLOWED_SUFFIXES = {
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".py",
    ".json",
    ".safetensors",
}
FORBIDDEN_NAMES = {
    ".env",
    "kaggle.json",
    "tasks.jsonl",
    "credentials.json",
    "id_rsa",
}
ALLOWED_MODELS = {
    "gemma-4-31b-it-qat-w4a16-ct",
    "gemma-4-12b-it-qat-w4a16-ct",
    "gemma-4-e4b-it-qat-w4a16-ct",
    "gemma-4-e2b-it-qat-w4a16-ct",
}
SECRET_MARKERS = ("kaggle_token", "AKIA", "BEGIN PRIVATE KEY", "gho_")
MAX_ZIP_BYTES = 3 * 1024 * 1024 * 1024


class PackageError(Exception):
    pass


def iter_submission_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name != "__pycache__" and name != "parts"]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.is_symlink():
                raise PackageError(f"symlink_forbidden:{path}")
            files.append(path)
    return files


def validate_tree(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "agent.yaml").is_file():
        errors.append("missing_agent_yaml")
    if not (root / "prompts" / "system.md").is_file():
        errors.append("missing_system_prompt")
    agent_text = (root / "agent.yaml").read_text(encoding="utf-8") if (root / "agent.yaml").is_file() else ""
    if "model:" not in agent_text:
        errors.append("missing_model")
    else:
        model_line = next((line.split(":", 1)[1].strip() for line in agent_text.splitlines() if line.startswith("model:")), "")
        if model_line not in ALLOWED_MODELS:
            errors.append(f"model_not_allowed:{model_line}")
    if "prompts/system.md" not in agent_text:
        errors.append("missing_system_include")
    try:
        files = iter_submission_files(root)
    except PackageError as exc:
        return [str(exc)]
    for path in files:
        relative = path.relative_to(root).as_posix()
        if relative.startswith("../") or "/../" in relative or relative.startswith("/"):
            errors.append(f"path_traversal:{relative}")
        if path.name in FORBIDDEN_NAMES or path.suffix == ".safetensors":
            errors.append(f"forbidden_file:{relative}")
        if path.suffix.lower() not in ALLOWED_SUFFIXES and path.name != "SKILL.md":
            errors.append(f"extension_forbidden:{relative}")
        text_sample = ""
        if path.suffix.lower() in {".md", ".yaml", ".yml", ".txt", ".py", ".json"}:
            text_sample = path.read_text(encoding="utf-8", errors="replace")[:4000]
        for marker in SECRET_MARKERS:
            if marker in text_sample:
                errors.append(f"secret_marker:{relative}")
                break
    skill = root / "skills" / "hegemon-repair" / "SKILL.md"
    if not skill.is_file():
        errors.append("missing_skill")
    return errors


def build_zip(root: Path, destination: Path) -> dict:
    errors = validate_tree(root)
    if errors:
        raise PackageError(";".join(errors))
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    files = iter_submission_files(root)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        names: set[str] = set()
        for path in files:
            relative = path.relative_to(root).as_posix()
            if relative in names:
                raise PackageError(f"duplicate:{relative}")
            names.add(relative)
            archive.write(path, relative)
    size = destination.stat().st_size
    if size > MAX_ZIP_BYTES:
        raise PackageError("zip_too_large")
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return {"path": str(destination), "bytes": size, "sha256": digest, "entries": len(files)}


def verify_zip(destination: Path) -> list[str]:
    errors: list[str] = []
    with zipfile.ZipFile(destination) as archive:
        names = archive.namelist()
        if "agent.yaml" not in names:
            errors.append("zip_missing_agent_yaml")
        if any(name.startswith("/") or ".." in name.split("/") for name in names):
            errors.append("zip_path_traversal")
        if len(names) != len(set(names)):
            errors.append("zip_duplicate_entries")
        for info in archive.infolist():
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode & 0o170000 == 0o120000:
                errors.append(f"zip_symlink:{info.filename}")
    return errors
