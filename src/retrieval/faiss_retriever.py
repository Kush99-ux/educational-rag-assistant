from src.core.base_retriever import BaseRetriever
from src.embeddings.bge_embedder import BGEEmbedder
from src.vectorstores.faiss_vector_store import FAISSVectorStore
from src.models.search_result import SearchResult

import re


class FAISSRetriever(
    BaseRetriever
):

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        embedder: BGEEmbedder
    ):

        self.vector_store = vector_store

        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        k: int = 10
    ):

        print("\n===== RETRIEVER CALLED =====")
        print(f"Query: {query}")

        query_lower = query.lower()

        special_results = []

        # ==========================
        # TABLE DETECTION
        # ==========================

        table_match = re.search(
            r"table\s+(\d+\.\d+)",
            query_lower
        )

        if table_match:

            table_number = table_match.group(1)

            print(
                f"TABLE DETECTED: "
                f"{table_number}"
            )

            for chunk in self.vector_store.embedded_chunks:

                if (
                    f"table {table_number}"
                    in chunk.text.lower()
                ):

                    print(
                        f"FOUND TABLE IN CHUNK "
                        f"{chunk.metadata.get('chunk_index')}"
                    )

                    special_results.append(
                        SearchResult(
                            chunk=chunk,
                            score=999.0
                        )
                    )

        # ==========================
        # PAGE DETECTION
        # ==========================

        page_match = re.search(
            r"page\s+(\d+)",
            query_lower
        )

        if page_match:

            page_number = page_match.group(1)

            print(
                f"PAGE DETECTED: "
                f"{page_number}"
            )

            for chunk in self.vector_store.embedded_chunks:

                if (
                    f"page_number: {page_number}"
                    in chunk.text.lower()
                ):

                    print(
                        f"FOUND PAGE IN CHUNK "
                        f"{chunk.metadata.get('chunk_index')}"
                    )

                    special_results.append(
                        SearchResult(
                            chunk=chunk,
                            score=999.0
                        )
                    )

        # ==========================
        # EMBEDDING
        # ==========================

        query_embedding = self.embedder.embed(
            query
        )

        # ==========================
        # WIDE RETRIEVAL
        # ==========================

        semantic_results = (
            self.vector_store.search(
                query_embedding,
                20
            )
        )

        # ==========================
        # ADAPTIVE FILTERING
        # ==========================

        if semantic_results:

            top_score = (
                semantic_results[0].score
            )

            threshold = (
                top_score * 0.80
            )

            print(
                f"TOP SCORE: "
                f"{top_score:.4f}"
            )

            print(
                f"THRESHOLD: "
                f"{threshold:.4f}"
            )

            semantic_results = [

                result

                for result in semantic_results

                if result.score >= threshold

            ]

            print(
                f"ADAPTIVE RESULTS: "
                f"{len(semantic_results)}"
            )

        # ==========================
        # MERGE RESULTS
        # ==========================

        all_results = (
            special_results +
            semantic_results
        )

        # ==========================
        # DEDUPLICATION
        # ==========================

        unique_results = []

        seen_chunks = set()

        for result in all_results:

            chunk_id = (
                result.chunk.chunk_id
            )

            if chunk_id not in seen_chunks:

                seen_chunks.add(
                    chunk_id
                )

                unique_results.append(
                    result
                )

        # ==========================
        # SORT
        # ==========================

        unique_results.sort(
            key=lambda x: x.score,
            reverse=True
        )

        print(
            f"FINAL RESULTS: "
            f"{len(unique_results)}"
        )

        return unique_results[:k]