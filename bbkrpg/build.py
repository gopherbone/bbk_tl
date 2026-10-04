"""Build a translated .gam: scripts, records, engine strings, font and text bank."""

from __future__ import annotations

from . import engine_text, fontpatch
from . import gam as gammod
from . import lib as libmod
from . import strings as strmod


def build(orig: bytes, rows: list[dict]) -> tuple[bytes, dict, list[str]]:
    """Return (new .gam, info, problems). `orig` is the untouched game."""
    bank: list[bytes] = [b""] * engine_text.RESERVED_SHORT
    lib = libmod.parse(gammod.split(orig)[0])
    built, problems = strmod.apply(lib, [r for r in rows if not r["id"].startswith("ENG/")], bank=bank)
    engine, eprob = engine_text.apply(orig, rows, bank)
    problems += eprob
    joined = gammod.join(engine, libmod.pack(built))
    out, info = fontpatch.patch(joined, bank)
    return out, info, problems
