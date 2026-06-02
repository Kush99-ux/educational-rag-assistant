from abc import ABC, abstractmethod


class BaseEmbedder(ABC):

    @abstractmethod
    def embed(self, text: str):
        """
        Embed a single text.
        """
        pass

    @abstractmethod
    def embed_batch(self, texts: list[str]):
        """
        Embed multiple texts.
        """
        pass