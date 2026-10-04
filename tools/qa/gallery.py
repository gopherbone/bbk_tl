"""Build a gallery .gam for row ids and screenshot each line.

  python3 tools/qa/gallery.py OUT_PREFIX id [id ...]     (uses work/fmj.strings.jsonl + --en file)
"""
import argparse, json, sys
sys.path.insert(0, "."); sys.path.insert(0, "bbkemu/cli/py"); sys.path.insert(0, "tools/font")
from bbkrpg import build, engine_text
from bbkemu import BBKEmu
from sheet import sheet

GAM = "gam4980/retroarch/downloads/bbk/伏魔记.gam"
ROMS = "gam4980/retroarch/system/gam4980"


def shots(gam_path, n, prefix, wait=90):
    """New Game, then capture each gallery item: a message when msgbox has
    drawn it (messages do not wait for a key), anything else after `wait`
    frames, followed by ENTER."""
    from bbkrpg import fontpatch
    _, syms = fontpatch.build_segment([0])
    data_off = int.from_bytes(open(gam_path, "rb").read()[0x42:0x46], "little")
    # the font segment sits right after the engine; find it from the header chain
    font_gam = 0x48000
    mdone = 0x20D000 + font_gam + syms["mdone"] - 0x5000
    paths = []
    with BBKEmu() as e:
        e.load_gam(gam_path, rom_dir=ROMS)
        e.run_frames(1000)
        e.break_add(None, phys=mdone)
        e.tap("ENTER"); e.run_frames(60)
        k = 0
        pending_enter = False
        while k < n:
            r = e.run_frames(wait)
            p = f"{prefix}_{k:02d}.png"
            if r.get("reason") == "breakpoint":
                e.step(400)             # finish restoring and return
            e.screen(p, scale=2); paths.append(p); k += 1
            if r.get("reason") != "breakpoint":
                e.tap("ENTER")
        assert e.call("info")["running"], "game stopped"
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix"); ap.add_argument("ids", nargs="+")
    ap.add_argument("--en", help="JSON {id: english}")
    ap.add_argument("--shots", type=int, default=0)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open("work/fmj.strings.jsonl")] + engine_text.export()
    en = json.load(open(a.en)) if a.en else {}
    for r in rows:
        if r["id"] in en:
            r["en"] = en[r["id"]]
    out, info, problems = build.build(open(GAM, "rb").read(), rows, gallery=a.ids)
    assert not problems, problems
    open(a.prefix + ".gam", "wb").write(out)
    paths = shots(a.prefix + ".gam", a.shots or len(a.ids) + 2, a.prefix)
    sheet(paths, a.prefix + "_sheet.png", 3)
    print(a.prefix + "_sheet.png")
