from abc import ABC, abstractmethod


class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(self, documents):
        pass

    @abstractmethod
    def search(self, query, k):
        pass