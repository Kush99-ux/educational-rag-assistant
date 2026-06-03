from abc import ABC, abstractmethod

from src.models.search_result import SearchResult


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        k: int = 5
    ) -> list[SearchResult]:
        pass