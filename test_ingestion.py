from src.ingestion.loader_factory import load_document
from src.preprocessing.chunker import chunk_document

document = load_document(
    "C:/Users/kushs/Downloads/c1.pdf"
)

chunks = chunk_document(document)

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk Metadata:")
print(chunks[0].metadata)

print("\nFirst Chunk Preview:")
print(chunks[0].text[:300])