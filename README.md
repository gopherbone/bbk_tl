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

## Tests

```sh
git clone --depth 1 https://github.com/stratosblue/BBKRPGSimulator refs/BBKRPGSimulator
python3 -m unittest discover -s tests
```

Covers byte-identical round trips (archive, directory form, every script via
rebuild and via text listing) for 伏魔记, 金庸群侠传, 赤壁之战 and 侠客行, and a
relocation stress test that lengthens every script string and checks each
jump still lands on the same instruction.

## Not done yet

- `gam split/join` are provisional: the archive is found by signature, and join
  only accepts a same-size archive until a real `.gam` is mapped (phase 1).
- bbkemu-cli (phase 3) needs `伏魔记.gam` plus `8.BIN`/`E.BIN` dumps.
