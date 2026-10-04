"""BBKRPG image resources (TIL/ACP/GDP/GGJ/PIC): decode and encode.

Header: type, index, width, height, frames, mode (1 = opaque 1 bpp,
2 = transparent: 2 bits per pixel, mask bit then colour bit). Rows are padded
to whole bytes; in mode 2 each row is also padded to an even byte count.
Pixels: 0 white, 1 black, None transparent.
"""

from __future__ import annotations


def header(blob: bytes):
    return {"type": blob[0], "index": blob[1], "w": blob[2], "h": blob[3], "frames": blob[4], "mode": blob[5]}


def _row_bytes(w: int, mode: int) -> int:
    n = (w * mode + 7) // 8
    if mode == 2 and n % 2:
        n += 1
    return n


def decode(blob: bytes) -> tuple[dict, list[list[list]]]:
    h = header(blob)
    w, hh, mode = h["w"], h["h"], h["mode"]
    rb = _row_bytes(w, mode)
    frames, pos = [], 6
    for _ in range(h["frames"]):
        img = []
        for _y in range(hh):
            row, bits = [], blob[pos:pos + rb]
            for x in range(w):
                if mode == 2:
                    b = (bits[(2 * x) // 8] << ((2 * x) % 8)) & 0xFF
                    row.append(None if b & 0x80 else (1 if b & 0x40 else 0))
                else:
                    row.append(1 if (bits[x // 8] << (x % 8)) & 0x80 else 0)
            img.append(row)
            pos += rb
        frames.append(img)
    return h, frames


def encode(h: dict, frames: list[list[list]]) -> bytes:
    w, hh, mode = h["w"], h["h"], h["mode"]
    rb = _row_bytes(w, mode)
    out = bytearray([h["type"], h["index"], w, hh, len(frames), mode])
    for img in frames:
        for row in img:
            bits = bytearray(rb)
            for x, p in enumerate(row):
                if mode == 2:
                    v = 0x80 if p is None else (0x40 if p else 0)
                    bits[(2 * x) // 8] |= v >> ((2 * x) % 8)
                elif p:
                    bits[x // 8] |= 0x80 >> (x % 8)
            out += bits
    return bytes(out)
