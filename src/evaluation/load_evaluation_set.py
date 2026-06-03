import json

from src.models.evaluation_sample import (
    EvaluationSample
)


def load_evaluation_set(
    path: str
):

    with open(
        path,
        "r"
    ) as f:

        data = json.load(f)

    return [
        EvaluationSample(
            question=item["question"],
            expected_source=item[
                "expected_source"
            ]
        )
        for item in data
    ]