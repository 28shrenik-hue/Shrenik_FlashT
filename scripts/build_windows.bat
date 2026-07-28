@echo off
setlocal
cd /d "%~dp0\.."

where py >nul 2>nul
if errorlevel 1 (
    echo The Python launcher was not found.
    exit /b 1
)

if not exist ".build-venv\Scripts\python.exe" (
    py -3.12 -m venv .build-venv
    if errorlevel 1 py -3 -m venv .build-venv
    if errorlevel 1 exit /b 1
)

.build-venv\Scripts\python.exe -m pip install --disable-pip-version-check --no-compile -r requirements-dev.txt
if errorlevel 1 exit /b 1

set "QT_QPA_PLATFORM=offscreen"
set "QT_QUICK_BACKEND=software"
.build-venv\Scripts\python.exe self_check.py
if errorlevel 1 exit /b 1
.build-venv\Scripts\python.exe -m pytest -q
if errorlevel 1 exit /b 1

.build-venv\Scripts\pyinstaller.exe --noconfirm --clean FlashTile.spec
if errorlevel 1 exit /b 1

copy /y README.md dist\FlashTile\README.md >nul
copy /y CHANGELOG.md dist\FlashTile\CHANGELOG.md >nul
if not exist release mkdir release
powershell -NoProfile -Command "$target='release\FlashTile-v1.0.0-rc12-win64.zip'; if (Test-Path $target) { Remove-Item $target }; Compress-Archive -Path 'dist\FlashTile\*' -DestinationPath $target"
if errorlevel 1 exit /b 1

echo.
echo Windows package created:
echo release\FlashTile-v1.0.0-rc12-win64.zip
