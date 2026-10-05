# 侠客行 (xkx): translator brief

Read before translating: `docs/xkx/glossary.md` (conventions and decisions), `docs/xkx/glossary.jsonl` (every
name and term), `docs/xkx/story.md` (plot, characters, voices, systems, **the quote tables**). For wuxia terms the
model is 金庸群侠传 (`docs/jy/`); for the text rules, 十字之门 (`docs/szzm/translating.md`).

## Workflow

```sh
python3 tools/tl/dump.py --game xkx --chapters 20               # rows to translate, story order, with context
python3 tools/tl/dump.py --game xkx --keys 1-4-1,1-4-2          # only these scripts
python3 tools/tl/dump.py --game xkx --kinds grs.desc,mrs.desc
python3 tools/tl/check.py --game xkx translations/xkx/parts/p1_story.jsonl
python3 tools/tl/build_en.py --game xkx                         # merge all parts, build the English .gam
```

A part file is JSON lines `{"id": "...", "en": "..."}`, one per row, in `translations/xkx/parts/`. `check.py` must
report no ERROR lines; read the warnings (glossary misses, long dialogue) and fix the real ones. All 842 name rows
(items, skills, ARS, maps, scene banners) are already filled by `parts/auto.jsonl` from the glossary (rerun
`python3 tools/tl/autofill.py --game xkx` after a glossary change); the engine strings are in
`parts/engine.jsonl`. Do not put name rows in your part. Glossary warnings for generic words are expected; the
`role` category (少侠, 师傅, 父亲...) is exempt on purpose.

`dump.py` lists each line once: a row whose kind and Chinese text repeat an earlier row anywhere in the game is
left out, and `build_en.py` copies the first one's English to it. Translate repeats yourself (dump `--all`) only
when the context needs different English; your row then wins. The full listings are in `work/xkx_gut/<key>.gut`
(key `1-4-3` for `gut/1-4-3@...` rows): read them for who speaks, what triggers a line, what a choice leads to.

### Script groups

| group | content | unique hanzi (dump) |
|---|---|---|
| 1-0 | intro scroll, credits x3, old-age death, status menu (allocation, Renown, age, Sect Points), second menu (teleport, sect, mode, ringtones), INSERT repair | 1540 |
| 1-1 | boot note; the five regions' streets (1-1-2 Central, 1-1-4 North, 1-1-5 South, 1-1-6 West, 1-1-7 East), the Nameless Elder (1-1-3), Japan Island (1-1-8), Hua Manor and the betrayal (1-1-9/10), Martial Tournament (1-1-97), rewards (1-1-98) | 4002 |
| 1-2 | Central Plains houses: errands, BBK's Zhang Zhanqing | 1711 |
| 1-3 | shops: pawnshop, inn, mall, pharmacy, Martial Hall, Fun City, regional merchants, Big Rabbit, Japan merchant | 2145 |
| 1-4 | the five sect halls (copies: 1-4-1..5), Matchmaker, Sect Hall, Net Cafe | 5764 (1-4-1..5 = 5239) |
| 1-5 | dungeons: pagoda bandits, Rock Hill, Bloom Maze (Bigeye), Well Bottom (Water Beast) | 985 |
| 1-6 | North houses (SSK, the Wushan Two, the Old Granny and marriage, Haunted House, Bandit Den) | 2211 |
| 1-7 | South houses (Xiaobao's secret, Blight's Den) | 1200 |
| 1-8 | West houses (Big Rabbit's mother, TAD) | 708 |
| 1-9 | East houses (Dugu Zheng, Tipsy Sword) | 1248 |
| 1-10 | Flybug's tunnel | 138 |
| 1-20 | Worryfree Village: New Game, father's illness, the studio room, the Sword Saint, the well | 1917 |
| 1-30 | Japan Island houses and the consulate | 673 |
| 1-40 | the four mazes and the finale | 229 |
| 1-50 | teleport menus | 254 |
| 1-100 | training maze (Coming-of-Age) | 197 |
| 1-255 | item scripts, Mother's letter, Father's note, Big Rabbit's letter | 766 |
| grs.desc / mrs.desc | item and skill descriptions | 5106 / 1488 |

Total 32,282 unique hanzi (about 46,000 with repeats).

### Parallel split (five parts, about 6,500 unique hanzi each)

| part | file | content | hanzi / rows |
|---|---|---|---|
| **A** story | `parts/p1_story.jsonl` | 1-20, 1-0, 1-40, 1-100, 1-255, 1-10, 1-50, 1-30, and the main-plot scripts of group 1 (1-1-1, 1-1-9, 1-1-10, 1-1-97, 1-1-98) | 6555 / 415 |
| **B** Central | `parts/p2_central.jsonl` | the region streets 1-1-2..1-1-8, group 2 (Central houses), the shops of group 3 except the pharmacy and Martial Hall | 6282 / 502 |
| **C** sects | `parts/p3_sects.jsonl` | group 4 (sect halls, Matchmaker, Sect Hall, Net Cafe) + 1-3-4 pharmacy and 1-3-5 Martial Hall | 6499 / 294 |
| **D** items | `parts/p4_items.jsonl` | grs.desc (all item descriptions) + group 5 (dungeons) | 6091 / 317 |
| **E** regions | `parts/p5_regions.jsonl` | groups 6, 7, 8, 9 (North, South, West, East houses) + mrs.desc (skill descriptions) | 6855 / 398 |

Exact dump commands:

```sh
# A
python3 tools/tl/dump.py --game xkx --chapters 0,10,20,30,40,50,100,255
python3 tools/tl/dump.py --game xkx --keys 1-1-1,1-1-9,1-1-10,1-1-97,1-1-98
# B
python3 tools/tl/dump.py --game xkx --keys 1-1-2,1-1-3,1-1-4,1-1-5,1-1-6,1-1-7,1-1-8,1-3-1,1-3-2,1-3-3,1-3-6,1-3-7,1-3-8,1-3-9,1-3-10,1-3-11
python3 tools/tl/dump.py --game xkx --chapters 2
# C
python3 tools/tl/dump.py --game xkx --chapters 4
python3 tools/tl/dump.py --game xkx --keys 1-3-4,1-3-5
# D
python3 tools/tl/dump.py --game xkx --kinds grs.desc
python3 tools/tl/dump.py --game xkx --chapters 5
# E
python3 tools/tl/dump.py --game xkx --chapters 6,7,8,9
python3 tools/tl/dump.py --game xkx --kinds mrs.desc
```

Together they cover every script and description row exactly once (`--keys` and `--chapters` both include the
two `timemsg` rows of 1-3-5). Shared lines show up in the part whose script comes first in the file (1-0, 1-1, 1-2 ... 1-255,
then the descriptions); the others get them copied. Lines shared across parts that must read the same:
- the **Top Ten notice exchange** ("HELLO, are you X?" / "Mm, that's me. What's up?" / "Wow, really? That's
  great, thanks." / "I know, thanks for telling me.") is in B (1-1-2 Paladin / solfen, 1-1-4 Flybug), A has none,
  E has SSK, Chengxin Electric, Chunlan Guardian, andygzq, Flooder, Xiyu, King of Comedy: **E copies B's wording**;
- the **system lines** ("System: You got killed. GAME OVER!", "System: You got N Essence Points.", "System:
  You're a year older.") first appear in B; A and E match them;
- the **sect masters' lines** (C) are five copies: translate 1-4-1 first, then make 1-4-2..5 identical apart from
  the name and the sect; the sect task "deliver a letter to Yi Tianchou" must match E's 1-7-1, and "Peace Cake" /
  "candied haws" (Sugar Haws) / "pet egg" the item names.

## Text rules

- Plain ASCII only: no curly quotes, accents, em dashes or ellipsis characters. Use `...` for `……` / `。。。` /
  `......`, `-` or ` - ` for `――` / `--` / `―`, `"` or `'` for `“”` / `‘’` / `《》` around names (《一天仇》 is just
  "Yi Tianchou"; 《名菡秘籍》 = "the Minghan Manual", no marks needed), `~` for `～` / `~~` ("Bye~", "Ha ha~").
  `★` stars in the reward box and Big Rabbit's signature become `*`.
- **Speaker tags**: keep every tag the source has, as `Name: text` with an ASCII colon and one space, glossary
  names: "Sword Saint: ...", "Doctor Wan: ...", "Mother: ...", "System: ...", "Girl: ..." (MM), "Bandit A: ..."
  (强盗甲), "Old Codger, Codger Old: Kill!". **pic=1 is always Mo Ming and has no tag**; never add tags. 莫名心想：
  = "Mo Ming thinks: ...". The tags count toward the box: keep the line short.
- Dialogue `say` rows: write natural English; the fitter wraps it into the box (3 rows a page) and pages it. More
  than 3 pages draws a warning: tighten if you can. `\n` forces a row, `\f` a page; only where layout needs it.
  The long ones to watch: Hua Yingxiong's confession (1-1-10@095a), the Sword Saint's array speech (1-20-3@0423),
  Zhang Zhanqing's Top Ten list (1-2-4@0364), the Water Beast lore (1-5-5@02d9), Dugu Zheng's story
  (1-9-2@0280), Xiaobao's secret (1-7-4@0404), the pharmacy owner (1-3-4@0346).
- Brackets in dialogue are asides: keep them, ASCII `( )`. "（汗。。。打我钱的如意）好吧！" -> "(Sweat... he's after my
  money) Fine!".
- The source's own English stays in its capitals and wording, fitted into the sentence: "HELLO, are you SSK?",
  "OK, WAIT A MINUTE!", "THANK YOU!", "ARE YOU ZHAOSI?" / "I'M? WHO ARE YOU?", "WHAT ARE YOU WANT TO DO?" (keep
  the broken English: it's the joke), "NO WHY!", "GO GO GO GO". Keyboard mashes and gibberish stay ASCII
  (`~!@#$%^&*`, `#$*#...`, `%#-%$*-`).
- `choice` rows (`@addr.1` / `.2`): at most 19 characters, no line breaks. Defaults: 是 / 否 / 不 "Yes" / "No", 给 /
  不给 "Pay" / "Don't pay", 买 / 不买 "Buy" / "Don't buy", 去 / 不去 "Go" / "Don't go", 加入 / 不加入 "Join" /
  "Don't join", 学习 / 不学 "Learn" / "Don't learn", 帮 / 帮忙 / 不帮 "Help" / "Don't help", 打 "Fight", 救 / 不救
  "Save him" / "Don't save him", 确定 "Confirm", 有 / 没有 "I do" / "I don't", 查看 / 战斗 "Look" / "Fight", 抢劫
  "Rob", 住店 "Stay the night", 打听消息 "Ask for news", 使用 / 不用 "Use" / "Don't use", 我换 / 不换 "Trade" / "No
  trade", 挂机 / 不挂 "AFK train" / "Don't", 多一事不如少一事 "Stay out of it", 虚是虚，实是实 (the right answer
  to the servant's riddle) "Fake=fake,real=real" (19), 帮他报仇 "Avenge him".
- `menu` rows: same number of space-separated items as the Chinese, **no spaces inside an item**; glossary forms,
  hyphens otherwise. The status menus: `分配精元点 查看声望 查看年龄 查看师门点 查看小地图` = `Allot-points Renown
  Age Sect-points Minimap`; `攻击力 防御力 身法 灵力 幸运 生命上限 真气上限` = `Attack Defense Agility Spirit Luck Max-HP
  Max-MP`; `传送 管理门派 切换游戏模式 播放音乐` = `Teleport Manage-sect Switch-mode Play-music`; regions `北部 南部 中原
  西部 东部` = `North South Central West East`; ringtones `铃声1 ... 停止播放` = `Ring1 ... Ring11 Stop`; the sect task
  menu `找点事做 完成任务 放弃任务 学习技能 灭门派` = `Find-work Turn-in Give-up Learn-skill Destroy-sect`; skill
  levels `5级技能` = `Lv5`..`Lv60`; `精元点 师门点 剧情点 声望值` = `Essence Sect-points Story-points Renown`; the
  pharmacy `Life-Joss Poison Repel-Joss Lure-Joss`; the Net Cafe `BBK-Forum BBK-Fan-Club Other-sites`; the
  teleport house lists (1-50-x) use each house's short map form, e.g. `Xiaoxue's Code-Nut's Elder's Charmer's
  Ah-Xiu's Jay-Fan's SSK's Wushan-Den Shopaholic Granny's Old-Wu's Haunted Bandit-Den`.
- `message` rows: a centred box of at most 4 rows of 140 px (about 25 characters a row); `check.py` errors past 4.
  "携带装备：X" = "Carrying: X" (glossary item name). The reward box 1-4-8@057c: "*** Level +30 ** Essence +200 **
  Sect Points +200 ***". Father's note (1-255-40): "Destroy the five sects\nClimb Bright Peak\nTake the Minghan
  Manual\n - Father".
- `showgut` (scrolls: the intro, credits, the five sect descriptions, the letters) scroll in 20-column rows; `\n`
  may break lines; drop the source's space padding. Intro: "Prologue:\n" then the text. Credits: one item per row,
  e.g. "== Game Engine ==\nNightbug\nSouthern Imp\n== Dev Team ==\nChunlan Studio\nPlanning:\nChunlan Guardian\nMaps:\nSSK\nScript:\nChunlan Guardian\nThanks to:\nNightbug\nGame King\nYe Lingling\nTesters:\nLeng Yi\nZF\n315200242\n...and many\nnetizens\nChunlan Studio\nJune 17, 2005". The letters start
  "Mo Ming,\n" (莫名：) and "Mother,\n" (母亲：).
- Item / skill descriptions (`grs.desc`, `mrs.desc`): at most 3 rows of 108 px (about 18-20 characters a row;
  `check.py` measures it). Keep the flavour joke if it fits, else the stats win. Stat lines: 防御+3 "DEF+3", 攻击 /
  攻 / 武术 ATK, 身法 AGI, 灵力 / 灵 / 灵气 SPI, 吉运 LUK, 真气上限 "MaxMP", 生命上限 "MaxHP", 真气 MP, hp / 生命 HP,
  减 / - "-"; 避毒 / 避乱 / 避眠 / 避封 / 避咒封 "Psn/Cnf/Slp/Sil immune" (several: "immune Psn Cnf"); 避免一切负面影响
  "immune to all ailments"; 可能产生N回合混乱 "may Cnf N turns" (中毒 Psn, 咒封 / 封咒 Sil, 昏睡 / 晕倒 Slp); 伤敌150
  "150 dmg"; 敌方全体 / 全体 "all enemies", 我方全体 "all allies"; 每回合恢复真气10 "MP+10 each turn"; HpMp+45
  "HP/MP+45"; 恢复15% "restores 15% HP". The 传奇中的... descriptions = "from Legend of Mir". The Waiyutong /
  4980 / 5980 / 6980 descriptions are BBK ad copy: "128MB flash, plays MP3s - recommended!".
- Numbers and money: "100 yuan", "8888 yuan", "100 RMB", "10,000 yen"; 1W = 10,000, 5W = 50,000; Chinese numerals
  as digits ("You're 23.", "80-something Sect Points"). Ages: "你的年龄是:四十多岁" = "Your age: forties".
- Names in running text follow the glossary, one spelling everywhere (Mo Ming, Mo Jingchou, Hua Yingxiong, the
  Sword Saint, Doctor Wan, Chunlan Guardian, Nightbug, Flybug, SSK, Bigeye, Green Blight, Worryfree Village, Bright
  Peak, the Central Plains, the Minghan Manual, the Dictionary Array, the Bagua Array, Sky Thunder, Martial Lord,
  Essence Points).
- Fix obvious source typos quietly (glossary.md lists them); drop the stray GBK bytes (`\xa3`).

## Register

A cheeky 2005 teenage fan game. Plain, quick modern English, contractions, short lines; light wuxia colour from
the glossary terms, never faux-archaic. Keep the net-slang energy with English equivalents (glossary Register:
汗 "(sweat)" / "Sheesh", 靠 "Damn", TMD "damn", 555 "Waaah", 嘎嘎 "Heh heh", 晕 "Ugh", 9494 "Yeah, yeah!", 88 "Bye!"),
the fourth-wall jokes about Chunlan Guardian and "Xiake", the profanity at its own level (操 "Damn it" / "Hell",
狗日的 "son of a dog", TMMD "goddamn"), and the jingoism of the Japan scenes as written (Decision 10). Voices:

- **Mo Ming**: cocky, playful, quick comebacks ("Whatever, you're trash!"), English words in capitals, soft with
  children and the sick; stunned and hurt by his father.
- **Sect masters**: gruff stock masters ("Oh? Not bad, kid...", "Get lost!", "Go go go!").
- **System**: brisk instructions with attitude.
- **Chunlan Guardian**: the author mugging for the player.
- **Sword Saint / Hua Yingxiong**: older, weary, a little formal; their sighs as "..." and "Sigh...".
- **Mottos** (see story.md, Quotes): the identified quotations in their given English; the rest as clean,
  quotable aphorisms. One motto = one tidy line, not a paraphrase with commentary.
