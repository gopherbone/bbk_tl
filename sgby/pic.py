"""三国霸业 pictures (iBaye src/baye/graph.h) and SPE animations.

Picture: {u16 wid, u16 hig, u8 count, u8 mask} (6 bytes natively; iBaye's
header declares a u16 count) then `count` frames. A frame
is `hig` rows of ceil(wid/8) bytes (MSB = left, 1 = black); with mask & 1 it
is followed by a second plane of the same size (drawn with SysPicture mode 1
then mode 2: the first plane is ANDed, the second ORed).

SPE animation (PublicFun.c GamSpeShow): u8 count?, ..., u8 picmax at +3,
6-byte header, `count` SPEUNIT records, then `picmax` pictures back to back.
"""

from __future__ import annotations

import struct

PICHEAD = 6


def frame_len(w: int, h: int, mask: int) -> int:
    return ((w + 7) // 8) * h * (2 if mask & 1 else 1)


def parse(blob: bytes, off: int = 0):
    w, h, count, mask = struct.unpack_from("<HHBB", blob, off)
    return {"w": w, "h": h, "count": count, "mask": mask, "off": off,
            "len": PICHEAD + frame_len(w, h, mask) * count}


def plausible(blob: bytes, off: int = 0) -> bool:
    if len(blob) - off < PICHEAD:
        return False
    p = parse(blob, off)
    return 1 <= p["w"] <= 320 and 1 <= p["h"] <= 200 and 1 <= p["count"] <= 255 and p["mask"] in (0, 1) \
        and off + p["len"] <= len(blob)


def frames(blob: bytes, off: int = 0) -> list[list[bytes]]:
    """Each frame as a list of planes (raw bytes)."""
    p = parse(blob, off)
    fl = frame_len(p["w"], p["h"], p["mask"])
    pl = ((p["w"] + 7) // 8) * p["h"]
    out = []
    pos = off + PICHEAD
    for _ in range(p["count"]):
        f = blob[pos:pos + fl]
        out.append([f[:pl], f[pl:]] if p["mask"] & 1 else [f])
        pos += fl
    return out


def to_rows(plane: bytes, w: int, h: int) -> list[list[int]]:
    rb = (w + 7) // 8
    return [[(plane[y * rb + x // 8] >> (7 - x % 8)) & 1 for x in range(w)] for y in range(h)]


def from_rows(rows: list[list[int]], w: int, h: int) -> bytes:
    rb = (w + 7) // 8
    out = bytearray(rb * h)
    for y in range(h):
        for x in range(w):
            if rows[y][x]:
                out[y * rb + x // 8] |= 0x80 >> (x % 8)
    return bytes(out)


def build(w: int, h: int, mask: int, frames_: list[list[bytes]]) -> bytes:
    out = bytearray(struct.pack("<HHBB", w, h, len(frames_), mask))
    for f in frames_:
        for plane in f:
            out += plane
    return bytes(out)
