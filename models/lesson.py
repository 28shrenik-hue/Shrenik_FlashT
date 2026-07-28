from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    topic: str
    title: str
    description: str
    why_it_matters: str = ""
    scenario: str = ""
    deeper: str = ""
    minutes: int = 5
    xp: int = 25
    question: str = ""
    options: tuple[str, ...] = ()
    answer: int = 0
    explanation: str = ""
    recall_scenario: str = ""
    recall_question: str = ""
    recall_options: tuple[str, ...] = ()
    recall_answer: int = 0
    recall_explanation: str = ""
