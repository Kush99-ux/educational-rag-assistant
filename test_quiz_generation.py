from src.core.service_container import (
    ServiceContainer
)

from src.models.quiz_request import (
    QuizRequest
)

container = (
    ServiceContainer()
)

container.vector_store.load(
    "vector_store"
)

request = QuizRequest(
    difficulty="easy",
    length=3,
    topics=["Java"],
    exam_focused=False
)

result = (
    container.quiz_service
    .generate_quiz(
        request
    )
)

print(
    result.quiz_text
)