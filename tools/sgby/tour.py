"""Scripted QA tour of 三国霸业: screenshots and drawn text per step.

    python3 tools/sgby/tour.py [GAM] [OUTDIR] [--only SECTION,...]

Default GAM work/sgby/sgby_en.gam, OUTDIR work/sgby/qa/tour.
Sections reset from snapshots, so one failing path does not derail the rest.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa import Session  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
GAM = args[0] if args else "work/sgby/sgby_en.gam"
OUT = args[1] if len(args) > 1 else "work/sgby/qa/tour"
ONLY = None
for a in sys.argv[1:]:
    if a.startswith("--only="):
        ONLY = set(a.split("=", 1)[1].split(","))

s = Session(GAM, OUT)
K = s.keys


def section(name):
    def deco(f):
        if ONLY is None or name in ONLY:
            f()
        return f
    return deco


s.run(600)
s.step("title")
s.save("title")


@section("credits")
def _():
    s.load("title")
    K("DOWN", n=2, wait=20); s.step("title_sel_credits")
    K("ENTER", wait=200); s.step("credits")
    K("ENTER", wait=60); s.step("credits_out")


@section("load")
def _():
    s.load("title")
    K("DOWN", wait=20); K("ENTER", wait=120); s.step("load_screen")
    K("EXIT", wait=60)


@section("periods")
def _():
    s.load("title")
    K("ENTER", wait=120); s.step("periods")
    for p, moves in enumerate([[], ["DOWN"], ["DOWN"] * 2, ["DOWN"] * 3]):
        s.load("title")
        K("ENTER", wait=120)
        for m in moves:
            K(m, wait=20)
        K("ENTER", wait=150); s.step(f"rulers_p{p}")
        for i in range(4):
            K("DOWN", n=4, wait=10); s.step(f"rulers_p{p}_{i}")


# --- the campaign: period 1, first ruler --------------------------------------
s.load("title")
K("ENTER", wait=120); K("ENTER", wait=120); K("ENTER", wait=120)
s.step("map_start")
K("ENTER", wait=120); s.step("main_menu")
s.save("menu")


def menu(path):
    """Open main menu item path[0], submenu item path[1]."""
    s.load("menu")
    K("DOWN", n=path[0], wait=10); K("ENTER", wait=90)
    if len(path) > 1:
        K("DOWN", n=path[1], wait=10); K("ENTER", wait=90)


DOMESTIC = ["farm", "trade", "search", "govern", "patrol", "recruit", "execute", "exile",
            "reward", "confiscate", "market", "banquet", "transport", "move"]


@section("domestic")
def _():
    menu([0]); s.step("domestic_menu")
    for i, name in enumerate(DOMESTIC):
        menu([0, i]); s.step(f"dom_{name}_0")
        K("ENTER", wait=150); s.step(f"dom_{name}_1")
        K("ENTER", wait=150); s.step(f"dom_{name}_2")
        K("ENTER", wait=150); s.step(f"dom_{name}_3")


@section("columns")
def _():
    # officer list: scroll right through every attribute column
    menu([0, 0])
    for i in range(12):
        s.step(f"cols_{i}")
        K("RIGHT", wait=30)


@section("diplomacy")
def _():
    menu([1]); s.step("diplomacy_menu")
    for i, name in enumerate(["sow", "hire", "incite", "counter", "surrender"]):
        menu([1, i]); s.step(f"dip_{name}_0")
        K("ENTER", wait=150); s.step(f"dip_{name}_1")
        K("ENTER", wait=150); s.step(f"dip_{name}_2")
        K("ENTER", wait=150); s.step(f"dip_{name}_3")


@section("military")
def _():
    menu([2]); s.step("military_menu")
    for i, name in enumerate(["scout", "conscript", "assign", "plunder", "attack"]):
        menu([2, i]); s.step(f"mil_{name}_0")
        K("ENTER", wait=150); s.step(f"mil_{name}_1")
        K("ENTER", wait=150); s.step(f"mil_{name}_2")
        K("HELP", wait=40); s.step(f"mil_{name}_3")
        K("ENTER", wait=150); s.step(f"mil_{name}_4")


@section("status")
def _():
    menu([3]); s.step("status_0")
    for i in range(3):
        K("DOWN", wait=40); s.step(f"status_{i + 1}")


@section("function")
def _():
    s.load("menu")
    K("EXIT", wait=60); K("EXIT", wait=90); s.step("func_menu")
    K("DOWN", wait=20); K("ENTER", wait=150); s.step("save_screen")
    K("EXIT", wait=60)
    s.load("menu")
    K("EXIT", wait=60); K("EXIT", wait=90); K("ENTER", wait=20)
    for i in range(12):
        s.run(150); s.step(f"month_end_{i}")


@section("battle")
def _():
    # 天水 (2 right, 2 down from the opening cursor) attacks 汉中 (one tile down).
    # Cursor keys need ~20 frames each (the map redraws), or presses are lost.
    s.load("menu")
    K("EXIT", wait=60); K("RIGHT", n=2, wait=25); K("DOWN", n=2, wait=25); K("ENTER", wait=90)
    K("DOWN", n=2, wait=20); K("ENTER", wait=90); K("DOWN", n=4, wait=20); K("ENTER", wait=120)
    s.step("bat_pick_0")
    K("ENTER", wait=90); K("ENTER", wait=90); K("EXIT", wait=90); s.step("bat_food")
    K("HELP", wait=30); K("ENTER", wait=150); s.step("bat_target_msg")
    K("ENTER", wait=90); K("DOWN", wait=25); K("ENTER", wait=150); s.step("bat_sent")
    K("EXIT", wait=90); s.step("bat_func")
    K("ENTER", wait=10)
    for i in range(8):
        s.run(180); s.step(f"bat_start_{i}")
    s.save("battle")
    # first unit: select it, move one cell left, then each command from the menu
    for i, name in enumerate(["attack", "tactic", "view", "wait"]):
        s.load("battle")
        K("ENTER", wait=60); K("LEFT", wait=30); K("ENTER", wait=250)
        if i == 0:
            s.step("bat_cmd")
        K("DOWN", n=i, wait=30); K("ENTER", wait=150); s.step(f"bat_{name}_0")
        K("ENTER", wait=120); s.step(f"bat_{name}_1")
        K("EXIT", wait=60); s.step(f"bat_{name}_2")
    s.load("battle")
    K("EXIT", wait=60); s.step("bat_sys")
    for i in range(1, 5):
        s.load("battle")
        K("EXIT", wait=60); K("DOWN", n=i, wait=30); K("ENTER", wait=120); s.step(f"bat_sys_{i}")


s.close()
print("done:", OUT)
