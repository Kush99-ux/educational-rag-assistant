class QueryRewriter:

    def __init__(self):

        self.pronouns = {
            "he",
            "his",
            "him",
            "she",
            "her",
            "hers",
            "they",
            "their",
            "them",
            "it",
            "its"
        }

    def rewrite(
        self,
        question: str,
        chat_history: list
    ) -> str:

        # ----------------------------------
        # NO HISTORY
        # ----------------------------------

        if len(chat_history) == 0:

            print(
                "REWRITER: No history."
            )

            return question

        # ----------------------------------
        # CHECK IF PRONOUN EXISTS
        # ----------------------------------

        words = set(
            question.lower().split()
        )

        contains_pronoun = any(
            word in self.pronouns
            for word in words
        )

        if not contains_pronoun:

            print(
                "REWRITER: Standalone question."
            )

            return question

        # ----------------------------------
        # FIND LAST USER QUESTION
        # ----------------------------------

        previous_user_question = ""

        for message in reversed(chat_history):

            if message["role"] == "user":

                previous_user_question = (
                    message["content"]
                )

                break

        if previous_user_question == "":

            return question

        # ----------------------------------
        # SIMPLE REWRITE
        # ----------------------------------

        rewritten_question = (
            previous_user_question
            + " | "
            + question
        )

        print(
            f"REWRITER OUTPUT: "
            f"{rewritten_question}"
        )

        return rewritten_question