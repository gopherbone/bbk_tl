# 侠客行 (xkx) English glossary

Status: **decisions made** (no open question blocks translation; the reviewer can override any row; Decision 10
is flagged for the owner). Machine-readable source: `docs/xkx/glossary.jsonl` (one term per line: `zh`, `en`,
`category`, `count`, optional `alt` / `short`, `note`, `source_ids`). This page summarises the same data. Story
background and the quote table: `docs/xkx/story.md`; translator brief: `docs/xkx/translating.md`.

- `count` = how often the zh string occurs as a substring across `work/xkx.strings.jsonl` (all kinds; for ASCII
  labels and the numeric placeholders, the number of rows that are or contain it). Short terms over-count, so read
  it as "how common".
- Field limits (`tools/tl/common.py problems()`): item names (grs.name) <= 10 chars, ARS names <= 11, skill names
  (mrs.name) <= 11, map names <= 12, scene banners (setscenename) <= 10, choices <= 19, menus = the same number of
  space-separated items as the Chinese, no spaces inside an item. `en` is the form for dialogue and for every name
  field it fits; `short` is used by `tools/tl/autofill.py` only where `en` breaks a row's limit (中原 "Central
  Plains" / map and banner "Central"; 华山派 "Huashan Sect" / banner "Huashan"; house banners "X's").
- All `en` / `alt` / `short` values are plain ASCII.
- Validation: every grs.name / mrs.name / ars.name / map.name / setscenename row (842 rows: 265 items, 69 skills,
  270 ARS, 118 maps, 120 banners) has a term that fits its limit. `autofill.py --game xkx` writes all 842 to
  `translations/xkx/parts/auto.jsonl`; `check.py` reports 0 errors and about 250 expected warnings (a `short` form
  in a banner/map row, or a substring hit such as 老伯 inside 老伯伯家).
- Category `role` (generic people words: 少侠, 师傅, 父亲, 强盗, 守卫...) is deliberately outside `check.py`'s
  glossary warning, because those words take different English by context ("young hero" / "sir"; "Father" / "Dad").

## What kind of game this is

A 2005 fan game for BBK's handheld (BBKRPG engine; the credits say "BBKRPG开发包V1.3版", and the engine is 伏魔记's)
by **Chunlan Studio (纯蓝工作室)**: script, planning and story by **Chunlan Guardian (纯蓝守护者)**, maps by
**SSK**. It calls itself 《侠客正传》 in the intro and "侠客完美版" (the "perfect edition") at boot; NPCs call the
game 侠客 "Xiake". It is a wuxia **raising sim**: free stat allocation (Essence Points), an age clock (one year per
hour of play), sects with fetch-quest ladders, a Martial Tournament, marriage and a daughter, a pet, a Coming-of-Age
trial, and a short main plot about the hero **Mo Ming** being used by his father **Mo Jingchou**, head of the Five
Poisons Cult. Around it sit about seventy one-room houses of villagers and **real BBK forum users** (SSK, Paladin,
solfen, andygzq, Flybug, Nightbug...), each with a one-line "famous saying" (the intro promises "all NPC dialogue
is famous quotes, so you learn something"; see story.md, Quotes), plus a lot of 2005 Chinese net humour (汗, 555,
靠, 9494, 88), BBK product placement (e-dictionaries, the forum, the RPG dev kit) and the author breaking in as a
speaker. Tone: cheeky, juvenile, fourth-wall-breaking; also some crude nationalism on the Japan island (Decision 10).

## Conventions

**Speaker tags.** Unlike szzm, this game writes the speaker into the text: `剑圣：你就是莫靖仇之子？`. Keep every tag,
in the form **`Name: text`** with an ASCII colon and one space (as in jy), using the glossary name: "Sword Saint:
You're Mo Jingchou's son?". The source mixes `：` and `:`; always write `: `. Two speakers: `糟老头，糟头老：杀！` =
"Old Codger, Codger Old: Kill!". 系统提示： (and the typo 系统提升：) = **"System: "**. Lines with no tag are the
hero (pic=1) or narration. Do not add tags the source lacks.

**Names.** Chinese personal names in pinyin, surname first (Mo Ming, Mo Jingchou, Hua Yingxiong, Zhang Zhanqing,
Dugu Zheng, Ye Lingling, Leng Yi); 阿- names "Ah X" (Ah San, Ah Xiu, Ah Dai), 小- children's names as one word
(Xiaohong, Xiaohu, Xiaomei, Xiaoxue, Xiaobao) except 小王 / 老王 "Young Wang" / "Old Wang" (brothers) and 小新
"Shin-chan" (Crayon Shin-chan). Descriptive nicknames are translated (Wise Elder, Code Nut, Charmer, Shopaholic,
PC Nut, Mad Patriot, Silly King, Old Codger, Big Rabbit, Shadow Pig, Windchime, Tipsy Sword, Bigeye, Green / Red
Blight). Jin Yong names as in jy (Yue Buqun); new sect masters in pinyin (Gongzhi Yi, He Tieshou, Dugu Hong, Leng
Aotian). The mock-Japanese names are read as Japanese (Kitsugi Ichiro, Inuinu Jiro "dog-dog", Kanto Binro).

**Forum handles.** Latin handles stay exactly (SSK, Paladin, solfen, andygzq, TAD, ZZQ, ZF). The studio and author
keep pinyin as their credit: **Chunlan Studio**, **Chunlan Guardian** (纯蓝 alone "Chunlan"). Chinese handles that
the game plays on are translated: 通宵虫 "Nightbug" (tagged 虫子 "Bug"), 虫虫飞 "Flybug", 灌水者 "Flooder" (灌水 =
forum flooding), 水王 "Flood King", 喜剧之王 "King of Comedy", 诚信电器 "Chengxin Electric", 影子猪 "Shadow Pig";
name-like handles stay pinyin (Ye Lingling, Leng Yi, Xiyu, Zhuofeng, Yaya...). The credits use the same forms.

**Hero.** 莫名 **Mo Ming** (ARS 3-1-1 / 3-1-4; the letter 1-255-39 is addressed "莫名：", and 莫名迷茫中 / 莫名心想
name him). The name means "inexplicable" in Chinese; the pun is not translated. His family arts: 莫名拳 "Mo Fist",
莫名心法 "Mo Mind Art". He calls his parents 爹 / 娘 "Dad" / "Mom" in speech, 父亲 / 母亲 "Father" / "Mother"
in more formal lines; tags 爹爹： / 爹： "Father:", 娘亲： / 母亲： "Mother:".

**Places.** Five regions: 中原 **the Central Plains** (map/banner "Central"), 北部 **the North**, 南部 **the
South**, 西部 **the West**, 东部 **the East** (maps "North" etc.), plus 日本岛 **Japan Island** ("Japan"). Home:
忘忧村 **Worryfree Village** ("Worryfree"), the family house 宁详居 "Serene Lodge" (banner "Home"). Story sites: 光明顶
**Bright Peak** (Jin Yong's Ming Cult summit; banner "Brightpeak"), 华英雄家 **Hua Manor**, 大雁塔 **the Wild Goose
Pagoda** (Pagoda 1F-3F), 乱石岗 **Rock Hill**, 井底 **Well Bottom**, 五行八卦阵 **the Bagua Array** with the four
mazes **Metal, Wood, Water, Earth** (金木水土). Houses: X家 = "X's House" in dialogue; map (12) and banner (10) take
the house form when it fits, else the short "X's" (Chief's, Fisher's, Ah Wang's); a few houses take a name
(Hermitage, Hua Manor, Wushan Den, Bandit Den, Blight's Den, Consulate). Shops: Pawnshop, Inn, Mall, Pharmacy,
Martial Hall (banner "Arts Hall"), Fun City, Net Cafe, Sect Hall.

**Sects.** Shared with jy: 丐帮 **Beggars' Sect** (short "Beggars"), 魔教 **Demon Cult**, 华山派 **Huashan Sect**
("Huashan"). New: 英雄门 **Hero Sect** (alt Heroes' Gate), 神龙帮 **Shenlong Gang** ("Shenlong"; alt Divine Dragon
Gang), 五毒教 **Five Poisons Cult** (the villain's). 门派 / 帮派 = sect; 五大门派 / 5大门派 = "the five great
sects"; 师傅 Master, 师娘 "Madam" (your master's wife), 小师弟 "your little brother" (junior), 教主 Cult Leader.
Arts in the showgut descriptions use jy forms: 打狗棒法 Dog Beater (alt Dog-Beating Staff), 降龙十八掌 18 Dragons
(Eighteen Dragon-Subduing Palms), 独孤九剑 Dugu Nine (Nine Swords of Dugu), 吸星大法 Star-Absorbing Art (new);
in running prose the long alt forms read better. 内力 = "internal energy", 武林 / 江湖 = "the martial world".

**Titles and systems.** 武林盟主 **Martial Lord** (alt Leader of the Martial World), 武林大会 **the Martial
Tournament**, 少侠 "young hero" (or "sir"), 大侠 "hero". Points: 精元点 **Essence Points**, 师门点 **Sect Points**,
剧情点 **Story Points**, 声望 **Renown** (ranks Nobody / Small Fry / Rising Star / Young Hero / Great Hero), 感情值
**Affection**, 支持度 **support rating** (for the BBK forum). 成人 = "come of age" (18), 成人仪式 "the
Coming-of-Age Rite". 挂机 "AFK training". 妙手空空 **Pickpocket** (the steal skill).

**Stats** (engine strings in `parts/engine.jsonl`: Attack, Defense, Agility, Spirit, Luck, HP, MP, Money): the
allocation menu (1-0-6) `攻击力 防御力 身法 灵力 幸运 生命上限 真气上限` = `Attack Defense Agility Spirit Luck Max-HP
Max-MP`. In descriptions: 攻击 / 攻 / 武术 ATK, 防御 / 御力 DEF, 身法 AGI, 灵力 / 灵 / 灵气 SPI, 吉运 LUK, 生命上限 /
体力 Max HP, 真气上限 / 最大真气值 Max MP, 真气 MP, 生命 / hp HP; ailments as the engine: 毒 Psn, 乱 / 混乱 Cnf, 封 /
咒封 / 封咒 Sil, 眠 / 昏睡 / 晕倒 Slp (the engine has no Stun); 避毒 "Psn immune", 避乱 "Cnf immune", 避眠 "Slp
immune", 避封 / 避咒封 "Sil immune".

**Money.** 元 = **yuan** ("8888 yuan", "100 yuan"); 100RMB "100 RMB"; 1W / 5W "10,000" / "50,000"; 日元 "yen"
(10000 yen = 2500 yuan is the hero's punchline). The engine label is "Money:".

**BBK.** 步步高 = **BBK** (its Chinese brand). The five e-dictionaries keep their model names: 外语通9188
**Waiyutong 9188** ("the 9188"), 下载王A100 **Download King A100**, 朗文4980 / 5980 / 6980 **Longman 4980 / 5980 /
6980**; item names `Waiyutong`, `A100`, `4980`, `5980`, `6980` as in the source. 电子词典阵 **the Electronic
Dictionary Array** (then "the Dictionary Array"). BBK论坛 / 步步高论坛 "the BBK forum", 步步高网友俱乐部 "the BBK Fan
Club", 十佳用户 "Top Ten Users", RPG开发包 "the RPG dev kit".

**Register.** Plain, cheeky modern English with light wuxia flavour; contractions; keep the net-slang energy with
English equivalents: 汗 "(sweat)" / "Sheesh...", 靠 / 我靠 "Damn" / "Crap", TMD / TMMD "damn" / "goddamn", 555
"Waaah" / "Boo-hoo", 嘎嘎 "Heh heh", 晕 "Ugh", 切 "Tch", 9494 "Yeah, yeah!", 88 / 886 "Bye!" / "Bye-bye!", 偶 = I
(cutesy), 饿？ (for 哦？) "Oh?", 呼啦呼啦 "Ha!". Keep the source's own English as it is, in its capitals ("HELLO",
"WAIT A MINUTE", "OK", "THANK YOU", "ARE YOU ZHAOSI?", "I'M?WHO ARE YOU?", "NO WHY!", "GO GO GO"); fix nothing in
it but put it in the English sentence naturally. Emoticons and keyboard mashes stay (`-_-#`, `~!@#$%^&*`, `==`).

## Decisions

1. **Title**: games.py has no `title_en` yet. The file is 侠客行, which is also Jin Yong's novel (English "Ode to
   Gallantry"), but this game is not that story. Suggested release name **"Xiake"** (the game's own short name; the
   intro's 《侠客正传》 = "The True Tale of the Xiake"); "Ode to Gallantry" would mislead. Owner to pick.
2. **Hero = Mo Ming**; father Mo Jingchou; mother unnamed ("Mother").
3. **Speaker-tag format `Name: text`** (ASCII colon + space), glossary names; 系统提示 = "System:".
4. **Sects**: jy forms for the three shared ones; Hero Sect, Shenlong Gang, Five Poisons Cult for the new.
5. **Money = yuan** (the source says 元 and RMB, not taels).
6. **BBK products keep their model names** (Waiyutong 9188, Download King A100, Longman 4980/5980/6980); BBK for
   步步高.
7. **Quotes**: lines that are real quotations use the established English (Qin Guan, Gu Cheng, Lu Xun, Petofi,
   Hai Zi, Jay Chou, the Romance of the Western Chamber; see story.md); the many unattributed modern aphorisms are
   translated faithfully as aphorisms, short and natural. Never invent an attribution.
8. **Forum handles**: Latin ones unchanged; the studio/author in pinyin; Chinese handles the game plays on translated
   (Nightbug, Flybug, Flooder, Flood King...).
9. **Placeholders kept**: ARS labels `001`..`052`, `1`..`255` (numeric enemy records shown in battle as numbers in
   the original too), and the author's numbered labels translated word for word (`58-Doctor`, `Fighter-6`,
   `11-Thread`, `Gold Vat-2`).
10. **小日本 (Japan island, 1-30-x; ARS 3-3-48)**: a common Chinese slur. Owner's decision: soften it. Write "the
    Japanese" / "those Japanese" / "a Japanese" as the sentence needs, never "Jap"; the enemy (ARS 3-3-48) is
    "Japanese Thug". The rest of the hostility stays as written ("揣死他" kick him to death, "给中国人丢脸" shaming
    China, the UN-seat jab). Do not add anything the source does not say. The release notes carry a content note.
11. **The wood-maze note**: boot showgut 1-1-1 "按插入键修复人物数据" = "Press INSERT to repair the character data";
    BBK key names in capitals as in szzm (INSERT, DEL). 1-0-9 "删除键目前尚未调用" = "The DEL key isn't used yet."
12. **Typos are fixed silently** (table below); deliberate jokes (糟头老, 我――爱――谷――蔓, gibberish spells) are kept.
13. **US spelling**; "..." for every …… / 。。。 run; "--" or " - " for ―― / --.
14. **Review (consistency pass)**: item and skill names in dialogue, "Carrying:" boxes and descriptions use the
    form the player sees in the menus. Where an `en` did not fit the 10/11-char name field, `en` is now that menu
    form and the old long form is `alt` (for prose). Exceptions kept long in dialogue: Minghan Manual (menu
    "Minghan"), Dragon Cauldron ("Cauldron"), Samadhi Fire ("True Fire"), Banana Leaf ("Banana Lf").
15. **Review**: GAME OVER lines read "System: <sentence>. GAME OVER!"; the Top Ten exchange is "Wow, really? That's
    great, thanks." for every speaker; the servant's riddle and SSK's hint use fake/real to match the answer
    choice "Fake=fake,real=real".

## Inconsistencies and typos found in the source

| source | where | fix |
|---|---|---|
| 后起之绣 | 1-0-6 Renown | 后起之秀 "Rising Star" |
| 暗惝多点 | 1-0-6@0f30 | garbled 八十多点: "80-something" |
| 叶林林 | 1-0-6 credits | 叶玲玲 Ye Lingling (the 1-0-5 copy is right) |
| 2005年6月17日 / 2005年7月1日 | credits 1-0-2/1-0-5 vs 1-0-6 | keep each date as written ("June 17, 2005" / "July 1, 2005") |
| 系统提升 | 1-10-1, 1-255-56 | 系统提示 "System:" |
| `哦\xa3`, `好吧\xa3` | 1-1-6@05b6, @063b | stray GBK byte (half of ！/～): drop |
| `\x86至ü韭\xb3abc...` | 1-9-8@037e | the Tipsy Sword's spell is deliberate gibberish; write ASCII gibberish ("Mimi mama jiji waiwai... abcdefghijklnmopqrsiuvwxyz!^#%*@^#*!... Galabang!") |
| 名菡密集 | 1-255-39 letter | 名菡秘籍 Minghan Manual |
| 三味真火 | everywhere | 三昧真火 Samadhi Fire |
| 宁详居 | home | 宁祥 (Serene Lodge) |
| 天龙盖地虎 | 1-6-13 | the password is 天王盖地虎 (see story.md, Quotes) |
| 渔翁家 vs 鱼翁家 | banner / map | same house: Fisher's |
| 五形金/木/水/土迷宫 | maps 2-40-1..4 | 五行: Metal / Wood / Water / Earth Maze |
| 小滩 | 1-1-7 | 小摊 "Hawker" |
| 公治一 | 1-4-1 | kept (公冶 is the real surname; the name is invented anyway) |
| 交给 written 教给 | 1-4-x sect letter task | "deliver it to" |
| 切需要 | 1-4-x skill lines | 且 "and" |
| 切误离开 | 1-3-5 | 切勿 "don't leave" |
| 使用用后 / 吸引除妖怪进身 | 1-3-4 incense lines | "attracts monsters" (遇敌香) / "keeps monsters away" (驱魔香) |
| 不能在孵化 | 1-3-6 | 再 "again" |
| 在梦想中声春 | 1-1-2 Paladin | 青春 "youth" (best guess) |
| 维哪斯 | 1-1-2 solfen | 维纳斯 Venus |
| 前生五白次回眸 | 1-6-9 | 五百 "five hundred" |
| 没有笑容的青春不完成 | 1-8-2 | 不完整 "incomplete" |
| 于是变有了 | 1-8-9 | 便 |
| 多写你救了我 | 1-6-10 | 多谢 "thanks for saving me" |
| 白杂头,褐杂头 | 1-6-13 | two bandits' names; ASCII comma |
| 兄弟门 | 1-6-13 | 兄弟们 "brothers" |
| 般到西部 | 1-6-3 | 搬到 "moved to" |
| 他叫\"名名 | 1-6-3 | stray quote: "He's called Mingming." |
| 10年前的久帐 | 1-7-10 | 旧账 "old score" |
| 对放看了你一眼 | 1-7-10 | 对方 "He glances at you" |
| 别大了 | 1-5-1 | 别打了 "Stop hitting me!" |
| 苦与 / 大与 / 小与 | 1-1-10, 1-20-3, 1-6-10 | 于 ("support range: above 0 and below 150") |
| 事阁这么多年 | 1-1-10 | 事隔 "after all these years" |
| 而不已经被别人利用了 | 1-1-10 | 而不知已经... "not knowing I was being used" |
| 费劲心机 | 1-1-10 | 费尽心机 |
| 改怎么说 | 1-9-2 | 该 |
| 隔天有抓了 | 1-9-2 | 又 |
| 东门A31984区 vs A31884区 | 1-6-13 | deliberate muddle by the bandits: keep the numbers as written |
| 1-30-5 tags 木次一郎 | 1-30-5@026c..02d8 | the hero is at Kanto Binro's house: write "Kanto Binro" |
| 吸取爹人内力 | 1-4-2 showgut | 敌人 "the enemy's internal energy" |
| “”以攻击代替防御 | 1-4-2 showgut | empty quotes: drop |
| 炎龙覆雨 | 1-4-5 showgut | the skill is 炎龙覆天: write "Fire Dragon" (its menu name) |
| 除此之外外 / 称着 / 口而相传 | 1-4-4, 1-4-3, 1-4-1 showguts | 除此之外 / 著称 / 口耳相传 |
| 立白家： | 1-7-7 tag | "Libai:" |
| 象 | several | 像 |
| 3三回合 | MRS 4-1-11 desc | "3 turns" |
| 可能产生5昏睡回合 | GRS 6-7-11 desc | "may cause Slp for 5 turns" |
| 攻击120灵力15... (no +) | GRS 6-7-12 desc | "ATK+120 SPI+15 AGI+12 LUK+12 DEF+15" |
| 孤独刀 | MRS 4-1-25 desc | 独孤刀 Lone Blade |
| 敌放 / 切杀伤力 / 切坚硬 | MRS 4-1-6, 4-1-12, GRS 6-14-29 | 敌方 / 且 |
| 一中野果 / 付有灵气 / 被不遗落 | GRS 6-9-8, 6-11-15, 6-6-13 | 一种 / 富有 / 被遗落 |
| 太已真人 | GRS 6-14-62 desc | 太乙真人 "Master Taiyi" (like Master Xuanji) |
| 黑白无尝 | GRS 6-10-2 desc | 黑白无常 the Black and White Impermanence ("Death" in the 3-row description) |
| 用三冥真火 | GRS 6-10-4 desc | 三昧 "Samadhi Fire" |
| 传奇中40女法师 | GRS 6-2-8 desc | "for level-40 female Wizards in Legend of Mir" |
| 6-1-5 每个的宇宙的人 | GRS desc | "everyone in every universe" (part of the joke ladder) |
| 6-7-31 desc ends 。。 | GRS desc | one full stop |
| 迷君杉 / 迷君衫, 勾魂散 / 钩魂散, 旋魂铊 / 旋魂陀, 缚龙索 / 缚龙锁, 蚀毒砂 / 蚀毒沙, 霸王靴 / 霸王鞋 and the other 鞋/靴 pairs, 飓行草 / 飚行草 | item names vs the 携带装备 messages | same items: use the item's glossary name |


## Counts

| category | terms |
|---|---|
| ui | 249 |
| person | 149 |
| place | 127 |
| armor | 87 |
| consumable | 85 |
| magic | 71 |
| item | 50 |
| other | 42 |
| role | 40 |
| monster | 36 |
| weapon | 32 |
| sect | 7 |
| title | 1 |
| skill | 1 |
| **total** | **977** (783 terms + 194 numeric placeholder labels) |


## People

| zh | en | short | alt | note |
|---|---|---|---|---|
| 莫名 | Mo Ming |  |  | The hero (actor 1, portrait pic=1, ARS 3-1-1 and the duplicate 3-1-4). Son of Mo Jingchou. The name is a pun (莫名 = 'inexplicable, nameless'); keep 'Mo Ming'. His thoughts: 莫名心想 = 'Mo Ming thinks:'. 莫名迷茫中 = 'Mo Ming is lost in confusion...'. Skills 莫名拳 / 莫名心法 = Mo Fist / Mo Mind Art. |
| 莫靖仇 | Mo Jingchou |  |  | The hero's father and the final villain: head of the Five Poisons Cult who wants to rule the martial world; used Hua Yingxiong to steal the Minghan Manual, then fakes his wound and uses his own son. 'Father' in the hero's mouth (爹 / 父亲). ARS 3-2-59 '59-Father', 3-3-55 'Father-55', transformed form 3-3-62. |
| 剑圣 | Sword Saint |  |  | Imprisoned master in the Forbidden Room of Worryfree Village (1-20-3); former keeper of the Minghan Manual on Bright Peak, beaten by Hua Yingxiong. Tells the hero the truth and the Dictionary Array plan. Speaker tag 'Sword Saint:'. |
| 华英雄 | Hua Yingxiong | Yingxiong |  | Master of Bright Peak who holds the Minghan Manual (1-1-10). Name borrowed from the comic 中华英雄 (Hua Ying-hung). Fights the hero, then reveals Mo Jingchou set them both up and flies him home with Sword Control (御剑术) before dying. ARS 3-2-72 / 3-3-52 use the short 'Yingxiong' (11-char field). |
| 万神医 | Doctor Wan |  | Miracle Doctor Wan | Worryfree Village's miracle doctor (神医). Diagnoses the father ('intermittent anaemia' in modern medicine) and brews the cure from five herbs in the Dragon Cauldron with Samadhi Fire. ARS '58-Doctor'. |
| 纯蓝守护者 | Chunlan Guardian |  | Chunlan | The author's handle (script, planning, story). Appears as an NPC (1-7-9), in his studio (1-20-5: 'Hey, who's touching my computer!'), and breaks in as a speaker with author's asides ('The hint's obvious enough, ha ha.'). Speaker tag 'Chunlan Guardian:'. 纯蓝 alone = 'Chunlan' ('Chunlan wrote the dialogue wrong, right?'). |
| 纯蓝 | Chunlan |  |  | Short for the author / studio. 纯蓝家 = Chunlan's House. ARS '62-Chunlan'. |
| SSK | SSK |  |  | Map maker and co-writer (credits), and an NPC in the North (1-6-7) who brews Tianshan Water and knows where Flybug hides. Keep as is. |
| 通宵虫 | Nightbug |  | Tongxiaochong | Real handle of the BBKRPG engine author (credits: 'Game engine: 通宵虫, 南方小鬼'), lit. 'all-night bug'. In game his home is 通宵虫家 / map 虫子家 and he is tagged 虫子 'Bug' ('Don't bother me, I'm thinking up an RPG plot!'). Pinyin Tongxiaochong in the note only. |
| 虫子 | Bug |  |  | Nightbug's nickname as speaker tag (1-2-15). Also 'bug' as in insect. |
| 南方小鬼 | Southern Imp |  | Nanfang Xiaogui | Co-author of the engine (credits only). |
| 游戏王 | Game King |  |  | Credits 'friendly support' handle. |
| 叶玲玲 | Ye Lingling |  |  | Credits 'friendly support' (also 叶林林 in 1-0-6's copy: same person, write Ye Lingling) and an East NPC (1-9-4) reciting exam doggerel. |
| 叶林林 | Ye Lingling |  |  | Typo of 叶玲玲 in the 1-0-6 credits. |
| 冷义 | Leng Yi |  |  | Tester (credits) and West NPC (1-8-12: '我――爱――谷――蔓' 'I - love - Gu - Man!'). |
| ZF | ZF |  |  | Tester (credits). |
| 虫虫飞 | Flybug |  | Chongchongfei | Forum user and hidden master in the North's secret tunnel (1-10-1): teaches his art for all your money. 'Bug Bug Fly' is a nursery rhyme; Flybug pairs with Nightbug. ARS 3-3-42, '63-Flybug'. |
| 张占卿 | Zhang Zhanqing |  | Zhang | BBK dictionary-marketing man (词典营销部) testing new machines (1-2-4). Gives the Waiyutong 9188 for delivering the forum Top Ten notices. |
| Paladin | Paladin |  |  | BBK forum user (Central Plains NPC). Keep. |
| solfen | solfen |  |  | BBK forum user (Central Plains NPC). Keep lower case. |
| andygzq | andygzq |  |  | BBK forum user (West, house 水王家 'Flood King'). Keep. |
| TAD | TAD |  |  | BBK RPG-site owner (1-8-7, tad.ys168.com). Keep. |
| ZZQ | ZZQ |  |  | The forum admin who 'chose the Top Ten users'. Keep. |
| 灌水者 | Flooder |  |  | Forum handle: 灌水 = flooding a forum with filler posts. West NPC (1-8-9). ARS 'Flooder-69'. |
| 水王 | Flood King |  |  | Forum title for the top poster (andygzq's house 水王家). |
| 希鱼 | Xiyu |  |  | Forum user (East, 1-9-1). ARS 'Xiyu-70'. |
| 喜剧之王 | King of Comedy | Comedian |  | Forum handle (Stephen Chow's film title). East NPC (1-9-9). ARS 'Comedy-71'; house short 'Comedian's'. |
| 诚信电器 | Chengxin Electric | Chengxin | Honest Electric | Forum handle (an electronics shop, 诚信 'honest'). South NPC (1-7-2). ARS 'Chengxin-65'. |
| 影子猪 | Shadow Pig |  |  | Forum handle (South, 1-7-8: 'BBK is my home!'). |
| 无名老人 | Nameless Elder |  |  | Old friend of the hero's father in the Central Plains (1-1-3, house 'Hermitage'): rumours, tips, the Coming-of-Age Rite (training maze, 5000 yuan, 88 Soul Wisps in 10 minutes). |
| 小红 | Xiaohong |  |  | Ah Xiu's runaway little sister, found among the flowers (1-1-2). |
| 阿绣 | Ah Xiu |  |  | North NPC (1-6-5) whose sister Xiaohong ran away. |
| 朴嫂 | Mrs. Pu |  |  | Village wife whose husband was dragged off by the chief to hunt monsters a year ago (1-2-5). 朴嫂丈夫 = 'Mr. Pu' (tag). |
| 朴嫂丈夫 | Mr. Pu |  | Mrs. Pu's husband | Speaker tag (1-1-2). |
| 墨镜男 | Man in Shades |  |  | The thief who stole Ah San's computer (1-1-2): 'I'm a great thief, I fear nothing, la la la!'. |
| 赵寺 | Zhao Si |  |  | Xiaoxian's sweetheart in the Central Plains; the hero greets him 'ARE YOU ZHAOSI?' (keep the source's caps English). Spicy bun / sweetest bun quest. |
| 小仙 | Xiaoxian |  |  | Huashan girl in love with Zhao Si (1-1-5). |
| 小飞仔 | Kid Fei |  |  | Gossip about the MP-draining art (1-1-2). |
| 小滩 | Hawker |  |  | Typo for 小摊 'street stall': the 'fresh boy's urine' seller (1-1-7). |
| 小虎 | Xiaohu |  |  | Kid who wants candied haws (1-2-1). His mother 虎大婶 'Auntie Hu'. |
| 虎大婶 | Auntie Hu |  |  | Xiaohu's mother. |
| 老王 | Old Wang |  |  | Receives Young Wang's letter; makes fishing rods (1-2-2). |
| 小王 | Young Wang |  |  | Old Wang's younger brother (1-2-10). |
| 鱼翁 | Old Fisher |  | Fisherman | 1-2-3 (banner 渔翁家, map 鱼翁家). |
| 渔翁 | Old Fisher |  |  | Banner form of 鱼翁. |
| 村长 | Village Chief |  |  | Drunkard who wants Sevenmile wine (1-2-6). |
| 阿三 | Ah San |  |  | His computer was stolen (1-2-7). (Not the slur sense of 阿三.) |
| 名名 | Mingming |  |  | Wise Elder's grandson (1-2-8). |
| 小神童 | Little Prodigy |  | Prodigy | Reads treasure maps for 1000 yuan (1-2-9). |
| 小美 | Xiaomei |  |  | Needs water for her sick sister (1-2-11). |
| 熊大伯 | Uncle Xiong |  |  | Asks about BBK's new machine (1-2-12; map 2-2-13). |
| 阿旺婆 | Granny Ah Wang | Ah Wang |  | Wants incense burnt for the Dragon King (1-2-13). |
| 胖大厨 | Fat Chef |  |  | Lost his cleaver (1-2-14). |
| 当铺老板 | Pawnbroker |  |  | 1-3-1. |
| 客栈伙计 | Waiter |  | Innkeeper | Inn: 'Staying the night restores you, but it's 100 yuan!'. |
| 矿石打造师 | Oresmith |  |  | Turns ten stones into one ore for 1000 yuan (80%). |
| 奸商 | Profiteer |  |  | Mall trader: Jay's CD 150, roses 100, Samadhi Fire '5W' (50,000). |
| 药铺老板 | Apothecary |  |  | Pharmacy owner. |
| 武馆教头 | Instructor |  | Head Instructor | Martial hall: buy levels (5000), Pickpocket (10000), AFK training (10,000). |
| 武馆小贩 | Hall Vendor |  |  | Sells hidden weapons. |
| 宠物商人 | Pet Dealer |  |  | Hatches Pet Eggs for 5000 yuan (Fun City). |
| 武器商 | Weaponsmith |  |  | Forges weapons from ores and Frog Cloth. |
| 大兔子 | Big Rabbit |  |  | Runaway would-be merchant (1-3-10, house in the West). 兔母 / 大兔子娘 = 'Mother Rabbit'. |
| 兔母 | Mother Rabbit |  |  | Big Rabbit's mother (1-8-6), about to hang herself; also tagged 大兔子娘. |
| 大兔子娘 | Mother Rabbit |  |  | Same as 兔母. |
| 中国商人 | Chinese Merchant |  |  | Merchant in Japan whose shop was sealed (1-3-11). |
| 公治一 | Gongzhi Yi |  |  | Head of the Beggars' Sect (1-4-1). (公治 looks like a slip for the surname 公冶; keep as written.) |
| 何铁手 | He Tieshou |  |  | Head of the Demon Cult (1-4-2). In Jin Yong she leads the Five Poisons Cult; here simply the Demon Cult master. |
| 岳不群 | Yue Buqun |  | Gentleman Sword | Head of the Huashan Sect (1-4-3), as in jy. |
| 独孤鸿 | Dugu Hong |  |  | Head of the Hero Sect (1-4-4). |
| 冷傲天 | Leng Aotian |  |  | Head of the Shenlong Gang (1-4-5). |
| 月老 | Matchmaker |  | Old Man Under the Moon | The god of marriage (1-4-6). Tag 'Matchmaker:'. Weds you for 88888 yuan; 二拜月老 parodies 二拜高堂: 'Second, bow to the Matchmaker.' |
| 勇士 | Warrior |  |  | Sect Hall clerk (1-4-7): builds your own sect for 88 Stones and 88 Cleavers once you are married. |
| 网吧老板 | Cafe Owner |  |  | Internet cafe (1-4-8): 100 RMB a session. |
| 论坛捣乱者 | Forum Troll |  |  | The 'forum crooks' you clean up (1-4-8). ARS 3-3-63 捣乱 'Troll'. |
| 毒瘤青 | Green Blight |  |  | Murderer of Bigeye's father; brags about CS, BnB and StarCraft (1-7-10). 毒瘤 'tumour' is net slang for a toxic pest; 'Blight' keeps it short. 死毒瘤 = 'you damn Blight'. |
| 毒瘤红 | Red Blight |  |  | Green Blight's partner (1-7-10). |
| 糟老头 | Old Codger |  |  | One of the Two Elders of Wushan (1-6-8). The other is 糟头老 'Codger Old' (the source's reversed-name joke). |
| 糟头老 | Codger Old |  |  | The other Wushan Elder; keep the reversed joke. |
| 巫山二老 | Wushan Two |  | Two Elders of Wushan | The villains who killed Old Uncle's family (1-9-2). ARS 巫山1/巫山2 'Wushan 1/2'. |
| 老婆婆 | Old Granny |  |  | North (1-6-10): her daughter (MM) was taken by bandits; the daughter becomes your wife. |
| MM | Girl |  |  | Net slang (美眉 / 妹妹) for a girl: the rescued daughter you court and marry (1-6-10, 1-6-13). Tag 'Girl:'; in narration 'the girl'. |
| 一天仇 | Yi Tianchou |  | Mr. Yi | South (1-7-1); receives the sect master's letter (《一天仇》 in the source's quote marks). 一先生 = 'Mr. Yi'. Quotes Gu Cheng. |
| 王伯伯 | Uncle Wang |  |  | House name 王伯伯家 (1-7-3). |
| 小宝 | Xiaobao |  |  | South (1-7-4): sells a 'secret' for 1000 yuan; tells of the treasure in the Bright Peak well. |
| 阿呆 | Ah Dai |  |  | Has a cold, wants Jade Fruit (1-7-5). |
| 电脑狂 | PC Nut |  |  | 'Computers are my life!'. |
| 立白 | Libai |  |  | 'Li Bai is my big brother, ha ha!' (pun on the poet Li Bai; 立白 is also a detergent brand). Tag in the source is 立白家 (sic): write 'Libai:'. |
| 玄机真人 | Master Xuanji | Xuanji |  | Taoist master in the West (1-8-1); his answer is gibberish symbols. 真人 = Taoist 'Perfected One': 'Master'. |
| 平平 | Pingping |  |  | 'I like the feeling of peace (和平).' |
| 小新 | Shin-chan |  |  | Crayon Shin-chan (蜡笔小新): '大象，大象...' is his elephant dance ('Mr. Elephant, Mr. Elephant...'). |
| 浊风 | Zhuofeng |  |  | Recites song-like love lines (1-8-5). |
| 丫丫 | Yaya |  |  | West NPC. |
| 风铃 | Windchime |  |  | 'I like the feeling of being blown by the wind.' |
| 傻王 | Silly King |  |  | 'Don't let the name fool you, I'm not silly at all!' |
| 独孤正 | Dugu Zheng |  |  | East (1-9-2): tells the Wushan Two story; quotes Petofi. |
| 方方 | Fangfang |  |  | East NPC. |
| 芹儿 | Qin'er |  |  | East NPC. |
| 豆子 | Douzi |  |  | East NPC. |
| 豆豆 | Doudou |  |  | East NPC. |
| 剑酒仙 | Tipsy Sword |  | Sword-and-Wine Immortal | Drunken swordsman in the East (1-9-8) who tried the Bright Peak treasure; casts a gibberish spell. Wants Sevenmile wine. |
| 丁风 | Ding Feng |  |  | East NPC. |
| 爱国狂 | Mad Patriot |  |  | 'China, China, I love you, like a mouse loves rice.' |
| 阿土伯 | Uncle Tu |  |  | Japan isle NPC (1-30-1). |
| 小旺 | Xiaowang |  |  | Japan isle NPC (1-30-2), quotes Lu Xun. Not 小王 (Young Wang). |
| 木次一郎 | Kitsugi Ichiro | Ichiro |  | Japanese villager who pays 10000 yen to kill his two neighbours (1-30-3). Mock-Japanese names read in Japanese. |
| 狗犬次朗 | Inuinu Jiro | Jiro |  | Mock name, 狗犬 'dog-dog' (inu = dog). |
| 干腾槟榔 | Kanto Binro | Binro |  | Mock name (槟榔 'betel nut'). 1-30-5 mislabels him 木次一郎 in two lines: use Kanto Binro there. |
| 日本官员 | Japanese Official |  |  | Consulate official who sealed the Chinese merchant's shop (1-30-6). |
| 红鲤鱼 | Red Carp |  |  | Wants to leap the Dragon Gate before the 500-year chance passes (1-1-8). |
| 智慧老人 | Wise Elder |  |  | West (1-6-3): letter to his grandson Mingming; asks about BBK's new machine. Map 2-6-3. |
| 编程狂 | Code Nut |  |  | North (1-6-2): wants the new RPG dev kit copied from Nightbug on a USB stick. |
| 万人迷 | Charmer |  | Heartthrob | North (1-6-4): wants flowers; quotes Hai Zi. |
| 超级JAY谜 | Super Jay Fan |  |  | North (1-6-6): Jay Chou fan; wants the album Yeh Hui-Mei. |
| 购物狂 | Shopaholic |  |  | North (1-6-9). |
| 吴老头 | Old Wu |  |  | North (1-6-11). |
| 小雪 | Xiaoxue |  |  | North (1-6-1): wants a Peace Cake. |
| JAY | Jay |  | Jay Chou | Jay Chou (周杰伦). JAY的CD碟 'Jay's CD'; the album <叶惠美> 'Yeh Hui-Mei' (2003); 双节棍 'Nunchucks'. |
| 花雷名 | Hua Leiming |  |  | Co-creator of Nine Heavens Thunder (MRS desc). |
| 陈夏菡 | Chen Xiahan |  |  | Co-creator of Nine Heavens Thunder. |
| 东游子 | Dongyouzi |  |  | Immortal who brought the Dragon Cauldron to the world. |
| 蚩尤 | Chiyou |  |  | Legend (Water Beast tip). |
| 炎帝 | the Flame Emperor |  |  | Legend. |
| 如来佛祖 | the Buddha |  |  |  |
| 李白 | Li Bai |  |  | The poet (Libai's joke). |
| 太上老君 | Laozi |  | Lord Lao | Item lore. |
| 张道陵 | Zhang Daoling |  |  | Item lore. |
| 孙悟空 | Sun Wukong |  |  | Item lore (Gold Hoop). |
| 牛魔王 | Bull Demon King |  |  | Item lore (Ox Helm). |
| 龙王 | Dragon King |  |  | Granny Ah Wang's rain god. |
| 龟仙人 | Master Roshi |  |  | Dragon Ball (Kamehameha description). |
| 笑天下 | Xiao Tianxia |  |  | 'Medicine King of the North' in item lore. |
| 北部商人 | North Merchant |  |  | Regional merchant (1-3-7): helmets and clothes. Speaker tag 'North Merchant:'. (added in review) |
| 南部商人 | South Merchant |  |  | Regional merchant (1-3-8): shoes and armor. (added in review) |
| 西部商人 | West Merchant |  |  | Regional merchant (1-3-9): wrist gear, accessories, weapons. (added in review) |
| 白杂头 | Whitemop |  |  | Bandit leader in the Bandit Den (1-6-13), tagged with Brownmop: 'Whitemop, Brownmop: Kill!' (source 白杂头,褐杂头). (added in review) |
| 褐杂头 | Brownmop |  |  | Bandit leader in the Bandit Den (1-6-13); see Whitemop. (added in review) |
| 太已真人 | Master Taiyi |  | Taiyi Zhenren | Source typo for 太乙真人 (GRS 6-14-62, the Lure Joss lore). Titled like Master Xuanji (玄机真人). (added in review) |
| 太乙真人 | Master Taiyi |  | Taiyi Zhenren | Correct form of the source's 太已真人. (added in review) |
| 共工 | Gonggong |  |  | Water god of myth (GRS 6-6-14). (added in review) |
| 李天王 | Heavenly King Li |  |  | Li Jing, the pagoda-bearing Heavenly King (GRS 6-4-11). (added in review) |
| 鲁班 | Lu Ban |  |  | The legendary master craftsman (GRS 6-4-13/14 reed armor). (added in review) |
| 张果老 | Zhang Guolao |  |  | One of the Eight Immortals (GRS 6-9-20 Twin Haws). (added in review) |
| 女娲 | Nuwa |  |  | The goddess who mended the sky (GRS 6-8-30). (added in review) |
| 风婆 | Granny Wind |  |  | Wind goddess (GRS 6-8-8). (added in review) |
| 雷神 | Thunder God |  |  | GRS 6-8-9; MRS 4-1-34's 电神 is also 'Thunder God'. (added in review) |
| 南海观音 | Guanyin |  |  | GRS 6-9-5. (added in review) |
| 孔明 | Kongming |  | Zhuge Liang | GRS 6-6-17. (added in review) |
| 织女 | Weaver Girl |  |  | GRS 6-4-12. (added in review) |

## Generic roles

| zh | en | short | alt | note |
|---|---|---|---|---|
| 娘亲 | Mother |  | Mom | The hero's mother (speaker tag 娘亲：/母亲：). Writes the farewell letter (1-255-39). 娘 = 'Mom' or 'Mother' in the hero's lines; tag 'Mother:'. |
| 母亲 | Mother |  |  | Speaker tag (1-20-6) and the hero's word; also Big Rabbit's letter to his mother (1-255-59). |
| 爹爹 | Father |  | Dad | Speaker tag 爹爹：/爹： for Mo Jingchou in 1-20-2. 爹 in the hero's lines = 'Dad'. |
| 父亲 | Father |  |  | The hero's 'my father'. |
| 神医 | miracle doctor |  | Doctor | 'You call yourself a miracle doctor?'. 神医家 banner = Doctor's House. |
| 村民 | Villager |  |  | Speaker tag. |
| 乞丐 | Beggar |  |  | Sells a secret for 1000 yuan (1-1-2). |
| 伤兵 | Wounded Soldier |  |  | West (1-1-6): takes your money for medicine and eats the wrapping paper. |
| 士兵 | Soldier |  |  | Speaker tag. |
| 守卫 | Guard |  |  | East guard (1-1-7) who keeps offering his lord's reward. |
| 小和尚 | Young Monk |  |  | West (1-1-6); quotes Qin Guan; his senior was carried off by Bigeye. |
| 和尚 | Monk |  |  | The rescued monk (1-1-7). |
| 老人 | Old Man |  |  | East (1-1-7) sells the Japanese phrasebook for 10000 yuan. |
| 路人 | Passerby |  |  | Speaker tag. |
| 大师兄 | Big Brother |  | senior brother | The Huashan senior disciple (1-1-5) worried about the black water / Water Demon. As a tag 'Big Brother:'. |
| 强盗 | Bandit |  |  | Generic; 强盗甲/乙/丙/丁 = Bandit A/B/C/D (1-6-13). ARS 3-3-29 / 3-3-46. |
| 厨师 | Cook |  |  | Inn cook who carries a banana leaf and a cleaver (1-3-2). |
| 酒保 | Barkeep |  |  | Sells Sevenmile (200 yuan). |
| 守护神 | Guardian |  |  | Cauldron guardian on Rock Hill (1-5-2): 'Who dares touch my bed?'; also the maze guardians of the Bagua Array. |
| 宠物 | Pet |  |  | Pet; ARS 3-1-5 the party pet; 宠物宝宝 'baby pet'. |
| 仆人 | Servant |  |  | Haunted House riddle-giver (1-6-12). |
| 鬼魂 | Ghost |  |  | Haunted House (ARS 3-3-31). |
| 老婆 | Wife |  |  | Your wife after the wedding (tag 'Wife:'; she calls you 老公 'honey'). |
| 老伯伯 | Old Uncle |  |  | Two old men: the pet-egg one in 王伯伯家 (1-7-3) and the one by the river (1-9-3) whose family the Wushan Two killed. 老伯 = same. |
| 老伯 | Old Uncle |  |  | Same as 老伯伯. |
| 哲学家 | Philosopher |  |  | 哲学屋 (1-9-11). |
| 少侠 | young hero |  |  | Standard address for the hero ('Young hero, could you...'). Often just 'sir' or dropped. |
| 大侠 | hero |  |  | As in jy. |
| 师傅 | Master |  |  | Your sect master (师傅我 = 'your master'). |
| 师娘 | Madam |  | your master's wife | 'Your master's wife keeps nagging for a pet.' |
| 小师弟 | little brother |  |  | 'your little brother (junior)'. |
| 教主 | Cult Leader |  |  | As in jy. |
| 帮主 | Chief |  |  | Sect chief (丐帮 history). |
| 小徒弟 | Apprentice |  |  | ARS 3-1-2: the disciple you can recruit (广招门徒 'Recruit disciples'). |
| 女儿 | Daughter |  |  | ARS 3-1-3: your daughter (born after the wedding). |
| 守护鼎 | Guardian |  |  | ARS 3-3-22: the Dragon Cauldron's guardian. |
| 宝宝 | Baby |  |  | ARS 3-3-30: the 'baby pet' you chase. |
| 青蛙 | Frog |  |  |  |
| 小子 | Kid |  |  | ARS 3-3-61; in dialogue 小子 = 'kid' / 'boy'. |
| 变身 | Transformed |  |  | ARS 3-3-62: Mo Jingchou transformed ('看我变身！' 'Watch me transform!'). |

## Titles

| zh | en | short | alt | note |
|---|---|---|---|---|
| 武林盟主 | Martial Lord |  | Leader of the Martial World | Title won at the Martial Tournament; needed (with the five sects destroyed and your own sect) to climb Bright Peak. |

## Sects

| zh | en | short | alt | note |
|---|---|---|---|---|
| 丐帮 | Beggars' Sect | Beggars |  | As in jy. Hall 1-4-1, master Gongzhi Yi; arts Dog Beater (打狗棒法) and 18 Dragons (降龙十八掌) in the showgut. Banner/ARS short 'Beggars'. |
| 魔教 | Demon Cult |  |  | As in jy. Hall 1-4-2, master He Tieshou; signature art Star Absorbing (吸星大法). |
| 华山派 | Huashan Sect | Huashan | Mount Hua Sect | As in jy. Hall 1-4-3, master Yue Buqun; Dugu Nine (独孤九剑). |
| 英雄门 | Hero Sect |  | Heroes' Gate | Hall 1-4-4, master Dugu Hong; from the Western Regions; signature Tornado (龙卷风). 门 = school/sect. |
| 神龙帮 | Shenlong Gang | Shenlong | Divine Dragon Gang | Hall 1-4-5, master Leng Aotian; small Changbai Mountains clan of healers; signature 'Fire Dragon' (the showgut writes 炎龙覆雨, the skill is 炎龙覆天). |
| 五毒教 | Five Poisons Cult |  |  | Mo Jingchou's cult (1-1-10, 1-20-3); 教主 = Cult Leader. |
| 百花派 | Hundred Flowers Sect |  |  | Lore sect in GRS 6-7-28 (its twin swords). Not one of the game's five sects. (added in review) |

## Places, maps and banners

| zh | en | short | alt | note |
|---|---|---|---|---|
| 叶玲玲家 | Ye Lingling's House | Lingling's |  | Map 2-9-4 / banner. |
| 中原 | Central Plains | Central |  | The central region and hub (shops, inn, sect halls). Map 2-1-1 / banner 1-1-2 use short 'Central' (with North / South / West / East); dialogue 'the Central Plains'. |
| 北部 | North |  | the North | Region (map 2-1-2, banner 1-1-4). |
| 南部 | South |  | the South | Region. |
| 西部 | West |  | the West | Region. |
| 东部 | East |  | the East | Region. |
| 日本岛 | Japan Island | Japan |  | Banner 1-1-8 (short Japan); reached from the East with the Japanese book. |
| 日本 | Japan |  |  | Map 2-1-6, banner 1-3-11. |
| 光明顶 | Bright Peak | Brightpeak |  | Hua Yingxiong's seat with the Minghan Manual; the finale's gate (needs Martial Lord + five sects destroyed + own sect). Jin Yong's Ming Cult summit. Banner short 'Brightpeak'. |
| 华英雄家 | Hua Manor |  |  | Banner 1-1-9 / 1-1-10, map 2-1-8. |
| 忘忧村 | Worryfree Village | Worryfree |  | The hero's home village (chapter 20). Banner/map short 'Worryfree'. |
| 宁详居 | Serene Lodge | Home |  | The hero's family home (2-20-2, banner 1-20-2 short 'Home'). 宁详 is a slip for 宁祥. |
| 禁室 | Forbidden Room | Forbidden |  | Where the Sword Saint is locked up (1-20-3). |
| 神医家 | Doctor's House | Doctor's |  | Banner 1-20-4 (map 2-20-4 is 药铺 Pharmacy). |
| 无名老人居 | Hermitage |  |  | The Nameless Elder's house (banner 1-1-3). |
| 和平居 | Peace Lodge |  |  | Map 2-2-1 (the Nameless Elder's house map). |
| 大雁塔 | Wild Goose Pagoda |  | Big Wild Goose Pagoda | Dungeon near the Central Plains: herb monsters on 3F (steal, don't attack), bandits for sect tasks. |
| 大雁塔一层 | Pagoda 1F |  |  | Banner/map. |
| 大雁塔二层 | Pagoda 2F |  |  | Banner/map. |
| 大雁塔三层 | Pagoda 3F |  |  | Banner/map. |
| 乱石岗 | Rock Hill |  |  | North: the Dragon Cauldron and its Guardian (1-5-2). |
| 十字迷宫 | Cross Maze |  |  | Banner 1-5-3. |
| 迷宫 | Maze |  |  | Map 2-5-3; generic. |
| 花丛迷宫 | Bloom Maze |  |  | Banner 1-5-4 (Bigeye's hideout). |
| 花丛 | Flowerbed |  |  | Map 2-5-4; dialogue 'the flowers'. |
| 万花丛 | Flower Sea |  |  | Banner/map 1-5-22. |
| 井底 | Well Bottom | The Well |  | Banner 1-5-5 / map 2-5-5: the Water Beast's lair under Bright Peak. |
| 当铺 | Pawnshop |  |  |  |
| 客栈 | Inn |  |  | As in jy. |
| 商城 | Mall |  |  | Shops (banners 1-3-3, 1-3-7..11); 中原商城 'the Central Plains mall'. |
| 药铺 | Pharmacy |  |  |  |
| 武馆 | Martial Hall | Arts Hall |  | Banner short 'Arts Hall'. |
| 娱乐城 | Fun City |  |  | Pet hatching. |
| 月老家 | Matchmaker |  |  | Banner 1-4-6 (map 月老). |
| 帮派管理处 | Sect Hall |  |  | Banner 1-4-7 (Warrior builds your sect). |
| 网吧城 | Net Cafe |  |  | Banner 1-4-8. |
| 网吧 | Net Cafe |  |  | Map 2-4-8; 网吧 in dialogue 'internet cafe'. |
| 鬼屋 | Haunted House | Haunted |  | North (1-6-12). |
| 强盗家 | Bandit Den |  |  | North (1-6-13). |
| 毒瘤居 | Blight's Den | Blight Den |  | South (1-7-10). |
| 神童居 | Prodigy's Den | Prodigy's |  |  |
| 哲学屋 | Philosophy Hut | Philosophy |  | East (1-9-11). |
| 日本领事馆 | Consulate |  | Japanese Consulate | Japan isle (1-30-6). |
| 五行金迷宫 | Metal Maze |  |  | One of the four Five-Element mazes (金木水土). Map spells 五形 (typo). |
| 五行木迷宫 | Wood Maze |  |  | The boot note says not to enter it after the data repair (the repair already counts one maze), to reach the full ending. |
| 五行水迷宫 | Water Maze |  |  |  |
| 五行土迷宫 | Earth Maze |  |  |  |
| 五形金迷宫 | Metal Maze |  |  | Map 2-40-1 typo of 五行. |
| 五形木迷宫 | Wood Maze |  |  | Map typo. |
| 五形水迷宫 | Water Maze |  |  | Map typo. |
| 五形土迷宫 | Earth Maze |  |  | Map typo. |
| 五行八卦阵 | Bagua Array | Bagua | Five-Element Bagua Array | Mo Jingchou's counter-array that swallows the Dictionary Array (1-20-1); four mazes, a guardian each; teleports you every 60 s. Banner short 'Bagua'. |
| 训练迷宫 | Training Maze | Trial Maze |  | Map 2-100-1: the Coming-of-Age trial (88 Soul Wisps in 10 minutes). |
| 天山 | Tianshan |  |  | 天山神水 Tianshan Water, 天山盐. |
| 华山 | Mt. Hua |  |  | As in jy. |
| 长白山 | Changbai Mountains |  |  | Shenlong Gang's home. |
| 西域 | the Western Regions |  |  |  |
| 龙门 | Dragon Gate |  |  | 跳龙门 'leap the Dragon Gate' (carp legend). |
| 大理 | Dali |  |  | As in jy (One Yang Finger). |
| 小虎家 | Xiaohu's House | Xiaohu's |  |  |
| 老王家 | Old Wang's House | Old Wang's |  |  |
| 渔翁家 | Fisher's House | Fisher's |  | Banner (map 鱼翁家). |
| 鱼翁家 | Fisher's House | Fisher's |  | Map 2-2-4. |
| 张占卿家 | Zhang's House | Zhang's |  |  |
| 朴嫂家 | Mrs. Pu's House | Mrs. Pu's |  |  |
| 村长家 | Chief's House | Chief's |  |  |
| 阿三家 | Ah San's House | Ah San's |  |  |
| 名名家 | Mingming's House | Mingming's |  |  |
| 小王家 | Young Wang's House | Young Wang |  |  |
| 小美家 | Xiaomei's House | Xiaomei's |  |  |
| 熊大伯家 | Uncle Xiong's House | Xiong's |  |  |
| 阿旺婆家 | Ah Wang's House | Ah Wang's |  |  |
| 胖大厨家 | Fat Chef's House | Fat Chef's |  |  |
| 通宵虫家 | Nightbug's House | Nightbug's |  | Banner 1-2-15. |
| 虫子家 | Bug's House | Bug's |  | Map 2-2-16 / teleport menu. |
| 小雪家 | Xiaoxue's House | Xiaoxue's |  |  |
| 编程狂家 | Code Nut's House | Code Nut's |  |  |
| 智慧老人家 | Wise Elder's House | Elder's |  |  |
| 万人迷家 | Charmer's House | Charmer's |  |  |
| 阿绣家 | Ah Xiu's House | Ah Xiu's |  |  |
| JAY谜家 | Jay Fan's House | Jay Fan's |  |  |
| SSK家 | SSK's House | SSK's |  |  |
| SSK的家 | SSK's House | SSK's |  | Map 2-6-7. |
| 巫山二老家 | Wushan Den |  |  |  |
| 购物狂家 | Shopaholic's House | Shopaholic |  |  |
| 老婆婆家 | Granny's House | Granny's |  |  |
| 吴老头家 | Old Wu's House | Old Wu's |  |  |
| 一天仇家 | Yi's House |  |  |  |
| 诚信电器家 | Chengxin's House | Chengxin's |  |  |
| 王伯伯家 | Uncle Wang's House | Wang's |  |  |
| 小宝家 | Xiaobao's House | Xiaobao's |  |  |
| 阿呆家 | Ah Dai's House | Ah Dai's |  |  |
| 电脑狂家 | PC Nut's House | PC Nut's |  |  |
| 立白家 | Libai's House | Libai's |  | Also the source's speaker tag (立白家：): write 'Libai:'. |
| 影子猪家 | Shadow Pig's House | Shadow Pig |  |  |
| 纯蓝家 | Chunlan's House | Chunlan's |  |  |
| 玄机真人居 | Xuanji's House | Xuanji's |  |  |
| 水王家 | Flood King's House | Flood King |  | andygzq's house. |
| 平平家 | Pingping's House | Pingping's |  |  |
| 小新家 | Shin-chan's House | Shin-chan |  |  |
| 浊风家 | Zhuofeng's House | Zhuofeng's |  |  |
| 大兔子家 | Big Rabbit's House | Rabbit's |  |  |
| TAD家 | TAD's House | TAD's |  |  |
| 丫丫家 | Yaya's House | Yaya's |  |  |
| 灌水者家 | Flooder's House | Flooder's |  |  |
| 风铃家 | Windchime's House | Windchime |  |  |
| 傻王家 | Silly King's House | Silly King |  |  |
| 冷义家 | Leng Yi's House | Leng Yi's |  |  |
| 希鱼家 | Xiyu's House | Xiyu's |  |  |
| 独孤正家 | Dugu Zheng's House | Dugu Zheng |  |  |
| 老伯伯家 | Old Uncle's House | Uncle's |  |  |
| 方方家 | Fangfang's House | Fangfang's |  |  |
| 芹儿家 | Qin'er's House | Qin'er's |  |  |
| 豆子家 | Douzi's House | Douzi's |  |  |
| 剑酒仙家 | Tipsy Sword's House | Tipsy's |  |  |
| 喜剧之王家 | Comedian's House | Comedian's |  |  |
| 丁风家 | Ding Feng's House | Ding's |  |  |
| 豆豆家 | Doudou's House | Doudou's |  |  |
| 爱国狂家 | Patriot's House | Patriot's |  |  |
| 虫虫飞家 | Flybug's House | Flybug's |  | Map 2-10-1. |
| 阿土伯家 | Uncle Tu's House | Uncle Tu's |  |  |
| 小旺家 | Xiaowang's House | Xiaowang's |  |  |
| 木次一郎家 | Ichiro's House | Ichiro's |  |  |
| 狗犬次朗家 | Jiro's House | Jiro's |  |  |
| 干腾槟榔家 | Binro's House | Binro's |  |  |
| 诡踪堡 | Stealth Fort |  |  | Lore name in GRS 6-2-17 (the Night Garb 诡踪衣 is its black garb). (added in review) |
| 火焰山 | Flaming Mountain |  |  | Journey to the West's Flaming Mountain (GRS 6-8-6, 6-8-28). (added in review) |

## Monsters and enemy labels

| zh | en | short | alt | note |
|---|---|---|---|---|
| 圣水兽 | Water Beast |  | Sacred Water Beast | Boss at the bottom of the Bright Peak well (1-5-5), with an absurd system-tip backstory (Chiyou, the Flame Emperor). ARS 3-3-54. |
| 大眼怪 | Bigeye |  | Big-Eyed Monster | The monster who carried off the monk (1-1-7), later dying in the Bloom Maze (1-5-4) and avenged at Blight's Den (1-7-10). Leaves the Doll Lamp. |
| 小日本 | Japanese Thug | Thug |  | ARS 3-3-48 and dialogue: a Chinese slur, softened by the owner's decision: 'the Japanese' in dialogue, never 'Jap'. See Decision 10. ARS 3-3-48 keeps the short 'Thug' (11-char field; the fight is on Japan Island). |
| 魂魄守护神 | Soul Guardian |  |  | Training maze boss (1-100-1). |
| 五行金 | Metal |  | Metal Guardian | Guardian of the Metal Maze (1-40-1); tag 'Metal:'. ARS 3-3-57 金. |
| 五行木 | Wood |  | Wood Guardian | Wood Maze (1-40-2). |
| 五行水 | Water |  | Water Guardian | Water Maze (1-40-3). |
| 五行土 | Earth |  | Earth Guardian | Earth Maze (1-40-4). |
| 开始纯蓝 | Chunlan |  |  | ARS 3-3-16: the first Chunlan Guardian fight (开始 'start'). |
| 药1 | Herb 1 |  |  | ARS 3-3-17..21: pagoda monsters carrying the five herbs. |
| 药2 | Herb 2 |  |  |  |
| 药3 | Herb 3 |  |  |  |
| 药4 | Herb 4 |  |  |  |
| 药5 | Herb 5 |  |  |  |
| 武1 | Fighter 1 |  |  | Tournament opponents (ARS 3-3-32..41). |
| 武2 | Fighter 2 |  |  |  |
| 武3 | Fighter 3 |  |  |  |
| 武4 | Fighter 4 |  |  |  |
| 武5 | Fighter 5 |  |  |  |
| 武-6 | Fighter-6 |  |  |  |
| 武7 | Fighter 7 |  |  |  |
| 武8 | Fighter 8 |  |  |  |
| 武9 | Fighter 9 |  |  |  |
| 武10 | Fighter 10 |  |  |  |
| 巫山1 | Wushan 1 |  |  |  |
| 巫山2 | Wushan 2 |  |  |  |
| 龙 | Dragon |  |  |  |
| 骗子-53 | Scammer-53 |  |  | Forum scammers (net cafe task). |
| 父亲-55 | Father-55 |  |  | Mo Jingchou, first form. |
| 最后-56 | Final-56 |  |  |  |
| 金 | Metal |  |  | ARS 3-3-57 (Metal Maze guardian). |
| 木 | Wood |  |  | ARS 3-3-58. |
| 土 | Earth |  |  | ARS 3-3-60 (3-3-59 水 is the item 水 'Water'). |
| 捣乱 | Troll |  |  | ARS 3-3-63: forum troll. |
| 水魔 | Water Demon |  |  | The demon that turns the water black on Mt. Hua (1-1-5, 1-6-7, GRS 6-14-48); SSK's Tianshan Holy Water beats it. Not the Water Beast (圣水兽) of Well Bottom. (added in review) |
| 火龙兽 | Fire Dragon Beast |  |  | Guardian of the Bright Peak well treasure in Xiaobao's secret (1-7-4). (added in review) |

## Items

| zh | en | short | alt | note |
|---|---|---|---|---|
| 外语通 | Waiyutong |  |  | GRS 6-14-12 (item name): BBK's 外语通9188 dictionary. In dialogue 外语通9188 = 'Waiyutong 9188' or 'the 9188'. |
| A100 | A100 |  |  | BBK e-dictionary (item 6-14-8). |
| 4980 | 4980 |  |  | BBK e-dictionary (item 6-14-9). |
| 5980 | 5980 |  |  | BBK e-dictionary (item 6-14-10). |
| 6980 | 6980 |  |  | BBK e-dictionary (item 6-14-11). |
| 名菡秘籍 | Minghan Manual | Minghan |  | The martial manual everyone fights over (GRS 6-14-42 short 'Minghan'). 名菡 comes from its creators' names (花雷名 and 陈夏菡, MRS 4-1-54). Source also writes 名菡密集 once. |
| 名菡密集 | Minghan Manual |  |  | Typo of 名菡秘籍 in the mother's letter. |
| 信 | Letter |  |  | Several letters (6-14-1/2/39/46/55). |
| 家书 | Kin Letter |  | letter home | Letter from Mrs. Pu's husband (6-14-21); a letter with money (6-14-59). In dialogue 'letter home'. |
| 香 | Incense |  |  | Incense to burn for the Dragon King. |
| U盘 | USB Stick |  |  | Carries BBK's new RPG dev kit. |
| 水 | Water |  |  |  |
| 花 | Flower |  |  |  |
| 菜刀 | Cleaver |  |  | Kitchen cleaver (also 88 of them build your sect). |
| 藏宝图 | Trove Map |  | treasure map | Six maps; the Little Prodigy translates the old one. |
| 线团 | Thread |  |  | Fishing-rod material. |
| 竹竿 | Bamboo |  | bamboo pole | Fishing-rod material. |
| 包子 | Steam Bun |  | bun | The spicy bun and the sweetest bun (Xiaoxian / Zhao Si). |
| 香蕉叶 | Banana Leaf | Banana Lf |  | GRS 6-14-24 (10) short 'Banana Lf'; ARS 3-3-15 fits 'Banana Leaf'. |
| 七里香 | Sevenmile |  |  | The village's famous wine, 'its scent carries seven li'. (Also a 2004 Jay Chou album title, not the reference here.) |
| 石头 | Stone |  |  |  |
| 黑铁矿 | Black Iron |  |  | Ore. |
| 玄铁矿 | Dark Iron |  |  | Ore (jy uses Dark Iron for 玄铁). |
| 乌金矿 | Black Gold |  |  | Ore. |
| 青蛙布 | Frog Cloth |  |  | Cloth for weapon grips and the wife's knitting. |
| 醒神果 | Wake Fruit |  |  | Herb for the father's cure (five herbs from the pagoda: Wake Fruit, Butter Tea, Jade Peony, Red Azalea, Red Whisk). |
| 酥油茶 | Butter Tea |  |  | Herb. |
| 绿牡丹 | Jade Peony |  | green peony | Herb. |
| 红杜鹃 | Red Azalea |  |  | Herb. |
| 红拂 | Red Whisk |  |  | Herb. |
| 神龙鼎 | Dragon Cauldron | Cauldron |  | Divine cauldron on Rock Hill; needed with Samadhi Fire to brew the cure. |
| 三味真火 | Samadhi Fire | True Fire |  | The divine fire (三昧真火; the source writes 三味). Bought at the mall if you miss it. |
| 万灵丹 | Cure-All |  |  | Doctor Wan's medicine. |
| 纸条 | Note |  |  | Father's note in the letter: '灭五大派 上光明顶 夺名菡秘籍 父亲 留' = 'Destroy the five sects. Climb Bright Peak. Take the Minghan Manual. - Father'. |
| 宠物蛋 | Pet Egg |  |  |  |
| 长命香 | Life Joss |  | longevity incense | Each use: one year younger in age, one hour more on the game clock. (Pharmacy menu 'Life-Joss'.) |
| 毒药 | Poison |  |  | The opposite of Life Joss. |
| 魂之魄 | Soul Wisp |  |  | 88 needed in the training maze (ARS 3-3-23 too). |
| CD碟 | CD |  |  | Jay's album CD. |
| 天山神水 | Holy Water |  | Tianshan Holy Water | SSK's potion against the Water Demon (水魔). Item name 'Holy Water'; in dialogue 'Tianshan Holy Water'. |
| 钥匙 | Key |  |  | As in szzm. |
| 飞行符 | Fly Charm |  |  | Teleport charms (to Central / North / South / West (45,45), East (11,4)). |
| 灵魂珠 | Soul Orb |  |  | Bigeye's orb. |
| 玫瑰花 | Rose |  |  | +1 affection. |
| 电池 | Batteries |  |  |  |
| 夜明珠 | Glow Pearl |  | night pearl | Big Rabbit's heirloom. |
| 驱魔香 | Repel Joss |  |  | No encounters until you change maps. |
| 遇敌香 | Lure Joss |  |  | Encounters on demand. |
| 霸王钟 | Tyrantbell |  | Tyrant Bell | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Tyrant Bell' is the long form for prose. |
| 棉线 | Thread |  | cotton thread | Old Wang's word for the Fishpole material (1-2-2); the item is 线团 'Thread'. (added in review) |

## Weapons

| zh | en | short | alt | note |
|---|---|---|---|---|
| 钓竿 | Fishpole |  | fishing rod | As in yxts. Old Wang makes one from Thread and Bamboo. |
| 不名剑 | Junk Sword |  |  | 'A shoddy sword, maker unknown.' |
| 羽毛剑 | Plumeblade |  |  |  |
| 九节棍 | Nine Staff |  | nine-section staff |  |
| 龙腾剑 | Dragonrise |  |  |  |
| 裁决之杖 | Judgment |  | Staff of Judgment | A Warrior weapon from Legend of Mir. |
| 钨龙刀 | Tungsten |  |  |  |
| 小刀 | Knife |  |  |  |
| 旋风剑 | Whirlwind |  |  |  |
| 屠魔剑 | Demonbane |  |  | Not 斩妖剑 Fiendslayer. |
| 芙蓉剑 | Hibiscus |  |  |  |
| 无影剑 | Shadowless |  |  |  |
| 幽真剑 | Enigma |  |  |  |
| 尺骨刀 | Ulna Blade |  |  |  |
| 斩妖剑 | Fiendbane |  | Fiendslayer | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Fiendslayer' is the long form for prose. |
| 龙吟剑 | Dragonsong |  |  | As in fmj (same BBK item/skill set). |
| 辟魔剑 | Peachwood |  | Demonward Sword | As in fmj (same BBK item/skill set). |
| 催眠剑 | Lull Sword |  | Sleep Sword | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Sleep Sword' is the long form for prose. |
| 七星剑 | Star Sword |  | Seven Star Sword | As in fmj (same BBK item/skill set). |
| 嗜血剑 | Bloodlust |  | Bloodthirst | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Bloodthirst' is the long form for prose. |
| 九龙道剑 | Ninedragon |  | Nine Dragon | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Nine Dragon' is the long form for prose. |
| 砍刀 | Machete |  |  | As in fmj (same BBK item/skill set). |
| 佩刀 | Saber |  |  | As in fmj (same BBK item/skill set). |
| 弯月刀 | Crescent |  | Crescent Blade | As in fmj (same BBK item/skill set). |
| 莲花刀 | Lotusblade |  | Lotus Blade | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Lotus Blade' is the long form for prose. |
| 魔哭刀 | Demonwail |  |  | As in fmj (same BBK item/skill set). |
| 移魂刀 | Soulshift |  |  | As in fmj (same BBK item/skill set). |
| 双手剑 | Twin Sword |  | Twin Swords | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Twin Swords' is the long form for prose. |
| 明目双剑 | Keen Twins |  |  | As in fmj (same BBK item/skill set). |
| 姐妹剑 | Sisters |  | Sister Pair | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Sister Pair' is the long form for prose. |
| 碧玉双剑 | Jade Twins |  |  | As in fmj (same BBK item/skill set). |
| 阴阳双剑 | Yin Yang |  | Yin-Yang Twins | As in fmj (same BBK item/skill set). |

## Armor and accessories

| zh | en | short | alt | note |
|---|---|---|---|---|
| 青铜头盔 | Bronze Cap |  |  |  |
| 铜头盔 | Copper Cap |  |  |  |
| 铁头盔 | Iron Helm |  |  |  |
| 钢头盔 | Steel Helm |  |  |  |
| 不锈钢盔 | Stainless |  | stainless-steel helm |  |
| 混凝土盔 | Cement Cap |  | concrete helm | The desc runs a joke ('...everyone in the universe knows. ...Waah~ I don't know.'). |
| 记忆头盔 | Mind Helm |  | Memory Helm |  |
| 祈祷头盔 | Pray Helm |  | Prayer Helm |  |
| 神秘头盔 | Mystic Cap |  |  |  |
| 黑铁头盔 | Black Helm |  |  |  |
| 牛头盔 | Ox Helm |  |  | Made from the Bull Demon King's horns. |
| 兔兔头盔 | Bunny Helm |  |  |  |
| 黑衣 | Black Garb |  |  |  |
| 忍者衣 | Ninja Garb |  |  |  |
| 圣袍 | Saint Robe |  |  | Not 朝圣衣 'Holy Robe'. |
| 霓裳羽衣 | Plume Gown |  | Rainbow Feather Gown |  |
| 乾坤衣 | World Coat |  |  |  |
| 手套 | Gloves |  |  |  |
| 金箍圈 | Gold Hoop |  |  | Sun Wukong's band. |
| 娃娃灯 | Doll Lamp |  |  | Bigeye's keepsake. |
| 金项链 | Gold Chain |  |  |  |
| 铜项链 | Brass Torc |  | bronze necklace |  |
| 避邪项链 | Ward Chain |  |  |  |
| 月亮镜 | Moonmirror |  |  |  |
| 祈祷项链 | Pray Chain |  |  |  |
| 恶魔铃铛 | Demon Bell |  |  |  |
| 狂暴项链 | Fury Chain |  |  |  |
| 不明链 | Odd Chain |  |  |  |
| 避邪冠 | Ward Crown |  |  | As in fmj (same BBK item/skill set). |
| 蓝玉冠 | Jade Crown |  | Azure Crown | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Azure Crown' is the long form for prose. |
| 防毒面罩 | Toxin Mask |  | Gas Mask | As in fmj (same BBK item/skill set). |
| 皮甲 | Hide Armor |  |  | As in fmj (same BBK item/skill set). |
| 百练衣 | Snakeskin |  |  | As in fmj (same BBK item/skill set). |
| 天师法衣 | Sage Robe |  | Celestial Master's Vestment | As in fmj (same BBK item/skill set). |
| 金缕衣 | Jade Suit |  | Gold-Thread Jade Suit | As in fmj (same BBK item/skill set). |
| 渺影衣 | Shadowsilk |  |  | As in fmj (same BBK item/skill set). |
| 火羽衣 | Flame Robe |  | Fire Feather Robe | As in fmj (same BBK item/skill set). |
| 朝圣衣 | Holy Robe |  | Pilgrim Robe | As in fmj (same BBK item/skill set). |
| 鬼针胃 | Spike Mail |  | Barbed Mail | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Barbed Mail' is the long form for prose. |
| 天蛛丝衣 | Spidersilk |  | Spider Silk | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Spider Silk' is the long form for prose. |
| 珍珠衫 | Pearl Vest |  | Pearl Shirt | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Pearl Shirt' is the long form for prose. |
| 避毒衣 | Swan Robe |  | Antitoxin Robe | As in fmj (same BBK item/skill set). |
| 诡踪衣 | Night Garb |  | Stealth Garb | As in fmj (same BBK item/skill set). |
| 潮海衣 | Tide Robe |  | Ocean Robe | As in fmj (same BBK item/skill set). |
| 草鞋 | Sandals |  | Straw Shoes | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Straw Shoes' is the long form for prose. |
| 布鞋 | Soft Boots |  | Cloth Shoes | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Cloth Shoes' is the long form for prose. |
| 道靴 | Tao Boots |  | Taoist Boots | As in fmj (same BBK item/skill set). |
| 长寿靴 | Life Boots |  | Longevity Boots | As in fmj (same BBK item/skill set). |
| 霸王靴 | Iron Boots |  | Steel Boots | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Steel Boots' is the long form for prose. |
| 追风靴 | Windchaser |  | Windchasers | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Windchasers' is the long form for prose. |
| 花布鞋 | Rose Shoes |  | Print Shoes | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Print Shoes' is the long form for prose. |
| 闺秀鞋 | Lady Shoes |  |  | As in fmj (same BBK item/skill set). |
| 鹿皮靴 | Deerskins |  |  | As in fmj (same BBK item/skill set). |
| 莲花靴 | Lotus Boot |  | Lotus Boots | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Lotus Boots' is the long form for prose. |
| 夜光靴 | Glow Boots |  |  | As in fmj (same BBK item/skill set). |
| 灵狐靴 | Fox Boots |  |  | As in fmj (same BBK item/skill set). |
| 登天泥鞋 | Skyclimber |  | Skyclimbers | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Skyclimbers' is the long form for prose. |
| 御风草鞋 | Windriders |  |  | As in fmj (same BBK item/skill set). |
| 乾坤游步 | Worldwalk |  | Cosmos Walk | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Cosmos Walk' is the long form for prose. |
| 披风 | Cape |  | Cloak | As in fmj (same BBK item/skill set). |
| 肩甲 | Pauldrons |  |  | As in fmj (same BBK item/skill set). |
| 青铜铠 | Bronzemail |  | Bronze Mail | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Bronze Mail' is the long form for prose. |
| 软蛟披风 | Wyrm Cape |  |  | As in fmj (same BBK item/skill set). |
| 铁鳞甲 | Scale Mail |  |  | As in fmj (same BBK item/skill set). |
| 金钢肌 | Steel Mail |  | Steel Plate | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Steel Plate' is the long form for prose. |
| 圣斗甲 | Saint Mail |  | Saint Cloth | As in fmj (same BBK item/skill set). |
| 青雷战衣 | Storm Coat |  | Green Thunder Coat | As in fmj (same BBK item/skill set). |
| 圣洁披风 | Holy Cape |  |  | As in fmj (same BBK item/skill set). |
| 御灵道袍 | Soul Robe |  | Spirit Robe | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Spirit Robe' is the long form for prose. |
| 神龙披风 | Dragoncape |  | Dragon Cape | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Dragon Cape' is the long form for prose. |
| 凤纹披风 | Plume Cape |  | Phoenix Cape | As in fmj (same BBK item/skill set). |
| 芦藤雌甲 | Reedmail F |  | Reed Mail F | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Reed Mail F' is the long form for prose. |
| 芦藤雄甲 | Reedmail M |  | Reed Mail M | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Reed Mail M' is the long form for prose. |
| 布护腕 | Cloth Cuff |  | Cloth Cuffs | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Cloth Cuffs' is the long form for prose. |
| 避血手腕 | Blood Cuff |  | Blood Cuffs | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Blood Cuffs' is the long form for prose. |
| 赤镯 | Red Bangle |  |  | As in fmj (same BBK item/skill set). |
| 玉镯 | Jade Ring |  | Jade Bangle | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Jade Bangle' is the long form for prose. |
| 飞天镯 | Sky Bangle |  | Apsara Bangle | As in fmj (same BBK item/skill set). |
| 吸灵镯 | Soul Ring |  | Soul Bangle | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Soul Bangle' is the long form for prose. |
| 长命锁 | Life Lock |  |  | As in fmj (same BBK item/skill set). |
| 象牙坠 | Ivory Tusk |  | Ivory Pendant | As in fmj (same BBK item/skill set). |
| 寒冰玉佩 | Frost Jade |  |  | As in fmj (same BBK item/skill set). |
| 定神珠 | Calm Pearl |  | Focus Pearl | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Focus Pearl' is the long form for prose. |
| 富贵珠 | Luck Pearl |  | Fortune Pearl | As in fmj (same BBK item/skill set). |
| 紫瞳魔灯 | Violet Eye |  | Violet Lamp | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Violet Lamp' is the long form for prose. |
| 天心灯 | Heart Lamp |  | Heaven Lamp | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Heaven Lamp' is the long form for prose. |
| 玄冰玉如意 | Frost Ruyi |  | Black Ice Jade Ruyi | As in fmj (same BBK item/skill set). |

## Consumables and throwables

| zh | en | short | alt | note |
|---|---|---|---|---|
| 千年朱果 | Ruby Fruit |  |  |  |
| 寒冰蛙 | Ice Frog |  |  |  |
| 飞蝗石 | Hurl Stone |  |  |  |
| 降魔符 | Demonward |  |  |  |
| 寒铁钉 | Iron Spike |  |  |  |
| 穿心镖 | Heart Dart |  |  |  |
| 唤风符 | Wind Charm |  |  |  |
| 召雷符 | Bolt Charm |  |  |  |
| 宇冰符 | Ice Charm |  |  |  |
| 囤土符 | Soil Charm |  |  |  |
| 狱火符 | Fire Charm |  |  |  |
| 七步蛇毒 | Asp Venom |  |  |  |
| 六毒蚀脏粉 | Six Venoms |  |  |  |
| 勾魂散 | Soul Hook |  |  | The 1-1-4 message writes 钩魂散. |
| 钩魂散 | Soul Hook |  |  | Variant of 勾魂散. |
| 迷君杉 | Siren Dust |  |  | Messages write 迷君衫. |
| 迷君衫 | Siren Dust |  |  | Variant. |
| 七杳草根 | Sleep Root |  |  |  |
| 平安糕 | Peace Cake |  |  | Sect task and Xiaoxue's errand. |
| 糖葫芦 | Sugar Haws |  | candied haws | As in yxts. |
| 紫竹符 | Cane Charm |  |  |  |
| 九正墨玉丹 | Jet Pill |  |  |  |
| 地补符 | Mend Charm |  |  |  |
| 青仙果 | Jade Fruit |  |  | Ah Dai's cold remedy. |
| 回神丹 | Mind Pill |  |  |  |
| 飘仙果 | Fairyberry |  |  |  |
| 紫荦杉 | Mind Balm |  |  |  |
| 茶叶蛋 | Tea Egg |  |  |  |
| 烤鹿肉 | Venison |  |  |  |
| 田七精 | Sanchi |  |  |  |
| 雌雄葫芦 | Twin Haws |  |  |  |
| 魔王须 | Devilbeard |  |  |  |
| 天山盐 | Rock Salt |  |  |  |
| 华山针树叶 | Needleleaf |  |  |  |
| 菊黄散 | Mum Powder |  |  |  |
| 清凉油 | Cool Balm |  |  |  |
| 灵芝草 | Lingzhi |  |  | As in jy / yzcq. |
| 幽灵灯 | Ghost Lamp |  |  |  |
| 悔罪汤 | Repent Tea |  |  | As in yzcq. |
| 原始延命香 | Joss Stick |  |  | As in yzcq. |
| 梅花镖 | Plum Dart |  |  | As in fmj (same BBK item/skill set). |
| 袖里剑 | Cuff Blade |  | Sleeveblade | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Sleeveblade' is the long form for prose. |
| 旋魂铊 | Soulspin |  | Soulspinner | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Soulspinner' is the long form for prose. |
| 青蛇卵 | Snake Egg |  |  | As in fmj (same BBK item/skill set). |
| 童尸肉 | Ghoul Meat |  | Corpse Meat | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Corpse Meat' is the long form for prose. |
| 红蝎卵 | Sting Egg |  | Scorpion Egg | As in fmj (same BBK item/skill set). |
| 蜘蛛卵 | Spider Egg |  |  | As in fmj (same BBK item/skill set). |
| 毒铁菱 | Caltrops |  | Poison Caltrops | As in fmj (same BBK item/skill set). |
| 蚀毒砂 | Venom Sand |  |  | As in fmj (same BBK item/skill set). |
| 缠魂丝 | Soul Silk |  |  | As in fmj (same BBK item/skill set). |
| 定魂旗 | Bind Flag |  | Bind Banner | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Bind Banner' is the long form for prose. |
| 缚龙索 | Dragonbind |  | Dragon Rope | As in fmj (same BBK item/skill set). |
| 太极符 | Taiji Seal |  | Taiji Charm | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Taiji Charm' is the long form for prose. |
| 火毛虫 | Fire Grub |  |  | As in fmj (same BBK item/skill set). |
| 罗喉针 | Rahu Pin |  | Rahu Needle | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Rahu Needle' is the long form for prose. |
| 石矶珠 | Shiji Bead |  | Shiji Pearl | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Shiji Pearl' is the long form for prose. |
| 玉蓝草 | Jadegrass |  |  | As in fmj (same BBK item/skill set). |
| 赤玉断续膏 | Ruby Salve |  |  | As in fmj (same BBK item/skill set). |
| 菊花酒 | Mum Wine |  |  | As in fmj (same BBK item/skill set). |
| 魔王甲 | Kingbeetle |  | King Beetle | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'King Beetle' is the long form for prose. |
| 西域奇糯 | Tibet Rice |  | Exotic Rice | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Exotic Rice' is the long form for prose. |
| 黑狐甲 | Fox Beetle |  |  | As in fmj (same BBK item/skill set). |
| 千里飘 | Farscent |  |  | As in fmj (same BBK item/skill set). |
| 净衣符 | Pure Charm |  |  | As in fmj (same BBK item/skill set). |
| 定心符 | Calm Charm |  |  | As in fmj (same BBK item/skill set). |
| 枸杞仙果 | Goji Berry |  |  | As in fmj (same BBK item/skill set). |
| 八仙石 | Fairystone |  | Fairy Stone | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Fairy Stone' is the long form for prose. |
| 霸王花 | Cereus |  |  | As in fmj (same BBK item/skill set). |
| 金鍪 | Gold Cap |  |  | As in fmj (same BBK item/skill set). |
| 无忧仙丹 | Bliss Pill |  | Carefree Pill | As in fmj (same BBK item/skill set). |
| 珠仙草 | Pearlweed |  |  | As in fmj (same BBK item/skill set). |
| 玄冥草 | Netherweed |  |  | As in fmj (same BBK item/skill set). |
| 无妄草 | Fateweed |  |  | As in fmj (same BBK item/skill set). |
| 佛天圆 | Sarira |  |  | As in fmj (same BBK item/skill set). |
| 天玉菩提 | Bodhi Seed |  |  | As in fmj (same BBK item/skill set). |
| 玉银杏宝 | Ginkgo Nut |  |  | As in fmj (same BBK item/skill set). |
| 罗汉笑 | Arhat Grin |  | Arhat Smile | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Arhat Smile' is the long form for prose. |
| 金毛虫 | Gold Grub |  |  | As in fmj (same BBK item/skill set). |
| 生龙活虎丹 | Vigor Pill |  |  | As in fmj (same BBK item/skill set). |
| 龟甲散 | Shell Dust |  |  | As in fmj (same BBK item/skill set). |
| 飘飘香 | Airy Scent |  |  | As in fmj (same BBK item/skill set). |
| 战狂石 | Rage Stone |  |  | As in fmj (same BBK item/skill set). |
| 子金光符 | Glow Charm |  | Glare Charm | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Glare Charm' is the long form for prose. |
| 飓行草 | Galeweed |  |  | As in fmj (same BBK item/skill set). |
| 引路石 | Guidestone |  | Guide Stone | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Guide Stone' is the long form for prose. |

## Skills and arts

| zh | en | short | alt | note |
|---|---|---|---|---|
| 太阳拳 | Sun Fist |  |  |  |
| 横气斩 | Sweep Slash |  |  |  |
| 剑气斩 | Qi Slash |  |  |  |
| 圣龙诀 | Holy Dragon |  |  |  |
| 小半月斩 | Half Moon |  |  |  |
| 大半月斩 | Half Moon+ |  |  |  |
| 九阴一骨爪 | Yin Claw |  |  | A play on 九阴白骨爪 (jy Bone Claw). |
| 魔爪乱舞 | Claw Frenzy |  |  |  |
| 鬼哭神嚎 | Ghost Wail |  |  |  |
| 漫天花羽 | Petal Storm |  |  |  |
| 冰心咒 | Ice Heart |  |  |  |
| 一阳指 | Yang Finger |  | One Yang Finger | Dali art taught by the Beggars here. |
| 小弯月斩 | Moon Slash |  |  |  |
| 大弯月斩 | Moon Slash+ |  |  |  |
| 气功波 | Qigong Wave |  |  | Desc: 'only in Dragon Ball - how did it get into Xiake?'. |
| 龟派气功 | Kamehameha |  |  | The Chinese name of Goku's Kamehameha (Master Roshi's art). |
| 瘴气攻击 | Miasma |  |  | Desc joke: really foot odour. |
| 雷电术 | Lightning |  |  |  |
| 御钟术 | Bell Drop |  |  |  |
| 噬灵虫咒 | Soul Bugs |  |  |  |
| 龙卷风 | Tornado |  |  | Hero Sect signature. |
| 圣之光环 | Holy Halo |  |  |  |
| 擒拿手 | Grappling |  | Seizing Hands | As in jy. |
| 圣火令 | Holy Flame |  |  |  |
| 飞剑斩 | Flyblade |  |  |  |
| 莫名拳 | Mo Fist |  | Mo family fist | The hero's family fist (starting choice). |
| 莫名心法 | Mo Mind Art |  |  | The hero's family healing art (starting choice). |
| 删帖大法 | Delete Post |  |  | Flybug's art: forum moderation as kung fu. |
| 九天狂雷 | Sky Thunder |  | Nine Heavens Thunder | The Minghan Manual's ultimate move, needed to power the Dictionary Array. |
| 血刀毒杀 | Blood Blade |  |  |  |
| 天雷落 | Thunderfall |  |  |  |
| 桃花剑法 | Peach Sword |  |  |  |
| 飞心术 | Heartflight |  |  |  |
| 降魔符法 | Warding |  |  |  |
| 妙手回春 | Rejuvenate |  |  |  |
| 群疗术 | Mass Heal |  |  |  |
| 血气方刚 | Hot Blood |  |  |  |
| 回生术 | Revive |  |  |  |
| 吸星大法 | Star Absorbing |  | Star-Absorbing Art | Demon Cult showgut (Jin Yong's 吸星大法). |
| 打狗棒法 | Dog Beater |  | Dog-Beating Staff | As in jy (Beggars' showgut). |
| 降龙十八掌 | 18 Dragons |  | Eighteen Dragon-Subduing Palms | As in jy. |
| 独孤九剑 | Dugu Nine |  | Nine Swords of Dugu | As in jy (Huashan showgut). |
| 炎龙覆天 | Fire Dragon |  | Flame Dragon | As in fmj. Showgut writes 炎龙覆雨. Menu form = en (the field limit); 'Flame Dragon' is the long form for prose. |
| 火雷破空 | Firebolt |  | Fire Thunder Burst | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Fire Thunder Burst' is the long form for prose. |
| 五鬼乱神 | Five Ghosts |  | Five Ghost Chaos | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Five Ghost Chaos' is the long form for prose. |
| 八门金锁 | Eight Gates |  | Eight Gate Lock | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Eight Gate Lock' is the long form for prose. |
| 剪刀剑气 | Scissor Qi |  | Scissor Sword Qi | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Scissor Sword Qi' is the long form for prose. |
| 傲剑诀 | Proud Sword |  | Proud Sword Mantra | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Proud Sword Mantra' is the long form for prose. |
| 独孤刀 | Lone Blade |  |  | As in fmj (same BBK item/skill set). |
| 剑气术 | Sword Qi |  | Sword Aura | As in fmj (same BBK item/skill set). |
| 狂刀斩 | Mad Slash |  | Mad Blade Slash | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Mad Blade Slash' is the long form for prose. |
| 神剑御魔 | Divine Ward |  | Divine Demonward | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Divine Demonward' is the long form for prose. |
| 人剑合一 | Sword Unity |  | One With the Sword | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'One With the Sword' is the long form for prose. |
| 万剑归一 | All Swords |  | All Swords As One | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'All Swords As One' is the long form for prose. |
| 破天一剑 | Skyrender |  | Sky-Rending Sword | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Sky-Rending Sword' is the long form for prose. |
| 火旋灯 | Pinwheel |  | Fire Pinwheel | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Fire Pinwheel' is the long form for prose. |
| 烈火旋灯 | Blaze Wheel |  | Blazing Pinwheel | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Blazing Pinwheel' is the long form for prose. |
| 冰咒 | Ice Spell |  |  | As in fmj (same BBK item/skill set). |
| 飞岩术 | Flying Rock |  | Flying Rocks | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Flying Rocks' is the long form for prose. |
| 火龙掌 | Fire Palm |  | Fire Dragon Palm | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Fire Dragon Palm' is the long form for prose. |
| 风咒 | Wind Spell |  |  | As in fmj (same BBK item/skill set). |
| 御虫咒 | Bug Swarm |  |  | As in fmj (same BBK item/skill set). |
| 魔域炼火 | Hellfire |  | Demon Realm Fire | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Demon Realm Fire' is the long form for prose. |
| 御蜂咒 | Bee Swarm |  |  | As in fmj (same BBK item/skill set). |
| 凤舞九天 | Sky Phoenix |  | Phoenix Dance | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Phoenix Dance' is the long form for prose. |
| 天火烈焰 | Skyblaze |  | Skyfire Blaze | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Skyfire Blaze' is the long form for prose. |
| 五煞齐出 | Five Fiends |  | Five Fiends Strike | As in fmj (same BBK item/skill set). Menu form = en (the field limit); 'Five Fiends Strike' is the long form for prose. |
| 百虫欺天 | Sky Swarm |  | Swarm Over Heaven | As in fmj (short Sky Swarm in the skill field). Nightbug's art: 'summons N bugs'. Menu form = en (the field limit); 'Swarm Over Heaven' is the long form for prose. |
| 魔音 | Demon Song |  |  | As in fmj (same BBK item/skill set). |
| 玄籁之音 | Mystic Echo |  |  | As in fmj (same BBK item/skill set). |
| 气疗术 | Qi Heal |  |  | As in fmj (same BBK item/skill set). |

## Skills (field)

| zh | en | short | alt | note |
|---|---|---|---|---|
| 妙手空空 | Pickpocket |  |  | The steal skill (Martial Hall, 10000 yuan). The intro's tip: 'use Pickpocket a lot'. Needed to take the herbs from the pagoda monsters. |

## Other terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 纯蓝工作室 | Chunlan Studio | Studio |  | The developers (credits 1-0-2 / 1-0-5 / 1-0-6, the hidden studio room 1-20-5). Credit form 'Chunlan Studio (纯蓝工作室)'. Banner/map 2-20-5 use short 'Studio'. |
| 315200242 | 315200242 |  |  | A tester listed by QQ number (credits); TAD's QQ number (1-8-7). Keep the digits. |
| 毒瘤 | Blight |  |  | See 毒瘤青. |
| 众玩家 | All players |  |  | 1-1-4 joke tag '众玩家：我吐……' 'All players: (retching)...'. |
| 五大门派 | five great sects |  |  | 5大门派 / 五大派: the five sects above. 灭五大派 'Destroy the five sects'. |
| 门派 | sect |  |  | Your sect / a sect. 加入门派 'join a sect'; 灭门派 'destroy a sect'; 建立自己的门派/帮派 'found your own sect'. |
| 帮派 | Sects |  | sect | Same as 门派 in this game (帮派管理处 = the Sect Hall). Map 2-4-7 '帮派' = 'Sects'. |
| 武林 | the martial world |  | wulin | As in jy. |
| 江湖 | the martial world |  | jianghu | As in jy. |
| 武林大会 | Martial Tournament |  |  | Held every five years (系统提示) / ten (the elder says ten); win ten fights in a row (1-1-97). |
| 五行 | Five Elements |  |  | 金木水土 = Metal, Wood, Water, Earth. |
| 步步高 | BBK |  |  | BBK's Chinese brand name. 步步高论坛 = the BBK forum; 步步高网友俱乐部 = the BBK Fan Club. |
| BBK论坛 | BBK forum |  |  | 'support the BBK forum' (支持度 = support rating, range 0-150; 9188 needs some). |
| 步步高论坛 | BBK Forum |  |  | Net cafe menu item 'BBK-Forum'. |
| 步步高网友俱乐部 | BBK Fan Club |  |  | Net cafe menu item 'BBK-Fan-Club'. |
| 电子词典阵 | Dictionary Array |  | Electronic Dictionary Array | The seal: five BBK e-dictionaries in the well at the west end of Worryfree Village draw every demon in the world into it. 'the Electronic Dictionary Array' on first mention, then 'the Dictionary Array'. |
| 词典阵 | Dictionary Array |  |  | Short form. |
| 外语通9188 | Waiyutong 9188 |  | the 9188 | BBK product; keep the model name. |
| 下载王A100 | Download King A100 |  | the A100 | BBK product (下载王 'download king'). Item name 'A100'. |
| 朗文4980 | Longman 4980 |  |  | BBK dictionary with Longman content; item '4980'. Same for 朗文5980 / 朗文6980. |
| 十佳用户 | Top Ten Users |  |  | 'BBK's Top Ten Users of the year' (forum award the hero announces). |
| 叶惠美 | Yeh Hui-Mei |  |  | Jay Chou's 2003 album (named after his mother). Write <Yeh Hui-Mei> with ASCII angle brackets or quotes. |
| RPG开发包 | RPG dev kit |  |  | BBK's RPG development kit (BBKRPG开发包). |
| 侠客正传 | The True Tale of the Xiake |  |  | The game's name for itself in the intro (《侠客正传》); 侠客 alone = 'Xiake' as the game's short name ('the latest Xiake!', 'how did it end up in Xiake'). Title of the release is 侠客行. |
| 侠客 | Xiake |  | knight-errant | (1) the game itself ('玩侠客' 'playing Xiake'); (2) a wandering swordsman. |
| 传奇 | Legend of Mir |  |  | In descriptions 传奇中的... = 'from Legend of Mir' (the MMO), e.g. the Judgment staff 'a Warrior item from Legend of Mir'. |
| 七龙珠 | Dragon Ball |  |  | 气功波 / 龟派气功 descriptions. |
| 泡泡堂 | BnB |  |  | The online game (Crazy Arcade, Chinese title 泡泡堂). |
| 星际 | StarCraft |  |  |  |
| CS | CS |  | Counter-Strike |  |
| 妖魔 | demons |  |  |  |
| 走火入魔 | qi deviation |  |  | 'went astray while training the Minghan Manual' / 'qi deviation'. |
| 御剑术 | Sword Control |  |  | Hua Yingxiong's flying-sword escape. |
| 鱼花石 | Fishbloom Stone |  |  | First of the three Dragon Gate stones on Japan Island (1-1-8): 'System: Leaping the Dragon Gate - the Fishbloom Stone.' (added in review) |
| 圣光石 | Holy Light Stone |  |  | Second Dragon Gate stone (1-1-8). (added in review) |
| 无影石 | Shadowless Stone |  |  | Third Dragon Gate stone (1-1-8). (added in review) |
| 幽冥鬼爪 | Nether Ghost Claw |  |  | Lore art in MRS 4-1-7 (Yin Claw is its top stage). Not a skill-menu name. (added in review) |
| 御魔诀 | Demonward Mantra |  |  | Lore art in MRS 4-1-26 (Divine Ward comes from it). (added in review) |
| 黑白无常 | Black and White Impermanence |  | Death | The two underworld soul-takers (GRS 6-10-2, source 黑白无尝). The 3-row description says 'Death'. (added in review) |
| 日本商人 | merchant |  |  | 1-30-6: the Japanese Official curses the merchant whose shop he sealed, i.e. the Chinese Merchant of 1-3-11 trading on Japan Island; written 'that goddamn merchant', no nationality. (added in review) |
| 火鸣滥圈 | Firecry Ring |  |  | Chiyou's ring that tamed the Water Beast (1-5-5 lore tip). (added in review) |
| 江湖之魄 | Soul of the Martial World |  |  | Fed to the Water Beast (1-5-5 lore tip), with the Myriad-Year Water Essence (万年水痢真元). (added in review) |

## UI, stats and labels

| zh | en | short | alt | note |
|---|---|---|---|---|
| 支持度 | support rating |  |  | Your support for the BBK forum (net cafe). |
| 系统提示 | System |  |  | Speaker tag of the system tips: '系统提示：...' -> 'System: ...'. Also the typo 系统提升. The system has personality ('System: Damn, posting a notice with no money?'). |
| 系统提升 | System |  |  | Typo of 系统提示 (1-10-1, 1-255-56). |
| 精元点 | Essence Points |  | Essence | Free stat points (10 per stat point, 2 for HP/MP). 'You got 100 Essence Points and 8888 yuan.' |
| 精元 | Essence |  |  |  |
| 师门点 | Sect Points |  |  | Earned from sect tasks; spent to learn the sect's skills. |
| 剧情点 | Story Points |  |  |  |
| 声望 | Renown |  |  | 声望值 'Renown'. Ranks: 无名小卒 Nobody, 江湖小虾 Small Fry, 后起之秀 Rising Star, 正义少侠 Young Hero, 一代大侠 Great Hero. |
| 无名小卒 | Nobody |  |  | Renown rank 1. |
| 江湖小虾 | Small Fry |  |  | Renown rank 2. |
| 后起之绣 | Rising Star |  |  | Renown rank 3 (绣 typo for 秀). |
| 正义少侠 | Young Hero |  |  | Renown rank 4. |
| 一代大侠 | Great Hero |  |  | Renown rank 5. |
| 感情值 | Affection |  |  | Your affection with the girl (0-100), raised by giving roses. |
| 年龄 | age |  |  | Age system: one year per in-game hour (event timer 7200); Martial Tournament at ages 10, 20...; past the 90s you die of old age. |
| 成人仪式 | Coming-of-Age Rite |  |  | The elder's trial at 18 (menu item 'Coming-of-Age'). |
| 成人 | come of age |  |  | 已经成人了 'You've already come of age.' |
| 元 | yuan |  |  | Money. '8888元' -> '8888 yuan'; 100RMB -> '100 RMB'; 1W / 5W -> '10,000' / '50,000'; 日元 'yen'. Engine label is 'Money:'. |
| 日元 | yen |  |  | 10000 yen = 2500 yuan (the hero's complaint). |
| 挂机 | AFK training |  |  | Martial Hall: idle in the hall for 1 Essence Point a minute. |
| 攻击力 | Attack |  | ATK | Stat (engine 'Attack'); ATK in descriptions (攻击 / 武术 too). |
| 防御力 | Defense |  | DEF | Stat; DEF in descriptions (防御). |
| 身法 | Agility |  | AGI | Stat (engine 'Agility'); AGI in descriptions. |
| 灵力 | Spirit |  | SPI | Stat (engine 'Spirit'); SPI in descriptions (灵 / 灵气 too). |
| 幸运 | Luck |  | LUK | Stat (engine 'Luck'); 吉运 in descriptions = LUK. |
| 吉运 | Luck |  | LUK | Description word for Luck. |
| 生命上限 | Max HP |  |  |  |
| 真气上限 | Max MP |  |  | 真气 = MP. |
| 真气 | MP |  | qi |  |
| 内力 | internal energy |  | MP | As in jy. |
| 自由模式 | Free Mode |  |  | 1-0-7 mode switch. |
| 竞技模式 | Contest Mode |  |  | 1-0-7 mode switch. |
| 安全模式 | Safe Mode |  |  | Repel Joss: no encounters until you change maps. |
| 携带装备 | Carrying |  |  | Look at an enemy (查看): '携带装备：龟甲散' -> 'Carrying: Shell Dust'. |
| GAMEOVER | GAME OVER |  |  |  |
| 58-神医 | 58-Doctor |  |  | ARS label. |
| 59-父亲 | 59-Father |  |  | ARS label. |
| 60-母亲 | 60-Mother |  |  | ARS label. |
| 61-SSK | 61-SSK |  |  | ARS label. |
| 62-纯蓝 | 62-Chunlan |  |  | ARS label. |
| 63-虫虫飞 | 63-Flybug |  |  | ARS label. |
| 64-我自己 | 64-Myself |  |  | ARS label (我自己 'myself'). |
| 诚信-65 | Chengxin-65 |  |  | ARS label. |
| Paladin-66 | Paladin-66 |  |  | ARS label. |
| solfen-67 | solfen-67 |  |  | ARS label. |
| andygzq-68 | andygzq-68 |  |  | ARS label. |
| 灌水者-69 | Flooder-69 |  |  | ARS label. |
| 希鱼-70 | Xiyu-70 |  |  | ARS label. |
| 喜剧之王-71 | Comedy-71 |  |  | ARS label. |
| 11线 | 11-Thread |  |  | ARS label (thread drop). |
| 12-竿 | 12-Pole |  |  | ARS label (bamboo drop). |
| 矿 | Ore |  |  | ARS 3-3-13 / 3-3-14. |
| 混元金斗-2 | Gold Vat-2 |  |  | ARS 3-4-2 scene object (the Fengshen relic 混元金斗). |
| 文字 | Text |  |  | ARS 3-4-3 scene object. |
| 灯-4 | Lamp-4 |  |  | ARS 3-4-4 scene object. |

Placeholder labels kept unchanged (category ui, en = zh): `001`, `002`, `003`, `004`, `005`, `006`, `007`, `008`, `009`, `010`, `011`, `012`, `013`, `014`, `015`, `016`, `017`, `018`, `019`, `020`, `021`, `022`, `023`, `024`, `025`, `026`, `027`, `028`, `029`, `030`, `031`, `032`, `033`, `034`, `035`, `036`, `037`, `038`, `039`, `040`, `041`, `042`, `043`, `044`, `045`, `046`, `047`, `048`, `049`, `050`, `051`, `052`, `53`, `54`, `55`, `56`, `57`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `64`, `65`, `66`, `67`, `68`, `69`, `70`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `79`, `80`, `101`, `102`, `103`, `104`, `105`, `106`, `107`, `108`, `109`, `110`, `111`, `112`, `113`, `114`, `115`, `116`, `117`, `118`, `119`, `120`, `121`, `122`, `123`, `124`, `125`, `126`, `127`, `128`, `129`, `130`, `131`, `132`, `133`, `134`, `135`, `136`, `137`, `138`, `139`, `140`, `141`, `142`, `143`, `144`, `145`, `146`, `147`, `148`, `149`, `150`, `151`, `152`, `153`, `154`, `155`, `201`, `202`, `203`, `204`, `205`, `206`, `207`, `208`, `209`, `210`, `211`, `212`, `213`, `214`, `215`, `216`, `217`, `218`, `219`, `220`, `221`, `222`, `223`, `224`, `225`, `226`, `227`, `228`, `229`, `230`, `231`, `232`, `233`, `234`, `235`, `36`, `237`, `238`, `239`, `240`, `241`, `242`, `243`, `244`, `245`, `246`, `247`, `248`, `249`, `250`, `251`, `252`, `253`, `254`, `255`.
