"""
Sentence alignment: maps Han sentences to Viet sentences.

Three methods:
  1. labse          — LaBSE cosine similarity (recommended)
  2. auto_translate — Gemini translate Han→Viet then TF-IDF compare
  3. greedy         — greedy length-ratio fallback (no external deps)
"""


def align(
    han_sentences: list[str],
    viet_sentences: list[str],
    method: str = "labse",
) -> list[dict]:
    """
    Align Han sentences to Viet sentences.

    Returns:
        List of dicts: {"han": str, "viet": str, "score": float}
    """
    # TODO: dispatch to _align_labse, _align_auto_translate, or _align_greedy
    pass


def _align_labse(han: list[str], viet: list[str]) -> list[dict]:
    # TODO: load LaBSE model via sentence_transformers (lazy-load / cache)
    # TODO: encode all han sentences → embeddings matrix H
    # TODO: encode all viet sentences → embeddings matrix V
    # TODO: compute cosine similarity matrix H × V^T
    # TODO: greedy best-match per Han sentence (argmax per row)
    # TODO: return pairs with cosine score
    pass


def _align_auto_translate(han: list[str], viet: list[str]) -> list[dict]:
    # TODO: for each Han sentence: call Gemini API to translate Han→Viet
    # TODO: build TF-IDF vectors for translated Han and original Viet
    # TODO: compute cosine similarity, greedy match
    # TODO: return pairs with similarity score
    pass


def _align_greedy(han: list[str], viet: list[str]) -> list[dict]:
    # TODO: compute length-ratio matrix len(h_i) / len(v_j)
    # TODO: greedily match sentence pairs closest to ratio 1.0
    # TODO: return pairs with ratio score
    pass
