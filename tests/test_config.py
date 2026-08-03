from pathlib import Path

import pytest

from question_folder.config import Settings, as_bool


def test_as_bool() -> None:
    assert as_bool("true", False) is True
    assert as_bool("0", True) is False


def test_as_bool_invalid() -> None:
    with pytest.raises(ValueError):
        as_bool("sometimes", True)


def test_notifications_can_be_disabled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("NOTIFICATIONS_ENABLED", raising=False)
    env = tmp_path / ".env"
    env.write_text(
        "OPENAI_API_KEY=test-key\nNOTIFICATIONS_ENABLED=false\n",
        encoding="utf-8",
    )
    settings = Settings.from_env(env)
    assert settings.notifications_enabled is False
