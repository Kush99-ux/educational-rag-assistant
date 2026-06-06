import time

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

# ----------------------------------
# CONFIGURATION
# ----------------------------------

MAX_CONTEXT_CHUNKS = 8

ALLOWED_DIFFICULTIES = [
    "easy",
    "medium",
    "hard",
    "mixed"
]

ALLOWED_LENGTHS = [
    5,
    10,
    20,
    50
]


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
            f"QUIZ DEBUG - Total Chunks: "
            f"{len(chunks)}"
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
                f"QUIZ DEBUG - Topics: "
                f"{topics}"
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
                chunks[
                    :MAX_CONTEXT_CHUNKS
                ]
            )

            print(
                f"QUIZ DEBUG - Using first "
                f"{MAX_CONTEXT_CHUNKS} chunks"
            )

        # ----------------------------------
        # FALLBACK
        # ----------------------------------

        if len(selected_chunks) == 0:

            print(
                "QUIZ DEBUG - No topic "
                "matches found."
            )

            selected_chunks = (
                chunks[
                    :MAX_CONTEXT_CHUNKS
                ]
            )

        # ----------------------------------
        # BUILD CONTEXT
        # ----------------------------------

        context = "\n\n".join(

            chunk.text

            for chunk in selected_chunks[
                :MAX_CONTEXT_CHUNKS
            ]

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
- Theoretical understanding
"""

        if difficulty == "mixed":

            return """
Generate a balanced mix of:

- Easy questions
- Medium questions
- Hard questions

Ensure variety.
"""

        return """
Generate MEDIUM difficulty questions.

Focus on:

- Conceptual understanding
- Applications
- Multi-step reasoning
"""

    # ----------------------------------
    # VALIDATION
    # ----------------------------------

    def _validate_request(
        self,
        request: QuizRequest
    ):

        if (
            request.difficulty
            not in ALLOWED_DIFFICULTIES
        ):

            raise ValueError(
                f"Invalid difficulty: "
                f"{request.difficulty}"
            )

        if (
            request.length
            not in ALLOWED_LENGTHS
        ):

            raise ValueError(
                f"Invalid length: "
                f"{request.length}"
            )

    # ----------------------------------
    # MAIN GENERATION
    # ----------------------------------

    def generate_quiz(
        self,
        request: QuizRequest
    ) -> QuizResult:

        print(
            "\n"
            + "=" * 50
        )

        print(
            "QUIZ GENERATION STARTED"
        )

        print(
            "=" * 50
        )

        start_time = (
            time.time()
        )

        self._validate_request(
            request
        )

        print(
            f"Difficulty: "
            f"{request.difficulty}"
        )

        print(
            f"Length: "
            f"{request.length}"
        )

        print(
            f"Topics: "
            f"{request.topics}"
        )

        print(
            f"Exam Focused: "
            f"{request.exam_focused}"
        )

        # ----------------------------------
        # CONTEXT
        # ----------------------------------

        context = (
            self._build_context(
                request.topics
            )
        )

        # ----------------------------------
        # DIFFICULTY
        # ----------------------------------

        difficulty_prompt = (
            self._difficulty_prompt(
                request.difficulty
            )
        )

        # ----------------------------------
        # EXAM MODE
        # ----------------------------------

        exam_prompt = ""

        if request.exam_focused:

            exam_prompt = """
Prioritize:

- High-yield exam topics
- Frequently repeated concepts
- Core formulas
- Numerical problem solving
- University examination patterns

Avoid:

- Rare facts
- Trivial details
- Low-value information
"""

        # ----------------------------------
        # PROMPT
        # ----------------------------------

        prompt = f"""
You are an expert educational quiz generator.

Generate exactly
{request.length}
multiple-choice questions.

{difficulty_prompt}

{exam_prompt}

Requirements:

1. Every question must have:

A)
B)
C)
D)

2. Only ONE option
should be correct.

3. Include:

Answer:

Explanation:

for every question.

4. Do NOT invent facts.

5. Use ONLY the
provided study material.

6. Do NOT repeat concepts.

7. Every question should
test a different idea.

8. Questions should
gradually increase in
difficulty when possible.

9. Make questions suitable
for university students.

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
            "QUIZ DEBUG - Sending "
            "Prompt To Ollama"
        )

        # ----------------------------------
        # GENERATION
        # ----------------------------------

        quiz_text = (
            self.llm.generate(
                prompt
            )
        )

        print(
            "QUIZ DEBUG - Ollama Returned"
        )

        elapsed_time = (
            time.time()
            - start_time
        )

        print(
            f"QUIZ GENERATED IN "
            f"{elapsed_time:.2f} sec"
        )

        print(
            "QUIZ V2 - Generation Complete"
        )

        print(
            "=" * 50
        )

        # ----------------------------------
        # RESULT
        # ----------------------------------

        return QuizResult(
            quiz_text=quiz_text,
            difficulty=request.difficulty,
            length=request.length,
            topics=request.topics or [],
            exam_focused=request.exam_focused,
            generated_questions=request.length,
            questions=[]
        )