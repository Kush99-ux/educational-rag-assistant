from dataclasses import dataclass

from src.models.embedded_chunk import EmbeddedChunk


@dataclass
class SearchResult:

    chunk: EmbeddedChunk

    score: float