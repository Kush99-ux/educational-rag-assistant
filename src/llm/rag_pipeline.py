from src.retrieval.faiss_retriever import (
    FAISSRetriever
)

from src.models.rag_response import (
    RAGResponse
)

from src.llm.prompt_builder import (
    build_rag_prompt
)

from src.llm.ollama_llm import (
    OllamaLLM
)

class RAGPipeline:

    def __init__(
        self,
        retriever: FAISSRetriever
    ):

        self.retriever = retriever

        self.llm = OllamaLLM()

    def answer(
        self,
        question: str,
        k: int = 3
    ) -> RAGResponse:

        results = self.retriever.retrieve(
        question,
        k=k
        )

        prompt = build_rag_prompt(
        question,
        results
        )

        answer = self.llm.generate(
            prompt
        )

        sources = []

        for result in results:

            sources.append(
                {
                    "source_name":
                        result.chunk.metadata[
                            "source_name"
                        ],

                    "chunk_index":
                        result.chunk.metadata[
                            "chunk_index"
                        ],

                    "score":
                        result.score
                }
            )

        return RAGResponse(
            answer=answer,
            sources=sources
        )