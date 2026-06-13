from pathlib import Path

import fitz

from src.models.document import (
    Document
)

from src.ingestion.ocr_extractor import (
    extract_text_from_image
)


def load_pdf(
    pdf_path: str
) -> Document:

    path = Path(pdf_path)

    if (
        path.suffix.lower()
        != ".pdf"
    ):

        raise ValueError(
            f"Expected a PDF file, "
            f"got: {path.suffix}"
        )

    if not path.exists():

        raise FileNotFoundError(
            f"PDF not found: "
            f"{pdf_path}"
        )

    pdf = fitz.open(
        pdf_path
    )

    text_parts = []

    image_counter = 0

    temp_dir = (
        Path("temp_ocr")
    )

    temp_dir.mkdir(
        exist_ok=True
    )

    # ----------------------------------
    # PAGE LOOP
    # ----------------------------------

    for page_num in range(
        len(pdf)
    ):

        page = pdf[
            page_num
        ]

        # --------------------------
        # TEXT EXTRACTION
        # --------------------------

        page_text = (
            page.get_text()
        )

        if page_text:

            text_parts.append(
                f""" 
        
        PAGE_NUMBER: {page_num + 1}
        {page_text}
        """
            )

        # --------------------------
        # IMAGE EXTRACTION
        # --------------------------

        images = (
            page.get_images(
                full=True
            )
        )

        print(
            f"Page "
            f"{page_num + 1}: "
            f"{len(images)} images"
        )

        for image in images:

            try:

                xref = image[0]

                image_dict = (
                    pdf.extract_image(
                        xref
                    )
                )

                image_bytes = (
                    image_dict[
                        "image"
                    ]
                )

                image_path = (
                    temp_dir
                    /
                    f"page_"
                    f"{page_num}_"
                    f"{image_counter}.png"
                )

                with open(
                    image_path,
                    "wb"
                ) as img_file:

                    img_file.write(
                        image_bytes
                    )

                ocr_text = (
                    extract_text_from_image(
                        str(image_path)
                    )
                )

                if ocr_text:

                    text_parts.append(
                        f"""

                    PAGE_NUMBER: {page_num + 1}

                    OCR_CONTENT:

                    {ocr_text}

                    """
                    )
                    
                image_counter += 1

            except Exception as e:

                print(
                    f"IMAGE OCR ERROR: "
                    f"{e}"
                )

    content = "\n\n".join(
        text_parts
    )

    print(
    "\n===== OCR DOCUMENT PREVIEW =====\n"
    )

    print(
        content[:10000]
    )

    print(
        "\n===============================\n"
    )

    return Document(
        source_name=path.name,
        content=content,
        metadata={
            "type": "pdf",
            "pages": len(pdf)
        }
    )
