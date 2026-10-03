import pymupdf


def extract_resume_text(pdf_path: str) -> str:
    """Extract text from a resume PDF."""

    document = pymupdf.open(pdf_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)