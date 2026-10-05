"""Build the English 三国霸业 .gam and a BPS patch for players.

    python3 tools/sgby/release.py VERSION
-> dist/ThreeKingdomsHegemony-<VERSION>.bps (+ README with checksums)
"""
import hashlib, os, subprocess, sys, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from bbkrpg import bps  # noqa: E402

ZH, TITLE = "三国霸业", "Three Kingdoms: Hegemony"
GAM = "gam4980/retroarch/downloads/bbk/三国霸业.gam"
OUT = "work/sgby/sgby_en.gam"
ver = sys.argv[1] if len(sys.argv) > 1 else "dev"
subprocess.run([sys.executable, "tools/sgby/build_en.py", "-o", OUT], check=True)
src, tgt = open(GAM, "rb").read(), open(OUT, "rb").read()
patch = bps.create(src, tgt, f"{TITLE} ({ZH}) English translation {ver}".encode())
assert bps.apply(patch, src) == tgt
name = f"ThreeKingdomsHegemony-{ver}"
os.makedirs("dist", exist_ok=True)
open(f"dist/{name}.bps", "wb").write(patch)
crc = lambda b: f"{zlib.crc32(b):08x}"
sha = lambda b: hashlib.sha1(b).hexdigest()
gver = src[0x37:0x40].split(b"\0")[0].decode("ascii")
open(f"dist/{name}.README.txt", "w").write(f"""{TITLE} - English translation of {ZH} (BBK native game) - {ver}

Apply {name}.bps to your own copy of {ZH}.gam with any BPS patcher
(Floating IPS, beat, Rom Patcher JS) and play the result on a BBK A4980/A4988
dictionary or in an emulator (gam4980 libretro core, BBKEmu).

Required original file ({gver}):
  {ZH}.gam  size {len(src)}  CRC32 {crc(src)}  SHA-1 {sha(src)}
Patched result:
  size {len(tgt)}  CRC32 {crc(tgt)}  SHA-1 {sha(tgt)}

The patch contains no BBK firmware and no game data beyond the translated
text, the English font and renderer, and the edited pictures. {ZH} belongs to
BBK (步步高) and its developers.
""")
print(f"dist/{name}.bps: {len(patch)} bytes")
