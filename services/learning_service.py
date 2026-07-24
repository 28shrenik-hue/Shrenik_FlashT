from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from models.lesson import Lesson
from services.excel_service import ExcelService


LESSONS = {
    "AWS Cloud": Lesson("AWS Cloud", "AWS Global Infrastructure", "Understand Regions, Availability Zones, and resilient cloud design."),
    "Artificial Intelligence": Lesson("Artificial Intelligence", "How Models Learn", "Explore training data, patterns, inference, and responsible use."),
    "Python": Lesson("Python", "Readable Comprehensions", "Transform collections with concise, expressive Python."),
    "Cybersecurity": Lesson("Cybersecurity", "The Principle of Least Privilege", "Reduce risk by granting only the access a task requires."),
    "Leadership": Lesson("Leadership", "Lead With Context", "Help teams make better decisions by sharing purpose and constraints."),
}


class LearningService(QObject):
    changed = Signal()
    celebration = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.store = ExcelService()
        self._topic = self.store.selected_topic()
        if self._topic not in LESSONS:
            self._topic = "AWS Cloud"
        self._xp, self._streak = self.store.totals()

    @Property("QStringList", constant=True)
    def topics(self) -> list[str]:
        return list(LESSONS)

    @Property(str, notify=changed)
    def topic(self) -> str:
        return self._topic

    @Property(str, notify=changed)
    def title(self) -> str:
        return LESSONS[self._topic].title

    @Property(str, notify=changed)
    def description(self) -> str:
        return LESSONS[self._topic].description

    @Property(int, notify=changed)
    def minutes(self) -> int:
        return LESSONS[self._topic].minutes

    @Property(int, notify=changed)
    def xp(self) -> int:
        return self._xp

    @Property(int, notify=changed)
    def streak(self) -> int:
        return self._streak

    @Slot(str)
    def selectTopic(self, topic: str) -> None:
        if topic in LESSONS and topic != self._topic:
            self._topic = topic
            self.store.set_selected_topic(topic)
            self.changed.emit()

    @Slot()
    def completeLesson(self) -> None:
        lesson = LESSONS[self._topic]
        if self.store.complete(lesson.topic, lesson.title, lesson.xp):
            self._xp, self._streak = self.store.totals()
            self.changed.emit()
            self.celebration.emit(f"+{lesson.xp} XP — learning complete!")
        else:
            self.celebration.emit("Today's card is already complete.")

