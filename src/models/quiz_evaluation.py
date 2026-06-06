from dataclasses import dataclass


@dataclass
class QuizEvaluation:

    score: int

    total_questions: int

    accuracy: float

    feedback: str

    correct_answers: list[str]