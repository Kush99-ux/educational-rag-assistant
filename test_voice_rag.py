from src.audio.stt import SpeechToText
from src.audio.tts import TextToSpeech

from src.ingestion.loader_factory import load_document
from src.preprocessing.chunker import chunk_document
from src.embeddings.embedding_pipeline import embed_chunks

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

stt = SpeechToText()

tts = TextToSpeech()

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

print("Transcribing audio...")

question = stt.transcribe(
    "question2.wav"
)

print(
    f"\nQuestion: {question}"
)

response = rag.answer(
    question
)

print(
    f"\nAnswer:\n{response.answer}"
)

print(
    "\nSpeaking answer..."
)

tts.speak(
    response.answer
)

print(
    "\nDone."
)