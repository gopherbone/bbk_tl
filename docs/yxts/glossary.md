# 英雄坛说 English glossary

Status: **draft, decisions made** (no open questions block translation; the reviewer can override any row).
Machine-readable source: `docs/yxts/glossary.jsonl` (one term per line: `zh`, `en`, `category`, `count`, `alt`,
`note`, `source_ids`, optional `short`). This page summarises the same data. Story background: `docs/yxts/story.md`;
translator brief: `docs/yxts/translating.md`.

- `count` = how often the zh string occurs as a substring across `work/yxts.strings.jsonl` (all kinds). Short terms
  over-count (信 matches every 信, 怪 matches 怪兽), so read it as "how common".
- Field limits (from `tools/tl/common.py problems()`): item names (grs.name) <= 10 chars, ARS names (party, NPCs,
  enemies) <= 11, magic names (mrs.name) <= 11, map names <= 12, scene banners (setscenename) <= 10, choices <= 19,
  menus = the same number of space-separated items as the Chinese. `en` fits every field the term is used in; when
  the natural form is longer it is in `alt`. `short` exists only where `en` is wanted in dialogue but is over an
  11-char ARS field or a 10-char banner (白瑞德 "Rhett Butler" / ARS "R. Butler"; 冰火岛 "Icefire Isle" / banner
  "Icefire"). `tools/tl/autofill.py` uses `short` automatically where `en` breaks the row's limit.
- All `en`/`alt`/`short` values are plain ASCII (no accents, curly quotes or em dashes; "Jose", not "José").
- Validation (scratch script): every grs.name / mrs.name / ars.name / map.name / setscenename row (510 rows,
  including the 62 numbered NPC/object labels) has a term that fits its limit. Result: 0 errors.
  `autofill.py` writes those 510 rows to `translations/yxts/parts/auto.jsonl`; `check.py` reports 0 errors and 31
  warnings, all expected (an ARS row showing the `short` form, or a substring hit such as 金矿 inside 金矿1 =
  "Gold 90%").

## What kind of game this is

A 2005 hobby RPG by 才子工作室 (Caizi Studio): design 金远见, adaptation 柴梓 (who was about to start his second
year of senior high school). Not a Jin Yong pastiche but a jokey **time-travel isekai**: a modern teenager switches on
a time machine and wakes up as a 14-year-old boy in 平安镇, a small town "west of the Central Plains", and must
take the tokens of six sects to lure out the Archdemon who came through with him. Heavy fourth-wall humour (the
adapter Chai Zi appears as a character, a chorus of "Players" complains, item descriptions argue with themselves),
2005 Chinese internet slang (MM, 886, 5555, 汗, 晕, 靠, 偶, 斑竹), cameos of BBK Club forum members (SSK,
Xiaoyao, Deng Shiyu...), literary and pop-culture parody names (Rhett Butler, Grandet, Camille, Jubei,
Tien Shrimp, Nobi), and MUD-style systems copied from 侠客行-type text MUDs (NPC "look" texts, potential points,
skill ranks, fame). See `docs/yxts/story.md`.

## Conventions

**Names.** Pinyin without tones, surname first, given name one word (Dugu Sheng, Ouyang Jian, Tang Jing, Gu Yanwu,
Li Qingzhao, Deng Shiyu), as fmj/jy. Apostrophes where pinyin needs them (Cong'er, Si'er). 阿- names "Ah X" (Ping Ah
Si). Real people keep their usual English (Gu Yanwu, Li Qingzhao, Zhu Yuanzhang, Ximen Qing). **Parody names are
rendered so the joke survives in English**: when the Chinese is the standard Chinese name of a Western or Japanese
character, use that character's English name (白瑞德 Rhett Butler, 葛朗台 Grandet, 茶花女 Camille, 荷西 Jose,
十兵卫 Jubei, 野比 Nobi); when it is a one-character twist on a famous name, twist the English name the same way
(天津虾 Tien Shrimp for Tien Shinhan, 孙悟莱 Son Gorai for Son Goku, 藤王丸 Fujiomaru for Haohmaru, 枳右京 Ukyo,
未知火舞 Mai Shiranui); Chinese parodies keep pinyin (李也白 Li Yebai, 西门广 Ximen Guang, 潘小莲 Pan Xiaolian).
Forum handles are translated as handles when they mean something (爱情没心跳 Flatline Love, 泡泡友 Bubble Pal)
and kept when they are already a name (SSK, 逍遥 Xiaoyao, 亮 Liang). Names over 11 chars get a `short` for the ARS
field: given name (Weiyang, Zhongyang, Daoming, Baozhen) or a short form (R. Butler, Shiranui). Dialogue uses the
full name.

**Places.** Invented places with a meaning are translated, one word where a menu needs it (平安镇 Safehaven,
大雪山 Snowpeak, 神童乐园 Prodigy Park, 锁妖塔 Demonspire, 幻境 Dreamscape, 阴间 the Nether, 极恶洞 Vile Cave);
real or literary places keep pinyin or their known English (香山 Mt. Xiang, 五指山 Mt. Wuzhi, 武当山 Mt. Wudang,
商家堡 Shang Fort, 冰火岛 Icefire Isle, 玉女峰 Jade Peak). Patterns: 入口 = "X Gate" (fmj), 后院 = "X Yard",
后山 = "X Ridge", 郊 = "Wilds", 山洞 = "Cave". Banners are 10 chars: 冰火岛 banner "Icefire", 冰火岛入口 banner
"Isle Gate", 恶魔洞一层 "Demon Cave" (the "first floor" is dropped; there is only one).

**Sects.** 花间派 Flower Sect, 伊贺谷 Iga Valley, 雪山派 Snow Sect, 红莲派/红莲教 Red Lotus Sect, 武当派 Wudang Sect,
八卦派 Bagua Sect; the player's own 门派/帮派 = "sect" ("My Sect"). 掌门 = Sect Head. The six sect heads' 令牌 are
"tokens" in dialogue; the item names are "X Tag" (Flower Tag, Iga Tag, Snow Tag, Lotus Tag, Wudang Tag, Bagua Tag)
because "Wudang Token" (12) is over the 10-char item field.

**Arts.** Elemental spells: 咒 = Spell (fmj): Fire / Wind / Earth / Ice / Bolt Spell (雷咒 "Thunder Spell" is 13).
The five elements are Thunder, Wind, Earth, Water, Fire (雷 风 土 水 火, menu 1-0-9). Higher spells are short
evocative names (True Fire, Meteor Rain, Inferno, Thunderclap, Sky Thunder, Sky Quake, Rain Sorrow, Dust Gale,
Heaven Gale, Flying Rock, Avalanche); the literal reading is in `alt` for dialogue and descriptions. Weapon arts:
鞭 = Whip/Lash, 拳 = Fist, 杖 = Staff, 刀 = Blade, 剑 = Sword (Basic Sword, Basic Staff as jy). Skills trained with
essence (1-1-19) and rated by Mr. Wenshi: 装备锻造 Forging, 读书识字 Literacy, 轻功 Step (lightness skill),
内功 Qi (inner art), 招架 Parry, 拳脚 Fist, 剑法 Sword, 刀法 Blade, 杖法 Staff, 鞭法 Whip, with 基本 = Basic,
门派 = Sect (Basic Step, Sect Qi).

**Equipment.** 10 chars. Slot words that fit: Hat, Helm, Robe, Silk, Gauze, Mail, Cape, Cuff (护腕, jy), Shoes,
Boots, Ward (符; fmj's "Charm" does not fit 白鬼符/黑鬼符), Orb (珠), Writ (令), Pill (丹/丸). Top items may drop the
slot word (Panther, Dragonhide, Dragonbug, Sky Silk). Metal swords are one word (Goldfang, Silverfang, Bronzefang,
Ironfang) because "Silver Sword" is 12. The 魔剑 is the **Hexblade**, purified "Hexblade+1" .. "Hexblade+9"; the
镇妖剑 the **Quellblade** (镇妖 = demon-quelling: Quellstone too); fused they make the **God-Demon**. Ores are named
by purity, as the descriptions do: 金矿1/2/3 = Gold 90% / 80% / 70%, likewise Silver, Copper, Iron.

**Menus.** A `menu` row is split on spaces and must keep the same number of items, so **menu items cannot contain
spaces**. Use the one-word forms this glossary gives (Safehaven, Snowpeak, Shang, Jade, Wuzhi, Icefire, Wudang,
Prodigy, Sect; Flower, Iga, Snow, Lotus, Bagua; Step, Qi, Parry, Fist...) and otherwise join words with a hyphen
(Fire-Spell, True-Guard, Sect-Qi, Check-Qi). The hero menu 1-1-1 "独孤圣 欧阳剑 唐静" uses the surnames:
"Dugu Ouyang Tang". Keep items short (<= 10 is safe).

**Forms of address.** 掌门 Sect Head ("掌门好!" from your disciples = "Welcome, Master!"), 大侠 hero, 少侠/小侠 young
hero, 女侠 heroine (本女侠 = Yuxin's "yours truly"), 客官 sir, 姑娘 Miss, 小伙子 lad, 小子 kid (bosses and villains
to the hero), 前辈 sir, 道长 Taoist (Taoist Qingxu), 长老 Elder (Elder Fang), 村长 Elder (fmj), 斑竹 moderator.
Humble 老夫 / 妾身 / 老身 = plain "I". Speaker tags stay "Name: text" with an ASCII colon (the source mixes ':' and
'：'). 系统提示 = "System:", 众玩家 = "Players:", 玩家 = "Player:", 我是谁 = "Who Am I:", ??? stays "???:".

**Register.** Cheeky teenage-forum comedy over a wuxia skin. Plain modern English, contractions, short punchy lines.
Keep the jokes, the fourth-wall asides and the bickering; translate net slang into English equivalents rather than
explaining it (886 "Bye!", 5555 "Boo-hoo", 汗 "*sweat*", 晕 "Ugh"/"Good grief", 靠/KAO "Damn", 嘎嘎 "Hehe",
TMD "damn it", MM "girls"). Censored swearing (`***`, `@#$%^&*`) and gibberish "translations" (the tiger's
"嗷嗷呜") stay as symbols/sounds. Real quotations (色即是空 "Form is emptiness", 一寸光阴一寸金 "An inch of time is an
inch of gold") may use their usual English. Bosses all say "滚!" ("Get lost!") and fall with "......看来我武功下降
了......啊!......" ("...Looks like my kung fu has slipped... Argh!...").

**UI and stats.** Engine strings are fmj's (`translations/yxts/parts/engine.jsonl`). Descriptions: 防御 Defense /
DEF, 攻击 Attack / ATK, 灵力 Spirit / SPI, 身法 (速度) Agility / AGI, 运气 Luck, 生命 HP (生命上限 Max HP), 真气 MP
(真气上限 Max MP), 回合 turns, 全体/单体 all / one, 毒乱封眠 Poison / Confuse / Silence / Sleep. **内力 is not MP**:
it is a script-kept 0-100 pool (meditate to refill; pays for teleports, Dreamscape, gathering, recruiting, healing):
write "qi". 潜能 potential, 实战经验 battle exp, 经验(值) EXP, 声望 fame, 资质 talent, 精元 essence. Money: 元
and RMB are the same joke currency, "RMB" (1W = 10K, 5W = 50K, 200W = 2M); 两 "taels" where the text says 两;
英雄币 "hero coins".

## Decisions

1. **Game title**: 英雄坛说 = "Heroes' Altar" (games.py `title_en`); 英雄坛 in the intro = "the Heroes' Altar".
2. **Main menu 魔法 stays "Magic"** (not jy's "Arts"). jy changed it because every jy MRS is a martial art. Here
   the core of the MRS list is elemental magic (each hero's fire / wind / earth mentor, thunder for Yuxin, water
   books), the scripts themselves call it 魔法 (starter pack 低级魔法, "a book of spells recording 魔法",
   黑魔法 for Demonwing) and the descriptions say 法术 "spell". The engine row ENG/13891.1 is unchanged.
3. **Heroes**: 独孤圣 Dugu Sheng, 欧阳剑 Ouyang Jian, 唐静 Tang Jing. All fit the 11-char ARS field in full. All three
   are boys in every script (少年, 小伙子, 小子); 唐静 is "he". The 1-1-1 menu shows surnames (Dugu / Ouyang / Tang).
4. **Party girls**: 陈雨馨 Yuxin, 赵冰雁 Bingyan in the ARS field (Zhao Bingyan is 12; Chen Yuxin follows for
   symmetry); full names when they introduce themselves.
5. **Long names in 11-char fields**: `short` = given name, or the recognisable half (R. Butler, Shiranui, Leopard).
6. **Battle names do not match the story** (see the inconsistencies table): the six sect heads, the possessed Gu
   Yanwu, the Demon Guard and the Archdemon all fight through unrelated monster records (Peddler, Ping Yizhi,
   Hawker, Jose, Ximen Guang, Mystery Man, Li Yebai, Jubei, Elder Fang, Retainer, Quarry Boss). Translate each
   record by its own name, as jy did; not fixable in text.
7. **Placeholder and label names are kept**: ARS 3-2-1..52 "001".."052" (NPC names are never shown), 3-4-x
   "b001".."b010" (scene objects), and the battle-visible placeholders "xxxx" / "xxxx2" (Demonspire enemies).
8. **Currency**: 元 and RMB = "RMB"; 两 = "taels" where written; the engine's battle reward " gold" (ENG/2fae0,
   fmj) is left as it is.
9. **令牌**: "token" in dialogue, "Tag" in the six item names (10-char limit).
10. **符 = Ward, 令 = Writ** in item names (10-char limit); the stat boosters are Power / Guard / Speed / Soul / Luck
    Writ and HP / MP Ward; pills HP Pill / MP Pill (真气 is MP; 内力 is qi).
11. **Ores by purity** (Gold 90% ...), **metal swords as -fang**, **Hexblade+N** for the purified sword.
12. **Parody names follow the joke** (see Conventions); 吸腥大法 (a pun on 吸星大法 "Star-Sucking Art") = "Leech
    Art", 北冥神功 = "Beiming" (the description itself says "everyone knows what it does").
13. **Typos are fixed silently** in English (table below); deliberate puns are kept.
14. **Menus**: no spaces inside items; one-word forms or hyphens (see Conventions).
15. **The credits and the end note** are translated as written: "about to start my second year of senior high"
    (马上升高二); 健康游戏忠告 = "Healthy Gaming Advice" (the official 2004 Chinese anti-addiction notice).

## Inconsistencies and typos found in the source

| source | where | glossary / fix |
|---|---|---|
| 玉女峰1号\xb7 | MAP 2-3-17 | the 12-byte field cut 房 (GBK B7 BF) in half: 玉女峰1号房 "Jade Room 1" (glossary row keyed by `source_ids`) |
| `\x0d` (CR) inside dialogue | 1-7-6@0258, 1-7-6@03d3, 1-10-1@0881, 1-10-1@08ac, 1-10-1@08d0, 1-255-30@002b | drop it; let the text wrap |
| 吸腥大法 | GRS 6-14-9, MRS 4-1-34, 1-9-4 | pun/typo for 吸星大法; "Leech Art" |
| 李青照 | MRS 4-1-31 desc | 李清照 Li Qingzhao |
| 朱元彰 | MRS 4-1-16 desc | 朱元璋 Zhu Yuanzhang |
| 白玉萧 | GRS 6-7-13 | 萧 for 箫 (flute) |
| 鬼头标 / 飞鬼标 / 灵鬼标, "一种鬼常带的标" | GRS 6-8-3..5 | 标 for 镖 (dart) |
| 冰心决 | MRS 4-2-5 | 决 for 诀 |
| 后起之绣 | 1-0-8 | 后起之秀 "Rising Star" |
| 童嫂无欺 | 1-1-14 | 童叟无欺 "honest prices for young and old" |
| 关与俱乐部 | 1-7-6, 1-10-1 | 关于 |
| 急燥 | 1-0-8 | 急躁 |
| 那个高人 | MRS 4-1-34 desc | 哪个 |
| 是敌人难以击中 | MRS 4-2-6 desc | 使 |
| 凌历 | MRS 4-1-33 desc | 凌厉 |
| 由余烟尘遮挡 | MRS 4-1-23 desc | 由于 |
| 一招半试 | 1-0-9 | 一招半式 |
| 我们两 | 1-1-18, 1-255-32 | 我们俩 |
| 在虚无的空间了飘来飘去 | 1-1-17 | 里 |
| 你拥有师门点 | 1-0-7@078b | leftover in the potential ladder: "potential" like its neighbours |
| 潜能 ladder skips "一百多点" | 1-0-7 | translate what is there |
| 花彩神布 vs 五彩神布 | GRS 6-14-41 / 1-11-2 | same item: Prism Silk |
| 猪肉 vs 狗肉 | GRS 6-9-5 desc, 1-0-9 quest log, 1-1-8 | the Matron asks for Pork; the log says dog meat, the description "from a pig: dog meat". Keep the description joke, make the quest log say Pork |
| 青铜矿 / 玄铁矿 vs 铜矿 / 铁矿 | 1-4-1 smiths vs GRS 6-14-19..24 | Copper / Iron ore (Bronzefang / Ironfang need them) |
| 镇妖塔 vs 锁妖塔 | GRS 6-7-28 desc | both Demonspire |
| 镇西郊 / 镇东郊 vs 村东郊 | MAP 2-1-1/6 vs banner 1-2-8 | town vs village: West Wilds / East Wilds |
| 披风拳法 described as a staff art | MRS 4-1-17 | name "Wind Fist"; the description may say "this art" |
| 雷动九天 has two records | MRS 4-1-27 (thunder attack) and 4-2-4 (buff; its description is about a Red Lotus move) | same English "Sky Quake" |
| 门派内功 twice | MRS 4-3-6 / 4-3-7 | same English "Sect Qi" |
| 门派武功X/Y/Z, "单体敌人X伤害" | MRS 4-1-36..38 | placeholders: "Sect Art X", "X damage to one enemy" |
| MRS descriptions cut at the 86-byte field (故若非万不得, 在烟幕散去之前对手的攻击, 当真抵得过一件上, 触景而创) | MRS 4-1-18, 4-1-23, 4-2-5, 4-1-31 | finish the sentence briefly in English |
| 1-255-8 menu 陈雨馨 / 赵冰雁 | both branches `learnmagic 4` | Demonwing always goes to Yuxin (script bug); translate the menu as written |
| `say 1` once for "多谢巡捕" and "靠!打八折吧!" | 1-1-17, 1-4-1 | shows Dugu Sheng's portrait whoever the hero is; translate as the hero |
| 小KS | 1-4-3 | 小case: "Piece of cake" |
| 1-10-7 "由于是试玩版" | Demonspire | demo leftover: "Since this is the demo version, we'll send you straight to floor 1!" |
| ARS reused in fights | 李清照 110, 白瑞德 115, 余鸿儒 113, 清虚道长 114, 王维扬 111, 和仲阳 112, possessed 顾炎武 102, 恶魔守卫 30, Archdemon 75 / 83 / 4, tigers 7, Lone Bandit and SSK's guards 50, Bingyan 23 | battle names will not match the story; not fixable in text |
| 伏魔记 template leftovers | no fmj characters survive (NPC records are renumbered "001".."052"); 19 generic names are identical to fmj's (发带 头巾 披风 匕首 长剑 玄铁剑 风咒 飞岩术 雷咒 冰咒 天罡战气 冰心决 净衣咒 小蛇 小狗 通用山洞 村长家 药店 当铺) | reuse the fmj English where it fits today's limits (Hair Band, Headscarf, Cape, Dagger, Long Sword, Wind Spell, Ice Spell, Icy Heart, Small Snake, Puppy, Cave, Herb Shop, Pawnshop); fmj's Thunder Spell, Flying Rocks, Heavenly War Qi, Purify Spell, Elder's House are over the 11/12-char limits used now, and 玄铁剑 joins the -fang set |
| GBK (traditional) names | none (only the cut 房 above) | - |

## Counts

| category | terms |
|---|---|
| person | 72 |
| title | 18 |
| sect | 8 |
| place | 69 |
| monster | 107 |
| weapon | 46 |
| armor | 48 |
| consumable | 34 |
| item | 48 |
| magic | 53 |
| skill | 21 |
| other | 88 |
| ui | 100 |
| **total** | **712** |


## People and speakers

| zh | en | short | alt | note |
|---|---|---|---|---|
| 独孤圣 | Dugu Sheng |  |  | Hero choice 1 (1-1-1 menu; var 0 = 1, actor 1). Fire element: starts with Fire 25 (var 38) and only he can learn the Snowpeak fire mentor's four arts. Never named in dialogue. Menu 1-1-1 has no room for spaces: use the surnames 'Dugu Ouyang Tang'. [ARS/3-1-1] |
| 欧阳剑 | Ouyang Jian |  |  | Hero choice 2 (var 0 = 2, actor 2). Wind element (var 35); Snowpeak wind mentor. Fits 11 exactly. [ARS/3-1-2] |
| 唐静 | Tang Jing |  |  | Hero choice 3 (var 0 = 3, actor 3). Earth element (var 36); Snowpeak earth mentor. The name could be a girl's, but every script treats the hero as a 14-year-old boy (少年, 小伙子, 小子): 'he'. [ARS/3-1-3] |
| 陈雨馨 | Yuxin |  | Chen Yuxin | First party member (actor 4, portrait pic=4), joins in Gu Yanwu's house (1-1-18) after the possessed Gu Yanwu is beaten; orphan, knows martial arts, teaches the Lingbo Step; bossy and cute ('本女侠' = 'yours truly'). The thunder teacher in Shang Fort (1-7-7) teaches only her ('Miss Chen'). Given name in the party field to match Bingyan; full name when she introduces herself. [ARS/3-1-4] |
| 赵冰雁 | Bingyan |  | Zhao Bingyan | Second party member (actor 5, pic=5), found asleep in your own sect's rooms (1-11-2): a girl from the hero's real world who sneaked into his time machine. Snappy ('滚!'), knows the family secret of equipment forging. Zhao Bingyan (12) is over the 11-char ARS field, so the field uses the given name. [ARS/3-1-5] |
| 柴梓 | Chai Zi |  |  | The game's adapter (credits: 游戏改编) playing himself: guide, prankster and fourth-wall commentator ('柴梓:靠,系统你也敢耍?'). Gives the Sect Codex in 1-1-20, rescues the hero from the Archdemon, is locked in the Demonspire, dies there and returns as a ghost in the final battle; in the good ending the hero wakes up in the future 'renamed Chai Zi'. Also 'current moderator of the BBK Club RPG board'. Casual net-slang voice. |
| 小神童 | Prodigy |  | Little Prodigy | Kid who greets the hero in 1-1-20 claiming to be 'the adapter of this game' before Chai Zi shoves him aside ('敢抢我台词!'). Probably the designer's handle. Also names 神童乐园 / 神童居. [ARS/3-2-53] |
| 金远见 | Jin Yuanjian |  |  | Game designer (credits 1-0-1, 游戏设计). |
| 顾炎武 | Gu Yanwu |  |  | The real Ming-Qing scholar, here Safehaven's village schoolmaster (lessons 180 taels, level-ups for 2000 RMB + 20K EXP, sells the Dream Cape, pays the Matron's quest rewards). Possessed by the Archdemon: he kidnaps Yuxin into his house (1-1-18), 'a hypocrite' (伪君子). [ARS/3-3-100] |
| 潘小莲 | Pan Xiaolian | Xiaolian |  | Tofu-shop widow 'past thirty but still charming; plenty of men want to eat her tofu' (吃豆腐 = flirt with): parody of 潘金莲 Pan Jinlian. Keep the tofu double meaning. 12 chars: ARS uses short 'Xiaolian'. [ARS/3-3-95] |
| 西门庆 | Ximen Qing |  |  | Named in the 绿水罗衣 description (Pan Jinlian's lover in Water Margin). |
| 西门广 | Ximen Guang |  |  | Townsman (ARS only), parody of Ximen Qing. [ARS/3-3-111] |
| 胡屠户 | Butcher Hu |  |  | Safehaven butcher (1-1-16) whose meat went missing; from 儒林外史. Brags 'without me you'd all eat hairy pork'. [ARS/3-3-121] |
| 李清照 | Li Qingzhao |  |  | The Song poetess, here head of the Flower Sect on Jade Peak (1-3-5, female). Boss line '滚!' ('Get lost!'). Written 李青照 in the 花簇鞭法 description (typo). Her fight uses ARS 110 (Peddler). |
| 李青照 | Li Qingzhao |  |  | Typo for 李清照 in MRS 4-1-31 description. |
| 白瑞德 | Rhett Butler | R. Butler |  | Snow Sect head on Snowpeak (1-4-3, male). 白瑞德 is the Chinese name of Rhett Butler (Gone with the Wind): keep the joke. 12 chars: ARS short 'R. Butler'. His fight uses ARS 115 (Ping Yizhi). [ARS/3-3-18] |
| 余鸿儒 | Yu Hongru |  |  | Red Lotus Sect head on Mt. Wuzhi (1-5-4); the script says 她: female. Fight uses ARS 113 (Hawker). [ARS/3-3-80] |
| 清虚道长 | Taoist Qingxu | Qingxu | Master Qingxu | Wudang Sect head (1-6-5). 13 chars: ARS short 'Qingxu'. Fight uses ARS 114 (Jose). [ARS/3-3-47] |
| 王维扬 | Wang Weiyang | Weiyang |  | Bagua Sect head at Shang Fort (1-7-8); from 书剑恩仇录 (Zhenyuan Escort, Bagua school). 12 chars: ARS short 'Weiyang'. Fight uses ARS 111 (Ximen Guang). [ARS/3-3-93] |
| 和仲阳 | He Zhongyang | Zhongyang |  | Iga Valley head on Icefire Isle (1-8-6). 12 chars: ARS short 'Zhongyang'. Fight uses ARS 112 (Mystery Man). [ARS/3-3-36] |
| 逍遥 | Xiaoyao |  |  | BBK Club's former RPG-board moderator (1-10-1, Prodigy Park): Chinese Paladin fan who sings 逍遥叹 lyrics, says 'YES' and runs off ('886'). Lost the Love Ring; knows where the club treasure is. Handle, also Li Xiaoyao's name: keep pinyin. |
| 邓世禹 | Deng Shiyu |  |  | Greedy information broker at Shang Fort (1-7-6): charges 1000/10000 RMB per answer, 'no discounts', then admits he knows nothing. 'Deng' in '姓邓的那小子'. |
| SSK | SSK |  |  | BBK Club 'super moderator' (超级斑竹) on Jade Peak (1-3-6): can edit his money ('flows like water'), refuses the antidote out of spite, fights, gets a stomach ache. Keep the handle as is. |
| 爱情没心跳 | Flatline Love |  |  | Forum handle (1-5-5, Wuzhi Cave): preaches about love; co-invented the antidote with SSK. 'Love without a heartbeat' -> Flatline Love. |
| 泡泡友 | Bubble Pal |  |  | Forum-handle cameo (1-6-2, Mt. Wudang): sells an 'immortality elixir' (arsenic, bezoar, horse dung...) that poisons Yuxin with Demon Powder. |
| 亮 | Liang |  |  | Handle cameo on Snowpeak (1-4-3): sends you to kill beasts and skin a tiger, then runs ('886'). |
| 陈骁 | Chen Xiao |  |  | Wizard on Snowpeak (1-4-1) who turned a man into the Beast; choice 'trust the Beast / trust Chen Xiao'. |
| 红桃K | King of Hearts |  |  | '赌圣' gambler in your sect rooms (1-11-2): bets money, potential, EXP and stats. |
| 闻世先生 | Mr. Wenshi |  | Sage Wenshi | All-knowing hermit 'who vanished from the martial world 60 years ago' (1-9-4): appraises your stats for 100 taels, gives the four rare books. Calls the hero 小子. [ARS/3-3-3] |
| 道德和尚 | Monk Daode |  |  | Kindly monk ('色即是空'); the Elder's errand 'visit Monk Daode'. [ARS/3-3-1] |
| 老婆婆 | Granny |  |  | Safehaven old woman: chores (sweep, fetch water, chop wood -> rhyming work songs, 1-1-19) and the candied-haws swap. [ARS/3-3-98] |
| 老裁缝 | Old Tailor |  |  | Needs his Spectacles (老花镜); gives a Fine Robe. [ARS/3-3-97] |
| 小裁缝 | Tailor Boy |  | Young Tailor | Apprentice tailor ('客官，买件衣服吧'). [ARS/3-3-96] |
| 小顽童 | Urchin |  |  | Kid who found 'a shiny thing that makes my head spin'. [ARS/3-3-99] |
| 小书童 | Page Boy |  |  | Gu Yanwu's study boy; lost his Brush. [ARS/3-3-101] |
| 中年妇人 | Matron |  | Middle-aged Woman | Gives fetch quests in humble 妾身 'I'; rewards at Gu Yanwu's. Quest menu label 中年妇人任务. [ARS/3-3-104] |
| 村长 | Elder |  | Village Head | Safehaven's head (fmj: 村长 = Elder): errand chain (wine, letter to the Inspector, visit X...). Uses 老夫. [ARS/3-3-105] |
| 巡捕 | Inspector |  |  | Yamen officer; receives the Elder's letter, reveals the demon in Prodigy Park, teaches a secret move. [ARS/3-3-108] |
| 捕快 | Constable |  |  | [ARS/3-3-107] |
| 官兵 | Soldier |  |  | Yamen soldier (1-1-17) who teleports the party to the Demonspire for 50K RMB, or for free if Yuxin threatens him (then he steals your qi and money). [ARS/3-3-106] |
| 平一指 | Ping Yizhi |  |  | Physician (笑傲江湖), an errand target. Also the ARS used for Rhett Butler's fight. [ARS/3-3-115] |
| 何铁手 | He Tieshou |  | Iron Hand He | Errand target (碧血剑). [ARS/3-3-116] |
| 石料管事 | Quarry Boss |  |  | Errand target. [ARS/3-3-4] |
| 独脚大盗 | Lone Bandit |  |  | 独脚大盗 is an idiom for a lone-wolf robber (not 'one-legged'). Cave 1 (1-2-2): '小子,俺就是独脚大盗!'. Errand target. [ARS/3-3-5] |
| 厨师 | Cook |  |  | [ARS/3-3-119] |
| 店小二 | Waiter |  |  | [ARS/3-3-118] |
| 挑夫 | Porter |  |  | [ARS/3-3-120] |
| 盐商 | Salt Trader |  |  | [ARS/3-3-122] |
| 卖花妞 | Flower Girl |  |  | '客官,买朵花吧.' [ARS/3-3-109] |
| 小商贩 | Peddler |  |  | Also the ARS used for Li Qingzhao's fight. [ARS/3-3-110] |
| 杂货贩 | Hawker |  |  | Sundries seller. Also the ARS for Yu Hongru's fight. [ARS/3-3-113] |
| 神秘人 | Mystery Man |  |  | Also the ARS for He Zhongyang's fight. [ARS/3-3-112] |
| 荷西 | Jose |  |  | José (Sanmao's husband), ASCII 'Jose'. ARS for Taoist Qingxu's fight. [ARS/3-3-114] |
| 葛朗台 | Grandet |  |  | Balzac's miser (Eugenie Grandet). [ARS/3-3-117] |
| 李也白 | Li Yebai |  |  | Parody of Li Bai ('Li Also-Bai'). ARS used for the possessed Gu Yanwu fight. [ARS/3-3-102] |
| 茶花女 | Camille |  |  | 茶花女 = La Dame aux Camelias (Camille). [ARS/3-3-59] |
| 独行大侠 | Lone Hero |  |  | [ARS/3-3-103] |
| 民团团丁 | Militiaman |  |  | Town watchman ('looks about 30, novice, light hands'). [ARS/3-3-2] |
| 小红 | Xiaohong |  |  | [ARS/3-3-58] |
| 天才装备打造员 | Genius Smith |  |  | Two Snowpeak smiths ('天才装备打造员1/2') forging the gold/silver and bronze/iron swords: 'Genius Smith 1/2'. |
| 宝藏守护神 | Treasure Guardian |  |  | Speaks gibberish (1-10-1). |
| 黄泉守卫 | Nether Guard |  | Guard of the Yellow Springs | Appears when you hang yourself in West Wilds ('Want to go to the underworld? 2000 toll!'); also the Nether 1 ferryman/teleporter (1-10-3). |
| 恶魔守卫 | Demon Guard |  |  | Demon Cave guard (1-10-2): 'I'm not the Archdemon, I'm just training to be a demon'. Drops the Fly Card. His fight uses ARS 30 (Jubei). |
| 天妖皇 | Fiend Emperor |  |  | Demo-version leftover in 1-10-7 ('the Demonspire's true master'); the next line says the demo sends you straight to floor 1. |
| 幻境守护神 | Dream Guardian |  |  | Dreamscape gatekeepers 1-5 (1-11-3): 'all level-N monsters here; challenge?'. 幻境BOSS = 'Dream Boss'. |
| 幻影守护者 | Dream Keeper |  |  | Taunts you when you refuse (1-11-3). |
| 魔剑魂灵 | Hexblade Spirit |  |  | Moans when the two swords are fused (1-255-6); 镇妖剑魂灵 = 'Quellblade Spirit'. |
| 大恶魔 | Archdemon |  | the Great Demon | Main villain: came through the time machine with the hero, controls the six sects; revealed (1-255-32) as the evil in the hero's own heart ('kill me and you kill yourself'). Same English for 大魔头 and 黑魔头. His fights use ARS 75 / 83 / 4 (Elder Fang, Retainer, Quarry Boss). |
| 大魔头 | Archdemon |  | archfiend | Chai Zi's word for the same villain (1-1-20, 1-1-3). |
| 魔王 | Demon King |  | Archdemon | 1-255-32 messages ('魔王使出大绝招'): the Archdemon. |
| 我是谁 | Who Am I |  |  | The Archdemon's speaker tag in the final battle (1-1-17): literally 'who am I' (he is the hero's other half). Tag 'Who Am I:'. |
| 朱元彰 | Zhu Yuanzhang |  |  | Ming founder (typo for 朱元璋) in the Taizu Fist description. |

## Titles and forms of address

| zh | en | short | alt | note |
|---|---|---|---|---|
| 掌门 | Sect Head |  |  | Head of a sect (the six bosses); your disciples greet you '掌门好!' ('Welcome, Master!'). |
| 大侠 | hero |  |  | 一代大侠 fame rank 'Great Hero'. |
| 少侠 | young hero |  |  | Chen Xiao to the hero; fame rank 正义少侠 'Righteous Hero'. |
| 小侠 | young hero |  |  | Yamen clerk to the hero. |
| 女侠 | heroine |  |  | Soldier to Yuxin; 本女侠 = Yuxin's 'yours truly'. |
| 客官 | sir |  |  | Shopkeepers. |
| 姑娘 | Miss |  |  |  |
| 小伙子 | lad |  | young man | The Elder and the magic-book hermit to the hero. |
| 前辈 | sir |  | elder | Hero to Mr. Wenshi. |
| 长老 | Elder |  |  | Red Lotus elders (方长老 Elder Fang, 韩长老 Elder Han). |
| 道长 | Taoist |  | Master Taoist | 清虚道长 / 古松道长: 'Taoist Qingxu', 'Taoist Gusong' (fmj: 道人 = Taoist X). |
| 斑竹 | moderator |  | mod | Net pun on 版主 (board moderator). 超级斑竹 'super moderator', 前任/现任斑竹 'former/current moderator'. |
| 导师 | mentor |  |  | '你好,我是欧阳剑导师' = 'I'm Ouyang Jian's mentor' (each hero's element teacher on Snowpeak). |
| 赌圣 | God of Gamblers |  | Gambling Saint | 红桃K's title. |
| 老夫 | I |  | this old man | The Elder's self-reference; plain 'I'. |
| 妾身 | I |  |  | The Matron's humble self-reference; plain 'I' with polite tone. |
| 老身 | I |  |  | Granny's self-reference. |
| 小子 | kid |  | boy; punk | How bosses, villains and Mr. Wenshi address the hero. |

## Sects and groups

| zh | en | short | alt | note |
|---|---|---|---|---|
| 花间派 | Flower Sect |  | Huajian Sect | Li Qingzhao's sect on Jade Peak; pun on the 花间 school of ci poetry. Whip arts (Myriad Lash, Ice Lash, Bloom Whip). Token menu item '花间' = 'Flower'. |
| 伊贺谷 | Iga Valley |  |  | Ninja clan (Japanese 伊賀) on Icefire Isle, head He Zhongyang; its members are game/anime parodies (Jubei, Fujiomaru, Ukyo...). Menu '伊贺' = 'Iga'. |
| 雪山派 | Snow Sect |  | Snowy Mountain Sect | Rhett Butler's sect on Snowpeak (name and the 万/千 member names parody 侠客行's Snowy Mountain Sect). Menu '雪山' = 'Snow'. |
| 红莲派 | Red Lotus Sect |  | Red Lotus Cult | Yu Hongru's sect on Mt. Wuzhi (also 红莲教 in MRS descriptions; members 黑衣/红衣/蓝衣教众). Menu '红莲' = 'Lotus'. |
| 红莲教 | Red Lotus Sect |  | Red Lotus Cult | MRS descriptions (披风拳法, 雷动九天). Same sect as 红莲派. |
| 白莲教 | White Lotus Sect |  |  | Taizu Fist description (Zhu Yuanzhang 'was a White Lotus man'). |
| 武当派 | Wudang Sect |  |  | Taoist Qingxu's sect on Mt. Wudang. Menu '武当' = 'Wudang'. |
| 八卦派 | Bagua Sect |  | Eight Trigrams Sect | Wang Weiyang's sect at Shang Fort. Menu '八卦' = 'Bagua'. |

## Places

| zh | en | short | alt | note |
|---|---|---|---|---|
| 平安镇 | Safehaven |  | Ping'an Town | The starting town (中原偏西, 'west of the Central Plains'). Meaningful invented name translated (fmj rule: Heartsease, Whitewater). One word: fits map, banner and the teleport menus. 平安小镇 in the intro = Safehaven too. [MAP/2-2-1] |
| 平安小镇 | Safehaven |  |  | Intro scroll ('this place was called Safehaven'). |
| 镇西郊 | West Wilds |  | West Outskirts | Wild map west of town: the hanging tree, the Nether Guard, a stone-and-cloth equipment maker. [MAP/2-1-1] |
| 镇东郊 | East Wilds |  | East Outskirts | [MAP/2-1-6] |
| 村东郊 | East Wilds |  |  | Banner of the same map (source says 村 'village' here, 镇 'town' in the map name). |
| 香山 | Mt. Xiang |  | Fragrant Hills | [MAP/2-1-2] |
| 极恶洞 | Vile Cave |  | Cave of Utmost Evil | Banner of 1-2-7. |
| 极恶洞岔道 | Vile Fork |  | Vile Cave Fork | [MAP/2-1-5] |
| 山洞1 | Cave 1 |  |  | Lone Bandit's cave (1-2-2). |
| 山洞2 | Cave 2 |  |  |  |
| 通用山洞 | Cave |  |  | Dev label 'general-purpose cave'. [MAP/2-1-9] |
| 玉女峰 | Jade Peak |  | Jade Maiden Peak | Flower Sect seat (Li Qingzhao), SSK's room. Menu 'Jade'. [MAP/2-2-6] |
| 玉女峰入口 | Jade Gate |  | Jade Peak Entrance | fmj: 入口 = 'X Gate'. [MAP/2-1-4] |
| 玉女峰后院 | Jade Yard |  |  | 后院 = 'Yard'. [MAP/2-2-7] |
| 玉女峰1号房 | Jade Room 1 |  |  | Map 2-3-17 is stored as '玉女峰1号\xb7': the 12-byte field cut 房 (GBK B7BF) in half. SSK's room (1-3-6). |
| 玉女峰1楼 | Jade Hall 1F |  |  | [MAP/2-3-18] |
| 玉女峰后楼 | Jade Annex |  |  | [MAP/2-3-20] |
| 雪山入口 | Snow Gate |  |  | [MAP/2-1-3] |
| 大雪山 | Snowpeak |  | Great Snow Mountain | Snow Sect seat (Rhett Butler); also the three element mentors, two Genius Smiths, the leopard-skin seller, Chen Xiao and the Beast. Menu 'Snowpeak'. [MAP/2-2-13] |
| 大雪山后山 | Snow Ridge |  |  | 后山 = 'Ridge'. [MAP/2-2-14] |
| 五指山 | Mt. Wuzhi |  | Five Finger Mountain | Red Lotus seat (Yu Hongru). Menu 'Wuzhi'. [MAP/2-2-8] |
| 五指山洞 | Wuzhi Cave |  |  | Flatline Love (1-5-5). [MAP/2-3-21] |
| 冰火岛 | Icefire Isle | Icefire | Ice and Fire Island | Iga Valley seat (He Zhongyang); island from 倚天屠龙记. Map name fits 12; the 10-char banner uses short 'Icefire'. Menu 'Icefire'. [MAP/2-2-9] |
| 冰火岛入口 | Icefire Gate | Isle Gate |  | Map name fits 12; banner (1-2-11) uses short 'Isle Gate'. [MAP/2-1-8] |
| 冰火岛后院 | Icefire Yard |  |  | [MAP/2-2-10] |
| 武当山 | Mt. Wudang |  |  | Wudang Sect seat (Taoist Qingxu); Bubble Pal; stone/cloth gathering. Menu 'Wudang'. [MAP/2-2-11] |
| 武当后山 | Wudang Ridge |  |  | [MAP/2-2-12] |
| 商家堡 | Shang Fort |  | Shang Family Fort | Bagua Sect seat (Wang Weiyang), from 飞狐外传; Deng Shiyu; the thunder teacher. Menu 'Shang'. [MAP/2-2-4] |
| 商家堡入口 | Shang Gate |  |  | [MAP/2-1-7] |
| 商家堡后花 | Shang Garden |  |  | Truncated 后花园 (back garden). [MAP/2-2-5] |
| 商家堡后房 | Shang Rooms |  |  | [MAP/2-3-15] |
| 神童乐园 | Prodigy Park |  |  | Where the Inspector says a great demon lives in the Hundred Flowers Array (1-10-1): rotating-gate puzzle, the Beast, Xiaoyao and the club treasure. Menu 'Prodigy'. [MAP/2-2-15] |
| 神童居 | Prodigy Home |  |  | [MAP/2-3-16] |
| 我的门派 | My Sect |  |  | The player's own sect HQ (after founding one); Bingyan and the King of Hearts are in its rooms (1-11-2). Menu 'Sect'. [MAP/2-1-11] |
| 商业街 | Market Row |  |  | Safehaven's shop street. [MAP/2-2-2] |
| 衙门 | Yamen |  | magistrate's office | Inspector, Constable, Soldier; bandit bounties; the teleport to the Demonspire. [MAP/2-2-3] |
| 通用小地图 | Room |  |  | Dev label 'general small map' (interior used for many scenes). [MAP/2-3-1] |
| 通用1楼 | Ground Floor |  |  | Dev label 'general 1st floor'. [MAP/2-3-22] |
| 英雄家 | Hero's Home |  |  | The hero's house with the time machine (1-1-3: bed, token slots). [MAP/2-3-2] |
| 豆腐店 | Tofu Shop |  |  | Pan Xiaolian's. [MAP/2-3-3] |
| 裁缝店 | Tailor Shop |  |  | [MAP/2-3-4] |
| 婆婆家 | Granny's |  | Granny's House | [MAP/2-3-5] |
| 婆婆家地下 | Cellar |  | Granny's Cellar | [MAP/2-3-14] |
| 顾炎武家 | Gu's Home |  | Gu Yanwu's House | Where Yuxin is held (1-1-18). [MAP/2-3-6] |
| 村长家 | Elder's Home |  |  | [MAP/2-3-7] |
| 商店 | Shop |  |  | [MAP/2-3-8] |
| 药店 | Herb Shop |  |  | fmj. [MAP/2-3-9] |
| 兵器铺 | Weapon Shop |  |  | [MAP/2-3-10] |
| 当铺 | Pawnshop |  |  | '高价收购，童嫂无欺' (sic, 童叟无欺). [MAP/2-3-11] |
| 客栈1楼 | Inn 1F |  |  | [MAP/2-3-12] |
| 客栈2楼 | Inn 2F |  |  | [MAP/2-3-13] |
| 恶魔洞 | Demon Cave |  |  | The Archdemon's lair (dialogue). |
| 恶魔洞一层 | Demon Cave |  | Demon Cave 1F | Banner of 1-10-2; 一层 'first floor' dropped (only one floor exists, and 'Demon Cave 1' is 12). |
| 锁妖塔 | Demonspire |  | Demon-Locking Tower | Where Chai Zi is imprisoned (1-12-1: 88 Body Parts open the way down) and the final battle is fought. One word fits the 10-char banner. Also a nod to Chinese Paladin's tower. |
| 镇妖塔 | Demonspire |  |  | Quellblade description ('a sword from atop the 镇妖塔'): same tower as 锁妖塔. |
| 阴间 | the Nether |  | the underworld | Reached by hanging yourself (West Wilds); Nether Guard sells passage. 阴间1层/2层 = 'Nether 1/2'. |
| 阴间1层 | Nether 1 |  |  | Banner 1-10-3; also a teleport choice. |
| 阴间2层 | Nether 2 |  |  | Banner 1-10-4; choice in 1-10-3. |
| 黄泉 | the Yellow Springs |  |  | Underworld (only in 黄泉守卫 'Nether Guard'). |
| 矿山1 | Mine 1 |  |  | Banner 1-10-5; Mine Imps. |
| 矿山2 | Mine 2 |  |  |  |
| 幻境 | Dreamscape |  | Illusion Realm | Training realm (1-11-3, entered from 1-0-8 with the Dream Cape, 10000 RMB and 50 qi): double EXP, no saving. |
| 幻影 | Dreamscape |  |  | 1-0-8 '在幻影里无法存档' and 幻影守护者: same realm. |
| 百花阵 | Hundred Flowers Array |  |  | In Prodigy Park (Inspector). 百花毒阵 = 'Hundred Flowers Poison Array' (1-10-1). |
| 百花谷 | Hundred Flower Valley |  |  | Li Qingzhao's retreat (MRS 4-1-31 desc). |
| 英雄坛 | Heroes' Altar |  |  | Title. 远古大陆英雄坛 = 'the Heroes' Altar of the ancient continent' (intro scroll). |
| 中原 | the Central Plains |  |  | Intro scroll. |
| 现实世界 | the real world |  |  | Quest log: the full version's quest is to return to the real world. |
| 未来世界 | the future |  | the future world | Good ending: 'you returned to the future, now named Chai Zi'. |

## Enemies and ARS-only names

| zh | en | short | alt | note |
|---|---|---|---|---|
| 怪兽 | Beast |  | Monster | 1-4-1: a man turned into a beast by Chen Xiao (speaks gibberish, then human speech); 1-10-1: the Prodigy Park boss ('小锣锣们上!'). [ARS/3-3-130] |
| 雪豹 | Snow Leopard | Leopard |  | Snowpeak: sells 'leopard skin... 1500' (his own!). Errand target ('Can it even understand?'). ARS 7 is also used for the tiger fights. 12 chars: ARS short 'Leopard'. [ARS/3-3-7] |
| 黑衣大盗 | Black Thief |  | Black-clad Bandit | [ARS/3-3-6] |
| 欧阳千善 | Ouyang Qianshan | Qianshan |  | Snow Sect member (千 generation; parody of 侠客行's 万 generation). ARS short 'Qianshan'. [ARS/3-3-8] |
| 马千刚 | Ma Qiangang |  |  | Snow Sect. [ARS/3-3-9] |
| 赵千猛 | Zhao Qianmeng | Qianmeng |  | Snow Sect. ARS short 'Qianmeng'. Also the magic-book hermit's fight (1-4-1). [ARS/3-3-10] |
| 薛千柔 | Xue Qianrou |  |  | Snow Sect. [ARS/3-3-11] |
| 花万红 | Hua Wanhong |  |  | Snow Sect (cf. 花万紫). [ARS/3-3-12] |
| 王万轫 | Wang Wanren |  |  | Snow Sect (cf. 王万仞). [ARS/3-3-13] |
| 柯万锺 | Ke Wanzhong |  |  | Snow Sect (锺 = 钟). [ARS/3-3-14] |
| 齐万翼 | Qi Wanyi |  |  | Snow Sect. [ARS/3-3-15] |
| 雪山教头 | Snow Tutor |  | Snow Sect Drillmaster | [ARS/3-3-16] |
| 封万剑 | Feng Wanjian | Wanjian |  | Snow Sect (cf. 封万里). ARS short 'Wanjian'. [ARS/3-3-17] |
| 张福来 | Zhang Fulai |  |  | [ARS/3-3-19] |
| xxxx | xxxx |  |  | Placeholder enemy name, shown in battle in the Demonspire (with xxxx2) and the endless-encounter item: keep as is. [ARS/3-3-20] |
| xxxx2 | xxxx2 |  |  | Placeholder, keep. [ARS/3-3-21] |
| 土匪头子 | Bandit Boss |  | Bandit Chief | Yamen bounty (1-1-17). [ARS/3-3-22] |
| 土匪 | Bandit |  |  | [ARS/3-3-23] |
| 强盗 | Robber |  |  | Yamen bounty; Mt. Wuzhi / Icefire encounters. [ARS/3-3-54] |
| 工地管事 | Foreman |  | Site Foreman | [ARS/3-3-24] |
| 流氓头 | Thug Boss |  |  | [ARS/3-3-25] |
| 流氓 | Thug |  |  | [ARS/3-3-26, 3-3-55] |
| 浪人甲 | Ronin A |  |  | Iga Valley. 甲/乙 = A/B. [ARS/3-3-27] |
| 浪人乙 | Ronin B |  |  | [ARS/3-3-28] |
| 陈美娜 | Chen Meina |  |  | Iga Valley. [ARS/3-3-29] |
| 十兵卫 | Jubei |  | Yagyu Jubei | Iga Valley; Samurai Shodown's Jubei. Also the ARS for the Demon Guard fight. [ARS/3-3-30] |
| 大熊 | Big Bear |  |  | Iga Valley; Demon Cave encounter (maybe a pun on Doraemon's 大雄 Nobita, next to 野比). [ARS/3-3-31] |
| 藤王丸 | Fujiomaru |  |  | Iga Valley; parody of Samurai Shodown's Haohmaru (霸王丸). Demon Cave encounter. [ARS/3-3-32] |
| 未知火舞 | Mai Shiranui | Shiranui |  | Iga Valley; KOF's Mai Shiranui (不知火舞) with 未知 'unknown' for 不知 'not knowing'. 12 chars: ARS short 'Shiranui'. [ARS/3-3-33] |
| 食野太郎 | Kuino Taro |  |  | Iga Valley; Japanese-style parody name (食野 'eat-field'). [ARS/3-3-34] |
| 孙悟莱 | Son Gorai |  | Sun Wulai | Iga Valley; Dragon Ball parody (孙悟空 Son Goku), Japanese reading keeps the joke. [ARS/3-3-35] |
| 枳右京 | Ukyo |  | Karatachi Ukyo | Iga Valley; Samurai Shodown's Ukyo Tachibana (橘右京) with 枳 'trifoliate orange' for 橘 'tangerine'. [ARS/3-3-37] |
| 天津虾 | Tien Shrimp |  |  | Iga Valley; Dragon Ball's Tien Shinhan (天津饭 'Tianjin rice') turned into 'Tianjin shrimp'. [ARS/3-3-38] |
| 野比 | Nobi |  | Nobita | Iga Valley; Doraemon's Nobita Nobi. [ARS/3-3-39] |
| 鬼1 | Ghost 1 |  |  | Nether 1 encounters (1-5 likewise). [ARS/3-3-40] |
| 鬼2 | Ghost 2 |  |  | [ARS/3-3-41] |
| 鬼3 | Ghost 3 |  |  | [ARS/3-3-42] |
| 鬼4 | Ghost 4 |  |  | [ARS/3-3-43] |
| 鬼5 | Ghost 5 |  |  | [ARS/3-3-44] |
| 桃花 | Taohua |  | Peach Blossom | Wudang group (a Taoist girl's name). [ARS/3-3-45] |
| 清风 | Qingfeng |  |  | Wudang acolyte (classic Taoist boy name). [ARS/3-3-46] |
| 烧饭道童 | Kitchen Boy |  | cooking acolyte | Wudang. [ARS/3-3-48] |
| 古松道长 | Taoist Gusong | Gusong |  | Wudang. 13 chars: ARS short 'Gusong'. [ARS/3-3-49] |
| 采花大盗 | Libertine |  | notorious rake | 采花 'flower-picking' = seducing women. ARS 50 is also used for the Lone Bandit fight and SSK's guards. [ARS/3-3-50, 3-3-123] |
| 洞虫 | Cave Worm |  |  | Jade Peak encounters; drops the Bug Ward. [ARS/3-3-51] |
| 大狗 | Big Dog |  |  | Jade Peak. [ARS/3-3-52] |
| 小蛇 | Small Snake |  |  | Jade Peak; drops the Snake Orb (fmj name). [ARS/3-3-53] |
| 怪 | Monster |  |  | Mt. Wuzhi / Icefire encounters. [ARS/3-3-56] |
| 怪2 | Monster 2 |  |  | [ARS/3-3-57] |
| 矿怪1 | Mine Imp 1 |  |  | Mine 1/2 encounters (矿怪1..12; the table order is 1,2,8,3,4..7,9..12). [ARS/3-3-60] |
| 矿怪2 | Mine Imp 2 |  |  | [ARS/3-3-61] |
| 矿怪3 | Mine Imp 3 |  |  | [ARS/3-3-63] |
| 矿怪4 | Mine Imp 4 |  |  | [ARS/3-3-64] |
| 矿怪5 | Mine Imp 5 |  |  | [ARS/3-3-65] |
| 矿怪6 | Mine Imp 6 |  |  | [ARS/3-3-66] |
| 矿怪7 | Mine Imp 7 |  |  | [ARS/3-3-67] |
| 矿怪8 | Mine Imp 8 |  |  | [ARS/3-3-62] |
| 矿怪9 | Mine Imp 9 |  |  | [ARS/3-3-68] |
| 矿怪10 | Mine Imp 10 |  |  | [ARS/3-3-69] |
| 矿怪11 | Mine Imp 11 |  |  | [ARS/3-3-70] |
| 矿怪12 | Mine Imp 12 |  |  | [ARS/3-3-71] |
| 黑衣教众 | Black Robe |  | black-robed cultist | Red Lotus members (红衣 Red Robe, 蓝衣 Blue Robe). [ARS/3-3-72] |
| 红衣教众 | Red Robe |  | red-robed cultist | [ARS/3-3-73] |
| 蓝衣教众 | Blue Robe |  | blue-robed cultist | [ARS/3-3-74] |
| 方长老 | Elder Fang |  |  | Red Lotus. ARS 75 is the Archdemon's fight in 1-255-32. [ARS/3-3-75] |
| 王璁儿 | Wang Cong'er | Cong'er |  | Flower Sect girl. 12 chars: ARS short 'Cong'er'. [ARS/3-3-76] |
| 韩长老 | Elder Han |  |  | Red Lotus. [ARS/3-3-77] |
| 褚红灯 | Chu Hongdeng | Hongdeng |  | Flower Sect. 12 chars: ARS short 'Hongdeng'. [ARS/3-3-78] |
| 唐思儿 | Tang Si'er |  |  | Flower Sect. [ARS/3-3-79] |
| 齐林天 | Qi Lintian |  |  | [ARS/3-3-81] |
| 护院武师 | Manor Guard |  |  | Shang Fort. [ARS/3-3-82] |
| 庄丁 | Retainer |  |  | Shang Fort. ARS 83 is the Archdemon's final-battle record (1-1-17). [ARS/3-3-83] |
| 武师教头 | Drillmaster |  |  | Shang Fort. Also the magic-book hermit's second fight. [ARS/3-3-84] |
| 王剑杰 | Wang Jianjie | Jianjie |  | Wang Weiyang's son (书剑). 12 chars: ARS short 'Jianjie'. [ARS/3-3-85] |
| 王剑英 | Wang Jianying | Jianying |  | Wang Weiyang's son. 13 chars: ARS short 'Jianying'. [ARS/3-3-86] |
| 马行空 | Ma Xingkong |  |  | 飞狐外传 (Shang Fort cast). [ARS/3-3-87] |
| 徐铮 | Xu Zheng |  |  | 飞狐外传. [ARS/3-3-88] |
| 商老太 | Mrs. Shang |  | Old Madam Shang | 飞狐外传. [ARS/3-3-89] |
| 阎基 | Yan Ji |  |  | 飞狐外传. [ARS/3-3-90] |
| 平阿四 | Ping Ah Si |  |  | 飞狐外传; fmj 'Ah X'. [ARS/3-3-91] |
| 商刀鸣 | Shang Daoming | Daoming |  | 飞狐外传's 商剑鸣 with 刀 for 剑. 13 chars: ARS short 'Daoming'. [ARS/3-3-92] |
| 马春花 | Ma Chunhua |  |  | 飞狐外传. [ARS/3-3-94] |
| 商宝震 | Shang Baozhen | Baozhen |  | 飞狐外传. 13 chars: ARS short 'Baozhen'. [ARS/3-3-124] |
| 虫1 | Bug 1 |  |  | Prodigy Park encounters (虫1..4). [ARS/3-3-125] |
| 虫2 | Bug 2 |  |  | [ARS/3-3-126] |
| 虫3 | Bug 3 |  |  | [ARS/3-3-127] |
| 虫4 | Bug 4 |  |  | [ARS/3-3-128] |
| 小狗 | Puppy |  |  | Prodigy Park. [ARS/3-3-129] |
| 猛虎 | Tiger |  | Fierce Tiger | Notice-board challenge 杀死猛虎 'Kill the tiger'; its line '(直译:嗷嗷呜...)' = '(Translation: Awoo awoo...)'. [ARS/3-3-131] |
| 老虎 | Tiger |  |  | Speaker tag (1-4-3). |
| 恶蛟 | Vile Wyrm |  |  | Notice-board challenge (蛟龙 in the dialogue = 'Wyrm', fmj 蛟 = wyrm). [ARS/3-3-132] |
| 蛟龙 | Wyrm |  |  | Speaker tag and 打败蛟龙 'Defeat the wyrm' (1-1-2). |
| 恶棍 | Ruffian |  |  | Notice-board challenge 驱逐恶棍 'Drive out the ruffian'. [ARS/3-3-133] |
| 怪啊1 | Yikes 1 |  |  | Dreamscape monsters 怪啊1..12 ('Monster, ahh!'), paired by level in 1-11-3. [ARS/3-3-134] |
| 怪啊2 | Yikes 2 |  |  | [ARS/3-3-135] |
| 怪啊3 | Yikes 3 |  |  | [ARS/3-3-136] |
| 怪啊4 | Yikes 4 |  |  | [ARS/3-3-137] |
| 怪啊5 | Yikes 5 |  |  | [ARS/3-3-138] |
| 怪啊6 | Yikes 6 |  |  | [ARS/3-3-139] |
| 怪啊7 | Yikes 7 |  |  | [ARS/3-3-140] |
| 怪啊8 | Yikes 8 |  |  | [ARS/3-3-141] |
| 怪啊9 | Yikes 9 |  |  | [ARS/3-3-142] |
| 怪啊10 | Yikes 10 |  |  | [ARS/3-3-143] |
| 怪啊11 | Yikes 11 |  |  | [ARS/3-3-144] |
| 怪啊12 | Yikes 12 |  |  | [ARS/3-3-145] |
| 银行 | Bank |  |  | Pseudo-enemy: the bank system 'fights' it to move money (1-0-8). [ARS/3-3-146] |
| 银行2 | Bank 2 |  |  | [ARS/3-3-147] |

## Weapons

| zh | en | short | alt | note |
|---|---|---|---|---|
| 魔剑 | Hexblade |  | Demon Sword | 'Drank its fill of blood; countless vengeful spirits dwell in it.' Purified up to 9 times with Purestones; fused with the Quellblade into the God-Demon. Short base so the purified forms fit 10. [GRS/6-7-1] |
| 魔剑(净化1) | Hexblade+1 |  | Hexblade (purified 1x) | 净化 = purified. [GRS/6-7-2] |
| 魔剑(净化2) | Hexblade+2 |  | Hexblade (purified 2x) | 净化 = purified. [GRS/6-7-3] |
| 魔剑(净化3) | Hexblade+3 |  | Hexblade (purified 3x) | 净化 = purified. [GRS/6-7-4] |
| 魔剑(净化4) | Hexblade+4 |  | Hexblade (purified 4x) | 净化 = purified. [GRS/6-7-5] |
| 魔剑(净化5) | Hexblade+5 |  | Hexblade (purified 5x) | 净化 = purified. [GRS/6-7-6] |
| 魔剑(净化6) | Hexblade+6 |  | Hexblade (purified 6x) | 净化 = purified. [GRS/6-7-7] |
| 魔剑(净化7) | Hexblade+7 |  | Hexblade (purified 7x) | 净化 = purified. [GRS/6-7-8] |
| 魔剑(净化8) | Hexblade+8 |  | Hexblade (purified 8x) | 净化 = purified. [GRS/6-7-9] |
| 魔剑(净化9) | Hexblade+9 |  | Hexblade (purified 9x) | 净化 = purified. [GRS/6-7-10] |
| 梨花鞭 | Pear Whip |  | Pear Blossom Whip | [GRS/6-7-11] |
| 红拂 | Red Whisk |  |  | Horsetail whisk (also the heroine Hongfu's name). [GRS/6-7-12] |
| 白玉萧 | Jade Flute |  | White Jade Flute | 萧 for 箫 (flute). Hits all enemies. [GRS/6-7-13] |
| 楚妃剑 | Chu Sword |  | Consort of Chu Sword | [GRS/6-7-14] |
| 凝碧剑 | Jade Sword |  | Emerald Sword | [GRS/6-7-15] |
| 细剑 | Rapier |  |  | [GRS/6-7-16] |
| 杀猪刀 | Pigsticker |  | Pig-Butchering Knife | Butcher Hu's reward. 'N厉害' = 'insanely strong'. [GRS/6-7-17] |
| 钢杖 | Steel Rod |  | Steel Staff | [GRS/6-7-18] |
| 匕首 | Dagger |  |  | [GRS/6-7-19] |
| 长鞭 | Long Whip |  |  | [GRS/6-7-20] |
| 檀香扇 | Sandal Fan |  | Sandalwood Fan | [GRS/6-7-21] |
| 护手钩 | Hook Sword |  |  | [GRS/6-7-22] |
| 钓竿 | Fishpole |  | Fishing Rod | 'Junk weapon.' Fishing at the town pond. [GRS/6-7-23] |
| 园丁剪 | Shears |  | Garden Shears | [GRS/6-7-24] |
| 长剑 | Long Sword |  |  | [GRS/6-7-25] |
| 钢刀 | Broadsword |  | Steel Blade | [GRS/6-7-26] |
| 麻绳 | Hemp Rope |  |  | 'Junk weapon, essential for suicide': use it on the West Wilds tree. [GRS/6-7-27] |
| 镇妖剑 | Quellblade |  | Demon-Quelling Sword | Chai Zi's gift in the Demonspire; also forged from ores. [GRS/6-7-28] |
| 神魔剑 | God-Demon |  | God-Demon Sword | Hexblade (purified) + Quellblade fused with a Forgestone (1-255-6). [GRS/6-7-29] |
| 黄金剑 | Goldfang |  | Gold Sword | Genius Smith 1: 10 gold ore. 'Silver Sword' (12) and 'Bronze Sword' (12) do not fit 10, so the four metal swords are one word: Goldfang / Silverfang / Bronzefang / Ironfang. [GRS/6-7-30] |
| 白银剑 | Silverfang |  | Silver Sword | [GRS/6-7-31] |
| 青铜剑 | Bronzefang |  | Bronze Sword | Needs copper ore (铜矿; the smith says 青铜矿). [GRS/6-7-32] |
| 玄铁剑 | Ironfang |  | Dark Iron Sword | 玄铁 = dark iron. [GRS/6-7-33] |
| 毛笔 | Brush |  | Writing Brush | The page boy's. [GRS/6-7-34] |
| 屠龙刀 | Dragonbane |  | Dragon Saber | As jy. [GRS/6-7-35] |
| 割鹿刀 | Deerslayer |  | Deer-Slaying Saber | Gu Long's saber. [GRS/6-7-36] |
| 血饮狂刀 | Bloodlust |  | Blood-Drinking Mad Saber | [GRS/6-7-37] |
| 陨石剑 | Starfall |  | Meteorite Sword | [GRS/6-7-38] |
| 飞镖 | Dart |  |  | Thrown. [GRS/6-8-1] |
| 毒镖 | Venom Dart |  | Poison Dart | [GRS/6-8-2] |
| 鬼头标 | Skull Dart |  | Ghost-Head Dart | 标 for 镖. [GRS/6-8-3] |
| 飞鬼标 | Ghost Dart |  | Flying Ghost Dart | [GRS/6-8-4] |
| 灵鬼标 | Spook Dart |  | Spirit Ghost Dart | [GRS/6-8-5] |
| 无影针 | Unseen Pin |  | Shadowless Needle | [GRS/6-8-6] |
| 飞天石 | Sky Stone |  |  | Thrown 'magic treasure'. [GRS/6-8-7] |
| 恶灵石 | Ghoulstone |  | Evil Spirit Stone | 'Bears a powerful curse.' [GRS/6-8-8] |

## Armour and accessories

| zh | en | short | alt | note |
|---|---|---|---|---|
| 发带 | Hair Band |  |  | 'A band for tying hair (duh, not a belt). Luck+1.' [GRS/6-1-1] |
| 头巾 | Headscarf |  |  | The joke compares it with a sanitary pad (卫生巾): keep a mild equivalent or drop. [GRS/6-1-2] |
| 巨帽子 | Big Hat |  |  | [GRS/6-1-3] |
| 恶魔帽 | Demon Hat |  |  | [GRS/6-1-4] |
| 战神盔 | War Helm |  | War God Helm | [GRS/6-1-5] |
| 龙虫盔 | Dragonbug |  | Dragonbug Helm | 'Everything unknown (Then don't write it!)'. [GRS/6-1-6] |
| 布衣 | Plain Robe |  | cloth clothes | DEF+5; MUD-style NPC look texts say '★带著：布衣' ('Wearing: plain robe'). [GRS/6-2-1] |
| 粉红绸衫 | Pink Silk |  | Pink Silk Shirt | [GRS/6-2-2] |
| 皮衣 | Hide Coat |  | Leather Coat | Matron quest item. [GRS/6-2-3] |
| 飞龙道袍 | Drake Robe |  | Flying Dragon Robe | [GRS/6-2-4] |
| 绿水罗衣 | Lake Gauze |  | Green Water Gauze Dress | 'Probably stolen by Ximen Qing from Pan Xiaolian.' [GRS/6-2-5] |
| 轻纱长裙 | Gauze Gown |  |  | [GRS/6-2-6] |
| 宝蓝缎衫 | Blue Satin |  | Sapphire Satin Shirt | [GRS/6-2-7] |
| 轻花绸衫 | Petal Silk |  |  | [GRS/6-2-8] |
| 精致布衣 | Fine Robe |  |  | The Old Tailor's gift. [GRS/6-2-9] |
| 道袍 | Tao Robe |  | Taoist Robe | [GRS/6-2-10] |
| 武道服 | Dojo Garb |  | martial arts uniform | 'Junk - who'd sell this?' [GRS/6-2-11] |
| 白罗袍 | White Robe |  |  | [GRS/6-2-12] |
| 天蚕宝衣 | Sky Silk |  | Heavenly Silkworm Robe | DEF+100, '速灵运+10' = Agility/Spirit/Luck +10. [GRS/6-2-13] |
| 黑石甲 | Stone Mail |  | Black Stone Armor | 'Made of stone, so it resists poison.' [GRS/6-2-14] |
| 绣花小鞋 | Slippers |  | Embroidered Slippers | [GRS/6-3-1] |
| 皮鞋 | Hide Shoes |  | Leather Shoes | [GRS/6-3-2] |
| 登天鞋 | Sky Boots |  |  | [GRS/6-3-3] |
| 夜行衣 | Night Garb |  |  | [GRS/6-4-1] |
| 披风 | Cape |  |  | [GRS/6-4-2] |
| 金锁子甲 | Goldmail |  | Gold Chainmail | [GRS/6-4-3] |
| 亮银甲 | Silvermail |  | Bright Silver Armor | [GRS/6-4-4] |
| 龙皮甲 | Dragonhide |  | Dragonhide Armor | [GRS/6-4-5] |
| 豹皮金甲 | Panther |  | Gold Leopard Armor | Made from ten leopard skins (Snowpeak smith); jy also shortens 豹 armour to Panther. [GRS/6-4-6] |
| 霓虹羽衣 | Neon Plume |  | Rainbow Feather Cape | [GRS/6-4-7] |
| 牛皮束带 | Ox Belt |  | Oxhide Belt | [GRS/6-4-8] |
| 恶魔袍 | Demon Robe |  |  | [GRS/6-4-9] |
| 幻影披风 | Dream Cape |  | Phantom Cape | Needed to enter the Dreamscape; sold by Gu Yanwu. [GRS/6-4-10] |
| 怪兽披风 | Beast Cape |  |  | The Beast's heirloom (1-4-1). [GRS/6-4-11] |
| 皮护腕 | Hide Cuff |  | Leather Bracer | jy: 护腕/护手 = Cuff. [GRS/6-5-1] |
| 圣护腕 | Holy Cuff |  |  | [GRS/6-5-2] |
| 钢铁手 | Steel Hand |  |  | 'At least 59 jin.' [GRS/6-5-3] |
| 老花镜 | Spectacles |  | Reading Glasses | The Old Tailor's; Granny's 'shiny thing' (1-1-6). [GRS/6-6-1] |
| 绿牡丹 | Jade Peony |  | Green Peony | MP+25 per turn. [GRS/6-6-2] |
| 红杜鹃 | Red Azalea |  |  | HP+30 per turn. [GRS/6-6-3] |
| 白玫瑰 | White Rose |  |  | [GRS/6-6-4] |
| 蛇灵珠 | Snake Orb |  | Snake Spirit Pearl | 珠 = Orb. [GRS/6-6-5] |
| 虫符 | Bug Ward |  | Bug Charm | 符 = Ward in yxts (fmj 'Charm' is too long for 白鬼符/黑鬼符 in 10). [GRS/6-6-6] |
| 鱼篓 | Fish Creel |  |  | [GRS/6-6-7] |
| 白鬼符 | White Ward |  | White Ghost Ward | [GRS/6-6-8] |
| 黑鬼符 | Black Ward |  | Black Ghost Ward | [GRS/6-6-9] |
| 黑暗珠 | Dark Orb |  |  | [GRS/6-6-10] |
| 挚爱金戒 | Love Ring |  | Golden Ring of True Love | Xiaoyao's lost ring, found by Deng Shiyu: the price of the treasure map. [GRS/6-6-11] |

## Consumables

| zh | en | short | alt | note |
|---|---|---|---|---|
| 翡翠豆腐 | Jade Tofu |  |  | Pan Xiaolian's tofu; HP100. [GRS/6-9-1] |
| 白玉豆腐 | White Tofu |  |  | MP50. [GRS/6-9-2] |
| 糖葫芦 | Sugar Haws |  | candied haws | Granny's favourite. [GRS/6-9-3] |
| 酥油茶 | Butter Tea |  |  | [GRS/6-9-4] |
| 猪肉 | Pork |  |  | Description says 'From a pig: delicious dog meat'; the quest log says 狗肉 'dog meat' where the Matron asks for 猪肉. Keep the joke in the description; the quest log should say Pork. [GRS/6-9-5] |
| 狗肉 | dog meat |  |  | Quest-log/description mix-up for Pork. |
| 烧鸡腿 | Drumstick |  | Roast Chicken Leg | [GRS/6-9-6] |
| 包子 | Steam Bun |  | baozi | [GRS/6-9-7] |
| 鲤鱼 | Carp |  |  | [GRS/6-9-8] |
| 生肌膏 | Heal Salve |  |  | HP1000, cures poison. [GRS/6-9-9] |
| 金创药 | Wound Balm |  |  | HP999. [GRS/6-9-10] |
| 清毒丸 | Antidote |  |  | Cures poison. [GRS/6-9-11] |
| 龙须草 | Dragonweed |  | Dragon's Beard Grass | MP800, cures Confuse/Silence/Sleep. [GRS/6-9-12] |
| 七里香 | Sevenscent |  | Seven-Li Fragrance | A wine 'that smells wonderful'. [GRS/6-9-13] |
| 八里香 | Eightscent |  | Eight-Li Fragrance | [GRS/6-9-14] |
| 海外仙丹 | Sea Elixir |  | Overseas Elixir | [GRS/6-9-15] |
| 大烧烤 | Big BBQ |  |  | Party HP+1000. [GRS/6-9-16] |
| 忘忧散 | Heartsease |  | Sorrow-Forgetting Powder | Cures all statuses for the party (fmj's 忘忧 = Heartsease). [GRS/6-9-17] |
| 攻击令 | Power Writ |  | Attack Writ | Attack+1. 令 = Writ: Power / Guard / Speed / Soul / Luck Writ. [GRS/6-11-1] |
| 防御令 | Guard Writ |  | Defense Writ | [GRS/6-11-2] |
| 生命符 | HP Ward |  | Life Ward | Max HP+1. [GRS/6-11-3] |
| 真气符 | MP Ward |  |  | Max MP+1. 真气 = MP (engine), not qi (内力). [GRS/6-11-4] |
| 神行令 | Speed Writ |  |  | Agility+1. [GRS/6-11-5] |
| 灵魂令 | Soul Writ |  |  | Spirit+1. [GRS/6-11-6] |
| 好运令 | Luck Writ |  |  | Luck+1. [GRS/6-11-7] |
| 乾坤 | Cosmos |  | Heaven and Earth | Max HP and MP +1. [GRS/6-11-8] |
| 战神 | War God |  |  | Attack and Defense +1. [GRS/6-11-9] |
| 大仙丹 | Big Elixir |  |  | [GRS/6-11-10] |
| 生命丹 | HP Pill |  |  | [GRS/6-11-11] |
| 真气丹 | MP Pill |  |  | [GRS/6-11-12] |
| 两仪仙丹 | Taiji Pill |  | Yin-Yang Elixir | Boosts ATK and DEF for 5 turns. [GRS/6-12-1] |
| 神机四枢丸 | Pivot Pill |  | Four Pivots Pill | Temporarily boosts Attack, Defense and Agility. [GRS/6-12-2] |
| 神秘仙丹 | mystery elixir |  |  | Bubble Pal's fake 'immortality' pill (1-6-2). |
| 恶魔散 | Demon Powder |  |  | The poison that fells Yuxin (1-6-2); the antidote quest follows. |

## Items and materials

| zh | en | short | alt | note |
|---|---|---|---|---|
| 令牌 | token |  | tag | The six sect heads' tokens (掌门令牌) that open the time machine. Item names use 'X Tag' because 'Wudang Token' (12) is over the 10-char item field; dialogue may say 'token'. |
| 时间机器 | time machine |  |  | In the hero's room (1-1-3): takes the six tokens and releases the Archdemon. Also 时空转换装置 'space-time transfer device' (intro). |
| 解药 | antidote |  |  | The cure for Demon Powder (chain Xiaoyao -> Deng Shiyu -> Liang -> Flatline Love -> SSK). |
| 安全网 | Safety Net |  |  | No encounters until the next map ('safe mode'). [GRS/6-14-1] |
| 镇妖石 | Quellstone |  | Demon-Quelling Stone | [GRS/6-14-2] |
| 拳经 | Fist Book |  | Boxing Canon | One of Mr. Wenshi's four rare books. [GRS/6-14-3] |
| 水镜 | Waterglass |  | Water Mirror | Water book: teaches Ice Spell. The five element books keep poetic one-word names: Flamestar, Stormwake, Windspring, Earthveil, Waterglass. [GRS/6-14-4] |
| 净化石 | Purestone |  | Purifying Stone | Purifies the Hexblade. [GRS/6-14-5] |
| 铸剑石 | Forgestone |  | Sword-Forging Stone | Fuses two swords. [GRS/6-14-6] |
| 雪豹皮 | Snow Pelt |  | Snow Leopard Skin | 豹皮 'leopard skin' in dialogue (ten make the Panther). [GRS/6-14-7] |
| 豹皮 | leopard skin |  |  | Dialogue (1-4-1). |
| 虎皮 | tiger skin |  |  | Liang's price (1-4-3). |
| 武林宝鉴 | Sect Codex |  | Treasure Mirror of the Martial World | Chai Zi's first gift (1-1-20): 'automatically records every sect's traits'. [GRS/6-14-11] |
| 惊世刀谱 | Blade Book |  | Earth-Shaking Saber Manual | [GRS/6-14-12] |
| 金矿1 | Gold 90% |  | Gold Ore 1 | Ore of 90% purity (the description says so); named by purity because 'Gold Ore 1' does not always fit 10. |
| 金矿2 | Gold 80% |  | Gold Ore 2 | Ore of 80% purity (the description says so); named by purity because 'Gold Ore 2' does not always fit 10. |
| 金矿3 | Gold 70% |  | Gold Ore 3 | Ore of 70% purity (the description says so); named by purity because 'Gold Ore 3' does not always fit 10. |
| 银矿1 | Silver 90% |  | Silver Ore 1 | Ore of 90% purity (the description says so); named by purity because 'Silver Ore 1' does not always fit 10. |
| 银矿2 | Silver 80% |  | Silver Ore 2 | Ore of 80% purity (the description says so); named by purity because 'Silver Ore 2' does not always fit 10. |
| 银矿3 | Silver 70% |  | Silver Ore 3 | Ore of 70% purity (the description says so); named by purity because 'Silver Ore 3' does not always fit 10. |
| 铜矿1 | Copper 90% |  | Copper Ore 1 | Ore of 90% purity (the description says so); named by purity because 'Copper Ore 1' does not always fit 10. |
| 铜矿2 | Copper 80% |  | Copper Ore 2 | Ore of 80% purity (the description says so); named by purity because 'Copper Ore 2' does not always fit 10. |
| 铜矿3 | Copper 70% |  | Copper Ore 3 | Ore of 70% purity (the description says so); named by purity because 'Copper Ore 3' does not always fit 10. |
| 铁矿1 | Iron 90% |  | Iron Ore 1 | Ore of 90% purity (the description says so); named by purity because 'Iron Ore 1' does not always fit 10. |
| 铁矿2 | Iron 80% |  | Iron Ore 2 | Ore of 80% purity (the description says so); named by purity because 'Iron Ore 2' does not always fit 10. |
| 铁矿3 | Iron 70% |  | Iron Ore 3 | Ore of 70% purity (the description says so); named by purity because 'Iron Ore 3' does not always fit 10. |
| 金矿 | gold ore |  |  | Dialogue (金矿石 'gold ore'). 银矿 silver ore, 铜矿/青铜矿 copper ore, 铁矿/玄铁矿 iron ore. |
| 炎宿 | Flamestar |  |  | Fire book: teaches Fire Spell. [GRS/6-14-25] |
| 雷觉 | Stormwake |  | Thunder Awakening | Thunder book: Bolt Spell. [GRS/6-14-26] |
| 风源 | Windspring |  | Source of Wind | Wind book: Wind Spell. [GRS/6-14-27] |
| 土隐 | Earthveil |  | Earth Hermit | Earth book: Earth Spell. [GRS/6-14-28] |
| 属性书 | Stat Book |  |  | 'If you can understand it, your stats rise a lot' (1-255-29: 'too dull to read it').[GRS/6-14-29] |
| 信 | Letter |  |  | The Elder's letter to the Inspector; opening it reveals a note (1-255-30). [GRS/6-14-30] |
| 升级秘籍 | Level Tome |  | Level-Up Manual | Required for each level-up from 1-0-9. [GRS/6-14-31] |
| 飞行卡 | Fly Card |  | Flight Card | The Demon Guard's card into the Demon Cave (1-255-32). [GRS/6-14-32] |
| 花间令牌 | Flower Tag |  | Flower Sect token | From Li Qingzhao. [GRS/6-14-33] |
| 伊贺谷令牌 | Iga Tag |  | Iga Valley token | From He Zhongyang. [GRS/6-14-34] |
| 雪山令牌 | Snow Tag |  | Snow Sect token | From Rhett Butler. [GRS/6-14-35] |
| 红莲令牌 | Lotus Tag |  | Red Lotus token | From Yu Hongru. [GRS/6-14-36] |
| 武当令牌 | Wudang Tag |  | Wudang Sect token | From Taoist Qingxu. [GRS/6-14-37] |
| 八卦令牌 | Bagua Tag |  | Bagua Sect token | From Wang Weiyang. [GRS/6-14-38] |
| 石块 | Stone |  |  | Crafting material. [GRS/6-14-39] |
| 布匹 | Cloth |  |  | Crafting material. [GRS/6-14-40] |
| 花彩神布 | Prism Silk |  | Five-Colour Divine Cloth | Bingyan's price for teaching forging; she calls it 五彩神布 (same item). [GRS/6-14-41] |
| 五彩神布 | Prism Silk |  |  | Bingyan's name for 花彩神布 (1-11-2). |
| 尸块 | Body Part |  | corpse chunk | 88 of them open the way down in the Demonspire. [GRS/6-14-42] |
| 回程 | Return |  |  | Returns you to town and allows saving. [GRS/6-14-43] |
| 秘籍 | manual |  |  |  |

## Arts (MRS)

| zh | en | short | alt | note |
|---|---|---|---|---|
| 魔翼欺天 | Demonwing |  | Demon Wings Defy Heaven | 'The Black Archfiend's mightiest spell: drains enemy MP.' A black art the hero cannot learn: one of the girls learns it (1-255-8). Also the book's item name (GRS 6-14-8). [MRS/4-1-40] |
| 吸腥大法 | Leech Art |  | Star-Sucking Art | Typo/pun on 吸星大法 'Star-Sucking Art' (腥 'blood-reek' for 星 'star'); drains enemy HP. Needs Lv 20. Book and MRS. [MRS/4-1-34] |
| 北冥神功 | Beiming |  | Beiming Divine Art | 'No need to explain, everyone knows what it does.' Needs the Leech Art first (Mr. Wenshi). Book and MRS. [MRS/4-1-35] |
| 吸星大法 | Star-Sucking Art |  |  | Not in the text; reference for 吸腥大法. |
| 炎咒 | Fire Spell |  |  | Fire basic (Flamestar). fmj: 咒 = Spell. [MRS/4-1-1] |
| 三味真火 | True Fire |  | Samadhi True Fire | Fire mid. [MRS/4-1-2] |
| 流星火雨 | Meteor Rain |  | Meteor Fire Rain | Fire high. [MRS/4-1-3] |
| 炼狱火海 | Inferno |  | Purgatory Fire Sea | Fire high (Dugu Sheng's mentor). [MRS/4-1-24] |
| 净衣咒 | Clean Spell |  | Cleansing Spell | Cures poison (fire mentor). fmj: Purify Spell (12, too long now). [MRS/4-3-1] |
| 惊雷闪 | Thunderclap |  |  | Thunder mid (Yuxin, 2000 EXP). [MRS/4-1-4] |
| 天雷空破 | Sky Thunder |  | Heaven's Thunder Breaks the Void | Thunder high (8000 EXP). [MRS/4-1-11] |
| 雷动九天 | Sky Quake |  | Thunder Shakes the Nine Heavens | Thunder high (15000 EXP). MRS 4-2-4 has the same name with a Red Lotus buff description. [MRS/4-1-27] |
| 雷咒 | Bolt Spell |  | Thunder Spell | Thunder basic (Stormwake). fmj said Thunder Spell (13, over the 11-char MRS limit used now). [MRS/4-1-10] |
| 雨恨云愁 | Rain Sorrow |  | Rain's Grief, Clouds' Sorrow | Water high. [MRS/4-1-5] |
| 冰咒 | Ice Spell |  |  | Water basic (Waterglass). [MRS/4-1-12] |
| 风咒 | Wind Spell |  |  | Wind basic (Windspring). [MRS/4-1-6] |
| 风卷尘生 | Dust Gale |  | Wind Whirls the Dust | Wind high (Ouyang Jian's mentor). [MRS/4-1-7] |
| 罡风惊天 | Heaven Gale |  | Sky-Shaking Gale | Wind high. [MRS/4-1-25] |
| 土咒 | Earth Spell |  |  | Earth basic (Earthveil). [MRS/4-1-8] |
| 飞岩术 | Flying Rock |  |  | Earth mid (Tang Jing's mentor). fmj: Flying Rocks (12, too long now). [MRS/4-1-9] |
| 泰山压顶 | Avalanche |  | Mount Tai Crushes Down | Earth high; the idiom (Mount Tai pressing down on your head) in 11 chars. [MRS/4-1-26] |
| 千练神鞭 | Myriad Lash |  | Thousand-Refined Divine Whip | Flower Sect mid whip art. [MRS/4-1-13] |
| 冰鞭一击 | Ice Lash |  |  | Flower Sect secret whip art. [MRS/4-1-14] |
| 天火鞭 | Fire Lash |  | Skyfire Whip | [MRS/4-1-15] |
| 太祖长拳 | Taizu Fist |  | Taizu Long Fist | As jy. Fist arts menu (1-255-3: 20 potential). [MRS/4-1-16] |
| 披风拳法 | Wind Fist |  | Cape Fist | Name says fist, description says staff ('a Red Lotus elder's drunken inspiration'): 披风 probably for 劈风 'wind-splitting'. 30 potential. [MRS/4-1-17] |
| 流星飞拳 | Meteor Fist |  |  | 40 potential. [MRS/4-1-18] |
| 无法杖 | Wild Staff |  | Lawless Staff | [MRS/4-1-19] |
| 川枫一刀流 | Kaede-ryu |  | Kawakaede Itto-ryu | Japanese sword-school parody (流川枫 of Slam Dunk + 一刀流); 'created by 花讽院'. Blade arts menu (1-255-12). [MRS/4-1-20] |
| 旋风三连斩 | Whirl Slash |  | Whirlwind Triple Slash | [MRS/4-1-21] |
| 迎风一刀斩 | Wind Cleave |  | Into-the-Wind Single Cut | [MRS/4-1-22] |
| 忍术烟幕 | Ninja Smoke |  | Ninjutsu Smokescreen | [MRS/4-1-23] |
| 基本剑法 | Basic Sword |  | Basic Swordplay | MRS (starter 'low-level magic' pack) and a trained skill. As jy. [MRS/4-1-28] |
| 柳叶剑法 | Leaf Sword |  | Willow Leaf Sword | [MRS/4-1-29] |
| 一剪梅花剑 | Plum Sword |  | A Twig of Plum Sword | 一剪梅 is a Li Qingzhao ci title. [MRS/4-1-30] |
| 花簇鞭法 | Bloom Whip |  | Flower Cluster Whip | Li Qingzhao's whip art (description). [MRS/4-1-31] |
| 基本杖法 | Basic Staff |  |  | Starter pack. [MRS/4-1-32] |
| 落英缤纷杖 | Petal Staff |  | Falling Petals Staff | [MRS/4-1-33] |
| 门派武功X | Sect Art X |  |  | Placeholder art for the player's own sect (research). [MRS/4-1-36] |
| 门派武功Y | Sect Art Y |  |  | [MRS/4-1-37] |
| 门派武功Z | Sect Art Z |  |  | [MRS/4-1-38] |
| 倾国银弹波 | Cash Cannon |  | Nation-Toppling Silver Bullet Wave | Chai Zi's dying gift (1-12-1): 'turns your lust for money into power'. 银弹 = silver bullets (money). [MRS/4-1-39] |
| 仙风云体 | Cloud Body |  | Immortal Wind Cloud Body | Agility up 4 turns (wind mentor). [MRS/4-2-1] |
| 真元护体 | True Guard |  | True Essence Guard | Defense up 4 turns (earth mentor). [MRS/4-2-2] |
| 天罡战气 | Battle Aura |  | Heavenly Battle Qi | Attack up 4 turns (thunder, 5000 EXP). fmj: Heavenly War Qi (15). [MRS/4-2-3] |
| 冰心决 | Icy Heart |  | Icy Heart Mantra | 决 for 诀. Ice armour. fmj name (its long form Icy Heart Mantra is 16). [MRS/4-2-5] |
| 逍遥游步 | Wander Step |  | Free and Easy Steps | [MRS/4-2-6] |
| 暖雾 | Warm Mist |  |  | Small heal (wind mentor). [MRS/4-3-2] |
| 雨润 | Rain Balm |  |  | Cures Confuse/Silence/Sleep. [MRS/4-3-3] |
| 承天载物 | Earth Grace |  | Bearing Heaven, Carrying All | Party heal (earth mentor). [MRS/4-3-4] |
| 五气连波 | Fivefold Qi |  | Five Qi in Waves | Big party heal. [MRS/4-3-5] |
| 门派内功 | Sect Qi |  | sect inner art | MRS 4-3-6/4-3-7 (heals) and a trained skill (1-1-19, 1-9-14). [MRS/4-3-6] |
| 烟水还魂 | Soul Return |  | Mist and Water Recall the Soul | Revive. [MRS/4-4-1] |

## Trained skills and martial terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 凌波微步 | Lingbo Step |  | Lingbo Weibu | Taught by Yuxin (1-1-18; event 397); written <凌波微步> in the text: use 'the Lingbo Step'. |
| 装备锻造 | Forging |  | Equipment Forging | Skill (Bingyan teaches it for a Prism Silk; Mr. Wenshi rates it). 打开了装备锻造系统 'Forging unlocked'. |
| 读书识字 | Literacy |  |  | Skill (Gu Yanwu's lessons). |
| 基本轻功 | Basic Step |  | basic lightness skill | 轻功 = 'Step' in skill names (jy: 基本身法 Basic Step); 'lightness skill' in prose. Menu item 'Step'. |
| 基本内功 | Basic Qi |  | basic inner art | 内功 = 'Qi' in skill names (jy Basic Qi). Menu item 'Qi'. |
| 基本招架 | Basic Parry |  |  | Menu 'Parry'. |
| 基本拳脚 | Basic Fist |  | basic fists and feet | Menu 'Fist'. |
| 基本刀法 | Basic Blade |  |  | Menu 'Blade'. |
| 基本鞭法 | Basic Whip |  |  | Menu 'Whip'. |
| 门派轻功 | Sect Step |  |  | Menu 'Sect-Step'. |
| 轻功 | lightness skill |  | Step | Appraisal menu item 'Step'; ranks below. |
| 内功 | inner art |  | Qi | Appraisal menu item 'Qi'. |
| 招架 | Parry |  |  |  |
| 拳脚 | Fist |  | fists and feet |  |
| 剑法 | Sword |  | swordplay | Menus (1-9-4, 1-255-11). |
| 刀法 | Blade |  | blade work |  |
| 杖法 | Staff |  |  |  |
| 鞭法 | Whip |  |  |  |
| 武功 | martial arts |  | kung fu |  |
| 绝技 | secret move |  |  |  |
| 法术 | spell |  |  | MRS descriptions (风系基本法术 'basic wind spell'); 招数 'move', 绝招 'ultimate move'. |

## Other terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 才子工作室 | Caizi Studio |  | Talent Studio | Developer name (credits, 健康游戏忠告 sign-off 'BY才子工作室', title timemsg). |
| 众玩家 | Players |  | All Players | Fourth-wall chorus tag ('众玩家:KAO!有完没完!'). |
| 玩家 | Player |  |  | Tag for the player complaining (1-1-17, 1-1-20). |
| 对方 | the other person |  |  | Generic NPC chatter (1-9-3): 'They stare at you...'. |
| MM | girls |  | babes | Net slang 美眉 (Chai Zi: 'take some girls along'; the quest log hint 'find two girls'). Use 'girls'. |
| 门派 | sect |  |  | Also 帮派 for the player's own sect (both 'sect'). 我的门派 = 'My Sect'; 建立门派 'found a sect'; 清理门派 'purge the sect' (deal with troublemakers). |
| 帮派 | sect |  | gang | Player's own sect in 1-0-9 (垃圾帮派 'a garbage sect', 小/中等/大型/超大型帮派 'small / mid-size / large / huge sect'). |
| BBK俱乐部 | BBK Club |  |  | The BBK (步步高) fan forum; 俱乐部RPG区 = 'the club's RPG board'. 步步高俱乐部 = 'BBK Club' too. |
| 步步高俱乐部 | BBK Club |  |  |  |
| 六芒星阵 | hexagram array |  |  | Townsfolk rumour of a space-time array; the hero mutters 'you mean my time machine'. |
| 英雄坛说 | Heroes' Altar |  | Tales of the Heroes' Altar | Game title (games.py title_en). |
| 走火入魔 | qi deviation |  |  | Failed self-healing (1-0-8): 'you lose your focus, your qi goes astray'. |
| 江湖 | the martial world |  | jianghu |  |
| 武林 | the martial world |  | wulin |  |
| 健康游戏忠告 | Healthy Gaming Advice |  |  | The 2004 official Chinese anti-addiction notice (1-0-5 timemsg): 抵制不良游戏 'Reject bad games', 拒绝盗版游戏 'Refuse pirated games', 适度自我保护 'Protect yourself', 谨防受骗上当 'Beware of scams', 适度游戏益脑 'Moderate play is good for the brain', 沉迷游戏伤身 'Addiction harms the body', 合理安排时间 'Manage your time', 享受健康生活 'Enjoy a healthy life'. |
| 886 | bye-bye |  | bye | Net slang (拜拜了); 'Bye!'. |
| 5555 | boo-hoo |  | sob | Crying (wuwuwu). 55555~~~ -> 'Boo-hoo~'. |
| 汗 | *sweat* |  |  | Net slang for embarrassment ('汗~~一滴' '*a drop of sweat*'). |
| 晕 | ugh |  |  | Net slang ('晕死!' 'Good grief!'). |
| 靠 | damn |  |  | Mild swear (KAO). TMD 'damn it'; *** and @#$% stay as is. |
| 嘎嘎 | hehe |  |  | Laugh. |
| 小KS | piece of cake |  |  | 小case (no big deal), written KS (1-4-3). |
| 纯蓝 | Pure Blue |  |  | '抄纯蓝的开头' - the intro copies the opening of 纯蓝, apparently another hobby game. |
| 仙剑 | Chinese Paladin |  |  | 仙剑迷 'a Chinese Paladin fan'; Xiaoyao's song (岁月难得沉默 秋风厌倦漂泊) is from the 2005 TV series song 逍遥叹. |
| 试玩版 | demo |  | demo version | Leftover demo lines (1-10-7); 正式版 'full version'. |
| 花讽院 | Hanafuin |  |  | Fictional school 'that created Kaede-ryu' (Slam Dunk pun); Japanese-style reading. |
| 001 .. 052, b001 .. b010 | (same) |  |  | Numbered dev labels: NPC records ARS 3-2-1..52 and scene objects ARS 3-4-1..10. Never displayed; kept as is (62 glossary rows so autofill covers every ARS name). |

## UI, stats, money and rank ladders

| zh | en | short | alt | note |
|---|---|---|---|---|
| 系统提示 | System |  | System note | Speaker tag of the game itself (26x). Write 'System: ...'. 提示 = 'Tip', 重要提示 = 'Important', 超级重要提示 = 'Super important', 练级提示 = 'Training tip'. |
| 门派提示 | Sect tip |  |  | Tag (1-0-9). 帮派提示 the same: 'Sect tip'. |
| 帮派提示 | Sect tip |  |  | Tag (1-0-9). |
| 瞬息转移系统 | Instant Transfer |  | teleport system | 1-0-6 message 'opened the Instant Transfer system' (teleport to towns; costs qi). |
| 魔法 | magic |  |  | Engine menu 魔法 stays 'Magic' (see decisions); dialogue 低级魔法 'low-level magic', 黑魔法 'black magic'. |
| 打坐 | Meditate |  |  | 1-0-8 menu (查看内力 打坐 疗伤 = 'Check-Qi Meditate Heal'): +5 qi per two hours. |
| 疗伤 | Heal |  |  | Heal with qi. |
| 内力 | qi |  | inner power | A script-kept pool 0-100 (var 53; '每个人内力最大值为100'), NOT the engine MP: it pays for teleporting, Dreamscape entry, gathering, recruiting, healing; refilled by meditating. Write 'qi' ('Not enough qi!'). 真气 is MP. |
| 真气 | MP |  |  | Engine MP (status screen 'MP'); 真气上限 'Max MP'. In prose (催动真气) 'qi' is fine. |
| 生命 | HP |  |  | 生命上限 'Max HP'. |
| 防御 | Defense |  | DEF | Descriptions ('防御+5' -> 'DEF+5'). |
| 攻击 | Attack |  | ATK | Also 攻击敌单体/全体 'hits one / all enemies'. |
| 灵力 | Spirit |  | SPI |  |
| 身法 | Agility |  | AGI | 速度 'speed' in descriptions = Agility. |
| 运气 | Luck |  | LCK | Engine 幸运 = Luck. |
| 速灵运 | AGI/SPI/LCK |  | Agility, Spirit and Luck | Sky Silk description. |
| 回合 | turns |  |  |  |
| 全体 | all |  | the whole party / all enemies |  |
| 单体 | one |  | a single target |  |
| 负面状态 | ailments |  | negative statuses |  |
| 解乱封眠 | cures Cnf/Sil/Slp |  | cures Confuse, Silence and Sleep | Descriptions; 毒 Poison, 乱 Confuse, 封 Silence, 眠 Sleep (engine Psn/Cnf/Sil/Slp). |
| 潜能 | potential |  | Potential | MUD-style points: spent on element stats (100 per +5) or arts. 'N点潜能' 'N potential'. 1-0-7 says 师门点 once (leftover): same thing. |
| 实战经验 | battle exp |  | Combat EXP | Separate counter for levelling via 1-0-9 ('50 needed'); 经验/经验值 = EXP. |
| 经验值 | EXP |  |  | Engine 经验值 = EXP. |
| 声望 | fame |  | Fame | Reputation (notice board, sect founding; ranks below). |
| 精元 | essence |  |  | Chore reward allocated to a skill (1-1-19). |
| 资质 | talent |  | Talent | Appraisal; ranks below. |
| 年龄 | Age |  |  | Appraisal ('你的年龄是:十多岁' 'Your age: in your teens'). |
| 属性 | attributes |  | elements | 雷/风/土/水/火属性 = the five element stats; also 'all your stats +10'. |
| 雷 | Thunder |  |  | Element (menu 1-0-9 '雷 风 土 水 火' = 'Thunder Wind Earth Water Fire'); 雷系 'thunder arts'. |
| 风 | Wind |  |  | Element. |
| 土 | Earth |  |  | Element. |
| 水 | Water |  |  | Element (水系). |
| 火 | Fire |  |  | Element. |
| 力量 | Strength |  |  | Gambler stake. |
| 敏捷 | Agility |  |  | Gambler stake. |
| 智力 | Intellect |  |  | Gambler stake. |
| RMB | RMB |  |  | Modern Chinese money as the game's joke currency: keep 'RMB'. 元 is the same money: '500 RMB'. 1W/5W/20W/200W (万 = 10,000) -> 10K/50K/200K/2M. |
| 元 | RMB |  | yuan | Same money as RMB ('需要500元' -> 'Costs 500 RMB'). Starter menu '1888元' -> '1888RMB' (no space in menus). |
| 两 | taels |  | tael | Old-style money where the text says 两 (Gu Yanwu's 180-tael lessons, 500-tael bounties, Mr. Wenshi's fee). Same purse as RMB. |
| 银两 | silver |  | taels |  |
| 赏银 | reward |  | bounty | '获得赏银500两' 'Reward: 500 taels'. |
| 英雄币 | hero coins |  |  | Purging your sect yields '2000 hero coins' (1-11-1). |
| 现金 | cash |  |  | Gambler payout. |
| 时辰 | two hours |  |  | '一个时辰过去了' 'Two hours pass.' |
| 级 | Lv |  | level | '需要等级5以上' 'Needs Lv 5+'. |
| 无名小卒 | Nobody |  |  | Fame rank (你的声望：...).  |
| 江湖小虾 | Small Fry |  |  | Fame rank (你的声望：...).  |
| 后起之绣 | Rising Star |  |  | Fame rank (你的声望：...). Typo 绣 for 秀. |
| 闲云野鹤 | Free Spirit |  |  | Fame rank (你的声望：...).  |
| 世外高人 | Hidden Master |  |  | Fame rank (你的声望：...).  |
| 乡间泼皮 | Village Rascal |  |  | Fame rank (你的声望：...).  |
| 已有恶名 | Ill-Famed |  |  | Fame rank (你的声望：...).  |
| 臭名昭著 | Notorious |  |  | Fame rank (你的声望：...).  |
| 绝代恶人 | Arch-Villain |  |  | Fame rank (你的声望：...).  |
| 正义少侠 | Righteous Hero |  |  | Fame rank (你的声望：...).  |
| 一代大侠 | Great Hero |  |  | Fame rank (你的声望：...).  |
| 愚不可及 | Hopeless |  |  | Talent rank (你的资质：...), lowest to highest. |
| 浑浑噩噩 | Muddled |  |  | Talent rank (你的资质：...), lowest to highest. |
| 一窍不通 | Clueless |  |  | Talent rank (你的资质：...), lowest to highest. |
| 笨头笨脑 | Dim |  |  | Talent rank (你的资质：...), lowest to highest. |
| 茅塞已开 | Awakening |  |  | Talent rank (你的资质：...), lowest to highest. |
| 聪明灵巧 | Clever |  |  | Talent rank (你的资质：...), lowest to highest. |
| 七窍玲珑 | Sharp |  |  | Talent rank (你的资质：...), lowest to highest. |
| 资质绝佳 | Gifted |  |  | Talent rank (你的资质：...), lowest to highest. |
| 玲珑剔透 | Brilliant |  |  | Talent rank (你的资质：...), lowest to highest. |
| 大智若愚 | Sage |  |  | Talent rank (你的资质：...), lowest to highest. |
| 不足挂齿 | Negligible |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 半生不熟 | Half-Baked |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 普普通通 | Ordinary |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 驾轻就熟 | Practised |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 行家里手 | Expert |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 出类拔萃 | Outstanding |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 能工巧匠 | Master |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 神乎其技 | Uncanny |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 举世无双 | Peerless |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 鬼斧神工 | Divine |  |  | Forging rank (锻造技能：...). 不足挂齿 also in NPC looks ('skill: negligible'). |
| 微力轻身 | Light Step |  |  | Lightness-skill rank (轻功技能：...). |
| 神行百里 | Swift Feet |  |  | Lightness-skill rank (轻功技能：...). |
| 飞檐走壁 | Wall Runner |  |  | Lightness-skill rank (轻功技能：...). |
| 壁虎游墙 | Gecko |  |  | Lightness-skill rank (轻功技能：...). |
| 微步凌波 | Ripple Step |  |  | Lightness-skill rank (轻功技能：...). |
| 千里追风 | Wind Chaser |  |  | Lightness-skill rank (轻功技能：...). |
| 凌空虚渡 | Sky Walker |  |  | Lightness-skill rank (轻功技能：...). |
| 万里独行 | Far Wanderer |  |  | Lightness-skill rank (轻功技能：...). |
| 化羽飞仙 | Winged Sage |  |  | Lightness-skill rank (轻功技能：...). |
| 瞬间转移 | Teleporter |  |  | Lightness-skill rank (轻功技能：...). |
| 平平常常 | Average |  |  | Cultivation rank (修为等级：...). |
| 初窥门径 | Beginner |  |  | Cultivation rank (修为等级：...). |
| 心领神会 | Grasping |  |  | Cultivation rank (修为等级：...). |
| 融会贯通 | Fluent |  |  | Cultivation rank (修为等级：...). |
| 已有大成 | Accomplished |  |  | Cultivation rank (修为等级：...). |
| 炉火纯青 | Refined |  |  | Cultivation rank (修为等级：...). |
| 深不可测 | Profound |  |  | Cultivation rank (修为等级：...). |
| 登峰造极 | Pinnacle |  |  | Cultivation rank (修为等级：...). |
| 出神入化 | Transcendent |  |  | Cultivation rank (修为等级：...). |
| 返璞归真 | Perfected |  |  | Cultivation rank (修为等级：...). |
| 初学乍练 | a novice |  |  | MUD-style look text '★武艺看起来...' ('Skill looks like: ...'). |
| 不堪一击 | a pushover |  |  | MUD-style look text '★武艺看起来...' ('Skill looks like: ...'). |
| 不知深浅 | unfathomable |  |  | MUD-style look text '★武艺看起来...' ('Skill looks like: ...'). |
