"""English versions of 英雄坛说's image resources that contain Chinese text.

Same op language as bbkrpg.images_en. The engine is 伏魔记's (Ver1.3, same
code), and the menus, save/load headers, battle status window, level-up
panels and death banner are byte-identical to 伏魔记's, so they reuse its ops.
There are no shop signs in the tilesets.
"""

from __future__ import annotations

from . import images_en as en
from .images_en import small_width

TITLE = "Heroes' Altar"

# PIC resources shared with 伏魔记 (same bytes), plus the title menu
IMAGES = {k: en.IMAGES[k] for k in [(11, 2, 9), (11, 2, 10), (11, 2, 11), (11, 2, 13),
                                    (11, 2, 15), (11, 2, 16)]}
# title menu (105x90): white-on-black header band, then 4 items 16 px apart
# whose glyphs span x 6..70: 初出茅庐 / 再现江湖 / 开发群 / 游戏声明
IMAGES[(11, 2, 14)] = [("clear", 2, 2, 103, 20, 1), ("ctext", 52, 5, TITLE, 1, 0),
                       ("clear", 2, 22, 103, 88)] + [
    ("ctext", 38, 25 + 16 * i, s, 1) for i, s in enumerate(["New Game", "Continue", "Credits", "Notice"])]


def _icon(word: str):
    """Battle pop-up (14x14, transparent): a white strip with 3x5 caps."""
    return [("clear", 0, 0, 14, 14, None), ("clear", 0, 3, 14, 10),
            ("small", 7 - small_width(word) // 2, 4, word)]


# Calligraphy is kept as drawn; English is added in free space beside it.
SRS_IMAGES = {
    # status pop-ups that float up in battle: 攻 防 速 毒 乱 封 眠
    **{(5, 1, 3 + i): {0: _icon(w)} for i, w in enumerate(["ATK", "DEF", "AGI", "PSN", "CNF", "SIL", "SLP"])},
    # boot logo: four 20x19 brush glyphs at x 32, 57, 82, 107 (y 38), drawn in
    # order, so the first (英) grows to span all four and carries the English
    # under them; the later glyphs draw over its top rows.
    (5, 1, 248): {0: [("resize", 97, 31, 0), ("ctext", 48, 20, TITLE, 1)]},
    # 神童乐园 card (96x24, drawn at 30,6): 12 more rows for the English
    (5, 1, 247): {1: [("resize", 96, 36, 0), ("ctext", 48, 24, "Prodigy Park", 1)]},
}


def apply(res: dict, rows: list[dict]) -> None:
    en.apply(res, IMAGES, SRS_IMAGES, {})
