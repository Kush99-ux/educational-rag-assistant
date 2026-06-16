import fitz

pdf = fitz.open(
    "Cancer-definition and types.pdf"
)

for page_num in range(
    len(pdf)
):

    page = pdf[page_num]

    images = page.get_images(
        full=True
    )

    print(
        f"Page {page_num + 1}: "
        f"{len(images)} images"
    )