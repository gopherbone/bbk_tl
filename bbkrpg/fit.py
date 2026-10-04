"""Fit English text into dialogue pages with bbk_tl Sans metrics.

A page is up to 3 rows. Rows beside a portrait are narrower (fontpatch's
ROW_WIDTHS_*). Words wrap greedily; a word wider than a row is split by
characters. "\\n" in the text forces a row break; "\\f" forces a page break.
"""

from __future__ import annotations

from . import font_sans
from .fontpatch import ROW_WIDTHS_PLAIN, ROW_WIDTHS_PORTRAIT


def _split_word(word: str, width: int) -> list[str]:
    parts, cur = [], ""
    for ch in word:
        if cur and font_sans.text_width(cur + ch) > width:
            parts.append(cur)
            cur = ch
        else:
            cur += ch
    return parts + ([cur] if cur else [])


def pages(text: str, portrait: bool) -> list[list[str]]:
    widths = ROW_WIDTHS_PORTRAIT if portrait else ROW_WIDTHS_PLAIN
    out: list[list[str]] = []
    for block in text.split("\f"):
        rows: list[str] = []

        def width_now() -> int:
            return widths[len(rows) % len(widths)]

        for line in block.split("\n"):
            cur = ""
            for word in line.split(" "):
                if not word:
                    continue
                cand = f"{cur} {word}" if cur else word
                if font_sans.text_width(cand) <= width_now():
                    cur = cand
                    continue
                if cur:
                    rows.append(cur)
                    cur = ""
                for piece in _split_word(word, width_now()):
                    if font_sans.text_width(piece) <= width_now() and not cur:
                        cur = piece
                    else:
                        rows.append(cur)
                        cur = piece
                    if font_sans.text_width(cur) > width_now():
                        rows.append(cur)
                        cur = ""
            rows.append(cur)
        rows = [r for r in rows] or [""]
        for i in range(0, len(rows), len(widths)):
            out.append(rows[i:i + len(widths)])
    return out


MESSAGE_WIDTH = 140      # widest row in a message box (fontpatch msgbox: box <= 155 px)


def rows(text: str, width: int) -> list[str]:
    """Word-wrap `text` into rows of at most `width` px ("\\n" forces a break)."""
    out: list[str] = []
    for line in text.split("\n"):
        cur = ""
        for word in line.split(" "):
            if not word:
                continue
            cand = f"{cur} {word}" if cur else word
            if font_sans.text_width(cand) <= width:
                cur = cand
                continue
            if cur:
                out.append(cur)
            cur = ""
            for piece in _split_word(word, width):
                if cur:
                    out.append(cur)
                cur = piece
        out.append(cur)
    return out
