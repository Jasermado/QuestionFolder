from __future__ import annotations

from datetime import datetime
from pathlib import Path


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def save_history(
    directory: Path,
    stem: str,
    response_text: str,
    mode: str,
    model: str,
    capture_path: Path | None,
) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{stem}.md"
    capture_line = f"- Capture: `{capture_path}`\n" if capture_path else "- Capture: not saved\n"
    content = (
        f"# Question review — {stem}\n\n"
        f"- Mode: `{mode}`\n"
        f"- Model: `{model}`\n"
        f"{capture_line}\n"
        f"## Response\n\n{response_text}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path
