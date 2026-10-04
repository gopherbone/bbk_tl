"""Two-slot save/load check on a fresh game (same inputs on bbkemu and gam4980)."""
import sys
sys.path.insert(0, "."); sys.path.insert(0, "bbkemu/cli/py"); sys.path.insert(0, "tools"); sys.path.insert(0, "tools/play")
import menus
from bbkrpg import games

GAM = games.from_argv().gam


class BE:          # bbkemu adapter
    def __init__(self):
        from bbkemu import BBKEmu
        self.e = BBKEmu(); self.e.load_gam(GAM, rom_dir=games.ROMS)
    def run(self, n): self.e.run_frames(n)
    def tap(self, k, hold=2, wait=30): self.e.tap(k, hold=hold, wait=wait)
    def ram(self, a, n): return self.e.read(a, n)
    def px(self): return menus.pixels(self.e)


class G:           # gam4980 adapter
    def __init__(self):
        from gam4980_headless import Gam4980
        self.g = Gam4980(); self.g.load(GAM)
    def run(self, n): self.g.run(n)
    def tap(self, k, hold=2, wait=30): self.g.tap(k, hold=hold, wait=wait)
    def ram(self, a, n): return self.g.ram(a, n)
    def px(self): return self.g.pixels()


def sel(m):
    px = m.px(); sc = [menus.dark(px, 21, 50, a, b) for a, b in menus.MAIN_ROWS]
    b = max(range(4), key=lambda i: sc[i]); return b if sc[b] > 0.45 else None


def to_sys(m):
    m.tap("EXIT")
    for _ in range(8):
        if sel(m) == 3: break
        m.tap("DOWN", wait=20)
    m.tap("ENTER")


def run(m):
    m.run(1000); m.tap("ENTER", hold=4, wait=60); m.tap("EXIT", hold=4, wait=240)
    for _ in range(14): m.tap("ENTER", hold=4, wait=60)
    pos = lambda: m.ram(0x1979, 8).hex()
    p1 = pos()
    to_sys(m); m.tap("DOWN"); m.tap("ENTER", wait=40); m.tap("ENTER", wait=60); m.run(240)    # save slot 1
    for _ in range(3): m.tap("LEFT", wait=10)
    m.run(60); p2 = pos()
    to_sys(m); m.tap("DOWN"); m.tap("ENTER", wait=40); m.tap("DOWN", wait=30); m.tap("ENTER", wait=60); m.run(240)  # slot 2
    for _ in range(3): m.tap("RIGHT", wait=10)
    m.run(60)
    to_sys(m); m.tap("ENTER", wait=40); m.tap("ENTER", wait=90); m.run(300); l1 = pos()          # load slot 1
    to_sys(m); m.tap("ENTER", wait=40); m.tap("DOWN", wait=30); m.tap("ENTER", wait=90); m.run(300); l2 = pos()  # slot 2
    return p1 == l1, p2 == l2, (p1, p2, l1, l2)


if __name__ == "__main__":
    print("bbkemu ", run(BE()))
    print("gam4980", run(G()))
