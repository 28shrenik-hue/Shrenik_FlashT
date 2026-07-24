from pathlib import Path

from services.excel_service import ExcelService


def test_completion_is_idempotent(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    assert store.complete("AWS Cloud", "Regions", 25)
    assert not store.complete("AWS Cloud", "Regions", 25)
    assert store.totals()[0] == 25


def test_topic_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.set_selected_topic("Python")
    assert store.selected_topic() == "Python"

