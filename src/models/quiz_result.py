from dataclasses import dataclass


@dataclass
class QuizResult:

    quiz_text: str

    difficulty: str

    length: int

    topics: list[str]

    exam_focused: bool