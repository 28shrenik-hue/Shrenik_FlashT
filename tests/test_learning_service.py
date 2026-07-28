from datetime import date
from pathlib import Path

from services import learning_service
from services.excel_service import ExcelService
from services.learning_service import LearningService


def make_service(tmp_path: Path, monkeypatch) -> LearningService:
    monkeypatch.setattr(
        learning_service,
        "ExcelService",
        lambda: ExcelService(tmp_path / "FlashTile.xlsx"),
    )
    return LearningService()


def test_completion_requires_correct_answer(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.completeLesson()
    assert service.xp == 0

    service.checkAnswer(1)
    assert service.quizPassed
    service.completeLesson()
    assert service.xp == 25


def test_topic_change_resets_quiz(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.checkAnswer(1)
    assert service.quizPassed
    service.selectTopic("AI / ML")
    assert not service.quizPassed


def test_next_lesson_advances_and_persists(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    first_title = service.title
    service.nextLesson()
    assert service.title != first_title

    resumed = make_service(tmp_path, monkeypatch)
    assert resumed.title == service.title


def test_flagship_lessons_have_complete_learning_stages() -> None:
    for lessons in learning_service.LESSONS.values():
        for lesson in lessons:
            assert lesson.description
            assert lesson.why_it_matters
            assert lesson.scenario
            assert lesson.deeper
            assert lesson.question
            assert len(lesson.options) == 3
            assert lesson.recall_scenario
            assert lesson.recall_question
            assert len(lesson.recall_options) == 3


def test_bookmark_and_note_persist_per_lesson(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    first_title = service.title
    assert not service.bookmarked
    assert service.lessonNote == ""

    service.toggleBookmark()
    service.saveLessonNote("A Region contains isolated Availability Zones.")

    resumed = make_service(tmp_path, monkeypatch)
    assert resumed.title == first_title
    assert resumed.bookmarked
    assert resumed.lessonNote == "A Region contains isolated Availability Zones."

    resumed.nextLesson()
    assert resumed.title != first_title
    assert not resumed.bookmarked
    assert resumed.lessonNote == ""


def test_confidence_schedules_review(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.checkAnswer(1)
    service.completeLesson()
    service.setConfidence("got_it")

    assert service.masteryLabel == "Practicing"
    assert "Next review:" in service.nextReviewText


def test_due_review_uses_alternate_recall_and_updates_mastery(
    tmp_path: Path, monkeypatch
) -> None:
    store = ExcelService(tmp_path / "FlashTile.xlsx")
    lesson = learning_service.LESSONS["AWS & Cloud"][0]
    store._save_review_state(
        lesson.topic,
        lesson.title,
        1,
        date.today().isoformat(),
        1,
        "need_practice",
        "lesson_complete",
    )

    service = make_service(tmp_path, monkeypatch)
    assert service.reviewMode
    assert service.scenario == lesson.recall_scenario
    assert service.question == lesson.recall_question

    service.checkAnswer(lesson.recall_answer)
    assert service.quizPassed
    assert service.completeLesson()
    assert service.xp == 10
    assert service.masteryLabel == "Practicing"
