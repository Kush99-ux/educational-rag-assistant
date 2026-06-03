import faiss
import numpy as np

from src.core.base_vector_store import BaseVectorStore
from src.models.embedded_chunk import EmbeddedChunk
from src.models.search_result import SearchResult


class FAISSVectorStore(
    BaseVectorStore
):

    def __init__(
        self,
        dimension: int = 384
    ):

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.embedded_chunks = []

    def add(
        self,
        embedded_chunks: list[EmbeddedChunk]
    ):

        vectors = np.array(
            [
                chunk.embedding
                for chunk in embedded_chunks
            ],
            dtype="float32"
        )

        self.index.add(vectors)

        self.embedded_chunks.extend(
            embedded_chunks
        )

    def search(
        self,
        query_embedding: list[float],
        k: int = 5
        ):

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_vector,
            k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            results.append(
                SearchResult(
                    chunk=self.embedded_chunks[idx],
                    score=float(score)
                )
            )

        return results