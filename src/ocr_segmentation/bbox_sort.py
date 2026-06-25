"""
Sorts OCR bounding boxes in the traditional Han reading order:
columns right → left, within each column top → bottom.
"""


def sort(lines: list[str], bbox_meta: list[dict] | None = None) -> list[str]:
    """
    Re-order OCR output lines by Han reading order.

    Args:
        lines:     Raw OCR text lines.
        bbox_meta: Optional list of bbox dicts {"x": ..., "y": ..., "w": ..., "h": ...}
                   corresponding to each line. If None, return lines as-is.

    Returns:
        Lines reordered right-to-left, top-to-bottom.
    """
    # TODO: if bbox_meta is None → return lines unchanged
    # TODO: pair each line with its bbox x-coordinate (column position)
    # TODO: cluster lines into columns by x-coordinate proximity
    # TODO: sort columns right → left (descending x)
    # TODO: within each column sort lines top → bottom (ascending y)
    # TODO: flatten and return sorted lines
    pass
