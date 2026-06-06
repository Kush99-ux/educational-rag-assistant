import faiss
from pathlib import Path
import pickle
import numpy as np

from src.core.base_vector_store import BaseVectorStore
from src.models.embedded_chunk import EmbeddedChunk
from src.models.search_result import SearchResult


class FAISSVectorStore(BaseVectorStore):

    def __init__(self, dimension: int = 384):
        self.index = faiss.IndexFlatIP(dimension)
        self.embedded_chunks = []

    def add(self, embedded_chunks: list[EmbeddedChunk]):
        vectors = np.array(
            [chunk.embedding for chunk in embedded_chunks], 
            dtype="float32"
        )
        self.index.add(vectors)
        self.embedded_chunks.extend(embedded_chunks)

    def save(self, directory: str):
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(path / "faiss.index"))

        with open(path / "chunks.pkl", "wb") as f:
            pickle.dump(self.embedded_chunks, f)

    def load(self, directory: str):
        path = Path(directory)

        self.index = faiss.read_index(str(path / "faiss.index"))

        with open(path / "chunks.pkl", "rb") as f:
            self.embedded_chunks = pickle.load(f)

        print(
            f"Loaded Chunks: "
            f"{len(self.embedded_chunks)}"
        )

        print(
            f"Loaded Vectors: "
            f"{self.index.ntotal}"
        )

    def search(self, query_embedding: list[float], k: int = 5):
        print(
            "\n===== SEARCH CALLED ====="
        )

        print(
            f"Embedded Chunks: "
            f"{len(self.embedded_chunks)}"
        )

        print(
            f"FAISS Vectors: "
            f"{self.index.ntotal}"
        )

        if len(self.embedded_chunks) == 0:
            return []

        k = min(k, len(self.embedded_chunks))
        query_vector = np.array([query_embedding], dtype="float32")
        scores, indices = self.index.search(query_vector, k)

        print(
            f"Indices Returned: "
            f"{indices}"
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            if idx >= len(self.embedded_chunks):
                continue

            results.append(
                SearchResult(
                    chunk=self.embedded_chunks[idx], 
                    score=float(score)
                )
            )

        return results