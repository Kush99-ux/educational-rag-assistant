from src.ingestion.loader_factory import (
    load_document
)

from src.preprocessing.chunker import (
    chunk_document
)

from src.embeddings.embedding_pipeline import (
    embed_chunks
)

from src.embeddings.bge_embedder import (
    BGEEmbedder
)

from src.vectorstores.faiss_vector_store import (
    FAISSVectorStore
)


class DocumentIngestionService:

    def __init__(
        self,
        embedder: BGEEmbedder,
        vector_store: FAISSVectorStore
    ):

        self.embedder = embedder

        self.vector_store = vector_store

    def ingest(
        self,
        file_path: str
    ):

        document = load_document(
            file_path
        )

        chunks = chunk_document(
            document
        )

        embedded_chunks = embed_chunks(
            chunks,
            self.embedder
        )

        self.vector_store.add(
            embedded_chunks
        )

        return len(
            embedded_chunks
        )