from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(data_root: Path | None = None) -> Path:
    root = data_root or Path.home() / ".flashtile"
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "FlashTile.log"

    root_logger = logging.getLogger()
    has_flash_file = any(
        isinstance(handler, RotatingFileHandler)
        and Path(handler.baseFilename) == log_file
        for handler in root_logger.handlers
    )
    if not has_flash_file:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )
        root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    return log_file
