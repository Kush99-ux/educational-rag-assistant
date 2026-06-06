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
        # EXTRACT ANSWERS
        # ----------------------------

        correct_answers = re.findall(
            r"Answer:\s*([A-D])",
            attempt.quiz_text
        )

        # ----------------------------
        # SCORE CALCULATION
        # ----------------------------

        score = 0

        for (
            user_answer,
            correct_answer
        ) in zip(

            attempt.user_answers,
            correct_answers

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
        # RESULT
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
            correct_answers
        )