from src.models.evaluation_sample import EvaluationSample


class RetrievalEvaluator:

    def __init__(
        self,
        retriever
    ):
        self.retriever = retriever

    def evaluate(
        self,
        samples: list[EvaluationSample],
        k: int = 3
    ):

        correct = 0

        for sample in samples:

            results = self.retriever.retrieve(
                sample.question,
                k=k
            )

            retrieved_sources = [
                result.chunk.metadata[
                    "source_name"
                ]
                for result in results
            ]

            if (
                sample.expected_source
                in retrieved_sources
            ):
                correct += 1

        accuracy = (
            correct / len(samples)
        ) * 100

        return {
            "total": len(samples),
            "correct": correct,
            "accuracy": accuracy
        }