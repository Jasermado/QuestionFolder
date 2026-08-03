from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str = "gpt-4o-mini"
    hotkey: str = "<ctrl>+<shift>+q"
    study_mode: str = "explain"
    copy_mode: str = "full"
    notifications_enabled: bool = True
    save_captures: bool = True
    save_history: bool = True
    capture_dir: Path = Path("captures")
    history_dir: Path = Path("history")
    max_output_tokens: int = 1200
    request_timeout_seconds: float = 90.0

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> "Settings":
        load_dotenv(dotenv_path=env_file, override=False)

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
            )

        study_mode = os.getenv("STUDY_MODE", "explain").strip().lower()
        if study_mode not in {"explain", "hint", "concise"}:
            raise ValueError("STUDY_MODE must be explain, hint, or concise.")

        copy_mode = os.getenv("COPY_MODE", "full").strip().lower()
        if copy_mode not in {"full", "result", "none"}:
            raise ValueError("COPY_MODE must be full, result, or none.")

        return cls(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
            hotkey=os.getenv("HOTKEY", "<ctrl>+<shift>+q").strip(),
            study_mode=study_mode,
            copy_mode=copy_mode,
            notifications_enabled=as_bool(os.getenv("NOTIFICATIONS_ENABLED"), True),
            save_captures=as_bool(os.getenv("SAVE_CAPTURES"), True),
            save_history=as_bool(os.getenv("SAVE_HISTORY"), True),
            capture_dir=Path(os.getenv("CAPTURE_DIR", "captures")),
            history_dir=Path(os.getenv("HISTORY_DIR", "history")),
            max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "1200")),
            request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "90")),
        )
