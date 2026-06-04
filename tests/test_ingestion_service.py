from src.core.service_container import (
    ServiceContainer
)

from src.services.document_ingestion_service import (
    DocumentIngestionService
)

container = ServiceContainer()

ingestion_service = (
    DocumentIngestionService(
        container.embedder,
        container.vector_store
    )
)

count = ingestion_service.ingest(
    "C:/Users/kushs/Downloads/c1.pdf"
)

print(
    f"Ingested {count} chunks"
)