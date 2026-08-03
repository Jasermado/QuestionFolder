from __future__ import annotations

import threading
import traceback
from io import BytesIO
from pathlib import Path

import pyperclip
from PIL import Image
from pynput import keyboard

from .capture import capture_interactively, save_capture
from .config import Settings
from .history import save_history, timestamp_slug
from .notifications import notify
from .openai_client import QuestionAnalyzer
from .parser import extract_key_result
from .prompts import get_prompt


class StudyAssistant:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.analyzer = QuestionAnalyzer(
            api_key=settings.api_key,
            model=settings.model,
            timeout_seconds=settings.request_timeout_seconds,
            max_output_tokens=settings.max_output_tokens,
        )
        self._busy = threading.Lock()

    def _notify(self, title: str, message: str) -> None:
        notify(title, message, enabled=self.settings.notifications_enabled)

    def process_png(self, png_bytes: bytes) -> str:
        return self.analyzer.analyze_png(png_bytes, get_prompt(self.settings.study_mode))

    def process_image_file(self, image_path: Path) -> str:
        with Image.open(image_path) as image:
            converted = image.convert("RGB")
            buffer = BytesIO()
            converted.save(buffer, format="PNG")
        return self.process_png(buffer.getvalue())

    def handle_capture(self) -> None:
        if not self._busy.acquire(blocking=False):
            self._notify("QuestionFolder", "A capture is already being processed.")
            return

        try:
            self._notify("QuestionFolder", "Select two corners of the question.")
            result = capture_interactively()
            stem = timestamp_slug()

            capture_path = None
            if self.settings.save_captures:
                capture_path = save_capture(result, self.settings.capture_dir, stem)

            self._notify("QuestionFolder", "Analyzing the selected question…")
            response_text = self.process_png(result.png_bytes)
            key_result = extract_key_result(response_text)

            print("\n" + "=" * 72)
            print(response_text)
            print("=" * 72 + "\n")

            if self.settings.copy_mode == "full":
                pyperclip.copy(response_text)
                self._notify("QuestionFolder", "Explanation copied to clipboard.")
            elif self.settings.copy_mode == "result":
                pyperclip.copy(key_result)
                self._notify("QuestionFolder", "Key result copied to clipboard.")
            else:
                self._notify("QuestionFolder", "Analysis complete. See the console.")

            if self.settings.save_history:
                history_path = save_history(
                    self.settings.history_dir,
                    stem,
                    response_text,
                    self.settings.study_mode,
                    self.settings.model,
                    capture_path,
                )
                print(f"History saved to: {history_path}")
        except Exception as exc:
            print(f"Error: {exc}")
            traceback.print_exc()
            self._notify("QuestionFolder error", str(exc)[:220])
        finally:
            self._busy.release()

    def run(self) -> None:
        status = "enabled" if self.settings.notifications_enabled else "disabled"
        print("QuestionFolder Study Assistant")
        print("Use only for permitted study, practice, and accessibility workflows.")
        print(f"Hotkey: {self.settings.hotkey}")
        print(f"Windows toast notifications: {status}")
        print("This console remains the visible status and output window. Press Ctrl+C to quit.\n")

        with keyboard.GlobalHotKeys({self.settings.hotkey: self.handle_capture}) as listener:
            listener.join()
