from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from models.lesson import Lesson
from services.excel_service import ExcelService


LESSONS = {
    "AWS & Cloud": (
        Lesson(
            "AWS & Cloud",
            "AWS Global Infrastructure",
            "A Region is a geographic area. Each Region contains separate Availability Zones, so an application can survive a failure in one location.",
            why_it_matters="Customers expect important services to remain available even when infrastructure fails.",
            scenario="A customer-facing application runs in one Availability Zone. That facility loses power. How would using a second Availability Zone change the outcome?",
            deeper="• Regions provide geographic separation.\n• Availability Zones isolate failures inside a Region.\n• Multi-AZ designs trade added cost for resilience.",
            question="A critical application must survive one facility failure. What is the best starting design?",
            options=("One large server", "Two Availability Zones", "One storage bucket"),
            answer=1,
            explanation="Using two Availability Zones reduces dependence on a single facility.",
            recall_scenario="A web service runs across two Availability Zones, but all requests still go to one unhealthy instance.",
            recall_question="What additional capability is most important?",
            recall_options=("A health-aware load balancer", "A larger logo", "One permanent server"),
            recall_answer=0,
            recall_explanation="A health-aware load balancer can redirect requests away from unhealthy capacity.",
        ),
        Lesson(
            "AWS & Cloud",
            "The Shared Responsibility Model",
            "AWS protects the cloud infrastructure. Customers protect what they place in the cloud, including data, identities, permissions, and configurations.",
            why_it_matters="Security gaps often happen when each side assumes the other is responsible.",
            scenario="A team stores sensitive documents in Amazon S3 but accidentally allows public access. AWS kept the infrastructure operating—who owned the access configuration?",
            deeper="• AWS secures physical facilities and managed infrastructure.\n• Customers secure identities, data, and configurations.\n• Responsibility changes by service type.",
            question="Who manages customer data and access permissions in AWS?",
            options=("AWS only", "The customer", "The internet provider"),
            answer=1,
            explanation="Customers remain responsible for their data, identities, and access configuration.",
            recall_scenario="A developer accidentally publishes an access key in a public repository.",
            recall_question="Who must revoke and replace that customer credential?",
            recall_options=("AWS facilities staff", "The customer team", "The internet provider"),
            recall_answer=1,
            recall_explanation="Customer identities and credentials remain the customer’s responsibility.",
        ),
        Lesson(
            "AWS & Cloud",
            "Amazon S3 Foundations",
            "Amazon S3 stores files and other data as objects inside named containers called buckets. It is designed for high durability and broad scalability.",
            why_it_matters="Choosing the right storage service affects cost, reliability, access, and application design.",
            scenario="A team must retain millions of reports and retrieve them by name. The files do not need to behave like a server disk. Which storage pattern fits?",
            deeper="• Objects combine data with metadata and a key.\n• Buckets organize objects and enforce access policies.\n• Lifecycle rules can move older objects to cheaper storage.",
            question="What does Amazon S3 primarily store?",
            options=("Objects", "Virtual machines", "User passwords"),
            answer=0,
            explanation="Amazon S3 stores data as objects inside buckets.",
            recall_scenario="Audit reports must be kept for seven years, but older reports are rarely opened.",
            recall_question="What can reduce storage cost without deleting the reports?",
            recall_options=("An S3 lifecycle rule", "A larger EC2 instance", "More IAM users"),
            recall_answer=0,
            recall_explanation="Lifecycle rules can transition older objects to lower-cost storage classes.",
        ),
    ),
    "AI / ML": (
        Lesson(
            "AI / ML",
            "How Models Learn",
            "A model learns patterns from examples during training. Inference happens later, when the trained model uses those patterns to produce a prediction or response.",
            why_it_matters="Understanding training and inference helps people judge what an AI system can—and cannot—reliably do.",
            scenario="A model studies past support requests, then categorizes a new request as billing or technical. Which part is training, and which part is inference?",
            deeper="• Training adjusts a model using example data.\n• Validation checks performance on unseen examples.\n• Inference applies the trained model to new input.",
            question="What is inference?",
            options=("Training a model", "Using a model to make a prediction", "Deleting training data"),
            answer=1,
            explanation="Inference uses a trained model to produce a prediction or response.",
            recall_scenario="A trained model receives a new support request and labels it as a billing issue.",
            recall_question="Which activity is occurring now?",
            recall_options=("Inference", "Training", "Data deletion"),
            recall_answer=0,
            recall_explanation="Applying a trained model to new input is inference.",
        ),
        Lesson(
            "AI / ML",
            "Training Data Quality",
            "AI systems learn from the examples they receive. Missing, inaccurate, or unrepresentative examples can produce unreliable or unfair results.",
            why_it_matters="A sophisticated model cannot compensate for data that does not represent the problem it must solve.",
            scenario="A recommendation model was trained only on employees from one department but will be used across the organization. What should the team investigate first?",
            deeper="• Representation matters as much as data volume.\n• Historical outcomes may contain historical bias.\n• Data quality must be monitored after deployment.",
            question="What can biased training data produce?",
            options=("Guaranteed accuracy", "Biased model outputs", "Smaller file sizes"),
            answer=1,
            explanation="Models can reproduce or amplify patterns and bias present in their training data.",
            recall_scenario="A model performed well during testing but becomes less accurate after a new customer segment begins using it.",
            recall_question="What should the team investigate first?",
            recall_options=("Data drift", "Screen brightness", "File compression"),
            recall_answer=0,
            recall_explanation="A changed input population can create data drift and reduce model reliability.",
        ),
        Lesson(
            "AI / ML",
            "Human Oversight",
            "AI can support a decision, but accountable people must define boundaries, review important outcomes, and know when to override or escalate.",
            why_it_matters="Automation without ownership can turn a model error into a business, customer, or compliance failure.",
            scenario="An AI system flags an unusual transaction. Should it permanently restrict the customer automatically, or route the case for appropriate review?",
            deeper="• Risk determines the required level of oversight.\n• Escalation paths must exist before deployment.\n• Monitoring should detect drift and unexpected outcomes.",
            question="Why is human review important for consequential AI decisions?",
            options=("It removes all risk", "It adds accountable judgment", "It makes models train faster"),
            answer=1,
            explanation="Human oversight adds context, judgment, and accountability to AI-assisted decisions.",
            recall_scenario="An AI system is uncertain about a decision that could materially affect a customer.",
            recall_question="What is the safest next step?",
            recall_options=("Escalate for authorized review", "Hide the uncertainty", "Always accept the output"),
            recall_answer=0,
            recall_explanation="Consequential, uncertain outcomes should follow a defined human-review path.",
        ),
    ),
    "Cybersecurity & Digital Trust": (
        Lesson(
            "Cybersecurity & Digital Trust",
            "The Principle of Least Privilege",
            "Give each person or system only the access required for its current task—and remove that access when it is no longer needed.",
            why_it_matters="Every unnecessary permission increases the impact of a mistake, compromised account, or malicious action.",
            scenario="A temporary analyst needs to read one report folder for two weeks. Should the analyst receive permanent administrator access or limited time-bound access?",
            deeper="• Access should be specific, temporary, and reviewable.\n• Roles are easier to govern than one-off permissions.\n• Privileged access deserves stronger verification.",
            question="What does least privilege mean?",
            options=("Give everyone admin access", "Grant only required access", "Never grant access"),
            answer=1,
            explanation="Least privilege limits access to only what a person or system needs.",
            recall_scenario="A service account finished a migration but still has administrator permissions.",
            recall_question="What should happen next?",
            recall_options=("Keep access forever", "Replace it with task-specific access", "Share the account"),
            recall_answer=1,
            recall_explanation="Permissions should be reduced when the privileged task is complete.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "AI-Enabled Fraud",
            "Generative AI can imitate writing, images, and voices. A familiar-looking message is therefore not proof that the sender is genuine.",
            why_it_matters="Cyber-enabled fraud is increasingly designed to exploit trust and urgency rather than break technical controls.",
            scenario="You receive an urgent voice message that sounds like a senior leader and requests an unusual financial action. What should you do before acting?",
            deeper="• Deepfakes can imitate trusted people.\n• Urgency discourages independent verification.\n• Verify through a separate approved channel.",
            question="What is the safest response to an unusual urgent request from a familiar voice?",
            options=("Act immediately", "Verify independently", "Forward it widely"),
            answer=1,
            explanation="Independent verification breaks the attacker’s control of the communication channel.",
            recall_scenario="A convincing video call asks you to bypass an established approval step for an urgent transfer.",
            recall_question="What is the strongest response?",
            recall_options=("Use an independent approved channel", "Trust the video", "Disable all messaging"),
            recall_answer=0,
            recall_explanation="Independent verification helps detect impersonation even when media appears authentic.",
        ),
        Lesson(
            "Cybersecurity & Digital Trust",
            "Post-Quantum Readiness",
            "Future quantum computers may weaken widely used public-key cryptography. Organizations must identify affected systems and prepare a careful migration.",
            why_it_matters="Sensitive information captured today may still require protection years from now.",
            scenario="A system stores information that must remain confidential for decades. Why should its team inventory cryptographic dependencies now?",
            deeper="• Migration can take years across complex estates.\n• Crypto-agility makes algorithms replaceable.\n• NIST has standardized initial post-quantum algorithms.",
            question="What is a practical first step toward post-quantum readiness?",
            options=("Inventory cryptography", "Delete all encryption", "Wait for a breach"),
            answer=0,
            explanation="An inventory identifies where vulnerable algorithms exist and what must be migrated.",
            recall_scenario="A large application depends on cryptography embedded across many vendors and services.",
            recall_question="Which capability will make future algorithm replacement easier?",
            recall_options=("Crypto-agility", "Permanent hard-coding", "Removing all encryption"),
            recall_answer=0,
            recall_explanation="Crypto-agility allows algorithms and keys to be replaced without redesigning the entire system.",
        ),
    ),
}

TOPIC_ALIASES = {
    "AWS Cloud": "AWS & Cloud",
    "Artificial Intelligence": "AI / ML",
    "Cybersecurity": "Cybersecurity & Digital Trust",
}


class LearningService(QObject):
    changed = Signal()
    celebration = Signal(str)
    quizResult = Signal(str, bool)

    def __init__(self) -> None:
        super().__init__()
        self.store = ExcelService()
        stored_topic = self.store.selected_topic()
        self._topic = TOPIC_ALIASES.get(stored_topic, stored_topic)
        if self._topic not in LESSONS:
            self._topic = "AWS & Cloud"
        self._lesson_index = self.store.lesson_index(self._topic) % len(LESSONS[self._topic])
        self._resume_topic = self._topic
        self._resume_lesson_index = self._lesson_index
        self._xp, self._streak = self.store.totals()
        self._quiz_passed = False
        self._review_mode = False
        self._activate_due_review()
        self._load_lesson_tools()

    def _lesson(self) -> Lesson:
        return LESSONS[self._topic][self._lesson_index]

    def _find_lesson(self, topic: str, title: str) -> int | None:
        for index, lesson in enumerate(LESSONS.get(topic, ())):
            if lesson.title == title:
                return index
        return None

    def _activate_due_review(self) -> bool:
        for topic, title in self.store.due_reviews():
            index = self._find_lesson(topic, title)
            if index is not None:
                self._topic = topic
                self._lesson_index = index
                self._review_mode = True
                return True
        return False

    def _load_lesson_tools(self) -> None:
        lesson = self._lesson()
        self._bookmarked = self.store.is_bookmarked(lesson.topic, lesson.title)
        self._lesson_note = self.store.lesson_note(lesson.topic, lesson.title)
        self._review_state = self.store.review_state(lesson.topic, lesson.title)

    @staticmethod
    def _mastery_label(level: int) -> str:
        return ("New", "Learning", "Practicing", "Mastered")[max(0, min(3, level))]

    @Property("QStringList", constant=True)
    def topics(self) -> list[str]:
        return list(LESSONS)

    @Property(str, notify=changed)
    def topic(self) -> str:
        return self._topic

    @Property(str, notify=changed)
    def title(self) -> str:
        return self._lesson().title

    @Property(str, notify=changed)
    def description(self) -> str:
        return self._lesson().description

    @Property(str, notify=changed)
    def whyItMatters(self) -> str:
        return self._lesson().why_it_matters

    @Property(str, notify=changed)
    def scenario(self) -> str:
        lesson = self._lesson()
        return lesson.recall_scenario if self._review_mode else lesson.scenario

    @Property(str, notify=changed)
    def deeper(self) -> str:
        return self._lesson().deeper

    @Property(int, notify=changed)
    def minutes(self) -> int:
        return self._lesson().minutes

    @Property(int, notify=changed)
    def xp(self) -> int:
        return self._xp

    @Property(int, notify=changed)
    def streak(self) -> int:
        return self._streak

    @Property(str, notify=changed)
    def question(self) -> str:
        lesson = self._lesson()
        return lesson.recall_question if self._review_mode else lesson.question

    @Property("QStringList", notify=changed)
    def options(self) -> list[str]:
        lesson = self._lesson()
        return list(lesson.recall_options if self._review_mode else lesson.options)

    @Property(bool, notify=changed)
    def quizPassed(self) -> bool:
        return self._quiz_passed

    @Property(bool, notify=changed)
    def bookmarked(self) -> bool:
        return self._bookmarked

    @Property(str, notify=changed)
    def lessonNote(self) -> str:
        return self._lesson_note

    @Property(bool, notify=changed)
    def reviewMode(self) -> bool:
        return self._review_mode

    @Property(int, notify=changed)
    def masteryLevel(self) -> int:
        return int(self._review_state["mastery_level"])

    @Property(str, notify=changed)
    def masteryLabel(self) -> str:
        return self._mastery_label(self.masteryLevel)

    @Property(str, notify=changed)
    def nextReviewText(self) -> str:
        due = str(self._review_state["due_date"])
        return f"Next review: {due}" if due else "Review schedule ready after completion"

    @Property(int, notify=changed)
    def bookmarkCount(self) -> int:
        return len(self.store.bookmarks())

    @Property("QStringList", notify=changed)
    def bookmarkItems(self) -> list[str]:
        return [f"{topic}  •  {title}" for topic, title in self.store.bookmarks()]

    @Slot(str)
    def selectTopic(self, topic: str) -> None:
        if topic in LESSONS and topic != self._topic:
            self._topic = topic
            self._lesson_index = self.store.lesson_index(topic) % len(LESSONS[topic])
            self._resume_topic = self._topic
            self._resume_lesson_index = self._lesson_index
            self._review_mode = False
            self._quiz_passed = False
            self.store.set_selected_topic(topic)
            self._load_lesson_tools()
            self.changed.emit()

    @Slot()
    def nextLesson(self) -> None:
        if self._review_mode:
            self._topic = self._resume_topic
            self._lesson_index = self._resume_lesson_index
            self._review_mode = False
        else:
            self._lesson_index = (self._lesson_index + 1) % len(LESSONS[self._topic])
            self._resume_topic = self._topic
            self._resume_lesson_index = self._lesson_index
        self.store.set_lesson_index(self._topic, self._lesson_index)
        self._quiz_passed = False
        self._load_lesson_tools()
        self.changed.emit()

    @Slot(result=bool)
    def toggleBookmark(self) -> bool:
        lesson = self._lesson()
        self._bookmarked = not self._bookmarked
        self.store.set_bookmarked(lesson.topic, lesson.title, self._bookmarked)
        self.changed.emit()
        self.celebration.emit(
            "Lesson bookmarked." if self._bookmarked else "Bookmark removed."
        )
        return self._bookmarked

    @Slot(int)
    def openBookmark(self, index: int) -> None:
        bookmarks = self.store.bookmarks()
        if index < 0 or index >= len(bookmarks):
            return
        topic, title = bookmarks[index]
        lesson_index = self._find_lesson(topic, title)
        if lesson_index is None:
            return
        self._topic = topic
        self._lesson_index = lesson_index
        self._resume_topic = topic
        self._resume_lesson_index = lesson_index
        self._review_mode = False
        self._quiz_passed = False
        self.store.set_selected_topic(topic)
        self.store.set_lesson_index(topic, lesson_index)
        self._load_lesson_tools()
        self.changed.emit()

    @Slot(int)
    def removeBookmark(self, index: int) -> None:
        bookmarks = self.store.bookmarks()
        if index < 0 or index >= len(bookmarks):
            return
        topic, title = bookmarks[index]
        self.store.set_bookmarked(topic, title, False)
        self._load_lesson_tools()
        self.changed.emit()
        self.celebration.emit("Bookmark removed.")

    @Slot(str)
    def saveLessonNote(self, note: str) -> None:
        lesson = self._lesson()
        self.store.save_lesson_note(lesson.topic, lesson.title, note)
        self._lesson_note = self.store.lesson_note(lesson.topic, lesson.title)
        self.changed.emit()
        self.celebration.emit(
            "Learning takeaway saved."
            if self._lesson_note
            else "Learning takeaway cleared."
        )

    @Slot(str)
    def setConfidence(self, confidence: str) -> None:
        if confidence not in {"got_it", "need_practice", "review_later"}:
            return
        lesson = self._lesson()
        self.store.set_confidence(lesson.topic, lesson.title, confidence)
        self._load_lesson_tools()
        self.changed.emit()

    @Slot(int)
    def checkAnswer(self, answer: int) -> None:
        lesson = self._lesson()
        expected = lesson.recall_answer if self._review_mode else lesson.answer
        explanation = (
            lesson.recall_explanation if self._review_mode else lesson.explanation
        )
        self._quiz_passed = answer == expected
        if self._review_mode and not self._quiz_passed:
            self.store.record_review_result(lesson.topic, lesson.title, False)
            self._load_lesson_tools()
        self.changed.emit()
        if self._quiz_passed:
            self.quizResult.emit(f"Correct — {explanation}", True)
        else:
            self.quizResult.emit("Not quite. Review the scenario and try again.", False)

    @Slot(result=bool)
    def completeLesson(self) -> bool:
        lesson = self._lesson()
        if not self._quiz_passed:
            self.celebration.emit("Answer the knowledge check first.")
            return False
        if self._review_mode:
            self.store.record_review_result(lesson.topic, lesson.title, True)
            awarded = self.store.complete(lesson.topic, f"{lesson.title} • Recall", 10)
            self._xp, self._streak = self.store.totals()
            self._load_lesson_tools()
            self.changed.emit()
            self.celebration.emit(
                (
                    f"+10 XP — mastery is now {self.masteryLabel}."
                    if awarded
                    else f"Recall strengthened — mastery is {self.masteryLabel}."
                )
            )
            return True
        if self.store.complete(lesson.topic, lesson.title, lesson.xp):
            self.store.set_confidence(lesson.topic, lesson.title, "review_later")
            self._xp, self._streak = self.store.totals()
            self._load_lesson_tools()
            self.changed.emit()
            self.celebration.emit(f"+{lesson.xp} XP — learning complete!")
        else:
            self.celebration.emit("This flash is already complete today.")
        return True
