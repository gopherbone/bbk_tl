"""bbkemu smoke test: boot 伏魔记, reach the first dialogue, and check that
text.log ties each line to its string-table row. Needs the gam4980 game set.

Run from the repo root: python3 bbkemu/cli/tests/smoke.py
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu", "cli", "py"))
from bbkemu import BBKEmu, Hooks  # noqa: E402

GAM = os.path.join(ROOT, "gam4980", "retroarch", "downloads", "bbk", "伏魔记.gam")
ROMS = os.path.join(ROOT, "gam4980", "retroarch", "system", "gam4980")


def main():
    if not os.path.exists(GAM):
        print("skip: game set not present")
        return
    with BBKEmu() as e:
        e.load_gam(GAM, rom_dir=ROMS)
        h = Hooks(e)
        e.run_frames(1000)
        title = e.screen()["hash"]
        e.save("title")
        drawn = []
        for key, wait in [("ENTER", 60), ("EXIT", 240)] + [("ENTER", 100)] * 3:
            e.tap(key)
            e.run_frames(wait)
            drawn += h.drain()
        first = next(d for d in drawn if d["text"].startswith("小蝴蝶"))
        assert first["script"] == ("1-1-1", 0x39B), first
        assert first["y"] == 58, first
        # determinism: replaying from the snapshot gives the same screen
        e.load("title")
        assert e.screen()["hash"] == title
        e.run_frames(10)
        a = e.screen()["hash"]
        e.load("title")
        e.run_frames(10)
        assert e.screen()["hash"] == a
        # a stopping breakpoint on the draw hook halts once the game starts
        e.load("title")
        e.call("break.clear")
        e.break_add(None, phys=0xE94843)
        e.call("input.tap", key="ENTER", run=False)
        r = e.run_frames(300)
        assert r["reason"] == "breakpoint" and r["detail"]["phys"] == "e94843", r
        r = e.step(1)
        assert not r["stopped"], r   # resuming does not re-fire immediately
        print("ok:", len(drawn), "text draws; first dialogue at", first["script"])


if __name__ == "__main__":
    main()
