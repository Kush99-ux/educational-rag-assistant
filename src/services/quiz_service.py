from src.llm.ollama_llm import (
    OllamaLLM
)

from src.models.quiz_request import (
    QuizRequest
)

from src.models.quiz_result import (
    QuizResult
)

from src.vectorstores.faiss_vector_store import (
    FAISSVectorStore
)


class QuizService:

    def __init__(
        self,
        vector_store: FAISSVectorStore
    ):

        self.vector_store = (
            vector_store
        )

        self.llm = OllamaLLM()

    # ----------------------------------
    # CONTEXT COLLECTION
    # ----------------------------------

    def _build_context(
        self,
        topics: list[str] | None
    ) -> str:

        chunks = (
            self.vector_store
            .embedded_chunks
        )

        print(
            f"QUIZ DEBUG - Total Chunks: {len(chunks)}"
        )

        if len(chunks) == 0:

            raise ValueError(
                "Knowledge base is empty."
            )

        selected_chunks = []

        # ----------------------------------
        # TOPIC FILTERING
        # ----------------------------------

        if topics:

            print(
                f"QUIZ DEBUG - Topics: {topics}"
            )

            for chunk in chunks:

                chunk_text = (
                    chunk.text.lower()
                )

                if any(
                    topic.lower()
                    in chunk_text
                    for topic in topics
                ):

                    selected_chunks.append(
                        chunk
                    )

            print(
                f"QUIZ DEBUG - Topic Matches: "
                f"{len(selected_chunks)}"
            )

        else:

            selected_chunks = (
                chunks[:3]
            )

            print(
                "QUIZ DEBUG - Using first 3 chunks"
            )

        # ----------------------------------
        # FALLBACK
        # ----------------------------------

        if len(selected_chunks) == 0:

            print(
                "QUIZ DEBUG - No topic matches."
            )

            selected_chunks = (
                chunks[:3]
            )

        # ----------------------------------
        # BUILD CONTEXT
        # ----------------------------------

        context = "\n\n".join(

            chunk.text

            for chunk in selected_chunks[:3]

        )

        print(
            f"QUIZ DEBUG - Context Length: "
            f"{len(context)}"
        )

        return context

    # ----------------------------------
    # DIFFICULTY PROMPT
    # ----------------------------------

    def _difficulty_prompt(
        self,
        difficulty: str
    ) -> str:

        difficulty = (
            difficulty.lower()
        )

        if difficulty == "easy":

            return """
Generate EASY questions.

Focus on:
- Definitions
- Core concepts
- Direct recall
- Basic formula usage
"""

        if difficulty == "hard":

            return """
Generate HARD questions.

Focus on:
- Deep analysis
- Advanced reasoning
- Edge cases
- Complex applications
"""

        if difficulty == "mixed":

            return """
Generate a MIX of:

- Easy questions
- Medium questions
- Hard questions
"""

        return """
Generate MEDIUM difficulty questions.

Focus on:
- Conceptual understanding
- Applications
- Multi-step reasoning
"""

    # ----------------------------------
    # MAIN GENERATION
    # ----------------------------------

    def generate_quiz(
        self,
        request: QuizRequest
    ) -> QuizResult:

        print(
            "\nQUIZ GENERATION STARTED"
        )

        print(
            f"Difficulty: {request.difficulty}"
        )

        print(
            f"Length: {request.length}"
        )

        print(
            f"Topics: {request.topics}"
        )

        print(
            f"Exam Focused: "
            f"{request.exam_focused}"
        )

        context = (
            self._build_context(
                request.topics
            )
        )

        difficulty_prompt = (
            self._difficulty_prompt(
                request.difficulty
            )
        )

        exam_prompt = ""

        if request.exam_focused:

            exam_prompt = """
Focus heavily on:

- Frequently tested concepts
- Important formulas
- Core definitions
- Typical university exam questions

Avoid trivia.
"""

        prompt = f"""
You are an expert educational quiz generator.

Generate exactly
{request.length}
multiple-choice questions.

{difficulty_prompt}

{exam_prompt}

Requirements:

1. Every question must have:
   A, B, C, D options

2. Only ONE option
   should be correct.

3. Include:

Answer:

Explanation:

for every question.

4. Do NOT invent facts.

5. Use only the
provided study material.

Output Format:

Question 1:
...

A)
B)
C)
D)

Answer: X

Explanation:
...

Study Material:

{context}
"""

        print(
            "QUIZ V2 - Prompt Built"
        )

        print(
            f"QUIZ DEBUG - Prompt Length: "
            f"{len(prompt)}"
        )

        print(
            "QUIZ DEBUG - Sending Prompt To Ollama"
        )

        quiz_text = (
            self.llm.generate(
                prompt
            )
        )

        print(
            "QUIZ DEBUG - Ollama Returned"
        )

        print(
            "QUIZ V2 - Generation Complete"
        )

        return QuizResult(
            quiz_text=quiz_text,
            difficulty=request.difficulty,
            length=request.length,
            topics=request.topics
            or [],
            exam_focused=request.exam_focused
        )