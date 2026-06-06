from dataclasses import dataclass

from src.models.quiz_question import (
    QuizQuestion
)


@dataclass
class QuizResult:

    quiz_text: str

    difficulty: str

    length: int

    topics: list[str]

    exam_focused: bool

    generated_questions: int

    questions: list[QuizQuestion]