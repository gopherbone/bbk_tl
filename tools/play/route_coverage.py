"""Replay a route headlessly and list the string-table rows it draws.

    python3 tools/play/route_coverage.py [--game fmj] [route] [--bin path]
Writes <playthrough>/route_seen.json and prints say-row coverage.
"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu/cli/py"))
sys.path.insert(0, ROOT)
from bbkemu import BBKEmu, Hooks  # noqa: E402
from bbkrpg import games  # noqa: E402

game = games.from_argv()
route = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else game.path("route")
binp = os.path.join(ROOT, "bbkemu/target/release/bbkemu")
if "--bin" in sys.argv:
    binp = sys.argv[sys.argv.index("--bin") + 1]
rows = {}
for l in open(game.path("strings"), encoding="utf-8"):
    r = json.loads(l)
    rows[r["id"]] = r
last = 0
for l in open(route):
    j = json.loads(l)
    last = max(last, j.get("f", 0))
e = BBKEmu(binp)
e.load_gam(game.path("gam"), rom_dir=game.path("roms"))
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
json.dump(sorted(seen), open(os.path.join(game.path("playthrough"), "route_seen.json"), "w"), indent=0)
print("frames", f, "rows", len(seen), "say", len(seen & say), "/", len(say), "%.1f%%" % (100 * len(seen & say) / len(say)))
print("hash", e.screen()["hash"])
