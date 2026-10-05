"""Layout data changes in dat.lib (not code): officer list column widths.

Resource 2 (IFACE_CONID) item 7 holds the officer list's column widths in
6 px units, in property order: faction, location, level, war, intelligence,
loyalty, EXP, stamina, troop type, troops, age, item 1, item 2. The name
column itself is a code constant (sgby.render.NAME_COL).
"""

from __future__ import annotations

import copy

from .lib import Lib, Resource

ORIG = bytes([8, 10, 4, 4, 4, 4, 4, 4, 4, 5, 4, 10, 10])
COLUMNS = bytes([11, 9, 5, 4, 4, 6, 4, 6, 7, 5, 4, 10, 10])
HEADER_FIRST = 24          # s/24.. are the column headers (s/23 the name header)
# ShowPersonControl keeps the start of each horizontal page in U8 spcv[7], so
# the columns must pack into at most 7 pages. A page holds 148 px of columns
# (6 * width + 1 each), name column included (sgby.render.NAME_COL).
LIST_PX = 148
MAX_PAGES = 7


def pages(name_col: int, cols: bytes = None) -> list[list[int]]:
    cols = COLUMNS if cols is None else cols
    out, cur, used = [], [], 6 * name_col + 1
    for i, w in enumerate(cols):
        px = 6 * w + 1
        if cur and used + px > LIST_PX:
            out.append(cur)
            cur, used = [], 6 * name_col + 1
        cur.append(i)
        used += px
    out.append(cur)
    return out


def apply(lib: Lib, changed: dict[int, Resource]):
    from .render import NAME_COL
    assert len(pages(NAME_COL)) <= MAX_PAGES, pages(NAME_COL)
    r = changed.get(2) or copy.deepcopy(lib.res[2])
    assert r.items[7] == ORIG
    r.items[7] = COLUMNS
    changed[2] = r


def column_px(i: int) -> int:
    return 6 * COLUMNS[i]
