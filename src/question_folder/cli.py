from __future__ import annotations

import argparse
from pathlib import Path

import pyperclip

from .app import StudyAssistant
from .config import Settings
from .parser import extract_key_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="question-folder",
        description="Transparent screenshot-based study assistant.",
    )
    parser.add_argument("--env-file", type=Path, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run", help="Start the global hotkey listener.")

    analyze = subparsers.add_parser("analyze", help="Analyze an existing image file.")
    analyze.add_argument("image", type=Path)
    analyze.add_argument("--no-copy", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = Settings.from_env(args.env_file)
    app = StudyAssistant(settings)

    if args.command == "run":
        app.run()
        return

    if not args.image.is_file():
        raise SystemExit(f"Image not found: {args.image}")

    response = app.process_image_file(args.image)
    print(response)
    if not args.no_copy and settings.copy_mode != "none":
        content = extract_key_result(response) if settings.copy_mode == "result" else response
        pyperclip.copy(content)
