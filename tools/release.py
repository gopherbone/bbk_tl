"""Build the English .gam and a BPS patch for players.

  python3 tools/release.py VERSION
-> dist/DemonbaneChronicle-<VERSION>.bps (+ README, checksums). The patch is
applied to the player's own 伏魔记.gam (BBK A4980/A4988, Ver1.3, CRC32 below).
"""
import hashlib, os, subprocess, sys, zlib
sys.path.insert(0, ".")
from bbkrpg import bps

ver = sys.argv[1] if len(sys.argv) > 1 else "dev"
GAM = "gam4980/retroarch/downloads/bbk/伏魔记.gam"
subprocess.run([sys.executable, "tools/tl/build_en.py", "--out", "work/fmj_en.gam"], check=True)
src = open(GAM, "rb").read()
tgt = open("work/fmj_en.gam", "rb").read()
patch = bps.create(src, tgt, f"Demonbane Chronicle (伏魔记) English translation {ver}".encode())
assert bps.apply(patch, src) == tgt
name = f"DemonbaneChronicle-{ver}"
open(f"dist/{name}.bps", "wb").write(patch)
crc = lambda b: f"{zlib.crc32(b):08x}"
sha = lambda b: hashlib.sha1(b).hexdigest()
readme = f"""Demonbane Chronicle - English translation of 伏魔记 (BBK BBKRPG) - {ver}

Apply {name}.bps to your own copy of 伏魔记.gam with any BPS patcher
(Floating IPS, beat, Rom Patcher JS) and play the result on a BBK A4980/A4988
dictionary or in an emulator (gam4980 libretro core, BBKEmu).

Required original file (Ver1.3):
  伏魔记.gam  size {len(src)}  CRC32 {crc(src)}  SHA-1 {sha(src)}
Patched result:
  size {len(tgt)}  CRC32 {crc(tgt)}  SHA-1 {sha(tgt)}

The patch contains no BBK firmware and no game data beyond the translated
text, font and the English renderer. 伏魔记 belongs to BBK.
"""
open(f"dist/{name}.README.txt", "w").write(readme)
print(f"dist/{name}.bps: {len(patch)} bytes")
