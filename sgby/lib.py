"""三国霸业's resource archive (dat.lib).

The .gam is: 6502 code segments (16 KiB each) up to the header's data offset,
then the 12x12 font (Gamhzk, 0x28000 bytes), then dat.lib to the end of the
file. dat.lib is byte-identical to iBaye's src/dat.lib.orig.

dat.lib layout (iBaye src/datman.c):
  * u32 address table: resource id n at (n-1)*4; 0xFFFFFFFF = absent;
  * each resource starts with RCHEAD {u32 len, u16 id, u16 count,
    u16 item_len, u8 key, u8 reserved} (12 bytes, len includes it);
  * item_len != 0: items are fixed size right after the header;
    item_len == 0 and count > 1: RIDX {u16 offset, u16 len} per item after
    the header, offsets relative to the resource start (iBaye's headers say
    u32; the native archive uses u16);
  * count can exceed the items actually stored (fixed-size resources hold
    (len - 12) // item_len items), and a few resources carry trailing bytes;
    both are kept as they are.
  * key != 0: every data byte is stored as plain + key (mod 256); the game
    subtracts it on load (ExpDataWithKey).

The game reads the archive through one 16 KiB window and never wraps
(gam_fread copies straight out of the window), so a resource must not cross
a 16 KiB boundary of the archive.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field

HEAD = 12
BANK = 0x4000
FONT_LEN = 0x28000


@dataclass
class Resource:
    rid: int
    count: int
    item_len: int
    key: int
    reserved: int
    items: list[bytes] = field(default_factory=list)   # plain (key removed)
    raw: bytes = b""                                    # original bytes, for unchanged resources
    tail: bytes = b""                                   # stored bytes after the items (as stored)

    def encode(self) -> bytes:
        k = self.key
        enc = (lambda b: bytes((x + k) & 0xFF for x in b)) if k else (lambda b: b)
        if self.item_len:
            body = b"".join(enc(it.ljust(self.item_len, b"\0")[: self.item_len]) for it in self.items)
            idx = b""
        elif self.count > 1:
            off = HEAD + 4 * len(self.items)
            idx, parts = b"", []
            for it in self.items:
                idx += struct.pack("<HH", off, len(it))
                parts.append(enc(it))
                off += len(it)
            body = b"".join(parts)
        else:
            idx, body = b"", enc(self.items[0])
        body += self.tail
        total = HEAD + len(idx) + len(body)
        count = self.count if self.item_len else len(self.items)
        return struct.pack("<IHHHBB", total, self.rid, count, self.item_len, k, self.reserved) + idx + body


def parse_resource(data: bytes, addr: int) -> Resource:
    ln, rid, cnt, il, key, rs = struct.unpack_from("<IHHHBB", data, addr)
    raw = data[addr: addr + ln]
    dec = (lambda b: bytes((x - key) & 0xFF for x in b)) if key else (lambda b: bytes(b))
    items, tail = [], b""
    if il:
        n = (ln - HEAD) // il
        for i in range(n):
            items.append(dec(raw[HEAD + i * il: HEAD + (i + 1) * il]))
        tail = raw[HEAD + n * il:]
    elif cnt > 1:
        end = HEAD
        for i in range(cnt):
            o, n = struct.unpack_from("<HH", raw, HEAD + 4 * i)
            items.append(dec(raw[o: o + n]))
            end = max(end, o + n)
        tail = raw[end:]
    else:
        items.append(dec(raw[HEAD:]))
    return Resource(rid, cnt, il, key, rs, items, raw, tail)


class Lib:
    def __init__(self, data: bytes):
        self.data = bytes(data)
        first = struct.unpack_from("<I", data, 0)[0]
        n = 0
        addrs = []
        while n * 4 < len(data):
            a = struct.unpack_from("<I", data, n * 4)[0]
            addrs.append(a)
            n += 1
            if a != 0xFFFFFFFF:
                first = min(first, a)
            if n * 4 >= first:
                break
        self.addrs = addrs
        self.res = {i + 1: parse_resource(data, a) for i, a in enumerate(addrs) if a != 0xFFFFFFFF}

    def build(self, changed: dict[int, Resource]) -> bytes:
        """Keep every unchanged resource where it is; append changed ones
        at the end, each kept inside one 16 KiB bank."""
        out = bytearray(self.data)
        addrs = list(self.addrs)
        for rid in sorted(changed):
            blob = changed[rid].encode()
            if len(blob) > BANK:
                raise ValueError(f"resource {rid} is {len(blob)} bytes, over one bank")
            pos = len(out)
            if pos // BANK != (pos + len(blob) - 1) // BANK:
                pos = (pos // BANK + 1) * BANK
                out += b"\xff" * (pos - len(out))
            out += blob
            addrs[rid - 1] = pos
        for i, a in enumerate(addrs):
            struct.pack_into("<I", out, i * 4, a)
        return bytes(out)


def split_gam(gam: bytes):
    """(code, font, lib) of a .gam."""
    data_off = struct.unpack_from("<I", gam, 0x42)[0]
    return gam[:data_off], gam[data_off: data_off + FONT_LEN], gam[data_off + FONT_LEN:]
