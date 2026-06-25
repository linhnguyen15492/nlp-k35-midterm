"""
Converts PDF pages to JPG images using PyMuPDF (fitz).
"""


def convert(pdf_path: str, pages: str | None = None, dpi: int = 200) -> list[str]:
    """
    Convert PDF pages to temporary JPG images.

    Args:
        pdf_path: Path to the PDF file.
        pages:    Page range string ("1-80", "1,3,5") or None for all pages.
        dpi:      Resolution for rendering.

    Returns:
        List of paths to temporary image files.
    """
    # TODO: open PDF with fitz.open(pdf_path)
    # TODO: parse pages string → list of 0-indexed page numbers
    # TODO: for each page: render to pixmap at given dpi, save to temp file
    # TODO: return list of temp image paths
    pass


def parse_page_range(pages: str | None, total: int) -> list[int]:
    """
    Parse a page range string into a list of 0-indexed page numbers.

    Args:
        pages: "1-80", "1,3,5", or None (all pages).
        total: Total number of pages in the PDF.

    Returns:
        List of 0-indexed page numbers.
    """
    # TODO: if pages is None → return list(range(total))
    # TODO: if pages contains "-" → parse as range (1-indexed → 0-indexed)
    # TODO: if pages contains "," → parse as comma-separated list
    pass
