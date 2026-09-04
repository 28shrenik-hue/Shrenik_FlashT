from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from services.learning_service import LearningService
from services.logging_service import configure_logging


LOGGER = logging.getLogger(__name__)


def _install_exception_logging() -> None:
    def handle_exception(exc_type, exc_value, exc_traceback) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        LOGGER.critical(
            "Unhandled application exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception


def run() -> int:
    log_file = configure_logging()
    _install_exception_logging()
    LOGGER.info("Starting FlashTile; log=%s", log_file)

    app = QGuiApplication(sys.argv)
    app.setApplicationName("FlashTile")
    app.setOrganizationName("FlashTile Capstone")

    project_root = Path(__file__).resolve().parents[1]
    icon_file = project_root / "assets" / "branding" / "FlashTile_3D_Logo.png"
    if icon_file.exists():
        app.setWindowIcon(QIcon(str(icon_file)))

    engine = QQmlApplicationEngine()
    try:
        learning = LearningService()
    except Exception:
        LOGGER.exception("Unable to initialize the learning service")
        return 2
    engine.rootContext().setContextProperty("learningService", learning)

    qml_file = project_root / "ui" / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        LOGGER.error("QML failed to create a root window: %s", qml_file)
        return 1

    # Reuse a valid saved position on the primary display. Otherwise, place the
    # tile at its original upper-right starting location.
    window = engine.rootObjects()[0]
    screen = app.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry()
        saved_position = learning.store.window_position()
        if saved_position is not None:
            saved_x, saved_y = saved_position
            position_is_visible = (
                saved_x >= available.x()
                and saved_y >= available.y()
                and saved_x + window.width() <= available.x() + available.width()
                and saved_y + window.height() <= available.y() + available.height()
            )
        else:
            position_is_visible = False
        if position_is_visible:
            window.setX(saved_x)
            window.setY(saved_y)
        else:
            window.setX(available.x() + available.width() - window.width() - 24)
            window.setY(available.y() + 40)
        LOGGER.info(
            "Window ready at x=%s y=%s width=%s height=%s",
            window.x(),
            window.y(),
            window.width(),
            window.height(),
        )

    return app.exec()
