#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
trap 'echo; echo "FlashTile could not start. Review the message above."; read -r -p "Press Return to close…"' ERR
export PYTHONIOENCODING="utf-8"
export PYTHONDONTWRITEBYTECODE="1"
export QT_QUICK_CONTROLS_STYLE="Basic"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found. Install Python 3.9 or newer and try again."
    exit 1
fi
if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)'; then
    echo "FlashTile requires Python 3.9 or newer."
    exit 1
fi
if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi
if ! .venv/bin/python -c "import PySide6, openpyxl" >/dev/null 2>&1; then
    .venv/bin/python -m pip install --disable-pip-version-check --no-compile -r requirements.txt
fi
.venv/bin/python self_check.py --quick
exec .venv/bin/python main.py
