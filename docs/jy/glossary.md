# 金庸群侠传 English glossary

Status: **draft, decisions made** (no open questions block translation; the reviewer can override any row).
Machine-readable source: `docs/jy/glossary.jsonl` (one term per line: `zh`, `en`, `category`, `count`, `alt`,
`note`, `source_ids`, optional `short`). This page summarises the same data. Story background: `docs/jy/story.md`.

- `count` = how often the zh string occurs as a substring across `work/jy.strings.jsonl` (all kinds). Short terms
  over-count (虎 also matches 虎皮, 剑 matches every sword), so read it as "how common".
- Field limits (from `tools/tl/common.py problems()`): item names (grs.name) <= 10 chars, ARS names (party,
  enemies, crafting results) <= 11, magic names (mrs.name) <= 11, map names <= 12, scene banners (setscenename)
  <= 10, choices <= 19. `en` fits every field the term is used in; when the natural form is longer it is in `alt`.
  `short` exists only where one zh string is used in two fields with different limits, or where a name needs its
  full form in dialogue but a shorter one in an 11-char field (京城 "The Capital" / banner "Capital";
  丁春秋 "Ding Chunqiu" / ARS "Chunqiu").
- All `en`/`alt`/`short` values are plain ASCII (no accents, curly quotes or em dashes; "Xiaolongnu", "Ke Zhen'e").
- Validation (scratch script): every grs.name / ars.name / mrs.name / map.name / setscenename / choice row in the
  table (827 rows) has a term that fits its limit; the 19 skill-animation banner names fit 11. Result: 0 errors.

## Conventions

**Names.** Pinyin without tones, surname first, given name one word (Guo Jing, Huang Rong, Linghu Chong, Yu
Daiyan). Established English renderings are used where they exist (Xiaolongnu, Hong Qigong, Huang Yaoshi,
Ouyang Feng, Zhang Sanfeng, Abbess Miejue). Apostrophes separate syllables where pinyin needs it (Ling'er,
Jing'er, Chong'er, Ke Zhen'e, Yang Chu'er). 阿- names are "Ah X" (Ah Fang, Ah Hong), as in fmj.
Epithets are translated: Eastern Heretic, Western Venom, Southern Emperor, Northern Beggar, Gentleman Sword,
Seven Freaks, Cyclone Mei. Names too long for the 11-char ARS field use (a) the established epithet when there is
one (梅超风 = Cyclone Mei everywhere), else (b) the given name (幻吟风 Yinfeng, 田伯光 Boguang), or (c) a
compound surname (东方不败 Dongfang). Dialogue uses the full name.

**Places.** Mountains "Mt. X" (Mt. Hua, Mt. Wudang, Mt. Emei); sects keep the pinyin of their mountain/palace
(Huashan Sect, Hengshan Sect, Wudang Sect, Lingjiu Palace, Xingxiu Sect, Xuedao Sect) except the ones with a
standard English name (Beggars' Sect, Ancient Tomb, Shaolin Temple, Peach Blossom Island). Cities: The Capital
(unnamed Song capital), Xixia, Dali, Yangzhou; 府 "prefecture" is dropped. Scene banners are 10 chars, so they
drop generic words: X野外 "X outskirts" shows only the place name, sect banners drop "Sect".

**Martial arts.** Translated by meaning, recognisable to wuxia readers, <= 11 chars: Dog Beater, 18 Dragons,
Bone Claw, Sunflower, Evil Ward, Dugu Nine, Qi Dissolve, Nine Yin, Nine Yang, Violet Mist, Taiji Fist. Long
forms (Eighteen Dragon-Subduing Palms, Nine Swords of Dugu...) are in `alt` for dialogue and descriptions.
Patterns: 剑法 = Sword, 掌 = Palm, 拳 = Fist, 爪 = Claw, 杖法 = Staff, 刀法 = Blade, 神功 = (dropped or "Art"),
阵 = Array, 符 = Charm (both as in fmj), 医术 = Heal (Basic / Minor / Mid / Major / Grand / Heng Heal).

**Equipment.** Slot words that fit 10 chars: Pin (hairpin), Helm, Cap, Robe/Coat/Tunic, Boots, Cape, Cuff
(护手 gauntlet/bracer), Ring, Chain (项链 necklace). Top-tier names may drop the slot word (Ghoststep, Godspeed,
Pegasus, Panther, Vermilion). Crafting materials: raw "Skin" -> tanned "Hide" (Ox Skin -> Ox Hide); ore
"Plat/Gold/Iron Ore" -> metal Platinum / Black Gold / Dark Iron; fibre Flax/Cotton/Raw Silk -> cloth
Linen/Calico/Silk.

**Four Symbols** (the altar quests): 青龙 Blue Dragon, 白虎 White Tiger, 朱雀 Vermilion Bird, 玄武 Black
Tortoise (fmj used Red Phoenix / Dark Turtle; jy needs 凤 = Phoenix for 凤翔靴, so 朱雀 takes the standard
"Vermilion Bird").

**Forms of address.** 师傅 = Master, 师兄/师哥 = Brother, 大师兄/大师哥 = Big Brother, 师姊 = Sister, 小师妹 =
Little Sister, 师叔 = Uncle, 太师叔 = Grand-uncle, 师太 = Abbess, 方丈 = Abbot, 长老 = Elder, 掌门 = Sect Head,
大侠 = hero / good sir, 客官 = sir, 姑娘 = Miss, 大妈 = Auntie, 大人 = Your Honor. Humble first-person forms
(在下, 晚辈, 老夫) become plain "I" with tone carried by the sentence. Speaker tags stay "Name: text" (the source
mixes ASCII ':' and full-width '：'; always write ASCII ':').

**Register.** A 2000s hobby fan game (BOSS Studio) stitching Jin Yong scenes onto a sandbox of sects, cities and
fetch quests. Plain modern English with light wuxia flavour. Jin Yong characters should sound like themselves:
Hong Qigong bluff and fatherly, Huang Rong teasing, Zhou Botong childish, Yue Buqun pompous and two-faced, Linghu
Chong easygoing, Feng Qingyang curt, Ping Yizhi cranky ("this old man" only where it adds flavour). Shop and quest
NPCs are stock phrases: keep them short and consistent across the four cities (the same line appears 4x).
Quotations (Yue Fei's 满江红 in the opening scroll, Tao Te Ching chapters, Liu Yong's 衣带渐宽 line) may use an
existing English rendering.

**UI and stats.** Engine strings are identical to fmj's (`bbkrpg/engine_text.JY` reuses the FMJ table), so reuse
the fmj glossary's UI terms. Descriptions: 防御 Defense, 攻击 Attack, 灵力 Spirit, 身法 Agility, 生命 HP,
内力 = MP (内力最大值 = Max MP), 抗毒/抗眠/抗封/抗乱 = resist Poison/Sleep/Silence/Confuse, 回合 turns,
两 taels. GRS descriptions contain literal `\x0d\x0a` (CR LF) sequences in the table (6-2-6, 6-3-4, 6-3-6,
6-6-15): do not copy them into English; let the text wrap.

## Decisions

1. **Game title**: 金庸群侠传 = "Heroes of Jin Yong" (established English name of the 1996 DOS game).
   Logo subtitle 之射雕英雄 = "Condor Heroes" (alt "Legend of the Condor Heroes"); full logo reading "Heroes of
   Jin Yong: Condor Heroes". Short form because the logo is an image with little room.
2. **Title menu**: 新的征程 / 再续前缘 = "New Game" / "Continue", as fmj.
3. **Protagonists**: 幻吟风 = Yinfeng (Huan Yinfeng), 紫灵儿 = Ling'er (Zi Ling'er). Given names in the ARS
   field because "Huan Yinfeng" is 12; the female name follows suit for symmetry. The 1-1-1 choice may show full
   names (fits 19).
4. **Long names in 11-char fields**: epithet > given name > compound surname (Cyclone Mei, Boguang, Dongfang,
   Chunqiu, Shengdi). Dialogue uses full names. Rationale: fmj's given-name rule, but an established epithet is
   more recognisable than a bare given name.
5. **梅超风 = "Cyclone Mei" everywhere** (dialogue too), not "Mei Chaofeng": it fits, and it is the published
   English name; one name avoids two spellings.
6. **Sect names**: pinyin for mountain/palace sects (Huashan, Hengshan, Wudang, Emei, Quanzhen, Lingjiu, Xingxiu,
   Xuedao), English for Beggars' Sect, Ancient Tomb, Shaolin Temple. 血刀门 = "Xuedao Sect" (alt Blood Blade
   Sect) so the sect matches its pinyin peers and the 10-char banner, while the skill 血刀刀法 stays "Blood Blade".
7. **Renegade enemies** (华山叛徒 ...): "Ex-Huashan", "Ex-Wudang" ... ("Huashan Traitor" is 15).
8. **Scene banners**: X野外 shows the place name only (Capital, Xixia, Dali, Yangzhou, Beggars, Lingjiu, Xuedao);
   altar banners show the beast (Dragon, Tiger, Vermilion, Tortoise). No 10-char "X Wilds"/"X Altar" fits all
   four, and a uniform rule beats ad-hoc abbreviations.
9. **京城** = "The Capital" (map, choice, dialogue), banner short "Capital". The source never names the city.
10. **Four Symbols**: Blue Dragon / White Tiger / Vermilion Bird / Black Tortoise (see Conventions).
11. **Equipment slot words**: Cuff for 护手, Chain for 项链, Pin for 发簪/钗; top tiers may drop the slot word.
12. **Signature weapons**: 倚天剑 = Sky Sword (alt Heaven Sword), 屠龙刀 = Dragonbane (alt Dragon Saber),
    玄铁重剑 = Greatsword (alt Heavy Iron Sword); 真武剑/湛卢剑/龙泉剑 keep pinyin (Zhenwu, Zhanlu, Longquan).
    The established English forms are 12+ chars.
13. **Martial-art short names** chosen to fit 11 and stay distinct: 降龙掌 Dragon Palm vs 降龙十八掌 18 Dragons;
    灭剑/绝剑 = Extinction / Severance (the two halves of Miejue's sword); 化功大法 Qi Dissolve; 辟邪剑法 Evil Ward.
14. **Materials**: raw Skin vs tanned Hide; ores named Plat/Gold/Iron Ore so the metal names (Platinum, Black
    Gold, Dark Iron) stay full.
15. **Tickets** keep the source numbering (Ticket 1..12, descriptions give routes); 银票1/2 are named by value
    (Note 1000 / Note 2000) because the descriptions say so and the Yue Fei's Sword quest needs the 2000s.
16. **fmj template leftovers** (ARS 3-2-x: 无机道人, 袁萍芷, 三清游人1..6, 通宵虫 ...): never displayed by jy's
    scripts (only their sprites are reused), so they keep the fmj glossary's English unchanged.
17. **GBK names**: 12 ARS enemy names are traditional characters (GBK) and appear as `\x` escapes in the table;
    glossary rows use the decoded text (強盜, 馬贼, 蒙面殺手 ...) with their ARS ids.
18. **Typos are fixed silently** in English (table below). Dialogue lines tagged with the wrong speaker
    (助功长老 vs 传功长老; player lines written as `say 0`) are translated as what they mean.
19. **Puns**: Yu Daiyan's 大象无形 quiz (大象 = "great image" / "elephant") and Huang Rong's 清圣浊贤 riddle (=
    wine) keep the choices "The greatest form" / "An animal" and "Wine" / "Tea"; the question text should hint at
    the pun in English (e.g. "great image - or great elephant?").
20. **The developer's end note** (busy with the gaokao) is translated as-is: "college entrance exam".

## Inconsistencies and typos found in the source

| source | where | glossary / fix |
|---|---|---|
| 左冷蝉 | 1-13-1 (Yue Buqun) | 左冷禅 Zuo Lengchan |
| 抽随掌 | MRS 4-1-50 | 抽髓掌 Marrow Palm |
| 百花腹蛇膏 | GRS 6-9-9 | 腹 for 蝮 (viper): Viper Balm |
| 苻苓草 vs 茯苓首乌丸 | GRS 6-14-40 / 6-9-8 | 苻 for 茯: both Poria |
| 驾裟 | GRS 6-2-10 desc | 袈裟 kasaya |
| 项练, 光茫, 冶链, 具说, 迷一般, 神不知鬼不绝, 过渡使用 | GRS descs (6-6-11, 6-6-15, 6-6-10, 6-5-6, 6-13-1, 6-3-5, 6-7-3) | 项链, 光芒, 冶炼, 据说, 谜一般, 觉, 过度 |
| 龙泉剑 desc "玄剑长剑, 虽名为玄铁" | GRS 6-7-6 | garbled; translate as "a Longquan sword, not true dark iron" |
| 黑剑 "唐代中期" etc. | GRS 6-7-4 | fine, only noted |
| 疯疯颠颠 | 1-4-7 | 疯癫 |
| 一翻打斗 / 一翻激烈 | 1-9-16, 1-11-28 | 一番 |
| 带者 | 1-9-14 | 带着 |
| 快吧紫霞秘籍交出来 | 1-12-26 | 把 |
| 闯了近来 | 1-12-26 | 进来 |
| 你那去试试 | 1-13-4 | 拿 |
| 苦海无崖 | 1-3-2 | 无涯 |
| 以柔刻刚 | 1-3-4 | 克 |
| 有人本国人在X开办地下赌场 | 1-10/11/12-24 | garbled; "someone from our country" |
| 洪七公 "，，" | 1-7-1 | double comma |
| 郭靖：/ 青龙仙人：(full-width colon) | 1-4-7, 1-6-x, many townsfolk | speaker tags: always ASCII ':' |
| 助功长老 then 传功长老 | 1-7-3 | same Beggar elder; English "Teaching Elder" for both lines in that script is acceptable |
| player lines as `say 0` | 1-5-12 ("没错，我先走一步了", "在哪？"), 1-9-14 ("道长这是怎么了？", "王道长，这是你要的解药。") | spoken by the player, no tag |
| 峨嵋 | everywhere | variant of 峨眉; "Emei" |
| 小琦 calls Xiaolongnu and Li Mochou 师妹 | 1-3-5 | render "our two famous sisters" |
| GBK traditional names (強盜, 馬贼 ...) | ARS 3-3-52..76 | decoded; English as for simplified |
| 化功大法, 血刀刀法 twice | MRS 4-1-8/53, 4-1-12/45 | enemy copy + player copy; same English |
| ARS reused in fights | Jin soldiers use 山贼/強盜/馬贼 (51-53); Wanyan Kang and Qiu Qianren fights use 梅超风 (95); the Feng Qingyang / Yue Buqun fight uses 华山/武当/少林叛徒 (81-83) | battle names will not match the story; not fixable in text |
| fmj ARS names (无机道人, 三清游人1 ...) | ARS 3-2-x | template leftovers, see decision 16 |
| 盟主令牌 | GRS 6-14-99 | no script gives it |
| `\x0d\x0a` in descriptions | GRS 6-2-6, 6-3-4, 6-3-6, 6-6-15 | do not copy |


## Counts

| category | terms |
|---|---|
| person | 144 |
| title | 49 |
| sect | 24 |
| place | 67 |
| monster | 43 |
| weapon | 11 |
| armor | 75 |
| consumable | 12 |
| item | 60 |
| magic | 79 |
| skill | 8 |
| other | 25 |
| ui | 88 |
| **total** | **685** |


## People and speakers

| zh | en | short | alt | note |
|---|---|---|---|---|
| 幻吟风 | Yinfeng |  | Huan Yinfeng | Male protagonist (choice 1 in 1-1-1, event flag 1). Full name Huan Yinfeng is 12 chars, over the 11-char ARS field, so the field uses the given name; the title choice (19) may show the full name. Never named in dialogue: his lines are untagged `say 1`. Can join Beggars, Shaolin, Wudang, Quanzhen, Huashan, Xingxiu, Xuedao. [ARS/3-1-1] |
| 紫灵儿 | Ling'er |  | Zi Ling'er | Female protagonist (choice 2, event flag 2). Given name like the hero; Zi Ling'er (10) would fit but the pair stays parallel. Can join Hengshan, Ancient Tomb, Lingjiu, Emei. [ARS/3-1-2] |
| 无机道人 | Taoist Wuji |  | Wuji the Taoist | 伏魔记 template leftover: ARS 3-2-1 keeps the fmj name; the sprite is reused for jy's sect masters (Hong Qigong, Zhang Sanfeng, Yue Buqun, Wang Chongyang...). Name not displayed in jy dialogue; kept as in the fmj glossary. |
| 小师弟 | Junior |  | Little Brother | fmj template leftover (ARS 3-2-2); not used by jy text. |
| 袁萍芷 | Pingzhi |  | Yuan Pingzhi | fmj template leftover (ARS 3-2-7); not used by jy text. |
| 蔡大妈 | Granny Cai |  | Auntie Cai | fmj template leftover (ARS 3-2-8); not used by jy text. |
| 慕容玄 | Murong Xuan |  |  | fmj template leftover (ARS 3-2-9); not used by jy text. |
| goods商人 | Merchant |  |  | fmj template leftover (ARS 3-2-11, half-translated dev label); sprite reused for jy townsfolk. |
| 药店商人 | Herbalist |  | Herb Seller | fmj template leftover (ARS 3-2-12); sprite reused for jy townsfolk. |
| 三清游人1 | Pilgrim 1 |  |  | fmj template leftover (ARS 3-2-13..18, numbered dev labels); sprites reused for jy sect disciples and townsfolk. |
| 三清游人2 | Pilgrim 2 |  |  | fmj template leftover. |
| 三清游人3 | Pilgrim 3 |  |  | fmj template leftover. |
| 三清游人4 | Pilgrim 4 |  |  | fmj template leftover. |
| 三清游人5 | Pilgrim 5 |  |  | fmj template leftover. |
| 三清游人6 | Pilgrim 6 |  |  | fmj template leftover. |
| 阿霞 | Ah Xia |  | Axia | fmj template leftover (ARS 3-2-21). |
| 李虎 | Li Hu |  | Tiger Li | fmj template leftover (ARS 3-2-25). |
| 通宵虫 | Allnighter |  | Tongxiaochong | fmj dev-team handle, template leftover (ARS 3-2-32); sprite 32 is jy's generic elder/disciple sprite. |
| 郭靖 | Guo Jing |  |  | Hero of the Condor story. Kidnapped by Cyclone Mei at Yanmen; at the Mount Hua summit he gives the player the Nine Yin Manual. |
| 靖儿 | Jing'er |  | young Jing | The Seven Freaks' pet name for Guo Jing ('Let Jing'er go!'). |
| 黄蓉 | Huang Rong |  |  | Huang Yaoshi's daughter; at Peach Blossom Island she teaches a Beggar disciple the Dog-Beating Staff after a riddle (answer: wine). Playful, sharp-tongued. |
| 蓉儿 | Rong'er |  |  | Hong Qigong's name for Huang Rong. |
| 洪七公 | Hong Qigong |  | Northern Beggar | Chief of the Beggars' Sect (1-7-1). Gruff, kindly; teaches the Eighteen Dragon Palms after the map delivery. |
| 黄药师 | Huang Yaoshi |  | Eastern Heretic | Master of Peach Blossom Island (1-6-5). One line: 'You dare intrude on my island!' |
| 欧阳锋 | Ouyang Feng |  | Western Venom | Final boss at the Mount Hua summit (ARS 3-3-89, fought three at once). Fits 11 exactly. [ARS/3-3-89] |
| 裘千仞 | Qiu Qianren |  |  | Jin collaborator; at Guiyun Manor (Dali) urges surrender to the Jin and flees. 'Iron Palm' not mentioned. |
| 周伯通 | Zhou Botong |  | Old Imp | Childish Quanzhen elder trapped in the Peach Blossom Island cave (1-5-12). Speaks like an excitable kid ('Nobody plays with me!'); 'Old Imp' only as alt. |
| 梅超风 | Cyclone Mei |  | Mei Chaofeng | Huang Yaoshi's renegade disciple; Nine Yin White Bone Claw. 'Mei Chaofeng' (12) does not fit 11, so use the established English epithet (Holmwood's 'Cyclone Mei') everywhere. Her ARS is also used for the Wanyan Kang and Qiu Qianren fights. [ARS/3-3-95] |
| 江南七怪 | Seven Freaks |  | Seven Freaks of Jiangnan | Guo Jing's seven teachers; speak as one ('Seven Freaks: ...'). |
| 七怪 | the Freaks |  | the Seven Freaks | Short form ('The Freaks have gone beyond the pass'). |
| 柯镇恶 | Ke Zhen'e |  |  | Eldest Freak, blind ('Your voice tells me you are no ordinary man'). In Yangzhou (1-12-29). |
| 华筝 | Huazheng |  | Princess Huazheng | Mongol girl at Yanmen Pass whose village the Jin attack; calls Guo Jing her anda. |
| 王处一 | Wang Chuyi |  | Taoist Wang | Quanzhen master; stops the Wanyan Kang duel, later found poisoned at the Capital inn (needs Dragon Dew). |
| 杨铁心 | Yang Tiexin |  |  | Named in Wang Chuyi's news: he and his wife are dead (suicide). |
| 穆易 | Mu Yi |  |  | Yang Tiexin's alias; holds the marriage tournament in the Capital. |
| 穆念慈 | Mu Nianci |  |  | Mu Yi's daughter, beaten by Wanyan Kang. |
| 完颜康 | Wanyan Kang |  |  | Jin prince; arrogant ('You dare insult the young prince of Jin?'). |
| 陆乘风 | Lu Chengfeng |  |  | Master of Guiyun Manor (narration only). |
| 王重阳 | Wang Chongyang |  |  | Quanzhen founder and sect head (1-12-1). |
| 全真七子 | Seven Masters |  | Seven Quanzhen Masters | Quanzhen elders (disciple chatter). |
| 小龙女 | Xiaolongnu |  | Dragon Maiden | Ancient Tomb head (1-11-1). ASCII 'Xiaolongnu', no umlaut. |
| 李莫愁 | Li Mochou |  |  | Ancient Tomb renegade (chatter). |
| 岳不群 | Yue Buqun |  | Gentleman Sword | Huashan sect head (1-13-1); smooth hypocrite who turns on the player in the Feng branch. Formal, self-righteous register. [ARS/3-3-88] |
| 岳灵珊 | Yue Lingshan |  |  | Yue's daughter; lost her sword in the Mt. Hua valley. |
| 令狐冲 | Linghu Chong |  |  | Huashan senior disciple; wine-lover ('Wine, wine, wine!'), warm and casual. Sends the player to Feng Qingyang. |
| 冲儿 | Chong'er |  |  | Feng Qingyang's name for Linghu Chong. |
| 劳德诺 | Lao Denuo |  |  | Huashan disciple, secretly a Songshan spy; stole the Violet Mist Manual, killed by a poisoned arrow in Yangzhou. |
| 梁发 | Liang Fa |  |  | Huashan disciple; bandit-clearing quest (Huashan Sword). |
| 陆大有 | Lu Dayou |  | Monkey | 'Sixth brother'; loves monkeys; tore the Tiger Kasaya; tiger-skin and lost-sword quests. |
| 英白罗 | Ying Bailuo |  |  | Huashan elder disciple; Dragon Dew and Yue Fei's Sword quests. |
| 林平之 | Lin Pingzhi |  |  | Mentioned: Huashan junior who brought the Evil-Warding Sword. |
| 风清扬 | Feng Qingyang |  |  | Sword School elder hiding in the Repentance Cliff cave; teaches the Nine Swords of Dugu. Terse, proud. |
| 成不忧 | Cheng Buyou |  |  | Sword School disciple; teaches Fatal Trio if given a Zhenwu. |
| 封不平 | Feng Buping |  |  | Sword School disciple. |
| 左冷蝉 | Zuo Lengchan |  |  | Songshan head. Source typo 蝉 for 禅. |
| 张三丰 | Zhang Sanfeng |  |  | Wudang founder (1-10-1); gentle quiz-master ('fist or sword?'). |
| 俞岱岩 | Yu Daiyan |  |  | Wudang elder; drills the Tao Te Ching and quizzes the player. |
| 定逸师太 | Abbess Dingyi |  |  | Hengshan head (1-9-1), female sect. |
| 灭绝师太 | Abbess Miejue |  |  | Emei head (1-17-1). |
| 仪琳 | Yilin |  |  | Hengshan nun. |
| 仪和 | Yihe |  |  | Hengshan nun. |
| 仪柳 | Yiliu |  |  | Hengshan nun. |
| 仪静 | Yijing |  |  | Hengshan nun. |
| 天山童姥 | Tong Lao |  | Child Elder of Tianshan | Lingjiu Palace head (1-14-1). |
| 丁春秋 | Ding Chunqiu | Chunqiu |  | Xingxiu sect head (1-15-1) and boss. Full name (12) in dialogue; the 11-char ARS field uses short 'Chunqiu'. [ARS/3-3-87] |
| 血刀老祖 | Blood Patriarch |  | Blood Blade Patriarch | Xuedao sect head (1-16-1). |
| 平一指 | Ping Yizhi |  |  | 'Killer physician' of the Demon Cult living in Xixia; makes Dragon Dew. Calls himself 老夫 'this old man'. |
| 东方不败 | Dongfang Bubai | Dongfang | Invincible East | Boss (ARS 3-3-90). 14 chars; the ARS field uses short 'Dongfang' (compound surname, how fans refer to him). [ARS/3-3-90] |
| 石中玉 | Shi Zhongyu |  |  | Boss (ARS 3-3-92); Snow Sword user. [ARS/3-3-92] |
| 田伯光 | Tian Boguang | Boguang |  | Boss (ARS 3-3-93): the notorious rake. 12 chars; the ARS field uses short 'Boguang' (given name, fmj convention). [ARS/3-3-93] |
| 鹤笔翁 | He Biweng |  |  | Boss (ARS 3-3-94), one of the Xuanming Elders (Dark Palm). [ARS/3-3-94] |
| 胜谛和尚 | Monk Shengdi | Shengdi |  | Xuedao monk boss (ARS 3-3-91). 12 chars; ARS field short 'Shengdi'. [ARS/3-3-91] |
| 岳飞 | Yue Fei |  |  | Song general; his sword is a Huashan quest item. |
| 老子 | Laozi |  |  | Author of the Tao Te Ching. |
| 达摩 | Bodhidharma |  | Damo | Shaolin patriarch (Damo Robe, Damo Sword). |
| 关公 | Lord Guan |  | Guan Yu | In the Valor Cuff description. |
| 欧冶子 | Ou Yezi |  |  | Legendary swordsmith (Zhanlu description). |
| 明叔 | Uncle Ming |  |  | Beggar. |
| 毛三 | Mao San |  |  | Beggar. |
| 杨初二 | Yang Chu'er |  |  | Beggar. |
| 朱四高 | Zhu Sigao |  |  | Beggar. |
| 洪阿凯 | Hong Akai |  |  | Beggar. |
| 张一任 | Zhang Yiren |  |  | Beggar. |
| 空性 | Kongxing |  |  | Shaolin monk. |
| 清乐 | Qingle |  |  | Shaolin monk. |
| 清无 | Qingwu |  |  | Shaolin monk. |
| 普刚 | Pugang |  |  | Shaolin monk. |
| 清颠 | Qingdian |  |  | Shaolin monk. |
| 小琦 | Xiaoqi |  |  | Ancient Tomb girl. |
| 小铃 | Xiaoling |  |  | Ancient Tomb girl. |
| 小雯 | Xiaowen |  |  | Ancient Tomb girl. |
| 小曼 | Xiaoman |  |  | Ancient Tomb girl. |
| 胜羽 | Shengyu |  |  | Xuedao disciple (all eight are 胜X: Shengyu, Shengwei, Shengping, Shenghou, Shengji, Shengmao, Shengquan, Shengfa). |
| 胜威 | Shengwei |  |  | Xuedao disciple. |
| 胜平 | Shengping |  |  | Xuedao disciple. |
| 胜侯 | Shenghou |  |  | Xuedao disciple. |
| 胜基 | Shengji |  |  | Xuedao disciple. |
| 胜瑁 | Shengmao |  |  | Xuedao disciple (a thug: 'scare them and they hand over their money'). |
| 胜全 | Shengquan |  |  | Xuedao disciple. |
| 胜发 | Shengfa |  |  | Xuedao disciple. |
| 阿芳 | Ah Fang |  |  | Capital girl who needs a dowry (earrings). |
| 苏忠 | Su Zhong |  |  | Capital boy who wants to enlist. |
| 苏大妈 | Auntie Su |  |  | Su Zhong's mother. |
| 虎子 | Huzi |  | Tiger | Capital boy who wants to learn kung fu and a slingshot. |
| 虎子爹 | Huzi's Dad |  |  |  |
| 天天 | Tiantian |  |  | Huzi's playmate (mentioned). |
| 牛牛 | Niuniu |  |  | Xixia boy who wants to be a hero. |
| 牛牛妈 | Niuniu's Mom |  |  |  |
| 李豫 | Li Yu |  |  | Lovesick Xixia man (quotes Liu Yong's 'Clothes grow loose...'). |
| 春香 | Chunxiang |  |  | The girl Li Yu loves. |
| 武介山 | Wu Jieshan |  |  | Dali tiger-skin buyer. |
| 王老先生 | Old Mr. Wang |  |  | Sick old man in Dali (Jade Salve). |
| 张菁 | Zhang Jing |  |  | Ah Hong's mother in Dali. |
| 阿鸿 | Ah Hong |  |  | Homesick worker in Yangzhou. |
| 刘员外 | Squire Liu |  |  | Ore buyer in Xixia. |
| 李员外 | Squire Li |  |  | Ore buyer in Yangzhou. |
| 民女 | Village Girl |  |  | Bandit victim in the Heartland. |
| 土匪 | Bandit |  |  | Heartland bandits (speaker). ARS shows 山贼 etc. |
| 打铁匠 | Blacksmith |  |  | City blacksmith (ore -> metal). |
| 铁匠 | Blacksmith |  |  | Same blacksmith in the slingshot quest. |
| 织女 | Weaver |  |  | City weaver (fibre -> cloth). Not the mythological Weaver Girl. |
| 猎人 | Hunter |  |  | City hunter (skin -> leather). |
| 铸剑师 | Swordsmith |  |  | Weapon shop forge. |
| 神秘裁缝 | Odd Tailor |  | Mysterious Tailor | Crafts armour from cloth/leather/metal. |
| 神秘工匠 | Odd Jeweller |  | Mysterious Artisan | Crafts rings and necklaces. |
| 地下赌场老板 | Casino Boss |  | Underground Casino Owner |  |
| 武师 | Instructor |  | Martial Instructor | City teacher of the basic arts (also takes Huzi as a pupil). |
| 大内侍卫 | Palace Guard |  |  | Receives Yue Fei's Sword / the northern map at the palace. |
| 丐帮弟子 | Beggar |  | Beggars' Sect disciple | Speaker tag. |
| 少林弟子 | Shaolin Monk |  |  | Speaker tag. |
| 武当弟子 | Wudang Disciple |  |  | Speaker tag. |
| 全真弟子 | Quanzhen Disciple |  |  | Speaker tag. |
| 华山弟子 | Huashan Disciple |  |  | Speaker tag. |
| 星宿弟子 | Xingxiu Disciple |  |  | Speaker tag. |
| 峨嵋弟子 | Emei Disciple |  |  | Speaker tag. |
| 嵩山派弟子 | Songshan Disciple |  |  | Speaker tag (1-12-26). |
| 传功长老 | Teaching Elder |  | Elder of Transmission | Beggars' Sect elder (1-7-2/1-7-3); jovial drunk ('The drunker, the clearer!'). |
| 助功长老 | Training Elder |  |  | 1-7-3's first line; later lines in the same script are tagged 传功长老 (inconsistent; same NPC sprite). |
| 净衣长老 | Clean Elder |  | Clean-Clothes Elder | Beggars' faction elder. |
| 污衣长老 | Ragged Elder |  | Dirty-Clothes Elder | Beggars' faction elder. |
| 青龙仙人 | Dragon Sage |  | Blue Dragon Immortal | Guardian of the Blue Dragon altar (1-6-1). |
| 白虎仙人 | Tiger Sage |  | White Tiger Immortal | Guardian of the White Tiger altar. |
| 朱雀仙人 | Vermilion Sage |  | Vermilion Bird Immortal | Guardian of the Vermilion Bird altar. |
| 玄武仙人 | Tortoise Sage |  | Black Tortoise Immortal | Guardian of the Black Tortoise altar. |

## Titles and forms of address

| zh | en | short | alt | note |
|---|---|---|---|---|
| 北丐 | Northern Beggar |  |  | Hong Qigong's epithet (one of the Five Greats). |
| 东邪 | Eastern Heretic |  |  | Huang Yaoshi's epithet. |
| 黄老邪 | Old Heretic |  | Old Heretic Huang | Zhou Botong's rude name for Huang Yaoshi. |
| 西毒 | Western Venom |  |  | Ouyang Feng's epithet; also in 西毒杖法 Venom Staff. |
| 南帝 | Southern Emperor |  |  | Fifth of the Greats, only named in the summit narration. |
| 周师叔 | Uncle Zhou |  |  | Quanzhen disciple's name for Zhou Botong. |
| 柯大侠 | Master Ke |  | Hero Ke | Huazheng's/the player's polite name for Ke Zhen'e. |
| 华筝小姐 | Miss Huazheng |  |  | Ke Zhen'e's polite form. |
| 安答 | anda |  | sworn brother | Mongol word for sworn brother; keep 'anda' with gloss on first use. |
| 王道长 | Taoist Wang |  | Master Wang | Player's address to Wang Chuyi. |
| 小王爷 | young prince |  | Little Prince | Wanyan Kang's title. |
| 赤炼仙子 | Red Fairy |  | Red Serpent Fairy | Li Mochou's epithet; pairs with 赤炼神掌 Red Serpent (palm). |
| 君子剑 | Gentleman Sword |  | the Gentleman Swordsman | Yue Buqun's epithet. |
| 周姐姐 | Sister Zhou |  |  | Emei disciples' name for Zhou Zhiruo (unnamed). |
| 星宿老仙 | Xingxiu Immortal |  | Old Immortal of Xingxiu | Disciples' flattering name for Ding Chunqiu. |
| 杀人名医 | killer physician |  |  | Ping Yizhi's epithet. |
| 岳王爷 | Lord Yue |  | Yue Fei | Respectful name for Yue Fei. |
| 皇上 | His Majesty |  | the Emperor |  |
| 师傅 | Master |  |  | Disciple to teacher (师父 not used in jy). |
| 徒儿 | my disciple |  |  | Teacher to disciple. |
| 师兄 | Brother |  |  | Senior fellow disciple ('Brother Liang', 'Brother Lu', 'Brother Cheng'). |
| 大师兄 | Big Brother |  |  | Linghu Chong (also 大师哥). |
| 大师哥 | Big Brother |  |  | Same as 大师兄. |
| 六师哥 | Sixth Brother |  |  | Lu Dayou. |
| 师姊 | Sister |  |  | Yue Lingshan (senior female fellow disciple). |
| 小师妹 | Little Sister |  |  | Linghu Chong's name for Yue Lingshan. |
| 师妹 | sister |  |  | Ancient Tomb girl speaking of Xiaolongnu and Li Mochou. |
| 师弟 | little brother |  |  | 'Brother Lin' (Lin Pingzhi). |
| 师叔 | Uncle |  |  | Teacher's fellow disciple. |
| 太师叔 | Grand-uncle |  |  | Player to Feng Qingyang ('Grand-uncle Feng'). |
| 掌门 | Sect Head |  |  |  |
| 长老 | Elder |  |  |  |
| 方丈 | Abbot |  |  | Shaolin head (speaker tag; unnamed). |
| 师太 | Abbess |  |  | Buddhist nun head (Abbess Dingyi, Abbess Miejue). |
| 道长 | Master Taoist |  | Taoist | As in fmj. |
| 老祖 | Patriarch |  |  | 血刀老祖. |
| 教主 | Cult Leader |  |  |  |
| 大侠 | hero |  | good sir | Townsfolk to the player. |
| 客官 | sir |  |  | Shopkeepers/innkeepers/boatmen. |
| 姑娘 | Miss |  |  |  |
| 蓉姑娘 | Miss Rong |  |  | Player to Huang Rong. |
| 大妈 | Auntie |  |  |  |
| 伯母 | Auntie |  | ma'am | Polite to an older woman (Zhang Jing). |
| 大人 | Your Honor |  | sir | Player to the magistrate. |
| 在下 | I |  | this humble one | Humble first person; render plainly. |
| 晚辈 | I |  | this junior | Humble first person. |
| 老夫 | I |  | this old man | Ping Yizhi's first person. |
| 弟子 | Disciple |  |  | Generic speaker tag in Lingjiu Palace (弟子:...). |
| 盟主 | Alliance Leader |  |  |  |

## Sects and groups

| zh | en | short | alt | note |
|---|---|---|---|---|
| 净衣派 | Clean Clothes |  | Clean-Clothes faction | Beggars' Sect faction. |
| 污衣派 | Ragged Clothes |  | Dirty-Clothes faction | Beggars' Sect faction. |
| 丐帮 | Beggars' Sect | Beggars |  | Banner short 'Beggars'. Headed by Hong Qigong. Male only. |
| 少林 | Shaolin |  |  |  |
| 少林寺 | Shaolin Temple | Shaolin |  | Banner short 'Shaolin'. |
| 武当 | Wudang |  |  |  |
| 武当派 | Wudang Sect | Wudang |  | Banner short 'Wudang'. Male only. |
| 恒山派 | Hengshan Sect | Hengshan |  | Banner short 'Hengshan'. Buddhist nuns of Mt. Heng; female only. |
| 古墓派 | Ancient Tomb | Old Tomb | Ancient Tomb Sect | Banner short 'Old Tomb' (12 > 10). Female only. |
| 古墓 | Ancient Tomb |  |  |  |
| 全真教 | Quanzhen Sect | Quanzhen | Complete Reality Sect | Banner short 'Quanzhen'. Male only. |
| 全真 | Quanzhen |  |  |  |
| 华山派 | Huashan Sect | Huashan | Mount Hua Sect | Banner short 'Huashan'. Male only; carries the main side story. |
| 剑宗 | Sword School |  |  | Huashan faction (Feng Qingyang). |
| 气宗 | Qi School |  |  | Huashan faction (Yue Buqun). |
| 嵩山派 | Songshan Sect |  |  | Zuo Lengchan's sect. |
| 灵鹫宫 | Lingjiu Palace | Lingjiu | Palace of the Numinous Vulture | Banner short 'Lingjiu'. Female only. |
| 星宿派 | Xingxiu Sect | Xingxiu | Star Lodge Sect | Banner short 'Xingxiu'. Poisoners; male only. |
| 血刀门 | Xuedao Sect | Xuedao | Blood Blade Sect | Banner short 'Xuedao'. Tibetan sect; male only. Pinyin like Xingxiu/Lingjiu; its skills use English (Blood Blade). |
| 西藏青教 | Tibetan Qing Sect |  |  | Xuedao's parent order (chatter). |
| 峨嵋派 | Emei Sect | Emei |  | Banner short 'Emei'. Female only. 峨嵋 is a variant of 峨眉. |
| 峨嵋 | Emei |  |  |  |
| 魔教 | Demon Cult |  |  | Righteous sects' slur for the Sun Moon Cult (Ping Yizhi). |
| 一品堂 | Yipin Hall |  |  | Xixia's martial corps (chatter). |

## Places

| zh | en | short | alt | note |
|---|---|---|---|---|
| 归云庄 | Guiyun Manor |  | Return-to-Clouds Manor | Lu Chengfeng's manor; here placed in Dali. |
| 活死人墓 | Tomb of the Living Dead |  |  | The Ancient Tomb's full name (chatter). |
| 雁门关 | Yanmen Pass | Yanmen |  | Map name; banner short 'Yanmen'. Huazheng rescue and Cyclone Mei fight. [MAP/2-5-1] |
| 中原腹地 | Heartland |  | Heart of the Central Plains | Bandit-clearing quest. [MAP/2-5-2] |
| 中原 | Central Plains |  |  |  |
| 桃花岛 | Peach Isle |  | Peach Blossom Island | Field name form; dialogue uses 'Peach Blossom Island'. [MAP/2-5-3] |
| 桃花岛山洞 | Peach Cave |  | Peach Blossom Island Cave | Where Zhou Botong is trapped. [MAP/2-5-12] |
| 桃花岛洞 | Peach Cave |  |  | Scene-name form of 桃花岛山洞. |
| 黄药师居 | Huang's |  | Huang Yaoshi's Residence | Scene banner (10). |
| 绝情谷 | Heartbreak |  | Passionless Valley | [MAP/2-5-4] |
| 高昌迷宫 | Gaochang |  | Gaochang Labyrinth | Scene banner only. |
| 青城山 | Qingcheng |  | Mt. Qingcheng | 'Mt. Qingcheng' is 13. [MAP/2-5-6] |
| 雪山 | Snow Peaks |  | Snowy Mountains | [MAP/2-5-7] |
| 雪山山洞 | Snow Cave |  |  | [MAP/2-5-11] |
| 百花谷 | Flower Vale | Bloom Vale | Hundred Flowers Valley | Tigers live here (tiger-skin quests). Banner short 'Bloom Vale'. [MAP/2-5-8] |
| 剑魔剑冢 | Sword Tomb |  | Sword Demon's Grave | Dugu Qiubai's sword grave. [MAP/2-5-9] |
| 逍遥洞 | Xiaoyao Cave | Xiaoyao | Carefree Cave | Scene banner short 'Xiaoyao'. |
| 山洞 | Cave |  |  | [MAP/2-5-10] |
| 总坛 | Headquarters |  | Main Hall | [MAP/2-6-1] |
| 掌门阁 | Master Hall |  | Sect Head's Pavilion | Sect head's room in each sect. [MAP/2-8-1] |
| 师叔阁 | Elders Hall |  | Uncles' Pavilion | [MAP/2-8-2] |
| 店铺 | Shop |  |  | [MAP/2-1-1..3] |
| 客栈 | Inn |  |  | [MAP/2-1-4] |
| 民居 | House |  | Residence | [MAP/2-1-5] |
| 衙门 | Magistracy |  | yamen | Magistrate's office (casino investigations). [MAP/2-1-6] |
| 城市野外 | Outskirts |  | City Outskirts | [MAP/2-2-1..2] |
| 门派 | Sect Hall |  |  | [MAP/2-3-1] |
| 门派野外 | Sect Lands |  | Sect Outskirts | [MAP/2-4-1..4] |
| 京城 | The Capital | Capital | Capital City | Song capital (unnamed). Map/choice 'The Capital'; banner short 'Capital'. Chapter 9. [MAP/2-9-1] |
| 京城野外 | Capital |  | Capital Outskirts | Banner: 野外 'outskirts' dropped (see Decisions). |
| 紫禁城 | Forbidden City |  |  | Townsfolk chatter. |
| 西夏 | Xixia |  | Western Xia | City and kingdom; chapter 10. |
| 西夏府 | Xixia |  | Xixia Prefecture | Map + banner. [MAP/2-9-2] |
| 西夏野外 | Xixia |  | Xixia Outskirts | Banner. |
| 大理 | Dali |  |  | Chapter 11. |
| 大理府 | Dali |  | Dali Prefecture | [MAP/2-9-3] |
| 大理野外 | Dali |  | Dali Outskirts | Banner. |
| 扬州 | Yangzhou |  |  | Chapter 12; port for Peach Blossom Island. |
| 扬州府 | Yangzhou |  | Yangzhou Prefecture | [MAP/2-9-4] |
| 扬州野外 | Yangzhou |  | Yangzhou Outskirts | Banner. |
| 丐帮野外 | Beggars |  | Beggars' Sect Outskirts | Banner (same as the sect banner). |
| 灵鹫宫野外 | Lingjiu |  | Lingjiu Palace Outskirts | Banner. |
| 血刀门野外 | Xuedao |  | Xuedao Outskirts | Banner. |
| 嵩山 | Mt. Song |  | Mount Song | Herb: Mugwort. |
| 恒山 | Mt. Heng |  | Mount Heng | Herb: Skyreach. |
| 武当山 | Mt. Wudang |  | Mount Wudang | Herb: Sesame. |
| 终南山 | Zhongnan |  | Mt. Zhongnan | 'Mt. Zhongnan' is 12 > 10. Quanzhen and Ancient Tomb. Herb: Rainflower. |
| 华山 | Mt. Hua |  | Mount Hua | Final scene (summit). Herb: Poria. |
| 峨嵋山 | Mt. Emei |  | Mount Emei | Herb: Peace Herb. |
| 星宿海 | Star Sea |  | Xingxiu Sea | Banner. |
| 青龙坛 | Dragon |  | Blue Dragon Altar | Banner (10): beast only; 'Dragon Altar' is 12. |
| 白虎坛 | Tiger |  | White Tiger Altar | Banner. |
| 朱雀坛 | Vermilion |  | Vermilion Bird Altar | Banner. |
| 玄武坛 | Tortoise |  | Black Tortoise Altar | Banner. |
| 思过崖 | Repentance Cliff |  |  | Huashan cliff where Feng Qingyang hides. |
| 思过崖山洞 | Repentance Cave |  |  |  |
| 后山 | back mountain |  |  |  |
| 江南 | Jiangnan |  | the South |  |
| 嘉兴 | Jiaxing |  |  | Where the Freaks' duel is set. |
| 大漠 | the desert |  | the steppe | Mongolia. |
| 关外 | beyond the pass |  |  |  |
| 地下赌场 | underground casino |  |  | One per city; gambling is banned. |
| 杂货铺 | general store |  |  |  |
| 布庄 | cloth shop |  |  |  |
| 药局 | pharmacy |  |  |  |
| 私塾 | village school |  |  |  |
| 码头 | pier |  |  |  |

## Enemies

| zh | en | short | alt | note |
|---|---|---|---|---|
| 山贼 | Bandit |  |  | [ARS/3-3-51] |
| 強盜 | Robber |  |  | Traditional/GBK in source (shows as \x escapes in the table). [ARS/3-3-52] |
| 馬贼 | Raider |  | Mounted Bandit | GBK. [ARS/3-3-53] |
| 採花贼 | Lecher |  | Flower Thief | GBK. 'Flower-picking thief' = sex predator. [ARS/3-3-54] |
| 恶道人 | Evil Taoist |  |  | [ARS/3-3-55] |
| 盜贼 | Thief |  |  | GBK. [ARS/3-3-56] |
| 破戒僧 | Rogue Monk |  | Vow-Breaker | [ARS/3-3-57] |
| 隱面人 | Faceless |  | Hidden-Face Man | GBK. [ARS/3-3-58] |
| 人肉屠子 | Man-Butcher |  |  | [ARS/3-3-59] |
| 恶武师 | Evil Master |  | Rogue Instructor | [ARS/3-3-60] |
| 山林怪儒 | Mad Scholar |  | Weird Hill Scholar | [ARS/3-3-61] |
| 老鬼 | Old Ghost |  |  | [ARS/3-3-62] |
| 山贼头子 | Bandit Boss |  | Bandit Chief | Heartland quest boss. [ARS/3-3-63] |
| 強盜头子 | Robber Boss |  |  | GBK. [ARS/3-3-64] |
| 馬贼王 | Raider King |  |  | GBK. [ARS/3-3-65] |
| 採花大盗 | Lecher Boss |  | Master Lecher | GBK. [ARS/3-3-66] |
| 恶道头子 | Taoist Boss |  | Evil Taoist Chief | [ARS/3-3-67] |
| 盜贼头子 | Thief Boss |  |  | GBK. [ARS/3-3-68] |
| 刺客 | Assassin |  |  | [ARS/3-3-69] |
| 蒙面殺手 | Mask Killer |  | Masked Killer | GBK; 'Masked Killer' is 13. [ARS/3-3-70] |
| 恶霸头子 | Bully Boss |  | Tyrant Chief | [ARS/3-3-71] |
| 山贼王 | Bandit King |  |  | [ARS/3-3-72] |
| 江洋大盜 | Outlaw |  | River Pirate | GBK. [ARS/3-3-73] |
| 邪派高手 | Dark Master |  | Evil Sect Expert | [ARS/3-3-74] |
| 护国法师 | Royal Lama |  | State Preceptor | [ARS/3-3-75] |
| 大內高手 | Royal Guard |  | Palace Expert | GBK. [ARS/3-3-76] |
| 退隐之士 | Recluse |  | Retired Master | [ARS/3-3-77] |
| 邪教教主 | Cult Leader |  |  | [ARS/3-3-78] |
| 邪僧 | Evil Monk |  |  | [ARS/3-3-79] |
| 蛮子王 | Savage King |  | Barbarian King | [ARS/3-3-80] |
| 华山叛徒 | Ex-Huashan |  | Huashan Traitor | 'Ex-<sect>' = renegade. ARS 81-83 are the ones fought in the Feng Qingyang / Yue Buqun battle. [ARS/3-3-81] |
| 武当叛徒 | Ex-Wudang |  | Wudang Traitor | [ARS/3-3-82] |
| 少林叛徒 | Ex-Shaolin |  | Shaolin Traitor | [ARS/3-3-83] |
| 全真叛徒 | Ex-Quanzhen |  | Quanzhen Traitor | [ARS/3-3-84] |
| 血刀叛徒 | Ex-Xuedao |  | Xuedao Traitor | [ARS/3-3-85] |
| 星宿叛徒 | Ex-Xingxiu |  | Xingxiu Traitor | [ARS/3-3-86] |
| 牛 | Ox |  |  | Field animal dropping Ox Skin. [ARS/3-3-44] |
| 蛇 | Snake |  |  | Drops Snake Skin. [ARS/3-3-45] |
| 虎 | Tiger |  |  | Drops Tiger Skin (Flower Vale). [ARS/3-3-46] |
| 赌具 | Dice |  | gambling set | The casino 'battle' (ARS 3-3-50) that rolls the bet. |
| 老虎 | tiger |  |  | Dialogue word. |
| 赤链蛇 | red-banded snake |  |  | Venomous snake in Ying Bailuo's quest. |
| 大马猿猴 | big apes |  |  | Mt. Hua valley. |

## Weapons

| zh | en | short | alt | note |
|---|---|---|---|---|
| 青铜短剑 | Dagger |  | Bronze Short Sword | [GRS/6-7-1] |
| 铁剑 | Iron Sword |  |  | [GRS/6-7-2] |
| 秦剑 | Qin Sword |  |  | [GRS/6-7-3] |
| 黑剑 | Dark Sword |  | Black Sword | [GRS/6-7-4] |
| 冷凝剑 | Cold Sword |  | Frostcore Sword | [GRS/6-7-5] |
| 龙泉剑 | Longquan |  | Longquan Sword | [GRS/6-7-6] |
| 真武剑 | Zhenwu |  | Zhenwu Sword; True Martial Sword | Zhang Sanfeng's sword; needed for Soft Cloud, Fatal Trio and the Greatsword. [GRS/6-7-7] |
| 玄铁重剑 | Greatsword |  | Heavy Iron Sword | Yang Guo's heavy sword. Crafted: 4 Platinum, 6 Black Gold, 5 Charcoal, 1 Zhenwu. [GRS/6-7-8] |
| 湛卢剑 | Zhanlu |  | Zhanlu Sword | One of Ou Yezi's five swords. [GRS/6-7-9] |
| 倚天剑 | Sky Sword |  | Heaven Sword | 'Heaven Sword' is 12. [GRS/6-7-10] |
| 屠龙刀 | Dragonbane |  | Dragon Saber | Ending reward if the Nine Yin Manual is torn up. [GRS/6-7-11] |

## Armor and accessories

| zh | en | short | alt | note |
|---|---|---|---|---|
| 头巾 | Headband |  |  | [GRS/6-1-1] |
| 绿棉帽 | Green Cap |  |  | [GRS/6-1-2] |
| 珍珠发簪 | Pearl Pin |  | Pearl Hairpin | [GRS/6-1-3] |
| 翠玉发簪 | Jade Pin |  | Jade Hairpin | [GRS/6-1-4] |
| 凤头珠钗 | Plume Pin |  | Phoenix-Head Pearl Pin | [GRS/6-1-5] |
| 明珠金钗 | Gilt Pin |  | Pearl Gold Hairpin | [GRS/6-1-6] |
| 黄金发簪 | Gold Pin |  | Gold Hairpin | [GRS/6-1-7] |
| 钢丝罩子 | Wire Mask |  | Steel Wire Hood | Crafted. [GRS/6-1-8] |
| 钢盔 | Steel Helm |  |  | Crafted. [GRS/6-1-9] |
| 金盔 | Gold Helm |  |  | Crafted. [GRS/6-1-10] |
| 青龙冠 | Dragon Cap |  | Blue Dragon Crown | Blue Dragon altar treasure. [GRS/6-1-11] |
| 便捷短衣 | Tunic |  | Light Short Coat | [GRS/6-2-1] |
| 射日短衣 | Sun Tunic |  | Sun-Shooter Coat | [GRS/6-2-2] |
| 黄罩甲 | Buff Coat |  | Yellow Mail | Hide/cloth/metal coat. [GRS/6-2-3] |
| 厚棉袄 | Quilt Coat |  | Padded Cotton Coat | [GRS/6-2-4] |
| 血焰缎袍 | Flame Robe |  | Blood-Flame Satin Robe | [GRS/6-2-5] |
| 缎面狐皮袍 | Fox Robe |  | Satin Fox-Fur Robe | [GRS/6-2-6] |
| 玄天轻装 | Sky Garb |  | Mystic Sky Garb | [GRS/6-2-7] |
| 黑豹服 | Panther |  | Black Panther Suit | Crafted. [GRS/6-2-8] |
| 金丝软甲 | Gold Mail |  | Golden Silk Armor | Crafted. [GRS/6-2-9] |
| 达摩袈裟 | Damo Robe |  | Bodhidharma's Kasaya | Crafted. [GRS/6-2-10] |
| 袈裟 | kasaya |  | monk's robe |  |
| 普通靴 | Boots |  | Plain Boots | [GRS/6-3-1] |
| 皮靴 | Hide Boots |  | Leather Boots | [GRS/6-3-2] |
| 速行靴 | Fast Boots |  | Swift Boots | [GRS/6-3-3] |
| 飘行靴 | Wave Boots |  | Water-Gliding Boots | Walk on water. [GRS/6-3-4] |
| 鬼魅靴 | Ghoststep |  | Phantom Boots | [GRS/6-3-5] |
| 神行靴 | Godspeed |  | Godspeed Boots | [GRS/6-3-6] |
| 龙舞靴 | Dragonstep |  | Dragon Dance Boots | [GRS/6-3-7] |
| 凤翔靴 | Phoenix |  | Soaring Phoenix Boots | Crafted. [GRS/6-3-8] |
| 飞马靴 | Pegasus |  | Flying Horse Boots | Crafted. [GRS/6-3-9] |
| 中华战斗靴 | Army Boots |  | Chinese Combat Boots | Crafted; the joke 'strongest shoes'. [GRS/6-3-10] |
| 玄武靴 | Dark Boots |  | Black Tortoise Boots | Black Tortoise altar treasure. [GRS/6-3-11] |
| 粗布披风 | Cloth Cape |  | Burlap Cape | [GRS/6-4-1] |
| 精神披风 | Focus Cape |  | Spirit Cape | [GRS/6-4-2] |
| 雷霆披风 | Storm Cape |  | Thunder Cape | [GRS/6-4-3] |
| 雪云披风 | Snow Cape |  | Snowcloud Cape | [GRS/6-4-4] |
| 正气披风 | Noble Cape |  | Righteous Cape | [GRS/6-4-5] |
| 星月披风 | Star Cape |  | Star-Moon Cape | [GRS/6-4-6] |
| 月梦披风 | Moon Cape |  | Moon Dream Cape | [GRS/6-4-7] |
| 万灵披风 | Soul Cape |  | Myriad Spirits Cape | Crafted. [GRS/6-4-8] |
| 鬼惊披风 | Dread Cape |  | Ghost-Scaring Cape | Crafted. [GRS/6-4-9] |
| 玄天披风 | Sky Cape |  | Mystic Sky Cape | Crafted. [GRS/6-4-10] |
| 朱雀披风 | Vermilion |  | Vermilion Bird Cape | Vermilion Bird altar treasure. [GRS/6-4-11] |
| 铁项护手 | Iron Cuff |  | Iron Gauntlets | 护手 = 'Cuff' (gauntlet/bracer) to fit 10. [GRS/6-5-1] |
| 绿石护手 | Jade Cuff |  | Greenstone Gauntlets | [GRS/6-5-2] |
| 强效护手 | Power Cuff |  |  | [GRS/6-5-3] |
| 愤击护手 | Fury Cuff |  |  | [GRS/6-5-4] |
| 轻巧护手 | Deft Cuff |  | Light Gauntlets | [GRS/6-5-5] |
| 异芒护手 | Glint Cuff |  | Strange-Gleam Gauntlets | [GRS/6-5-6] |
| 武神护手 | Valor Cuff |  | Martial God Gauntlets | Lord Guan's. [GRS/6-5-7] |
| 天神护手 | Deity Cuff |  | Heavenly God Gauntlets | Crafted. [GRS/6-5-8] |
| 紫凤护手 | Royal Cuff |  | Purple Phoenix Gauntlets | Crafted. Purple + phoenix = imperial. [GRS/6-5-9] |
| 战神护手 | War Cuff |  | War God Gauntlets | Crafted. [GRS/6-5-10] |
| 白虎护手 | Tiger Cuff |  | White Tiger Gauntlets | White Tiger altar treasure. [GRS/6-5-11] |
| 指环 | Ring |  | Plain Ring | [GRS/6-6-1] |
| 精钢戒 | Steel Ring |  |  | [GRS/6-6-2] |
| 混元戒 | Prime Ring |  | Primordial Ring | [GRS/6-6-3] |
| 龙威戒 | Drake Ring |  | Dragon Might Ring | [GRS/6-6-4] |
| 寒玉戒 | Frost Ring |  | Cold Jade Ring | [GRS/6-6-5] |
| 梦痕戒 | Dream Ring |  | Dream Trace Ring | [GRS/6-6-6] |
| 紫霞戒 | Mist Ring |  | Violet Mist Ring | [GRS/6-6-7] |
| 映雪戒 | Snow Ring |  | Snowlight Ring | Crafted. [GRS/6-6-8] |
| 星悸戒 | Star Ring |  | Starthrill Ring | Crafted. [GRS/6-6-9] |
| 极光戒 | Polar Ring |  | Aurora Ring | Crafted. [GRS/6-6-10] |
| 黄铜项链 | Tin Chain |  | Brass Necklace | 'Brass Chain' is 11; necklaces are 'Chain'. [GRS/6-6-11] |
| 金链子 | Gold Chain |  |  | [GRS/6-6-12] |
| 莹月项链 | Moon Chain |  | Moonglow Necklace | [GRS/6-6-13] |
| 天眼项链 | Seer Chain |  | Heaven's Eye Necklace | [GRS/6-6-14] |
| 七彩项链 | Opal Chain |  | Rainbow Necklace | Seven-coloured light. [GRS/6-6-15] |
| 万金项链 | Rich Chain |  | Fortune Necklace | [GRS/6-6-16] |
| 星辰项链 | Star Chain |  | Starry Necklace | [GRS/6-6-17] |
| 圣洁项链 | Holy Chain |  | Holy Necklace | Crafted. [GRS/6-6-18] |
| 龙爪项链 | Claw Chain |  | Dragon Claw Necklace | Crafted. [GRS/6-6-19] |
| 惑心项链 | Lure Chain |  | Bewitching Necklace | Crafted. [GRS/6-6-20] |

## Consumables

| zh | en | short | alt | note |
|---|---|---|---|---|
| 黑玉断续膏 | Jade Salve |  | Black Jade Mending Paste | HP+100. Old Mr. Wang's medicine. [GRS/6-9-1] |
| 人形何首乌 | Fo-ti Root |  | Man-Shaped Fo-ti | HP+200. [GRS/6-9-2] |
| 人参养荣丸 | Ginseng |  | Ginseng Pill | HP+500. The basic teachers ask for one. [GRS/6-9-3] |
| 九花玉露丸 | Jade Dew |  | Nine Flower Jade Dew Pill | HP+999. [GRS/6-9-4] |
| 还气符 | Qi Charm |  | Qi-Restoring Charm | MP+50. [GRS/6-9-5] |
| 雪参玉蟾丸 | Toad Pill |  | Snow Ginseng Jade Toad Pill | MP+100. [GRS/6-9-6] |
| 灵芝草 | Lingzhi |  | Lingzhi Mushroom | MP+200. [GRS/6-9-7] |
| 茯苓首乌丸 | Poria Pill |  | Poria Fo-ti Pill | MP+500. [GRS/6-9-8] |
| 百花腹蛇膏 | Viper Balm |  | Hundred-Flower Viper Paste | MP+999. Source 腹 typo for 蝮. [GRS/6-9-9] |
| 天香断续胶 | Heaven Gel |  | Heavenly Fragrance Mending Gel | HP+999 MP+999. [GRS/6-9-10] |
| 毒龙涎 | Dragon Dew |  | Venom Dragon Drool | Ping Yizhi's universal antidote (cures Wang Chuyi and the snakebite). [GRS/6-9-11] |
| 大还丹 | Grand Pill |  | Great Restoration Pill | Max MP+100; given on joining any sect. [GRS/6-11-1] |

## Items and materials

| zh | en | short | alt | note |
|---|---|---|---|---|
| 岳王剑 | Yue Fei's Sword |  | Sword of Lord Yue | Quest item (not in GRS): message 'Got Yue Fei's Sword'. |
| 伏虎袈裟 | Tiger Kasaya |  | Tiger-Taming Kasaya | Robe on which Tiger Fist is written (Lu Dayou). |
| 耳环 | earrings |  |  | Ah Fang's dowry. |
| 荷花扇 | lotus fan |  |  | Li Yu's love token. |
| 弹弓 | slingshot |  |  | Huzi's. |
| 引路石 | Waystone |  | Guide Stone | Starting item; returns you to the nearest city (the 'Use / Examine' prompt on the world map). [GRS/6-13-1] |
| 车票 | ticket |  | coach ticket | Generic; numbered tickets below. |
| 车票1 | Ticket 1 |  |  | Capital -> Xixia. Tickets 1-12 keep the source numbers; the description gives the route. [GRS/6-14-1] |
| 车票2 | Ticket 2 |  |  | Capital -> Dali. |
| 车票3 | Ticket 3 |  |  | Capital -> Yangzhou. |
| 车票4 | Ticket 4 |  |  | Xixia -> Dali. |
| 车票5 | Ticket 5 |  |  | Xixia -> Yangzhou. |
| 车票6 | Ticket 6 |  |  | Xixia -> Capital. |
| 车票7 | Ticket 7 |  |  | Dali -> Yangzhou. |
| 车票8 | Ticket 8 |  |  | Dali -> Capital. |
| 车票9 | Ticket 9 |  |  | Dali -> Xixia. |
| 车票10 | Ticket 10 |  |  | Yangzhou -> Capital. |
| 车票11 | Ticket 11 |  |  | Yangzhou -> Xixia. |
| 车票12 | Ticket 12 |  |  | Yangzhou -> Dali. |
| 银票 | banknote |  | silver note |  |
| 银票1 | Note 1000 |  | 1000-tael Note | Named by value (desc: 1000 taels). [GRS/6-14-13] |
| 银票2 | Note 2000 |  | 2000-tael Note | Ten of these buy Yue Fei's Sword. [GRS/6-14-14] |
| 白金矿 | Plat Ore |  | Platinum Ore | Sells for 500. [GRS/6-14-15] |
| 乌金矿 | Gold Ore |  | Black Gold Ore | Sells for 1000. [GRS/6-14-16] |
| 玄铁矿 | Iron Ore |  | Dark Iron Ore | [GRS/6-14-17] |
| 白金 | Platinum |  |  | Smelted from 5 Plat Ore. [GRS/6-14-18] |
| 乌金 | Black Gold |  |  | [GRS/6-14-19] |
| 玄铁 | Dark Iron |  | Meteoric Iron | [GRS/6-14-20] |
| 黑炭 | Charcoal |  | Black Charcoal | [GRS/6-14-21] |
| 无烟炭 | Anthracite |  | Smokeless Coal | [GRS/6-14-22] |
| 白炭 | White Coal |  | White Charcoal | [GRS/6-14-23] |
| 牛皮 | Ox Skin |  | Oxhide | Raw skin; 5 -> 1 Ox Hide at the Hunter. [GRS/6-14-24] |
| 蛇皮 | Snake Skin |  |  | [GRS/6-14-25] |
| 虎皮 | Tiger Skin |  | Tiger Pelt | Wanted by Lu Dayou and Wu Jieshan. [GRS/6-14-26] |
| 牛皮皮革 | Ox Hide |  | Ox Leather | Tanned leather ('Hide' = processed, 'Skin' = raw). [GRS/6-14-27] |
| 蛇皮皮革 | Snake Hide |  | Snake Leather | [GRS/6-14-28] |
| 虎皮皮革 | Tiger Hide |  | Tiger Leather | [GRS/6-14-29] |
| 麻 | Flax |  | Hemp | Raw fibre (also a field ARS). [GRS/6-14-30] |
| 棉 | Cotton |  |  | [GRS/6-14-31] |
| 丝 | Raw Silk |  |  | ARS 3-3-49 (a field 'enemy' that drops it) may read 'Silkworm' if the translator prefers. [GRS/6-14-32] |
| 麻布 | Linen |  | Hemp Cloth | [GRS/6-14-33] |
| 棉布 | Calico |  | Cotton Cloth | [GRS/6-14-34] |
| 丝绸 | Silk |  | Silk Cloth | [GRS/6-14-35] |
| 艾草 | Mugwort |  |  | Herb from Mt. Song. [GRS/6-14-36] |
| 通天草 | Skyreach |  | Skyreach Herb | Herb from Mt. Heng. [GRS/6-14-37] |
| 胡麻花 | Sesame |  | Sesame Flower | Herb from Mt. Wudang. [GRS/6-14-38] |
| 甘霖花 | Rainflower |  | Sweet Rain Flower | Herb from Zhongnan. [GRS/6-14-39] |
| 苻苓草 | Poria |  | Poria Herb | Herb from Mt. Hua. 苻 is a typo for 茯. [GRS/6-14-40] |
| 人和草 | Peace Herb |  | Harmony Herb | Herb from Mt. Emei. [GRS/6-14-41] |
| 盟主令牌 | Chief Seal |  | Alliance Leader's Token | 'Only one in the land'; not equippable. Not given by any script. [GRS/6-14-99] |
| 锦盒 | brocade box |  |  | Holds the map of the north. |
| 北方地图 | map of the north |  |  | Beggars' quest. |
| 紫霞秘籍 | Violet Mist Manual |  |  | Yue Buqun's stolen manual. |
| 家书 | letter from home |  |  |  |
| 信函 | letter |  |  |  |
| 惠泉酒 | Huiquan wine |  |  | One of the five Jiangnan wines. |
| 金陵春 | Jinling Spring |  |  | Wine. |
| 百花酿 | Hundred Flower brew |  |  | Wine. |
| 琼花露 | Jade Blossom dew |  |  | Wine. |
| 双沟大曲 | Shuanggou Daqu |  |  | Wine (a real baijiu brand). |

## Martial arts (MRS)

| zh | en | short | alt | note |
|---|---|---|---|---|
| 九阴真经 | Nine Yin |  | Nine Yin Manual | MRS 4-1-72 (fits 11) and the book Guo Jing gives at the summit ('Nine Yin Manual' in dialogue). [MRS/4-1-72] |
| 葵花宝典 | Sunflower |  | Sunflower Manual | Dongfang Bubai's art (enemy skill / animation banner). [MRS/4-1-11] |
| 基本剑法 | Basic Sword |  | Basic Swordplay | Capital Instructor (1-9-16). Animation banner. [MRS/4-1-1] |
| 疯猫剑法 | Mad Cat |  | Mad Cat Swordplay | Enemy skill; animation banner. [MRS/4-1-2] |
| 开山掌法 | Cleave Palm |  | Mountain-Cleaving Palm | Enemy skill; banner. [MRS/4-1-3] |
| 擒拿手 | Grappling |  | Seizing Hands | Enemy skill; banner. [MRS/4-1-4] |
| 上清快剑 | Swift Sword |  | Shangqing Swift Sword | Enemy skill; banner. [MRS/4-1-5] |
| 万佛朝宗 | All Buddhas |  | Ten Thousand Buddhas | Enemy skill; banner. [MRS/4-1-6] |
| 降龙掌 | Dragon Palm |  | Dragon-Subduing Palm | Enemy skill; banner. [MRS/4-1-7] |
| 化功大法 | Qi Dissolve |  | Energy-Dissolving Art | Ding Chunqiu (4-1-8) and the player's Xingxiu copy (4-1-53). Banner. [MRS/4-1-8; MRS/4-1-53] |
| 辟邪剑法 | Evil Ward |  | Evil-Warding Sword | Yue Buqun's enemy skill; banner. [MRS/4-1-9] |
| 西毒杖法 | Venom Staff |  | Western Venom Staff | Ouyang Feng; banner. [MRS/4-1-10] |
| 血刀刀法 | Blood Blade |  | Blood Blade Saber Art | Enemy (4-1-12) and Xuedao (4-1-45). Banner. [MRS/4-1-12; MRS/4-1-45] |
| 雪山剑法 | Snow Sword |  | Snow Mountain Swordplay | Shi Zhongyu; banner. [MRS/4-1-13] |
| 狂风刀法 | Gale Blade |  | Mad Wind Saber | Tian Boguang; banner. [MRS/4-1-14] |
| 玄冥神掌 | Dark Palm |  | Xuanming Divine Palm | He Biweng; banner. [MRS/4-1-15] |
| 九阴白骨爪 | Bone Claw |  | Nine Yin White Bone Claw | Cyclone Mei; banner. [MRS/4-1-16] |
| 华山剑法 | Hua Sword |  | Huashan Swordplay | Liang Fa. 'Huashan Sword' is 13. [MRS/4-1-17] |
| 伏虎拳 | Tiger Fist |  | Tiger-Taming Fist | Lu Dayou. [MRS/4-1-18] |
| 混元掌 | Prime Palm |  | Primordial Palm | Ying Bailuo. [MRS/4-1-19] |
| 劈石破玉拳 | Stone Fist |  | Stone-Splitting Jade-Breaking Fist | Ying Bailuo. [MRS/4-1-20] |
| 紫霞神功 | Violet Mist |  | Violet Mist Divine Art | Yue Buqun's inner art. [MRS/4-1-21] |
| 夺命三仙剑 | Fatal Trio |  | Deadly Three Immortals Sword | Cheng Buyou (full name 夺命连环三仙剑). [MRS/4-1-22] |
| 独孤九剑 | Dugu Nine |  | Nine Swords of Dugu | Feng Qingyang. [MRS/4-1-23] |
| 太祖长拳 | Taizu Fist |  | Emperor Taizu Long Fist | Teaching Elder. [MRS/4-1-24] |
| 疯魔杖法 | Mad Staff |  | Demon-Mad Staff | Teaching Elder. [MRS/4-1-25] |
| 莲花掌 | Lotus Palm |  |  | Teaching Elder. [MRS/4-1-26] |
| 打狗棒法 | Dog Beater |  | Dog-Beating Staff | Huang Rong. [MRS/4-1-27] |
| 降龙十八掌 | 18 Dragons |  | Eighteen Dragon-Subduing Palms | Hong Qigong. 'Dragon Palms' (12) does not fit 11 and would clash with 降龙掌 Dragon Palm. [MRS/4-1-28] |
| 武当长拳 | Wudang Fist |  | Wudang Long Fist | Yu Daiyan. [MRS/4-1-29] |
| 绕指柔剑 | Coil Sword |  | Finger-Wrapping Soft Sword | Yu Daiyan. [MRS/4-1-30] |
| 柔云剑法 | Cloud Sword |  | Soft Cloud Sword | Yu Daiyan (needs a Zhenwu). [MRS/4-1-31] |
| 纯阳无极功 | Pure Yang |  | Pure Yang Limitless Art | Zhang Sanfeng (six herbs). [MRS/4-1-32] |
| 太极拳 | Taiji Fist |  | Tai Chi Fist | Zhang Sanfeng (answer 'Fist'). [MRS/4-1-33] |
| 太极剑 | Taiji Sword |  | Tai Chi Sword | Zhang Sanfeng (answer 'Sword'). [MRS/4-1-34] |
| 全真剑法 | Quanzhen |  | Quanzhen Swordplay | Wang Chongyang. [MRS/4-1-35] |
| 昊天掌 | Sky Palm |  | Vast Heaven Palm | [MRS/4-1-36] |
| 同归剑法 | Doom Sword |  | Shared-Doom Sword | 'Die together' sword. [MRS/4-1-37] |
| 三花聚顶掌 | Crown Palm |  | Three Flowers Crown Palm | [MRS/4-1-38] |
| 左右互搏 | Dual Hands |  | Left-Right Combat | Zhou Botong's art. [MRS/4-1-39] |
| 少林长拳 | Long Fist |  | Shaolin Long Fist | [MRS/4-1-40] |
| 罗汉拳 | Arhat Fist |  |  | [MRS/4-1-41] |
| 达摩剑法 | Damo Sword |  | Bodhidharma Sword | [MRS/4-1-42] |
| 龙爪功 | Dragon Claw |  | Dragon Claw Art | [MRS/4-1-43] |
| 九阳神功 | Nine Yang |  | Nine Yang Divine Art | [MRS/4-1-44] |
| 灭仙掌 | Godslayer |  | Immortal-Slaying Palm | Xuedao. [MRS/4-1-46] |
| 雪遁步行 | Snow Step |  | Snow-Escape Walk | Xuedao. [MRS/4-1-47] |
| 血海魔功 | Blood Sea |  | Blood Sea Demonic Art | Xuedao. [MRS/4-1-48] |
| 放毒法 | Venom Cast |  | Poison-Releasing Art | Xingxiu. [MRS/4-1-49] |
| 抽随掌 | Marrow Palm |  | Marrow-Drawing Palm | Xingxiu. Source 随 typo for 髓. [MRS/4-1-50] |
| 三阴蜈蚣爪 | Centipede |  | Three Yin Centipede Claw | Xingxiu. [MRS/4-1-51] |
| 天山杖法 | Tian Staff |  | Tianshan Staff | Xingxiu. [MRS/4-1-52] |
| 飘雪穿云掌 | Cloud Palm |  | Drifting Snow Cloud-Piercing Palm | Emei. [MRS/4-1-54] |
| 回风拂柳剑 | Wind Willow |  | Whirlwind Willow Sword | Emei. [MRS/4-1-55] |
| 灭剑 | Extinction |  | Mie Sword | Emei; with 绝剑 the two halves of Miejue's sword ('灭绝剑法 is two sword arts'). [MRS/4-1-56] |
| 绝剑 | Severance |  | Jue Sword | Emei. [MRS/4-1-57] |
| 灭绝剑法 | Miejue Sword |  | Extinction-Severance Sword | Chatter only. |
| 佛光普照掌 | Buddha Glow |  | Buddha's Light Palm | Emei. [MRS/4-1-58] |
| 玉女剑法 | Jade Maiden |  | Jade Maiden Swordplay | Ancient Tomb. [MRS/4-1-59] |
| 美女拳法 | Beauty Fist |  | Beauty Boxing | Ancient Tomb. [MRS/4-1-60] |
| 天罗地网掌 | Sky Net |  | Heaven-and-Earth Net Palm | Ancient Tomb. [MRS/4-1-61] |
| 赤炼神掌 | Red Serpent |  | Red Serpent Divine Palm | Ancient Tomb (Li Mochou's palm). [MRS/4-1-62] |
| 黯然消魂掌 | Sorrow Palm |  | Soul-Dispersing Sorrow Palm | Ancient Tomb (Yang Guo's). [MRS/4-1-63] |
| 天羽奇剑 | Sky Feather |  | Heavenly Feather Sword | Lingjiu. [MRS/4-1-64] |
| 天山折梅手 | Plum Hand |  | Tianshan Plum-Plucking Hand | Lingjiu. [MRS/4-1-65] |
| 八荒六合 | Eight Wilds |  | Eight Wilds Supremacy Art | Lingjiu; full name 八荒六合唯我独尊功 (chatter). [MRS/4-1-66] |
| 生死符 | Death Charm |  | Life-and-Death Charm | Lingjiu. 符 = Charm as in fmj. [MRS/4-1-67] |
| 恒山剑法 | Heng Sword |  | Hengshan Swordplay | [MRS/4-1-68] |
| 天长掌法 | Ever Palm |  | Everlasting Palm | Hengshan. [MRS/4-1-69] |
| 万花剑法 | Bloom Sword |  | Myriad Flowers Sword | Hengshan. [MRS/4-1-70] |
| 恒山剑阵 | Heng Array |  | Hengshan Sword Array | Hengshan. 阵 = Array as in fmj. [MRS/4-1-71] |
| 基本身法 | Basic Step |  | Basic Footwork | Xixia Instructor; Agility +5% for 3 turns. Banner. [MRS/4-2-1] |
| 基本心法 | Basic Qi |  | Basic Inner Art | Yangzhou Instructor; Attack/Defense +5% for 3 turns. Banner. [MRS/4-2-2] |
| 基本医术 | Basic Heal |  | Basic Medicine | Dali Instructor. Banner. Healing family: Basic / Minor / Mid / Major / Grand / Heng Heal. [MRS/4-3-1] |
| 低级医术 | Minor Heal |  | Lesser Medicine | Hengshan. [MRS/4-3-2] |
| 中级医术 | Mid Heal |  | Medium Medicine | Hengshan. [MRS/4-3-3] |
| 高级医术 | Major Heal |  | Greater Medicine | Hengshan. [MRS/4-3-4] |
| 特级医术 | Grand Heal |  | Supreme Medicine | Hengshan. [MRS/4-3-5] |
| 恒山医术 | Heng Heal |  | Hengshan Medicine | Hengshan. [MRS/4-3-6] |

## Other martial terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 重阳剑法 | Chongyang Sword |  |  | Chatter (Quanzhen). |
| 天罡北斗阵 | Big Dipper Array |  | Heavenly Dipper Formation | Chatter (Quanzhen). |
| 太极 | Taiji |  | Tai Chi |  |
| 内功 | inner art |  | internal kung fu |  |
| 武功 | martial arts |  | kung fu |  |
| 武学 | martial arts |  |  |  |
| 剑法 | swordplay |  |  |  |
| 轻功 | lightness skill |  | qinggong |  |

## Other story terms

| zh | en | short | alt | note |
|---|---|---|---|---|
| 福威镖局 | Fuwei Escorts |  | Fuwei Escort Agency | Escort agency with branches in all four cities (delivery quests). |
| 同仁堂 | Tongren Hall |  |  | Pharmacy chain in all four cities. |
| 金国 | Jin |  | the Jin Empire |  |
| 大金 | the Great Jin |  |  |  |
| 金兵 | Jin soldiers |  |  |  |
| 金贼 | Jin dog |  | Jin traitor | Insult for Qiu Qianren. |
| 宋朝 | the Song |  | Song dynasty |  |
| 抗金 | resist the Jin |  |  |  |
| BOSS工作室 | BOSS Studio |  |  | The hobby team credited at the end. |
| 道德经 | Tao Te Ching |  | Daodejing | Yu Daiyan quotes chapters 1, 25, 33, 41, 42; use a standard translation. |
| 般若波罗蜜多心经 | Heart Sutra |  |  |  |
| 华山论剑 | Mount Hua Summit |  | Contest of Mount Hua | The finale (needs Lv 70 and the Zhou Botong event). |
| 天下第一 | best in the world |  | number one under heaven |  |
| 江湖 | the martial world |  | jianghu |  |
| 武林 | the martial world |  | wulin |  |
| 镇坛之宝 | altar treasure |  |  | The four altar guardians' prize. |
| 比武招亲 | marriage tournament |  |  | Mu Yi's contest. |
| 清圣浊贤 | clear sage, cloudy worthy |  |  | Huang Rong's riddle: an old name for wine (clear = sage, cloudy = worthy). Answer 酒 Wine. |
| 大象无形 | the great image has no form |  |  | Tao Te Ching 41. Pun: 大象 also means 'elephant' (wrong answer 'an animal'). Keep the joke with a note-like rewording if needed. |
| 四大皆空 | all is emptiness |  |  | Buddhist saying. |
| 主线剧情 | main story |  |  | End-of-game line. |
| 高考 | college entrance exam |  | gaokao | The developer apologises: busy with the gaokao. |
| 金庸群侠传 | Heroes of Jin Yong |  | Jin Yong Qun Xia Zhuan | Game title (the 1996 DOS game's established English name). |
| 之射雕英雄 | Condor Heroes |  | Legend of the Condor Heroes | Title-logo subtitle. 'Heroes of Jin Yong: Condor Heroes'. |
| 射雕英雄 | Condor Heroes |  | Legend of the Condor Heroes |  |

## UI, stats and choices

| zh | en | short | alt | note |
|---|---|---|---|---|
| 内力 | MP |  | internal energy | Stat in descriptions = the engine MP (真气); in dialogue "internal energy". '内力最大值+10' -> 'Max MP+10'. |
| 两 | tael |  | taels | Currency ('500 taels'). |
| 纹银 | silver |  |  |  |
| 系统提示 | Note |  | System | Tag in '系统提示：...' (Lv 70 hint). |
| 新的征程 | New Game |  | A New Journey | Title menu (title-screen image/engine, not in the string table), as fmj. |
| 再续前缘 | Continue |  | Renew Old Bonds | Title menu (not in the string table), as fmj. |
| 防御 | Defense |  | DEF | Stat in descriptions. |
| 攻击 | Attack |  | ATK |  |
| 灵力 | Spirit |  | SPI |  |
| 生命 | HP |  |  | Rings/necklaces '生命+1': render 'HP+1'. |
| 身法 | Agility |  | AGI |  |
| 抗毒 | resist Poison |  |  | Equipment immunity (also 抗眠 Sleep, 抗封 Silence, 抗乱 Confuse). |
| 抗眠 | resist Sleep |  |  |  |
| 抗封 | resist Silence |  |  |  |
| 抗乱 | resist Confuse |  |  |  |
| 带封 | inflicts Silence |  |  | Dragonbane description. |
| 回合 | turns |  |  |  |
| 级 | Lv |  | level | '需要10级以上' -> 'You must be Lv 10 or higher.' |
| 请选择游戏主角 | Choose your hero |  |  | Message before the protagonist choice. |
| 学会新武功 | Learned a new art! |  |  | Sect masters. |
| 使用 | Use |  |  | Choice on the world map (with the Waystone). |
| 查看 | Examine |  | Look |  |
| 要去 | Go |  | Yes, go | Boatman to/from Peach Blossom Island. |
| 不去 | Stay |  | Not now |  |
| 挑战 | Challenge |  |  | Altar guardians. |
| 离开 | Leave |  |  |  |
| 酒 | Wine |  |  | Riddle answer (correct). |
| 茶 | Tea |  |  | Riddle answer (wrong). |
| 加入 | Join |  |  | Sect join prompt. |
| 不加入 | Decline |  | Not now |  |
| 责无旁贷 | Leave it to me |  | It's my duty | Accept a sect mission. |
| 难担此重任 | Not up to it |  | I can't take this on | Refuse a sect mission. |
| 帮 | Help |  |  |  |
| 不帮 | Won't help |  |  |  |
| 劝说 | Dissuade |  | Talk him out of it | Su Zhong / Niuniu. |
| 赞同 | Agree |  |  |  |
| 支持 | Encourage |  | Support |  |
| 买票 | Buy ticket |  |  | Coach station. |
| 坐车 | Take coach |  | Ride |  |
| 下一个城市 | Next city |  |  |  |
| 哪也不去 | Stay here |  | Nowhere |  |
| 买东西 | Buy |  |  |  |
| 卖东西 | Sell |  |  |  |
| 住店 | Rent a room |  | Stay | Inn (10 taels). |
| 交谈 | Talk |  |  |  |
| 我想学 | Teach me |  | I want to learn |  |
| 我不想学 | No thanks |  |  |  |
| 运 | Deliver |  |  | Escort agency job. |
| 不运 | Decline |  |  |  |
| 帮我打吧 | Smelt it |  | Please do | Blacksmith. |
| 不要你帮忙 | No thanks |  |  |  |
| 下一种 | Next |  | Next one | Crafting list paging. |
| 不想做了 | Never mind |  |  |  |
| 帮我织吧 | Weave it |  |  | Weaver. |
| 帮我做吧 | Make it |  |  | Hunter / swordsmith. |
| 铸剑 | Forge sword |  |  |  |
| 查看材料 | Recipes |  | See materials | Shows the material lists. |
| 赌 | Bet |  |  | Casino (10 taels, pays 10:1). |
| 不赌 | Pass |  |  |  |
| 我帮你去问问他 | I'll ask him |  |  |  |
| 无能为力 | Can't help |  |  |  |
| 我无能为力 | I can't help |  |  |  |
| 做装备 | Craft gear |  |  | Tailor / jeweller. |
| 拳 | Fist |  |  | Zhang Sanfeng's quiz -> Taiji Fist. |
| 剑 | Sword |  |  | Zhang Sanfeng's quiz -> Taiji Sword. |
| 最大形状 | The greatest form |  | Formless greatness | Correct answer to Yu Daiyan's quiz. |
| 一种动物 | An animal |  | An elephant | Wrong answer (大象 = elephant pun). |
| 卖 | Sell |  |  |  |
| 不卖 | Don't sell |  |  |  |
| 卖白金矿 | Sell Plat Ore |  |  |  |
| 卖乌金矿 | Sell Gold Ore |  |  |  |
| 我帮你去找他 | I'll find him |  |  |  |
| 我即刻就去 | I'll go now |  |  |  |
| 找齐了 | Got them all |  |  |  |
| 没找齐 | Not yet |  |  |  |
| 我帮你跟她说说 | I'll talk to her |  |  |  |
| 我可帮不上忙 | Can't help you |  |  |  |
| 我帮你这个忙吧 | I'll help you |  |  |  |
| 买 | Buy |  |  |  |
| 不买 | Don't buy |  |  |  |
| 帮他 | Help him |  |  |  |
| 我帮你 | I'll help |  |  |  |
| 询问情况 | What's wrong? |  |  |  |
| 不理睬 | Ignore |  |  |  |
| 愿意 | I will |  | Yes |  |
| 不愿意 | I won't |  | No |  |
| 联手 | Join forces |  |  | Side with Yue Buqun (kill the Sword School). |
| 不联手 | Refuse |  |  | Side with Feng Qingyang (fight Yue Buqun). |
