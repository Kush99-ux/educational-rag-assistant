from src.core.service_container import (
    ServiceContainer
)

container = ServiceContainer()

count = container.ingestion_service.ingest(
    "C:/Users/kushs/Downloads/c1.pdf"
)

print(f"Ingested {count} chunks")

response = container.rag_pipeline.answer(
    "What is the GPA of Kush Sahu?"
)

print(response.answer)