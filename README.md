# FlashTile — Tile-First Learning Engine

**Knowledge that finds you.**

FlashTile is a small, always-on-top desktop micro-learning tile built with Python,
PySide6/QML, and a replaceable Excel persistence layer. It intentionally does not
expand into a conventional full-screen application.

## v1.0 release-candidate experience

- One compact fixed 410 × 690 floating tile
- Draggable from the FlashTile title/header, with the last valid screen position remembered
- Every-launch Welcome Tile with product context, Learning Goal selection, and a direct Begin Learning action
- Welcome → Learning Goal → Learning sequence on every fresh application launch
- Original 3D liquid-glass FlashTile logo integrated into the compact header
- Premium glass styling and mouse-position swivel
- Fifteen flagship lessons across AWS & Cloud, AI / ML, and Cybersecurity & Digital Trust
- Three category-aligned learning-goal paths that sequence relevant curated lessons locally
- An editable Prepared Learning Topics selector with six visible team-requested subjects
- Exact lesson routing for Risk & Decision Making, BCBS 239 & Data Governance, human-in-the-loop AI controls, Issues & Errors Management, legal-obligation impact assessments, and alternative investments
- Prediction-free custom-goal typing plus a separate browser for the six prepared examples
- Nine choices in the in-learning dropdown: the three flagship areas plus all six exact prepared subjects
- A local request queue when a described topic is not yet available
- Date-rotating Daily Discovery cards for general knowledge, history, and major milestones
- Team Board capability preview with local illustrative progress and contributor data
- Weekly team challenge with a shared target and team-badge reward
- Personal Progress with topic completion, mastery, due reviews, and six achievement badges
- Category-scoped search across the selected topic's lesson titles and descriptions
- Seven-step Guided Tour and safely backed-up progress reset
- Visible authoritative source links on every Daily Discovery card
- Continuous curated lessons with no daily stopping point
- Structured Core Concept → Practical Scenario → Go Deeper → Knowledge Check → Completion lessons
- XP and streak persistence in a local Excel workbook
- Per-lesson bookmarks, 500-character Quick Notes, and a saved-takeaways browser
- Saved Review list, confidence check, spaced recall scheduling, and concept mastery
- Optional in-tile 60-second breathing reset with no wellness data collection
- Persistent reduced-motion mode and keyboard shortcuts for core learning tools
- Named hover labels for Learning Goals, Saved Lessons, Meditation, Daily Discovery, and Quick Notes
- Team features remain local and are not yet connected to shared cloud sync
- Primary-screen-safe startup positioning on multi-monitor Macs and PCs
- Restrained perspective slide, depth scale, light sweep, and background parallax between flashes
- No dashboard, sidebar, social feed, or full-screen navigation

## Responsible-use notice

FlashTile provides educational content and is not legal, investment, compliance, or other professional advice. Users should not enter confidential, customer, personal, or restricted information. AI-assisted or prepared learning content must be reviewed against applicable firm policy and qualified guidance before it is used for consequential decisions. A disclaimer supports transparency; it does not replace governance, access controls, content review, or legal approval for production use.

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
python self_check.py
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Progress is stored locally at `~/.flashtile/FlashTile.xlsx`; it is never committed.
Daily workbook backups are stored in `~/.flashtile/backups/`, and rotating logs
are written to `~/.flashtile/logs/FlashTile.log`.
No confidential or customer data should be entered into the app.

## Build the portable Windows package

On Windows, run:

```text
scripts\build_windows.bat
```

The no-Python-required package is created at:

```text
release\FlashTile-v1.0.0-rc16-win64.zip
```

The same build can run from the **Windows release package** GitHub Actions
workflow.

## Repository layout

- `app/` application startup
- `ui/qml/` desktop interface
- `services/` learning and Excel persistence
- `models/` domain models
- `docs/` capstone vision, proposal, and roadmap
- `tests/` automated tests
- `scripts/` macOS and Windows launchers
- `self_check.py` release diagnostics
- `FlashTile.spec` portable Windows packaging
