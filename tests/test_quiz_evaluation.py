from src.models.quiz_attempt import (
    QuizAttempt
)

from src.services.quiz_evaluator import (
    QuizEvaluator
)

quiz_text = """
Question 1

Answer: A

Question 2

Answer: C

Question 3

Answer: B
"""

attempt = QuizAttempt(

    quiz_text=quiz_text,

    user_answers=[
        "A",
        "B",
        "B"
    ]
)

result = (
    QuizEvaluator()
    .evaluate(
        attempt
    )
)

print(result)