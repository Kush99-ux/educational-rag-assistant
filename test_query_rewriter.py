from src.retrieval.query_rewriter import (
    QueryRewriter
)

rewriter = QueryRewriter()

history = [
    {
        "role": "user",
        "content": "What is Kush's GPA?"
    },
    {
        "role": "assistant",
        "content": "8.1"
    }
]

question = (
    "Where does he study?"
)

print(
    rewriter.rewrite(
        question,
        history
    )
)