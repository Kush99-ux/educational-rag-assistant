from src.models.search_result import SearchResult


def build_rag_prompt(
    question: str,
    results: list[SearchResult]
) -> str:

    context = "\n\n".join(
        [
            result.chunk.text
            for result in results
        ]
    )

    prompt = f"""
You are an educational assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I could not find the answer in the provided material."

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt