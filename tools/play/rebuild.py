"""Re-record a route prefix through bbkemu's own recorder (no hand edits).

    python3 tools/play/run.py -f tools/play/rebuild.py   (inside the daemon; set REBUILD_SRC/REBUILD_CUT)

Why: snapshot.load truncates the recorded route to the snapshot's event *count*,
so loading a snapshot that is not an ancestor of the current state (a sibling in
a search tree) leaves the wrong events in the route and replays diverge. When
that happened, this script boots a fresh session, starts route.record on the
route path with resume=False, and re-issues every event of a known-good source
route up to frame CUT with input.press/release/route.mark at the same frames,
so the recorder writes an identical prefix. Then play continues from there.
"""
import json, builtins
import play
from bbkemu import BBKEmu, Hooks

SRC = builtins.REBUILD_SRC
CUT = builtins.REBUILD_CUT
STOP_AT = getattr(builtins, "REBUILD_STOP_AT", CUT)
evs = [json.loads(l) for l in open(SRC)]
assert evs[0].get("route") == 1
e = BBKEmu(play.BIN)
e.load_gam(play.GAM, rom_dir=play.ROMS)
print(e.call("route.record", path=play.ROUTE, resume=False))
n = 0
for ev in evs[1:]:
    f = ev.get("f")
    if f is None or f > CUT or "end" in ev:
        continue
    cur = e.call("info")["frame"]
    if f > cur:
        e.call("run.frames", n=f - cur)
    if "k" in ev:
        e.call("input.press", key=ev["k"])
    elif "up" in ev:
        e.call("input.release")
    elif "mark" in ev:
        e.call("route.mark", text=ev["mark"])
    else:
        raise ValueError(ev)
    n += 1
cur = e.call("info")["frame"]
if STOP_AT > cur:
    e.call("run.frames", n=STOP_AT - cur)
builtins.e, builtins.h = e, Hooks(e)
play.e, play.h = e, builtins.h
print("re-recorded", n, "events; frame", e.call("info")["frame"], e.call("route.status"))
