"""三国霸业 string table: export rows from dat.lib, encode translations back.

Row ids:
  e/<n>         resource 1 (engine strings, pstring.h order), n = item (1-based)
  s/<n>         resource 64 (STRING_CONST, sconst.h names)
  e/<n>#<k>, s/<n>#<k>   one fixed-width item of a packed menu/list string
  skill/<n>     resource 11 (4-byte skill names)       skilldesc/<n>  resource 12
  item/<n>      resource 73 (10-byte item names)        itemdesc/<n>   resource 74
  city/<n>      resource 58 (10-byte city names)
  name/<zh>     general names (resources 62, 70, 71, 72; one row per distinct name)

Every translated string keeps the byte length of the original (the game sizes
highlight bars, centres text and slices menus by byte count). English that
fits is stored inline and padded with the zero-width filler byte; longer
English goes into the text bank (resources 78-99) and the field holds a 2-byte
token plus filler. The pixel budget for a row is 6 px per original byte (the
original ASCII cell), unless a screen-specific budget is set in BUDGETS.
"""

from __future__ import annotations

import json
import re

from . import layout, render
from .lib import Lib, Resource

ENGINE, STRCONST = 1, 64
SKILL, SKILLDESC, ITEM, ITEMDESC, CITY = 11, 12, 73, 74, 58
NAMES = (62, 70, 71, 72)
FILL = bytes([render.FILL1])

# packed strings: (resource, item) -> item width in bytes
SPLIT = {
    (ENGINE, 7): 4, (ENGINE, 8): 4, (ENGINE, 9): 8, (ENGINE, 10): 4, (ENGINE, 11): 4, (ENGINE, 12): 4,
    (STRCONST, 37): 4, (STRCONST, 38): 4, (STRCONST, 39): 4, (STRCONST, 40): 4, (STRCONST, 46): 4,
    (STRCONST, 121): 8,
}

PREFIX = {ENGINE: "e", STRCONST: "s", SKILL: "skill", SKILLDESC: "skilldesc", ITEM: "item",
          ITEMDESC: "itemdesc", CITY: "city"}


def gb(b: bytes) -> str:
    return b.decode("gb2312", errors="backslashreplace")


def cstr(b: bytes) -> bytes:
    """Item content up to the first NUL (fixed-size fields)."""
    return b.split(b"\0", 1)[0]


def export(lib: Lib) -> list[dict]:
    rows = []
    for rid in (ENGINE, STRCONST):
        for i, it in enumerate(lib.res[rid].items, 1):
            body = cstr(it)
            w = SPLIT.get((rid, i))
            if w:
                for k in range(0, len(body), w):
                    rows.append({"id": f"{PREFIX[rid]}/{i}#{k // w}", "zh": gb(body[k:k + w]), "bytes": w})
            else:
                rows.append({"id": f"{PREFIX[rid]}/{i}", "zh": gb(body), "bytes": len(body)})
    for rid in (SKILL, SKILLDESC, ITEM, ITEMDESC, CITY):
        r = lib.res[rid]
        for i, it in enumerate(r.items, 1):
            body = cstr(it)
            if not body.strip(b"\0"):
                continue
            rows.append({"id": f"{PREFIX[rid]}/{i}", "zh": gb(body), "bytes": len(body), "field": r.item_len})
    seen = {}
    for rid in NAMES:
        r = lib.res[rid]
        for it in r.items:
            body = cstr(it)
            if body and body not in seen:
                seen[body] = True
                rows.append({"id": f"name/{gb(body)}", "zh": gb(body), "bytes": len(body), "field": r.item_len})
    for row in rows:
        spec(row)
    return rows


SPEECH_S = {95, 100, 101} | set(range(122, 149)) | set(range(153, 163))
SPEECH_E = set(range(39, 45))
MENUS = {("s", n) for n in (37, 38, 39, 40, 46, 121)} | {("e", n) for n in (8, 9, 10, 11)}
NAME_PX = 6 * render.NAME_COL         # officer list name column (61 px incl. the 1 px gap)
CITY_PX = 43                            # map side panel: x 114..157
# officer list column headers (s/24..s/36) and values shown in those columns
COLUMN_ROWS = {24 + i: layout.column_px(i) - 2 for i in range(13)}
COLUMN_ROWS.update({n: layout.column_px(8) - 2 for n in range(17, 23)})    # troop types
COLUMN_ROWS.update({n: layout.column_px(0) - 2 for n in (47, 48, 49)})     # Free / Ruler / Captive
COLUMN_ROWS[23] = 6 * render.NAME_COL - 2                                  # name header
# item list (ShowGoodsPro): name 10 cells, then usage 4, STR+/INT+/Move+/troop 6
COLUMN_ROWS.update({65: 58, 66: 22, 67: 34, 68: 34, 69: 34, 70: 34, 71: 22, 72: 22, 73: 34, 74: 34, 75: 34})
SPEECH_BOX = (90, 3)          # ShowGReport: x 62..151, three 12 px lines beside the portrait
MSG_W = 148                   # GamMsgBox: c_Sx = WK_SX + 5 .. c_Ex = WK_EX - 4


def spec(row: dict):
    """Fit spec: row["box"] = [width, lines] for wrapped text, else
    row["budget"] = single-line pixel width."""
    pre, _, rest = row["id"].partition("/")
    n = rest.split("#")[0]
    num = int(n) if n.isdigit() else None
    if (pre == "s" and num in SPEECH_S) or (pre == "e" and num in SPEECH_E):
        row["kind"], row["box"] = "speech", list(SPEECH_BOX)
    elif (pre, num) in MENUS and "#" in rest:
        row["kind"], row["budget"] = "menu", render.menu_px(row["bytes"]) - 2
    elif pre == "name":
        row["kind"], row["budget"] = "name", NAME_PX
    elif pre == "city":
        row["kind"], row["budget"] = "city", CITY_PX
    elif pre == "s" and num in COLUMN_ROWS:
        row["kind"], row["budget"] = "label", COLUMN_ROWS[num]
    elif pre == "item":
        row["kind"], row["budget"] = "item", layout.column_px(11) - 2
    elif pre == "skill":
        row["kind"], row["budget"] = "skill", render.menu_px(4) - 2
    elif pre in ("skilldesc", "itemdesc"):
        row["kind"], row["box"] = "desc", [MSG_W, max(1, -(-6 * row["bytes"] // MSG_W))]
    elif row["bytes"] >= 24 and any(ord(c) > 0x2e80 for c in row["zh"]):
        row["kind"], row["box"] = "msg", [MSG_W, max(1, -(-6 * row["bytes"] // MSG_W))]
    else:
        row["kind"], row["budget"] = "label", 6 * row["bytes"]


def wrap(en: str, w: int) -> list[str]:
    """Lines as the renderer word-wraps `en` in a w px box."""
    lines, cur = [], ""
    for para in en.split("\n"):
        cur = ""
        for word in para.split(" "):
            cand = word if not cur else cur + " " + word
            if width(cand) <= w or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def check(row: dict) -> str | None:
    """Problem with row["en"], or None."""
    en = row.get("en")
    if not en:
        return None
    try:
        en.encode("ascii")
    except UnicodeEncodeError:
        return "non-ASCII character"
    zf, ef = formats(row["zh"]), formats(en)
    if zf != ef:
        return f"format specifiers differ: {zf} vs {ef}"
    if "box" in row:
        w, n = row["box"]
        ls = wrap(en, w)
        if len(ls) > n or any(width(x) > w for x in ls):
            return f"needs {len(ls)} lines of {w}px (max {n}): {ls}"
    elif width(en) > row["budget"]:
        return f"{width(en)}px > {row['budget']}px"
    if len(en.encode()) > render.TOKEN_MAX and len(en.encode()) > row["bytes"]:
        return f"{len(en)} chars > {render.TOKEN_MAX} (bank limit)"
    return None


# --- encoding ---------------------------------------------------------------

class Bank:
    """Text-bank strings, deduplicated, in resources 78.. (255 items each)."""

    def __init__(self):
        self.items: list[bytes] = []
        self.index: dict[bytes, int] = {}

    def token(self, text: bytes) -> bytes:
        if len(text) > render.TOKEN_MAX:
            raise ValueError(f"bank string over {render.TOKEN_MAX} bytes: {text!r}")
        if text not in self.index:
            self.index[text] = len(self.items)
            self.items.append(text)
        n = self.index[text]
        res, item = divmod(n, 255)
        if res > render.TOKEN_HI - render.TOKEN_LO:
            raise ValueError("text bank full")
        return bytes([render.TOKEN_LO + res, item + 1])

    def resources(self, key: int = 0xC0) -> dict[int, Resource]:
        out = {}
        for r in range(0, len(self.items), 255):
            chunk = self.items[r:r + 255]
            rid = render.BANK_RES + r // 255
            out[rid] = Resource(rid, len(chunk), 0, key, 0, list(chunk))
        return out


def fit(en: str, nbytes: int, bank: Bank) -> bytes:
    """English for a field of exactly `nbytes` bytes (inline or token, padded)."""
    b = en.encode("ascii")
    if len(b) <= nbytes:
        return b + FILL * (nbytes - len(b))
    if nbytes < 2:
        raise ValueError(f"{en!r} does not fit in {nbytes} byte(s) and a token needs 2")
    return bank.token(b) + FILL * (nbytes - 2)


def width(en: str) -> int:
    """Pixel width of English drawn by the renderer (no trailing spacing).
    Control bytes (fillers, the month marker) take no width."""
    w = sum(render.advance(c) for c in en if " " <= c < "\x7f")
    return max(0, w - 1) if en else 0


def field_len(en: str, orig: int, field: int) -> int:
    """Stored length for English in a fixed-size field: at least the original
    length, and long enough that the game's 6 px-per-byte layouts (centring,
    highlight bars) reserve the English width; at most field - 1 (NUL)."""
    return max(orig, min(field - 1, -(-width(en) // 6)))


def apply(lib: Lib, rows: list[dict]) -> dict[int, Resource]:
    """Changed resources for a set of translated rows (rows without "en"
    keep the Chinese)."""
    import copy

    tr = {r["id"]: r["en"] for r in rows if r.get("en")}
    bank = Bank()
    changed: dict[int, Resource] = {}

    def res(rid):
        if rid not in changed:
            changed[rid] = copy.deepcopy(lib.res[rid])
        return changed[rid]

    for rid in (ENGINE, STRCONST):
        r = lib.res[rid]
        for i, it in enumerate(r.items, 1):
            body = cstr(it)
            w = SPLIT.get((rid, i))
            if w:
                parts = []
                any_tr = False
                for k in range(0, len(body), w):
                    rid_s = f"{PREFIX[rid]}/{i}#{k // w}"
                    if rid_s in tr:
                        any_tr = True
                        parts.append(fit(tr[rid_s], w, bank))
                    else:
                        parts.append(body[k:k + w])
                if any_tr:
                    res(rid).items[i - 1] = b"".join(parts) + it[len(body):]
            else:
                key = f"{PREFIX[rid]}/{i}"
                if key in tr:
                    res(rid).items[i - 1] = fit(tr[key], len(body), bank) + it[len(body):]
    for rid in (SKILL, SKILLDESC, ITEM, ITEMDESC, CITY):
        r = lib.res[rid]
        for i, it in enumerate(r.items, 1):
            key = f"{PREFIX[rid]}/{i}"
            if key in tr:
                body = cstr(it)
                n = field_len(tr[key], len(body), r.item_len) if rid in (ITEM, CITY) else len(body)
                enc = fit(tr[key], n, bank)
                res(rid).items[i - 1] = enc + b"\0" + it[len(enc) + 1:] if len(enc) >= len(body) else enc + it[len(body):]
    for rid in NAMES:
        r = lib.res[rid]
        for i, it in enumerate(r.items):
            body = cstr(it)
            key = f"name/{gb(body)}"
            if body and key in tr:
                # at most 6 bytes: the ruler list copies names into 6-byte slots
                enc = fit(tr[key], min(6, field_len(tr[key], len(body), r.item_len)), bank)
                res(rid).items[i] = enc + b"\0" + it[len(enc) + 1:] if len(enc) >= len(body) else enc + it[len(body):]
    changed.update(bank.resources())
    return changed


def load_rows(path: str) -> list[dict]:
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def save_rows(path: str, rows: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


_FMT = re.compile(r"%[-0-9]*[dsxuc]")


def formats(s: str) -> list[str]:
    return _FMT.findall(s)
