"""GUT (story script) resources: decode, disassemble to a listing, assemble back.

Resource layout:
  0x00  u8 type, 0x01 u8 index
  0x02  description, GB2312, NUL-padded to 0x18
  0x18  u16 LE length L, counted from 0x18 to the end of the resource
  0x1a  u8 n = number of scene events
  0x1b  n x u16 LE event entry addresses (0 = unused)
  ...   code, L - 2n - 3 bytes

Script addresses (event entries and jump operands) count from offset 0x18, so
code offset c has address 2n + 3 + c.

Operand layouts come from BBKRPGSimulator's command classes, with two fixes:
DeleteGoods reads its jump target at operand offset 4 (the C# port reads 2),
and EnterFight's last two words are jump targets (loss, win; 0 = none).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Operand kinds: w = u16, d = u32, a = jump address (u16), s = text string,
# z = NUL-terminated byte list that is not text (shop goods list).
OPS: dict[int, tuple[str, str]] = {
    0x00: ("music", "ww"),
    0x01: ("loadmap", "wwww"),
    0x02: ("createactor", "www"),
    0x03: ("deletenpc", "w"),
    0x06: ("move", "www"),
    0x09: ("callback", ""),
    0x0a: ("goto", "a"),
    0x0b: ("if", "wa"),
    0x0c: ("set", "ww"),
    0x0d: ("say", "ws"),
    0x0e: ("startchapter", "ww"),
    0x10: ("screenset", "ww"),
    0x14: ("gameover", ""),
    0x15: ("ifcmp", "wwa"),
    0x16: ("add", "ww"),
    0x17: ("sub", "ww"),
    0x18: ("setcontrolid", "w"),
    0x1a: ("setevent", "w"),
    0x1b: ("clrevent", "w"),
    0x1c: ("buy", "z"),
    0x1d: ("facetoface", "ww"),
    0x1e: ("movie", "wwwww"),
    0x1f: ("choice", "ssa"),
    0x20: ("createbox", "wwww"),
    0x21: ("deletebox", "w"),
    0x22: ("gaingoods", "ww"),
    0x23: ("initfight", "wwwwwwwwwww"),
    0x24: ("fightenable", ""),
    0x25: ("fightdisable", ""),
    0x26: ("createnpc", "wwww"),
    0x27: ("enterfight", "wwwwwwwwwwwww" + "aa"),
    0x28: ("deleteactor", "w"),
    0x29: ("gainmoney", "d"),
    0x2a: ("usemoney", "d"),
    0x2b: ("setmoney", "d"),
    0x2c: ("learnmagic", "www"),
    0x2d: ("sale", ""),
    0x2e: ("npcmovemod", "ww"),
    0x2f: ("message", "s"),
    0x30: ("deletegoods", "wwa"),
    0x31: ("resumeactorhp", "ww"),
    0x32: ("actorlayerup", "ww"),
    0x33: ("boxopen", "w"),
    0x34: ("delallnpc", ""),
    0x35: ("npcstep", "www"),
    0x36: ("setscenename", "s"),
    0x37: ("showscenename", ""),
    0x38: ("showscreen", ""),
    0x39: ("usegoods", "wwa"),
    0x3a: ("attribtest", "wwwaa"),
    0x3b: ("attribset", "www"),
    0x3c: ("attribadd", "www"),
    0x3d: ("showgut", "wws"),
    0x3e: ("usegoodsnum", "wwwa"),
    0x3f: ("randrade", "wa"),
    0x40: ("menu", "ws"),
    0x41: ("testmoney", "da"),
    0x42: ("callchapter", "ww"),
    0x43: ("discmp", "wwaa"),
    0x44: ("return", ""),
    0x45: ("timemsg", "ws"),
    0x46: ("disablesave", ""),
    0x47: ("enablesave", ""),
    0x48: ("gamesave", ""),
    0x49: ("seteventtimer", "ww"),
    0x4a: ("enableshowpos", ""),
    0x4b: ("disableshowpos", ""),
    0x4c: ("setto", "ww"),
    0x4d: ("testgoodsnum", "wwwaa"),
    0x4e: ("setfightmiss", "w"),
    0x4f: ("setarmstoss", "w"),
}
BY_NAME = {name: (op, kinds) for op, (name, kinds) in OPS.items()}

DESC_LEN = 0x16


class GutError(Exception):
    pass


@dataclass
class Instr:
    off: int          # code offset
    op: int
    args: list        # int | bytes, per operand kind
    raw: bytes        # original encoding (opcode included)

    @property
    def name(self) -> str:
        return OPS[self.op][0]

    @property
    def kinds(self) -> str:
        return OPS[self.op][1]


@dataclass
class Gut:
    type: int
    index: int
    desc: bytes             # 22 raw bytes
    events: list[int]       # addresses
    code: list[Instr]
    trailer: bytes = b""    # undecodable bytes after the last instruction

    @property
    def header_len(self) -> int:
        return 2 * len(self.events) + 3


def _cstr(buf: bytes, pos: int, what: str) -> bytes:
    end = buf.find(b"\0", pos)
    if end < 0:
        raise GutError(f"unterminated {what} at code offset {pos:#x}")
    return buf[pos:end]


def decode_code(code: bytes) -> tuple[list[Instr], bytes]:
    out: list[Instr] = []
    pos = 0
    while pos < len(code):
        op = code[pos]
        if op not in OPS:
            raise GutError(f"unknown opcode {op:#04x} at code offset {pos:#x}")
        p = pos + 1
        args: list = []
        for k in OPS[op][1]:
            if k in "wa":
                if p + 2 > len(code):
                    raise GutError(f"{OPS[op][0]} at {pos:#x} runs past the end of the script")
                args.append(code[p] | code[p + 1] << 8)
                p += 2
            elif k == "d":
                if p + 4 > len(code):
                    raise GutError(f"{OPS[op][0]} at {pos:#x} runs past the end of the script")
                args.append(int.from_bytes(code[p:p + 4], "little"))
                p += 4
            else:
                s = _cstr(code, p, OPS[op][0])
                args.append(s)
                p += len(s) + 1
        out.append(Instr(pos, op, args, code[pos:p]))
        pos = p
    return out, b""


def parse(blob: bytes) -> Gut:
    if len(blob) < 0x1b:
        raise GutError("script resource shorter than its header")
    length = blob[0x18] | blob[0x19] << 8
    if 0x18 + length != len(blob):
        raise GutError(f"length field {length} does not match resource size {len(blob)}")
    n = blob[0x1a]
    events = [blob[0x1b + 2 * i] | blob[0x1c + 2 * i] << 8 for i in range(n)]
    code_start = 0x1b + 2 * n
    instrs, trailer = decode_code(blob[code_start:])
    return Gut(blob[0], blob[1], blob[2:0x18], events, instrs, trailer)


def encode_instr(op: int, args: list) -> bytes:
    out = bytearray([op])
    for k, v in zip(OPS[op][1], args):
        if k in "wa":
            out += int(v).to_bytes(2, "little")
        elif k == "d":
            out += int(v).to_bytes(4, "little")
        else:
            if b"\0" in v:
                raise GutError(f"{OPS[op][0]}: string contains NUL")
            out += v + b"\0"
    return bytes(out)


def build(g: Gut, targets: dict[int, int] | None = None) -> bytes:
    """Encode a Gut. `targets` maps old addresses to instruction indexes; when
    given, every jump and event is relocated to that instruction's new
    address. Without it, addresses are written as they are."""
    hl = g.header_len
    encoded = [encode_instr(i.op, i.args) for i in g.code]
    new_addr: list[int] = []
    pos = hl
    for e in encoded:
        new_addr.append(pos)
        pos += len(e)
    end_addr = pos

    def reloc(a: int) -> int:
        if targets is None or a == 0:
            return a
        if a not in targets:
            raise GutError(f"address {a:#x} is not an instruction start; cannot relocate")
        idx = targets[a]
        return end_addr if idx == len(g.code) else new_addr[idx]

    if targets is not None:
        encoded = []
        for i in g.code:
            args = [reloc(v) if k == "a" else v for k, v in zip(i.kinds, i.args)]
            encoded.append(encode_instr(i.op, args))
    body = b"".join(encoded) + g.trailer
    length = hl + len(body)
    if length > 0xffff:
        raise GutError(f"script is {length} bytes; the length field holds 65535")
    out = bytearray([g.type, g.index]) + g.desc
    out += length.to_bytes(2, "little") + bytes([len(g.events)])
    for a in g.events:
        out += reloc(a).to_bytes(2, "little")
    return bytes(out + body)


def target_map(g: Gut) -> dict[int, int]:
    """Old address -> instruction index (len(code) = end of script)."""
    hl = g.header_len
    m = {hl + i.off: n for n, i in enumerate(g.code)}
    end = hl + (g.code[-1].off + len(g.code[-1].raw) if g.code else 0)
    m.setdefault(end, len(g.code))
    return m


# --- text listing -----------------------------------------------------------

_SAFE = re.compile(r'[^"\\\x00-\x1f\x7f]')


def bytes_to_text(b: bytes) -> str:
    """GB2312 bytes -> quoted-string body; anything that does not decode
    cleanly (or would re-encode differently) becomes \\xNN."""
    out = []
    i = 0
    while i < len(b):
        c = b[i]
        if c < 0x80:
            ch = chr(c)
            if ch == '"' or ch == "\\":
                out.append("\\" + ch)
            elif 0x20 <= c < 0x7f:
                out.append(ch)
            else:
                out.append(f"\\x{c:02x}")
            i += 1
            continue
        pair = b[i:i + 2]
        try:
            ch = pair.decode("gb2312")
            if len(pair) == 2 and len(ch) == 1 and ch.encode("gb2312") == pair:
                out.append(ch)
                i += 2
                continue
        except UnicodeDecodeError:
            pass
        out.append(f"\\x{c:02x}")
        i += 1
    return "".join(out)


def text_to_bytes(s: str) -> bytes:
    out = bytearray()
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\":
            nxt = s[i + 1:i + 2]
            if nxt == "x":
                out.append(int(s[i + 2:i + 4], 16))
                i += 4
                continue
            if nxt in ('"', "\\"):
                out += nxt.encode()
                i += 2
                continue
            raise GutError(f"bad escape \\{nxt}")
        try:
            out += ch.encode("gb2312")
        except UnicodeEncodeError:
            raise GutError(f"character {ch!r} (U+{ord(ch):04X}) is not in GB2312") from None
        i += 1
    return bytes(out)


def label(addr: int) -> str:
    return f"L_{addr:04x}"


def disasm(g: Gut, key: str = "") -> str:
    hl = g.header_len
    targets = target_map(g)
    labels = {a for a in g.events if a} | {
        v for i in g.code for k, v in zip(i.kinds, i.args) if k == "a" and v}

    def fmt_addr(a: int) -> str:
        if a == 0:
            return "0"
        if a in targets:
            return label(a)
        return f"@{a:#06x}"  # not an instruction start: kept verbatim

    lines = [f"; BBKRPG script {key}".rstrip(), f".type {g.type}", f".index {g.index}",
             f'.desc "{bytes_to_text(g.desc)}"', f".events {len(g.events)}"]
    for n, a in enumerate(g.events, 1):
        if a:
            lines.append(f".event {n} {fmt_addr(a)}")
    lines.append("")
    for i in g.code:
        a = hl + i.off
        if a in labels:
            lines.append(f"{label(a)}:")
        parts = []
        for k, v in zip(i.kinds, i.args):
            if k == "a":
                parts.append(fmt_addr(v))
            elif k in "sz":
                parts.append(f'"{bytes_to_text(v)}"')
            else:
                parts.append(str(v))
        lines.append(f"    {i.name} {', '.join(parts)}".rstrip())
    end = hl + (g.code[-1].off + len(g.code[-1].raw) if g.code else 0)
    if end in labels:
        lines.append(f"{label(end)}:")
    if g.trailer:
        lines.append(f".bytes {g.trailer.hex()}")
    return "\n".join(lines) + "\n"


_TOKEN = re.compile(r'\s*("(?:[^"\\]|\\.)*"|[^,\s]+)\s*(?:,|$)')


def _split_args(s: str) -> list[str]:
    out, pos = [], 0
    s = s.strip()
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if not m:
            raise GutError(f"cannot parse operands: {s!r}")
        out.append(m.group(1))
        pos = m.end()
    return out


def asm(text: str) -> bytes:
    """Assemble a listing. Labels resolve to new addresses, so strings may
    change length freely; `@0x...` raw addresses are only allowed when the
    script's code size is unchanged."""
    meta: dict = {"events": 0}
    events: dict[int, str] = {}
    items: list[tuple[str, int, list[str]]] = []   # (label-or-"", op, args)
    pending_labels: list[str] = []
    label_at: dict[str, int] = {}
    trailer = b""
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.split(";", 1)[0] if '"' not in raw else _strip_comment(raw)
        line = line.strip()
        if not line:
            continue
        try:
            if line.startswith("."):
                d, _, rest = line.partition(" ")
                rest = rest.strip()
                if d in (".type", ".index", ".events"):
                    meta[d[1:]] = int(rest, 0)
                elif d == ".desc":
                    meta["desc"] = text_to_bytes(rest[1:-1])
                elif d == ".event":
                    n, tgt = rest.split()
                    events[int(n)] = tgt
                elif d == ".bytes":
                    trailer = bytes.fromhex(rest)
                else:
                    raise GutError(f"unknown directive {d}")
            elif line.endswith(":"):
                lab = line[:-1]
                label_at[lab] = len(items)
                pending_labels.append(lab)
            else:
                name, _, rest = line.partition(" ")
                if name not in BY_NAME:
                    raise GutError(f"unknown command {name!r}")
                op, kinds = BY_NAME[name]
                args = _split_args(rest) if rest.strip() else []
                if len(args) != len(kinds):
                    raise GutError(f"{name} takes {len(kinds)} operands, got {len(args)}")
                items.append(("", op, args))
                pending_labels = []
        except (GutError, ValueError) as e:
            raise GutError(f"line {ln}: {e}") from None

    desc = meta.get("desc", b"")
    if len(desc) > DESC_LEN:
        raise GutError(f".desc is {len(desc)} bytes; max {DESC_LEN}")
    desc = desc + b"\0" * (DESC_LEN - len(desc)) if len(desc) < DESC_LEN else desc
    nev = meta["events"]
    hl = 2 * nev + 3

    def conv(kind: str, tok: str):
        if kind in "sz":
            if not (tok.startswith('"') and tok.endswith('"')):
                raise GutError(f"expected a quoted string, got {tok}")
            return text_to_bytes(tok[1:-1])
        if kind == "a":
            return tok
        return int(tok, 0)

    code: list[Instr] = []
    for _, op, args in items:
        vals = [conv(k, t) for k, t in zip(OPS[op][1], args)]
        code.append(Instr(0, op, vals, b""))

    # Lay out with placeholder addresses (all u16), then resolve labels.
    addrs, pos = [], hl
    for i in code:
        addrs.append(pos)
        pos += len(encode_instr(i.op, [0 if k == "a" else v for k, v in zip(i.kinds, i.args)]))
    end = pos

    def resolve(tok: str, ln_hint: str) -> int:
        if tok == "0":
            return 0
        if tok.startswith("@"):
            return int(tok[1:], 0)
        if tok not in label_at:
            raise GutError(f"undefined label {tok} ({ln_hint})")
        idx = label_at[tok]
        return end if idx == len(code) else addrs[idx]

    for i in code:
        i.args = [resolve(v, i.name) if k == "a" else v for k, v in zip(i.kinds, i.args)]
    ev = [0] * nev
    for n, tgt in events.items():
        if not 1 <= n <= nev:
            raise GutError(f".event {n} outside 1..{nev}")
        ev[n - 1] = resolve(tgt, f".event {n}")
    g = Gut(meta.get("type", 0), meta.get("index", 0), desc, ev, code, trailer)
    return build(g)


def _strip_comment(line: str) -> str:
    out, q, i = [], False, 0
    while i < len(line):
        c = line[i]
        if c == "\\" and q:
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == '"':
            q = not q
        elif c == ";" and not q:
            break
        out.append(c)
        i += 1
    return "".join(out)
