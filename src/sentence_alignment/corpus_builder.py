"""
Builds the final HVB corpus TSV from aligned sentence pairs.

ID format: HVB_fff.ccc.ppp.ss
  fff = file/work index (3 digits)
  ccc = chapter index (3 digits)
  ppp = page index (3 digits)
  ss  = sentence index within page (2 digits)
"""


def build(pairs: list[dict], work_id: str, work_index: int) -> list[dict]:
    """
    Assign HVB IDs and format pairs as TSV rows.

    Args:
        pairs:      List of {"han": str, "viet": str, "score": float}
        work_id:    Work slug (e.g. "an-nam-chi-luoc")
        work_index: 1-based index of this work in config.

    Returns:
        List of dicts ready to write as TSV rows.
    """
    # TODO: for each pair, assign ID using utils.generate_id(work_index, chapter, page, sent)
    # TODO: chapter/page defaults to 1 unless metadata is available
    # TODO: return list of {"id": ..., "han_text": ..., "viet_text": ..., "align_score": ...}
    pass


def write_tsv(rows: list[dict], output_path: str) -> None:
    # TODO: open output_path for writing with utf-8 encoding
    # TODO: write header: id, han_text, viet_text, align_score
    # TODO: write each row as tab-separated values
    pass


def merge_tsv(input_paths: list[str], output_path: str) -> None:
    # TODO: read all input TSV files (skip header after first)
    # TODO: write merged content to output_path
    pass
