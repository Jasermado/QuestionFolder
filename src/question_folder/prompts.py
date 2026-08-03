from __future__ import annotations

PROMPTS = {
    "explain": (
        "Read the question in the image carefully and solve it as a study tutor. "
        "Show clear steps, state assumptions, and end with a separate line formatted exactly "
        "as 'Key Result: <result>'. If anything is unreadable, say so instead of guessing."
    ),
    "hint": (
        "Read the question in the image and give a useful first hint without immediately "
        "revealing the complete solution. Identify the concept and suggest the next step. "
        "If anything is unreadable, explain what needs to be recaptured."
    ),
    "concise": (
        "Read the question in the image. Give a compact explanation with only the necessary "
        "working, then end with 'Key Result: <result>'. Do not guess unreadable text."
    ),
}


def get_prompt(mode: str) -> str:
    try:
        return PROMPTS[mode]
    except KeyError as exc:
        raise ValueError(f"Unknown study mode: {mode}") from exc
