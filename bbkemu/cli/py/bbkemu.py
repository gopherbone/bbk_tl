"""Python client for bbkemu (stdlib only).

    from bbkemu import BBKEmu
    with BBKEmu("bbkemu/target/release/bbkemu") as e:
        e.load_gam("game.gam", rom_dir="gam4980/retroarch/system/gam4980")
        e.run_frames(1000)
        e.tap("ENTER")
        e.screen("shot.png", scale=3)
"""

from __future__ import annotations

import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BIN = os.path.join(HERE, "..", "..", "target", "release", "bbkemu")


class BBKEmuError(Exception):
    pass


class BBKEmu:
    def __init__(self, binary: str | None = None):
        self.p = subprocess.Popen([binary or DEFAULT_BIN], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        self._id = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        if self.p.poll() is None:
            try:
                self.call("quit")
            except Exception:  # noqa: BLE001 - shutting down anyway
                pass
            self.p.wait(timeout=5)

    def call(self, cmd: str, **params):
        self._id += 1
        self.p.stdin.write(json.dumps({"id": self._id, "cmd": cmd, "params": params}) + "\n")
        self.p.stdin.flush()
        line = self.p.stdout.readline()
        if not line:
            raise BBKEmuError(f"{cmd}: emulator exited")
        r = json.loads(line)
        if not r.get("ok"):
            raise BBKEmuError(f"{cmd}: {r.get('error')}")
        return r["result"]

    # conveniences ---------------------------------------------------------
    def load_gam(self, path, model="4988", rom_dir=None, **kw):
        return self.call("load_gam", path=path, model=model, rom_dir=rom_dir, **kw)

    def run_frames(self, n=1):
        return self.call("run.frames", n=n)

    def step(self, n=1):
        return self.call("step", n=n)

    def tap(self, key, hold=4, wait=4):
        return self.call("input.tap", key=key, hold=hold, wait=wait)

    def script(self, steps):
        return self.call("input.script", steps=steps)

    def screen(self, path=None, scale=1):
        return self.call("screen.capture", path=path, scale=scale)

    def regs(self):
        return self.call("regs.get")

    def read(self, addr=None, length=16, **where):
        if addr is not None:
            where["addr"] = addr
        return bytes.fromhex(self.call("mem.read", len=length, **where)["data"])

    def save(self, name):
        return self.call("snapshot.save", name=name)

    def load(self, name):
        return self.call("snapshot.load", name=name)

    def break_add(self, addr, **kw):
        return self.call("break.add", addr=addr, **kw)["id"]

    def watch_add(self, **kw):
        return self.call("watch.add", **kw)["id"]


# --- BBKRPG text and script hooks ---------------------------------------------
#
# TEXT_DRAW: the OS draw-string handler (OS call 0x2E), once per call, after
# it has loaded the string pointer into $2f/$30. It is in the OS ROM, so it is
# the same for every game. Args at ($28): [0] y, [1..2] string pointer, ...
# SCRIPT_FETCH: the 伏魔记 engine's script interpreter reading an opcode via
# ($20). Engine-specific: re-find it for other engine builds (docs/recon.md).
TEXT_DRAW_PHYS = 0xE94843
SCRIPT_FETCH_PHYS = 0x211134


def _gb(h: str) -> str:
    b = bytes.fromhex(h)
    try:
        return b.decode("gb2312")
    except UnicodeDecodeError:
        return b.decode("gb2312", errors="backslashreplace")


class Hooks:
    """text.log and script.where on top of silent breakpoints."""

    def __init__(self, emu: BBKEmu, script_fetch_phys: int = SCRIPT_FETCH_PHYS):
        self.e = emu
        self.text_id = emu.break_add(None, phys=TEXT_DRAW_PHYS, stop=False, capture=[
            {"addr": 0x2F, "deref": True, "cstr": True, "len": 256},
            {"addr": 0x28, "deref": True, "len": 8},
        ])
        self.fetch_id = emu.break_add(None, phys=script_fetch_phys, stop=False, capture=[
            {"addr": 0x20, "deref": True, "phys": True},
        ])
        self.where = None   # last script position seen
        self._map_cache = {}

    def _script_pos(self, phys_hex: str):
        if phys_hex not in self._map_cache:
            m = self.e.call("lib.map", phys=int(phys_hex, 16))
            pos = None
            if m.get("resource", "").startswith("GUT/") and "script_addr" in m:
                pos = (m["resource"][4:], int(m["script_addr"], 16))
            self._map_cache[phys_hex] = pos
        return self._map_cache[phys_hex]

    def drain(self):
        """Consume break.log; return text draws, each tagged with the script
        instruction executing when it was drawn (key, script address)."""
        out = []
        for x in self.e.call("break.log", clear=True, max=100000)["entries"]:
            if x["id"] == self.fetch_id:
                pos = self._script_pos(x["mem"][0])
                if pos:
                    self.where = pos
            elif x["id"] == self.text_id:
                args = bytes.fromhex(x["mem"][1])
                out.append({"frame": x["frame"], "y": args[0], "text": _gb(x["mem"][0]),
                            "raw": x["mem"][0], "args": x["mem"][1], "script": self.where})
        return out


class EnHooks(Hooks):
    """Hooks for English builds (bbkrpg fontpatch): text is drawn by our
    renderer, so log its entry points and decode text-bank tokens with the
    bank written next to the .gam (<name>.bank.json)."""

    def __init__(self, emu: BBKEmu, bank_path: str, script_fetch_phys: int = SCRIPT_FETCH_PHYS):
        import sys as _sys
        _sys.path.insert(0, os.path.join(HERE, "..", "..", ".."))
        from bbkrpg import fontpatch
        self.bank = json.load(open(bank_path))["bank"]
        _, syms = fontpatch.build_segment([0])
        base = 0x20D000 + 0x48000 - 0x5000          # font segment at .gam 0x48000, CPU $5000
        self.e = emu
        self.text_id = emu.break_add(None, phys=base + syms["drawstring"], stop=False, capture=[
            {"addr": 0x28, "deref": True, "len": 1},
            {"addr": 0x28, "deref": True, "ptr_off": 1, "cstr": True, "len": 160}])
        self.msg_id = emu.break_add(None, phys=base + syms["msgbox"], stop=False, capture=[
            {"addr": 0x28, "deref": True, "len": 1},
            {"addr": 0x28, "deref": True, "ptr_off": 0, "cstr": True, "len": 160}])
        self.fetch_id = emu.break_add(None, phys=script_fetch_phys, stop=False, capture=[
            {"addr": 0x20, "deref": True, "phys": True}])
        self.where = None
        self._map_cache = {}

    def _decode(self, raw: bytes) -> str:
        out, i = [], 0
        while i < len(raw):
            b = raw[i]
            if b in (0xFE, 0xFF) and i + 3 < len(raw):
                n = ((raw[i + 1] & 0x7F) << 7) | (raw[i + 3] & 0x7F)
                out.append(self.bank[n] if n < len(self.bank) else f"<tok{n}>")
                i += 4
            elif b == 0xFD and i + 1 < len(raw):
                n = raw[i + 1] & 0x7F
                out.append(self.bank[n] if n < len(self.bank) else f"<tok{n}>")
                i += 2
            elif b == 0xFC:
                i += 2
            elif b < 0x80:
                out.append(chr(b)); i += 1
            else:
                out.append(raw[i:i + 2].decode("gb2312", "replace")); i += 2
        return "".join(out)

    def _read_str(self, ptr: int) -> bytes:
        data = self.e.read(ptr, 96)
        return data.split(b"\0", 1)[0]

    def drain(self):
        out = []
        for x in self.e.call("break.log", clear=True, max=100000)["entries"]:
            if x["id"] == self.fetch_id:
                pos = self._script_pos(x["mem"][0])
                if pos:
                    self.where = pos
            elif x["id"] in (self.text_id, self.msg_id):
                y = bytes.fromhex(x["mem"][0])[0] if x["id"] == self.text_id else None
                raw = bytes.fromhex(x["mem"][1])
                out.append({"frame": x["frame"], "y": y, "kind": "msg" if y is None else "text",
                            "text": self._decode(raw), "script": self.where})
        return out
