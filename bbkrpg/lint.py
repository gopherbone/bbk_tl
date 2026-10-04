"""Checks on a translation table and the archive it builds."""

from __future__ import annotations

import re

from . import lib as libmod
from . import strings as strmod
from .lib import Lib

_HANZI = re.compile(r"[^\x00-\x7f]")


def lint(lib: Lib, rows: list[dict]) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    seen = set()
    known = {r["id"] for r in strmod.export(lib)}
    for r in rows:
        rid, en = r["id"], r.get("en", "")
        if rid in seen:
            errors.append(f"{rid}: duplicate row")
        seen.add(rid)
        if rid not in known:
            errors.append(f"{rid}: no such string in this archive")
            continue
        if not en:
            continue
        if _HANZI.search(en):
            errors.append(f"{rid}: non-ASCII text in en: {_HANZI.findall(en)[:5]}")
        try:
            n = len(strmod.encode_en(en))
        except Exception as e:  # noqa: BLE001 - surfaced as a lint error
            errors.append(f"{rid}: {e}")
            continue
        mx = r.get("limits", {}).get("max_bytes")
        if mx is not None and n > mx:
            errors.append(f"{rid}: {n} bytes, limit {mx}")
        if r["kind"] == "showgut":
            for line in _cols(en, 20):
                if len(line) > 20:
                    warnings.append(f"{rid}: scroll line over 20 columns: {line!r}")
                    break
        if r["kind"] == "menu" and len(en.split(" ")) != len(r["zh"].split(" ")):
            errors.append(f"{rid}: menu needs {len(r['zh'].split(' '))} space-separated items")

    built, problems = strmod.apply(lib, rows)
    errors += problems
    try:
        out = libmod.pack(built)
    except libmod.LibError as e:
        errors.append(f"pack: {e}")
    else:
        grown = len(out) // libmod.BANK - 1 - len(lib.banks)
        if grown:
            warnings.append(f"pack: {grown} overflow bank(s) appended; archive grows to {len(out)} bytes")
    todo = sum(1 for r in rows if not r.get("en"))
    if todo:
        warnings.append(f"{todo} of {len(rows)} rows untranslated")
    return errors, warnings


def _cols(text: str, width: int):
    for i in range(0, len(text), width):
        yield text[i:i + width]
