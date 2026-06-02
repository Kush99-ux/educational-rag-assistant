from pathlib import Path

from src.ingestion.pdf_loader import load_pdf


def load_document(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )