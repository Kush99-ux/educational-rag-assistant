import re

from src.models.quiz_attempt import (
    QuizAttempt
)

from src.models.quiz_evaluation import (
    QuizEvaluation
)


class QuizEvaluator:

    def evaluate(
        self,
        attempt: QuizAttempt
    ) -> QuizEvaluation:

        # ----------------------------
        # EXTRACT CORRECT ANSWERS
        # ----------------------------

        correct_answers = re.findall(
            r"Answer:\s*([A-D])",
            attempt.quiz_text
        )

        # ----------------------------
        # SCORE CALCULATION
        # ----------------------------

        score = 0

        incorrect_questions = []

        for index, (
            user_answer,
            correct_answer
        ) in enumerate(

            zip(
                attempt.user_answers,
                correct_answers
            ),

            start=1

        ):

            if (

                user_answer
                .strip()
                .upper()

                ==

                correct_answer
                .strip()
                .upper()

            ):

                score += 1

            else:

                incorrect_questions.append(
                    index
                )

        # ----------------------------
        # ACCURACY
        # ----------------------------

        total_questions = (
            len(correct_answers)
        )

        accuracy = 0

        if total_questions > 0:

            accuracy = (

                score

                /

                total_questions

            ) * 100

        # ----------------------------
        # FEEDBACK
        # ----------------------------

        if accuracy >= 90:

            feedback = (
                "Excellent performance."
            )

        elif accuracy >= 75:

            feedback = (
                "Good performance."
            )

        elif accuracy >= 50:

            feedback = (
                "Average performance."
            )

        else:

            feedback = (
                "Needs improvement."
            )

        # ----------------------------
        # RETURN RESULT
        # ----------------------------

        return QuizEvaluation(

        score=score,

        total_questions=
        total_questions,

        accuracy=
        accuracy,

        feedback=
        feedback,

        correct_answers=
        correct_answers,

        incorrect_questions=
        incorrect_questions
    )