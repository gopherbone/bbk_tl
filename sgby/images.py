"""English for the 三国霸业 pictures that carry Chinese.

Calligraphy (the 三国霸业 logo, the four title buttons, the hand-lettered
credits) is kept as drawn; English is added beside it in a 5-px small-caps
font on a band that reads as part of the frame. Plain-font labels (the period
cards' side panels, the battle status bar) are replaced.

Ops work on pixel rows (1 = black) of a picture frame:
  ("fill", x0, y0, x1, y1, color)      fill [x0,x1) x [y0,y1)
  ("small", x, y, text, color)         5-px caps at (x, y) = top-left
  ("csmall", cx, y, text, color)       centred on cx
  ("sans", x, y, text, color)          bbk_tl Sans (11 rows from y)
  ("csans", cx, y, text, color)
"""

from __future__ import annotations

from bbkrpg import font_sans

from . import pic
from .lib import Lib, Resource

# proportional 5-px caps (rows top to bottom; '1' = ink)
SMALL = {
    "A": ["010", "101", "111", "101", "101"], "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"], "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"], "F": ["111", "100", "110", "100", "100"],
    "G": ["011", "100", "101", "101", "011"], "H": ["101", "101", "111", "101", "101"],
    "I": ["1", "1", "1", "1", "1"], "J": ["001", "001", "001", "101", "010"],
    "K": ["101", "101", "110", "101", "101"], "L": ["100", "100", "100", "100", "111"],
    "M": ["10001", "11011", "10101", "10001", "10001"], "N": ["1001", "1101", "1011", "1001", "1001"],
    "O": ["010", "101", "101", "101", "010"], "P": ["110", "101", "110", "100", "100"],
    "Q": ["010", "101", "101", "110", "011"], "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"], "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"], "V": ["101", "101", "101", "101", "010"],
    "W": ["10001", "10001", "10101", "11011", "10001"], "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"], "Z": ["111", "001", "010", "100", "111"],
    " ": ["00", "00", "00", "00", "00"], ":": ["0", "1", "0", "1", "0"], "-": ["00", "00", "11", "00", "00"],
    "'": ["1", "1", "0", "0", "0"], ".": ["0", "0", "0", "0", "1"], ",": ["0", "0", "0", "1", "1"],
    "0": ["010", "101", "101", "101", "010"], "1": ["01", "11", "01", "01", "01"],
    "2": ["110", "001", "010", "100", "111"], "3": ["110", "001", "010", "001", "110"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "110", "001", "110"],
    "6": ["011", "100", "110", "101", "010"], "7": ["111", "001", "010", "010", "010"],
    "8": ["010", "101", "010", "101", "010"], "9": ["010", "101", "011", "001", "110"],
}


def small_width(s: str) -> int:
    return sum(len(SMALL[c][0]) + 1 for c in s) - 1 if s else 0


def sans_width(s: str) -> int:
    return sum(font_sans.width(c) + 1 for c in s) - 1 if s else 0


def _put(img, x, y, color):
    if 0 <= y < len(img) and 0 <= x < len(img[0]):
        img[y][x] = color


def draw_small(img, x, y, s, color):
    for ch in s:
        g = SMALL[ch]
        for r, row in enumerate(g):
            for c, p in enumerate(row):
                if p == "1":
                    _put(img, x + c, y + r, color)
        x += len(g[0]) + 1


def draw_sans(img, x, y, s, color):
    for ch in s:
        g = font_sans.GLYPHS[ch]
        for r, row in enumerate(g):
            for c, p in enumerate(row):
                if p == "#":
                    _put(img, x + c, y + r, color)
        x += font_sans.width(ch) + 1


def run_ops(img, ops, dx=0, dy=0):
    """Apply ops to a frame; (dx, dy) shifts op coordinates (for sprites
    cut out of a background)."""
    for op in ops:
        k = op[0]
        if k == "fill":
            x0, y0, x1, y1, color = op[1:]
            for y in range(y0 + dy, y1 + dy):
                for x in range(x0 + dx, x1 + dx):
                    _put(img, x, y, color)
        elif k in ("small", "csmall"):
            x, y, s, color = op[1:]
            if k == "csmall":
                x -= small_width(s) // 2
            draw_small(img, x + dx, y + dy, s, color)
        elif k in ("sans", "csans"):
            x, y, s, color = op[1:]
            if k == "csans":
                x -= sans_width(s) // 2
            draw_sans(img, x + dx, y + dy, s, color)
        else:
            raise ValueError(op)


def check_clear(rows, ops, dx=0, dy=0):
    """Text ops must land on blank pixels (1 px margin): no art is overdrawn."""
    for op in ops:
        if op[0] in ("small", "csmall"):
            x, y, t, color = op[1:]
            w = small_width(t)
            if op[0] == "csmall":
                x -= w // 2
            x, y = x + dx, y + dy
            ink = 1 - color
            for yy in range(y - 1, y + 6):
                for xx in range(x - 1, x + w + 1):
                    if 0 <= yy < len(rows) and 0 <= xx < len(rows[0]) and rows[yy][xx] != ink:
                        raise ValueError(f"{t!r} at ({x},{y}) overlaps art at ({xx},{yy})")


def edit_picture(blob: bytes, off: int, ops, dx=0, dy=0, clear=False) -> bytes:
    """Return blob with the picture at `off` edited (every frame, data plane)."""
    p = pic.parse(blob, off)
    fr = pic.frames(blob, off)
    new = []
    for planes in fr:
        rows = pic.to_rows(planes[0], p["w"], p["h"])
        if clear:
            check_clear(rows, ops, dx, dy)
        run_ops(rows, ops, dx, dy)
        new.append([pic.from_rows(rows, p["w"], p["h"])] + planes[1:])
    rebuilt = pic.build(p["w"], p["h"], p["mask"], new)
    return blob[:off] + rebuilt + blob[off + p["len"]:]


def spe_pictures(blob: bytes) -> list[int]:
    """Offsets of the pictures in an SPE animation resource."""
    cnt, pm = blob[2], blob[3]
    off, out = 6 + 5 * cnt, []
    for _ in range(pm):
        out.append(off)
        off += pic.parse(blob, off)["len"]
    return out


def spe_units(blob: bytes) -> list[tuple[int, int]]:
    """(x, y) of each SPE frame record."""
    cnt = blob[2]
    return [(blob[6 + 5 * i], blob[7 + 5 * i]) for i in range(cnt)]


# --- the edits ---------------------------------------------------------------

TITLE_BUTTONS = [(6, 44, "NEW GAME"), (83, 44, "LOAD GAME"), (6, 69, "CREDITS"), (83, 69, "QUIT")]
BUTTON_W, BUTTON_H = 69, 19


def _title_ops():
    ops = [("fill", 27, 35, 134, 43, 1), ("csmall", 80, 37, "THREE KINGDOMS: HEGEMONY", 0)]
    for x, y, label in TITLE_BUTTONS:
        y1 = y + BUTTON_H
        ops += [("fill", x, y1, x + BUTTON_W, y1 + 5, 1), ("csmall", x + BUTTON_W // 2, y1, label, 0)]
    return ops


# period cards: picture at (x, y) on the background, 78x33; side panel x 55..77
PERIODS = [
    ((1, 25), ["DONG", "ZHUO", "TAKES", "POWER"]),
    ((1, 61), ["RISE", "OF", "CAO", "CAO"]),
    ((81, 25), ["BATTLE", "OF RED", "CLIFFS"]),
    ((81, 61), ["THREE", "KING-", "DOMS"]),
]
PANEL_X0, PANEL_X1 = 54, 78


def _period_ops(lines):
    ops = [("fill", PANEL_X0, 1, PANEL_X1, 32, 1)]
    top = 1 + (31 - (6 * len(lines) - 1)) // 2
    cx = (PANEL_X0 + PANEL_X1) // 2
    for i, s in enumerate(lines):
        ops.append(("csmall", cx, top + 6 * i, s, 0))
    return ops


# credits scroll (resource 6, an unrolling SPE of one 159x96 picture): small
# captions in the blank rows under the hand-lettered labels and names
CREDITS_OPS = [
    ("small", 13, 38, "CODE", 1),
    ("small", 98, 23, "ALL-", 1),
    ("small", 98, 29, "NIGHTER", 1),
    ("small", 66, 54, "SOUTH IMP", 1),
    ("small", 18, 74, "ART", 1),
]


def apply(lib: Lib, changed: dict[int, Resource]):
    """Add the edited picture resources to `changed`."""
    import copy

    def res(rid):
        if rid not in changed:
            changed[rid] = copy.deepcopy(lib.res[rid])
        return changed[rid]

    # battle status bar: [粮 food][天 weather][? info] -> [Food food][weather][? info]
    r = res(8)
    r.items[0] = edit_picture(r.items[0], 0, [
        ("fill", 1, 1, 60, 15, 0), ("sans", 2, 3, "Food", 1), ("fill", 43, 1, 44, 15, 1)])
    # battle day counter box: 第 [n] 天 -> "Day [n]"
    r = res(33)
    r.items[0] = edit_picture(r.items[0], 0, [("fill", 2, 2, 42, 19, 0), ("sans", 3, 5, "Day", 1)])
    r = res(6)
    blob = r.items[0]
    for off in spe_pictures(blob):
        blob = edit_picture(blob, off, CREDITS_OPS, clear=True)
    r.items[0] = blob
    # title background and the four blinking button sprites
    r = res(44)
    r.items[0] = edit_picture(r.items[0], 0, _title_ops())
    # period background: card side panels
    r = res(45)
    blob = r.items[0]
    for (x, y), lines in PERIODS:
        blob = edit_picture(blob, 0, _period_ops(lines), dx=x, dy=y)
    r.items[0] = blob
    # period card sprites (two jiggle frames, same picture)
    for i, rid in enumerate(range(104, 108)):
        r = res(rid)
        blob = r.items[0]
        lines = PERIODS[i][1]                    # 104..107 are drawn at PERIODS' positions
        for off in spe_pictures(blob):
            blob = edit_picture(blob, off, _period_ops(lines))
        r.items[0] = blob
