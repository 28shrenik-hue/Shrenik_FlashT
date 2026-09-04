from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

ROOT = Path(__file__).resolve().parents[1] / "FlashTile-RC15"
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import QMetaObject, QObject, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from services import learning_service
from services.excel_service import ExcelService


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--state",
        choices=("welcome", "goals", "lesson", "scenario", "deeper", "quiz", "team", "progress"),
        default="welcome",
    )
    parser.add_argument("--goal", default="Build resilient cloud skills")
    args = parser.parse_args()

    with TemporaryDirectory() as folder:
        original_store = learning_service.ExcelService
        learning_service.ExcelService = lambda: ExcelService(Path(folder) / "FlashTile.xlsx")
        try:
            app = QGuiApplication([])
            engine = QQmlApplicationEngine()
            service = learning_service.LearningService()
            engine.rootContext().setContextProperty("learningService", service)
            engine.load(QUrl.fromLocalFile(str(ROOT / "ui" / "qml" / "Main.qml")))
            if not engine.rootObjects():
                raise RuntimeError("QML root window was not created")
            window = engine.rootObjects()[0]
            app.processEvents()

            if args.state != "welcome":
                continue_button = window.findChild(QObject, "welcomeContinueButton")
                start_button = window.findChild(QObject, "startLearningButton")
                if continue_button is None or start_button is None:
                    raise RuntimeError("Onboarding controls are missing")
                QMetaObject.invokeMethod(continue_button, "click")
                app.processEvents()
                if args.state == "goals":
                    pass
                else:
                    window.setProperty("onboardingGoal", args.goal)
                    QMetaObject.invokeMethod(start_button, "click")
                    app.processEvents()
                    if args.state in {"scenario", "deeper", "quiz"}:
                        step = {"scenario": 1, "deeper": 2, "quiz": 3}[args.state]
                        window.setProperty("flowStep", step)
                    elif args.state in {"team", "progress"}:
                        popup_name = "teamBoardPopup" if args.state == "team" else "progressPopup"
                        popup = window.findChild(QObject, popup_name)
                        if popup is None:
                            raise RuntimeError(f"Missing popup: {popup_name}")
                        QMetaObject.invokeMethod(popup, "open")
                    app.processEvents()

            saved = {"ok": False}

            def capture() -> None:
                try:
                    screen = window.screen() or app.primaryScreen()
                    if screen is not None:
                        image = screen.grabWindow(int(window.winId()))
                        args.output.parent.mkdir(parents=True, exist_ok=True)
                        saved["ok"] = bool(image.save(str(args.output)))
                finally:
                    app.quit()

            QTimer.singleShot(800, capture)
            app.exec()
            return 0 if saved["ok"] else 1
        finally:
            learning_service.ExcelService = original_store


if __name__ == "__main__":
    raise SystemExit(main())
