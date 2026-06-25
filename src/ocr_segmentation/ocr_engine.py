"""
OCR dispatcher: routes to PaddleOCR (Han), pytesseract (Viet),
text-layer extraction, or direct read depending on lang and format.
"""


def run(image_paths: list[str], lang: str, fmt: str) -> list[str]:
    """
    Run OCR on a list of images or return text directly.

    Args:
        image_paths: List of image file paths (or empty for text format).
        lang:        "han" or "viet".
        fmt:         "pdf" | "images" | "text" | "mixed_page".

    Returns:
        List of raw text lines (one bbox / paragraph per element).
    """
    # TODO: if fmt == "text"       → read file directly, return lines
    # TODO: if fmt == "mixed_page" → call _ocr_mixed(image_paths) → pick lines for lang
    # TODO: if lang == "han"       → call _ocr_paddle_han(image_paths)
    # TODO: if lang == "viet"      → try _extract_text_layer first; if empty → call _ocr_tesseract_viet(image_paths)
    pass


def _ocr_paddle_han(image_paths: list[str]) -> list[str]:
    # TODO: init PaddleOCR(lang="ch", use_angle_cls=True, use_gpu=False) (lazy-load / cache)
    # TODO: for each image: call ocr.ocr(image_path, cls=True)
    # TODO: collect (bbox, text, confidence) tuples
    # TODO: return list of text strings (bbox metadata passed separately to bbox_sort)
    pass


def _ocr_tesseract_viet(image_paths: list[str]) -> list[str]:
    # TODO: import pytesseract; configure tesseract_cmd path if needed
    # TODO: for each image: call pytesseract.image_to_string(image, lang="vie")
    # TODO: split result into non-empty lines, collect and return
    pass


def _ocr_mixed(image_paths: list[str]) -> dict[str, list[str]]:
    # TODO: for each image: crop into Han region and Viet region
    #       (use fixed ratio or configurable "region" from pipeline.yaml)
    # TODO: call _ocr_paddle_han([han_crop]) for the Han region
    # TODO: call _ocr_tesseract_viet([viet_crop]) for the Viet region
    # TODO: return {"han": [...], "viet": [...]}
    pass


def _extract_text_layer(pdf_path: str, pages: list[int]) -> list[str]:
    # TODO: use fitz (PyMuPDF) to extract embedded text layer from PDF pages
    # TODO: return list of text lines; empty list if no text layer
    pass
