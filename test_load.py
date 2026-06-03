from src.vectorstores.faiss_vector_store import (
    FAISSVectorStore
)

store = FAISSVectorStore()

store.load(
    "vector_store"
)

print(
    len(store.embedded_chunks)
)

print(
    store.embedded_chunks[0].metadata
)