"""Translation string table: export every translatable string from an archive
to JSONL rows, and import translated rows back into a copy of the archive.

Import always starts from the original (Chinese) archive, so row ids are
stable: they name the resource and the string's original address.

Row ids
  gut/<key>@<addr>[.<n>]   script string; addr is the instruction's original
                           script address, n = operand number when a command
                           carries more than one string (choice)
  <TYPE>/<key>/<field>     fixed-width field in a record (GRS/MRS/ARS/MAP)
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from . import fit, fontpatch
from . import gut as gutmod
from .lib import Key, Lib, key_str, parse_key


@dataclass(frozen=True)
class Field:
    res_type: int
    subtypes: frozenset | None
    offset: int
    size: int
    name: str
    tag: str


# Field spans run to the next field the engine reads (BBKRPGSimulator).
FIELDS = [
    Field(6, None, 0x06, 0x0c, "name", "GRS"),
    Field(6, None, 0x1e, 0x66, "desc", "GRS"),
    Field(4, None, 0x06, 0x14, "name", "MRS"),
    Field(4, None, 0x1a, 0x56, "desc", "MRS"),
    Field(3, frozenset({1}), 0x0a, 0x0c, "name", "ARS"),       # player
    Field(3, frozenset({2, 4}), 0x09, 0x0c, "name", "ARS"),    # npc, scene object
    Field(3, frozenset({3}), 0x06, 0x0c, "name", "ARS"),       # monster
    Field(2, None, 0x03, 0x0d, "name", "MAP"),
]

STRING_KINDS = {"say", "choice", "message", "setscenename", "showgut", "menu", "timemsg"}


def _field_text(raw: bytes) -> bytes:
    return raw.split(b"\0", 1)[0]


def fields_for(k: Key) -> list[Field]:
    return [f for f in FIELDS if f.res_type == k[0] and (f.subtypes is None or k[1] in f.subtypes)]


def export(lib: Lib) -> list[dict]:
    rows: list[dict] = []
    map_names = {}
    for k in lib.keys_of(2):
        map_names[k] = gutmod.bytes_to_text(_field_text(lib.res[k][0x03:0x10]))

    for k in lib.keys_of(1):
        g = gutmod.parse(lib.res[k])
        hl = g.header_len
        scene = None
        script_rows: list[dict] = []
        for i in g.code:
            if i.name == "loadmap":
                scene = map_names.get((2, i.args[0], i.args[1]), scene)
            if i.name not in STRING_KINDS:
                continue
            addr = hl + i.off
            strs = [(n, v) for n, (kind, v) in enumerate(zip(i.kinds, i.args)) if kind == "s"]
            for sn, (argn, v) in enumerate(strs):
                rid = f"gut/{key_str(k)}@{addr:04x}" + (f".{sn + 1}" if len(strs) > 1 else "")
                ctx: dict = {"scene": scene}
                limits: dict = {"max_bytes": None}
                if i.name == "say":
                    ctx["pic"] = i.args[0]
                    limits.update(box="say", portrait=bool(i.args[0]))
                elif i.name == "choice":
                    limits.update(box="choice", max_bytes=19)   # 8 px per byte, 160 px wide frame
                elif i.name == "showgut":
                    limits.update(box="scroll", cols=20)
                elif i.name == "menu":
                    limits.update(box="menu", sep=" ")
                elif i.name == "setscenename":
                    limits.update(box="scenename")
                if i.name == "setscenename":
                    scene = gutmod.bytes_to_text(v)
                script_rows.append({
                    "id": rid, "kind": i.name, "zh": gutmod.bytes_to_text(v), "en": "",
                    "ctx": ctx, "limits": limits, "status": "todo", "note": "",
                })
        for n, r in enumerate(script_rows):
            r["prev"] = script_rows[n - 1]["id"] if n else None
            r["next"] = script_rows[n + 1]["id"] if n + 1 < len(script_rows) else None
        rows += script_rows

    for t in (6, 4, 3, 2):
        for k in lib.keys_of(t):
            blob = lib.res[k]
            for f in fields_for(k):
                text = _field_text(blob[f.offset:f.offset + f.size])
                if not text:
                    continue
                rows.append({
                    "id": f"{f.tag}/{key_str(k)}/{f.name}", "kind": f"{f.tag.lower()}.{f.name}",
                    "zh": gutmod.bytes_to_text(text), "en": "", "ctx": {},
                    "limits": {"max_bytes": f.size - 1 if f.name == "name" else f.size},
                    "status": "todo", "note": "",
                })
    return rows


def write_jsonl(rows: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


class ImportError_(Exception):
    pass


def encode_en(s: str) -> bytes:
    """English text -> bytes. Escapes (\\xNN) pass through like the listing."""
    return gutmod.text_to_bytes(s)


def translate_instr(i, argn: int, value, bank: list[bytes] | None) -> list:
    """Put a translation into string operand `argn` of instruction `i`.
    `value` is bytes (written as is) or, for a `say` with a text bank, the
    English text, which is fitted into pages: `i` gets the first page token
    and the extra `say`s for the other pages are returned (insert them after
    `i`)."""
    if not isinstance(value, str):
        i.args[argn] = value
        return []
    if i.name == "showgut":                 # the engine lays the scroll out 20 bytes per row
        i.args[argn] = fit.scroll_bytes(value)
        return []
    if i.name == "message":                 # one box, rows from the bank
        bank.append("\n".join(fit.rows(value, fit.MESSAGE_WIDTH)).encode("ascii"))
        n = len(bank) - 1
        i.args[argn] = bytes([0xFE, 0x80 | n >> 7, 0xFE, 0x80 | n & 0x7F])
        return []
    ps = fit.pages(value, portrait=bool(i.args[0]))
    toks = []
    for page in ps:
        bank.append("\n".join(page).encode("ascii"))
        toks.append(fontpatch.token(len(bank) - 1))
    i.args[argn] = toks[0]
    extra = []
    for t in toks[1:]:
        args = list(i.args)
        args[argn] = t
        extra.append(gutmod.Instr(0, i.op, args, b""))
    return extra


def apply(lib: Lib, rows: list[dict], bank: list[bytes] | None = None) -> tuple[Lib, list[str]]:
    """Return a new Lib with every row that has `en` applied, plus problems.
    Problems are fatal for that row only; the original text stays.

    With `bank` (a list to fill), `say` lines are fitted into pages for the
    patched renderer (fontpatch): each page becomes its own `say` carrying a
    page token, and the page text is appended to `bank`."""
    problems: list[str] = []
    res = dict(lib.res)
    gut_rows: dict[Key, dict[str, bytes]] = {}
    for r in rows:
        if not r.get("en"):
            continue
        rid = r["id"]
        try:
            data = encode_en(r["en"])
        except gutmod.GutError as e:
            problems.append(f"{rid}: {e}")
            continue
        if b"\0" in data:
            problems.append(f"{rid}: contains NUL")
            continue
        if rid.startswith("gut/"):
            key_s, _, where = rid[4:].partition("@")
            gut_rows.setdefault(parse_key(key_s), {})[where] = (
                r["en"] if bank is not None and r["kind"] in ("say", "message", "showgut") else data)
            continue
        tag, key_s, fname = rid.split("/")
        k = parse_key(key_s)
        if k not in res:
            problems.append(f"{rid}: no such resource")
            continue
        fs = [f for f in fields_for(k) if f.name == fname and f.tag == tag]
        if not fs:
            problems.append(f"{rid}: unknown field")
            continue
        f = fs[0]
        cap = f.size - 1 if f.name == "name" else f.size
        if f.name == "desc" and bank is not None:     # wrapped rows in the bank, token in the record
            rws = fit.rows(r["en"], fit.DESC_WIDTH)
            if len(rws) > fit.DESC_ROWS:
                problems.append(f"{rid}: {len(rws)} rows, the window shows {fit.DESC_ROWS}")
                continue
            bank.append("\n".join(rws).encode("ascii"))
            data = fontpatch.token(len(bank) - 1)
        if len(data) > cap:
            problems.append(f"{rid}: {len(data)} bytes, field holds {cap}")
            continue
        blob = bytearray(res[k])
        span = data + (b"\0" if len(data) < f.size else b"")
        blob[f.offset:f.offset + len(span)] = span
        res[k] = bytes(blob)

    for k, repl in gut_rows.items():
        if k not in res:
            problems.append(f"gut/{key_str(k)}: no such script")
            continue
        g = gutmod.parse(lib.res[k])
        targets = gutmod.target_map(g)
        hl = g.header_len
        code: list = []
        new_index: dict[int, int] = {}
        for n, i in enumerate(g.code):
            new_index[n] = len(code)
            addr = f"{hl + i.off:04x}"
            sidx = [m for m, kind in enumerate(i.kinds) if kind == "s"]
            extra: list = []
            for sn, argn in enumerate(sidx):
                tag = addr + (f".{sn + 1}" if len(sidx) > 1 else "")
                if tag not in repl:
                    continue
                extra += translate_instr(i, argn, repl.pop(tag), bank)
            code.append(i)
            code += extra
        new_index[len(g.code)] = len(code)
        for tag in repl:
            problems.append(f"gut/{key_str(k)}@{tag}: no string at that address")
        g.code = code
        targets = {a: new_index[ix] for a, ix in targets.items()}
        try:
            res[k] = gutmod.build(g, targets)
        except gutmod.GutError as e:
            problems.append(f"gut/{key_str(k)}: {e}")
    out = Lib(lib.head, lib.banks, lib.order, res, lib.tail)
    return out, problems
