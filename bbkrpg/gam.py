""".gam container: find, split out and replace the BBKRPG archive.

.gam header (BBKEmu docs/Game-File-Formats.md, checked on the 152-game set):
  0x00  "GAM\\0", then game name (GB2312) from 0x06
  0x40  u16 LE entry point (6502 address)
  0x42  u32 LE data section offset

In every BBKRPG game the data section is the archive ("LIB" + name), usually
at 0x48000, and it runs to the end of the file. Nothing in the header records
the archive size, so a larger archive is written by extending the file. A few
fan games carry bytes after the archive's last bank; those are kept as the
archive's tail.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from . import lib as libmod

DATA_OFFSET = 0x42


@dataclass
class Found:
    offset: int
    size: int
    name: str
    entry: int
    engine_sha1: str      # hash of the bytes before the archive, header excluded


def data_offset(data: bytes) -> int:
    return int.from_bytes(data[DATA_OFFSET:DATA_OFFSET + 4], "little")


def find(data: bytes) -> list[Found]:
    """The BBKRPG archive named by the header, if there is one."""
    if data[:3] != b"GAM":
        return []
    off = data_offset(data)
    if data[off:off + 3] != b"LIB":
        return []
    try:
        L = libmod.parse(data[off:])
    except libmod.LibError:
        return []
    entry = data[0x40] | data[0x41] << 8
    return [Found(off, len(data) - off, L.name, entry,
                  hashlib.sha1(data[0x46:off]).hexdigest())]


def split(data: bytes) -> tuple[bytes, Found]:
    hits = find(data)
    if not hits:
        raise libmod.LibError("no BBKRPG archive at the .gam's data offset")
    h = hits[0]
    return data[h.offset:], h


def join(data: bytes, new_lib: bytes) -> bytes:
    """Replace the archive; the file grows or shrinks with it."""
    _, h = split(data)
    return data[:h.offset] + new_lib
