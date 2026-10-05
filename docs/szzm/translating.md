# 十字之门 (Cross Entry): translator brief

Read before translating: `docs/szzm/glossary.md` (conventions and decisions), `docs/szzm/glossary.jsonl` (every
name and term), `docs/szzm/story.md` (plot, characters, voices, systems). The 伏魔记 translation
(`translations/parts/*.jsonl` with `work/fmj.strings.jsonl`) is the house style; 英雄坛说
(`translations/yxts/parts/`) is the latest sibling.

## Workflow

```sh
python3 tools/tl/dump.py --game szzm --chapters 1               # rows to translate, story order, with context
python3 tools/tl/dump.py --game szzm --kinds grs.desc,mrs.desc
python3 tools/tl/check.py --game szzm translations/szzm/parts/ch1.jsonl
python3 tools/tl/build_en.py --game szzm                        # merge all parts, build work/szzm_en.gam
```

A part file is JSON lines `{"id": "...", "en": "..."}`, one per row, in `translations/szzm/parts/`. `check.py`
must report no ERROR lines; read the warnings (glossary misses, long dialogue) and fix the real ones. All name
rows (items, skills, ARS, maps, scene banners: 357 rows) are already filled by `parts/auto.jsonl` from the glossary
(`python3 tools/tl/autofill.py --game szzm` after a glossary change); the engine strings are in
`parts/engine.jsonl`. Do not put name rows in your part.

`dump.py` lists each line once: a row whose kind and Chinese text repeat an earlier row is left out, and
`build_en.py` copies the first one's English to it. Translate repeats yourself (dump `--all`) only when the
context needs different English; your row then wins.

The full script listings are in `work/szzm_gut/<key>.gut` (key `1-3-5` for `gut/1-3-5@...` rows): read them for
who is speaking, what triggers a line, what the choices lead to.

### Script groups and the split

| group | content | unique zh chars |
|---|---|---|
| 1-0 | field-skill handlers (Ignite / Dig / Climb / Smash), Yiwang's cameo | 75 |
| 1-1 | Kabras: New Game and prologue, temple, exam, Royal Library, workshop, shops, side quests, graveyard, sewers | 4661 (about 800 is Genesis 1, use the KJV) |
| 1-2 | Snowblade: Reiter, the Magic Institute break-in, Crest I, side quests | 3489 |
| 1-3 | Silverleaf: Heath, the Moon's hideout, the mine, Crest II, the doctor | 2883 |
| 1-4 | Nightstar: the Eternal Darkness, Crest III, side quests | 681 |
| 1-5 | the Forgotten City, Crest IV, the black-winged giant | 703 |
| 1-6 | the roads: Leoz (twice), graveyard tunnel, chests | 1299 |
| 1-7 | finale: Kabras taken, the palace depths, the Cross Entry, epilogue, credits | 1179 |
| 1-255 | item scripts (Homeward, key prompts) | 50 |
| grs.desc / mrs.desc | item and skill descriptions | 1200 / 546 |

Parallel split (about 4000 characters each): **A** 1-0, 1-1, 1-255 (`parts/ch1.jsonl`); **B** 1-2 + mrs.desc
(`parts/ch2.jsonl`, `parts/mrs_desc.jsonl`); **C** 1-3 + grs.desc (`parts/ch3.jsonl`, `parts/grs_desc.jsonl`);
**D** 1-4, 1-5, 1-6, 1-7 (`parts/ch4-7.jsonl`). The chapter dump filter is the middle number of the key:
`--chapters 0,1,255` for A, `--chapters 2` for B, and so on. Shared lines (inn, shop, "快走吧。", the key
choices, "没有该物品") appear in A's or B's dump first; others get them copied.

## Text rules

- Plain ASCII only: no curly quotes, accents, em dashes or ellipsis characters. Use `...` for `……` / `…………` /
  `......`, `-` or ` - ` for dashes, `"` or `'` for quotes (the source's `“十字之门”` / `‘地面’` become `"..."`),
  `~` for `～` ("Ohhh~", "Tomorrow~~~!!!").
- Dialogue `say` rows: write natural English; the fitter wraps it into the box (3 rows a page, narrower beside a
  portrait) and pages it. More than 3 pages draws a warning: tighten if you can. `\n` forces a new row and `\f` a
  new page; use them only where the layout needs it.
- **Who is speaking**: `pic` is a portrait. **pic=1 is Delat, pic=2 is Eluna, always.** pic=0 is anyone else
  (the NPC spoken to, a boss, a guard, the temple keeper, Reiter, Heath, Leoz, a Guardian). There are no speaker
  tags except `翼王：` (1-0-7): write it "Yiwang: ...". Do not add tags. Check the .gut when unsure.
- Brackets in dialogue are inner thoughts or stage business: keep them in brackets, ASCII `( )`. "（可是这是我的家耶...）"
  -> "(But this is my own house... why am I sneaking into it...)".
- `choice` rows (`@addr.1` / `.2`): at most 19 characters, no line breaks. Defaults: 是 / 否 "Yes" / "No", 好 / 不好
  "Sure" / "No thanks", 换 / 不换 "Trade" / "Don't trade", 有 / 没有 "I have" / "I don't", 要 / 不要 "Yes please" /
  "No thanks", 是 / 不是 "Yes" / "No", 确定 / 取消 "OK" / "Cancel", 使用钥匙 "Use Key", 使用白钥匙 "Use White Key",
  使用黑钥匙 "Use Black Key", 嵌入星光石 "Set Starstone", 嵌入零件 "Fit Cogwheel", 制作物品 / 提炼光之石 "Craft item" /
  "Refine lightstone", 普通 / 特别 "Normal" / "Special", 战技封锁 / 复活术 "Skill Lock" / "Revive", 怒雷击 / 耀击
  "Thunderclap" / "Dazzle".
- `menu` rows: same number of space-separated items as the Chinese, **no spaces inside an item**; glossary forms,
  hyphens otherwise, items up to 11 characters. The five menus are given in glossary.md (Menus); the X=/Y= menus
  are copied unchanged.
- `message` rows: a centred box of at most 4 rows of 140 px (about 25 characters a row); `check.py` errors past 4.
  Long ones to watch: the two Moon of Vengeance explanations (1-3-1), the engine-bug notice (1-1-1), the crafting
  recipe lines (1-1-14), the armoured man's description (1-6-1). Item gains: "获得金币: 1000" -> "Got 1000 Gold."
  Recipe lines: `"'Glimstone' x2"`, `"'Hematite' x20  'Glimstone' x2  'Glowwood' x5"`; the Rune Boots line uses
  the code's amounts (glossary Decision 12).
- `showgut` (the prologue scroll 1-1-1, the credits 1-7-10) scrolls in 20-column rows; `\n` may break lines. The
  prologue starts "序：" padded to the row end: write "Prologue:\n" and drop the padding. Credits: "STAFF:\nArt:
  Yiwang\nStory: Yiwang\nDesign: Yiwang\nSetting: Yiwang\nProduction: Yiwang".
- Item / skill descriptions (`grs.desc`, `mrs.desc`): at most 3 rows of 108 px (about 18-20 characters a row;
  `check.py` measures it). Stat lines: 防御力提高12，灵巧提高4 -> "DEF+12 DEX+4"; 减少 -> minus ("HP-20"); 魔法值 MP,
  生命值 HP, 攻击力 ATK, 敏捷 / 敏 / 速 AGI, 精神 SPI, 灵巧 DEX; 每回合回复生命值20 "HP+20 each turn"; 晕眩免疫 "Stn
  immune", 咒封免疫 "Sil immune", 混乱免疫 "Cnf immune", 全免疫 "Immune to all ailments", 毒x3 "Inflicts Psn",
  群攻击力 "Hits all enemies"; 单体生命值回复180 "Restores 180 HP to one". Skills: 单体 / 群体攻击技能 "Attacks one
  / all enemies", 基本伤害180 "base dmg 180", 有机会造成敌人攻击降低50%，效果持续3回合 "may cut ATK 50% for 3 turns",
  全体 "all allies". 纯度很低的光之石 "Lightstone of very low purity." 不详 "Unknown." Drop the trailing `\x0d\x0a`.
- Field-skill prompts (GRS 6-14-2/3/4/17 desc and 1-255-2/3/4/17): "Press SEARCH to use this item." (INSERT,
  MODIFY, DEL), the key names in capitals as the emulator labels them.
- Numbers and money: Gold ("100 Gold", "5000 Gold", 5000块 / 5000钱块 too). Chinese numerals as digits or words,
  whichever reads better ("sixty books", "16,000").
- Names in running text follow the glossary; one spelling everywhere (Delat, Eluna, Luna, Locke Reiter, Heath,
  Leoz, Kabras, Okaros, Snowblade, Silverleaf, Nightstar, the Forgotten City, St. Melo Keep, the Cross Entry, the
  Moon of Vengeance, the Magic Institute, lightstone, Sunstone, Blazestone, Crest).
- Fix obvious source typos quietly (list in glossary.md); drop the stray GBK bytes (`\xa1`, `\xbb`, `\xce`: see the
  table for what they stood for).

## Register

Light fantasy comedy with a sad, sincere core, written by one teenager for players his age. Plain modern English,
contractions, short punchy lines, no faux-archaic fantasy diction (the Guardians may be a touch formal). The
engine is the couple's bickering: keep the timing (one-word comebacks, "..." silences, ellipses as beats), the
slapstick narration and the emoticons (`-_-~~`, `=_=!`). Voices:

- **Eluna** (pic=2): bossy, impatient, cheerful, physical; commands ("Move it!", "Explain."), stretched shouts
  ("Tomorrow~~~!!!"), calls Delat "idiot". Kind and sharp with Heath, raw in 1-2-4 @09db and at the gate.
- **Delat** (pic=1): whiny, dry, sarcastic, sensible, always overruled; "Good grief..." (天......), bracketed
  grumbles; a prince who sounds like an ordinary teen. Hurt and evasive about his father, firm about the throne.
- **The temple keeper**: grumbling "If I'd known..." every time, never finished.
- **Reiter**: curt and theatrical, then grave. **Heath**: cheeky kid, then a sad, apologetic one. **The doctor**:
  few, quiet words. **Leoz**: gruff, bitter, proud. **Guardians**: measured challengers; the last one gentle and
  nostalgic; the black-winged child mocking, then tired.
- **Townsfolk**: plain; the philosophers deadpan; the 1-4-11 teacher keeps his English words in capitals (HEY!
  GOOD! OK! OH!).
- **Yiwang**: "Damn it, I was lurking down here!" (TMD = "damn it"; 潜水 = forum lurking).

Quotations: Genesis 1 (1-1-5) in the King James Version, line by line; 我思故我在 "I think, therefore I am".
Sound words: 呵啊 = a yawn or a gasp ("Haaah..."), 噫 "Huh?", 哇 "Waah!", 哼 "Hmph", 呼 "Phew".
