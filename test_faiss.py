from src.ingestion.loader_factory import load_document
from src.preprocessing.chunker import chunk_document
from src.embeddings.embedding_pipeline import embed_chunks
from src.embeddings.bge_embedder import BGEEmbedder
from src.vectorstores.faiss_vector_store import FAISSVectorStore


document = load_document(
    "C:/Users/kushs/Downloads/c1.pdf"
)

chunks = chunk_document(
    document
)

embedded_chunks = embed_chunks(
    chunks
)

vector_store = FAISSVectorStore()

vector_store.add(
    embedded_chunks
)

embedder = BGEEmbedder()

query_embedding = embedder.embed(
    "education"
)

results = vector_store.search(
    query_embedding,
    k=3
)

print(
    f"Results: {len(results)}"
)

print(results[0].score)

print(results[0].chunk.metadata)

print(results[0].chunk.text[:300])