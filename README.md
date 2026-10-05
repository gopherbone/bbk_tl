# bbk_tl — BBK dictionary game translation

Tools for translating BBKRPG games (伏魔记 first) on the BBK A-series
dictionaries. The games, firmware and translated builds are not in this
repository: releases are BPS patches applied to your own copy of a game.

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
| `fmj` | 伏魔记 | `translations/parts/` | `docs/glossary.jsonl` | Demonbane Chronicle v0.5 |
| `jy` | 金庸群侠传 | `translations/jy/parts/` | `docs/jy/glossary.jsonl` | Heroes of Jin Yong v0.4 |
| `yxts` | 英雄坛说 | `translations/yxts/parts/` | `docs/yxts/glossary.jsonl` | Heroes' Altar v0.3 |
| `szzm` | 十字之门 | `translations/szzm/parts/` | `docs/szzm/glossary.jsonl` | Cross Entry v0.3 |
| `xkx` | 侠客行 | `translations/xkx/parts/` | `docs/xkx/glossary.jsonl` | Ode to Gallantry v0.1 |

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

## 三国霸业 (sgby, native game)

三国霸业 is not a BBKRPG game: it is BBK's own 6502 program with an embedded
resource archive (`dat.lib`, identical to iBaye's `src/dat.lib.orig`). Its
toolkit is the `sgby/` package; `docs/sgby/recon.md` explains the format, the
English renderer and the layout patches.

```sh
python3 tools/sgby/export.py                  # -> translations/sgby/strings.jsonl (budgets, usage context)
python3 tools/sgby/check.py                   # translations/sgby/en.jsonl against the pixel budgets
python3 tools/sgby/build_en.py                # en.jsonl + fix*.jsonl -> work/sgby/sgby_en.gam
python3 tools/sgby/tour.py work/sgby/sgby_en.gam work/sgby/qa/en && python3 tools/sgby/sheets.py work/sgby/qa/en
python3 tools/sgby/coverage.py work/sgby/qa/en/texts.jsonl
python3 tools/sgby/release.py v0.1            # -> dist/ThreeKingdomsHegemony-v0.1.bps
```

The tour needs `refs/iBaye` only for `export.py` (usage context):
`git clone --depth 1 https://gitee.com/bgwp/iBaye.git refs/iBaye`.

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

## Credits

The games belong to their authors; the English patches change only text,
images and the renderer, and ship no game data.

| Game | English | Original authors |
| --- | --- | --- |
| 伏魔记 | Demonbane Chronicle | 通宵虫 (Allnighter) and 南方小鬼 (South Imp), with the BBK Game Team (2004) |
| 金庸群侠传 | Heroes of Jin Yong | BOSS工作室 (BOSS Studio) |
| 英雄坛说 | Heroes' Altar | 才子工作室 (Caizi Studio): 金远见 (Jin Yuanjian), 柴梓 (Chai Zi) (2005) |
| 十字之门 | Cross Entry | 翼王 (Yiwang) |
| 三国霸业 | Three Kingdoms: Hegemony | BBK Game Group; code by 通宵虫 (Allnighter) and 南方小鬼 (South Imp), art by Sunday (2005) |

The BBK A-series dictionaries, their firmware and the BBKRPG engine are BBK's
(步步高). Translation, tools, the bbk_tl Sans font and the English renderer:
gopherbone, with Claude (Anthropic).

Third-party work this builds on:

- [BBKEmu](https://github.com/AloysHF/BBKEmu) by Aloys (AloysHF), GPL-3.0:
  vendored with patches as `bbkemu/core` (see `bbkemu/core/UPSTREAM`); the
  `bbkemu` CLI and `bbkplay` are built on it.
- [gam4980](https://codeberg.org/iyzsong/gam4980) by iyzsong, based on the
  [BA4988 simulator](https://gitee.com/BA4988/BBK-simulator) by 无云 and
  [vrEmu6502](https://github.com/visrealm/vrEmu6502) by Troy Schrapel, GPL-3.0:
  the web player's core, as built by
  [iuxt/bbk-games](https://github.com/iuxt/bbk-games) (`site/vendor/gam4988`).
- [BBKRPGSimulator](https://github.com/stratosblue/BBKRPGSimulator) by
  stratosblue: the reference for the BBKRPG archive, script and record
  formats (`bbkrpg/gut.py`, `bbkrpg/strings.py`) and the test oracle.
- [iBaye](https://gitee.com/bgwp/iBaye): usage context for 三国霸业's strings
  (`sgby`).
- The bbkemu CLI protocol follows gopherbone's gbemu-cli.

## License

GPL-3.0-or-later (`LICENSE`), the license of the emulator code vendored here.
