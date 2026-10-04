"""Headless gam4980 (libretro core) driver for comparisons with bbkemu.

Build the core first:
  SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk \
    clang -O2 -shared -fPIC -o work/gam4980.dylib gam4980/src/libretro.c
"""

from __future__ import annotations

import ctypes as C
import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "work", "gam4980.dylib")
SYSTEM_DIR = os.path.join(ROOT, "gam4980", "retroarch", "system")   # holds gam4980/8.BIN, E.BIN

JOY = {"B": 0, "Y": 1, "SELECT": 2, "START": 3, "UP": 4, "DOWN": 5, "LEFT": 6, "RIGHT": 7,
       "A": 8, "X": 9, "L": 10, "R": 11}
KEYS = {"ENTER": "A", "EXIT": "B", "UP": "UP", "DOWN": "DOWN", "LEFT": "LEFT", "RIGHT": "RIGHT"}

ENV_CB = C.CFUNCTYPE(C.c_bool, C.c_uint, C.c_void_p)
VIDEO_CB = C.CFUNCTYPE(None, C.c_void_p, C.c_uint, C.c_uint, C.c_size_t)
AUDIO_CB = C.CFUNCTYPE(None, C.c_int16, C.c_int16)
AUDIO_BATCH_CB = C.CFUNCTYPE(C.c_size_t, C.c_void_p, C.c_size_t)
POLL_CB = C.CFUNCTYPE(None)
STATE_CB = C.CFUNCTYPE(C.c_int16, C.c_uint, C.c_uint, C.c_uint, C.c_uint)


class GameInfo(C.Structure):
    _fields_ = [("path", C.c_char_p), ("data", C.c_void_p), ("size", C.c_size_t), ("meta", C.c_char_p)]


class Gam4980:
    def __init__(self, lib=LIB):
        self.lib = C.CDLL(lib)
        self.pressed: str | None = None
        self.frame = 0
        self.fb = None
        self._sysdir = C.c_char_p(SYSTEM_DIR.encode())

        def env(cmd, data):
            if cmd == 9:            # GET_SYSTEM_DIRECTORY
                C.cast(data, C.POINTER(C.c_char_p))[0] = self._sysdir.value
                return True
            return False

        def video(data, w, h, pitch):
            if data:
                self.fb = (C.string_at(data, h * pitch), w, h, pitch)

        def state(port, device, index, id_):
            return 1 if (device == 1 and self.pressed is not None and JOY[self.pressed] == id_) else 0

        self._cbs = [ENV_CB(env), VIDEO_CB(video), AUDIO_CB(lambda l, r: None),
                     AUDIO_BATCH_CB(lambda d, n: n), POLL_CB(lambda: None), STATE_CB(state)]
        L = self.lib
        L.retro_set_environment(self._cbs[0])
        L.retro_set_video_refresh(self._cbs[1])
        L.retro_set_audio_sample(self._cbs[2])
        L.retro_set_audio_sample_batch(self._cbs[3])
        L.retro_set_input_poll(self._cbs[4])
        L.retro_set_input_state(self._cbs[5])
        L.retro_init()
        L.retro_get_memory_data.restype = C.c_void_p

    def load(self, path):
        data = open(path, "rb").read()
        self._buf = C.create_string_buffer(data, len(data))
        info = GameInfo(path.encode(), C.cast(self._buf, C.c_void_p), len(data), None)
        if not self.lib.retro_load_game(C.byref(info)):
            raise RuntimeError("load failed")

    def run(self, n=1):
        for _ in range(n):
            self.lib.retro_run()
            self.frame += 1

    def tap(self, key, hold=4, wait=4):
        self.pressed = KEYS[key]
        self.run(hold)
        self.pressed = None
        self.run(wait)

    def ram(self, addr, n=1):
        p = self.lib.retro_get_memory_data(2)
        return C.string_at(p + addr, n)

    def flash(self, index, n=1):
        p = self.lib.retro_get_memory_data(0)
        return C.string_at(p + index, n)

    def pixels(self):
        raw, w, h, pitch = self.fb
        return [[struct.unpack_from("<H", raw, y * pitch + 2 * x)[0] != 0xD6DA for x in range(w)] for y in range(h)]

    def screen(self, path=None, scale=2):
        px = self.pixels()
        h, w = len(px), len(px[0])
        rows = []
        for y in range(h * scale):
            rows.append(b"\0" + bytes(0x10 if px[y // scale][x // scale] else 0xD8 for x in range(w * scale)))
        ch = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
        png = (b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w * scale, h * scale, 8, 0, 0, 0, 0))
               + ch(b"IDAT", zlib.compress(b"".join(rows))) + ch(b"IEND", b""))
        if path:
            open(path, "wb").write(png)
        return zlib.crc32(b"".join(bytes(r) for r in px))

    def regs(self):
        return None
