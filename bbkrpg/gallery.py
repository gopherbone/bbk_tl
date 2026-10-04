"""QA gallery: a build whose opening script shows chosen strings one after
another, translated exactly as the real build translates them.

The opening script (1-1-1, run by New Game) is replaced by: the original
scene setup (map, hero), then one display command per requested row id,
copied from the row's original instruction with the translation applied
(say lines become their page tokens), and finally an idle loop. Each command
waits for a key like it does in the game, so a driver can screenshot, press
ENTER, and repeat.
"""

from __future__ import annotations

import copy

from . import gut as gutmod
from . import strings as strmod
from .lib import Lib, parse_key

OPENING = (1, 1, 1)
SETUP_OPS = {"loadmap", "createactor", "movie", "music", "createnpc"}


def _find(lib: Lib, rid: str):
    key_s, _, where = rid[4:].partition("@")
    addr_s, _, sub = where.partition(".")
    k = parse_key(key_s)
    g = gutmod.parse(lib.res[k])
    for i in g.code:
        if g.header_len + i.off == int(addr_s, 16):
            sidx = [n for n, kind in enumerate(i.kinds) if kind == "s"]
            return copy.deepcopy(i), sidx[int(sub) - 1 if sub else 0]
    raise KeyError(rid)


def script(orig: Lib, rows: dict[str, dict], ids: list[str], bank: list[bytes] | None) -> bytes:
    """Gallery opening script for `ids` (gut row ids)."""
    g = gutmod.parse(orig.res[OPENING])
    code = []
    for i in g.code:                       # scene setup up to the first line of text
        if i.name in strmod.STRING_KINDS:
            if code:
                break
            continue
        if i.name in SETUP_OPS:
            code.append(i)
    for rid in ids:
        base = rid.split(".")[0] if "@" in rid and "." in rid.split("@")[1] else rid
        i, _ = _find(orig, rid)
        sidx = [n for n, kind in enumerate(i.kinds) if kind == "s"]
        extra = []
        for sn, argn in enumerate(sidx):            # translate every string of the command
            r = rows.get(base + (f".{sn + 1}" if len(sidx) > 1 else ""), {})
            en = r.get("en")
            if en:
                value = en if (bank is not None and r.get("kind") in ("say", "message", "showgut")) else strmod.encode_en(en)
                extra += strmod.translate_instr(i, argn, value, bank)
        code += [i] + extra
    idle = gutmod.Instr(0, gutmod.BY_NAME["goto"][0], [0], b"")
    code.append(idle)
    # lay out, then point every jump at the next instruction (the idle loop jumps to itself)
    out = gutmod.Gut(g.type, g.index, g.desc, [], code)
    hl = out.header_len
    addrs, pos = [], hl
    for i in code:
        addrs.append(pos)
        pos += len(gutmod.encode_instr(i.op, [0 if k == "a" else v for k, v in zip(i.kinds, i.args)]))
    for n, i in enumerate(code):
        nxt = addrs[n + 1] if n + 1 < len(code) else addrs[n]
        i.args = [nxt if k == "a" else v for k, v in zip(i.kinds, i.args)]
    return gutmod.build(out)
