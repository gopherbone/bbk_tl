"""Gallery sweep: show every script row of the English build and check it.

  python3 tools/qa/sweep.py [--game fmj] [--batch 40] [--kinds say,message,choice,menu] [--only N]
For each batch of row ids: build a gallery .gam, play it (ENTER through every
page), log what the English renderer drew (EnHooks), and check that each
expected page/message/choice text was drawn and that no CJK text appeared.
Writes <qa>/sweep/batch_NN_sheet.png and <qa>/sweep/report.json (qa dir from
the game profile, work/qa for fmj).
"""
import argparse, json, os, re, sys
sys.path.insert(0, "."); sys.path.insert(0, "bbkemu/cli/py"); sys.path.insert(0, "tools/font")
from bbkrpg import build, engine_text, fit, games
from bbkemu import BBKEmu, EnHooks
from sheet import sheet

GAME = games.from_argv()
ROMS = games.ROMS
OUT = f"{GAME.qa}/sweep"
CJK = re.compile(r"[　-鿿＀-￯]")

ap = argparse.ArgumentParser()
ap.add_argument("--batch", type=int, default=40)
ap.add_argument("--kinds", default="say,message,choice,menu")
ap.add_argument("--only", type=int)
a = ap.parse_args()
os.makedirs(OUT, exist_ok=True)

rows = [json.loads(l) for l in open(GAME.strings)] + engine_text.export(GAME.engine)
en = {d["id"]: d["en"] for d in map(json.loads, open(GAME.merged))}
for r in rows:
    r["en"] = en.get(r["id"], "")
kinds = set(a.kinds.split(","))
ids = []
for r in rows:
    if r["id"].startswith("gut/") and r["kind"] in kinds:
        base = r["id"].split(".")[0] if r["kind"] == "choice" else r["id"]
        if base not in ids:
            ids.append(base)


def expected(rid):
    if "@" in rid and rid + ".1" in en:              # choice
        return [en[rid + ".1"], en[rid + ".2"]], "choice"
    r = next(x for x in rows if x["id"] == rid)
    if r["kind"] == "say":
        return ["\n".join(p) for p in fit.pages(r["en"], bool(r["ctx"].get("pic")))], "say"
    if r["kind"] == "message":
        return ["\n".join(fit.rows(r["en"], fit.MESSAGE_WIDTH))], "message"
    if r["kind"] == "menu":
        return r["en"].split(" "), "menu"
    if r["kind"] == "showgut":                       # the scroll is logged row by row
        return [l.strip() for l in r["en"].split("\n") if l.strip()], "showgut"
    return [r["en"]], r["kind"]


def budget(rid):
    """ENTER presses (70 frames apart) to give a row: one per page; a scroll
    moves about one row per two presses whatever the keys do."""
    exp, kind = expected(rid)
    return 1 if kind == "menu" else 2 * len(exp) if kind == "showgut" else len(exp)


orig = GAME.read_gam()
report = json.load(open(f"{OUT}/report.json")) if os.path.exists(f"{OUT}/report.json") else {}
batches = [ids[i:i + a.batch] for i in range(0, len(ids), a.batch)]
for bn, batch in enumerate(batches):
    if a.only is not None and bn != a.only:
        continue
    out, info, probs = build.build(orig, rows, gallery=batch, game=GAME)
    assert not probs, probs
    path = f"{OUT}/batch_{bn:02d}.gam"
    open(path, "wb").write(out)
    json.dump({"bank": info["bank"]}, open(path[:-4] + ".bank.json", "w"))
    pages = sum(budget(i) for i in batch)
    shots, drawn = [], []
    with BBKEmu() as e:
        e.load_gam(path, rom_dir=ROMS)
        h = EnHooks(e, path[:-4] + ".bank.json")
        e.run_frames(1000)
        e.tap("ENTER"); e.run_frames(120)
        for k in range(pages + 8):
            drawn += h.drain()
            if k % 2 == 0 and len(shots) < 36:
                p = f"{OUT}/b{bn:02d}_{k:03d}.png"; e.screen(p, scale=1); shots.append(p)
            e.tap("ENTER"); e.run_frames(70)
        drawn += h.drain()
        alive = e.call("info")["running"]
    texts = [d["text"] for d in drawn]
    joined = "\n\x00".join(texts)
    for rid in batch:
        exp, kind = expected(rid)
        missing = [x for x in exp if x and x not in joined]
        report[rid] = {"kind": kind, "missing": missing}
    cjk = sorted({t for t in texts if CJK.search(t)})
    sheet(shots, f"{OUT}/batch_{bn:02d}_sheet.png", 6)
    for p in shots:
        os.remove(p)
    bad = [i for i in batch if report[i]["missing"]]
    print(f"batch {bn:02d}: {len(batch)} rows, {pages} pages, alive={alive}, missing={len(bad)}, cjk={len(cjk)}")
    for i in bad[:5]:
        print("   missing", i, report[i]["missing"][:1])
    for t in cjk[:3]:
        print("   cjk", repr(t[:40]))
    json.dump(report, open(f"{OUT}/report.json", "w"), ensure_ascii=False, indent=0)
