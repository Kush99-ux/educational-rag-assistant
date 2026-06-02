from src.ingestion.loader_factory import load_document

document = load_document(
    "C:/Users/kushs/Downloads/c1.pdf"
)

print(document.source_name)
print(document.metadata)