"""Shared helpers for the translation workflow.

Every tl script takes `--game KEY` (or BBK_GAME=KEY); the default is fmj.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from bbkrpg import fit, font_sans, games  # noqa: E402

GAME = games.from_argv()
STRINGS = GAME.path("strings")
GLOSSARY = GAME.path("glossary")
PARTS = GAME.path("parts")
MERGED = GAME.path("merged")


def rows():
    return [json.loads(l) for l in open(STRINGS, encoding="utf-8")]


def glossary():
    out = {}
    for t in map(json.loads, open(GLOSSARY, encoding="utf-8")):
        out.setdefault(t["zh"], t)
    return out


def load_part(path):
    """A part file: JSON lines {"id", "en"} (other keys ignored)."""
    return {d["id"]: d["en"] for d in map(json.loads, open(path, encoding="utf-8")) if d.get("en")}


def problems(r: dict, en: str) -> list[str]:
    """Hard errors for one translation."""
    out = []
    if not en.isascii():
        out.append("non-ASCII characters: " + "".join(sorted({c for c in en if not c.isascii()})))
    if "\0" in en:
        out.append("contains NUL")
    k = r["kind"]
    if k == "choice" and len(en) > 19:
        out.append(f"choice is {len(en)} chars; max 19")
    # display limits found in QA (the engine shows fewer bytes than the fields hold)
    shown = {"grs.name": 10, "mrs.name": 11, "ars.name": 11, "map.name": 12}
    if k in shown and len(en) > min(shown[k], r["limits"]["max_bytes"]):
        out.append(f"name is {len(en)} chars; max {min(shown[k], r['limits']['max_bytes'])}")
    if k == "setscenename" and len(en) > 10:
        # copied unbounded into a 10-byte RAM buffer (0x1942); the banner shows 10
        out.append(f"scene name is {len(en)} chars; max 10")
    if k in ("grs.desc", "mrs.desc") and len(fit.rows(en, fit.DESC_WIDTH)) > fit.DESC_ROWS:
        out.append(f"description needs {len(fit.rows(en, fit.DESC_WIDTH))} rows; the window shows {fit.DESC_ROWS}")
    if k == "message" and len(fit.rows(en, fit.MESSAGE_WIDTH)) > 4:
        out.append("message needs more than 4 rows")
    if k == "menu" and len(en.split(" ")) != len(r["zh"].split(" ")):
        out.append("menu needs the same number of space-separated items")
    return out


def warnings(r: dict, en: str, gl: dict) -> list[str]:
    out = []
    if r["kind"] == "say":
        pages = len(fit.pages(en, portrait=bool(r["ctx"].get("pic"))))
        if pages > 3:
            out.append(f"{pages} dialogue pages (consider tightening)")
    low = en.lower()
    for zh, t in gl.items():
        if len(zh) >= 2 and zh in r["zh"] and t["category"] in ("person", "place", "sect", "monster", "title", "item",
                                                                "weapon", "armor", "consumable", "magic", "skill"):
            if t["en"].lower() not in low and not any(a.lower() in low for a in (t.get("alt") or []) if isinstance(a, str)):
                out.append(f"glossary: {zh} = {t['en']!r} not found")
    return out
