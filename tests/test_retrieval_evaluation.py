from src.ingestion.loader_factory import load_document
from src.preprocessing.chunker import chunk_document
from src.embeddings.embedding_pipeline import embed_chunks

from src.vectorstores.faiss_vector_store import (
    FAISSVectorStore
)

from src.retrieval.faiss_retriever import (
    FAISSRetriever
)

from src.evaluation.load_evaluation_set import (
    load_evaluation_set
)

from src.evaluation.retrieval_evaluator import (
    RetrievalEvaluator
)

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

retriever = FAISSRetriever(
    vector_store
)

samples = load_evaluation_set(
    "data/evaluation/evaluation_set.json"
)

evaluator = RetrievalEvaluator(
    retriever
)

results = evaluator.evaluate(
    samples,
    k=3
)

print(results)