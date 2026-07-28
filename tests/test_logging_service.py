import logging

from services.logging_service import configure_logging


def test_configure_logging_writes_local_file(tmp_path) -> None:
    log_file = configure_logging(tmp_path)
    logging.getLogger("flashtile-test").info("release check")

    assert log_file.exists()
    assert "release check" in log_file.read_text(encoding="utf-8")
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, "baseFilename", None) == str(log_file):
            root.removeHandler(handler)
            handler.close()
