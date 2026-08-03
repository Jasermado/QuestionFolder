@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found.
  echo Run scripts\setup_windows.ps1 first.
  pause
  exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m question_folder run
pause
