# bbk_tl — BBK dictionary game translation

Tools for translating BBKRPG games (伏魔记 first) on the BBK A-series
dictionaries. Plan: https://claude.ai/artifact/LRsiui8Mka3ZqHKQgsY3t2

## bbkrpg (format toolkit)

Pure Python 3.10+, no dependencies. Run as `python3 -m bbkrpg` (or
`pip install -e .` for a `bbkrpg` command). Anything that takes an archive
also accepts an unpacked directory or a `.gam`.

```sh
bbkrpg lib info fmj.LIB
bbkrpg lib unpack fmj.LIB work/fmj          # manifest.json + head.bin + res/<TYPE>/<t-s-i>.bin
bbkrpg lib pack work/fmj out.LIB             # byte-identical when nothing changed
bbkrpg gut disasm fmj.LIB 1-1-1              # one script as a labelled listing
bbkrpg gut disasm fmj.LIB --all -o work/gut  # every script
bbkrpg gut asm work/gut/1-1-1.gut 1-1-1.bin  # labels relocate, strings can change length
bbkrpg strings export fmj.LIB fmj.jsonl      # translation table, one row per string
bbkrpg lint fmj.LIB fmj.jsonl                # field limits, ASCII-only, menu items, bank fit
bbkrpg strings import fmj.LIB fmj.jsonl out.LIB [--gam game.gam]
bbkrpg detect game.gam                       # finds the archive, hashes the engine code
```

`strings import` always builds from the original archive, so row ids
(`gut/<key>@<addr>`, `GRS/<key>/name`, ...) stay stable across builds.
Scripts that grow stay in their bank when they fit; otherwise they move to a
new bank of the same type appended at the end of the archive.

Format notes live in the module docstrings (`bbkrpg/lib.py`, `bbkrpg/gut.py`).

## Games

`bbkrpg/games.py` holds one profile per game being translated: its `.gam`,
engine string table, image redraws and working paths. The scripts in
`tools/tl`, `tools/qa`, `tools/play` and `tools/release.py` take
`--game KEY` (or `BBK_GAME=KEY`) and default to `fmj`.

| Key | Game | Parts | Glossary | Release |
| --- | --- | --- | --- | --- |
| `fmj` | 伏魔记 | `translations/parts/` | `docs/glossary.jsonl` | Demonbane Chronicle v0.3 |
| `jy` | 金庸群侠传 | `translations/jy/parts/` | `docs/jy/glossary.jsonl` | Heroes of Jin Yong v0.2 |
| `yxts` | 英雄坛说 | `translations/yxts/parts/` | `docs/yxts/glossary.jsonl` | Heroes' Altar v0.1 |
| `szzm` | 十字之门 | `translations/szzm/parts/` | `docs/szzm/glossary.jsonl` | Cross Entry v0.1 |

```sh
python3 -m bbkrpg strings export gam4980/retroarch/downloads/bbk/金庸群侠传.gam work/jy.strings.jsonl
python3 -m bbkrpg gut disasm gam4980/retroarch/downloads/bbk/金庸群侠传.gam --all -o work/jy_gut
python3 tools/tl/build_en.py --game jy        # -> work/jy_en.gam
python3 tools/qa/sweep.py --game jy           # every script row in the emulator -> work/jy/qa/sweep
python3 tools/release.py --game jy v0.1       # -> dist/HeroesOfJinYong-v0.1.bps
tools/play/restart.sh jy                      # play daemon on work/jy/playthrough/daemon.sock
```

Adding a game: a profile in `bbkrpg/games.py` (engine-string offsets in
`bbkrpg/engine_text.py`, image redraws like `bbkrpg/images_jy.py`), then the
docs/<key>/ glossary and brief, parts, sweep and release. 金庸群侠传's notes
are in `docs/jy/` (`translating.md` is the brief its translators used).

## Tests

```sh
git clone --depth 1 https://github.com/stratosblue/BBKRPGSimulator refs/BBKRPGSimulator
python3 -m unittest discover -s tests
```

Covers byte-identical round trips (archive, directory form, every script via
rebuild and via text listing) for 伏魔记, 金庸群侠传, 赤壁之战 and 侠客行, and a
relocation stress test that lengthens every script string and checks each
jump still lands on the same instruction.

## bbkemu (agent emulator)

`bbkemu/` is a Cargo workspace: `core/` is BBKEmu's core vendored with small
patches (snapshots by clone, bus access recording, a split frame loop), and
`cli/` is a JSON-lines server with gbemu-cli's envelope. GPLv3, like BBKEmu.

```sh
cd bbkemu && cargo build --release        # -> bbkemu/target/release/bbkemu
python3 bbkemu/cli/tests/smoke.py         # boot, first dialogue, text.log ids
```

`bbkemu/PROTOCOL.md` lists the commands. `bbkemu/cli/py/bbkemu.py` is the
Python client; its `Hooks` class gives `text.log` (every string the OS draws)
tagged with `script.where` (the string-table row id that drew it).

## Playthrough route

`PLAYING.md`: play in `bbkplay` (records `routes/*.route.jsonl`); replay with
`input.replay` in `bbkemu`. Both apply inputs through `core/src/route.rs`, so
replays match frame for frame.

## Not done yet

- Phase 4: full-game input route, glossary, engine-code strings.
- 10 fan games have script variants the decoder rejects (e.g. 魔道传奇 leaves the
  script length field at 0); 伏魔记 and 87 others decode cleanly.

## Game set

`gam4980/` (gitignored) holds the 152-game set and the `8.BIN`/`E.BIN` BIOS
dumps; tests that need it skip when it is absent. `docs/recon.md` has the
伏魔记.gam byte map and the engine-build groups.
