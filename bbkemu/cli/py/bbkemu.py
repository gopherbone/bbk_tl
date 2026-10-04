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
