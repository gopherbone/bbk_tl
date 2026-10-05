# 三国霸业 (Three Kingdoms: Hegemony): translator brief

三国霸业 is BBK's 2005 turn-based Three Kingdoms strategy game: pick one of four periods
(董卓弄权, 曹操崛起, 赤壁之战, 三足鼎立) and a ruler, then run
cities month by month (domestic affairs, diplomacy, military) and fight
tactical battles on a hex-like grid. The whole text is 740 rows (about 3,300
hanzi): UI labels, menus, city/order messages, short speeches by officers,
battle messages, skill and item names and descriptions, and 295 officer names.

Source: `translations/sgby/strings.jsonl` (exported by `tools/sgby/export.py`).
Each row has `id`, `zh`, `bytes` (original length), `kind`, and either
`budget` (single line, pixels) or `box` ([width px, lines], word-wrapped), and
for engine strings the C macro name and `usage` lines from the iBaye port of
the original source (`refs/iBaye/src/*.c`, which you may read for context).

Output: `translations/sgby/en.jsonl`, the same rows with an `"en"` field.
`python3 tools/sgby/check.py` must report 0 problems.

```sh
python3 tools/sgby/check.py                          # all rows
python3 tools/sgby/check.py --width "Cavalry"         # pixel width of a string
python3 tools/sgby/check.py --wrap 90 "Some speech"   # how the renderer wraps it
```

## How text is drawn

A proportional font (about 4.7 px per character on average; `i`/`l` 2-3 px,
`m`/`w` 8 px) on a 159x96 one-bit screen, 12 px per line. Text wraps at word
boundaries inside its box. The pixel limits are hard: anything over is
clipped or collides with the next column.

- `speech` (box 90x3): an officer speaks in a box beside his portrait. Three
  lines of 90 px is about 50 characters. Keep it punchy; cut padding words,
  never meaning.
- `msg`, `desc` (box 148xN): message boxes and item/skill descriptions.
- `menu`: one menu item (12 px per original byte; a two-hanzi item gets 46 px,
  about 8-9 characters). Items in one menu should be parallel in form.
- `label`: single-line labels and fragments that the game glues together
  with numbers or names (see below). 6 px per original byte.
- `name`: officer names, 48 px. `city`: city names, 36 px.

## Fragments and format strings

Many rows are pieces the game concatenates. Read `usage` (and the source) to
see the assembly, and keep the leading/trailing spaces the assembly needs:

- `s/99` `城中找到 ` + item name; `s/102` `城中找到金钱 ` + number;
  `s/113`..`s/118` `<city>` + ` 农业开发度变为 ` + value + ` (+` + delta + `)。`.
- `s/104` `军 vs ` and `s/105` `军`: `<ruler>军 vs <ruler>军` (the "army of"
  around ruler names): English like `<ruler> vs <ruler>` may need the
  fragments to become empty-ish; an empty translation is not allowed, use a
  single space " " where a fragment should vanish.
- `e/13` is the battle help panel with `|`-separated cells and `%` value
  slots; keep every `|` and `%` in place, and each cell's label short (it is a
  fixed grid: about 6 px per original byte per cell).
- `e/48` `第    天` ("day ____"): the spaces are where the number is drawn;
  keep a gap of the same width (`Day    `).
- `s/65` `              年` is a year field: keep the leading spaces count
  and put the unit (or nothing, `" "`) at the end.
- Keep `%d`/`%s` specifiers exactly (check.py compares them).
- `保留序号` ("reserved") rows are unused; translate as `Reserved`.
- `sango .sav` is a file name: keep it unchanged.

## Names and terms

- Officers: standard Hanyu Pinyin, family name first, two words, no tones:
  曹操 Cao Cao, 诸葛亮 Zhuge Liang, 司马懿 Sima Yi, 夏侯惇 Xiahou Dun, 公孙瓒
  Gongsun Zan. Compound surnames (诸葛, 司马, 夏侯, 公孙, 太史, 皇甫, 欧阳, 上官,
  令狐, 淳于) stay one word. Watch for heteronyms: 单 Shan, 曾 Zeng, 乐进 Yue
  Jin, 吕布 Lü -> `Lu Bu` (ASCII), 阚泽 Kan Ze, 鲁肃 Lu Su, 阎圃 Yan Pu.
  If a name is over 48 px, report it in your summary (do not abbreviate).
- Cities: pinyin, one word where conventional (长安 Chang'an -> `Chang'an`,
  洛阳 Luoyang, 建业 Jianye, 成都 Chengdu, 襄阳 Xiangyang, 西凉 Xiliang). Use
  the apostrophe only where needed for syllable breaks.
- Troop types: 骑兵 Cavalry, 步兵 Infantry, 弓兵 Archers, 水军/水兵 Navy,
  极兵 Elite, 玄兵 Mystic (these are BBK inventions; 极兵/玄兵 are the
  super-units).
- Stats: 武力 STR (War), 智力 INT, 忠诚 Loyalty, 体力 Stamina (HP-like for
  officers), 兵力 Troops, 等级 Level, 经验 EXP, 技力 SP (skill points),
  攻击 ATK, 防御 DEF, 移动 Move. City: 农业 Farming, 商业 Commerce, 民忠 Morale,
  防灾 Disaster prevention (label: `Relief`), 人口 Population, 金钱 Gold,
  粮食 Food, 后备兵力 Reserves. Be consistent: the same term everywhere.
- Ranks/status: 君主 Ruler, 太守 Governor, 在野 Free (unaffiliated officer),
  俘虏 Captive, 归属 Faction, 所在城市 Location.
- Orders (menus): 内政 Domestic, 外交 Diplomacy, 军备 Military, 状况 Status;
  开垦 Farm, 招商 Trade, 搜寻 Search, 治理 Govern, 出巡 Patrol, 招降 Recruit,
  处斩 Execute, 流放 Exile, 赏赐 Reward, 没收 Confiscate, 交易 Trade (market:
  choose distinct words, e.g. 招商 Commerce vs 交易 Market), 宴请 Banquet,
  输送 Transport, 移动 Move; 离间 Sow Discord, 招揽 Recruit (diplomatic hire:
  pick distinct wording from 招降), 策反 Incite, 反间 Counter-spy, 劝降 Demand
  Surrender; 侦察 Scout, 征兵 Conscript, 分配 Assign, 掠夺 Plunder, 出征 Attack.
  Pick final forms that fit 46 px and are distinct within each menu.
- Battle: 攻击 Attack, 计谋 Tactic, 查看 View/Look, 待机 Wait; 回合结束 End Turn,
  全军撤退 Retreat, 战斗动画 Animation, 移动速度 Move Speed, 敌军移动 Enemy Moves.
- Skills (`skill/*`, 2 hanzi each): short punchy names (践踏 Trample, 火攻 Fire
  Attack -> `Fire`, 落石 Rockslide, 箭雨 Arrow Rain, 奇门遁甲 parts...). The
  `skilldesc` rows explain them.
- Items: famous weapons/books/horses by their usual English: 方天画戟 Sky
  Piercer (halberd), 青龙刀 Green Dragon Blade, 孙子兵法 Art of War, 赤兔 Red
  Hare, 的卢 Dilu, 绝影 Jueying, 爪黄飞电 Flying Lightning... `item` budget is
  6 px per byte.

## Register

Brisk, modern, a little classical flavour in the speeches (officers address
the ruler as "my lord"). No archaisms ("thee"), no slang. Plain ASCII only:
`...` for `……`, straight quotes, no em dashes. Exclamations as in the source.

## Deliverables

1. `translations/sgby/en.jsonl` with every row translated and check.py clean.
2. `docs/sgby/glossary.md`: the term decisions (stats, orders, troop types,
   ranks), plus any names or terms you had to compromise on.
3. A short summary: rows that could not reach their budget (if any), names
   over 48 px, and judgement calls worth a second look.
