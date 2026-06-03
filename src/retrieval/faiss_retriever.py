from src.core.base_retriever import BaseRetriever
from src.embeddings.bge_embedder import BGEEmbedder
from src.vectorstores.faiss_vector_store import FAISSVectorStore


class FAISSRetriever(
    BaseRetriever
):

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        embedder: BGEEmbedder
    ):

        self.vector_store = vector_store

        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        k: int = 5
    ):

        query_embedding = self.embedder.embed(
            query
        )

        return self.vector_store.search(
            query_embedding,
            k
        )