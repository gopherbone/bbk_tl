"""MAP resources of the current game (BBK_GAME, default fmj): walkability +
tile events, and BFS path finding.

Map resource (BBKRPGSimulator ResMap): [0]=type [1]=index [2]=til index
[3..] name (GB2312, NUL), [0x10]=width [0x11]=height, then w*h 2-byte cells:
low byte bit7 = walkable, low 7 bits = tile; high byte = event number (0 none).
Map ids in `loadmap a, b, x, y` are MAP keys (2, a, b); x, y = view origin.
"""
import os, sys
from collections import deque

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from bbkrpg import games, lib as libmod, gam as gammod  # noqa: E402

_LIB = None


def lib():
    global _LIB
    if _LIB is None:
        data = games.get().read_gam()
        raw, _ = gammod.split(data)
        _LIB = libmod.parse(raw)
    return _LIB


class Map:
    def __init__(self, a, b):
        buf = lib().res[(2, a, b)]
        self.key = (a, b)
        self.name = buf[3:0x10].split(b"\0")[0].decode("gb2312", "replace")
        self.w, self.h = buf[0x10], buf[0x11]
        self.d = buf[0x12:0x12 + self.w * self.h * 2]

    def walk(self, x, y):
        # the player's tile is view origin + (4, 3); the view stays on the map
        if not (4 <= x < self.w - 4 and 3 <= y < self.h - 2):
            return False
        return bool(self.d[(y * self.w + x) * 2] & 0x80)

    def event(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return -1
        return self.d[(y * self.w + x) * 2 + 1]

    def events(self):
        out = {}
        for y in range(self.h):
            for x in range(self.w):
                ev = self.event(x, y)
                if ev:
                    out.setdefault(ev, []).append((x, y))
        return out

    def show(self, me=None, marks=None):
        marks = marks or {}
        rows = []
        for y in range(self.h):
            r = "%2d " % y
            for x in range(self.w):
                if me == (x, y):
                    c = "@"
                elif (x, y) in marks:
                    c = marks[(x, y)]
                elif self.event(x, y):
                    ev = self.event(x, y)
                    c = chr(ord("A") + ev - 41) if ev >= 41 else "%d" % (ev % 10)
                else:
                    c = "." if self.walk(x, y) else "#"
                r += c
            rows.append(r)
        hdr = "   " + "".join(str(x % 10) for x in range(self.w))
        return "%s %dx%d\n%s\n%s" % (self.name, self.w, self.h, hdr, "\n".join(rows))

    def path(self, start, goal, blocked=()):
        """BFS over walkable cells; goal may be unwalkable (adjacent stop)."""
        prev = {start: None}
        q = deque([start])
        goals = goal if isinstance(goal, (set, list)) else [goal]
        goals = set(goals)
        while q:
            p = q.popleft()
            if p in goals:
                break
            for dx, dy, k in ((1, 0, "RIGHT"), (-1, 0, "LEFT"), (0, 1, "DOWN"), (0, -1, "UP")):
                n = (p[0] + dx, p[1] + dy)
                if n in prev or n in blocked:
                    continue
                if self.walk(*n) or n in goals:
                    prev[n] = (p, k)
                    q.append(n)
        else:
            return None
        steps = []
        while prev[p] is not None:
            p, k = prev[p]
            steps.append(k)
        return steps[::-1]


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    m = Map(a, b)
    print(m.show())
    print(m.events())
