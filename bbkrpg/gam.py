"""Locate a BBKRPG archive inside a .gam file.

Provisional until phase 1 recon on a real 伏魔记.gam: we assume the archive
is stored raw and contiguous, and find it by its "LIB" signature plus a
successful parse. Join only supports writing back an archive of the same
size; growing the archive needs the .gam header fields mapped first.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from . import lib as libmod


@dataclass
class Found:
    offset: int
    size: int
    name: str
    engine_sha1: str      # hash of every byte outside the archive


def _archive_size(data: bytes, off: int) -> int | None:
    """Parse the archive's tables and return the end of its last bank."""
    nbytes = data[off + 0x0c] | data[off + 0x0d] << 8
    if nbytes == 0 or nbytes % 3 or nbytes > 0x1ff0:
        return None
    last = 0
    for e in range(nbytes // 3):
        p = data[off + 0x2000 + 3 * e: off + 0x2003 + 3 * e]
        if len(p) < 3:
            return None
        last = max(last, p[0])
    size = (last + 1) * libmod.BANK
    return size if off + size <= len(data) else None


def find(data: bytes) -> list[Found]:
    out = []
    pos = data.find(b"LIB")
    while pos >= 0:
        size = _archive_size(data, pos)
        if size:
            try:
                L = libmod.parse(data[pos:pos + size])
            except libmod.LibError:
                L = None
            if L is not None:
                engine = data[:pos] + data[pos + size:]
                out.append(Found(pos, size, L.name, hashlib.sha1(engine).hexdigest()))
        pos = data.find(b"LIB", pos + 1)
    return out


def split(data: bytes) -> tuple[bytes, Found]:
    hits = find(data)
    if len(hits) != 1:
        raise libmod.LibError(f"expected one BBKRPG archive in the .gam, found {len(hits)}")
    h = hits[0]
    return data[h.offset:h.offset + h.size], h


def join(data: bytes, new_lib: bytes) -> bytes:
    _, h = split(data)
    if len(new_lib) != h.size:
        raise libmod.LibError(
            f"archive is {len(new_lib)} bytes, the .gam slot holds {h.size}; "
            "resizing needs the .gam header mapped (phase 1)")
    return data[:h.offset] + new_lib + data[h.offset + h.size:]
