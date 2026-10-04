# 金庸群侠传 (Heroes of Jin Yong): translator brief

Read before translating: `docs/jy/glossary.md` (conventions and decisions),
`docs/jy/glossary.jsonl` (every name and term), `docs/jy/story.md` (plot,
characters, voices). The 伏魔记 translation (`translations/parts/*.jsonl`
with `work/fmj.strings.jsonl`) is the house style to match.

## Workflow

```sh
python3 tools/tl/dump.py --game jy --chapters 9            # rows to translate, story order, with context
python3 tools/tl/dump.py --game jy --kinds grs.desc,mrs.desc
python3 tools/tl/check.py --game jy translations/jy/parts/ch09.jsonl
python3 tools/tl/build_en.py --game jy                     # merge all parts, build work/jy_en.gam
```

A part file is JSON lines `{"id": "...", "en": "..."}`, one per row, in
`translations/jy/parts/`. `check.py` must report no ERROR lines; read the
warnings (glossary misses, long dialogue) and fix the ones that are real.

`dump.py` lists each line once: a row whose kind and Chinese text repeat an
earlier row is left out, and `build_en.py` copies the first one's English to
it. Translate repeats yourself (dump `--all`) only when the context needs
different English; your row then wins.

The full script listings are in `work/jy_gut/<key>.gut` (key `1-9-3` for
`gut/1-9-3@...` rows): read them for who is speaking, what triggers a line,
what the choices lead to.

## Text rules

- Plain ASCII only: no curly quotes, accents, em dashes or ellipsis
  characters. Use `...` for `……`/`…`, `-` or ` - ` for dashes, `"` for quotes.
- Dialogue `say` rows: write natural English; the fitter wraps it into the
  box (3 rows a page, narrower beside a portrait) and pages it. More than 3
  pages draws a warning: tighten if you can. `\n` forces a new row and `\f` a
  new page; use them only where the layout needs it (poems, lists).
- Speaker tags: when the Chinese starts with `名字：` or `名字:`, start the English with
  `Name: ` (ASCII colon) using the glossary's English (the `en`, as in menus).
- `choice` rows (`@addr.1` / `.2`): at most 19 characters each, no line
  breaks. They are answers or actions the player picks; keep them short and
  parallel.
- `message` rows: a centred box of at most 4 rows of 140 px (about 25
  characters a row).
- `showgut` (the scrolling intro poem): may use `\n` for verse lines.
- Item/skill descriptions (`grs.desc`, `mrs.desc`): at most 3 rows of 108 px
  (about 18-20 characters a row; `check.py` measures it). Keep the stats
  (`防御+30` -> `DEF +30`, `攻击` ATK, `内力`/`真气` MP, `生命`/`体力` HP,
  `身法` AGI, `回合` turns). Drop the literal `\x0d\x0a` sequences in the source.
- Numbers and money: `两` is "tael(s)", `银票` "banknote".
- Names in running text follow the glossary; use the `alt` long form where a
  character would say it in full and it reads better.
- Fix obvious source typos and garbled lines quietly; when a line is
  deliberately unreadable (e.g. `!@#$%^&*` scribbles), keep the effect.
- The hero is whichever protagonist the player chose (幻吟风 or 紫灵儿); check
  story.md for how scripts refer to them and keep pronouns safe ("you").

## Register

Wuxia, but readable modern English: brisk, idiomatic, not archaic. Keep the
voice differences (beggars are blunt, monks polite, villains swagger, Wei
Xiaobao-type rogues joke). Martial terms follow the glossary (internal energy
for 内力, martial world for 江湖/武林 where it reads naturally).
