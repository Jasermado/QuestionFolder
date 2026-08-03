from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageGrab
from pynput import mouse


@dataclass(frozen=True)
class CaptureResult:
    image: Image.Image
    png_bytes: bytes
    box: tuple[int, int, int, int]


def select_region() -> tuple[int, int, int, int]:
    points: list[tuple[int, int]] = []

    def on_click(x: float, y: float, button: mouse.Button, pressed: bool):
        if pressed and button == mouse.Button.left:
            points.append((int(x), int(y)))
            print(f"Corner {len(points)} selected at ({int(x)}, {int(y)})")
            if len(points) == 2:
                return False
        return None

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if len(points) != 2:
        raise RuntimeError("Region selection ended before two corners were selected.")

    (x1, y1), (x2, y2) = points
    box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    if box[0] == box[2] or box[1] == box[3]:
        raise ValueError("The selected region has zero width or height.")
    return box


def capture_interactively() -> CaptureResult:
    print("Click the top-left and bottom-right corners of the question.")
    box = select_region()
    image = ImageGrab.grab(bbox=box)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return CaptureResult(image=image, png_bytes=buffer.getvalue(), box=box)


def save_capture(result: CaptureResult, directory: Path, stem: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{stem}.png"
    result.image.save(path)
    return path
