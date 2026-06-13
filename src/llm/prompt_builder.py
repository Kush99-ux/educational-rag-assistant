from src.models.search_result import (
    SearchResult
)


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

Answer the question using ONLY the provided context.

Instructions:

1. Carefully analyze all context sections before answering.

2. If the answer appears across multiple context sections,
combine the information into one complete answer.

3. If the context contains a table,
extract the table contents and present them clearly.

4. If the context contains a list,
return the full list.

5. If the answer is partially present,
provide the available information.

6. Only say:

"I could not find the answer in the provided material."

when the context contains absolutely no relevant information.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt