# Changelog

## 1.0.0-rc13.3 — Judge Demo Roster

- Replaced placeholder contributors with the six project-team names supplied for the judge demo.
- Marked Patel, Shrenik as the current user.
- Rebalanced team XP, completed lessons, and the weekly goal for the six-member roster.
- Expanded the Team Board so all six contributors remain visible without clipping.

## 1.0.0-rc13.2 — Team Board Demo

- Added a judge-ready Team Board capability preview in the tile header.
- Added clearly labeled sample team data for weekly XP, streak, lesson progress, and contributors.
- Added a weekly-goal progress bar and four representative team learning paths.
- Kept private notes, quiz answers, and confidence ratings out of the team view.
- Added a `Ctrl+T` shortcut and a clear Demo Mode label to avoid implying live synchronization.
- Reduced unused vertical space in Daily Discovery while preserving room for longer cards.
- Expanded automated regression coverage to 21 tests.

## 1.0.0-rc13.1 — Daily Discovery

- Added Daily Discovery as the fifth bottom control.
- Added twelve curated offline cards spanning general knowledge, history, and important milestones.
- Made the featured discovery rotate automatically by date, with a Show Another action.
- Ordered the footer as Learning Goals, Saved Lessons, Meditation, Daily Discovery, and Quick Notes.
- Added exact hover labels for all five footer controls and a `Ctrl+D` shortcut for Daily Discovery.
- Expanded automated regression coverage to 20 tests.

## 1.0.0-rc13 — Guided Learning Paths

- Expanded the curated library from nine to fifteen complete lessons.
- Added four local learning-goal paths that sequence relevant curated lessons.
- Added a saved-takeaways browser with open, edit, and remove actions.
- Added a persistent reduced-motion preference for decorative animation.
- Added keyboard shortcuts for goals (`Ctrl+G`), bookmarks (`Ctrl+B`), and notes (`Ctrl+N`).
- Expanded workbook and learning-service regression coverage to 19 tests.
- Preserved the approved single 430 × 730 tile and offline Excel persistence.

## 1.0.0-rc12 — Release Stabilization

- Added rotating local application logs and uncaught-error recording.
- Added daily workbook backups, atomic saves, and corrupt-workbook preservation.
- Added a repeatable self-check for dependencies, assets, data services, QML, and geometry.
- Prevented Windows from reinstalling dependencies on every launch.
- Added clearer macOS and Windows launcher failures.
- Added a PyInstaller portable Windows build and GitHub Actions artifact workflow.
- Expanded automated regression coverage to 14 tests.
- Preserved the approved RC11 design and all learning functionality.

## 1.0.0-rc11 — Branded Header

- Restored the original 3D liquid-glass FlashTile logo asset.
- Added the icon portion of the exact logo to the compact tile header.
- Retained the FlashTile wordmark and “Knowledge that finds you” tagline.
- Preserved the 430 × 730 geometry, learning flow, footer tools, and visual effects.

## 1.0.0-rc10 — Smart Recall & Mastery

- Turned the Bookmark control into an in-tile Saved Review library.
- Added a post-lesson confidence check: Got it, Need practice, or Review later.
- Added Excel-backed review scheduling and four mastery states.
- Prioritized due review flashes before new lessons.
- Added a distinct recall scenario and question for every flagship lesson.
- Awarded 10 XP for completed recall checks.
- Preserved the exact 430 × 730 tile and approved glass, swivel, and transition effects.

## 1.0.0-rc9 — Learning Tools Footer

- Added a working per-lesson Bookmark control on the left.
- Kept the larger guided-breathing control in the center.
- Added a working Quick Notes control on the right.
- Persisted bookmarks and 500-character learning takeaways in new Excel sheets.
- Added non-destructive workbook migration for existing FlashTile users.
- Preserved the exact 430 × 730 tile and all approved visual effects.

## 1.0.0-rc8 — Refined Learning Language

- Renamed the first learning stage from “Plain English” to “Core Concept.”
- Updated supporting guidance and documentation with respectful, professional language.
- Centered and enlarged the guided-breathing control without changing the 430 × 730 tile.
- Preserved the approved glass, swivel, parallax, and learning-stage transitions.

## 1.0.0-rc7 — Structured Learning Engine

- Replaced quick fact-and-quiz cards with a five-stage learning loop.
- Added Core Concept, Practical Scenario, Go Deeper, Knowledge Check, and Completion stages.
- Added nine complete flagship lessons across AWS & Cloud, AI / ML, and Cybersecurity & Digital Trust.
- Added clear “why it matters” explanations and scenario-based knowledge transfer.
- Reused the frozen tile design and premium depth transitions between learning stages.

## 1.0.0-rc6 — Clean Footer

- Removed the “Tile-only • Offline • Excel-backed” implementation copy.
- Kept the breathing reset icon aligned at the bottom-right.
- Preserved all dimensions, motion, and functionality.

## 1.0.0-rc5 — Breathing Reset Icon

- Replaced the “60s Reset” footer text with a compact breathing-wave mark.
- Added hover feedback, a tooltip, and an accessible action name.
- Preserved the exact tile size, layout, and reset behavior.

## 1.0.0-rc4 — Visibility + Premium Motion

- Fixed invisible launches by positioning the tile on the primary display.
- Preserved the exact 430 × 730 window and frozen visual layout.
- Added a restrained 600 ms depth transition between flashes.
- Added perspective rotation, depth scaling, fade, and a soft light sweep.
- Added subtle background particles that respond to the existing card swivel.

## 1.0.0-rc3 — Continuous Learning + 60s Reset

- Kept the tile at exactly 430 × 730 with the frozen glass and swivel design.
- Added three curated flashes per topic and a continuous Next flash action.
- Remembered the current flash separately for every topic.
- Added a small bottom-panel 60s Reset action.
- Added an in-tile inhale (4), hold (2), exhale (6) breathing guide.
- The reset stores no wellness or personal data.

## 1.0.0-rc2 — In-Tile Flow Fix

- Kept the v1.0 RC1 dimensions, glass treatment, colors, and swivel unchanged.
- Added reliable forward and back movement inside the tile.
- Added lesson, knowledge-check, and completion states without opening a full app.
- Made lesson completion return an explicit success result to the interface.
- Added a visible saved-progress confirmation state.

## 1.0.0-rc1 — Minimal Reset

- Reset FlashTile to a single 430 × 730 always-on-top desktop tile.
- Restored the original spring-based two-axis swivel and cursor-following glow.
- Restored frameless glass styling, hover scale, pulse, and completion animation.
- Added an in-tile three-choice knowledge check.
- Gated completion and XP behind a correct answer.
- Preserved topic selection, XP, streaks, duplicate protection, and Excel persistence.
- Removed full-screen navigation, dashboards, sidebars, and nested application pages.
