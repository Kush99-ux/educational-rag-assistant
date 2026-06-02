from src.models.document import Document
from src.models.chunk import Chunk
from src.core.settings import load_config


def chunk_document(
    document: Document,
    chunk_size: int | None = None,
    overlap: int | None = None
):
    """
    Split a Document into overlapping chunks.

    If chunk_size or overlap are not provided,
    values are loaded from config.yaml.
    """

    config = load_config()

    if chunk_size is None:
        chunk_size = config["chunking"]["chunk_size"]

    if overlap is None:
        overlap = config["chunking"]["overlap"]

    chunks = []

    text = document.content

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end]

        chunk = Chunk(
            text=chunk_text,
            metadata={
                "document_id": document.document_id,
                "source_name": document.source_name,
                "chunk_index": len(chunks),
                **document.metadata
            }
        )

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks