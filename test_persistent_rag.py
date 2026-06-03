from src.core.service_container import (
    ServiceContainer
)

container = ServiceContainer()

container.vector_store.load(
    "vector_store"
)

response = container.rag_pipeline.answer(
    "What is the GPA of Kush Sahu?"
)

print("ANSWER:")
print(response.answer)

print("\nSOURCES:")

for source in response.sources:
    print(source)