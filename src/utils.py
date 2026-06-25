"""
Shared utilities: ID generation and file I/O helpers.
"""
import json
import os


def generate_id(fff: int, ccc: int, ppp: int, ss: int) -> str:
    """
    Generate a HVB corpus ID.

    Format: HVB_fff.ccc.ppp.ss
    """
    # TODO: format each component with zero-padding (fff=3, ccc=3, ppp=3, ss=2)
    # TODO: return formatted ID string
    pass


def read_json(path: str) -> dict:
    # TODO: open path, parse JSON, return dict
    pass


def write_json(data: dict, path: str) -> None:
    # TODO: create parent directories if needed
    # TODO: write data as pretty-printed JSON with utf-8 encoding
    pass


def read_lines(path: str) -> list[str]:
    # TODO: open path with utf-8 encoding, return non-empty stripped lines
    pass


def write_lines(lines: list[str], path: str) -> None:
    # TODO: create parent directories if needed
    # TODO: write each line followed by newline, utf-8 encoding
    pass
