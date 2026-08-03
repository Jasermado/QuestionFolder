$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' was not found. Install Python 3.10 or newer first."
}

py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Created .env. Add OPENAI_API_KEY before running the app."
}

Write-Host "Setup complete. Run .\run.bat after configuring .env."
