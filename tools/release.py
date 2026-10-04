"""Build the English .gam and a BPS patch for players.

  python3 tools/release.py [--game fmj] VERSION
-> dist/<Title>-<VERSION>.bps (+ README, checksums). The patch is applied to
the player's own copy of the game (BBK A4980/A4988, CRC32 below).
"""
import hashlib, subprocess, sys, zlib
sys.path.insert(0, ".")
from bbkrpg import bps, games

game = games.from_argv()
if not game.title_en:
    sys.exit(f"{game.key}: no English title in bbkrpg/games.py yet")
ver = sys.argv[1] if len(sys.argv) > 1 else "dev"
subprocess.run([sys.executable, "tools/tl/build_en.py", "--game", game.key, "--out", game.en_gam], check=True)
src = game.read_gam()
tgt = open(game.en_gam, "rb").read()
patch = bps.create(src, tgt, f"{game.title_en} ({game.zh}) English translation {ver}".encode())
assert bps.apply(patch, src) == tgt
name = f"{game.title_en.replace(' ', '')}-{ver}"
open(f"dist/{name}.bps", "wb").write(patch)
gver = src[0x37:0x40].split(b"\0")[0].decode("ascii")   # header version string, e.g. Ver1.3
crc = lambda b: f"{zlib.crc32(b):08x}"
sha = lambda b: hashlib.sha1(b).hexdigest()
readme = f"""{game.title_en} - English translation of {game.zh} (BBK BBKRPG) - {ver}

Apply {name}.bps to your own copy of {game.zh}.gam with any BPS patcher
(Floating IPS, beat, Rom Patcher JS) and play the result on a BBK A4980/A4988
dictionary or in an emulator (gam4980 libretro core, BBKEmu).

Required original file ({gver}):
  {game.zh}.gam  size {len(src)}  CRC32 {crc(src)}  SHA-1 {sha(src)}
Patched result:
  size {len(tgt)}  CRC32 {crc(tgt)}  SHA-1 {sha(tgt)}

The patch contains no BBK firmware and no game data beyond the translated
text, font and the English renderer. {game.zh} belongs to BBK.
"""
open(f"dist/{name}.README.txt", "w").write(readme)
print(f"dist/{name}.bps: {len(patch)} bytes")
