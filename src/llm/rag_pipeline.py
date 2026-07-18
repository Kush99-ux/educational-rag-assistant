import time

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

        # Start total timer
        total_start = time.perf_counter()

        # -------------------------------
        # Query Rewrite
        # -------------------------------
        rewrite_start = time.perf_counter()

        rewritten_question = (
            self.query_rewriter.rewrite(
                question,
                chat_history
            )
        )

        rewrite_time = (
            time.perf_counter()
            - rewrite_start
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

        # -------------------------------
        # Retrieval
        # -------------------------------
        retrieval_start = (
            time.perf_counter()
        )

        results = (
            self.retriever.retrieve(
                rewritten_question,
                k=k
            )
        )

        retrieval_time = (
            time.perf_counter()
            - retrieval_start
        )

        print(
            "STEP 2 - Retrieval Done"
        )

        # -------------------------------
        # Prompt Building
        # -------------------------------
        prompt_start = (
            time.perf_counter()
        )

        prompt = build_rag_prompt(
            rewritten_question,
            results
        )

        prompt_time = (
            time.perf_counter()
            - prompt_start
        )

        print(
            "STEP 3 - Prompt Built"
        )

        # -------------------------------
        # LLM Generation
        # -------------------------------
        llm_start = (
            time.perf_counter()
        )

        answer = (
            self.llm.generate(
                prompt
            )
        )

        llm_time = (
            time.perf_counter()
            - llm_start
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

        # -------------------------------
        # Performance Report
        # -------------------------------
        total_time = (
            time.perf_counter()
            - total_start
        )

        print("\n" + "=" * 45)
        print("          PERFORMANCE REPORT")
        print("=" * 45)
        print(
            f"Query Rewrite      : {rewrite_time:.3f} s"
        )
        print(
            f"Retrieval          : {retrieval_time:.3f} s"
        )
        print(
            f"Prompt Building    : {prompt_time:.3f} s"
        )
        print(
            f"LLM Generation     : {llm_time:.3f} s"
        )
        print("-" * 45)
        print(
            f"Total Pipeline     : {total_time:.3f} s"
        )
        print("=" * 45)

        return RAGResponse(
            answer=answer,
            sources=sources
        )
