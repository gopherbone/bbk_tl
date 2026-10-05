# 十字之门 (Cross Entry) English glossary

Status: **decisions made** (no open questions block translation; the reviewer can override any row).
Machine-readable source: `docs/szzm/glossary.jsonl` (one term per line: `zh`, `en`, `category`, `count`,
optional `alt` / `short`, `note`, `source_ids`). This page summarises the same data. Story background:
`docs/szzm/story.md`; translator brief: `docs/szzm/translating.md`.

- `count` = how often the zh string occurs as a substring across `work/szzm.strings.jsonl` (all kinds; for the
  ASCII placeholder labels, the number of rows with exactly that name). Short terms over-count, so read it as
  "how common".
- Field limits (from `tools/tl/common.py problems()`): item names (grs.name) <= 10 chars, ARS names <= 11, skill
  names (mrs.name) <= 11, map names <= 12, scene banners (setscenename) <= 10, choices <= 19, menus = the same
  number of space-separated items as the Chinese, no spaces inside an item. `en` fits every name field the term is
  used in; `short` exists only where `en` is wanted in dialogue but is over a name field (剑士工会 "Swordsmen's
  Guild" / banner "Guild Hall"; 遗忘之城 "Forgotten City" / map "Forgotten"; 夜星城外 / 雪刃城外 "Nightstar Wilds" /
  "Snowblade Wilds" / maps "Star Wilds" / "Blade Wilds"). `tools/tl/autofill.py` uses `short` where `en` breaks a
  row's limit.
- All `en` / `alt` / `short` values are plain ASCII.
- Validation: every grs.name / mrs.name / ars.name / map.name / setscenename row (357 rows: 121 items, 28 skills,
  144 ARS, 55 maps, 9 banners) has a term that fits its limit. `autofill.py` writes all 357 to
  `translations/szzm/parts/auto.jsonl`; `check.py` reports 0 errors and 8 expected warnings (a `short` form in a
  map/banner row, or a substring hit such as 短剑 inside 魔纹短剑 "Runed Dirk"). `build_en.py --game szzm`
  builds.
- 392 terms: 261 real terms plus 131 ASCII placeholder labels kept as they are (see the end of this page).

## What kind of game this is

A one-person hobby RPG on the BBKRPG engine (伏魔记's Ver1.3 build) by **翼王 (Yiwang)**, credited for art, story,
design, setting and production (1-7-10). Western fantasy with a short, tight plot and a lot of banter: a bossy
foundling swordswoman, **Eluna**, drags the put-upon crown prince, **Delat**, across the underground kingdom of
**Okaros** to collect four magic keys for the legendary **Cross Entry**, the gate back to the surface humans were
banished from 2000 years ago. On the way they uncover that Delat's father seized the throne by murder (the rebel
**Moon of Vengeance** is led by Delat's uncle **Leoz**), and at the gate they learn the surface is a dead
wasteland. Eluna decides to fix it anyway; the epilogue (Year 6 of the Cross Era) has all of Okaros replanting the
surface. Tone: light romantic comedy (slapstick, Eluna's threats, Delat's bracketed grumbling, emoticons like
`-_-~~` and `=_=!`) with sincere sad beats (Heath's last day, the massacre, the dead surface). Little net slang
(one TMD, one 潜水 joke); no fourth-wall humour except the author's cameo and the engine-bug notice. See
`docs/szzm/story.md`.

## Conventions

**Names.** The game invents Western-fantasy names in Chinese transliteration. Render them as plausible Western
names, never pinyin, one spelling everywhere: 德拉特 **Delat**, 艾露娜 **Eluna** (Delat's pet name 小娜 **Luna**),
洛克斯・雷特 **Locke Reiter** (雷特 alone = Reiter; the ・ is a separator), 希瑟 **Heath** (a boy, so not
"Heather"), 莱奥兹 **Leoz**, 奥卡洛斯 **Okaros**, 卡布拉斯 **Kabras**, 圣梅洛堡 **St. Melo Keep**, 多罗维尔综合症
**Dorowell Syndrome**. The K spelling (Kabras, Okaros) is deliberate: they read as one world. The author's handle
翼王 stays pinyin, **Yiwang** (a handle, like yxts's Xiaoyao). The King, the temple keeper, the doctor and the
Guardians have no names.

**Places.** Chinese-meaning city names are translated (雪刃城 **Snowblade**, 银叶城 **Silverleaf**, 夜星城
**Nightstar**, 遗忘之城 / 被遗忘之城 **the Forgotten City**); add "City" only where a line needs it. 城外 =
"outside the city" in dialogue, **Outskirts** on the banner; X城外 maps = "X Wilds" (short "Star Wilds",
"Blade Wilds"). Generic map names: Indoors, Library, Corridor, Hall, Shop, Inn, Workshop, Temple, Sewers, Stairs,
Maze, Wilds, Tunnel, Graveyard, Mine, Institute. 未命名 (the author's placeholder on the two ending maps) =
"Unnamed". Map 2-2-15's name is four spaces: kept blank.

**The gate.** 十字之门 = **the Cross Entry** (the title; the boot logo says "CrossEntry"). Never "Cross Gate".
"门" alone = "the gate" / "the door". 十字历 = the Cross Era (十字历六年 "Year 6 of the Cross Era").

**Institutions.** 复仇之月 = **the Moon of Vengeance** ("the Moon" on later mentions); 剑士工会 = the
Swordsmen's Guild (工会 is a typo for 公会); the six names of the Snowblade institute (魔法研究所, 魔法研究与控制所,
魔法控制研究协会, 魔法研究控制所, 魔法控制研究学会, 魔法研究协会) are all **the Magic Institute**; the palace has its
own ("the palace's Institute"). 行政处 = the city office. 神殿 = the Temple (Kabras Temple). 治安管理队 = the
Watch.

**Lightstone.** 光之石 = lightstone (lower case), graded by purity as the descriptions say: 碎光石 Shardstone (very
low) < 微光石 Glimstone (low) < 星光石 Starstone (fairly high) < 晨光石 Dawnstone (very high). 耀星石 **Blazestone**
is a specially refined stone that breaks the Eternal Darkness (永恒的黑暗). 太阳石 **Sunstone** is the ultimate
refinement, the stone in Eluna's bracelet and the weapon that killed the surface. 最纯的光之石 = "the purest
lightstone".

**Keys.** 钥匙 is both the plain Key item (White Key, Black Key, Odd Key) and, in the story, the four magic "keys"
to the Cross Entry. Those turn out to be the **Crests** (纹章I-IV = Crest I-IV). In dialogue they stay "keys"
("only three cities besides Kabras, so three keys?"); item names and the pillar messages say "Crest".

**Equipment.** 10 chars. Slot words that fit: Cap, Hat, Helm, Mail, Garb, Robe, Suit, Boots, Shoes, Mitts,
Gloves, Grip, Hand, Aegis, Ward, Rod, Staff. The four 骑士 "knight" pieces use real armour words (Great Helm, Plate
Mail, Sabatons, Gauntlets) because "Knight X" is over 10. 预言者 = Seer (Seer Hat, Seer Staff). 咒文 = Rune (Rune
Boots, Rune Mitts). Scroll items drop the word "Scroll" (Recovery, Revival, Homeward); skill scrolls are "Scroll
A".."Scroll L", fragments "Fragment A".."Fragment D". In dialogue: "a Homeward scroll", "a Recovery scroll".

**Skills.** The main menu says "Skill" (技能, engine row). MRS names are short spell/move names: Delat casts (Fire
Strike, Ice Rush, Whirlwind, Meteor, Life Drain, Thunderclap, Hailstorm, Mind Blast, Light Ward, Heal, Holy Light,
Revive), Eluna fights (Skill Lock, Dark Cut, Gale Slash, Red Lotus, Dazzle, Shade Slash, Venom Sting, Hot Blood,
Haste, First Aid, Pilfer). No script teaches Fire Strike or Shatter (starting / level-up skills). MRS 4-1-17..20 are placeholders "1"/"2", kept.

**Menus.** No spaces inside an item; one-word glossary forms, otherwise hyphens (never CamelCase); items up to 11
characters fit. The five menus:
- 1-1-14 crafting: `Seer-Hat Holy-Robe Rune-Boots Hope-Aegis Sure-Hand Key Scroll-L Cancel`
- 1-1-14 refining: `Glimstone Starstone Dawnstone Cancel` and `Glimstone Starstone Dawnstone Blazestone Cancel`
- 1-2-12 puzzle: `X=0 X=1 ... X=9` and `Y=0 ... Y=9`: copy unchanged.

**Forms of address.** Eluna and Delat use plain names. 大叔 = "Uncle" for the temple keeper who raised Eluna, and
"mister" for Leoz before the reveal ("Uncle Leoz" after). 大伯 = uncle (father's elder brother). 父王 = "Father" /
"my father"; 国王 = the King; 王子 = prince. 前史官(大人) = "the former Historian" / "Master Historian". 小姑娘 =
"little girl" (the guard; Eluna: "I'm not a little girl! I'm a Junior Swordsman!"). 小子 = "boy" / "kid" (Leoz to
Delat). 笨蛋 = "idiot" (Eluna to Delat, often).

**Register.** Light fantasy comedy with real feeling. Plain modern English, contractions, short lines; the
couple's bickering is the heart of the script. Keep the slapstick and the threats light ("Want me to cut you a few
times so you can see?"), keep the bracketed asides as asides in brackets, keep the emoticons in ASCII (`-_-~~`,
`=_=!`), keep `~` for drawn-out vowels ("Ohhh~"). The sad scenes (Heath, the evacuation figures, the dead surface,
Eluna's tears) are played straight, without jokes added. Real quotations use their standard English: the Genesis
1 passage read by a Kabras townsman (1-1-5) is the Chinese Union Version; use the **King James Version** of
Genesis 1:1-31 line for line ("In the beginning God created the heaven and the earth."). 我思故我在 = "I think,
therefore I am."

**UI and stats.** Engine strings are translated (`translations/szzm/parts/engine.jsonl`): HP, MP, Attack, Defense,
Agility, Spirit, Dexterity, Resist; ailments Psn / Cnf / Sil / Stn (毒 乱 封 晕); money "Gold". In descriptions:
防御力 DEF, 攻击力 ATK, 敏捷 / 敏 / 速 AGI, 精神 SPI, 灵巧 DEX, 生命值 HP, 魔法值 MP; 提高N = +N, 减少N = -N;
单体 / 群体 / 全体 = one / all enemies / all allies; 基本伤害 = base damage; 回合 = turns; 晕眩免疫 "Stn immune",
咒封免疫 "Sil immune", 混乱免疫 "Cnf immune", 全免疫 "immune to all ailments", 消除异常 "cures ailments", 毒x3
"inflicts Psn". Money: 金币 / 钱 / 块 = Gold ("100 Gold", "5000 Gold").

## Decisions

1. **Title**: 十字之门 = "Cross Entry" (games.py `title_en`), and the gate in the text is "the Cross Entry".
2. **Heroes**: 德拉特 Delat (prince, mage, actor 1, pic=1), 艾露娜 Eluna (swordswoman, actor 2, pic=2). Both fit the
   11-char ARS field. ARS 3-1-3 / 3-1-4 are duplicate records with the same names.
3. **Western names, not pinyin** (Conventions); Kabras / Okaros with K; Heath for the boy 希瑟.
4. **Mode names**: 普通 "Normal", 特别 "Special". Special (event 2008) raises the heroes' starting stats, swaps every
   enemy set for a tougher one, and unlocks eight extra teachers who refuse on Normal ("You're not on 'Special',
   huh? If you were, I could teach you something."). Not "Hard": NPCs quote the word.
5. **Moon of Vengeance** for 复仇之月 (not "Vengeful Moon" / "Revenge Moon"); "the Moon" for short.
6. **One name per institution**: the Magic Institute (six source variants), the Swordsmen's Guild.
7. **Crests** for 纹章 (items, pillar messages); "keys" in dialogue.
8. **Enemies have no names**: every monster ARS record is a placeholder (`d1`..`d41`, `x`, numbers, `c6`..`c25`,
   `a` `b` `c`), so battles show those labels. Kept as they are; there is nothing to translate.
9. **Placeholders are kept**: ARS NPC labels `1`..`22`, MRS `1` / `2`, the blank map name, 未命名 "Unnamed".
10. **The credits** (`STUFF:` showgut, 1-7-10): fix the author's typo to "STAFF:", then "Art: Yiwang", "Story:
    Yiwang", "Design: Yiwang", "Setting: Yiwang", "Production: Yiwang", one per 20-column row.
11. **Keys of the BBK keyboard** in the four field-skill messages: 查找 SEARCH, 插入 INSERT, 修改 MODIFY, 删除 DEL,
    in capitals as the emulator labels them ("Press SEARCH to use this item.").
12. **Recipe message fixed to the code**: 1-1-14 shows 咒文之靴 needing "磷木X10 赤铁矿X3 星光石X3" but the script
    takes Glowwood x3, Hematite x3, Starstone x10. Write "Glowwood x3  Hematite x3  Starstone x10".
13. **Typos are fixed silently** (table below); the deliberate pun on 道 (sewer "passage") is kept.
14. **US spelling**; ellipses "..." for every …… / 。。。 run.

## Inconsistencies and typos found in the source

| source | where | fix |
|---|---|---|
| `错\xce` | 1-0-6@021b | GBK cut of 错误: "Wrong!" (torch-order puzzle) |
| trailing `\xa1` | 1-2-3@01b7, 1-3-5@044c | half of a full-width ！/～: drop it |
| `用力地\xbb` | 1-3-1@0362 | cut of 晃: "waves a sheet of paper hard in front of them" |
| trailing `\x0d\x0a` | GRS 6-7-7, 6-14-3, 6-14-4, 6-14-17 desc | drop |
| `找到没？\"` | 1-1-1 | stray quote: drop |
| `还不快 走开？？` | 1-2-1 | stray space |
| 艾露 | 1-2-4 message | 艾露娜 Eluna |
| 剑士工会 | 1-1-10 banner, 1-1-1 | 公会 guild |
| 旨喻 | prologue | 旨谕 decree |
| 担误太时间 / 担搁 | 1-1-13 / 1-5-1 | 耽误太多时间 / 耽搁 |
| 提练 / 实验实 | 1-1-8 | 提炼 refine / 实验室 lab |
| 不想要做呢呢 | 1-1-8 | doubled 呢 |
| 象 | 1-1-13 | 像 |
| 那心啦 / 抢拖着 / 怎么有么多 | 1-2-5 | 放心啦 / 拖着 / 这么多 |
| 睡休息 | 1-2-1 | 休息 |
| 五秒种 / 就是定是 / 一遍荒芜 | 1-2-4 | 五秒钟 / 就一定是 / 一片荒芜 |
| 监护我 / 岂个人 / 利害 | 1-3-5 | 监护人 / 几个人 / 厉害 |
| 请匆打扰 | 1-3-4 | 请勿打扰 "Busy, do not disturb." |
| 能。 | 1-3-11 | 能力: "Let me see your strength." |
| 把我学东西 | 1-4-11 | 跟我学 |
| 5000钱块 | 1-3-17 | 5000块钱 "5000 Gold" |
| 一幅 / 那里发闷 | 1-6-1 | 一副 / "sulk there, then" |
| 用易 / 装原本 / 做卡布拉斯做官 / 的的 | 1-6-4, 1-6-5 | 容易 / 将原本 / 在 / 的. The two Leoz scenes are copies; the 装/将 variants make some lines separate rows: translate them identically |
| 通过太阳被改造 | 1-7-10 | 太阳石 Sunstone |
| 纯度纯高 | GRS 6-13-16 desc | 较高 "fairly high purity" |
| 御力提高30 | GRS 6-2-2 desc | 防御力 DEF+30 |
| 攻击力提高少12 | GRS 6-1-3 desc | ATK+12 |
| 敏减少 / 敏提高 / 速 | GRS 6-2-5, 6-3-6, 6-5-6, 6-12-1 desc | 敏捷 AGI |
| 群攻击力 | GRS 6-7-5 desc | "hits all enemies" |
| 单回复 | MRS 4-3-1 desc | 单体 one ally |
| 作用该物品 | GRS 6-14-2 desc | 使用: "Press SEARCH to use this item." |
| 圣光长袍 vs 圣光之袍 | 1-1-14 menu / GRS 6-2-10 | same item: Holy Robe |
| 王国早期历史记录 vs 王国早期记录 | 1-1-1 / 1-1-13 | same book: Early History of the Kingdom |
| 回城卷 vs 回城卷轴 | 1-2-1 | same item: Homeward scroll |
| 遗忘之城 vs 被遗忘之城 | map / 1-5-1 | the Forgotten City |
| six names for the Magic Institute | 1-2-1, 1-2-5 | the Magic Institute |
| 咒文之靴 recipe message vs code | 1-1-14@0315 | write what the code takes (Decision 12) |
| `清除lost` | 1-1-24 | the lose branch of the clean-up fights: "Clean-up failed." |
| `STUFF:` | 1-7-10 credits | "STAFF:" |
| 非常抱歉！因为引擎的BUG... | 1-1-1@0a96 | real notice: starting a second New Game without quitting breaks the engine; "Sorry! Due to an engine bug, please quit the game completely and restart before starting a new game." |
| item descriptions | GRS | 40 items have no description (key items, materials, scrolls, the bracelet, the ring...); 6-6-12 苹果's is 不详 "Unknown". Nothing to add |
| GBK (traditional) names | none | - |

## Counts

| category | terms |
|---|---|
| person | 9 |
| title | 11 |
| monster | 3 |
| other | 20 |
| sect | 1 |
| place | 43 |
| ui | 151 |
| item | 53 |
| armor | 48 |
| weapon | 19 |
| consumable | 10 |
| magic | 24 |
| **total** | **392** |


## People and titles

| zh | en | short | alt | note |
|---|---|---|---|---|
| 德拉特 | Delat |  |  | Hero 1 and crown prince of Okaros (王子; the King is his 父王). A mage: leaves the palace 'to train in magic' (1-1-9); stat/skill rewards for actor 1. Portrait pic=1. Sarcastic, put-upon, low stamina, secretly loyal; inner grumbles in brackets. Plain 'Delat' everywhere (no title). ARS 3-1-1 and the duplicate 3-1-3. |
| 艾露娜 | Eluna |  |  | Hero 2 (actor 2, portrait pic=2): orphan raised by Kabras Temple, junior swordswoman, bookworm on the 'surface' legend, wears the strange bracelet that is the real key to the Cross Entry. Bossy, impulsive, fearless, kind underneath. ARS 3-1-2 and duplicate 3-1-4. |
| 小娜 | Luna |  |  | Delat's pet name for Eluna (1-1-9, while she is trying to stab him). From the last syllable of E-lu-na. |
| 艾露 | Eluna |  |  | Typo for 艾露娜 in the message 前史官指着艾露的右手 (1-2-4). Write Eluna. |
| 洛克斯・雷特 | Locke Reiter |  | Reiter | The former royal historian (前史官) living outside Snowblade (1-2-2, 1-2-4). Resigned over the King's massacre; rude and cryptic ('I'll give you five seconds to get out'). Gives the Odd Key. The ・ is a name separator. |
| 雷特 | Reiter |  |  | Short for Locke Reiter: 雷特大人的信件 'a letter from Lord Reiter' (1-5-1). |
| 前史官 | former Historian |  | Master Historian | How everyone refers to Locke Reiter. 前史官大人 (Eluna's polite address) = 'Master Historian'. |
| 史官 | historian |  |  | Court historian (Reiter's old post). |
| 希瑟 | Heath |  |  | Sickly boy of 12-13 in Silverleaf (1-3-1, 1-3-5) who trades the expired pass for a meeting with the Moon branch leader who looks like his dead sister. Has Dorowell Syndrome and dies the next day. A boy: 'Heath', not 'Heather'. |
| 莱奥兹 | Leoz |  | Uncle Leoz | Ringleader of the Moon of Vengeance; armoured man in his forties (1-6-1). Elder brother of the King, so Delat's uncle (大伯); claims the throne was stolen from him. Eluna calls him 大叔 'mister' and, once she knows, 'Uncle Leoz' (莱奥兹大叔). His kids are 'little princes' in the epilogue. |
| 翼王 | Yiwang |  |  | The author's handle (credits 1-7-10: art, story, design, setting, production). Cameo when you Dig the right spot (1-0-7): '翼王:...TMD,我正在潜水...' - 潜水 'diving' is net slang for lurking on a forum: 'Damn it, I was lurking down here, why'd you dig me up?!' Keep the handle as pinyin (it means 'Wing King'). |
| 大叔 | Uncle |  |  | Two uses. (1) The temple keeper who raised Eluna (1-1-1, 1-1-3, 1-1-4, pic=0): Eluna calls him 'Uncle'; his tic is 早知道... 'If I'd known...'. (2) Eluna's 'mister' for strangers and Leoz ('Mister, why were you alone last time?'); after the reveal 'Uncle Leoz' works both ways. |
| 大伯 | uncle |  |  | Father's elder brother: Eluna to Delat about Leoz, 'He's your uncle, show some respect!' (1-6-4). |
| 父王 | Father |  |  | Delat's 'my father the King'. In dialogue 'Father' or 'my father'; 国王 = the King. The King is never named. |
| 国王 | King |  |  | The unnamed King of Okaros, Delat's father, Leoz's younger brother. Seized the throne, killed his mother (the ruler), drove out Kabras's people; wants the purest lightstone as a weapon against the Moon. |
| 王子 | prince |  |  | Delat ('刺杀王子那可是死罪' = 'Stabbing a prince is a capital crime'). |
| 医生 | doctor |  |  | Heath's doctor and guardian, a man of about thirty (1-3-5). |
| 管理者 | Steward |  |  | 被遗忘之城的管理者: the Forgotten City's steward, who shows them the evacuation records (1-5-1). |
| 队长 | Captain |  |  | 夜星城治安管理队的队长 = captain of the Nightstar Watch (1-4-1), who forgot his report. |
| 剑士 | swordsman |  | swordswoman | Eluna's calling (神殿里会出一个剑士 'a swordsman out of a temple'); 初级剑士 = 'Junior Swordsman' (the rank she earns: 'I'm not a little girl! I'm a Junior Swordsman!'). |

## Groups

| zh | en | short | alt | note |
|---|---|---|---|---|
| 复仇之月 | Moon of Vengeance |  | the Moon | Armed anti-government group (类武装恐怖分子组织 'quasi-armed terrorist group', founded ten years ago by Kabras's expelled citizens under Leoz). 'the Moon of Vengeance' in full; 'the Moon' is fine on second mention. 银叶城分部 = Silverleaf branch; 总部 = headquarters. |

## Places

| zh | en | short | alt | note |
|---|---|---|---|---|
| 剑士工会 | Swordsmen's Guild | Guild Hall |  | Where Eluna takes the junior swordsman exam (1-1-10); 工会 is a typo for 公会 'guild'. Banner (10) uses short 'Guild Hall'. |
| 魔法研究所 | Magic Institute |  | Institute for Magical Research and Control | The institute in Snowblade with the magic detector and the sealed maze underneath (1-2-1, 1-2-5). The source names it six ways (魔法研究与控制所, 魔法控制研究协会, 魔法研究控制所, 魔法控制研究学会, 魔法研究协会, 研究所): always 'the Magic Institute' (王宫的研究所 / 王宫的魔法研究协会 = 'the palace's Institute'). Map 2-3-3 研究所 = 'Institute'. |
| 魔法研究与控制所 | Magic Institute |  |  | Variant name (1-2-5 message): 'Magic Institute Hall' for 魔法研究与控制所大厅. |
| 魔法控制研究协会 | Magic Institute |  |  | Variant name (1-2-5). |
| 魔法研究控制所 | Magic Institute |  |  | Variant name (1-2-1). |
| 魔法控制研究学会 | Magic Institute |  |  | Variant name (1-2-5). |
| 魔法研究协会 | Magic Institute |  |  | Variant (1-2-5 '王宫的魔法研究协会' = the palace's Institute). |
| 研究所 | Institute |  |  | Map 2-3-3 (the maze under the Snowblade Institute); also short for the Magic Institute. |
| 神殿 | Temple |  |  | Kabras Temple (卡布拉斯的神殿), where Eluna was taken in as a foundling. Banner 1-1-2, map 2-2-12. 神职者 = clergy. |
| 圣殿内 | Sanctum |  |  | Banner 1-1-3: inside the temple. |
| 行政处 | city office |  |  | Silverleaf's administration office (1-3-4) that issues passes and pays bounties. Also '圣梅洛堡的行政处'. |
| 奥卡洛斯 | Okaros |  |  | The underground kingdom (奥卡洛斯王国 'the Kingdom of Okaros'), founded 500 years after the banishment. 全奥卡洛斯 = 'all of Okaros'. |
| 卡布拉斯 | Kabras |  |  | Capital of Okaros (国都), with the palace, the temple, the library and the graveyard. Banner 1-1-5/1-1-6, maps 2-1-1..3. The Cross Entry is under its palace. |
| 雪刃城 | Snowblade |  | Snowblade City | City west of Kabras (Reiter lives outside it; the Magic Institute). Map 2-1-5. 'Snowblade' alone in dialogue ('to Snowblade'); 'Snowblade City' only if the line needs it. |
| 银叶城 | Silverleaf |  | Silverleaf City | City with the old lightstone mine, Heath, and a Moon branch. Maps 2-1-6/7. |
| 夜星城 | Nightstar |  | Nightstar City | City whose top holds an ancient stone; outside it lies the Eternal Darkness. Maps 2-1-9/10. |
| 遗忘之城 | Forgotten City | Forgotten | the Forgotten City | Hidden city reached through the graveyard tunnel (1-6-6, 1-5-1) where the survivors of the King's purge of Kabras live. Map 2-1-11 (12): short 'Forgotten'. 被遗忘之城 is the same place. |
| 被遗忘之城 | Forgotten City |  |  | Same as 遗忘之城 (1-5-1 message). |
| 圣梅洛堡 | St. Melo Keep |  |  | The citadel of Silverleaf: 圣梅洛堡的矿区 'the St. Melo Keep mine' (1-3-1), 圣梅洛堡的行政处 'the St. Melo Keep office' (1-6-4). Same office as 银叶城的行政处. |
| 王宫 | palace |  | Royal Palace | The royal palace in Kabras (also 皇宫). 王宫的下水道 = the palace sewers (Eluna's favourite entrance). |
| 皇宫 | palace |  |  | Same as 王宫. |
| 王宫前 | Palace |  |  | Banner 1-1-7 (in front of the palace). |
| 皇宫图书馆 | Royal Library |  |  | Palace library where Delat and Eluna read (1-1-1, 1-1-9, 1-1-13). |
| 图书馆 | Library |  |  | Banner 1-1-13, map 2-2-5. |
| 房间 | Bedroom |  |  | Banner 1-1-4: Eluna's room at the temple. |
| 城外 | Outskirts |  |  | Banner 1-2-2: Reiter's house outside Snowblade. In dialogue 'outside the city'. |
| 墓地 | Graveyard |  |  | Kabras Graveyard (map 2-1-4): the movable gravestone hides the tunnel to the Forgotten City. |
| 矿区 | Mine |  |  | Map 2-1-8: Silverleaf's old lightstone mine, sealed after a great explosion; needs a pass. Also 光之石的矿区 'lightstone mines'. |
| 室内 | Indoors |  |  | Generic interior maps 2-2-1..4. |
| 走廊 | Corridor |  |  | Map 2-2-6. |
| 大厅 | Hall |  |  | Map 2-2-7. |
| 商店 | Shop |  |  | Maps 2-2-8/9. |
| 旅馆 | Inn |  |  | Map 2-2-10; inn stays cost 100 Gold. |
| 工房 | Workshop |  |  | Map 2-2-11: the Kabras crafting/refining workshop (1-1-14). |
| 下水道 | Sewers |  |  | Map 2-2-13: the palace sewers. Eluna: 是'道'就是用来走的 - a pun on 道 'road/way': 'If it's called a passage, it's meant to be passed through.' |
| 楼梯 | Stairs |  |  | Map 2-2-14. |
| 夜星城外 | Nightstar Wilds | Star Wilds |  | Maps 2-2-16 (the black screen used for the prologue scroll and the Eternal Darkness) and 2-3-4. 12-char map field: short 'Star Wilds'. |
| 雪刃城外 | Snowblade Wilds | Blade Wilds |  | Map 2-3-2. Short 'Blade Wilds'. |
| 迷宫 | Maze |  |  | Maps 2-2-17, 2-3-1, 2-3-6..18, 2-4-7. The exam tower, the Institute maze, the mine, the palace depths. |
| 十字之门 | Cross Entry |  | the Cross Entry | The gate to the surface (map 2-3-5) and the game's title; the author's own logo says 'CrossEntry'. Write 'the Cross Entry' in text, never 'Cross Gate'. It lies under Kabras palace; four pillars take the four Crests. |
| 野外 | Wilds |  |  | Overworld maps 2-4-1..4, 2-4-6. |
| 地道 | Tunnel |  |  | Map 2-4-5: the tunnel under the graveyard (地下道 in 1-1-15). |
| 未命名 | Unnamed |  |  | Maps 2-2-18/19 (the true surface and the epilogue) carry the author's placeholder name 未命名 'unnamed'; the scene field of 1-7-10 shows it too. Keep 'Unnamed'. |

## Weapons

| zh | en | short | alt | note |
|---|---|---|---|---|
| 短剑 | Shortsword |  |  | Hand (sword). |
| 晶石短刃 | Gem Dagger |  |  | Hand (crystal short blade). |
| 魔纹短剑 | Runed Dirk |  |  | Hand (rune-etched short sword). Dig reward. |
| 暗影之触 | Dark Touch |  |  | Hand (touch of shadow). |
| 冰霜之刃 | Frostblade |  |  | Hand; immune to Cnf. Dig reward. |
| 铁剑 | Iron Sword |  |  | Sword. |
| 长战剑 | Longsword |  |  | Sword. |
| 十字剑 | Crossblade |  |  | Sword (cross sword). |
| 细刃剑 | Rapier |  |  | Sword (thin-bladed). |
| 暗银剑 | Darksilver |  |  | Sword; hits all enemies (群攻击). Nightstar maze. |
| 杀龙之剑 | Dragonbane |  |  | Sword; ATK+220 DEF-60. Nightstar. |
| 太阳之剑 | Sunblade |  |  | Sword; mine treasure (1-3-10). |
| 木杖 | Wood Staff |  |  | Staff. |
| 星之杖 | Star Staff |  |  | Staff. |
| 炽炎之杖 | Blaze Rod |  |  | Staff (blazing staff). |
| 预言者之杖 | Seer Staff |  |  | Staff. Mine chest. |
| 祭司权杖 | Cleric Rod |  |  | Staff (priest's sceptre); sold for 5000 Gold by a Nightstar man (1-4-12). |
| 诅咒之杖 | Curse Rod |  |  | Staff; inflicts Psn (毒x3 'Psn x3'). |
| 彩光之轮 | Prism Disc |  |  | Weapon (wheel of coloured light); locked chest in Kabras (1-1-23). |

## Armour and accessories

| zh | en | short | alt | note |
|---|---|---|---|---|
| 羽帽 | Plume Cap |  |  | Head. DEF+12 DEX+4. Reward for the Kabras clean-up quest (1-1-24). |
| 轻质头盔 | Light Helm |  |  | Head. |
| 骑士头盔 | Great Helm |  |  | Head. The four 骑士 'knight' pieces use real knightly armour words because 'Knight X' is over 10: Great Helm, Plate Mail, Sabatons, Gauntlets. |
| 强化头盔 | Steel Helm |  |  | Head (reinforced helm). Institute maze chest. |
| 雷鸣战盔 | Storm Helm |  |  | Head (thunder war helm). Palace depths. |
| 魔术师之帽 | Wizard Hat |  |  | Head. |
| 预言者之帽 | Seer Hat |  |  | Head; craftable (1-1-14 menu item 'Seer-Hat'). 预言者 = Seer (Seer Staff). |
| 守护之帽 | Guard Cap |  |  | Head; DEF+50, immune to Stn. Dig reward. |
| 旅行之服 | Trail Garb |  |  | Body (travel clothes). |
| 贵族套服 | Noble Suit |  |  | Body. |
| 轻铁甲 | Light Mail |  |  | Body. |
| 链甲 | Chain Mail |  |  | Body. |
| 骑士之铠 | Plate Mail |  |  | Body (knight's armour). |
| 勇气之铠 | Brave Mail |  |  | Body; immune to Sil. Reward for the Snowblade lost-son quest chest. |
| 龙鳞战甲 | Dragonmail |  |  | Body (dragon-scale war armour). 'Dragon Mail' is 11. |
| 月影之服 | Moon Garb |  |  | Body (moon-shadow clothes). |
| 祭司长袍 | Vestments |  |  | Body (priest's robe). 'Priest Robe' is 11. |
| 圣光之袍 | Holy Robe |  |  | Body; immune to all ailments; craftable. The 1-1-14 menu writes it 圣光长袍: same item, menu 'Holy-Robe'. |
| 圣光长袍 | Holy Robe |  |  | Menu spelling (1-1-14) of 圣光之袍. |
| 布靴 | Soft Boots |  |  | Feet (cloth boots). |
| 锁链鞋 | Mail Shoes |  |  | Feet (chain shoes). |
| 钢甲靴 | Iron Boots |  |  | Feet (steel-plated boots). |
| 荆棘战靴 | Thornboots |  |  | Feet; ATK+65 HP-30. |
| 疾风之鞋 | Gale Shoes |  |  | Feet. |
| 骑士战靴 | Sabatons |  |  | Feet (knight's boots). |
| 咒文之靴 | Rune Boots |  |  | Feet; craftable; a Kabras girl trades Scroll G for a pair (1-1-25: 'shoes with pretty writing on them... spell-something'). 咒文 = runes. Menu 'Rune-Boots'. |
| 无声之靴 | Hush Boots |  |  | Feet (silent boots). |
| 轻木盾 | Buckler |  |  | Hand (light wooden shield). |
| 厚钢盾 | Big Shield |  |  | Hand (thick steel shield). 'Steel Shield' is 12. |
| 十字重盾 | Cross Ward |  |  | Hand (heavy cross shield). Mine chest. |
| 黄金战盾 | Gold Aegis |  |  | Hand (golden war shield). |
| 希望之盾 | Hope Aegis |  |  | Hand; craftable (menu 'Hope-Aegis'). |
| 软布手套 | Soft Mitts |  |  | Wrist (soft cloth gloves). |
| 战斗手套 | War Gloves |  |  | Wrist. |
| 咒文手套 | Rune Mitts |  |  | Wrist (rune gloves). Dig reward. |
| 骑士手套 | Gauntlets |  |  | Wrist (knight's gloves). |
| 耐力之手 | Stout Hand |  |  | Wrist (hand of endurance). Mine chest. |
| 精准之手 | Sure Hand |  |  | Wrist (hand of precision); craftable (menu 'Sure-Hand'). |
| 荆棘手套 | Thorn Grip |  |  | Wrist (thorn gloves). |
| 书签 | Bookmark |  |  | Accessory, SPI+4; a Nightstar girl's handmade thanks for her necklace (1-4-13). |
| 剑士徽章 | Sword Pin |  | swordsman's badge | Accessory, ATK+25: the swordsman badge Eluna gets for passing the exam (1-1-12). In dialogue 'swordsman's badge' is fine. |
| 恶魔之眼 | Demon Eye |  |  | Accessory: Yiwang's gift after his cameo fight (1-0-7). |
| 十字项链 | Rosary |  |  | Accessory, HP+20 per turn (cross necklace); the apple man's thanks (1-3-18). |
| 银质指环 | Silverband |  |  | Accessory, MP+17 per turn (silver ring). |
| 星月耳环 | Star Studs |  |  | Accessory (star-and-moon earrings). |
| 火焰之心 | Flameheart |  |  | Accessory. |
| 永恒之印 | Ever Seal |  |  | Accessory (seal of eternity). |
| 飓风之石 | Storm Gem |  |  | Accessory (hurricane stone). |

## Consumables

| zh | en | short | alt | note |
|---|---|---|---|---|
| 苹果 | Apple |  |  | Two items: accessory 6-6-12 (desc 不详 'Unknown'), bought for 5000 Gold (1-3-17), and food 6-9-1, which the hungry man wants (1-3-18). |
| 生命药剂 | HP Potion |  |  | Restores 180 HP to one. |
| 魔力药剂 | MP Potion |  |  | Restores 120 MP; the Kabras potion maker trades them for Shardstones (1-1-21). |
| 生命之泉 | HP Fount |  |  | Restores 360 HP (fount of life). |
| 魔力之泉 | MP Fount |  |  | Restores 270 MP. |
| 特殊药剂 | Elixir |  |  | Restores 200 HP and 200 MP (special potion). Not related to the 'Special' mode. |
| 圣水 | Holy Water |  |  | Cures ailments (one). |
| 恢复卷轴 | Recovery |  | Recovery scroll | Scroll: restores 300 HP and MP to one. Scroll items drop the word 'Scroll' (10-char field); in dialogue 'a Recovery scroll'. |
| 复活卷轴 | Revival |  | Revival scroll | Scroll: revives an ally. |
| 强化药剂 | Booster |  |  | ATK, DEF and AGI +50% for 4 turns. |

## Items, key items and materials

| zh | en | short | alt | note |
|---|---|---|---|---|
| 王国早期历史记录 | Early History of the Kingdom |  |  | Book title (1-1-1). Same book as 王国早期记录 (1-1-13): use one title for both. |
| 王国早期记录 | Early History of the Kingdom |  |  | Book title (1-1-13); same book as 王国早期历史记录. |
| 隐秘炼金术全解 | Complete Secrets of Alchemy |  |  | Book title (1-1-1). |
| 怪异喷泉杀人事件 | The Strange Fountain Murders |  |  | Delat's secret mystery novel (1-1-1): a Detective Conan-style case title. |
| 奇怪的手链 | Bracelet |  | strange bracelet | Eluna's strange bracelet (item 6-6-10): its stone is Sunstone and it is the true key to the Cross Entry. In dialogue 这条手链 = 'this bracelet'. |
| 手链 | bracelet |  |  | Eluna's bracelet in dialogue. |
| 戒指 | Ring |  |  | Leoz's ring (6-6-11): dropped on the road (1-6-1), worth a bounty; Eluna hands the office a fake and returns the real one (1-6-4). |
| 回城卷轴 | Homeward |  | Homeward scroll | Scroll: returns you to the last city (1-255-1) and powers the teleport circles; useless once inside the palace finale ('回城卷轴无法使用！！' = 'The Homeward scroll won't work!!'). 回城卷 (1-2-1) is the same. |
| 回城卷 | Homeward |  | Homeward scroll | Short form in 1-2-1: 'a Homeward scroll'. |
| 钥匙 | Key |  |  | Plain key (6-13-1); craftable; opens chests. In the story 钥匙 also means the four magic 'keys' that open the Cross Entry, which turn out to be the Crests: 'key' in dialogue. |
| 白钥匙 | White Key |  |  | Opens white doors in the mazes. |
| 黑钥匙 | Black Key |  |  | Opens black doors in the mazes. |
| 特殊的钥匙 | Odd Key |  |  | Reiter's key to the movable gravestone (1-2-4). 'Special Key' is 11. |
| 纹章I | Crest I |  |  | First Cross Entry key, from the Institute maze guardian (1-2-7). The four Crests go into the four pillars at the Cross Entry (1-7-10: 将纹章I嵌入了柱子 'Set Crest I into the pillar'). |
| 纹章II | Crest II |  |  | Second key: the Silverleaf mine guardian (1-3-11). |
| 纹章III | Crest III |  |  | Third key: the Nightstar maze guardian (1-4-6). |
| 纹章IV | Crest IV |  |  | Fourth key: the Forgotten City maze guardian (1-5-6). |
| 纹章 | Crest |  |  | Generic. |
| 卷轴碎片A | Fragment A |  |  | One of four scroll fragments (A-D) that the workshop joins into Scroll L. |
| 卷轴碎片B | Fragment B |  |  | Reward for the X/Y puzzle in Snowblade (1-2-12). |
| 卷轴碎片C | Fragment C |  |  | Mine. |
| 卷轴碎片D | Fragment D |  |  | Nightstar maze. |
| 卷轴碎片 | Fragment |  | scroll fragment | Generic: the scroll fragments A-D ('scroll fragment' in running text). |
| 项链 | Necklace |  | locket | Key item 6-13-13: the Nightstar girl's lost necklace (1-4-13/14). In 1-3-1 Heath's 项链 holds a photo: 'locket' there. |
| 碎光石 | Shardstone |  |  | Lightstone of very low purity; the basic refining material (2 -> 1 Glimstone). |
| 微光石 | Glimstone |  |  | Low-purity lightstone (2 -> 1 Starstone). Menu 'Glimstone'. |
| 星光石 | Starstone |  |  | Fairly high purity (desc 纯度纯高 = 较高). Set into the mine pillars. |
| 晨光石 | Dawnstone |  |  | Very high purity. |
| 耀星石 | Blazestone |  |  | Lightstone refined by a special method (Starstone + Dawnstone + Glowwood), from the recipe in the Early History; breaks the Eternal Darkness (1-1-13, 1-4-3). |
| 赤铁矿 | Hematite |  |  | Crafting ore (red iron ore). |
| 磷木 | Glowwood |  |  | Crafting material (phosphor wood). |
| 绒羽 | Soft Down |  |  | Crafting material (down feathers). |
| 书本 | Book |  |  | Key item. |
| 零件 | Cogwheel |  |  | Machine part, fitted into the mine machinery (嵌入零件). |
| 通行证 | Pass |  |  | The Silverleaf mine pass. Heath's 'special pass' turns out to be a month out of date; the office swaps Leoz's (fake) ring for a valid one. In the prologue also the palace pass Eluna wants. |
| 点燃 | Ignite |  |  | Field skill item (drawn as 'Ignite' in the banner image). Desc/1-255-2: 'Press SEARCH to use this item.' 无法点燃 = 'Nothing to light here.' Also lights the four torches of a puzzle (1-0-6; 错误 'Wrong!'). |
| 挖掘 | Dig |  |  | Field skill item ('Dig' banner). INSERT key. 什么都没有挖到 = 'You dug up nothing.' 严禁到处乱挖 = 'Digging here is strictly forbidden.' |
| 攀爬 | Climb |  |  | Field skill item ('Climb' banner). MODIFY key. 无法攀爬 = 'Nothing to climb here.' |
| 击碎 | Smash |  |  | Field skill item ('Smash' banner). DEL key. 无法击碎 = 'Nothing to smash here.' |
| 指北针 | Compass |  |  | Toggles the coordinate display (1-255-18). |
| 技能卷轴A | Scroll A |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴B | Scroll B |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴C | Scroll C |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴D | Scroll D |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴E | Scroll E |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴F | Scroll F |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴G | Scroll G |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴H | Scroll H |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴I | Scroll I |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴J | Scroll J |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴K | Scroll K |  |  | Skill scroll: using it teaches a skill (1-255-5..16). |
| 技能卷轴L | Scroll L |  |  | Skill scroll: using it teaches a skill (1-255-5..16). Craftable from Fragments A-D; menu item 'Scroll-L'. |
| 技能卷轴 | Scroll |  | skill scroll | Generic: the skill scrolls A-L ('skill scroll' in running text). |

## Skills (MRS)

| zh | en | short | alt | note |
|---|---|---|---|---|
| 炎击术 | Fire Strike |  |  | Delat. Single target, base 180, may cut ATK. |
| 冰刃突袭 | Ice Rush |  |  | Delat (Scroll A). Single, may cut AGI. |
| 狂风术 | Whirlwind |  |  | Delat (1-3-18 teacher, Special). Single, base 280. |
| 陨石术 | Meteor |  |  | Delat (Scroll C). Single, may stun. |
| 生命吸取 | Life Drain |  |  | Delat (Scroll I). |
| 怒雷击 | Thunderclap |  |  | Delat (1-4-11 teacher, Special). All enemies. |
| 冰陨碎破 | Hailstorm |  |  | Delat (Scroll L). All enemies, may cut AGI. |
| 精神冲击 | Mind Blast |  |  | Delat (Scroll G). Drains MP, may cut DEF. |
| 战技封锁 | Skill Lock |  |  | Eluna (1-3-15 teacher, Special). Silences one enemy (咒封 = Sil). Also a choice row. |
| 暗削 | Dark Cut |  |  | Eluna (Scroll D). May silence. |
| 烈风斩 | Gale Slash |  |  | Eluna (Nightstar captain, Special). All enemies. |
| 破碎击 | Shatter |  |  | Single, may cut DEF. |
| 红莲之印 | Red Lotus |  |  | Eluna (Scroll K). Single, base 400 (seal of the red lotus). |
| 耀击 | Dazzle |  |  | Eluna (1-4-11 teacher, Special). Damage plus MP damage. |
| 影斩 | Shade Slash |  |  | Eluna (Scroll E). May confuse. |
| 毒刺 | Venom Sting |  |  | Eluna (Scroll H). May poison. |
| 光盾术 | Light Ward |  |  | Delat (1-2-11 drunk, Special). All allies DEF+50%. |
| 热血 | Hot Blood |  |  | Eluna (Scroll B). All allies ATK+50%. |
| 疾驰 | Haste |  |  | Eluna (1-2-12 puzzle man, Special). One ally AGI+50%. |
| 治愈术 | Heal |  |  | Delat (1-1-20 inn guest, Special). 180 HP and cures ailments. |
| 急救 | First Aid |  |  | Eluna (1-1-21 potion maker for a Dawnstone, Special). 450 HP. |
| 圣光术 | Holy Light |  |  | Delat (Scroll F). Heals all. |
| 复活术 | Revive |  |  | Delat (1-3-15 teacher, Special). Also a choice row. |
| 巧取 | Pilfer |  |  | Eluna (Scroll J). Steals an item. |

## Enemies

| zh | en | short | alt | note |
|---|---|---|---|---|
| 守护者 | Guardian |  |  | The four key-keepers (纹章 bosses) and the final boss at the Cross Entry: humans turned into living Sunstone weapons 2000 years ago, who led the survivors underground and guard the exit. 最后的守护者 = 'the last Guardian'. |
| 召唤兽 | summoned beasts |  |  | The Moon's fighters bring summoned beasts (1-3-3). |
| 怪物 | monster |  |  | Generic. |

## Other terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 治安管理队 | Watch |  |  | Nightstar's security force: 'the Nightstar Watch'. 管治安的家伙 = 'the Watch fellow'. |
| 地面 | surface |  |  | The world above (地面 'the ground surface'): 'the surface', 美丽的地面 'the beautiful surface'. 地下 = underground / 'down here'. |
| 魔法研究所禁区 | Institute restricted area |  |  | Message 1-2-5. |
| 传送阵 | teleport circle |  |  | The cities' warp circles, started with a Homeward scroll (1-2-1); destroyed by the Moon in the attack (1-7-3). |
| 光之石 | lightstone |  |  | The underground world's magic ore and energy source, graded by purity (Shardstone < Glimstone < Starstone < Dawnstone; Blazestone is a specially refined one). Lower case in running text. |
| 太阳石 | Sunstone |  |  | The ultimate refinement of lightstone: does not glow but holds terrible power. The stone in Eluna's bracelet. 2000 years ago a Sunstone war and a destroyed Sunstone reserve (太阳石能源库) poisoned the surface. 通过太阳被改造 (1-7-10) is a slip for 太阳石: 'remade with Sunstone'. |
| 永恒的黑暗 | Eternal Darkness |  |  | Magical darkness outside Nightstar that torches cannot light (1-4-3); the Blazestone dispels it. |
| 十字历 | Cross Era |  |  | Epilogue calendar: 十字历六年 = 'Year 6 of the Cross Era'. |
| 魔法探测装置 | magic detector |  |  | The Institute's detection array (also 魔法探测器). Eluna supercharges it and spots every magical anomaly in the country. |
| 魔法探测器 | magic detector |  |  | Same as 魔法探测装置. |
| 恐怖分子 | terrorists |  |  | The Moon of Vengeance as the government brands it. |
| 叛军 | rebels |  |  | The King's cover story for Kabras's expelled citizens (1-6-4). |
| 通缉令 | wanted poster |  |  | Leoz's poster at the Silverleaf office (1-3-4). |
| 多罗维尔综合症 | Dorowell Syndrome |  |  | Heath's fatal illness; the sign is a spot on the right ear (1-3-5). Invented disease. |
| 剑术考试 | sword exam |  |  | Eluna's junior swordsman exam at the Swordsmen's Guild (1-1-1..12): climb the tower maze in three hours and beat the monster on top. |
| 神职者 | clergy |  |  | 做个神职者 = 'be one of the clergy'. |
| 高速波动剑 | Hyper Wave Sword |  |  | Eluna's comic 'special move' on Delat (1-1-9 messages: 平挥 'Side sweep', 直刺 'Straight thrust', 高速波动剑 'Hyper Wave Sword!'). |
| 狂风流秘术 | Whirlwind-school secret art |  |  | 1-3-18 teacher's cry before teaching Whirlwind: 'Behold! The secret art of the Whirlwind school...' |
| 迷阵・改 | Maze Mk II |  |  | Maze sign (1-5-3). With 相同到相同 'Same to same' and 坚持就是胜利 'Persistence is victory'. |
| 圆周率 | Pi |  |  | Maze hint sign in the Institute maze (1-2-6): the puzzle is solved with the digits of pi (3.1415926...). |

## UI, stats and labels

| zh | en | short | alt | note |
|---|---|---|---|---|
| 普通 | Normal |  |  | New Game mode (1-1-1 choice 1). |
| 特别 | Special |  |  | New Game mode (1-1-1 choice 2, sets event 2008): tougher enemy sets, higher starting stats, and extra skill teachers who only teach on Special. NPCs quote it: 你不是'特别'啊 = 'You're not on "Special", huh?'. Keep 'Special' in quotes there. |
| 请选择模式 | Choose a mode. |  |  | 1-1-1 message before the Normal / Special choice. |
| 金币 | Gold |  |  | Money (UI 'Gold:'). 获得金币: 1000 = 'Got 1000 Gold.' 100金币 = '100 Gold'. 5000块 / 5000钱块 = '5000 Gold'. |
| 生命值 | HP |  |  | Status word (生命 in the UI). |
| 魔法值 | MP |  |  | Status word. |
| 攻击力 | ATK |  | Attack | Status word: 'Attack' in the status screen, ATK in descriptions. |
| 防御力 | DEF |  | Defense | Status word: 'Defense' / DEF. |
| 敏捷 | AGI |  | Agility | Agility / AGI (also 敏, 速 in descriptions). |
| 精神 | SPI |  | Spirit | Spirit / SPI. |
| 灵巧 | DEX |  | Dexterity | Dexterity / DEX. |
| 使用钥匙 | Use Key |  |  | Choice; partner 取消 'Cancel'. |
| 使用黑钥匙 | Use Black Key |  |  | Choice. |
| 使用白钥匙 | Use White Key |  |  | Choice. |
| 嵌入星光石 | Set Starstone |  |  | Choice (mine pillars, 1-3-7). |
| 嵌入零件 | Fit Cogwheel |  |  | Choice (mine machinery, 1-3-8). |
| 制作物品 | Craft item |  |  | Workshop choice (1-1-14); partner 提炼光之石 'Refine lightstone'. |
| 提炼光之石 | Refine lightstone |  |  | Workshop choice (1-1-14). |
| 没有该物品 | You don't have that. |  |  | Message after a failed key/item use. |
| 材料不足 | Not enough materials. |  |  | Workshop message. |

Placeholder labels kept unchanged (category ui, en = zh): `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `43`, `44`, `45`, `46`, `47`, `48`, `49`, `50`, `51`, `52`, `53`, `54`, `55`, `56`, `57`, `58`, `59`, `60`, `61`, `62`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `81`, `82`, `83`, `84`, `85`, `86`, `a`, `b`, `c`, `c6`, `c7`, `c8`, `c9`, `c10`, `c11`, `c12`, `c13`, `c14`, `c15`, `c16`, `c17`, `c18`, `c19`, `c20`, `c21`, `c22`, `c23`, `c24`, `c25`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `d10`, `d11`, `d12`, `d13`, `d14`, `d15`, `d16`, `d17`, `d18`, `d19`, `d20`, `d21`, `d22`, `d23`, `d24`, `d25`, `d26`, `d27`, `d28`, `d29`, `d30`, `d31`, `d32`, `d33`, `d34`, `d35`, `d36`, `d37`, `d38`, `d39`, `d40`, `d41`, `x`.
