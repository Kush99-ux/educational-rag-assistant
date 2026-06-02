from src.ingestion.loader_factory import load_document
from src.preprocessing.chunker import chunk_document
from src.embeddings.embedding_pipeline import embed_chunks

document = load_document(
    "C:/Users/kushs/Downloads/c1.pdf"
)

chunks = chunk_document(
    document
)

embedded_chunks = embed_chunks(
    chunks
)

print(
    f"Chunks: {len(chunks)}"
)

print(
    f"Embedded Chunks: {len(embedded_chunks)}"
)

print(
    len(
        embedded_chunks[0].embedding
    )
)

print(
    embedded_chunks[0].metadata
)