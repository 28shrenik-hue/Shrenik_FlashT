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
    assert sum(len(lessons) for lessons in learning_service.LESSONS.values()) == 25
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


def test_learning_goal_sequences_curated_lessons(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.selectLearningGoal("Build resilient cloud skills")

    assert service.goalActive
    assert service.learningGoal == "Build resilient cloud skills"
    assert service.title == "AWS Global Infrastructure"
    assert service.goalProgressText == "Flash 1 of 5"

    service.nextLesson()
    assert service.topic == "AWS & Cloud"
    assert service.title == "The Shared Responsibility Model"
    assert service.goalProgressText == "Flash 2 of 5"

    resumed = make_service(tmp_path, monkeypatch)
    assert resumed.learningGoal == service.learningGoal
    assert resumed.title == service.title


def test_custom_goal_matches_prepared_demo_paths(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)

    result = service.createCustomLearningPath(
        "I want to understand BCBS 239 and data governance"
    )
    assert result == "STARTED|Navigate risk and governance decisions"
    assert service.learningGoal == "Navigate risk and governance decisions"
    assert service.topic == "Risk & Governance"
    assert service.title == "Risk-Informed Decision Making"

    result = service.createCustomLearningPath(
        "What are the benefits of alternative investments in my portfolio?"
    )
    assert result == "STARTED|Understand alternative investments"
    assert service.topic == "Investment Fundamentals"


def test_unknown_custom_goal_is_queued(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)

    result = service.createCustomLearningPath("Advanced supply-chain forecasting")
    assert result.startswith("REQUESTED|")
    assert service.store.topic_requests()[0][1] == "Advanced supply-chain forecasting"


def test_each_prepared_topic_opens_its_exact_lesson(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    expected = {
        "Risk & Decision Making": "Risk-Informed Decision Making",
        "BCBS 239 & Data Governance": "BCBS 239 & Data Governance",
        "Human-in-the-loop AI controls": "Human-in-the-Loop AI Controls",
        "Issues & Errors Management": "Issues & Errors Management",
        "Legal-obligation impact assessments": "Legal-Obligation Impact Assessment",
        "Alternative investments and portfolio diversification": "Understanding Alternative Investments",
    }

    assert service.preparedLearningTopics == list(expected)
    assert service.topLearningItems == [
        "AWS & Cloud",
        "AI / ML",
        "Cybersecurity & Digital Trust",
        *expected,
    ]
    for subject, title in expected.items():
        assert service.openPreparedLearningTopic(subject)
        assert service.title == title
        assert service.currentTopLearningItem == subject

    service.selectTopLearningItem("BCBS 239 & Data Governance")
    assert service.title == "BCBS 239 & Data Governance"


def test_saved_takeaway_browser_opens_and_removes_note(
    tmp_path: Path, monkeypatch
) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.saveLessonNote("Remember the failure boundary.")
    service.nextLesson()

    assert service.noteCount == 1
    assert "Remember the failure boundary" in service.noteItems[0]

    service.openNote(0)
    assert service.title == "AWS Global Infrastructure"
    assert service.lessonNote == "Remember the failure boundary."

    service.removeNote(0)
    assert service.noteCount == 0


def test_reduced_motion_preference_persists(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.setReducedMotion(True)
    assert service.reducedMotion

    resumed = make_service(tmp_path, monkeypatch)
    assert resumed.reducedMotion


def test_first_run_welcome_is_completed_and_persists(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    assert not service.welcomeSeen

    service.completeWelcome()
    assert service.welcomeSeen

    resumed = make_service(tmp_path, monkeypatch)
    assert resumed.welcomeSeen


def test_daily_discovery_is_complete_and_can_advance(
    tmp_path: Path, monkeypatch
) -> None:
    service = make_service(tmp_path, monkeypatch)
    first_title = service.dailyDiscoveryTitle

    assert service.dailyDiscoveryDate
    assert service.dailyDiscoveryCategory in {
        "General Knowledge",
        "History Spotlight",
        "Important Milestone",
    }
    assert service.dailyDiscoveryBody
    assert service.dailyDiscoveryContext
    assert service.dailyDiscoverySource
    assert service.dailyDiscoverySourceUrl.startswith("https://")

    service.nextDiscovery()
    assert service.dailyDiscoveryTitle != first_title


def test_team_board_demo_exposes_complete_sample_metrics(
    tmp_path: Path, monkeypatch
) -> None:
    service = make_service(tmp_path, monkeypatch)

    assert service.teamName == "Cloud Pioneers"
    assert service.teamWeeklyCompleted == 26
    assert service.teamWeeklyGoal == 35
    assert service.teamXp == 1850
    assert service.teamStreak == 6
    assert len(service.teamMemberItems) == 6
    assert any("Patel, Shrenik (You)" in member for member in service.teamMemberItems)
    assert all(len(member.split("|")) == 4 for member in service.teamMemberItems)
    assert service.teamChallenge == "Complete 35 lessons together"
    assert service.teamChallengeReward


def test_search_opens_matching_lesson(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    assert service.searchResultCount == 5
    assert all(item.startswith("AWS & Cloud|") for item in service.searchLessonItems)

    service.searchLessons("zero trust")
    assert service.searchResultCount == 0

    service.selectTopic("Cybersecurity & Digital Trust")
    service.searchLessons("zero trust")
    assert service.searchResultCount == 1
    assert "Cybersecurity & Digital Trust|Zero Trust Foundations" in service.searchLessonItems
    service.openSearchResult(0)
    assert service.topic == "Cybersecurity & Digital Trust"
    assert service.title == "Zero Trust Foundations"


def test_selected_topic_owns_next_lesson_sequence(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.selectLearningGoal("Use AI responsibly")
    service.nextLesson()
    assert service.topic == "AI / ML"

    service.selectTopic("AWS & Cloud")
    assert not service.goalActive
    for _ in range(8):
        assert service.topic == "AWS & Cloud"
        service.nextLesson()


def test_every_learning_goal_maps_to_its_own_category(
    tmp_path: Path, monkeypatch
) -> None:
    expected = {
        "Build resilient cloud skills": ("AWS & Cloud", "AWS Global Infrastructure"),
        "Use AI responsibly": ("AI / ML", "How Models Learn"),
        "Strengthen digital trust": (
            "Cybersecurity & Digital Trust",
            "The Principle of Least Privilege",
        ),
    }
    service = make_service(tmp_path, monkeypatch)
    assert service.learningGoals == list(expected)
    for goal, (topic, first_title) in expected.items():
        service.selectLearningGoal(goal)
        assert service.learningGoal == goal
        assert service.topic == topic
        assert service.title == first_title
        for _ in range(7):
            service.nextLesson()
            assert service.topic == topic


def test_legacy_balanced_goal_migrates_to_selected_category(
    tmp_path: Path, monkeypatch
) -> None:
    store = ExcelService(tmp_path / "FlashTile.xlsx")
    store.set_selected_topic("AI / ML")
    store.set_learning_goal("Balanced digital foundations")
    service = make_service(tmp_path, monkeypatch)

    assert service.learningGoal == "Use AI responsibly"
    assert service.topic == "AI / ML"
    assert service.title == "How Models Learn"


def test_progress_badges_and_tour(tmp_path: Path, monkeypatch) -> None:
    service = make_service(tmp_path, monkeypatch)
    assert service.progressCompleted == 0
    assert service.unlockedBadgeCount == 0
    assert len(service.badgeItems) == 6
    assert len(service.progressTopicItems) == 3

    service.checkAnswer(1)
    service.completeLesson()
    assert service.progressCompleted == 1
    assert service.progressPercent == 7
    assert service.unlockedBadgeCount == 1

    assert service.tourProgressText == "1 of 7"
    first = service.tourTitle
    service.nextTour()
    assert service.tourTitle != first
    service.previousTour()
    assert service.tourTitle == first


def test_demo_reset_preserves_motion_preference_and_creates_backup(
    tmp_path: Path, monkeypatch
) -> None:
    service = make_service(tmp_path, monkeypatch)
    service.completeWelcome()
    service.setReducedMotion(True)
    service.toggleBookmark()
    service.saveLessonNote("Demo note")
    service.checkAnswer(1)
    service.completeLesson()

    backup = Path(service.resetDemoData())
    assert backup.exists()
    assert service.xp == 0
    assert service.progressCompleted == 0
    assert service.bookmarkCount == 0
    assert service.noteCount == 0
    assert service.reducedMotion
    assert service.topic == "AWS & Cloud"
    assert not service.welcomeSeen
