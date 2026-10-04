"""Event-state maze solver for flag-driven map mazes (伏魔记 三清山 bridges, 原野).

A maze script's tile handlers branch on which "room" event (e.g. 100..128) is set,
then clrevent/setevent and `startchapter`. simulate() runs a handler for a given
set of events; solve() BFSes (script, events) states to a target script.

    python3 tools/play/maze.py 2-32 2-43 --events 100-128
"""
import os, re, sys
from collections import deque

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from bbkrpg import games  # noqa: E402
GUT = games.from_argv().path("gut")


def parse(key):
    lines = open(os.path.join(GUT, "1-%s.gut" % key), encoding="utf-8").read().splitlines()
    ops, labels, events = [], {}, {}
    for l in lines:
        s = l.split(";")[0].rstrip() if not l.lstrip().startswith(("say", "message", "choice", "setscenename")) else l.rstrip()
        if not s.strip():
            continue
        if s.startswith(".event "):
            _, n, lab = s.split()
            events[int(n)] = lab
            continue
        if s.startswith("."):
            continue
        if re.match(r"^L_[0-9a-f]+:", s):
            labels[s[:-1]] = len(ops)
            continue
        t = s.strip()
        op, _, rest = t.partition(" ")
        ops.append((op, [a.strip() for a in rest.split(",")] if rest else []))
    return ops, labels, events


_cache = {}


def script(key):
    if key not in _cache:
        _cache[key] = parse(key)
    return _cache[key]


def simulate(key, ev, flags, maxsteps=500):
    """Run tile handler `ev` (script event number) of script `key` with `flags` set.
    Returns (new_flags, next_script_key or None, notes)."""
    ops, labels, events = script(key)
    if ev not in events:
        return flags, None, ["no handler"]
    pc = labels[events[ev]]
    flags = set(flags)
    notes = []
    nxt = None
    for _ in range(maxsteps):
        if pc >= len(ops):
            break
        op, a = ops[pc]
        pc += 1
        if op == "if":
            if int(a[0]) in flags:
                pc = labels[a[1]]
        elif op == "goto":
            pc = labels[a[0]]
        elif op == "setevent":
            flags.add(int(a[0]))
        elif op == "clrevent":
            flags.discard(int(a[0]))
        elif op == "startchapter":
            nxt = "%s-%s" % (a[0], a[1])
        elif op == "callback":
            break
        elif op in ("enterfight", "gameover", "choice", "usegoods"):
            notes.append(op)
            if op == "gameover":
                break
        elif op in ("say", "message"):
            notes.append(op)
    return flags, nxt, notes


def exits(key):
    _, _, events = script(key)
    return sorted(k for k in events if k > 40)


def solve(start, goal, flags=frozenset(), mask=range(100, 129)):
    mask = set(mask)
    s0 = (start, frozenset(f for f in flags if f in mask))
    prev = {s0: None}
    q = deque([s0])
    while q:
        cur = q.popleft()
        key, fl = cur
        if key == goal:
            path = []
            while prev[cur]:
                cur, step = prev[cur]
                path.append(step)
            return path[::-1]
        for ev in exits(key):
            nf, nxt, notes = simulate(key, ev, fl)
            if not nxt:
                continue
            st = (nxt, frozenset(f for f in nf if f in mask))
            if st not in prev:
                prev[st] = (cur, (key, ev - 40, nxt, sorted(st[1]), notes))
                q.append(st)
    return None


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    lo, hi = 100, 128
    if "--events" in sys.argv:
        lo, hi = map(int, sys.argv[sys.argv.index("--events") + 1].split("-"))
    fl = set()
    if "--flags" in sys.argv:
        fl = set(map(int, sys.argv[sys.argv.index("--flags") + 1].split(",")))
    p = solve(a, b, fl, range(lo, hi + 1))
    if p is None:
        print("no path")
    else:
        for s in p:
            print("in %s take tile %d -> %s  flags %s %s" % s)
