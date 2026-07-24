# FlashTile

**Knowledge that finds you.**

FlashTile is a cross-platform desktop micro-learning companion built with Python, PySide6/QML, and a replaceable Excel persistence layer. The foundation ships with AWS Cloud, Artificial Intelligence, Python, Cybersecurity, and Leadership cards plus XP and streak tracking.

## Run on macOS

Control-click `scripts/run_mac.command`, choose **Open**, and allow the first-time dependency installation.

Or run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Run on Windows

Double-click `scripts\run_windows.bat`. Install Python 3.12 first and select **Add Python to PATH** during installation.

## Test

```bash
python -m pytest
```

Progress is stored locally at `~/.flashtile/FlashTile.xlsx`; it is never committed. No confidential or customer data should be entered into the app.

## Repository layout

- `app/` application startup
- `ui/qml/` desktop interface
- `services/` learning and Excel persistence
- `models/` domain models
- `docs/` capstone vision, proposal, and roadmap
- `tests/` automated tests
- `scripts/` macOS and Windows launchers

