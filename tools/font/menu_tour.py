"""Boot a build, get to free movement in 三清宫, and screenshot the menus."""
import sys
sys.path.insert(0, "bbkemu/cli/py")
from bbkemu import BBKEmu

def idle(e):
    r = e.regs()
    return r["pc_phys"] == "e9e317" and r["sp"] == "e8"

def tour(gam, prefix):
    shots = []
    with BBKEmu() as e:
        e.load_gam(gam, rom_dir="gam4980/retroarch/system/gam4980")
        e.run_frames(1000)
        for k, w in [("ENTER", 60), ("EXIT", 240)]:
            e.tap(k); e.run_frames(w)
        for _ in range(60):
            if idle(e):
                break
            e.tap("ENTER"); e.run_frames(60)
        assert idle(e), "never reached the map"
        def shot(name, *keys, wait=30):
            for k in keys:
                e.tap(k); e.run_frames(wait)
            p = f"work/shots/{prefix}_{name}.png"; e.screen(p, scale=3); shots.append(p)
        shot("menu", "EXIT")
        shot("stats", "ENTER")
        shot("stats2", "ENTER")
        e.tap("EXIT"); e.run_frames(30); e.tap("EXIT"); e.run_frames(30)
        shot("menu_magic", "RIGHT")
        shot("magic", "ENTER")
        e.tap("EXIT"); e.run_frames(30)
        shot("menu_items", "RIGHT")
        shot("items", "ENTER")
        e.tap("EXIT"); e.run_frames(30)
        shot("menu_sys", "RIGHT")
        shot("sys", "ENTER")
    return shots

if __name__ == "__main__":
    print(tour(sys.argv[1], sys.argv[2]))
