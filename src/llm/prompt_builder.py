from src.models.search_result import SearchResult


def build_rag_prompt(
    question: str,
    results: list[SearchResult]
) -> str:

    question_lower = question.lower()

    # =====================================
    # QUESTION TYPE DETECTION
    # =====================================

    question_type = "general"

    if any(
        keyword in question_lower
        for keyword in [
            "summarize",
            "summary",
            "overview",
            "everything about",
            "tell me about",
            "profile"
        ]
    ):
        question_type = "summary"

    elif "table" in question_lower:
        question_type = "table"

    elif "page" in question_lower:
        question_type = "page"

    elif any(
        keyword in question_lower
        for keyword in [
            "phone",
            "email",
            "cgpa",
            "gpa",
            "age",
            "dob",
            "date of birth",
            "qualification",
            "education",
            "languages",
            "skills"
        ]
    ):
        question_type = "fact"

    # =====================================
    # BUILD STRUCTURED CONTEXT
    # =====================================

    context_sections = []

    for i, result in enumerate(results, start=1):

        source_name = (
            result.chunk.metadata.get(
                "source_name",
                "Unknown"
            )
        )

        chunk_index = (
            result.chunk.metadata.get(
                "chunk_index",
                "Unknown"
            )
        )

        context_sections.append(
            f"""
CONTEXT SECTION {i}

Source: {source_name}
Chunk: {chunk_index}

{result.chunk.text}
"""
        )

    context = "\n".join(
        context_sections
    )

    # =====================================
    # QUESTION-SPECIFIC INSTRUCTIONS
    # =====================================

    extra_instruction = ""

    if question_type == "summary":

        extra_instruction = """
This is a summary request.

Create a structured summary.

When applicable include:

- Personal Information
- Education
- Experience
- Skills
- Certifications
- Awards
- Key Highlights

Combine information from all relevant context sections.
"""

    elif question_type == "table":

        extra_instruction = """
This is a table extraction request.

If a table exists in the context:

- Extract ALL rows and columns.
- Return the complete table.
- Do not summarize.
- Do not omit entries.
- Preserve structure whenever possible.
"""

    elif question_type == "page":

        extra_instruction = """
This is a page-specific request.

Focus on information from the requested page.

Provide a detailed answer using only the relevant page content.
"""

    elif question_type == "fact":

        extra_instruction = """
This is a factual lookup request.

Return only the requested information.

Be concise and precise.
"""

    # =====================================
    # FINAL PROMPT
    # =====================================

    prompt = f"""
You are an educational document assistant.

Use ONLY the provided context.

General Instructions:

1. Carefully analyze ALL context sections.

2. Combine information from multiple sections when necessary.

3. Use only information explicitly present in the context.

4. Do NOT use outside knowledge.

5. Do NOT invent facts.

6. If partial information exists,
provide the available information.

7. When multiple sections contain relevant information,
combine them into one complete answer.

8. If a table is requested and present,
extract the complete table.

9. If a summary is requested,
provide a structured summary.

10. Only respond with:

"I could not find the answer in the provided material."

when absolutely no relevant information exists.

{extra_instruction}

========================================

{context}

========================================

Question:
{question}

Answer:
"""

    return prompt