from src.audio.voice_assistant import (
    VoiceAssistant
)

from src.ingestion.loader_factory import (
    load_document
)

from src.preprocessing.chunker import (
    chunk_document
)

from src.embeddings.embedding_pipeline import (
    embed_chunks
)

from src.vectorstores.faiss_vector_store import (
    FAISSVectorStore
)

from src.retrieval.faiss_retriever import (
    FAISSRetriever
)

from src.llm.rag_pipeline import (
    RAGPipeline
)

from src.embeddings.bge_embedder import (
    BGEEmbedder
)


print("Loading models...")

embedder = BGEEmbedder()

print("Loading document...")

document = load_document(
    "C:/Users/kushs/Downloads/c1.pdf"
)

chunks = chunk_document(
    document
)

embedded_chunks = embed_chunks(
    chunks,
    embedder
)

vector_store = FAISSVectorStore()

vector_store.add(
    embedded_chunks
)

retriever = FAISSRetriever(
    vector_store,
    embedder
)

rag = RAGPipeline(
    retriever
)

voice_assistant = VoiceAssistant(
    rag
)

print("Processing audio...")

result = (
    voice_assistant.answer_audio(
        "question.wav"
    )
)

print(
    "\n===================="
)

print(
    "QUESTION:"
)

print(
    result["question"]
)

print(
    "\nANSWER:"
)

print(
    result["answer"]
)

print(
    "\nSOURCES:"
)

for source in result["sources"]:

    print(source)

print(
    "\n===================="
)