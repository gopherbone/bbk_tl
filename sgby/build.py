"""Assemble a translated 三国霸业 .gam from the original."""

from __future__ import annotations

import struct

from . import render
from .lib import FONT_LEN, Lib, split_gam


def build(gam: bytes, changed: dict, king_title_w: int = 60) -> bytes:
    """`changed`: rid -> Resource (replacing or adding resources).
    The renderer segment is inserted and the archive rebuilt."""
    code, font, lib = split_gam(gam)
    L = Lib(lib)
    allres = dict(changed)
    need = max(allres) if allres else 0
    if need > len(L.addrs):
        raise ValueError("resource id beyond the address table")
    new_lib = L.build(allres)
    patched = render.patch(code + font, king_title_w)      # code + font only; lib appended below
    data_off = struct.unpack_from("<I", patched, 0x42)[0]
    return patched[: data_off + FONT_LEN] + new_lib
