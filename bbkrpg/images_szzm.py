"""English versions of 十字之门's image resources that contain Chinese text.

Same op language as bbkrpg.images_en. The game ships English art of its own
(title menu, save/load headers, Game Over, The End, the CrossEntry logo), so
only the stat panels, the "learned" box, the field-skill banners and the
battle pop-ups need redrawing. Its panels are white on black, the reverse of
伏魔记's. The 十字之门 brush logo (SRS 5-1-248 image 2) is kept as drawn: the
English logo above it already names the game.
"""

from __future__ import annotations

from . import images_en as en
from .images_en import small_width

STATS = ["ATK", "DEF", "AGI", "PSN", "CNF", "SIL", "STN"]   # 攻 防 敏 毒 乱 封 晕

IMAGES = {
    # level-up panel (128x96): HP and MP are drawn in English already; the
    # five Chinese labels below them (攻击 防御 敏捷 精神 灵巧) sit 12 px apart.
    # The bottom rows start at x 11 to spare the corner ornament.
    (11, 2, 9): [("clear", 10, 30, 36, 86, 1), ("clear", 11, 86, 36, 90, 1)] + [
        ("text", 16, 33 + 12 * i, s, 1, 0) for i, s in enumerate(["Atk", "Def", "Agi", "Spi", "Dex"])],
    # learned-skill box (114x65): 学会 in the middle
    (11, 2, 10): [("clear", 40, 24, 74, 40), ("ctext", 57, 27, "Learned", 1)],
    # battle status window (120x72): 攻 under HP, 巧 and 敏 in the second
    # column, then the seven status counters 16 px apart
    (11, 2, 11): [
        ("clear", 33, 19, 49, 31, 1), ("small", 35, 22, "ATK", 0),
        ("clear", 72, 7, 88, 18, 1), ("small", 74, 10, "DEX", 0),
        ("clear", 72, 19, 88, 31, 1), ("small", 74, 22, "AGI", 0),
        ("clear", 5, 34, 116, 47, 1)] + [("small", 9 + 16 * i, 38, s, 0) for i, s in enumerate(STATS)],
}


def _banner(word: str):
    """Field-skill banner (70x27): icon on the left, the name white on black."""
    return [("clear", 27, 3, 68, 23, 1), ("ctext", 47, 9, word, 1, 0)]


def _icon(word: str, w: int):
    """Battle pop-up (13x13, transparent): a white strip with 3x5 caps."""
    return [("clear", 0, 0, w, 13, None), ("clear", 0, 3, w, 10),
            ("small", (w - small_width(word) + 1) // 2, 4, word)]


SRS_IMAGES = {
    # 点燃 挖掘 攀爬 击碎: the field skills
    **{(5, 1, 4 + i): {0: _banner(w)} for i, w in enumerate(["Ignite", "Dig", "Climb", "Smash"])},
    # status pop-ups that float up in battle
    **{(5, 1, 240 + i): {0: _icon(w, 12 if i == 6 else 13)} for i, w in enumerate(STATS)},
}


def apply(res: dict, rows: list[dict]) -> None:
    en.apply(res, IMAGES, SRS_IMAGES, {})
