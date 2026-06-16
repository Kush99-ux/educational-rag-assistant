import fitz
import pytesseract

from PIL import Image


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf = fitz.open(
    r"C:\Users\kushs\educational-rag-assistant\Cancer-definition and types.pdf"
)

page = pdf[9]   # page 10

images = page.get_images(
    full=True
)

print(
    f"Images found: {len(images)}"
)

if len(images) > 0:

    xref = images[0][0]

    image_dict = pdf.extract_image(
        xref
    )

    image_bytes = image_dict[
        "image"
    ]

    with open(
        "temp_image.png",
        "wb"
    ) as f:

        f.write(
            image_bytes
        )

    text = pytesseract.image_to_string(
        Image.open(
            "temp_image.png"
        )
    )

    print(
        "\nOCR RESULT:\n"
    )

    print(text[:3000])