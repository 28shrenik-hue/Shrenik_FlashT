from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    topic: str
    title: str
    description: str
    minutes: int = 5
    xp: int = 25

