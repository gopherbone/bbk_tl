"""BBKRPG resource archive (DAT.LIB): parse, unpack to a directory, pack back.

Layout (checked against fmj/jy/cb/xkx archives):

  bank 0 (0x0000-0x3fff)
    0x00  "LIB" + game name, GB2312, NUL-padded (to 0x0c)
    0x0c  u16 LE: size of the key table in bytes (3 per resource)
    0x10  key table: (res_type, sub_type, index), 3 bytes each, sorted
    0x2000 pointer table, same order: (bank, addr_lo, addr_hi);
          offset = bank * 0x4000 + addr
  bank N (N >= 1), 16 KiB each
    0x00  3-byte type tag ("GUT", "MAP", ...) + 9 bytes of authoring junk
    0x0c  u16 LE: end offset of the last resource, from bank start
    0x10  resources, back to back, never crossing the bank end
    end.. filler (mostly 0xff, sometimes junk) up to the bank end

Resource sizes are not stored; a resource runs to the next one in its bank or
to the bank's end offset. Packing keeps every resource in its original bank
when it still fits, so an unchanged archive packs byte-identically, and moves
any resource that no longer fits into a new bank of the same tag appended at
the end of the archive.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

BANK = 0x4000
BANK_HDR = 0x10
KEY_TABLE = 0x10
PTR_TABLE = 0x2000

RES_TYPES = {
    1: "GUT", 2: "MAP", 3: "ARS", 4: "MRS", 5: "SRS", 6: "GRS",
    7: "TIL", 8: "ACP", 9: "GDP", 10: "GGJ", 11: "PIC", 12: "MLR",
}

Key = tuple[int, int, int]


class LibError(Exception):
    pass


def key_str(k: Key) -> str:
    return f"{k[0]}-{k[1]}-{k[2]}"


def parse_key(s: str) -> Key:
    a, b, c = (int(x) for x in s.split("-"))
    return (a, b, c)


@dataclass
class Bank:
    header: bytes                 # 16 bytes as found (end offset rewritten on pack)
    keys: list[Key]               # resources in address order
    filler: bytes                 # bytes after the last resource

    @property
    def tag(self) -> str:
        return self.header[:3].decode("latin1")


@dataclass
class Lib:
    head: bytes                   # bank 0, raw (tables rewritten on pack)
    banks: list[Bank]             # banks 1..n
    order: list[Key]              # key table order
    res: dict[Key, bytes]
    tail: bytes = b""             # bytes past the last whole bank
    extra: dict = field(default_factory=dict)

    @property
    def name(self) -> str:
        raw = self.head[3:0x0c].split(b"\0", 1)[0]
        return raw.decode("gb2312", errors="replace")

    def keys_of(self, res_type: int) -> list[Key]:
        return [k for k in self.order if k[0] == res_type]


def parse(data: bytes) -> Lib:
    if data[:3] != b"LIB":
        raise LibError("not a BBKRPG archive (no LIB signature)")
    nbytes = data[0x0c] | data[0x0d] << 8
    if nbytes % 3:
        raise LibError(f"key table size {nbytes} is not a multiple of 3")
    n = nbytes // 3
    order: list[Key] = []
    offs: dict[Key, int] = {}
    for e in range(n):
        k = tuple(data[KEY_TABLE + 3 * e: KEY_TABLE + 3 * e + 3])
        p = data[PTR_TABLE + 3 * e: PTR_TABLE + 3 * e + 3]
        if k in offs:
            raise LibError(f"duplicate key {k}")
        order.append(k)  # type: ignore[arg-type]
        offs[k] = p[0] * BANK + (p[1] | p[2] << 8)  # type: ignore[index]

    nbanks = len(data) // BANK
    by_bank: dict[int, list[tuple[int, Key]]] = {}
    for k, o in offs.items():
        b = o // BANK
        if b < 1 or b >= nbanks:
            raise LibError(f"{key_str(k)} points outside the archive ({o:#x})")
        by_bank.setdefault(b, []).append((o % BANK, k))

    banks: list[Bank] = []
    res: dict[Key, bytes] = {}
    for b in range(1, nbanks):
        base = b * BANK
        hdr = data[base: base + BANK_HDR]
        end = hdr[12] | hdr[13] << 8
        items = sorted(by_bank.get(b, []))
        if items and items[0][0] != BANK_HDR:
            raise LibError(f"bank {b}: first resource at {items[0][0]:#x}, expected 0x10")
        if items and end <= items[-1][0]:
            raise LibError(f"bank {b}: end offset {end:#x} before last resource")
        if not items:
            end = BANK_HDR if end < BANK_HDR or end > BANK else end
        for i, (a, k) in enumerate(items):
            stop = items[i + 1][0] if i + 1 < len(items) else end
            res[k] = data[base + a: base + stop]
        banks.append(Bank(hdr, [k for _, k in items], data[base + end: base + BANK]))

    return Lib(data[:BANK], banks, order, res, data[nbanks * BANK:])


def read(path: str) -> Lib:
    with open(path, "rb") as f:
        return parse(f.read())


def pack(lib: Lib) -> bytes:
    """Lay resources back into banks and rebuild the key/pointer tables."""
    out_banks: list[bytes] = []
    where: dict[Key, int] = {}
    overflow: dict[str, list[Key]] = {}
    template: dict[str, bytes] = {}

    def emit(header: bytes, keys: list[Key], filler: bytes | None) -> None:
        b = len(out_banks) + 1
        body = bytearray()
        for k in keys:
            where[k] = b * BANK + BANK_HDR + len(body)
            body += lib.res[k]
        end = BANK_HDR + len(body)
        hdr = bytearray(header)
        hdr[12], hdr[13] = end & 0xff, end >> 8
        room = BANK - end
        fill = filler if filler is not None and len(filler) == room else b"\xff" * room
        out_banks.append(bytes(hdr) + bytes(body) + fill)

    for bank in lib.banks:
        template.setdefault(bank.tag, bank.header[:3] + b"\0" * 13)
        kept: list[Key] = []
        used = BANK_HDR
        for k in bank.keys:
            size = len(lib.res[k])
            if size > BANK - BANK_HDR:
                raise LibError(f"{key_str(k)} is {size} bytes; a bank holds {BANK - BANK_HDR}")
            if used + size <= BANK:
                kept.append(k)
                used += size
            else:
                overflow.setdefault(bank.tag, []).append(k)
        emit(bank.header, kept, bank.filler)

    for tag, keys in overflow.items():
        cur: list[Key] = []
        used = BANK_HDR
        for k in keys:
            size = len(lib.res[k])
            if used + size > BANK:
                emit(template[tag], cur, None)
                cur, used = [], BANK_HDR
            cur.append(k)
            used += size
        if cur:
            emit(template[tag], cur, None)

    if len(out_banks) + 1 > 0xff:
        raise LibError("archive needs more than 255 banks")
    head = bytearray(lib.head)
    nbytes = 3 * len(lib.order)
    head[0x0c], head[0x0d] = nbytes & 0xff, nbytes >> 8
    for e, k in enumerate(lib.order):
        o = where[k]
        head[KEY_TABLE + 3 * e: KEY_TABLE + 3 * e + 3] = bytes(k)
        head[PTR_TABLE + 3 * e: PTR_TABLE + 3 * e + 3] = bytes(
            [o // BANK, o % BANK & 0xff, o % BANK >> 8])
    return bytes(head) + b"".join(out_banks) + lib.tail


# --- directory form -------------------------------------------------------

def res_path(k: Key) -> str:
    return os.path.join("res", RES_TYPES.get(k[0], f"T{k[0]}"), key_str(k) + ".bin")


def _filler_json(b: bytes):
    return {"ff": len(b)} if b == b"\xff" * len(b) else b.hex()


def _filler_bytes(v) -> bytes:
    return b"\xff" * v["ff"] if isinstance(v, dict) else bytes.fromhex(v)


def unpack(lib: Lib, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "head.bin"), "wb") as f:
        f.write(lib.head)
    for k, blob in lib.res.items():
        p = os.path.join(outdir, res_path(k))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(blob)
    manifest = {
        "format": "bbkrpg-lib/1",
        "name": lib.name,
        "order": [key_str(k) for k in lib.order],
        "banks": [{"header": b.header.hex(), "keys": [key_str(k) for k in b.keys],
                   "filler": _filler_json(b.filler)} for b in lib.banks],
        "tail": lib.tail.hex(),
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)


def load_dir(indir: str) -> Lib:
    with open(os.path.join(indir, "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)
    if m.get("format") != "bbkrpg-lib/1":
        raise LibError(f"{indir}: unknown manifest format {m.get('format')!r}")
    with open(os.path.join(indir, "head.bin"), "rb") as f:
        head = f.read()
    order = [parse_key(s) for s in m["order"]]
    res = {}
    for k in order:
        with open(os.path.join(indir, res_path(k)), "rb") as f:
            res[k] = f.read()
    banks = [Bank(bytes.fromhex(b["header"]), [parse_key(s) for s in b["keys"]],
                  _filler_bytes(b["filler"])) for b in m["banks"]]
    return Lib(head, banks, order, res, bytes.fromhex(m["tail"]))
