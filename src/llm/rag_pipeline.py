from src.retrieval.faiss_retriever import (
    FAISSRetriever
)

from src.retrieval.query_rewriter import (
    QueryRewriter
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

        self.query_rewriter = (
            QueryRewriter()
        )

    def answer(
        self,
        question: str,
        chat_history: list = None,
        k: int = 3
    ) -> RAGResponse:

        if chat_history is None:

            chat_history = []

        rewritten_question = (
            self.query_rewriter.rewrite(
                question,
                chat_history
            )
        )

        print(
            f"\nOriginal Question: {question}"
        )

        print(
            f"Rewritten Question: {rewritten_question}"
        )

        question_lower = (
            rewritten_question.lower()
        )

        if (
            "table" in question_lower
            or
            "page" in question_lower
        ):
            k = 10

        print(
            "STEP 1 - Query Rewrite Done"
        )

        results = self.retriever.retrieve(
            rewritten_question,
            k=k
        )

        print(
            "STEP 2 - Retrieval Done"
        )

        prompt = build_rag_prompt(
            rewritten_question,
            results
        )

        print(
            "STEP 3 - Prompt Built"
        )

        answer = self.llm.generate(
            prompt
        )

        print(
            "STEP 4 - LLM Finished"
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