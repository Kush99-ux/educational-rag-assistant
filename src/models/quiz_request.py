from dataclasses import dataclass


@dataclass
class QuizRequest:

    difficulty: str = "medium"

    length: int = 5

    topics: list[str] | None = None

    exam_focused: bool = False