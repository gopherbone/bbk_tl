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
    "U": ["101", "101", "101", "101", "111"], "W": ["101", "101", "111", "111", "101"],
    "V": ["101", "101", "101", "101", "010"], "X": ["101", "101", "010", "101", "101"],
    "J": ["001", "001", "001", "101", "010"], "Q": ["010", "101", "101", "110", "011"],
    "Z": ["111", "001", "010", "100", "111"], "Y": ["101", "101", "010", "010", "010"],
    " ": ["000"] * 5, "-": ["000", "000", "111", "000", "000"], "'": ["010", "010", "000", "000", "000"],
    ":": ["000", "010", "000", "010", "000"], "^": ["010", "101", "000", "000", "000"],
    "_": ["000", "000", "000", "000", "111"], "[": ["110", "100", "100", "100", "110"],
    "]": ["011", "001", "001", "001", "011"], ",": ["000", "000", "000", "010", "100"],
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["110", "001", "010", "100", "111"], "3": ["110", "001", "010", "001", "110"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "110", "001", "110"],
    "6": ["011", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "110"],
}


def small_width(s: str) -> int:
    return 4 * len(s) - 1 if s else 0


def sans_width(s: str, scale: int = 1) -> int:
    return font_sans.text_width(s) * scale


# key -> list of ops: ("clear", x0, y0, x1, y1[, color]) clears [x0,x1) x [y0,y1)
# ("text", x, y, str, scale[, color]) bbk_tl Sans, top of the 11-row glyph cell at y
# ("small", x, y, str[, color]) 3x5 caps
# ("ctext", cx, y, str, scale[, color]) centred on cx
# ("invert", x0, y0, x1, y1) inverts opaque pixels in [x0,x1) x [y0,y1)
# ("resize", w, h, color) grows/crops the canvas at the right and bottom
# ("despeckle", n) whitens black blobs (8-connected) of at most n pixels
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
        ("clear", 68, 4, 86, 32), ("small", 71, 10, "LUK"), ("small", 71, 22, "AGI"),
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


def _despeckle(img, n):
    seen = set()
    for y0, row in enumerate(img):
        for x0, p in enumerate(row):
            if p != 1 or (x0, y0) in seen:
                continue
            blob, todo = [], [(x0, y0)]
            seen.add((x0, y0))
            while todo:
                x, y = todo.pop()
                blob.append((x, y))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if 0 <= yy < len(img) and 0 <= xx < len(row) and img[yy][xx] == 1 and (xx, yy) not in seen:
                            seen.add((xx, yy))
                            todo.append((xx, yy))
            if len(blob) <= n:
                for x, y in blob:
                    img[y][x] = 0


def _draw_small(img, x, y, s, color):
    for ch in s:
        for r, row in enumerate(_SMALL[ch]):
            for c, p in enumerate(row):
                if p == "1" and 0 <= y + r < len(img) and 0 <= x + c < len(img[0]):
                    img[y + r][x + c] = color
        x += 4


def render(key, blob: bytes) -> bytes:
    return render_ops(IMAGES[key], blob)


def render_ops(ops, blob: bytes) -> bytes:
    h, frames = image.decode(blob)
    for img in frames:
        for op in ops:
            if op[0] == "resize":
                w, hh, color = op[1:4]
                del img[hh:]
                for row in img:
                    del row[w:]
                    row.extend([color] * (w - len(row)))
                img.extend([[color] * w for _ in range(hh - len(img))])
                h = dict(h, w=w, h=hh)
            elif op[0] == "despeckle":
                _despeckle(img, op[1])
            elif op[0] == "clear":
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
            elif op[0] == "invert":
                x0, y0, x1, y1 = op[1:5]
                for y in range(y0, min(y1, len(img))):
                    for x in range(x0, min(x1, len(img[0]))):
                        if img[y][x] is not None:
                            img[y][x] ^= 1
    return image.encode(h, frames)


def _stone(*lines):
    ops = [("clear", 8, 7, 26, 24)]
    y = 15 - (6 * len(lines) - 1) // 2
    for ln in lines:
        ops.append(("small", 16 - small_width(ln) // 2, y, ln))
        y += 6
    return ops


# the four chime stones in the Mt. Heming cave spell 替天行道
for _key, _lines in {(8, 4, 32): ("FOR",), (8, 4, 33): ("HEA", "VEN"),
                     (8, 4, 34): ("UPH", "OLD"), (8, 4, 35): ("THE", "WAY")}.items():
    IMAGES[_key] = _stone(*_lines)

# images embedded in SRS effect resources: key -> {image number: ops}
SRS_IMAGES = {
    # the zooming 完 end card
    (5, 1, 4): {0: [("clear", 0, 0, 8, 9), ("small", 2, 2, "E")],
                1: [("clear", 0, 0, 12, 13), ("small", 1, 4, "END")],
                2: [("clear", 0, 0, 16, 16), ("ctext", 8, 2, "End", 1)],
                3: [("clear", 0, 0, 23, 25), ("ctext", 11, 1, "THE", 1), ("ctext", 11, 13, "END", 1)]},
    # boot logo animation (伏魔记 with lightning): image 2 is the 106x32 title
    (5, 1, 248): {2: [("clear", 0, 0, 106, 32), ("ctext", 53, 7, "Demonbane", 2)]},
}


def render_srs(key, blob: bytes, table: dict | None = None) -> bytes:
    """SRS: header (6), frame table (5 bytes per frame), then the images.
    `table` maps image number -> ops (default SRS_IMAGES[key])."""
    table = SRS_IMAGES[key] if table is None else table
    out = bytearray(blob[:6 + 5 * blob[2]])
    p = len(out)
    for i in range(blob[3]):
        h = image.header(blob[p:])
        rb = image._row_bytes(h["w"], h["mode"])
        n = 6 + rb * h["h"] * h["frames"]
        part = blob[p:p + n]
        if i in table:
            part = render_ops(table[i], part)          # a "resize" changes its length
        out += part
        p += n
    out += blob[p:]
    return bytes(out)


# shop signs in the town tilesets (16x16 tiles; black border, white inside)
def _sign(top: str, bottom: str):
    return [("clear", 2, 2, 14, 14), ("small", 8 - small_width(top) // 2, 3, top),
            ("small", 8 - small_width(bottom) // 2, 9, bottom)]


_SIGNS = {0: _sign("PA", "WN"), 1: _sign("AR", "MS"), 2: _sign("HE", "RB"),
          3: [("clear", 2, 2, 16, 14), ("text", 9, 2, "Inn", 1)],
          4: [("clear", 0, 2, 14, 14), ("text", 9 - 16, 2, "Inn", 1)],
          5: _sign("SH", "OP")}
TILE_FRAMES = {(7, 1, 1): {120 + i: ops for i, ops in _SIGNS.items()},
               (7, 1, 9): {80 + i: ops for i, ops in _SIGNS.items()}}


def render_frames(key, blob: bytes, table: dict | None = None) -> bytes:
    h, frames = image.decode(blob)
    for n, ops in (TILE_FRAMES[key] if table is None else table).items():
        one = image.encode(dict(h, frames=1), [frames[n]])
        frames[n] = image.decode(render_ops(ops, one))[1][0]
    return image.encode(h, frames)


def apply(res: dict, images: dict | None = None, srs: dict | None = None,
          tiles: dict | None = None) -> None:
    """Replace the translated images in an archive's resource dict, in place.
    The tables default to 伏魔记's (IMAGES, SRS_IMAGES, TILE_FRAMES)."""
    for key, ops in (IMAGES if images is None else images).items():
        if key in res:
            res[key] = render_ops(ops, res[key])
    for key, table in (SRS_IMAGES if srs is None else srs).items():
        if key in res:
            res[key] = render_srs(key, res[key], table)
    for key, table in (TILE_FRAMES if tiles is None else tiles).items():
        if key in res:
            res[key] = render_frames(key, res[key], table)
