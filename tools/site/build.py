#!/usr/bin/env python3
"""Build the static web player site into site/dist (deploy with wrangler).

    python3 tools/site/build.py [--no-shots]

Copies site/src and the vendored gam4988 web core, writes the firmware
(8.BIN + E.BIN, the core's 4 MiB legacy mode) and every game version from
site/catalog.json under content-hashed names, then writes dist/games.json.
Versions are a base .gam, optionally with a BPS patch from dist/.

Unless --no-shots, each game is booted in the same core compiled natively
(tools/site/shot.c) as a smoke test, and its title screen becomes the card
image. Firmware and games stay out of git: site/dist is ignored.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from bbkrpg import bps  # noqa: E402

SITE = ROOT / "site"
DIST = SITE / "dist"
WORK = ROOT / "work" / "site"
CORE = SITE / "vendor" / "gam4988"
SDK = "/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk"
SHOT_FRAME = 1000             # past the boot logo: title screens are up
LCD_BG = (120, 140, 104)      # the core's default background (RGB565 0x7C6D)


def hashed(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:10]


def version_bytes(v: dict) -> bytes:
    base = (ROOT / v["base"]).read_bytes()
    if "patch" in v:
        return bps.apply((ROOT / v["patch"]).read_bytes(), base)
    return base


def shot_tool() -> Path:
    exe = WORK / "shot"
    srcs = [ROOT / "tools/site/shot.c", CORE / "src/web_main.c", CORE / "src/s6502.c"]
    if exe.exists() and all(exe.stat().st_mtime > s.stat().st_mtime for s in srcs):
        return exe
    WORK.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if Path(SDK).exists():
        env["SDKROOT"] = SDK
    subprocess.run(["cc", "-O2", "-w", "-I", str(ROOT / "tools/site/stub"), "-o", str(exe),
                    str(srcs[0]), str(srcs[1])], check=True, env=env)
    return exe


def title_shot(bios: Path, gam: Path, out_png: Path) -> None:
    """Boot `gam`, check the screen is not blank, save frame SHOT_FRAME at 2x."""
    from PIL import Image

    exe = shot_tool()
    tmp = WORK / "shots"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    script = tmp / "script.txt"
    script.write_text(f"{SHOT_FRAME} shot\n")
    res = subprocess.run([str(exe), str(bios), str(gam), str(tmp / "f"), str(script)],
                         capture_output=True, text=True)
    if res.returncode != 0 or "init 0" not in res.stdout or "load 1" not in res.stdout:
        raise SystemExit(f"{gam.name}: core failed to boot it:\n{res.stdout}{res.stderr}")
    img = Image.open(next(tmp.glob("f_*.pgm")))
    if img.getextrema()[0] == img.getextrema()[1]:
        raise SystemExit(f"{gam.name}: blank screen at frame {SHOT_FRAME}")
    # the dump is the green channel: dark pixels are set
    lit = img.point(lambda p: 255 if p < 64 else 0)
    rgb = Image.new("RGB", img.size, LCD_BG)
    rgb.paste((20, 24, 18), mask=lit)
    rgb.resize((img.width * 2, img.height * 2), Image.NEAREST).save(out_png, optimize=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-shots", action="store_true", help="skip booting games natively")
    args = ap.parse_args()

    catalog = json.loads((SITE / "catalog.json").read_text())
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(SITE / "src", DIST)
    shutil.copytree(CORE, DIST / "vendor/gam4988")
    for d in ("firmware", "games", "patches", "img/games"):
        (DIST / d).mkdir(parents=True, exist_ok=True)

    fw = b"".join((ROOT / p).read_bytes() for p in catalog["firmware"])
    assert len(fw) == 4 << 20, "8.BIN + E.BIN should be 4 MiB"
    bios_name = f"firmware/bios-{hashed(fw)}.bin"
    (DIST / bios_name).write_bytes(fw)

    games = []
    for g in catalog["games"]:
        out = {k: v for k, v in g.items() if k != "versions"}
        out["versions"] = []
        for v in g["versions"]:
            data = version_bytes(v)
            name = f"games/{g['id']}-{v['lang']}-{hashed(data)}.gam"
            (DIST / name).write_bytes(data)
            ov = {k: v[k] for k in ("lang", "label", "version", "status")}
            ov.update(url=name, size=len(data))
            if "patch" in v:
                patch = ROOT / v["patch"]
                shutil.copy(patch, DIST / "patches" / patch.name)
                ov["patch"] = f"patches/{patch.name}"
            if not args.no_shots:
                png = f"img/games/{g['id']}-{v['lang']}.png"
                title_shot(DIST / bios_name, DIST / name, DIST / png)
                ov["shot"] = png
            out["versions"].append(ov)
            print(f"  {name}  {len(data):,} bytes  ({v['label']} {v['version']})")
        games.append(out)

    (DIST / "games.json").write_text(json.dumps({"bios": bios_name, "games": games},
                                                ensure_ascii=False, indent=1) + "\n")
    print(f"built {DIST.relative_to(ROOT)}: {len(games)} games, firmware {bios_name}")


if __name__ == "__main__":
    main()
