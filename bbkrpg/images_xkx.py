"""English versions of 侠客行's image resources that contain Chinese text.

Same op language as bbkrpg.images_en. The engine is 伏魔记's (Ver1.3), and
the level-up panel, learned box, battle status window, Game Over banner and
save/load headers are byte-identical to 伏魔记's, so they reuse its ops.
Calligraphy (the 侠客行 boot logo, the brush-stroke intro, 剧终, the title's
vertical 侠客行) is kept as drawn, with English added beside it.
"""

from __future__ import annotations

from . import images_en as en
from .images_en import small_width

TITLE = "Ode to Gallantry"

# PIC resources shared with 伏魔记 (same bytes)
IMAGES = {k: en.IMAGES[k] for k in [(11, 2, 9), (11, 2, 10), (11, 2, 11), (11, 2, 13),
                                    (11, 2, 15), (11, 2, 16)]}

# title menu (159x96): four black bands at x 107..158, 22 px apart, white
# text: 踏入红尘 / 刻骨铭心 / 游戏介绍 / 开发小组
IMAGES[(11, 2, 14)] = [op for i, s in enumerate(["New Game", "Continue", "About", "Credits"])
                       for op in [("clear", 108, 11 + 22 * i, 158, 25 + 22 * i, 1),
                                  ("ctext", 133, 13 + 22 * i, s, 1, 0)]]


def _cell(x0, y0, word):
    """One 20x10 cell of the battle command cross, black 3x5 caps."""
    return [("clear", x0, y0, x0 + 20, y0 + 10), ("small", x0 + 10 - small_width(word) // 2, y0 + 3, word)]


# battle command cross (40x32, 4 frames, one cell inverted per frame, in
# this order): 攻击 up, 绝招 left, 其他 down, 合击 right
_CELLS = [(10, 0, "ATK"), (0, 10, "ARTS"), (10, 20, "MORE"), (20, 10, "COMBO")]


def _cross():
    """Frames differ only in which cell is inverted, so draw all four cells
    plain and let `apply` invert one per frame."""
    return [op for c in _CELLS for op in _cell(*c)]


# battle frames (159x96): 【忍者无敌】 at the top right, 我方队伍 at the bottom
# right; the 忍 stamps are decoration and stay
IMAGES[(11, 4, 1)] = [("clear", 98, 4, 156, 16), ("small", 127 - small_width("[PATIENCE WINS]") // 2, 8,
                                                     "[PATIENCE WINS]")]
IMAGES[(11, 4, 2)] = [("clear", 126, 70, 156, 93), ("small", 141 - small_width("OUR") // 2, 75, "OUR"),
                      ("small", 141 - small_width("PARTY") // 2, 83, "PARTY")]
# page headers (159x16): ×侠客正传× between corner ornaments, ===纯蓝工作室===
IMAGES[(11, 5, 1)] = [("clear", 22, 1, 137, 15), ("ctext", 79, 2, TITLE, 1)]
IMAGES[(11, 5, 2)] = [("clear", 30, 1, 130, 15), ("ctext", 80, 2, "Chunlan Studio", 1)]


def _icon(word: str):
    """Battle pop-up (14x14, transparent): a white strip with 3x5 caps."""
    return [("clear", 0, 0, 14, 14, None), ("clear", 0, 3, 14, 10),
            ("small", 7 - small_width(word) // 2, 4, word)]


def _forging(h: int):
    """打造中 on the forging animation's bottom bar (white on black); the
    dots after it animate and stay."""
    top = h - 16
    return [("clear", 12, top + 2, 50, top + 14, 1), ("text", 13, top + 3, "Forging", 1, 0)]


_FORGE_H = [96] * 10 + [48, 53, 56]
_BANNER = "CHUNLAN STUDIO: QUALITY GUARANTEED ^_^"

def _rows(x0, x1, y0, lines):
    """3x5 caps lines 6 px apart, centred between x0 and x1."""
    c = (x0 + x1) // 2
    return [("small", c - small_width(t) // 2, y0 + 6 * i, t) for i, t in enumerate(lines) if t]


# world map (158x96, SRS 5-1-6): a table of places and their map coordinates,
# split by lines at y 21 / 74 and x 48 / 111 into North, West, Central, East
# and South. Redrawn in 3x5 caps with the coordinates as "x,y".
_MAP = ([("clear", 0, 0, 158, 21), ("clear", 0, 22, 48, 74), ("clear", 49, 22, 111, 74),
         ("clear", 112, 22, 158, 74), ("clear", 0, 75, 158, 96)]
        + _rows(0, 158, 1, ["- NORTH -", "DEMON CULT 73,12   SECTS 17,62", "MATCHMAKER 49,71  ROCK HILL 59,38"])
        + _rows(0, 48, 24, ["- WEST -", "VILLAGE", "0,39", "NET CAFE", "65,42", "HERO SECT", "7,8", ""])
        + _rows(49, 111, 24, ["- CENTRAL -", "", "PHARMACY 20,41", "BEGGARS 37,32", "PAGODA 7,8", "PAWNSHOP 2,61"])
        + _rows(112, 158, 24, ["- EAST -", "MALL", "19,72", "SHENLONG", "15,39", "BIG FLOWER", "71,19"])
        + _rows(0, 158, 77, ["- SOUTH -", "HUASHAN 10,6   BRIGHT PEAK 40,1", "FLOWER BUSH 68,33"]))


def _sign(*rows):
    """A one-hanzi sign tile (16x16, framed): one or two rows of 3x5 caps."""
    ys = [6] if len(rows) == 1 else [3, 9]
    return [("clear", 2, 2, 14, 14)] + [("small", 8 - small_width(t) // 2, y, t) for y, t in zip(ys, rows)]


# Sign tiles in the town tileset (TIL 7-1-1), one hanzi each, spaced out
# along the facades. Several signs share a tile (帮 in 帮派 / 丐帮 / 神龙帮,
# 城 in 娱乐城 / 商城, 龙 in 神龙帮 / 龙门, 门 in 英雄门 / 龙门), so each tile
# gets a word that reads in all of them. 馆 also tiles the Japanese
# consulate's facade. 客栈 is adjacent: "Inn" spans both, as in 伏魔记.
_SIGNS = {
    34: _sign("PA", "WN"), 35: _sign("DO", "JO"), 36: _sign("HA", "LL"),
    37: en._SIGNS[3], 38: en._SIGNS[4],
    39: _sign("MAT", "CH"), 62: _sign("MAK", "ER"),
    63: _sign("GA", "NG"), 64: _sign("SE", "CT"), 65: _sign("THE"), 66: _sign("BRI", "GHT"),
    67: _sign("PE", "AK"), 68: _sign("DEM", "ON"), 69: _sign("CU", "LT"), 70: _sign("BEG", "GAR"),
    71: _sign("HUA"), 72: _sign("SH", "AN"), 73: _sign("HE", "RO"), 74: [("clear", 2, 2, 14, 14)],
    75: _sign("GA", "TE"), 76: _sign("SH", "EN"), 77: _sign("DRA", "GON"), 78: _sign("GA", "ME"),
    79: _sign("FUN"), 80: _sign("CI", "TY"), 81: _sign("NET"), 82: _sign("CA", "FE"),
    83: _sign("ME", "DS"), 84: _sign("SH", "OP"),
}
TILES = {(7, 1, 1): _SIGNS}


SRS_IMAGES = {
    # status pop-ups that float up in battle: 攻 防 速 毒 乱 封 眠
    **{(5, 1, 240 + i): {0: _icon(w)} for i, w in enumerate(["ATK", "DEF", "AGI", "PSN", "CNF", "SIL", "SLP"])},
    # forging animation: 13 frames with the bar, then 恭喜你 / 打造成功
    (5, 1, 3): {**{i: _forging(h) for i, h in enumerate(_FORGE_H)},
                13: [("clear", 30, 24, 68, 40), ("ctext", 49, 27, "Congrats!", 1),
                     ("clear", 29, 45, 69, 57), ("ctext", 49, 46, "Forged!", 1)]},
    # boot logo: the brush 侠客行 stays; BY纯蓝工作室 in the ellipse becomes
    # the English title, and the studio goes in the band under it
    (5, 1, 248): {0: [("clear", 36, 63, 124, 77, 1), ("ctext", 80, 64, TITLE, 1, 0),
                      ("clear", 44, 86, 116, 93, 1),
                      ("small", 80 - small_width("BY CHUNLAN STUDIO") // 2, 87, "BY CHUNLAN STUDIO", 0)]},
    (5, 1, 6): {0: _MAP},
    # 剧终 end card: the brush strokes stay, THE END under them
    (5, 1, 7): {0: [("clear", 12, 32, 50, 40), ("small", 31 - small_width("THE END") // 2, 34, "THE END")]},
    # 纯蓝出品，必属精品^_^ scrolling banner (159x10)
    **{(5, 1, 250 + i): {1: [("clear", 0, 0, 159, 10), ("small", 2, 3, _BANNER)]} for i in range(4)},
}


def apply(res: dict, rows: list[dict]) -> None:
    en.apply(res, IMAGES, SRS_IMAGES, TILES)
    # battle command cross: redraw each frame, then invert its highlighted cell
    key = (11, 2, 1)
    if key in res:
        from . import image
        h, frames = image.decode(res[key])
        out = []
        for f, (x0, y0, _) in enumerate(_CELLS[:len(frames)]):
            one = image.encode(dict(h, frames=1), [frames[f]])
            one = en.render_ops(_cross() + [("invert", x0, y0, x0 + 20, y0 + 10)], one)
            out.append(image.decode(one)[1][0])
        res[key] = image.encode(h, out)
