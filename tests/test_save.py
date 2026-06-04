from src.core.service_container import (
    ServiceContainer
)

container = ServiceContainer()

container.ingestion_service.ingest(
    "C:/Users/kushs/Downloads/c1.pdf"
)

container.vector_store.save(
    "vector_store"
)

print("Saved successfully")