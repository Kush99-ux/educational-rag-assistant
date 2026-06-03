from dataclasses import dataclass


@dataclass
class EvaluationSample:

    question: str

    expected_source: str