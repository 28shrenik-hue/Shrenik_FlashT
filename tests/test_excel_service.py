from pathlib import Path

from services.excel_service import ExcelService


def test_completion_is_idempotent(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    assert store.complete("AWS Cloud", "Regions", 25)
    assert not store.complete("AWS Cloud", "Regions", 25)
    assert store.totals()[0] == 25


def test_topic_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.set_selected_topic("AI / ML")
    assert store.selected_topic() == "AI / ML"


def test_lesson_position_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.set_lesson_index("AWS & Cloud", 2)
    assert store.lesson_index("AWS & Cloud") == 2


def test_bookmark_and_note_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    topic = "AWS & Cloud"
    lesson = "AWS Global Infrastructure"

    assert not store.is_bookmarked(topic, lesson)
    store.set_bookmarked(topic, lesson, True)
    assert store.is_bookmarked(topic, lesson)
    store.set_bookmarked(topic, lesson, False)
    assert not store.is_bookmarked(topic, lesson)

    store.save_lesson_note(topic, lesson, "Use multiple Availability Zones.")
    assert store.lesson_note(topic, lesson) == "Use multiple Availability Zones."
    assert store.notes() == [
        (topic, lesson, "Use multiple Availability Zones.")
    ]
    store.save_lesson_note(topic, lesson, "")
    assert store.lesson_note(topic, lesson) == ""
    assert store.notes() == []


def test_learning_preferences_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.set_learning_goal("Use AI responsibly")
    store.set_learning_goal_position(3)
    store.set_reduced_motion(True)
    store.set_welcome_seen(True)

    resumed = ExcelService(tmp_path / "test.xlsx")
    assert resumed.learning_goal() == "Use AI responsibly"
    assert resumed.learning_goal_position() == 3
    assert resumed.reduced_motion()
    assert resumed.welcome_seen()


def test_topic_request_is_saved_once(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "FlashTile.xlsx")
    assert store.submit_topic_request("Quantum-safe vendor governance")
    assert not store.submit_topic_request("  quantum-safe vendor governance  ")
    assert store.topic_requests() == [
        (
            store.topic_requests()[0][0],
            "Quantum-safe vendor governance",
            "Requested",
        )
    ]


def test_window_position_round_trip(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "FlashTile.xlsx")
    assert store.window_position() is None
    store.set_window_position(42, 84)
    assert ExcelService(tmp_path / "FlashTile.xlsx").window_position() == (42, 84)


def test_confidence_and_review_result_update_mastery(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    topic = "AWS & Cloud"
    lesson = "AWS Global Infrastructure"

    store.set_confidence(topic, lesson, "need_practice")
    state = store.review_state(topic, lesson)
    assert state["mastery_level"] == 1
    assert state["interval_days"] == 1

    store.record_review_result(topic, lesson, True)
    state = store.review_state(topic, lesson)
    assert state["mastery_level"] == 2
    assert state["interval_days"] == 7


def test_write_creates_daily_backup(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.set_selected_topic("AI / ML")

    backups = list((tmp_path / "backups").glob("test-*.xlsx"))
    assert len(backups) == 1


def test_corrupt_workbook_is_preserved_and_rebuilt(tmp_path: Path) -> None:
    workbook = tmp_path / "test.xlsx"
    workbook.write_bytes(b"not a workbook")

    store = ExcelService(workbook)

    assert store.selected_topic() == "AWS & Cloud"
    assert workbook.exists()
    assert len(list(tmp_path.glob("test.corrupt-*.xlsx"))) == 1


def test_progress_summary_and_safe_demo_reset(tmp_path: Path) -> None:
    store = ExcelService(tmp_path / "test.xlsx")
    store.complete("AWS & Cloud", "Regions", 25)
    store.complete("AWS & Cloud", "Regions • Recall", 10)
    store.set_bookmarked("AWS & Cloud", "Regions", True)
    store.save_lesson_note("AWS & Cloud", "Regions", "Remember isolation.")

    summary = store.progress_summary(15)
    assert summary["completed"] == 1
    assert summary["bookmarks"] == 1
    assert summary["notes"] == 1
    assert summary["topic_counts"] == {"AWS & Cloud": 1}

    backup = store.reset_demo_data()
    assert backup.exists()
    assert "demo-reset" in backup.name
    assert store.progress_summary(15)["completed"] == 0
    assert store.bookmarks() == []
    assert store.notes() == []
