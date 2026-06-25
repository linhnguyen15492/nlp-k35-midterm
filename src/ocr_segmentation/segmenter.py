"""
Sentence segmentation:
  - Han text  → HanLP sentence tokenizer
  - Viet text → Underthesea sent_tokenize
"""


def segment(lines: list[str], lang: str) -> list[str]:
    """
    Tokenize a list of raw text lines into sentences.

    Args:
        lines: Raw OCR lines.
        lang:  "han" or "viet".

    Returns:
        List of sentence strings.
    """
    # TODO: join lines into a single text block
    # TODO: if lang == "han"  → use HanLP to split into sentences
    # TODO: if lang == "viet" → use underthesea.sent_tokenize
    # TODO: strip empty sentences
    # TODO: return list of sentence strings
    pass


def _segment_han(text: str) -> list[str]:
    # TODO: import hanlp
    # TODO: load HanLP pipeline (lazy-load / cache model)
    # TODO: run sentence segmentation on text
    # TODO: return list of sentences
    pass


def _segment_viet(text: str) -> list[str]:
    # TODO: from underthesea import sent_tokenize
    # TODO: run sent_tokenize(text)
    # TODO: return list of sentences
    pass
