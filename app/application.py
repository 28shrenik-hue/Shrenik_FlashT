from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from services.learning_service import LearningService


def run() -> int:
    app = QGuiApplication(sys.argv)
    app.setApplicationName("FlashTile")
    app.setOrganizationName("FlashTile Capstone")

    engine = QQmlApplicationEngine()
    learning = LearningService()
    engine.rootContext().setContextProperty("learningService", learning)

    qml_file = Path(__file__).resolve().parents[1] / "ui" / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        return 1
    return app.exec()

