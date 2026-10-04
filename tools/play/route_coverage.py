"""Replay a route headlessly and list the string-table rows it draws.

    python3 tools/play/route_coverage.py [route] [--bin path]
Writes work/playthrough/route_seen.json and prints say-row coverage.
"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu/cli/py"))
from bbkemu import BBKEmu, Hooks  # noqa: E402

route = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(ROOT, "routes/fmj.agent.route.jsonl")
binp = os.path.join(ROOT, "bbkemu/target/release/bbkemu")
if "--bin" in sys.argv:
    binp = sys.argv[sys.argv.index("--bin") + 1]
rows = {}
for l in open(os.path.join(ROOT, "work/fmj.strings.jsonl"), encoding="utf-8"):
    r = json.loads(l)
    rows[r["id"]] = r
last = 0
for l in open(route):
    j = json.loads(l)
    last = max(last, j.get("f", 0))
e = BBKEmu(binp)
e.load_gam(os.path.join(ROOT, "gam4980/retroarch/downloads/bbk/伏魔记.gam"), rom_dir=os.path.join(ROOT, "gam4980/retroarch/system/gam4980"))
h = Hooks(e)
e.call("input.replay", path=route, run=False)
seen, lines = set(), []
f = 0
while f < last + 60:
    e.run_frames(500)
    f = e.call("info")["frame"]
    for d in h.drain():
        if d["script"]:
            rid = "gut/%s@%04x" % d["script"]
            if rid in rows:
                seen.add(rid)
            lines.append((d["frame"], rid, d["text"].rstrip()))
say = {k for k, r in rows.items() if r["kind"] == "say"}
json.dump(sorted(seen), open(os.path.join(ROOT, "work/playthrough/route_seen.json"), "w"), indent=0)
print("frames", f, "rows", len(seen), "say", len(seen & say), "/", len(say), "%.1f%%" % (100 * len(seen & say) / len(say)))
print("hash", e.screen()["hash"])
