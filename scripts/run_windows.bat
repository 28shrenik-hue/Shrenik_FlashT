@echo off
setlocal
cd /d "%~dp0\.."

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python 3 was not found. Install Python 3.9 or newer and try again.
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)"
if errorlevel 1 (
    echo FlashTile requires Python 3.9 or newer.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :failed
)

.venv\Scripts\python.exe -c "import PySide6, openpyxl" >nul 2>nul
if errorlevel 1 (
    .venv\Scripts\python.exe -m pip install --disable-pip-version-check --no-compile -r requirements.txt
    if errorlevel 1 goto :failed
)

.venv\Scripts\python.exe self_check.py --quick
if errorlevel 1 goto :failed

.venv\Scripts\python.exe main.py
if errorlevel 1 goto :failed
exit /b 0

:failed
echo.
echo FlashTile could not start. Review the message above.
pause
exit /b 1
