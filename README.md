# QuestionFolder 1.1

QuestionFolder is a configurable Windows screenshot-based study assistant for permitted learning, practice, homework review, and accessibility workflows.

It does **not** contain functionality intended to conceal itself from supervisors, evade monitoring, bypass proctoring, or provide unauthorized assessment assistance.

## What changed in 1.1

Windows toast notifications are now optional. Add this to `.env`:

```env
NOTIFICATIONS_ENABLED=false
```

With that setting:

- Windows toast popups and notification sounds are suppressed.
- Status messages still appear in the open console.
- Full answers still print in the console.
- Clipboard behavior still follows `COPY_MODE`.
- The application does not hide its process or bypass monitoring software.

To restore notifications:

```env
NOTIFICATIONS_ENABLED=true
```

Restart QuestionFolder after changing the setting.

## Setup

1. Install Python 3.10 or newer.
2. Open PowerShell in the repository folder.
3. Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup_windows.ps1
```

4. Open `.env` and add your API key:

```env
OPENAI_API_KEY=your_key_here
```

5. Optionally disable toast notifications:

```env
NOTIFICATIONS_ENABLED=false
```

6. Double-click `run.bat`.

## Usage

1. Keep the console open.
2. Press the configured hotkey, default `Ctrl + Shift + Q`.
3. Click the top-left and bottom-right corners of the question.
4. Read the result in the console or clipboard.

## Configuration

| Setting | Default | Values |
|---|---|---|
| `OPENAI_API_KEY` | required | API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Vision-capable model |
| `HOTKEY` | `<ctrl>+<shift>+q` | `pynput` hotkey syntax |
| `STUDY_MODE` | `explain` | `explain`, `hint`, `concise` |
| `COPY_MODE` | `full` | `full`, `result`, `none` |
| `NOTIFICATIONS_ENABLED` | `true` | `true`, `false` |
| `SAVE_CAPTURES` | `true` | `true`, `false` |
| `SAVE_HISTORY` | `true` | `true`, `false` |

## Privacy-focused permitted-use configuration

```env
NOTIFICATIONS_ENABLED=false
SAVE_CAPTURES=false
SAVE_HISTORY=false
COPY_MODE=none
```

This suppresses toast popups and avoids deliberate local storage, but the visible console remains open and the selected image is still sent to the configured API.

## Analyze a saved image

```powershell
question-folder analyze "C:\path\to\question.png"
```

## Development

```powershell
pip install -e ".[dev]"
pytest
ruff check .
```

## Responsible use

Use QuestionFolder only where external assistance is permitted. Do not use it during closed-book tests, proctored exams, interviews, certifications, or competitions that prohibit outside tools.
