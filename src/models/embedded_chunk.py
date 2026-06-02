from dataclasses import dataclass, field


@dataclass
class EmbeddedChunk:

    chunk_id: str

    text: str

    embedding: list[float]

    metadata: dict = field(default_factory=dict)