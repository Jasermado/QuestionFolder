from __future__ import annotations


def notify(title: str, message: str, enabled: bool = True) -> None:
    """Show a Windows toast when enabled; otherwise log visibly to the console."""
    if not enabled:
        print(f"[{title}] {message}")
        return

    try:
        from winotify import Notification, audio

        toast = Notification(
            app_id="QuestionFolder Study Assistant",
            title=title,
            msg=message,
            duration="short",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception:
        print(f"[{title}] {message}")
