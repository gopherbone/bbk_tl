"""English versions of the image resources that contain Chinese text.

Each entry clears rectangles of the original picture and draws English in
bbk_tl Sans (scale 1 or 2) or in a 3x5 caps font that matches the game's small
digits. Coordinates are in image pixels. Images are rebuilt with
bbkrpg.image and replace the archive resource (same size, same mode).
"""

from __future__ import annotations

from . import font_sans
from . import image

# 3x5 capital letters for tight labels (battle status window)
_SMALL = {
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"], "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"], "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"], "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"], "M": ["101", "111", "111", "101", "101"],
    "N": ["110", "101", "101", "101", "101"], "O": ["010", "101", "101", "101", "010"],
    "P": ["110", "101", "110", "100", "100"], "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "Y": ["101", "101", "010", "010", "010"],
}


def small_width(s: str) -> int:
    return 4 * len(s) - 1 if s else 0


def sans_width(s: str, scale: int = 1) -> int:
    return font_sans.text_width(s) * scale


# key -> list of ops: ("clear", x0, y0, x1, y1[, color]) clears [x0,x1) x [y0,y1)
# ("text", x, y, str, scale[, color]) bbk_tl Sans, top of the 11-row glyph cell at y
# ("small", x, y, str[, color]) 3x5 caps
# ("ctext", cx, y, str, scale[, color]) centred on cx
IMAGES = {
    # title screen: logo, menu box, edition tag
    (11, 2, 14): [
        ("clear", 30, 3, 129, 30), ("ctext", 80, 6, "Demonbane", 2),
        ("clear", 96, 26, 152, 36), ("ctext", 124, 26, "Chronicle", 1),
        ("clear", 97, 45, 150, 76), ("ctext", 123, 48, "New Game", 1), ("ctext", 123, 62, "Continue", 1),
        ("clear", 95, 82, 132, 95), ("text", 99, 84, "Deluxe", 1),
    ],
    # save / load screen headers (white text on the black band)
    (11, 2, 15): [("clear", 36, 2, 124, 26, 1), ("ctext", 80, 8, "Save Game", 1, 0)],
    (11, 2, 16): [("clear", 36, 2, 124, 26, 1), ("ctext", 80, 8, "Load Game", 1, 0)],
    # battle status window: labels next to the small numbers, status counters row
    (11, 2, 11): [
        ("clear", 34, 4, 49, 32), ("small", 38, 10, "HP"), ("small", 34, 22, "ATK"),
        ("clear", 70, 4, 86, 32), ("small", 74, 10, "LUK"), ("small", 74, 22, "AGI"),
        ("clear", 5, 34, 116, 50),
        ("small", 9, 40, "ATK"), ("small", 25, 40, "DEF"), ("small", 41, 40, "AGI"), ("small", 57, 40, "PSN"),
        ("small", 73, 40, "CNF"), ("small", 89, 40, "SIL"), ("small", 105, 40, "SLP"),
    ],
    # level-up panel: stat labels
    (11, 2, 9): [("clear", 10, 7, 37, 91)] + [
        ("text", 11, 9 + 12 * i, s, 1) for i, s in enumerate(["HP", "MP", "Atk", "Def", "Agi", "Spi", "Luck"])
    ],
    # learned-magic box title
    (11, 2, 10): [("clear", 26, 6, 88, 50), ("ctext", 57, 24, "Learned", 1)],
    # game over banner
    (11, 2, 13): [("clear", 2, 2, 118, 20), ("ctext", 60, 6, "Death is a new beginning", 1)],
    # date banner (credits)
    (11, 5, 2): [("clear", 26, 1, 134, 15), ("ctext", 80, 3, "10 July 2004", 1)],
    # scroll / page header logo
    (11, 5, 1): [("clear", 44, 1, 116, 15), ("ctext", 80, 3, "Demonbane", 1)],
}


def _draw_sans(img, x, y, s, scale, color):
    for ch in s:
        g = font_sans.GLYPHS.get(ch, font_sans.GLYPHS["?"])
        for r, row in enumerate(g):
            for c, p in enumerate(row):
                if p == "#":
                    for dy in range(scale):
                        for dx in range(scale):
                            yy, xx = y + r * scale + dy, x + c * scale + dx
                            if 0 <= yy < len(img) and 0 <= xx < len(img[0]):
                                img[yy][xx] = color
        x += (len(g[0]) + 1) * scale


def _draw_small(img, x, y, s, color):
    for ch in s:
        for r, row in enumerate(_SMALL[ch]):
            for c, p in enumerate(row):
                if p == "1" and 0 <= y + r < len(img) and 0 <= x + c < len(img[0]):
                    img[y + r][x + c] = color
        x += 4


def render(key, blob: bytes) -> bytes:
    h, frames = image.decode(blob)
    for img in frames:
        for op in IMAGES[key]:
            if op[0] == "clear":
                x0, y0, x1, y1 = op[1:5]
                color = op[5] if len(op) > 5 else 0
                for y in range(y0, min(y1, len(img))):
                    for x in range(x0, min(x1, len(img[0]))):
                        if img[y][x] is not None or color is not None:
                            img[y][x] = color
            elif op[0] in ("text", "ctext"):
                x, y, s, scale = op[1:5]
                color = op[5] if len(op) > 5 else 1
                if op[0] == "ctext":
                    x = x - sans_width(s, scale) // 2
                _draw_sans(img, x, y, s, scale, color)
            elif op[0] == "small":
                x, y, s = op[1:4]
                _draw_small(img, x, y, s, op[4] if len(op) > 4 else 1)
    return image.encode(h, frames)


def apply(res: dict) -> None:
    """Replace the translated images in an archive's resource dict, in place."""
    for key in IMAGES:
        if key in res:
            res[key] = render(key, res[key])
