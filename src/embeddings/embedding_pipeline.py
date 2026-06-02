from src.models.chunk import Chunk
from src.models.embedded_chunk import EmbeddedChunk
from src.embeddings.bge_embedder import BGEEmbedder


def embed_chunks(
    chunks: list[Chunk]
) -> list[EmbeddedChunk]:

    embedder = BGEEmbedder()

    texts = [
        chunk.text
        for chunk in chunks
    ]

    embeddings = embedder.embed_batch(
        texts
    )

    embedded_chunks = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        embedded_chunk = EmbeddedChunk(
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            embedding=embedding,
            metadata=chunk.metadata
        )

        embedded_chunks.append(
            embedded_chunk
        )

    return embedded_chunks