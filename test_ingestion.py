from src.ingestion.pdf_loader import load_pdf

document = load_pdf(
    "C:/Users/kushs/Downloads/c1.pdf"
)

print(document.filename)
print(document.page_count)
print(document.content[:500])