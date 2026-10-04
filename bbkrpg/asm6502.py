"""A small two-pass NMOS 6502 assembler for engine patches.

Syntax (one statement per line, ';' comments):
    label:                     define a label (at the current address)
    name = expr                define a constant
    .org expr                  set the address (output is contiguous from the first .org)
    .byte e, e, "text"         bytes (strings are ASCII)
    .word e, e                 little-endian words
    .res n [, fill]            n bytes of fill (default 0)
    lda #<label / #>label      low / high byte
    lda $12   lda $1234   lda $12,x   lda ($12),y   lda ($12,x)   jmp ($1234)
    bne label                  relative branches
Expressions: numbers ($hex, %bin, decimal), labels, + - * / & | >> <<,
<x (low byte), >x (high byte), parentheses only inside expressions.
Zero-page forms are used when the operand is known in pass 1 and < $100.
"""

from __future__ import annotations

import re

# mnemonic -> {mode: opcode}
_T: dict[str, dict[str, int]] = {}


def _add(m, **modes):
    _T[m] = modes


for m, base in [("ora", 0x00), ("and", 0x20), ("eor", 0x40), ("adc", 0x60), ("lda", 0xA0), ("cmp", 0xC0), ("sbc", 0xE0)]:
    _add(m, izx=base + 1, zp=base + 5, imm=base + 9, abs=base + 0xD, izy=base + 0x11, zpx=base + 0x15,
         aby=base + 0x19, abx=base + 0x1D)
_add("sta", izx=0x81, zp=0x85, abs=0x8D, izy=0x91, zpx=0x95, aby=0x99, abx=0x9D)
for m, base in [("asl", 0x00), ("rol", 0x20), ("lsr", 0x40), ("ror", 0x60)]:
    _add(m, zp=base + 6, acc=base + 0xA, abs=base + 0xE, zpx=base + 0x16, abx=base + 0x1E)
_add("inc", zp=0xE6, abs=0xEE, zpx=0xF6, abx=0xFE)
_add("dec", zp=0xC6, abs=0xCE, zpx=0xD6, abx=0xDE)
_add("ldx", imm=0xA2, zp=0xA6, abs=0xAE, zpy=0xB6, aby=0xBE)
_add("ldy", imm=0xA0, zp=0xA4, abs=0xAC, zpx=0xB4, abx=0xBC)
_add("stx", zp=0x86, abs=0x8E, zpy=0x96)
_add("sty", zp=0x84, abs=0x8C, zpx=0x94)
_add("cpx", imm=0xE0, zp=0xE4, abs=0xEC)
_add("cpy", imm=0xC0, zp=0xC4, abs=0xCC)
_add("bit", zp=0x24, abs=0x2C)
_add("jmp", abs=0x4C, ind=0x6C)
_add("jsr", abs=0x20)
for m, op in [("bpl", 0x10), ("bmi", 0x30), ("bvc", 0x50), ("bvs", 0x70), ("bcc", 0x90), ("bcs", 0xB0),
              ("bne", 0xD0), ("beq", 0xF0)]:
    _add(m, rel=op)
for m, op in [("brk", 0x00), ("php", 0x08), ("clc", 0x18), ("plp", 0x28), ("sec", 0x38), ("rti", 0x40),
              ("pha", 0x48), ("cli", 0x58), ("rts", 0x60), ("pla", 0x68), ("sei", 0x78), ("dey", 0x88),
              ("txa", 0x8A), ("tya", 0x98), ("txs", 0x9A), ("tay", 0xA8), ("tax", 0xAA), ("clv", 0xB8),
              ("tsx", 0xBA), ("iny", 0xC8), ("dex", 0xCA), ("cld", 0xD8), ("inx", 0xE8), ("nop", 0xEA),
              ("sed", 0xF8)]:
    _add(m, imp=op)

_LEN = {"imp": 1, "acc": 1, "imm": 2, "zp": 2, "zpx": 2, "zpy": 2, "izx": 2, "izy": 2, "rel": 2,
        "abs": 3, "abx": 3, "aby": 3, "ind": 3}


class AsmError(Exception):
    pass


def _num(tok: str) -> int:
    if tok.startswith("$"):
        return int(tok[1:], 16)
    if tok.startswith("%"):
        return int(tok[1:], 2)
    if tok.startswith("0x"):
        return int(tok, 16)
    return int(tok)


_TOKEN = re.compile(r"\s*(\$[0-9a-fA-F]+|%[01]+|0x[0-9a-fA-F]+|\d+|[A-Za-z_.@][\w.@]*|>>|<<|[-+*/&|()<>])")


def evaluate(expr: str, syms: dict[str, int], strict: bool) -> int | None:
    toks = []
    pos = 0
    expr = expr.strip()
    while pos < len(expr):
        m = _TOKEN.match(expr, pos)
        if not m:
            raise AsmError(f"bad expression {expr!r}")
        toks.append(m.group(1))
        pos = m.end()
    i = 0

    def peek():
        return toks[i] if i < len(toks) else None

    def take():
        nonlocal i
        i += 1
        return toks[i - 1]

    def atom():
        t = take()
        if t == "(":
            v = binop(0)
            if take() != ")":
                raise AsmError(f"missing ) in {expr!r}")
            return v
        if t == "<":
            v = atom()
            return None if v is None else v & 0xFF
        if t == ">":
            v = atom()
            return None if v is None else (v >> 8) & 0xFF
        if t == "-":
            v = atom()
            return None if v is None else -v
        if t[0] in "$%" or t[0].isdigit():
            return _num(t)
        if t in syms:
            return syms[t]
        if strict:
            raise AsmError(f"undefined symbol {t}")
        return None

    prec = {"|": 1, "&": 2, "<<": 3, ">>": 3, "+": 4, "-": 4, "*": 5, "/": 5}

    def binop(minp):
        lhs = atom()
        while peek() in prec and prec[peek()] >= minp:
            op = take()
            rhs = binop(prec[op] + 1)
            if lhs is None or rhs is None:
                lhs = None
                continue
            lhs = {"|": lhs | rhs, "&": lhs & rhs, "<<": lhs << rhs, ">>": lhs >> rhs, "+": lhs + rhs,
                   "-": lhs - rhs, "*": lhs * rhs, "/": lhs // rhs}[op]
        return lhs

    v = binop(0)
    if i != len(toks):
        raise AsmError(f"trailing tokens in {expr!r}")
    return v


def _split_operands(s: str) -> list[str]:
    out, cur, q = [], "", False
    for ch in s:
        if ch == '"':
            q = not q
        if ch == "," and not q:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def _mode(mn: str, opnd: str, syms, strict):
    """Return (mode, expr) for an instruction operand."""
    o = opnd.strip()
    modes = _T[mn]
    if not o:
        return ("acc" if "acc" in modes and "imp" not in modes else "imp"), None
    if o.lower() == "a" and "acc" in modes:
        return "acc", None
    if "rel" in modes:
        return "rel", o
    if o.startswith("#"):
        return "imm", o[1:]
    m = re.fullmatch(r"\((.+),\s*[xX]\)", o)
    if m:
        return "izx", m.group(1)
    m = re.fullmatch(r"\((.+)\)\s*,\s*[yY]", o)
    if m:
        return "izy", m.group(1)
    m = re.fullmatch(r"\((.+)\)", o)
    if m and "ind" in modes:
        return "ind", m.group(1)
    idx = None
    m = re.fullmatch(r"(.+),\s*([xXyY])", o)
    if m:
        o, idx = m.group(1), m.group(2).lower()
    v = evaluate(o, syms, False)
    small = v is not None and 0 <= v < 0x100
    if idx is None:
        return ("zp" if small and "zp" in modes else "abs"), o
    zp_mode, abs_mode = ("zpx", "abx") if idx == "x" else ("zpy", "aby")
    return (zp_mode if small and zp_mode in modes else abs_mode), o


def assemble(src: str, syms: dict[str, int] | None = None) -> tuple[int, bytes, dict[str, int]]:
    """Assemble `src`; returns (origin, bytes, symbols)."""
    base_syms = dict(syms or {})
    lines = []
    for n, raw in enumerate(src.splitlines(), 1):
        line = raw.split(";", 1)[0].rstrip() if '"' not in raw else raw.rstrip()
        if '"' in raw:  # strip comment outside quotes
            q, cut = False, len(raw)
            for k, ch in enumerate(raw):
                if ch == '"':
                    q = not q
                elif ch == ";" and not q:
                    cut = k
                    break
            line = raw[:cut].rstrip()
        if line.strip():
            lines.append((n, line))

    sizes: dict[int, int] = {}

    def run(pass_no: int, symbols: dict[str, int]):
        strict = pass_no == 2
        pc = None
        origin = None
        out = bytearray()
        for n, line in lines:
            try:
                s = line.strip()
                m = re.match(r"^([A-Za-z_.@][\w.@]*):\s*(.*)$", s)
                if m:
                    if pc is None:
                        raise AsmError("label before .org")
                    if pass_no == 1 and m.group(1) in symbols and m.group(1) not in base_syms:
                        raise AsmError(f"duplicate label {m.group(1)}")
                    symbols[m.group(1)] = pc
                    s = m.group(2).strip()
                    if not s:
                        continue
                m = re.match(r"^([A-Za-z_][\w.]*)\s*=\s*(.+)$", s)
                if m:
                    v = evaluate(m.group(2), symbols, strict)
                    if v is not None:
                        symbols[m.group(1)] = v
                    continue
                word, _, rest = s.partition(" ")
                word = word.lower()
                if word == ".org":
                    v = evaluate(rest, symbols, True)
                    if origin is None:
                        origin = v
                    elif v < pc:
                        raise AsmError(".org moves backwards")
                    else:
                        out += b"\xff" * (v - pc)
                    pc = v
                    continue
                if pc is None:
                    raise AsmError("code before .org")
                if word == ".byte":
                    for o in _split_operands(rest):
                        if o.startswith('"'):
                            data = o[1:-1].encode("ascii")
                        else:
                            v = evaluate(o, symbols, strict)
                            data = bytes([(v or 0) & 0xFF])
                        out += data
                        pc += len(data)
                    continue
                if word == ".word":
                    for o in _split_operands(rest):
                        v = evaluate(o, symbols, strict) or 0
                        out += (v & 0xFFFF).to_bytes(2, "little")
                        pc += 2
                    continue
                if word == ".res":
                    ops = _split_operands(rest)
                    cnt = evaluate(ops[0], symbols, True)
                    fill = evaluate(ops[1], symbols, True) if len(ops) > 1 else 0
                    out += bytes([fill]) * cnt
                    pc += cnt
                    continue
                if word not in _T:
                    raise AsmError(f"unknown mnemonic {word}")
                mode, expr = _mode(word, rest, symbols, strict)
                if pass_no == 2 and n in sizes and _LEN[mode] != sizes[n]:
                    # keep pass-1 sizing (forward refs assumed absolute)
                    mode = {"zp": "abs", "zpx": "abx", "zpy": "aby"}.get(mode, mode)
                if pass_no == 1:
                    sizes[n] = _LEN[mode]
                if mode not in _T[word]:
                    raise AsmError(f"{word} has no {mode} mode")
                op = _T[word][mode]
                v = evaluate(expr, symbols, strict) if expr is not None else None
                if mode == "rel":
                    if v is None:
                        out += bytes([op, 0])
                    else:
                        d = v - (pc + 2)
                        if strict and not -128 <= d <= 127:
                            raise AsmError(f"branch out of range ({d})")
                        out += bytes([op, d & 0xFF])
                elif _LEN[mode] == 1:
                    out.append(op)
                elif _LEN[mode] == 2:
                    if strict and v is not None and not -128 <= v <= 0xFF:
                        raise AsmError(f"operand {v:#x} does not fit a byte")
                    out += bytes([op, (v or 0) & 0xFF])
                else:
                    out += bytes([op]) + ((v or 0) & 0xFFFF).to_bytes(2, "little")
                pc += _LEN[mode]
            except AsmError as e:
                raise AsmError(f"line {n}: {e}: {line.strip()}") from None
        return origin, bytes(out)

    s1 = dict(base_syms)
    run(1, s1)
    s2 = dict(base_syms)
    s2.update({k: v for k, v in s1.items()})
    origin, data = run(2, s2)
    return origin, data, s2
