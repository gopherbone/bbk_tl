"""English versions of 金庸群侠传's image resources that contain Chinese text.

Same op language as bbkrpg.images_en. The menus, save/load headers, battle
status window, level-up panels and death banner are byte-identical to
伏魔记's and reuse its ops. The martial-art banners in the skill animations
(SRS 2-62..2-80) are drawn from the translated MRS names, so they always
match the names in menus and battle.
"""

from __future__ import annotations

from . import images_en as en
from .images_en import small_width

# PIC resources shared with 伏魔记 (same bytes), plus the title menu
IMAGES = {k: en.IMAGES[k] for k in [(11, 2, 9), (11, 2, 10), (11, 2, 11), (11, 2, 13),
                                    (11, 2, 15), (11, 2, 16)]}
IMAGES[(11, 2, 14)] = [("clear", 10, 5, 102, 42), ("ctext", 52, 9, "New Game", 1),
                       ("ctext", 52, 25, "Continue", 1)]


# Calligraphy is kept as drawn; English is added in free space beside it.
# Title logo 金庸群侠传 / 之射雕英雄 (140x45): the lower left is empty, and a
# 5-row strip separates the title from the subtitle.
_LOGO = [("text", 3, 24, "Heroes of", 1), ("text", 3, 33, "Jin Yong", 1),
         ("small", 139 - small_width("THE CONDOR HEROES"), 25, "THE CONDOR HEROES")]

SRS_IMAGES = {
    # the zooming 完 end card: the last, largest frame gets "END" underneath
    (5, 1, 4): {3: [("resize", 23, 31, 0), ("small", 12 - small_width("END") // 2, 25, "END")]},
    # BOSS工作室 card (128x25, drawn at y 50): 11 more rows for "Studio" under
    # 工作室. Images 22-27 (步步高游戏站) are in no frame of this movie.
    (5, 1, 247): {21: [("resize", 128, 36, 0), ("ctext", 86, 23, "Studio", 1)]},
    (5, 1, 248): {2: _LOGO, 4: _LOGO},
}

# World map (SRS 1-8, shown by 查看 on the map item): each place is one hand-drawn
# hanzi joined by roads. Each glyph box is cleared and relabelled in 3x5 caps,
# two rows of up to 3 letters. glyph -> (box x0, y0, x1, y1)
MAP_GLYPHS = {
    "高": (3, 2, 16, 14), "玄": (93, 0, 105, 11), "雁": (118, 1, 139, 15), "龙": (143, 9, 158, 22),
    "灵": (31, 9, 41, 21), "恒": (69, 14, 83, 27), "丐": (106, 15, 120, 24), "京": (124, 22, 137, 35),
    "嵩": (90, 28, 104, 41), "西": (17, 24, 28, 35), "绝": (39, 23, 51, 36), "星": (3, 33, 17, 46),
    "青": (21, 44, 39, 54), "华": (54, 38, 67, 50), "武": (74, 44, 90, 58), "古": (110, 36, 128, 50),
    "扬": (145, 45, 158, 59), "虎": (3, 50, 15, 63), "百": (45, 53, 58, 64), "雪": (22, 58, 36, 68),
    "终": (106, 60, 122, 73), "血": (3, 67, 13, 78), "剑": (78, 67, 91, 80), "峨": (30, 75, 48, 87),
    "桃": (144, 73, 158, 86), "理": (59, 84, 73, 95), "逍": (100, 82, 118, 95),
}
# glyph -> label rows, from the glossary's place names (docs/jy/glossary.md)
MAP_LABELS: dict[str, tuple[str, ...]] = {
    "高": ("GAO",), "玄": ("TOR", "TSE"), "雁": ("YAN", "MEN"), "龙": ("DRA", "GON"),
    "灵": ("LIN", "JIU"), "恒": ("HENG",), "丐": ("BEG",), "京": ("CAP",),
    "嵩": ("SONG",), "西": ("XI", "XIA"), "绝": ("HRT", "BRK"), "星": ("STAR", "SEA"),
    "青": ("QING",), "华": ("HUA",), "武": ("WU", "DANG"), "古": ("OLD", "TOMB"),
    "扬": ("YANG",), "虎": ("TIG", "ER"), "百": ("FLWR",), "雪": ("SNOW",),
    "终": ("ZHO", "NAN"), "血": ("XUE", "DAO"), "剑": ("SWD", "TOMB"), "峨": ("EMEI",),
    "桃": ("PCH", "ISLE"), "理": ("DALI",), "逍": ("XIAO", "YAO"),
}


def _map_ops():
    ops = [("clear", *box) for g, box in MAP_GLYPHS.items() if g in MAP_LABELS]
    ops.append(("despeckle", 12))             # glyph strokes left outside the boxes
    for g, (x0, y0, x1, y1) in MAP_GLYPHS.items():
        lines = MAP_LABELS.get(g)
        if not lines:
            continue
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        y = cy - (6 * len(lines) - 1) // 2
        for ln in lines:
            ops.append(("small", cx - small_width(ln) // 2, y, ln))
            y += 6
    return ops


if MAP_LABELS:
    SRS_IMAGES[(5, 1, 8)] = {0: _map_ops(), 1: _map_ops()}

# martial-art name banners (60x15) in skill animations: (SRS key, image) -> MRS name row
BANNERS = {
    (5, 2, 62): {8: "MRS/4-1-1/name", 9: "MRS/4-2-1/name"},
    **{(5, 2, n): {4: "MRS/4-2-1/name", 5: "MRS/4-2-2/name", 6: "MRS/4-3-1/name", 7: "MRS/4-2-1/name"}
       for n in (63, 64, 65)},
    (5, 2, 66): {1: "MRS/4-1-2/name"}, (5, 2, 67): {2: "MRS/4-1-3/name"}, (5, 2, 68): {3: "MRS/4-1-4/name"},
    (5, 2, 69): {1: "MRS/4-1-5/name"}, (5, 2, 70): {4: "MRS/4-1-6/name"}, (5, 2, 71): {4: "MRS/4-1-7/name"},
    (5, 2, 72): {1: "MRS/4-1-8/name"}, (5, 2, 73): {3: "MRS/4-1-9/name"}, (5, 2, 74): {4: "MRS/4-1-10/name"},
    (5, 2, 75): {3: "MRS/4-1-11/name"}, (5, 2, 76): {1: "MRS/4-1-12/name"}, (5, 2, 77): {1: "MRS/4-1-13/name"},
    (5, 2, 78): {1: "MRS/4-1-14/name"}, (5, 2, 79): {1: "MRS/4-1-15/name"}, (5, 2, 80): {1: "MRS/4-1-16/name"},
}
BANNER_W = 58          # usable width inside the 60x15 banner


def banner(name: str):
    """Black text on a transparent ground: Sans when it fits, else 3x5 caps."""
    ops = [("clear", 0, 0, 60, 15, None)]
    if en.sans_width(name) <= BANNER_W:
        return ops + [("ctext", 30, 2, name, 1)]
    caps = name.upper()
    if small_width(caps) > BANNER_W or not all(c in en._SMALL or c == " " for c in caps):
        raise ValueError(f"banner text {name!r} does not fit {BANNER_W} px")
    return ops + [("small", 30 - small_width(caps) // 2, 5, caps)]


def _sign(top: str, bottom: str = ""):
    if not bottom:
        return [("clear", 2, 2, 14, 14), ("small", 8 - small_width(top) // 2, 6, top)]
    return [("clear", 2, 2, 14, 14), ("small", 8 - small_width(top) // 2, 3, top),
            ("small", 8 - small_width(bottom) // 2, 9, bottom)]


# shop-sign glyph tiles in the town tileset 7-1-1 (one hanzi per 16x16 tile);
# words: 打铁铺 IRON SMITH SHOP, 装备店 ARMOR GEAR SHOP, 杂货铺 MISC GOODS SHOP,
# 武器店 ARMS GEAR SHOP, 武馆 ARMS HALL, 镖局 ESCORT AGENCY, 药铺 HERB SHOP,
# 布庄 CLOTH SHOP, 客栈 GUEST HOUSE, 驿 POST, 当 PAWN, 商 TRADE, 门 GATE
_SIGNS = {2: _sign("SH", "OP"), 3: _sign("AR", "MOR"), 4: _sign("GE", "AR"), 5: _sign("ESC", "ORT"),
          6: _sign("AGE", "NCY"), 7: _sign("HE", "RB"), 8: _sign("GU", "EST"), 9: _sign("HO", "USE"),
          10: _sign("IR", "ON"), 11: _sign("SMI", "TH"), 12: _sign("SH", "OP"), 13: _sign("PA", "WN"),
          14: _sign("TR", "ADE"), 15: _sign("GA", "TE"), 16: _sign("HA", "LL"), 17: _sign("PO", "ST"),
          18: _sign("CL", "OTH"), 19: _sign("SH", "OP"), 118: _sign("MI", "SC"), 119: _sign("GO", "ODS"),
          120: _sign("AR", "MS"), 121: _sign("GE", "AR")}
TILE_FRAMES = {(7, 1, 1): _SIGNS, (7, 1, 9): en.TILE_FRAMES[(7, 1, 9)]}


def apply(res: dict, rows: list[dict]) -> None:
    en_by_id = {r["id"]: r.get("en") for r in rows}
    srs = dict(SRS_IMAGES)
    for key, table in BANNERS.items():
        ops = {i: banner(en_by_id[rid]) for i, rid in table.items() if en_by_id.get(rid)}
        if ops:
            srs[key] = ops
    en.apply(res, IMAGES, srs, TILE_FRAMES)
