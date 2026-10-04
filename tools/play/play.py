"""Helpers for playing 伏魔记 in bbkemu while recording a route.

Used inside the daemon namespace (tools/play/daemon.py) or directly:
    from play import *; start()
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu", "cli", "py"))
from bbkemu import BBKEmu, Hooks  # noqa: E402

GAM = os.path.join(ROOT, "gam4980/retroarch/downloads/bbk/伏魔记.gam")
ROMS = os.path.join(ROOT, "gam4980/retroarch/system/gam4980")
ROUTE = os.path.join(ROOT, "routes/fmj.agent.route.jsonl")
SEEN = os.path.join(ROOT, "work/playthrough/seen.json")
SHOTS = os.path.join(ROOT, "work/playthrough/shots")
STRINGS = os.path.join(ROOT, "work/fmj.strings.jsonl")
# The stock bbkemu hangs at frame ~3540 (RTC alarm IRQ storm: IRQ entry does not
# set the I flag), and load_gam clobbers gam 0x30f8..0x30ff (engine code) with a
# save-area marker (fixed in bbkemu/core since commit "core: fix IRQ I flag...").
BIN = os.environ.get("BBKEMU_BIN", os.path.join(ROOT, "bbkemu/target/release/bbkemu"))

import builtins as _b
e = getattr(_b, "e", None)
h = getattr(_b, "h", None)
_PRIVATE = {"e", "h"}
seen = set()
log = []          # every drawn line this session: (frame, row id or None, text)

ROWS = {}
for _l in open(STRINGS, encoding="utf-8"):
    _r = json.loads(_l)
    ROWS[_r["id"]] = _r
SAY_IDS = {k for k, r in ROWS.items() if r["kind"] == "say"}
# engine-drawn resource text (item/actor/magic names, descriptions) by text
NAME_IDX = {}
DESC_ROWS = []
for _k, _r in ROWS.items():
    if _r["kind"] in ("grs.name", "ars.name", "mrs.name", "map.name"):
        NAME_IDX.setdefault(_r["zh"].strip(), []).append(_k)
    elif _r["kind"] in ("grs.desc", "mrs.desc"):
        DESC_ROWS.append((_k, _r["zh"]))
if os.path.exists(SEEN):
    seen = set(json.load(open(SEEN)))


def _load_seen():
    global seen
    if os.path.exists(SEEN):
        seen = set(json.load(open(SEEN)))


def save_seen():
    json.dump(sorted(seen), open(SEEN, "w"), indent=0)


def start(record=True):
    """Boot, replay/resume the route, install hooks."""
    global e, h
    _load_seen()
    e = BBKEmu(BIN)
    e.load_gam(GAM, rom_dir=ROMS)
    if record:
        r = e.call("route.record", path=ROUTE)
        print("route.record:", r)
    h = Hooks(e)
    import builtins
    builtins.e, builtins.h = e, h
    print("frame", frame())


WATCH_LOG = []  # watchpoint hits drained by poll()
LAST_HIT = {}   # breakpoint id -> last frame it fired (non-hook breakpoints)


def _drain():
    """Hooks.drain, but also remembers when other silent breakpoints fired."""
    from bbkemu import _gb
    out = []
    for x in e.call("break.log", clear=True, max=100000)["entries"]:
        if x["id"] == h.fetch_id:
            pos_ = h._script_pos(x["mem"][0])
            if pos_:
                h.where = pos_
        elif x["id"] == h.text_id:
            args = bytes.fromhex(x["mem"][1])
            out.append({"frame": x["frame"], "y": args[0], "text": _gb(x["mem"][0]),
                        "raw": x["mem"][0], "args": x["mem"][1], "script": h.where})
        elif "frame" in x:
            LAST_HIT[x["id"]] = x["frame"]
        else:
            WATCH_LOG.append(x)   # watchpoint hit (watch.add log=True)
    return out


def frame():
    return e.call("info")["frame"]


def poll(quiet=False):
    """Drain drawn text, update coverage, print new lines."""
    out = []
    printed = set()
    for d in _drain():
        rid = None
        if d["script"]:
            rid = "gut/%s@%04x" % d["script"]
        txt = d["text"].rstrip()
        if rid in ROWS:
            seen.add(rid)
        t = txt.strip()
        if t in NAME_IDX:
            seen.update(NAME_IDX[t])
        elif len(t) >= 4:
            for k, z in DESC_ROWS:
                if z.startswith(t):
                    seen.add(k)
        log.append((d["frame"], rid, txt))
        out.append((rid, txt))
        if not quiet and txt not in printed:
            printed.add(txt)
            print("  [%s] %s" % (rid, txt))
    save_seen()
    return out


def tap(key, hold=4, wait=4, n=1, quiet=False):
    for _ in range(n):
        e.tap(key, hold=hold, wait=wait)
    return poll(quiet)


def wait(n):
    e.run_frames(n)
    return poll()


def shot(name="s", scale=2):
    p = os.path.join(SHOTS, name + ".png")
    e.screen(p, scale=scale)
    return p


def hash_():
    return e.screen()["hash"]


def coverage():
    s = len(seen & SAY_IDS)
    print("say rows seen: %d / %d (%.1f%%); all rows seen: %d / %d" % (
        s, len(SAY_IDS), 100.0 * s / len(SAY_IDS), len(seen), len(ROWS)))


def mark(text):
    e.call("route.mark", text=text)


def stop():
    e.call("route.stop")
    save_seen()



# --- RAM ------------------------------------------------------------------
# 0x1979 map type, 0x197a map index (MAP key (2, a, b) = `loadmap a, b`)
# 0x197c/0x197d view origin x/y; player tile = origin + (4, 3)
# 0x197e/0x197f map width/height
def pos():
    b = e.read(0x1979, 7)
    return (b[3] + 4, b[4] + 3)


def mapid():
    b = e.read(0x1979, 2)
    return (b[0], b[1])


def stack():
    sp = int(e.regs()["sp"], 16)
    return e.read(0x100 + sp + 1, 0xff - sp).hex()


# --- walking ----------------------------------------------------------------
import maps as _maps  # noqa: E402
_mapcache = {}


def curmap():
    k = mapid()
    if k not in _mapcache:
        _mapcache[k] = _maps.Map(*k)
    return _mapcache[k]


def step(k, quiet=False):
    """One tile step (10 frames). Returns text drawn (list) or [] ."""
    e.tap(k, hold=2, wait=8)
    return poll(quiet)


def walk(keys, quiet=False):
    """Walk a key list; stop early if the position doesn't change or text appears."""
    for i, k in enumerate(keys):
        p0, m0 = pos(), mapid()
        out = step(k, quiet)
        if out or mapid() != m0:
            return ("event", i, out)
        if pos() == p0 and in_battle():
            return ("fight", i, fight(quiet=quiet))
        if pos() == p0:
            out = step(k, quiet)
            if out or mapid() != m0:
                return ("event", i, out)
            if pos() == p0:
                return ("blocked", i, k)
    return ("ok", len(keys), None)


def _event_cells(m, keep=()):
    return {c for cs in m.events().values() for c in cs} - set(keep)


def goto(x, y, blocked=(), quiet=False):
    for _ in range(10):
        m = curmap()
        p = m.path(pos(), (x, y), blocked=set(blocked) | _event_cells(m, [(x, y)]) | (blockers() - {(x, y)}))
        if p is None:
            return ("nopath", 0, None)
        r = walk(p, quiet)
        if r[0] != "fight":
            return r
        print("  fight:", r[2])
    return r


def show(marks=None):
    print(curmap().show(me=pos(), marks=marks))



# --- dialogue ----------------------------------------------------------------
KEYWAIT_PC = "e9e317"   # OS wait-for-key; on the free map the hardware sp is 0xe8
IDLE_SP = 0xE8


def cpu():
    r = e.regs()
    return r["pc_phys"], int(r["sp"], 16)


def waitstate(n=8):
    """Sample n frames: 'idle' (free map), 'key' (waiting a key in a box/menu), 'busy'."""
    sps = set()
    e.run_frames(2)
    for _ in range(n):
        e.run_frames(1)
        pc, sp = cpu()
        if pc == KEYWAIT_PC:
            sps.add(sp)
    if sps - {IDLE_SP}:
        return "key"
    if IDLE_SP in sps:
        return "idle"
    return "busy"


def idle():
    return waitstate() == "idle"


BATTLE_FRAMES = ("12d3e709", "12d3e33b")   # far-call frames under the battle key wait


def in_battle():
    """At a key wait whose call stack is the battle command loop."""
    for _ in range(40):
        e.run_frames(3)
        pc, sp = cpu()
        if pc == KEYWAIT_PC:
            st = stack()
            return any(f in st for f in BATTLE_FRAMES)
    return False


AUTO_FIGHT = True   # adv(): spam-attack battles that come up. Set False before scripted boss fights.


def adv(max_taps=80, quiet=False, key="ENTER"):
    """Press ENTER until back on the free map. Returns drawn lines.
    Stops (and prints STUCK) when 3 taps in a row draw nothing new: a menu/shop."""
    out = []
    texts = set()
    stale = 0
    for _ in range(max_taps):
        st = waitstate()
        out += poll(quiet)
        if st == "idle":
            break
        if st == "busy":
            e.run_frames(10)
            continue
        if in_battle():
            if wheel_shown() and not AUTO_FIGHT:
                print("adv: battle wheel (AUTO_FIGHT off)")
                break
            out += [(None, t) for t in fight(quiet=quiet)]
            continue
        e.tap(key, hold=2, wait=10)
        new = poll(quiet)
        out += new
        if any(t in ("耗真气:", "数量：") for _, t in new):
            # ENTER opened the battle magic/item menu: we are in a fight
            e.tap("EXIT", hold=2, wait=10)
            out += [(None, t) for t in fight(quiet=quiet)]
            continue
        fresh = [t for t in new if t not in texts]
        texts.update(new)
        stale = 0 if fresh else stale + 1
        if stale >= 3:
            print("adv: STUCK (menu/shop?)")
            break
    return out


def talk(direction=None, quiet=False):
    """Face direction (if given) and press ENTER, then advance the dialogue."""
    if direction:
        e.tap(direction, hold=2, wait=8)
    e.tap("ENTER", hold=2, wait=10)
    return adv(quiet=quiet)



# --- NPCs --------------------------------------------------------------------
# Map objects (NPCs, boxes) are heap records: "75 6e 20 00" (heap tag), then
# +4 kind (2 npc, 3 npc variant, 4 box), +5 actor type, +9/+10 tile x/y,
# +11/+12 initial x/y, +13 name (GB2312). Found by scanning 0x3000-0x7fff.
_TAG = bytes.fromhex("756e2000")


def objs():
    m = e.read(0x3000, 0x5000)
    out = []
    i = m.find(_TAG)
    while i >= 0:
        r = m[i:i + 0x20]
        if len(r) >= 0x14 and r[4] in (2, 3, 4) and r[9] < 128 and r[10] < 128:
            name = r[13:r.find(b"\0", 13)] if b"\0" in r[13:] else b""
            out.append({"addr": 0x3000 + i, "kind": r[4], "type": r[5], "x": r[9], "y": r[10],
                        "x0": r[11], "y0": r[12], "name": name.decode("gb2312", "replace")})
        i = m.find(_TAG, i + 4)
    return out


def npcs():
    """{(x0, y0): (x, y)} for NPCs, keyed by their createnpc position."""
    return {(o["x0"], o["y0"]): (o["x"], o["y"]) for o in objs() if o["kind"] in (2, 3)}


def blockers():
    return {(o["x"], o["y"]) for o in objs()}


_DIRS = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}


def goto_adj(x, y, tries=4, quiet=False):
    """Walk next to (x, y) and face it."""
    for _ in range(tries):
        m = curmap()
        others = blockers() - {(x, y)}
        goals = [(x + dx, y + dy) for dx, dy in _DIRS if m.walk(x + dx, y + dy) and (x + dx, y + dy) not in others]
        p = m.path(pos(), set(goals), blocked=others | _event_cells(m, goals))
        if p is None:
            return False
        r = walk(p, quiet)
        if r[0] == "event":
            return r
        px, py = pos()
        d = (x - px, y - py)
        if d in _DIRS:
            e.tap(_DIRS[d], hold=2, wait=8)
            return True
    return False


def talk_npc(i, quiet=False):
    """i = the NPC's createnpc position (x0, y0)."""
    for _ in range(4):
        n = npcs().get(i)
        if not n:
            return None
        r = goto_adj(*n, quiet=quiet)
        if r is not True:
            return r
        if npcs().get(i) != n:
            continue
        return press_enter(quiet)
    return None


def press_enter(quiet=False, tries=3):
    """ENTER (retrying when nothing happens), then advance the dialogue."""
    for _ in range(tries):
        e.run_frames(6)
        e.tap("ENTER", hold=2, wait=12)
        out = poll(quiet)
        if out or waitstate() != "idle":
            return out + adv(quiet=quiet)
    return []


def open_box(x, y, quiet=False):
    r = goto_adj(x, y, quiet=quiet)
    if r is not True:
        return r
    return press_enter(quiet)



# --- scripts -------------------------------------------------------------------
import re as _re
GUT_DIR = os.path.join(ROOT, "work/fmj_gut")


def gut(key):
    return open(os.path.join(GUT_DIR, key + ".gut"), encoding="utf-8").read()


def boxes(key):
    """createbox id, type, x, y in a script's init part."""
    return [tuple(map(int, m)) for m in _re.findall(r"createbox (\d+), (\d+), (\d+), (\d+)", gut(key))]


def loot(key, quiet=False):
    out = []
    for bid, _t, x, y in boxes(key):
        r = open_box(x, y, quiet=quiet)
        out.append(((x, y), r if not isinstance(r, list) else [t for _, t in r]))
    return out


def exit_room(ev=1, quiet=False):
    """Walk onto the room's tile event `ev` (script event 40+ev)."""
    m = curmap()
    cells = m.events().get(ev, [])
    for c in cells:
        r = goto(*c, quiet=quiet)
        adv(quiet=quiet)
        return r



def enter_door(ev, quiet=False, tries=8, once=False):
    """Trigger map tile event `ev` (script event 40+ev): step onto it, or walk
    into it when it is not walkable. Returns True when the map changed."""
    m0 = mapid()
    for _ in range(tries):
        m = curmap()
        for c in m.events().get(ev, []):
            if m.walk(*c):
                goto(*c, quiet=quiet)
            else:
                r = goto_adj(*c, quiet=quiet)
                px, py = pos()
                if r is True and mapid() == m0 and (c[0] - px, c[1] - py) in _DIRS:
                    e.tap(_DIRS[(c[0] - px, c[1] - py)], hold=2, wait=8)
            adv(quiet=quiet)
            if mapid() != m0 or once:
                return mapid() != m0
        e.run_frames(40)
    return False



# --- battles -------------------------------------------------------------------
FIGHTS = []   # (frame, texts) per battle
FLEE = False  # fight(): try 逃跑 instead of attacking (e.g. to avoid exp before a scripted fight)


def fight(quiet=True, max_rounds=200):
    """Spam ENTER (attack the default target) until back on the free map.
    Returns the texts drawn. Assumes the default command (attack) wins."""
    texts = []
    for _ in range(max_rounds):
        st = waitstate()
        texts += [t for _, t in poll(quiet)]
        if st == "idle":
            break
        if st == "busy" and wheel_shown():
            st = "key"      # 2nd member's wheel can wait outside the OS key wait (pc 227d3c)
        if st == "key":
            # battle wheel: UP = attack (sword), LEFT = magic, RIGHT = items,
            # DOWN = flee/other. UP is harmless on message boxes.
            if FLEE and wheel_shown():
                # DOWN -> 围攻/道具/防御/逃跑/状态: 逃跑 is the 4th entry
                for k in ("DOWN", "ENTER", "DOWN", "DOWN", "DOWN", "ENTER"):
                    e.tap(k, hold=2, wait=20)
                e.run_frames(30)
                continue
            e.tap("UP", hold=2, wait=6)
            e.tap("ENTER", hold=2, wait=20)
        else:
            e.run_frames(20)
    texts += [t for _, t in poll(quiet)]
    FIGHTS.append((frame(), texts))
    if not quiet:
        print("fight:", texts)
    return texts



def stats():
    """Hero record: heap block after the name record "柳清风"."""
    m = e.read(0x3000, 0x5000)
    i = m.find("柳清风".encode("gb2312"))
    if i < 0:
        return None
    j = m.find(bytes.fromhex("756e1c00"), i)
    r = m[j + 4:j + 0x20]
    w = lambda k: r[k] | r[k + 1] << 8
    return {"hpmax": w(6), "hp": w(8), "mpmax": w(10), "mp": w(12), "atk": w(14), "def": w(16),
            "lv": r[3] if False else None, "addr": hex(0x3000 + j)}



def lamp_cave(n, quiet=True):
    """伏魔洞 lamp cave n (1..8): loot boxes, fight the lamp guardian, leave."""
    assert enter_door(n + 1, quiet=quiet), "could not enter cave %d" % n
    res = {"map": mapid()}
    os_ = objs()
    for o in os_:
        if "宝箱" in o["name"]:
            r = open_box(o["x"], o["y"], quiet=quiet)
            res.setdefault("boxes", []).append((o["name"], r if not isinstance(r, list) else [t for _, t in r]))
    for o in os_:
        if o["name"] == "伏魔灯":
            for _ in range(5):
                r = open_box(o["x"], o["y"], quiet=quiet)
                if isinstance(r, list) and r:
                    break
            res["lamp"] = r if not isinstance(r, list) else [t for _, t in r]
    ex = 1 if n <= 4 else 2   # caves 5-8 are mirrored: the stairs are tile 2
    for _ in range(3):
        res["exit"] = enter_door(ex, quiet=quiet)
        if res["exit"]:
            break
    res["stats"] = stats()
    return res



def wheel_shown():
    """Battle command wheel + HP box on screen (HP box top border in LCD RAM)."""
    m = e.read(0x400 + 69 * 32, 3 * 32)
    return m[9:14] == b"\xff" * 5 and (m[2 * 32 + 14] & 0x10) != 0


def fight2(heal_below=0.45, quiet=True, max_rounds=400, log_hp=False):
    """Battle loop: at the command wheel cast 气疗术 (magic slot 1, on self)
    when HP is low, else attack the default target. Returns texts."""
    texts = []
    for _ in range(max_rounds):
        st = waitstate()
        texts += [t for _, t in poll(quiet)]
        if st == "idle":
            break
        if st == "busy":
            e.run_frames(10)
            continue
        if wheel_shown():
            s_ = stats() or {}
            if log_hp:
                print("  hp", s_.get("hp"), "/", s_.get("hpmax"), "mp", s_.get("mp"))
            if s_ and s_["hp"] < heal_below * s_["hpmax"] and s_["mp"] >= 36:
                for k, w in (("LEFT", 20), ("ENTER", 40), ("ENTER", 40), ("ENTER", 60)):
                    e.tap(k, hold=2, wait=w)
            else:
                e.tap("UP", hold=2, wait=8)
                e.tap("ENTER", hold=2, wait=30)
        else:
            e.tap("ENTER", hold=2, wait=20)
    texts += [t for _, t in poll(quiet)]
    FIGHTS.append((frame(), texts))
    return texts



# battle wheel actions (UP attack, LEFT magic, DOWN misc: 围攻/道具/防御/逃跑/状态,
# RIGHT 合击). 道具 -> 装备/投掷/使用 -> item list (cursor starts at the top).
def act_attack():
    e.tap("UP", hold=2, wait=8)
    e.tap("ENTER", hold=2, wait=30)
    e.tap("ENTER", hold=2, wait=30)   # default target when several enemies


def act_heal_magic():
    for k, w in (("LEFT", 20), ("ENTER", 40), ("ENTER", 40), ("ENTER", 60)):
        e.tap(k, hold=2, wait=w)


def act_item(kind, idx):
    """kind 1 = 投掷 (throw), 2 = 使用 (use); idx = position in that list."""
    for k, w in [("DOWN", 20), ("ENTER", 40), ("DOWN", 20), ("ENTER", 40)] + [("DOWN", 20)] * kind + [("ENTER", 50)]:
        e.tap(k, hold=2, wait=w)
    for _ in range(idx):
        e.tap("DOWN", hold=2, wait=25)
    e.tap("ENTER", hold=2, wait=40)
    e.tap("ENTER", hold=2, wait=40)


def fight3(plan=(), heal_below=0.5, quiet=True, max_rounds=400, log_hp=True):
    """Like fight2, but the first turns follow `plan` (callables)."""
    plan = list(plan)
    texts = []
    for _ in range(max_rounds):
        st = waitstate()
        texts += [t for _, t in poll(quiet)]
        if st == "idle":
            break
        if st == "busy":
            e.run_frames(10)
            continue
        if wheel_shown():
            s_ = stats() or {}
            if log_hp:
                print("  hp", s_.get("hp"), "/", s_.get("hpmax"), "mp", s_.get("mp"), "plan", len(plan))
            if s_ and s_["hp"] < heal_below * s_["hpmax"] and s_["mp"] >= 36:
                act_heal_magic()
            elif plan:
                plan.pop(0)()
            else:
                act_attack()
        else:
            e.tap("ENTER", hold=2, wait=20)
        if "引：" in texts:
            print("GAME OVER")
            break
    texts += [t for _, t in poll(quiet)]
    FIGHTS.append((frame(), texts))
    return texts




def to_wheel(max_taps=30, quiet=False):
    """ENTER through dialogue until the battle command wheel is shown."""
    for _ in range(max_taps):
        if wheel_shown():
            return True
        st = waitstate()
        poll(quiet)
        if wheel_shown():
            return True
        if st == "idle":
            return False
        e.tap("ENTER", hold=2, wait=20)
    return wheel_shown()




def wait_wheel(max_frames=3000):
    """Run until the battle wheel waits for a key ("wheel"), the free map ("idle"),
    or a key wait that is neither for 90+ frames ("msg": results/dialogue box)."""
    n = 0
    still = 0
    while n < max_frames:
        e.run_frames(5)
        n += 5
        pc, sp = cpu()
        if pc == KEYWAIT_PC:
            if wheel_shown():
                e.run_frames(2)
                if wheel_shown() and cpu()[0] == KEYWAIT_PC:
                    return "wheel"
            elif sp == IDLE_SP:
                return "idle"
            still += 5
            if still >= 90:
                return "msg"
        else:
            still = 0
    return None


def turn(*keys, quiet=True):
    """Press keys (each with a 25-frame wait) from the wheel, then wait for the next wheel."""
    for k in keys:
        e.tap(k, hold=2, wait=25)
    r = wait_wheel()
    t = [x for _, x in poll(quiet)]
    s_ = stats() or {}
    print("turn", keys, "->", r, "hp", s_.get("hp"), "mp", s_.get("mp"), mons(), t[:12])
    return r




MON_BASE, MON_STRIDE = 0x1826, 0x33   # battle monster records (ARS type-3 layout)


def mons(n=3):
    """[(name, hp, maxhp)] of the battle's monsters (records copied from ARS)."""
    out = []
    for i in range(n):
        r = e.read(MON_BASE + i * MON_STRIDE, MON_STRIDE)
        if r[0] != 3:
            break
        name = r[6:0x12].split(b"\0")[0].decode("gb2312", "replace")
        out.append((name, r[0x1a] | r[0x1b] << 8, r[0x18] | r[0x19] << 8))
    return out




# battle action key sequences (from the command wheel)
A_ATTACK = ("UP", "ENTER")    # the hero's sword hits a group: no target step


def A_ATK(ix=0):
    """Single-target attack (慕容小梅): wheel, then pick the target."""
    return ("UP", "ENTER", None) + ("RIGHT",) * ix + ("ENTER",)
A_HEAL = ("LEFT", "ENTER", "ENTER", "ENTER")   # 气疗术 (first magic) on self


def A_USE(i):
    """道具/使用 list item i (cursor reset by UPs), on the hero."""
    return ("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "DOWN", "ENTER", None) + ("UP",) * 14 + ("DOWN",) * i + ("ENTER", "ENTER")


def A_THROW(i, right=0):
    """道具/投掷 list item i at target (default first, RIGHT moves)."""
    return ("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "ENTER", None) + ("UP",) * 12 + ("DOWN",) * i + ("ENTER",) + ("RIGHT",) * right + ("ENTER",)


def act(keys, delay=0, w=26):
    if delay:
        e.run_frames(delay)
    if callable(keys):
        keys()
        keys = ()
    for k in keys:
        if k is None:
            e.run_frames(30)   # let a list finish drawing (first key is dropped otherwise)
        else:
            e.tap(k, hold=2, wait=w)
    r = wait_wheel()
    poll(True)
    return r




def bstate():
    s_ = stats() or {}
    return sum(h_ for _, h_, _m in mons()), s_.get("hp", 0), s_.get("mp", 0), mons()


def best_round(keys, delays=(0, 2, 5, 9, 14, 20), w_hp=1.5, tag="br"):
    """Try `keys` after each delay from a saved state; keep the best outcome.
    Score = enemy HP removed - w_hp * hero HP lost (+ big bonus on a win)."""
    e.call("snapshot.save", name=tag)
    m0, h0, _, _ = bstate()
    best = None
    for d in delays:
        e.call("snapshot.load", name=tag)
        r = act(keys, delay=d)
        m1, h1, mp1, ms = bstate()
        if r != "wheel":
            sc = 1e6 if (h1 > 0 and m1 == 0) or r == "idle" else (-1e6 if h1 == 0 else 0)
            if r == "msg" and h1 > 0:
                sc = 1e6
        else:
            sc = (m0 - m1) - w_hp * (h0 - h1)
        if best is None or sc > best[0]:
            best = (sc, d, r)
        if sc >= 1e6:
            break
    e.call("snapshot.load", name=tag)
    r = act(keys, delay=best[1])
    print("round", keys[:2], "delay", best[1], "score", best[0], "->", r, bstate())
    return r




def boss_policy(rounds=60, heal_at=140, first=(), tag="bp"):
    """Run a battle with a simple policy, snapshot each round as tag%d."""
    plan = list(first)
    hist = []
    for i in range(rounds):
        m, h_, mp, ms = bstate()
        if plan:
            keys = plan.pop(0)
        elif h_ < heal_at:
            keys = A_USE(12)
        else:
            keys = A_ATTACK
        e.call("snapshot.save", name="%s%d" % (tag, i))
        r = act(keys)
        st = bstate()
        hist.append((i, keys if callable(keys) else keys[:1], r, st[1], st[2], [x[1] for x in st[3]]))
        print(hist[-1])
        if r != "wheel":
            break
    return hist




def try_actions(cands, score, tag="ta"):
    """Evaluate each (name, keys) from the saved state; replay the best. Returns (name, result)."""
    e.call("snapshot.save", name=tag)
    res = []
    for name, keys in cands:
        e.call("snapshot.load", name=tag)
        try:
            r = act(keys)
        except LookupError:
            continue
        st = bstate()
        res.append((score(r, st), name, keys, r, st))
    res.sort(key=lambda x: -x[0])
    best = res[0]
    e.call("snapshot.load", name=tag)
    r = act(best[2])
    return best[1], r, res


def boss_greedy(rounds=80, heal_at=150, extra=(), tag="bg", items=None):
    """Greedy one-round lookahead battle loop. extra: more attack-ish candidates
    [(name, keys)]; items: dict name->count for consumables in extra."""
    items = dict(items or {})
    hist = []
    for i in range(rounds):
        m0, h0, mp0, ms0 = bstate()
        e.call("snapshot.save", name="%s%d" % (tag, i))
        if h0 < heal_at:
            cands = [("qyj", A_USE_N("青阴君"))]
            if mp0 >= 36:
                cands.append(("qls", A_HEAL))
            def sc(r, st):
                if r != "wheel":
                    return 1e6 if st[1] > 0 else -1e6
                return st[1] + 0.3 * (m0 - st[0])
        else:
            cands = [("atk", A_ATTACK)] + list(extra)
            def sc(r, st):
                if r != "wheel":
                    return 1e6 if st[1] > 0 else -1e6
                return (m0 - st[0]) - 1.0 * (h0 - st[1])
        name, r, res = try_actions(cands, sc)
        st = bstate()
        hist.append((i, name, r, st[1], st[2], [x[1] for x in st[3]]))
        print(hist[-1], [(round(x[0]), x[1]) for x in res])
        if r != "wheel":
            break
    return hist




def _pick(menu_keys, name, max_items=24):
    """Open an item list with menu_keys, move to `name` by reading the drawn names.
    Returns True when the cursor is on it."""
    for k in menu_keys:
        e.tap(k, hold=2, wait=26)
    e.run_frames(30)
    cur = [t for _, t in poll(True)]
    nm = cur[cur.index("数量：") - 1] if "数量：" in cur else None
    for _ in range(max_items):          # to the top
        if nm == name:
            return True
        e.tap("UP", hold=2, wait=26)
        o = [t for _, t in poll(True)]
        if not o:
            break
        nm = o[0]
    for _ in range(max_items):
        if nm == name:
            return True
        e.tap("DOWN", hold=2, wait=26)
        o = [t for _, t in poll(True)]
        if not o:
            return False
        nm = o[0]
    return nm == name


def A_USE_N(name):
    def f():
        if not _pick(("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "DOWN", "ENTER"), name):
            raise LookupError(name)
        e.tap("ENTER", hold=2, wait=26)
        e.tap("ENTER", hold=2, wait=26)
    return f


def A_THROW_N(name, right=0):
    def f():
        if not _pick(("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "ENTER"), name):
            raise LookupError(name)
        e.tap("ENTER", hold=2, wait=26)
        for _ in range(right):
            e.tap("RIGHT", hold=2, wait=26)
        e.tap("ENTER", hold=2, wait=26)
    return f




EVENT_BASE = 0x2c04   # script event flags: event n = bit (n % 8) of byte EVENT_BASE + n // 8


def flags(lo=0, hi=2400):
    m = e.read(EVENT_BASE, 300)
    return [n for n in range(lo, hi) if m[n // 8] >> (n % 8) & 1]


def maze_walk(goal, lo=100, hi=128, maxsteps=30, quiet=True):
    """Follow tools/play/maze.py's solution from the current script to `goal` ("3-1"),
    re-solving after every step from the live event flags."""
    import maze as _mz
    for _ in range(maxsteps):
        key = h.where[0][2:] if h.where else None
        if key == goal:
            return True
        p = _mz.solve(key, goal, set(flags(lo, hi + 1)), range(lo, hi + 1))
        if not p:
            print("maze: no path from", key, flags(lo, hi + 1))
            return False
        k, tile, nxt, fl, _n = p[0]
        r = enter_door(tile, quiet=quiet)
        print("maze:", k, "tile", tile, "->", h.where, "flags", flags(lo, hi + 1), r)
    return False




def npc_pos(key):
    """createnpc positions (x, y) in a script."""
    return [(int(x), int(y)) for _i, _t, x, y in _re.findall(r"createnpc (\d+), (\d+), (\d+), (\d+)", gut(key))]


def visit(tile, key, talks=1, exit_tile=1, do_loot=True, quiet=False):
    """Enter a house by map tile `tile`, talk to its NPCs `talks` times each,
    loot its boxes, leave by `exit_tile`."""
    m0 = mapid()
    if not enter_door(tile, quiet=quiet):
        print("visit: could not enter", tile)
        return False
    talk_all(talks, quiet=quiet)
    if do_loot:
        loot(key, quiet=quiet)
    if exit_tile:
        enter_door(exit_tile, quiet=quiet)
    return mapid() == m0




def _obj_at(addr):
    for o in objs():
        if o["addr"] == addr:
            return o
    return None


def talk_obj(addr, quiet=False, tries=6):
    """Talk to the map object whose heap record is at `addr` (NPCs wander, and the
    record's +11/+12 fields follow x/y, so position is not an identity)."""
    for _ in range(tries):
        o = _obj_at(addr)
        if not o:
            return None
        r = goto_adj(o["x"], o["y"], quiet=quiet)
        if r is not True:
            if isinstance(r, tuple):
                return r
            continue
        o2 = _obj_at(addr)
        px, py = pos()
        if not o2 or (o2["x"] - px, o2["y"] - py) not in _DIRS:
            continue
        e.tap(_DIRS[(o2["x"] - px, o2["y"] - py)], hold=2, wait=8)
        return press_enter(quiet)
    return None


def talk_all(times=1, quiet=False, names=None):
    out = {}
    for o in objs():
        if o["kind"] in (2, 3) and (names is None or o["name"] in names):
            for _ in range(times):
                out.setdefault(o["name"], []).append(talk_obj(o["addr"], quiet=quiet))
    return out




def shop_browse(addr=None, n=30, quiet=False, tile=None):
    """Talk to the shopkeeper (object addr, default first NPC), page through the
    shop list with DOWN (draws every item name/description), then EXIT."""
    if tile is not None:       # counter: walk into the map tile event
        m = curmap()
        for c in m.events().get(tile, []):
            if goto_adj(*c, quiet=quiet) is True:
                px, py = pos()
                e.tap(_DIRS[(c[0] - px, c[1] - py)], hold=2, wait=8)
                break
    else:
        if addr is None:
            addr = [o for o in objs() if o["kind"] in (2, 3)][0]["addr"]
        o = _obj_at(addr)
        r = goto_adj(o["x"], o["y"], quiet=quiet)
        o = _obj_at(addr)
        px, py = pos()
        e.tap(_DIRS[(o["x"] - px, o["y"] - py)], hold=2, wait=8)
        e.tap("ENTER", hold=2, wait=20)
    names = []
    for _ in range(10):        # through the greeting, until the list is drawn
        e.run_frames(20)
        t = [x for _, x in poll(quiet)]
        if "价：" in t or "名：" in t:
            break
        if waitstate() == "key":
            e.tap("ENTER", hold=2, wait=20)
            t = [x for _, x in poll(quiet)]
            if "价：" in t or "名：" in t:
                break
    e.run_frames(20)
    poll(quiet)
    for _ in range(n):
        e.tap("DOWN", hold=2, wait=26)
        t = [x for _, x in poll(quiet)]
        if not t:
            break
        names.append(t[0])
    e.tap("EXIT", hold=2, wait=30)
    adv(quiet=quiet)
    return names




def engage(addr, quiet=False, tries=6):
    """Walk to the object at heap record `addr`, face it, press ENTER and advance
    dialogue only until a battle command wheel shows (for boss fights).
    Returns True at the wheel."""
    for _ in range(tries):
        o = _obj_at(addr)
        if not o:
            return False
        r = goto_adj(o["x"], o["y"], quiet=quiet)
        o2 = _obj_at(addr)
        px, py = pos()
        if r is not True or not o2 or (o2["x"] - px, o2["y"] - py) not in _DIRS:
            continue
        e.tap(_DIRS[(o2["x"] - px, o2["y"] - py)], hold=2, wait=8)
        e.tap("ENTER", hold=2, wait=20)
        if waitstate() == "idle":
            continue
        return to_wheel(quiet=quiet)
    return False


def party():
    """[(name, stats)] of party members: heap name blocks followed by a 75 6e 1c 00 stat block."""
    m = e.read(0x3000, 0x5000)
    out = []
    i = m.find(bytes.fromhex("756e1c00"))
    while i >= 0:
        r = m[i + 4:i + 0x20]
        w = lambda k: r[k] | r[k + 1] << 8
        # name block precedes: 75 6e 10 00 <name>
        j = m.rfind(bytes.fromhex("756e1000"), max(0, i - 0x20), i)
        name = m[j + 4:j + 0x10].split(b"\0")[0].decode("gb2312", "replace") if j >= 0 else "?"
        if j < 0 and 0 < r[0] < 100 and 0 < w(6) < 10000 and w(8) <= w(6) and w(12) <= w(10):
            # 3rd member re-created by createactor: the name block sits elsewhere
            j = m.rfind(bytes.fromhex("756e1000"), max(0, i - 0x200), i)
            name = m[j + 4:j + 0x10].split(b"\0")[0].decode("gb2312", "replace") if j >= 0 else "?"
            if name not in ("袁萍芷",):
                j = -1
        if j >= 0 and 0 < r[0] < 100 and 0 < w(6) < 10000 and w(8) <= w(6) and name.isprintable():
            out.append((name, {"hpmax": w(6), "hp": w(8), "mpmax": w(10), "mp": w(12), "atk": w(14), "def": w(16), "addr": hex(0x3000 + i)}))
        i = m.find(bytes.fromhex("756e1c00"), i + 4)
    return out





def A_MAG(idx, right=0):
    """Magic list entry idx (0-based), target = first enemy + `right` RIGHTs."""
    return ("LEFT", "ENTER", None) + ("DOWN",) * idx + ("ENTER", None) + ("RIGHT",) * right + ("ENTER",)


def A_MAG_SELF(idx):
    """Magic idx on a party member (default target = the caster)."""
    return ("LEFT", "ENTER", None) + ("DOWN",) * idx + ("ENTER", None, "ENTER")



def alive_index(name):
    """Target index (RIGHT presses) of monster `name` among living monsters."""
    ms = [m for m in mons_all() if m[1] > 0]
    for i, m in enumerate(ms):
        if m[0] == name:
            return i
    return None


def mons_all(n=3):
    """Like mons() but keeps scanning past zeroed (dead) records."""
    out = []
    for i in range(n):
        r = e.read(MON_BASE + i * MON_STRIDE, MON_STRIDE)
        if r[0] != 3:
            continue
        name = r[6:0x12].split(b"\0")[0].decode("gb2312", "replace")
        out.append((name, r[0x1a] | r[0x1b] << 8, r[0x18] | r[0x19] << 8))
    return out


def pstate():
    return [(n, s["hp"], s["mp"]) for n, s in party()]


ACTOR = 0x1785   # battle: index of the party member whose command wheel is up


def act_as(keys, want, tries=4):
    """act() from a wheel, then make sure the wheel that follows belongs to party
    member `want` (0x1785); returns 'wheel'/'msg'/'idle'/None ('stuck' if the
    input did not register)."""
    if want == 0:
        # the round runs after the last command: wait for the wheel to go away first
        e.run_frames(10)
        if callable(keys):
            keys()
            keys = ()
        for k in keys:
            if k is None:
                e.run_frames(30)
            else:
                e.tap(k, hold=2, wait=26)
        for _ in range(40):
            if not wheel_shown():
                break
            e.run_frames(3)
        r = wait_wheel()
        poll(True)
    else:
        # the next member's wheel shows at once; just send the keys
        e.run_frames(10)
        if callable(keys):
            keys()
            keys = ()
        for k in keys:
            if k is None:
                e.run_frames(30)
            else:
                e.tap(k, hold=2, wait=26)
        # the next member's wheel shows at once; if it does not, that member
        # was skipped (asleep etc.) and the round is already running
        for _ in range(10):
            e.run_frames(5)
            if wheel_shown():
                break
        poll(True)
        if wheel_shown():
            r = "wheel"
        else:
            r = wait_wheel()
            if r == "wheel":
                r = "newround"
    return r


def duo_round(hero, mei, tag="dr"):
    """One battle round for 柳清风 + 慕容小梅: key tuples/callables for each.
    Returns (result, monsters, party)."""
    if mei is None:                      # hero fights alone
        r = act_as(hero, 0)
    else:
        r = act_as(hero, 1)
        if r == "wheel":
            r = act_as(mei, 0)
        elif r == "newround":
            r = "wheel"
    for _ in range(12):     # in-battle dialogue (enterfight events): ENTER through it
        if r not in ("msg", None) or not any(m[1] > 0 for m in mons_all()):
            break
        if r is None and not any(m[1] > 0 for m in mons_all()):
            break
        e.tap("ENTER", hold=2, wait=20)
        r = wait_wheel(max_frames=1500)
        poll(True)
    return r, mons_all(), pstate()



def battle_list(kind="throw", n=30):
    """At a battle wheel: names in the 道具 投掷 (kind='throw') or 使用 ('use') list.
    Leaves the menu with EXITs (back at the same wheel)."""
    keys = ("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "ENTER") if kind == "throw" else ("DOWN", "ENTER", "DOWN", "ENTER", "DOWN", "DOWN", "ENTER")
    for k in keys:
        e.tap(k, hold=2, wait=26)
    e.run_frames(30)
    cur = [t for _, t in poll(True)]
    names = [cur[cur.index("数量：") - 1]] if "数量：" in cur else []
    for _ in range(n):
        e.tap("DOWN", hold=2, wait=26)
        o = [t for _, t in poll(True)]
        if not o or o[0] in names:
            break
        names.append(o[0])
    for _ in range(3):
        e.tap("EXIT", hold=2, wait=26)
    poll(True)
    return names



def duo_greedy(target, rounds=40, hero_cands=None, mei_cands=None, heal_hero=120, heal_mei=70,
               w_other=0.3, tag="dg", verbose=True, safety=None, w_safe=1.0):
    """Greedy one-round lookahead for 柳清风 + 慕容小梅 boss fights.
    hero_cands/mei_cands: functions (ix) -> [(name, keys)] where ix = target's
    RIGHT count among living monsters. Default: hero magic 天师符法 / attack,
    小梅 attack or 观音咒 when someone is low."""
    if hero_cands is None:
        hero_cands = lambda ix: [("tsf", A_MAG(2, ix)), ("atk", A_ATTACK)]
    if mei_cands is None:
        def mei_cands(ix):
            ps = dict((n, hp) for n, hp, mp in pstate())
            c = [("atk", A_ATTACK)]
            if ps.get("柳清风", 999) < heal_hero or ps.get("慕容小梅", 999) < heal_mei:
                c += [("heal0", A_MAG_SELF(0)),
                      ("healL", ("LEFT", "ENTER", None, "ENTER", None, "LEFT", "ENTER")),
                      ("healR", ("LEFT", "ENTER", None, "ENTER", None, "RIGHT", "ENTER"))]
            return c
    safety = safety or {}
    hist = []
    for i in range(rounds):
        ms0 = {m[0]: m[1] for m in mons_all()}
        ps0 = dict((n, hp) for n, hp, mp in pstate())
        ix = alive_index(target)
        ix = 0 if ix is None else ix
        e.call("snapshot.save", name="%s%d" % (tag, i))
        res = []
        for hn, hk in hero_cands(ix):
            for mn, mk in mei_cands(ix):
                e.call("snapshot.load", name="%s%d" % (tag, i))
                try:
                    r, ms, ps = duo_round(hk, mk)
                except LookupError:
                    continue
                msd = {m[0]: m[1] for m in ms}
                psd = dict((n, hp) for n, hp, mp in ps)
                if r is None:
                    sc = -2e6
                elif r != "wheel":
                    sc = 1e6 if all(v > 0 for v in psd.values()) and not any(m[1] > 0 for m in ms) else -1e6
                else:
                    dt = ms0.get(target, 0) - msd.get(target, 0)
                    do = sum(ms0.values()) - sum(msd.values()) - dt
                    loss = sum(ps0[n] - psd.get(n, 0) for n in ps0)
                    sc = dt + w_other * do - loss
                    for n, lim in safety.items():
                        sc -= max(0, lim - psd.get(n, 0)) * w_safe
                    if any(v == 0 for v in psd.values()):
                        sc -= 5000
                res.append((sc, hn, mn, hk, mk, r))
        res.sort(key=lambda x: -x[0])
        b = res[0]
        e.call("snapshot.load", name="%s%d" % (tag, i))
        r, ms, ps = duo_round(b[3], b[4])
        hist.append((i, b[1], b[2], r, ms, ps))
        if verbose:
            print(i, b[1], b[2], r, ms, ps, [(round(x[0]), x[1], x[2]) for x in res[:4]])
        if r != "wheel":
            break
    return hist



def duo_beam(target, rounds=30, width=3, hero_cands=None, mei_cands=None, value=None, start=None, verbose=True):
    """Beam search over battle rounds (RNG depends only on the action sequence).
    hero_cands/mei_cands: f(ix, party_state) -> [(name, keys)]. value(ms, ps) -> float.
    Leaves the emulator in the best final state (battle won if found). Returns the
    winning action list or None."""
    if value is None:
        def value(ms, ps):
            d = dict((n, hp) for n, hp, mp in ps)
            boss = sum(m[1] for m in ms)
            return -boss + 0.6 * d.get("柳清风", 0) + 0.3 * d.get("慕容小梅", 0) + (80 if d.get("慕容小梅", 0) > 0 else 0)
    root = start or "beam_root"
    e.call("snapshot.save", name=root)
    beam = [(0.0, root, [], [])]
    n = 0
    for rnd in range(rounds):
        kids = []
        for _sc, snap, hist, keys in beam:
            e.call("snapshot.load", name=snap)
            ps0 = pstate()
            ix = alive_index(target)
            ix = 0 if ix is None else ix
            for hn, hk in hero_cands(ix, ps0):
                for mn, mk in mei_cands(ix, ps0):
                    e.call("snapshot.load", name=snap)
                    try:
                        r, ms, ps = duo_round(hk, mk)
                    except LookupError:
                        continue
                    d = dict((x, hp) for x, hp, mp in ps)
                    if r in ("idle", "msg") or (r != "wheel" and not any(m[1] > 0 for m in ms)):
                        if any(v > 0 for v in d.values()):   # someone alive (a game over also zeroes the monsters)
                            if verbose:
                                print("WIN at round", rnd, hist + [(hn, mn)])
                            return _beam_replay(root, keys + [(hk, mk)], hist + [(hn, mn)])
                    if r != "wheel" or d.get("柳清风", 0) == 0:
                        continue
                    n += 1
                    name = "bm%d" % n
                    e.call("snapshot.save", name=name)
                    kids.append((value(ms, ps), name, hist + [(hn, mn)], ms, ps, keys + [(hk, mk)]))
        if not kids:
            print("beam: no survivors at round", rnd)
            return None
        kids.sort(key=lambda k: -k[0])
        keep = kids[:width]
        for k in kids[width:]:
            e.call("snapshot.delete", name=k[1])
        for b in beam:
            if b[1] != root:
                e.call("snapshot.delete", name=b[1])
        beam = [(k[0], k[1], k[2], k[5]) for k in keep]
        if verbose:
            k = keep[0]
            print(rnd, round(k[0]), k[2][-1], k[3], k[4], "| kids", len(kids))
    # no win: leave the emulator on the best line, replayed from the root so the
    # recorded route stays one straight path
    _beam_replay(root, beam[0][3], beam[0][2])
    return None


def _beam_replay(root, keys, hist):
    """Reload the beam root (an ancestor: route truncation is exact) and replay
    the chosen rounds. Loading a sibling snapshot directly would leave the wrong
    events in the route (snapshot.load truncates by event count only)."""
    e.call("snapshot.load", name=root)
    for (hk, mk), hm in zip(keys, hist):
        r = duo_round(hk, mk)
        print("  replay", hm, r[0], r[1], r[2])
    return hist



def equip_list_goto(name, max_items=40):
    """In a map-menu item list (物品 使用/装备, shops): move the cursor to `name`
    (reads drawn names). A list end draws nothing; one dropped key is tolerated."""
    e.run_frames(30)
    poll(True)
    miss = 0
    for _ in range(max_items):          # to the top
        e.tap("UP", hold=2, wait=30)
        o = [t for _, t in poll(True)]
        if not o:
            miss += 1
            if miss >= 2:
                break
            continue
        miss = 0
        if o[0] == name:
            return True
    miss = 0
    for _ in range(max_items):
        e.tap("DOWN", hold=2, wait=30)
        o = [t for _, t in poll(True)]
        if not o:
            miss += 1
            if miss >= 2:
                return False
            continue
        miss = 0
        if o[0] == name:
            return True
    return False


def equip(name, who=0):
    """From the 物品/装备 list: equip `name` on party member `who` (0 hero)."""
    if not equip_list_goto(name):
        return False
    e.run_frames(20)
    e.tap("ENTER", hold=2, wait=40)
    t = [x for _, x in poll(True)]
    if "柳清风" in t or "慕容小梅" in t:      # who-wears-it popup (several can)
        for _ in range(who):
            e.tap("DOWN", hold=2, wait=30)
        e.tap("ENTER", hold=2, wait=40)       # -> stat comparison screen
    e.tap("ENTER", hold=2, wait=40)           # confirm
    poll(True)
    return True



def menu_use(name, times=1, who=0):
    """At the map menu's 物品/使用 list: use `name` `times` times on party member `who`."""
    if not equip_list_goto(name):
        return False
    e.run_frames(20)
    e.tap("ENTER", hold=2, wait=40)
    for _ in range(who):
        e.tap("DOWN", hold=2, wait=30)
    for _ in range(times):
        e.tap("ENTER", hold=2, wait=40)
    e.tap("EXIT", hold=2, wait=40)
    poll(True)
    return True



MONEY = 0x1a8f   # u16 (3807 seen); party money


def money():
    b = e.read(MONEY, 3)
    return b[0] | b[1] << 8 | b[2] << 16


def shop_buy(tile, want, quiet=True):
    """At a shop counter (map tile event `tile` inside the shop): buy {name: count}.
    The list cursor is moved by drawn names; 买入个数 counts up with UP."""
    m = curmap()
    for c in m.events().get(tile, []):
        if goto_adj(*c, quiet=quiet) is True:
            px, py = pos()
            e.tap(_DIRS[(c[0] - px, c[1] - py)], hold=2, wait=8)
            break
    for _ in range(10):
        e.run_frames(20)
        t = [x for _, x in poll(quiet)]
        if "价：" in t or "名：" in t:
            break
        if waitstate() == "key":
            e.tap("ENTER", hold=2, wait=20)
            t = [x for _, x in poll(quiet)]
            if "价：" in t or "名：" in t:
                break
    e.run_frames(30)
    poll(True)
    got = {}
    for name, cnt in want.items():
        if not equip_list_goto(name):
            print("shop: no", name)
            continue
        m0 = money()
        e.run_frames(20)
        e.tap("ENTER", hold=2, wait=40)
        for _ in range(cnt):
            e.tap("UP", hold=2, wait=20)
        e.tap("ENTER", hold=2, wait=40)
        poll(True)
        got[name] = m0 - money()
    e.tap("EXIT", hold=2, wait=30)
    adv(quiet=quiet)
    return got



def map_heal(target=0, times=1, caster=1, spell=0):
    """Map menu 魔法: `caster` casts magic #spell (观音咒 for 小梅) on `target`, `times` times."""
    for k in ("EXIT", "DOWN", "ENTER"):
        e.tap(k, hold=2, wait=30)
    for _ in range(caster):
        e.tap("DOWN", hold=2, wait=30)
    e.tap("ENTER", hold=2, wait=40)
    e.run_frames(20)
    for _ in range(spell):
        e.tap("DOWN", hold=2, wait=30)
    e.tap("ENTER", hold=2, wait=40)
    e.run_frames(20)
    for _ in range(target):            # RIGHT cycles the target (PGUP/PGDN page stats)
        e.tap("RIGHT", hold=2, wait=30)
    for _ in range(times):
        e.tap("ENTER", hold=2, wait=60)
    for _ in range(6):
        e.tap("EXIT", hold=2, wait=30)
        if waitstate() == "idle":
            break
    poll(True)
    return pstate()
# --- session 5 -------------------------------------------------------------------

def mwalk(goal, mask, maxsteps=30):
    """maze_walk with an explicit flag mask (e.g. set(range(101,114)) | {216, 218}):
    story flags in the mask let the solver follow `if 216` branches."""
    import maze as _mz
    mask = set(mask)
    for _ in range(maxsteps):
        key = h.where[0][2:]
        if key == goal:
            return True
        fl = set(f for f in flags(min(mask), max(mask) + 1) if f in mask)
        p = _mz.solve(key, goal, fl, mask)
        if not p:
            print("no path", key, fl)
            return False
        k, tile, nxt, f2, notes = p[0]
        enter_door(tile, quiet=False)
        print("maze:", k, tile, "->", h.where, sorted(set(flags(min(mask), max(mask) + 1)) & mask), notes)
    return False


def send(keys):
    """Send a key tuple (None = wait 30 frames) or call a callable."""
    if callable(keys):
        keys()
        return
    for k in keys:
        if k is None:
            e.run_frames(30)
        else:
            e.tap(k, hold=2, wait=26)


def pair(mk, yk):
    """Trio battles: duo_beam's mei_cands keys for 小梅 then 袁萍芷 (3rd wheel)."""
    def f():
        send(mk)
        e.run_frames(20)
        send(yk)
    return f


def MEI_MAG(idx, side):
    """小梅 party-target magic idx; side 0 self, -1 hero (LEFT), +1 3rd member (RIGHT)."""
    k = ("LEFT", "ENTER", None) + ("DOWN",) * idx + ("ENTER", None)
    k += ("LEFT",) if side < 0 else (("RIGHT",) if side > 0 else ())
    return k + ("ENTER",)


def use_item(name, who=0):
    """Map menu 物品/使用 `name` on party member `who` (who>0 is unreliable)."""
    import menus
    menus.main_menu_select(e, 2)
    tap("ENTER", hold=2, wait=30, quiet=True)
    tap("ENTER", hold=2, wait=40, quiet=True)
    r = menu_use(name, 1, who)
    for _ in range(5):
        if waitstate() == "idle":
            break
        e.tap("EXIT", hold=2, wait=30)
    poll(True)
    return r


def topup():
    """Between fights: 小梅 heals anyone under 60% (观音咒)."""
    for _ in range(4):
        ps = party()
        low = [i for i, (n, s) in enumerate(ps) if s["hp"] < 0.6 * s["hpmax"]]
        mei = [s for n, s in ps if n == "慕容小梅"]
        if not low or not mei or mei[0]["mp"] < 10:
            return
        map_heal(low[0], 1)


def safe_adj(x, y, tries=40):
    """goto_adj that survives many random fights, healing in between.
    Returns 'dead' if the party vanished (game over)."""
    for _ in range(tries):
        topup()
        r = goto_adj(x, y, tries=1, quiet=True)
        if r is True or isinstance(r, tuple):
            return r
        if not party():
            return "dead"
    return False


# --- session 6 -------------------------------------------------------------------

def counter(tile, quiet=False):
    """Walk up to an unwalkable map tile event (shop/inn counter), face it, ENTER."""
    m = curmap()
    for c in m.events().get(tile, []):
        if goto_adj(*c, quiet=quiet) is True:
            px, py = pos()
            d = (c[0] - px, c[1] - py)
            if d in _DIRS:
                e.tap(_DIRS[d], hold=2, wait=8)
                return press_enter(quiet)
    return None


def choose(i, quiet=False):
    """At a script choice box: move to option i (0/1) and confirm, then advance."""
    e.run_frames(30)
    for _ in range(i):
        e.tap("DOWN", hold=2, wait=30)
    e.tap("ENTER", hold=2, wait=30)
    return poll(quiet) + adv(quiet=quiet)


def save_game(slot):
    """Main menu 系统 -> 存储进度 -> slot (1-based). Returns the drawn texts."""
    import menus
    menus.main_menu_select(e, 3)
    out = []
    for k, w in (("ENTER", 30), ("DOWN", 30), ("ENTER", 60)):
        e.tap(k, hold=2, wait=w)
    out += [t for _, t in poll(True)]
    for _ in range(slot - 1):
        e.tap("DOWN", hold=2, wait=30)
    e.tap("ENTER", hold=2, wait=200)
    out += [t for _, t in poll(True)]
    for _ in range(6):
        if waitstate() == "idle":
            break
        e.tap("EXIT", hold=2, wait=30)
    out += [t for _, t in poll(True)]
    print("save:", out)
    return out


def equip_item(name, who=0):
    """Map menu 物品/装备 `name` on party member `who`."""
    import menus
    menus.main_menu_select(e, 2)
    tap("ENTER", hold=2, wait=30, quiet=True)
    tap("DOWN", hold=2, wait=30, quiet=True)
    tap("ENTER", hold=2, wait=40, quiet=True)
    r = equip(name, who)
    for _ in range(6):
        if waitstate() == "idle":
            break
        e.tap("EXIT", hold=2, wait=30)
    poll(True)
    return r


_GRSN = None


def grs_names():
    global _GRSN
    if _GRSN is None:
        _GRSN = {}
        for k, r in ROWS.items():
            if r["kind"] == "grs.name":
                t, i = map(int, k.split("/")[1].split("-")[1:])
                _GRSN[(t, i)] = r["zh"].strip()
    return _GRSN


def inv(addr=0x4a00, n=0x200):
    """Inventory: (type, index, count) triples in a heap block (0x4a2d in session 6).
    Finds the first triple after a zero run; returns {name: count}."""
    m = e.read(addr, n)
    i = 0
    while i < n and m[i] == 0:
        i += 1
    names = grs_names()
    out = {}
    while i + 3 <= n and m[i] and (m[i], m[i + 1]) in names:
        out[names[(m[i], m[i + 1])]] = m[i + 2]
        i += 3
    return out


def _to_idle():
    for _ in range(8):
        if waitstate() == "idle":
            return True
        e.tap("EXIT", hold=2, wait=30)
    return waitstate() == "idle"


def open_items(kind="use"):
    """Open the map menu 物品 list: kind 'use' (使用) or 'equip' (装备).
    The submenu remembers its last choice and sometimes drops a key, so the
    list is checked by the GRS type of the first drawn name (equipment 1-7)."""
    import menus
    rev = {v: k for k, v in grs_names().items()}
    for attempt in range(4):
        _to_idle()
        menus.main_menu_select(e, 2)
        tap("ENTER", hold=2, wait=40, quiet=True)
        e.run_frames(20)
        want_top = kind == "use"
        for _ in range(3):      # 使用 (top) / 装备 (bottom): read the inverted row
            px = menus.pixels(e)
            top = menus.dark(px, 40, 75, 42, 56) > menus.dark(px, 40, 75, 58, 72)
            if top == want_top:
                break
            e.tap("DOWN", hold=2, wait=30)
        e.tap("ENTER", hold=2, wait=40)
        e.run_frames(30)
        poll(True)
        e.tap("DOWN", hold=2, wait=30)
        o = [t for _, t in poll(True)]
        if not o:
            e.tap("DOWN", hold=2, wait=30)
            o = [t for _, t in poll(True)]
        if o and o[0] in rev:
            is_eq = rev[o[0]][0] <= 7
            if is_eq == (kind == "equip"):
                return True
    return False


def use_on(name, who=0, times=1):
    """Map menu 物品/使用 `name` on party member `who` (RIGHT moves the target)."""
    ok = open_items("use") and equip_list_goto(name)
    if ok:
        for _ in range(times):
            e.run_frames(20)
            e.tap("ENTER", hold=2, wait=40)
            for _ in range(who):
                e.tap("RIGHT", hold=2, wait=30)
            e.tap("ENTER", hold=2, wait=40)
            e.run_frames(20)
            poll(True)
    _to_idle()
    poll(True)
    return ok


def equip_on(name, who=0):
    ok = open_items("equip") and equip(name, who)
    _to_idle()
    poll(True)
    return ok


__all__ = [k for k in list(globals()) if not k.startswith("_") and k not in _PRIVATE]
