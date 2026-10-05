"""Build a translated .gam: scripts, records, engine strings, font and text bank."""

from __future__ import annotations

from . import engine_text, fontpatch, games
from . import gam as gammod
from . import lib as libmod
from . import strings as strmod


def build(orig: bytes, rows: list[dict], gallery: list[str] | None = None,
          images: bool = True, game=None) -> tuple[bytes, dict, list[str]]:
    """Return (new .gam, info, problems). `orig` is the untouched game and
    `game` its bbkrpg.games profile (default 伏魔记), which supplies the engine
    string table and the image redraws. With `gallery` (gut row ids), New Game
    shows those lines one by one instead of the opening (bbkrpg.gallery)."""
    game = game or games.get("fmj")
    bank: list[bytes] = [b""] * engine_text.RESERVED_SHORT
    lib = libmod.parse(gammod.split(orig)[0])
    built, problems = strmod.apply(lib, [r for r in rows if not r["id"].startswith("ENG/")], bank=bank)
    if images and game.images:
        game.images(built.res, rows)
    if gallery:
        from . import gallery as gallerymod
        built.res[gallerymod.OPENING] = gallerymod.script(lib, {r["id"]: r for r in rows}, gallery, bank)
    engine, eprob = engine_text.apply(orig, rows, bank, game.engine)
    problems += eprob
    joined = gammod.join(engine, libmod.pack(built))
    out, info = fontpatch.patch(joined, bank, game.dialogue_top)
    info["bank"] = [b.decode("ascii", "replace") for b in bank]
    return out, info, problems
