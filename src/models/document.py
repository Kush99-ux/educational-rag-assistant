from dataclasses import dataclass


@dataclass
class Document:
    filename: str
    content: str
    page_count: int