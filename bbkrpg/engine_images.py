"""Bitmaps with Chinese text inside the BBKRPG engine code (not in the archive).

The equipment screen's header 穿戴 is a 24-px-wide 1-bpp bitmap in the
engine (.gam 0x33861, the same offset in every engine build seen so far),
blitted at the top right of the screen. It is redrawn in place with the
translated name of the 穿戴 menu item (ENG/138a3.1). `apply` checks the
original bytes first and leaves other engine builds alone.
"""

from __future__ import annotations

import hashlib

from .images_en import _draw_sans, sans_width

GEAR_OFF = 0x33861
GEAR_W = 24                        # px; 3 bytes a row
GEAR_ROWS = 42                     # 穿 rows 2-16, 戴 rows 26-41
GEAR_SHA1 = "768fdd2a6a598ec638130c8867c04d925863a083"   # the original 126 bytes


def _pack(img: list[list[int]]) -> bytes:
    out = bytearray()
    for row in img:
        for b in range(3):
            out.append(sum(row[b * 8 + i] << (7 - i) for i in range(8)))
    return bytes(out)


def apply(gam: bytes, rows: list[dict]) -> tuple[bytes, list[str]]:
    n = GEAR_ROWS * 3
    orig = gam[GEAR_OFF:GEAR_OFF + n]
    if hashlib.sha1(orig).hexdigest() != GEAR_SHA1:
        return gam, []
    word = next((r["en"] for r in rows if r["id"] == "ENG/138a3.1" and r.get("en")), None)
    if not word:
        return gam, []
    if sans_width(word) > GEAR_W:
        return gam, [f"engine bitmap: {word!r} is wider than {GEAR_W} px"]
    img = [[0] * GEAR_W for _ in range(GEAR_ROWS)]
    _draw_sans(img, (GEAR_W - sans_width(word)) // 2, 4, word, 1, 1)
    return gam[:GEAR_OFF] + _pack(img) + gam[GEAR_OFF + n:], []
