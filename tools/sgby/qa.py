"""QA harness for 三国霸业: drive the game, log every string drawn, screenshot.

    from qa import Session
    s = Session("work/sgby/sgby_en.gam", "work/sgby/qa/tour")
    s.keys("ENTER", wait=120); s.step("title")
    ...
    s.close()     # writes texts.jsonl (all draws) next to the screenshots

On an English build (with <gam>.json from build_en.py) draws are logged at our
renderer's entry and tokens are expanded; on the original .gam at the native
GamStrShow (e1:$5B68).
"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "bbkemu", "cli", "py"))
from bbkemu import BBKEmu  # noqa: E402

ROMS = os.path.join(ROOT, "gam4980/retroarch/system/gam4980")
GAM_PHYS = 0x20D000
NATIVE_STRSHOW = GAM_PHYS + 0x4000 + 0x5B68 - 0x5000
NEW_SEG = 0x40000


def decode(raw: bytes, bank) -> str:
    out, i = [], 0
    while i < len(raw):
        b = raw[i]
        if 0x80 <= b <= 0x95 and bank is not None and i + 1 < len(raw):
            res, item = b - 0x80, raw[i + 1] - 1
            try:
                out.append(bank[res][item])
            except (IndexError, TypeError):
                out.append("<?>")
            i += 2
        elif b == 0xA0:
            i += 2
        elif b >= 0xA1 and i + 1 < len(raw):
            out.append(raw[i:i + 2].decode("gb2312", errors="replace"))
            i += 2
        elif b == 0x0A:
            out.append("\n")
            i += 1
        elif b < 0x20 or b == 0x7F:
            i += 1
        else:
            out.append(chr(b))
            i += 1
    return "".join(out)


class Session:
    def __init__(self, gam, outdir, emu=None):
        self.gam, self.outdir = gam, outdir
        os.makedirs(outdir, exist_ok=True)
        meta = gam + ".json"
        self.bank = None
        if os.path.exists(meta):
            m = json.load(open(meta))
            self.bank = m["bank"]
            phys = GAM_PHYS + NEW_SEG + m["strshow"] - 0x5000
        else:
            phys = NATIVE_STRSHOW
        self.e = emu or BBKEmu()
        self.e.load_gam(gam, rom_dir=ROMS)
        self.bid = self.e.break_add(None, phys=phys, stop=False, capture=[
            {"addr": 0x28, "deref": True, "len": 1},
            {"addr": 0x28, "deref": True, "ptr_off": 1, "cstr": True, "len": 160},
            {"addr": 0x1812, "len": 4}, {"addr": 0x180F, "len": 2}])
        self.log, self.n = [], 0
        self.out = open(os.path.join(outdir, "texts.jsonl"), "w")

    def keys(self, *ks, wait=40, hold=4, n=1):
        for k in ks:
            for _ in range(n):
                self.e.tap(k, hold=hold, wait=wait)

    def run(self, frames):
        self.e.run_frames(frames)

    def drain(self):
        got = []
        for x in self.e.call("break.log", clear=True, max=100000)["entries"]:
            if x["id"] != self.bid:
                continue
            raw = bytes.fromhex(x["mem"][1])
            got.append({"frame": x["frame"], "x": x["a"], "y": x["mem"][0], "clip": x["mem"][2],
                        "vscr": x["mem"][3] != "0000", "raw": raw.hex(), "text": decode(raw, self.bank)})
        return got

    def step(self, name):
        self.n += 1
        draws = self.drain()
        shot = os.path.join(self.outdir, f"{self.n:03d}_{name}.png")
        self.e.screen(shot, scale=3)
        for d in draws:
            d["step"] = f"{self.n:03d}_{name}"
            self.out.write(json.dumps(d, ensure_ascii=False) + "\n")
        self.out.flush()
        return draws

    def save(self, name):
        self.e.call("snapshot.save", name=name)

    def load(self, name):
        self.e.call("snapshot.load", name=name)
        self.drain()

    def close(self):
        self.out.close()
        self.e.close()
