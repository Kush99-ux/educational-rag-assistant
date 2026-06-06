from src.core.service_container import (
    ServiceContainer
)

container = (
    ServiceContainer()
)

container.vector_store.load(
    "vector_store"
)

quiz = (
    container.quiz_service
    .generate_quiz(
        num_questions=5
    )
)

print(quiz)