from pathlib import Path

from pypdf import PdfReader

from src.models.document import Document


def load_pdf(pdf_path: str) -> Document:

    path = Path(pdf_path)

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Expected a PDF file, got: {path.suffix}"
        )

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    reader = PdfReader(path)

    text_parts = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text)

    content = "\n\n".join(text_parts)

    return Document(
        filename=path.name,
        content=content,
        page_count=len(reader.pages)
    )