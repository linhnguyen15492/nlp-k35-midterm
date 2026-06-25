"""
Character-level alignment verification using:
  - MED (Minimum Edit Distance / Levenshtein)
  - SinoNom_Similar.dic  (visually similar Han characters)
  - QuocNgu_SinoNom.dic  (Quoc ngu → SinoNom mapping)
"""


def verify(pairs: list[dict]) -> list[dict]:
    """
    Annotate each pair with per-character OCR confidence.

    Args:
        pairs: List of {"han": str, "viet": str, "score": float}

    Returns:
        Same list with added "char_status" field per character:
        "ok" | "corrected" | "error"
    """
    # TODO: load SinoNom_Similar.dic and QuocNgu_SinoNom.dic (lazy-load)
    # TODO: for each pair: call _verify_pair(han, viet)
    # TODO: attach result to pair dict
    pass


def _verify_pair(han: str, viet: str) -> list[dict]:
    """
    Returns per-character annotation for a Han/Viet sentence pair.
    """
    # TODO: transliterate viet → han candidates using QuocNgu_SinoNom.dic
    # TODO: compute MED between han and candidate string
    # TODO: for each Han char: check SinoNom_Similar.dic for near-duplicates
    # TODO: classify each char: "ok" / "corrected" / "error"
    # TODO: return list of {"char": str, "status": str}
    pass


def load_dic(path: str) -> dict:
    # TODO: read .dic file, parse into dict
    # TODO: return mapping dict
    pass
