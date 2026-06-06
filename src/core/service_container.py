from src.embeddings.bge_embedder import (
    BGEEmbedder
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
from src.services.document_ingestion_service import (
    DocumentIngestionService
)

from src.services.quiz_service import (
    QuizService
)

from src.services.quiz_evaluator import (
    QuizEvaluator
)


class ServiceContainer:

    def __init__(self):

        self.embedder = BGEEmbedder()

        self.vector_store = (
            FAISSVectorStore()
        )

        self.retriever = (
            FAISSRetriever(
                self.vector_store,
                self.embedder
            )
        )

        self.rag_pipeline = (
            RAGPipeline(
                self.retriever
            )
        )

        self.ingestion_service = (
            DocumentIngestionService(
                self.embedder,
                self.vector_store
            )
        )

        self.quiz_service = (
            QuizService(
                self.vector_store
             )
        )

        self.quiz_evaluator = (
            QuizEvaluator()
        )