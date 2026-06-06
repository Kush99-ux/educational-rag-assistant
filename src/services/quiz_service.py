from src.llm.ollama_llm import (
    OllamaLLM
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

    def generate_quiz(
        self,
        num_questions: int = 3
    ) -> str:
        # ----------------------------------
        # COLLECT KNOWLEDGE BASE CONTENT
        # ----------------------------------

        chunks = (
            self.vector_store
            .embedded_chunks
        )

        print(f"Total Chunks: {len(chunks)}")

        if len(chunks) == 0:

            return (
                "No documents found in "
                "knowledge base."
            )

        # ----------------------------------
        # LIMIT CONTEXT SIZE
        # ----------------------------------

        context = "\n\n".join(

            chunk.text

            for chunk in chunks[:5]

        )

        # ----------------------------------
        # BUILD PROMPT
        # ----------------------------------

        prompt = f"""
You are an expert educational quiz generator.

Generate exactly {num_questions}
multiple-choice questions from the
provided study material.

Requirements:

1. Each question must have 4 options:
   A, B, C, D

2. Only one option should be correct.

3. Include the correct answer
   immediately below each question.

4. Do not invent facts that are not
   present in the material.

5. Focus on important concepts.

6. Make questions suitable for
   university students.

Output Format:

Question 1:
...

A)
B)
C)
D)

Answer: X

Question 2:
...

Material:

{context}
"""

        # ----------------------------------
        # GENERATE QUIZ
        # ----------------------------------

        print("QUIZ STEP 1 - Prompt Built")

        quiz = self.llm.generate(
            prompt
        )

        print("QUIZ STEP 2 - Quiz Generated"
        )

        return quiz
    
