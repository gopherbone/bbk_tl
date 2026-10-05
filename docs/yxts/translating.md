# 英雄坛说 (Heroes' Altar): translator brief

Read before translating: `docs/yxts/glossary.md` (conventions and decisions),
`docs/yxts/glossary.jsonl` (every name and term), `docs/yxts/story.md` (plot,
characters, voices, systems). The 伏魔记 translation (`translations/parts/*.jsonl`
with `work/fmj.strings.jsonl`) is the house style to match; 金庸群侠传
(`translations/jy/parts/`) is the closest sibling.

## Workflow

```sh
python3 tools/tl/dump.py --game yxts --chapters 1               # rows to translate, story order, with context
python3 tools/tl/dump.py --game yxts --kinds grs.desc,mrs.desc
python3 tools/tl/check.py --game yxts translations/yxts/parts/ch01.jsonl
python3 tools/tl/build_en.py --game yxts                        # merge all parts, build work/yxts_en.gam
```

A part file is JSON lines `{"id": "...", "en": "..."}`, one per row, in
`translations/yxts/parts/`. `check.py` must report no ERROR lines; read the
warnings (glossary misses, long dialogue) and fix the ones that are real.
All name rows (items, arts, ARS, maps, scene banners) are already filled by
`parts/auto.jsonl` from the glossary (`python3 tools/tl/autofill.py --game yxts`
after a glossary change); the engine strings are in `parts/engine.jsonl`.

`dump.py` lists each line once: a row whose kind and Chinese text repeat an
earlier row is left out, and `build_en.py` copies the first one's English to
it. Translate repeats yourself (dump `--all`) only when the context needs
different English; your row then wins.

The full script listings are in `work/yxts_gut/<key>.gut` (key `1-4-1` for
`gut/1-4-1@...` rows): read them for who is speaking, what triggers a line,
what the choices lead to. Script groups: 1-0 credits and system menus, 1-1
Safehaven, 1-2 wilds and caves, 1-3..1-8 the six sect seats (Jade Peak,
Snowpeak, Mt. Wuzhi, Mt. Wudang, Shang Fort, Icefire Isle), 1-9 shared
handlers, 1-10 Prodigy Park / Demon Cave / Nether / mines / Demonspire, 1-11
My Sect and the Dreamscape, 1-12 the Demonspire basement, 1-255 item scripts.

## Text rules

- Plain ASCII only: no curly quotes, accents, em dashes or ellipsis
  characters. Use `...` for `……`/`…`/`......`, `-` or ` - ` for dashes, `"` for quotes,
  `~` is fine (the font has it; "Boo-hoo~~").
- Dialogue `say` rows: write natural English; the fitter wraps it into the
  box (3 rows a page, narrower beside a portrait) and pages it. More than 3
  pages draws a warning: tighten if you can. `\n` forces a new row and `\f` a
  new page; use them only where the layout needs it (Granny's rhymes, lists).
  Six source lines contain a literal `\x0d` (1-7-6, 1-10-1, 1-255-30): drop it.
- **Who is speaking**: `pic` is a portrait, not a speaker. Tagged lines
  (`柴梓:`, `SSK:`...) are that character; `pic=4` is Yuxin, `pic=5` Bingyan;
  untagged `pic=0` lines in story scenes are usually **the hero** answering, in
  shops the shopkeeper. Check the .gut when unsure.
- Speaker tags: when the Chinese starts with `名字：` or `名字:`, start the English with
  `Name: ` (ASCII colon) using the glossary's `en` ("Chai Zi:", "System:", "Players:",
  "Who Am I:", "???:", "Deng Shiyu:"). Tag-like prefixes that are not speakers
  ("你的声望：", "当前任务:", "锻造技能：") become labels: "Fame: Nobody", "Current
  quest: buy wine.", "Forging: Expert".
- `choice` rows (`@addr.1` / `.2`): at most 19 characters each, no line
  breaks. Keep pairs short and parallel ("Buy" / "Don't buy", "Challenge" / "Leave").
- `menu` rows: same number of space-separated items as the Chinese, **no spaces
  inside an item**. Use the glossary's one-word forms (Safehaven, Snowpeak, Shang,
  Jade, Wuzhi, Icefire, Wudang, Prodigy, Sect; Flower, Iga, Snow, Lotus, Bagua;
  Forging, Literacy, Step, Qi, Parry, Fist, Sword, Blade, Staff, Whip; Thunder Wind
  Earth Water Fire); otherwise join words with hyphens, never CamelCase (Pay-Heal,
  Sect-Qi, Warm-Mist, Heaven-Gale, 1888RMB). Hero menu: "Dugu Ouyang Tang". Items up
  to 11 characters fit (the box grows 8 px a character).
- `message` rows: a centred box of at most 4 rows of 140 px (about 25
  characters a row). The MUD "look" texts (`★...`) are messages: write each ★ as `*` (text must be ASCII) and
  stay within 4 rows; the source pads them with full-width spaces, drop the padding.
- `showgut` (the intro scroll, credits, end note, the opened letter) scrolls in 20-column
  rows; `\n` may break lines. `timemsg` rows (loading / Healthy Gaming Advice / studio
  card) are timed message boxes fed from the text bank: `\n` breaks rows, at most 5 rows
  of 140 px (`check.py` errors past 5). Do not copy the source's 16-byte space padding.
- Item/art descriptions (`grs.desc`, `mrs.desc`): at most 3 rows of 108 px
  (about 18-20 characters a row; `check.py` measures it). Keep the stats with the
  status-screen words: `防御+30` -> `DEF+30`, `攻击` ATK, `灵力` SPI, `身法`/`速度` AGI,
  `运气` LCK, `生命` HP (`生命上限` Max HP), `真气` MP (`真气上限` Max MP), `回合`
  turns, `全体`/`单体` all / one, `解毒` cures Poison, `解乱封眠` cures Cnf/Sil/Slp,
  `负面状态` ailments. Bare stat lines ("hp100", "HP100MP50") -> "HP+100", "HP+100 MP+50".
  Keep the descriptions' jokey asides in brackets. Four MRS descriptions are cut
  mid-sentence by the field: finish them briefly.
- **内力 is "qi", not MP**: a 0-100 pool the scripts keep (meditation, teleport,
  Dreamscape, gathering). "你的内力不足" = "Not enough qi!". 真气 is MP.
- Numbers and money: 元 and RMB are both "RMB" ("Costs 500 RMB"); `W` (万) is
  ten thousand: 1W = 10K, 5W = 50K, 16W = 160K, 200W = 2M; 两 = taels where the text
  says 两; 英雄币 hero coins. Chinese numerals in ladders ("二十多点" -> "20-odd points",
  "十多岁" -> "in your teens").
- Names in running text follow the glossary; use the `alt` long form where a
  character would say it in full and it reads better.
- Fix obvious source typos quietly (list in glossary.md); keep deliberate puns
  and the deliberately unreadable bits (`@#$%^&*`, `***`, `&*&*&*`, `嗷嗷呜` as "awoo").
- The hero is whichever of Dugu Sheng / Ouyang Jian / Tang Jing the player chose;
  all three are the same 14-year-old boy and are never named in dialogue. Address
  him as "you"; "he" is safe.

## Register

A teenager's comedy RPG for his forum friends: brisk, cheeky modern English with
a light wuxia veneer. Keep every joke, fourth-wall aside and insult; prefer an
English joke of the same shape to a footnote. Net slang becomes English chat
slang (886 "Bye!", 5555 "Boo-hoo", 汗 "*sweat*", 晕 "Ugh"/"Good grief", 靠/KAO
"Damn", 嘎嘎 "Hehe", 偶 = "me", MM "girls", 小KS "piece of cake", 94 = "just").
Keep mild swearing mild (TMD "damn it"). Voices: Chai Zi bossy and smug;
Yuxin bubbly and bossy ("yours truly"); Bingyan snappy; the hero cocky and
whiny; villains sneer ("Kid, you got lucky this time"); Gu Yanwu and Mr. Wenshi
stiffly scholarly; the Elder an old man; forum cameos each with one shtick
(Deng Shiyu's prices, SSK's spite, Xiaoyao's singing, Flatline Love's sermon).
Martial terms follow the glossary (martial world for 江湖/武林, Sect Head for
掌门, Archdemon for 大恶魔/大魔头).
