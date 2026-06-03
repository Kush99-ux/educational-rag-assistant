from abc import ABC, abstractmethod

from src.models.embedded_chunk import EmbeddedChunk


class BaseVectorStore(ABC):

    @abstractmethod
    def add(
        self,
        embedded_chunks: list[EmbeddedChunk]
    ):
        """
        Store embedded chunks.
        """
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        k: int = 5
    ) -> list[EmbeddedChunk]:
        """
        Return top-k similar chunks.
        """
        pass