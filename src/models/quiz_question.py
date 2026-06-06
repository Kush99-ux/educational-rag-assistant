from dataclasses import dataclass

from src.models.quiz_option import (
    QuizOption
)


@dataclass
class QuizQuestion:

    question: str

    options: list[QuizOption]

    answer: str

    explanation: str

    topic: str = "General"

    difficulty: str = "medium"