from dataclasses import dataclass


@dataclass
class QuizAttempt:

    quiz_text: str

    user_answers: list[str]