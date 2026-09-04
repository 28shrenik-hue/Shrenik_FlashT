from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import QMetaObject, QObject, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from services import learning_service
from services.excel_service import ExcelService


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a FlashTile preview")
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--popup",
        choices=(
            "goalPopup",
            "preparedTopicsPopup",
            "bookmarksPopup",
            "teamBoardPopup",
            "discoveryPopup",
            "notesPopup",
            "takeawaysPopup",
            "progressPopup",
            "achievementsPopup",
            "searchPopup",
            "tourPopup",
            "demoResetPopup",
        ),
    )
    parser.add_argument(
        "--welcome-goals",
        action="store_true",
        help="Render the second onboarding step for Learning Goals",
    )
    args = parser.parse_args()

    with TemporaryDirectory() as folder:
        original_store = learning_service.ExcelService
        learning_service.ExcelService = lambda: ExcelService(
            Path(folder) / "FlashTile.xlsx"
        )
        try:
            app = QGuiApplication([])
            engine = QQmlApplicationEngine()
            learning = learning_service.LearningService()
            engine.rootContext().setContextProperty("learningService", learning)
            engine.load(QUrl.fromLocalFile(str(ROOT / "ui" / "qml" / "Main.qml")))
            if not engine.rootObjects():
                raise RuntimeError("QML did not create a window")
            window = engine.rootObjects()[0]
            if args.welcome_goals:
                continue_button = window.findChild(QObject, "welcomeContinueButton")
                if continue_button is None:
                    raise RuntimeError("Welcome Continue button not found")
                QMetaObject.invokeMethod(continue_button, "click")
                app.processEvents()
            if args.popup:
                popup = window.findChild(QObject, args.popup)
                if popup is None:
                    raise RuntimeError(f"Popup not found: {args.popup}")
                QMetaObject.invokeMethod(popup, "open")

            result = {"saved": False}

            def capture() -> None:
                try:
                    screen = window.screen() or app.primaryScreen()
                    if screen is None:
                        return
                    image = screen.grabWindow(int(window.winId()))
                    args.output.parent.mkdir(parents=True, exist_ok=True)
                    result["saved"] = bool(image.save(str(args.output)))
                finally:
                    app.quit()

            QTimer.singleShot(700, capture)
            app.exec()
            return 0 if result["saved"] else 1
        finally:
            learning_service.ExcelService = original_store


if __name__ == "__main__":
    raise SystemExit(main())
