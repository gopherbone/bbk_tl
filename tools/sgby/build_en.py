"""Build the English 三国霸业 .gam.

    python3 tools/sgby/build_en.py [rows.jsonl ...] [-o work/sgby/sgby_en.gam]

Rows are merged in order (later files win per id); default
translations/sgby/en.jsonl plus any translations/sgby/fix*.jsonl.
"""
import glob, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from sgby import strings, images, layout, build as B  # noqa: E402
from sgby.lib import Lib, split_gam  # noqa: E402

GAM = "gam4980/retroarch/downloads/bbk/三国霸业.gam"


def main(argv):
    out = "work/sgby/sgby_en.gam"
    if "-o" in argv:
        i = argv.index("-o")
        out = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    files = argv or (["translations/sgby/en.jsonl"] + sorted(glob.glob("translations/sgby/fix*.jsonl")))
    merged = {}
    for f in files:
        for r in strings.load_rows(f):
            if r.get("en"):
                merged[r["id"]] = r["en"]
    base = strings.load_rows("translations/sgby/strings.jsonl")
    rows = [dict(r, en=merged[r["id"]]) if r["id"] in merged else r for r in base]
    gam = open(GAM, "rb").read()
    code, font, lib = split_gam(gam)
    L = Lib(lib)
    changed = strings.apply(L, rows)
    images.apply(L, changed)
    layout.apply(L, changed)
    title = next((r["en"] for r in rows if r["id"] == "e/45" and r.get("en")), None)
    data = B.build(gam, changed, strings.width(title) if title else 60)
    bank = []
    for rid in sorted(k for k in changed if k >= 78 and k < 100):
        bank.append([it.decode("latin-1") for it in changed[rid].items])
    import json
    from sgby import render
    _, syms = render.build_segment()
    json.dump({"bank": bank, "strshow": syms["strshow"]}, open(out + ".json", "w"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "wb").write(data)
    print(f"{out}: {len(data)} bytes, {sum(1 for r in rows if r.get('en'))} rows in English")


main(sys.argv[1:])
