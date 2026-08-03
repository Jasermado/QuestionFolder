from __future__ import annotations

import re

_RESULT_PATTERN = re.compile(r"^(?:key\s*result|final\s*answer|answer)\b[:\- ]*(.*)$", re.I)


def extract_key_result(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        match = _RESULT_PATTERN.match(line)
        if match and match.group(1).strip():
            return match.group(1).strip()
    return lines[-1] if lines else "N/A"
