from __future__ import annotations

from hegemon.paths import PROMPT_PARTS, SYSTEM_PROMPT

PART_ORDER = (
    "01_role.md",
    "02_policy.md",
    "03_tools.md",
    "04_constraints.md",
)


def render_system_prompt() -> str:
    chunks: list[str] = []
    for name in PART_ORDER:
        path = PROMPT_PARTS / name
        text = path.read_text(encoding="utf-8").strip()
        chunks.append(text)
    return "\n\n".join(chunks) + "\n"


def write_system_prompt() -> str:
    rendered = render_system_prompt()
    SYSTEM_PROMPT.parent.mkdir(parents=True, exist_ok=True)
    SYSTEM_PROMPT.write_text(rendered, encoding="utf-8")
    return rendered
