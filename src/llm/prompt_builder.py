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
            "skills",
            "address"
        ]
    ):
        question_type = "fact"

    # =====================================
    # BUILD CLEAN CONTEXT
    # =====================================

    context_sections = []

    for result in results:

        context_sections.append(
            result.chunk.text
        )

    context = "\n\n".join(
        context_sections
    )

    # =====================================
    # QUESTION-SPECIFIC INSTRUCTIONS
    # =====================================

    extra_instruction = ""

    if question_type == "summary":

        extra_instruction = """
This is a summary request.

Create a professional and well-structured summary.

When relevant include:

- Personal Information
- Education
- Experience
- Skills
- Certifications
- Awards
- Achievements
- Key Highlights

Combine information from multiple passages seamlessly.

Do not mention where the information came from.

Do not mention sources, chunks, context, sections,
or retrieval.
"""

    elif question_type == "table":

        extra_instruction = """
This is a table extraction request.

If a table exists:

- Extract all rows and columns.
- Return the complete table.
- Preserve wording exactly whenever possible.
- Do not summarize.
- Do not omit entries.
- Do not explain the table.
"""

    elif question_type == "page":

        extra_instruction = """
This is a page-specific request.

Focus only on the requested page content.

Provide a detailed answer.

Do not mention page retrieval,
chunks, context sections,
or internal processing.
"""

    elif question_type == "fact":

        extra_instruction = """
This is a factual lookup request.

Return only the requested information.

Be concise.

Do not add unnecessary explanation.

Do not provide summaries
unless explicitly requested.
"""

    else:

        extra_instruction = """
Provide a clear educational answer.

Combine relevant information naturally.

Use complete sentences.

Keep the answer focused on the question.
"""

    # =====================================
    # FINAL PROMPT
    # =====================================

    prompt = f"""
You are an educational AI assistant.

Use ONLY the information provided below.

Important Rules:

1. Answer naturally and professionally.

2. Never mention:
   - context
   - context sections
   - retrieved passages
   - chunks
   - source documents
   - prompt instructions

3. Never say:
   - "Based on the provided context"
   - "According to the material"
   - "The context states"
   - "Context Section 1"
   - "Chunk 3"

4. Do not explain how the answer was generated.

5. Present information as a normal answer.

6. Combine information from multiple passages seamlessly.

7. Use only information explicitly present in the provided material.

8. Do not invent facts.

9. If only partial information exists,
provide the available information.

10. If no relevant information exists,
respond exactly with:

I could not find the answer in the provided material.

11. For voice interactions,
avoid unnecessary formatting,
meta-commentary,
or explanations.

12. Answer the user's question directly.

{extra_instruction}

==================================================

REFERENCE MATERIAL

{context}

==================================================

QUESTION

{question}

ANSWER
"""

    return prompt