# 伏魔记 English glossary (draft for review)

Status: **draft, awaiting approval** before translation starts.
Machine-readable source: `docs/glossary.jsonl` (one term per line: `zh`, `en`, `category`, `count`, `alt`, `note`, `source_ids`).
This page is a readable summary of the same data.

- `count` = how many times the zh string occurs as a substring across `work/fmj.strings.jsonl` (all kinds),
  plus the number of engine-string slots (`ENG/...`) for UI terms. Substring counting over-counts short terms
  (道 also matches 知道, 无机 also matches 无机子), so treat counts as "how common", not exact.
- `en` always respects the field limits: item names (grs.name) <= 11 ASCII chars, ARS names (characters, monsters,
  scene objects) <= 11, map names <= 12, magic names (mrs.name) <= 19, choices <= 19, packed menu labels <= 6 and
  within their pixel slot. When the natural name is longer, the long form is in `alt`.
- All `en`/`alt` values are plain ASCII (no accents, curly quotes or em dashes). The validation script checked every
  item/magic/ARS/map/scene/choice name in the string table has a term and fits its limit.

## Conventions

**Names.**
- People: Hanyu pinyin without tone marks, surname first, given name written as one word
  (Liu Qingfeng, Murong Xiaomei, Murong Xuan, Li Hu). The 11-byte character field cannot hold full names, so party
  members use the given name (Qingfeng, Xiaomei, Pingzhi); dialogue may use full names where they are spoken.
  阿- diminutives are written "Ah X" (Ah Xia, Ah Jun).
- Nicknames, epithets and monster names are translated (Madman, Lockmaster, Crimson Demon, Swordwarden, Thunderling).
  Taoist name suffixes are dropped (无机子 -> Wuji); 道人 becomes "Taoist X" (Taoist Chongxu).
- The dev-team cameos (通宵虫, 南方小鬼, 不点点) are online handles; they are translated as handles (Allnighter,
  South Imp, Tiny Tot) - see open decisions.
- Places: real places use pinyin (Mt. Sanqing, Jianye, Fengdu, Mt. Heming, Mt. Zhong, Longquan); invented places with
  a meaning are translated (Heartsease = 忘忧村 'forget-sorrow village', Stonedream = 石梦城, Whitewater = 白水镇,
  Cloudstep, Sky Summit). Mountains are "Mt. X"; 入口 entrances are "X Gate"; 洞 caves "X Cave". Generic rooms
  get generic English (Kitchen, Dormitory, Herb Shop, Pawnshop).
- Mythology uses the standard English where it fits: Four Symbols (Blue Dragon, White Tiger, Red Phoenix,
  Dark Turtle - shortened from Azure Dragon / Vermilion Bird / Black Tortoise for the 11-byte field), Ox-Head,
  Bai Wuchang, Zhou Chu, Zhang Daoling, Way of the Five Pecks of Rice.

**Recurring vocabulary.** 魔 = demon (demonic), 妖 = fiend, 妖怪 = monster, 妖魔 = demons (generic), 鬼 = ghost,
仙 = immortal, 道 = the Way, 伏魔 = Demonbane (Demonbane Sword, Primal Demonbane Array; places shorten to "Demon":
Demon Cave, Demon Trail), 阵 = Array, 符 = Charm, 咒 = Spell (Curse when evil), 诀 = Mantra, 剑 = sword,
刀 = blade/saber, 双剑 = twin swords, 霸王 = Tyrant (Tyrant Bell), 蛟 = wyrm, 天师 = Celestial Master
(short "Sage" in compounds), 四象 = Four Symbols.

**Forms of address.** Translated into natural English equivalents rather than kept as pinyin:
师父/师傅 = Master, 师兄 = Brother (as in the demo dialogue), 师弟 = little brother, 大师兄 = Big Brother,
师叔 = Uncle (Uncle Chongxu), 掌门 = Sect Head, 道长 = Master Taoist (villagers to the hero), 大侠 = hero,
恩公 = benefactor, 客官 = sir, 姑娘 = Miss, 婆婆 = Granny (Granny Cai), 大哥 = Brother (Brother Liu),
姐姐 = Sister (Sister Yuan), 掌柜 = Innkeeper, 村长 = Elder, 镇长 = Mayor.
Speaker tags stay in the "Name: text" form the game already uses (护剑神:... -> "Swordwarden: ...").

**Tone and register.** Plain modern English with light wuxia flavor. The source is a light-hearted 2004 hobby
game: the hero is cocky and jokey ("Xiaomei, tonight I'm treating you to snake soup"), the bosses trade insults
(lizard / puppy), there are fourth-wall jokes (dev cameos, "a super sword you can't equip - ha!", the Saint Seiya
armor, a gas mask). Keep the jokes, keep it readable, avoid archaic "thee/thou" and avoid heavy pinyin.
Classical tags (the opening scroll's 天地玄黄 line, 道非道，魔非魔 echoing the Tao Te Ching) can be slightly
elevated. Censored swearing like `@#$!` stays as-is.

**UI.** The engine strings keep the `tools/font/engine_demo.py` drafts (all fit their pixel slots) except three
packed menu labels shortened to <= 6 characters (Setup, Music, Mute; demo forms in `alt`). Item and magic
descriptions use the same stat words as the status screen: HP, MP, Attack, Defense, Agility, Spirit, Luck
(abbreviate ATK/DEF/AGI/SPI/LCK only if a description overflows its 102/86 bytes); statuses Poison, Confuse,
Silence, Sleep (status-screen abbreviations Psn/Cnf/Sil/Slp); 回合 = turns.

## Open decisions for the reviewer

1. **Hero names in battle/menus**: given names only (Qingfeng / Xiaomei / Pingzhi) because "Liu Qingfeng" (12)
   and "Murong Xiaomei" (14) do not fit 11 bytes. OK, or prefer surnames (Liu / Murong / Yuan)?
2. **天师**: "Celestial Master" in dialogue but "Sage" in 11-byte compounds (Sage Charm, Sage Robe, Sage Spirit,
   Sage's Tomb). Alternative: "Tianshi" everywhere, or "Sage" everywhere.
3. **伏魔**: "Demonbane" (sword, array, game title) but "Demon" in place names (Demon Cave, Demon Trail) to fit
   12-byte map names. Alternative: "Sealing Cave" etc.
4. **Game title**: "Demonbane Chronicle" vs "Record of Demon Quelling" vs keeping "Fu Mo Ji".
5. **The sword**: dialogue calls the sword pulled from Demon Cave 伏魔剑 "Demonbane Sword"; the key item is
   无机乾坤剑 and the ARS object 无极乾坤剑 (both "Wuji Sword"). Are they the same sword (then use one name
   everywhere), or is the Wuji Sword a separate item?
6. **玄虚子 vs 冲虚**: Wuji (1-2-2) says "your uncle 玄虚子 sent a pigeon from Zhongshan", but the uncle at
   Zhongshan is 冲虚道人; 玄虚真人 is also the ancient master who sealed the Red Phoenix. Fix the 1-2-2 line to
   "Chongxu" (recommended), or translate literally?
7. **North Sea guards**: ARS 蛇护院 'snake guard' vs dialogue 龙护院 / 北海龙 'dragon'. Glossary unifies to
   Drake Guard / North Sea Drake (pairs with Wyrm). Accept, or keep the literal Snake Guard?
8. **Ghost King's battle name**: ARS 真阎罗 "True Yama" while dialogue only says 鬼王 "Ghost King". Use
   "Ghost King" for the battle name too?
9. **The steal skill**: Pingzhi teaches "妙手空空" but the magic list shows 飞龙探云手 ("Dragon Cloud Grab").
   Make her line name the listed skill?
10. **Dev-team handles** (通宵虫 Allnighter, 南方小鬼 South Imp, 不点点 Tiny Tot, 小画家 Painter,
    陈泽伟 Chen Zewei): translate the handles (as drafted) or keep pinyin to honor the real people?
11. **小画家** ("little painter", Granny Cai's daughter): "Painter" fits 11 bytes but is odd in dialogue;
    allow "Little Painter" in dialogue, or give her a pinyin name?
12. **道长** (villagers addressing the hero): "Master Taoist" vs "Reverend" vs "Taoist sir".
13. **Menu labels**: engine_demo's Options / Music On / Music Off exceed 6 characters (though they fit the pixels).
    Drafted Setup / Music / Mute. Keep the demo versions instead?
14. **三清宫 / 无机阁**: "Sanqing Hall" and "Wuji Tower" fit the 12-byte map field; "Sanqing Temple" (14) and the
    demo's "Wuji Pavilion" (13) do not. The demo dialogue in tools/font/build_demo.py says "Wuji Pavilion" and
    would need updating.
15. **龟头虫** (a deliberately crude pun): drafted as the neutral "Turtle Bug". Keep it clean or find a cheeky name?
16. **Twin-sword weapon names** mix "X Twins" and single words (Shadowless, Enigma, Yin Yang, Hibiscus) because of the
    11-byte limit. Acceptable?

## Inconsistencies found in the source

| zh variants | where | glossary |
|---|---|---|
| 无机乾坤剑 / 无极乾坤剑 | GRS 6-14-12 / ARS 3-4-8 | both "Wuji Sword" |
| 伏魔剑 / 伏魔宝剑 vs 无机乾坤剑 | dialogue vs items | open decision 5 |
| 无机 / 无机子 / 无机道人 / 无机道长 | everywhere | Wuji / Wuji / Taoist Wuji / Master Wuji |
| 师父 / 师傅 | 1-1-1, map 师傅居 | both "Master" |
| 护剑神 / 护剑兽 | 1-2-18 / 1-2-2 | both "Swordwarden" |
| 玄虚子 / 冲虚道人 | 1-2-2 / 1-8-x | open decision 6 |
| 参虚阁 | Zhongshan scene name | possibly 冲虚; kept "Canxu Tower" |
| 蔡婆婆 / 蔡大妈 | dialogue / ARS 3-2-8 | both "Granny Cai" |
| 李府 / 李俯 | dialogue / scene names | both "Li Manor" (俯 typo) |
| 瘴气林 / 毒瘴林 | dialogue / map + scene | both "Miasma Wood" |
| 腥风 / 醒风 | 1-12-3 / 1-10-x | both "reek wind" (醒 typo) |
| 蛇护院 / 龙护院 / 北海龙 | ARS / dialogue | open decision 7 |
| 真阎罗 / 鬼王 | ARS / dialogue | open decision 8 |
| 天师魂魄 / 天师精魄 | ARS / speaker tag | both "Sage Spirit" |
| 妙手空空 / 飞龙探云手 | 1-14-8 / MRS 4-5-1 | open decision 9 |
| 无忧丹 / 无忧仙丹 | 1-10-2 / GRS 6-11-6 | both "Bliss Pill" |
| 蛇妖 / 蛇妖男 | dialogue + object / ARS monster | both "Snake Demon" |
| 建业客栈 / 新野客栈 | scene / map 2-2-21 | Jianye Inn / Xinye Inn (leftover map label) |
| 村长家 | scene name reused in Whitewater (1-9-4), where it is the Mayor's house | "Elder's House"; translator may adapt |
| 三清宫丹房 / 三清练丹房 / 炼丹房 | scene / map / Zhongshan | all "Elixir Room" (练 typo) |
| 独孤刀 / 孤独刀 | MRS name / its description | name wins: "Lone Blade" |
| 冰心决 | MRS 4-3-12 | 决 for 诀; "Icy Heart Mantra" |
| 鬼针胃, 金钢肌 | GRS 6-2-13, 6-4-6 | 胃/肌 typos for 胄/甲 (armor) |
| 矛山 | 天师符法 description | typo for 茅山 Maoshan |
| 幸运 / 吉运 | engine label / descriptions | both "Luck" |
| 武术, 体力 | a few descriptions | read as Attack / HP |
| 珍珠衫 / 珍珠衣 | name / own description | "Pearl Shirt" |


## Counts

| category | terms |
|---|---|
| person | 73 |
| title | 38 |
| sect | 8 |
| place | 176 |
| monster | 68 |
| item | 16 |
| weapon | 34 |
| armor | 87 |
| consumable | 84 |
| magic | 105 |
| skill | 6 |
| other | 74 |
| ui | 102 |
| **total** | **871** |

Numbered dev labels (三清游人1..6, 歇息台子1..7, 怨妇幻妖1..8, 转折路口1..5, 灯洞1..8, 民宅1..5, ...) are separate rows in the .jsonl (`<base English> <n>`) but are collapsed into their base row below.


## People and speakers

| zh | en | note |
|---|---|---|
| 柳清风 | Qingfeng | Hero (party slot 1), young disciple of Wuji at Sanqing Hall. Full name Liu Qingfeng does not fit the 11-byte ARS field, so the field uses the given name; dialogue may use the full name where it is spoken in full. [ARS/3-1-1] *Alt:* Liu Qingfeng. |
| 清风 | Qingfeng | How Wuji, Chongxu and others address the hero. |
| 慕容小梅 | Xiaomei | Heroine (party slot 2), daughter of Elder Murong Xuan of Heartsease, trained in medicine; twin-sword fighter and healer. Field limit 11 -> given name; long form in dialogue/system messages ('Murong Xiaomei joins the party'). [ARS/3-1-2; ARS/3-2-6] *Alt:* Murong Xiaomei. |
| 小梅 | Xiaomei | Short name used by everyone. *Alt:* Mei. |
| 慕容 | Murong | Compound surname of Xiaomei's family (慕容家 = the Murong family; 慕容家双剑术 = Murong twin-sword style). |
| 袁萍芷 | Pingzhi | Third party member; met as a thief in Jianye, secretly the Red Phoenix (朱雀) sent by Wuji to watch the hero. Field limit 11 -> given name. [ARS/3-1-3; ARS/3-2-7] *Alt:* Yuan Pingzhi. |
| 无机 | Wuji | Hero's master, head of Sanqing Hall; legendary swordsman who fought the Crimson Demon 20 years ago; secretly turning demonic and final boss. Pinyin; 无机 and 无极 both read Wuji, which conveniently merges the two spellings of the sword (see 无机乾坤剑). [ARS/3-3-47] |
| 无机子 | Wuji | Formal Taoist name (子 suffix). Dropped in English: 'I am Liu Qingfeng, disciple of Wuji of Sanqing Hall.' *Alt:* Wujizi; Master Wuji. |
| 无机道人 | Taoist Wuji | ARS NPC name (3-2-1) and once in tourist dialogue. Fits 11 bytes. [ARS/3-2-1] *Alt:* Wuji the Taoist. |
| 无机道长 | Master Wuji | Used only in the opening scroll (5x): the legend of the peerless swordsman. *Alt:* Taoist Master Wuji. |
| 慕容玄 | Murong Xuan | Xiaomei's father, village elder of Heartsease; killed by the Snake Demon (1-3-12). [ARS/3-2-9] |
| 蔡婆婆 | Granny Cai | Old woman in Heartsease whose daughter (the little painter) was abducted by Li Hu. |
| 蔡婆 | Granny Cai | Short form in the scene name 蔡婆家. |
| 蔡大妈 | Granny Cai | ARS name of the same NPC (3-2-8); dialogue always says 蔡婆婆. Unified as Granny Cai. INCONSISTENT in source (大妈 'auntie' vs 婆婆 'granny'). [ARS/3-2-8] *Alt:* Auntie Cai. |
| 小画家 | Painter | Granny Cai's daughter, a nickname ('little painter'); probably a dev-team artist's handle, like the other cameos. Short form for the 11-byte field; 'Little Painter' in dialogue if the reviewer accepts two forms. [ARS/3-2-20] *Alt:* Little Painter; Xiao Huajia. |
| 阿霞 | Ah Xia | Heartsease villager (jokes about being a clerk in the 'development department'). [ARS/3-2-21] *Alt:* Axia; A-Xia. |
| 东东 | Dongdong | Heartsease villager. [ARS/3-2-22] |
| 疯子 | Madman | Heartsease villager: 'Everyone calls me "Madman", but I'm actually very handsome!' [ARS/3-2-23] *Alt:* Loony. |
| 老孟 | Old Meng | Heartsease villager (a woman, despite 老) who sends a love letter to her boyfriend Ah Jun in Jianye. [ARS/3-2-24] *Alt:* Meng. |
| 阿军 | Ah Jun | Old Meng's boyfriend in Jianye, a locksmith nicknamed 万锁开; gives the Picklocks. *Alt:* Ajun; A-Jun. |
| 万锁开 | Lockmaster | Ah Jun's nickname ('opens ten thousand locks'). *Alt:* Wan Suokai. |
| 猎人 | Hunter | Hunter near the Miasma Wood who explains the Reed Mail. 猎户 in his dialogue = same. [ARS/3-2-19] |
| 鲁斧 | Lu Fu | Descendant of Lu Ban living in Stonedream; owner of the Reed Mail. [ARS/3-2-26] |
| 鲁公 | Lord Lu | Lu Ban, legendary craftsman (鲁班 in item descriptions); 'Lord Lu made the Reed Mail'. *Alt:* Master Lu; Lu Ban. |
| 鲁班 | Lu Ban | Legendary craftsman in Reed Mail descriptions; same person as 鲁公. |
| 李虎 | Li Hu | Thug boss of Stonedream who kidnaps girls and stole the Reed Mail; boss fight (ARS 3-2-25 NPC, 3-3-9 monster). Name means 'tiger Li' but pinyin per convention. [ARS/3-2-25; ARS/3-3-9] *Alt:* Tiger Li. |
| 老王 | Old Wang | Li Hu's servant; can be spared (then his wife tells of the secret passage) or killed. Also ARS monster 3-3-19. [ARS/3-3-19] |
| 王妻 | Mrs. Wang | Old Wang's wife, former wet-nurse in Li Manor. |
| 冲虚道人 | Taoist Chongxu | The hero's uncle (师叔), head of Zhongshan Abbey. Speaker tag in 1-8-x. |
| 冲虚 | Chongxu | As in 冲虚居 (Chongxu's room). |
| 玄虚子 | Xuanxu | Named once by Wuji (1-2-2) as 'your uncle Xuanxu' who sends the pigeon from Zhongshan, but the uncle at Zhongshan is 冲虚. INCONSISTENT in source; recommend 'Chongxu' in 1-2-2 (reviewer decision). *Alt:* Chongxu (fix). |
| 玄虚真人 | Perfected Xuanxu | Ancient master who sealed the Red Phoenix in Demon Cave (1-14-8). 真人 = Perfected One (Taoist title). *Alt:* Xuanxu the Perfected. |
| 参虚 | Canxu | Only in scene name 参虚阁 at Zhongshan; possibly a slip for 冲虚. |
| 张道陵 | Zhang Daoling | Historical founder of Celestial Master Taoism (the 天师); his soul fragment appears in the Sage's Tomb. |
| 天师精魄 | Sage Spirit | Speaker tag in the tomb; ARS calls it 天师魂魄 (same entity, both -> Sage Spirit). *Alt:* Celestial Master's Soul. |
| 周处 | Zhou Chu | Jin-dynasty hero of the 'Zhou Chu eliminates the three scourges' legend (tiger, river dragon, himself); now a local god with a shrine in Nanbei Village. |
| 周公 | Lord Zhou | Villagers' name for Zhou Chu in Nanbei Village (not the Duke of Zhou). |
| 天道 | Tiandao | Villain: head (掌教) of the Way of the Five Pecks of Rice at Mt. Heming, steals the Tyrant Bell; ARS boss 3-3-44. Name = 'Heaven's Way' (cf. the banner 替天行道); pinyin keeps it a name. [ARS/3-3-44] *Alt:* Heavenway. |
| 赤血天魔 | Crimson Demon | Full title in the opening scroll ('the great archfiend of the age - the Crimson Demon'). *Alt:* Crimson Heavenly Demon; Chixue. |
| 鬼王 | Ghost King | Ruler of the ghosts in Fengdu; hates Taoists because of Tiandao. Fought as ARS 真阎罗. |
| 黑无常 | Hei Wuchang | His absent brother ('away on business'). *Alt:* Black Impermanence. |
| 牛头马面 | Ox-Head and Horse-Face | The two underworld vanguard generals the ghosts lost to the bell. |
| 北海蛟 | North Sea Wyrm | Speaker tag; Blue Dragon's guard (蛟 jiao = flood dragon). The hero mocks it as a lizard. Fought as ARS 蛟护院. *Alt:* North Sea Jiao. |
| 北海龙 | North Sea Drake | Speaker tag; the other guard, mocked as a puppy. 'Drake' pairs with 'Wyrm' and fits the ARS field. Fought as ARS 蛇护院 (sic). *Alt:* North Sea Dragon. |
| 通宵虫 | Allnighter | Dev-team cameo (credited for engine and production); handle = 'all-night bug'. Teaches 百虫欺天. Real person's online handle - see open decisions. [ARS/3-2-32] *Alt:* Tongxiaochong; All-Night Bug. |
| 南方小鬼 | South Imp | Dev-team cameo (credited engine/production); handle = 'little imp from the south'. Teaches 泽伟补命术. [ARS/3-2-33] *Alt:* Southern Imp; Nanfang Xiaogui. |
| 不点点 | Tiny Tot | Cameo; Allnighter's girlfriend ('my BF'), sells gear for her card. [ARS/3-2-34] *Alt:* Budiandian. |
| 纯蓝守护者 | Pure Blue Guardian | Credits only (wrote the intro, a forum member). |
| 陈泽伟 | Chen Zewei | Named in the 泽伟补命术 description as the outlander who taught it (another cameo). |
| 小师弟 | Junior | ARS 3-2-2: the youngest disciple who fetches the hero in the opening (calls him 师兄). [ARS/3-2-2] *Alt:* Little Brother. |
| 普通弟子 | Disciple | ARS 3-2-3, generic Sanqing disciple. [ARS/3-2-3] |
| 门卫 | Guard | Gate guards of Li Manor (ARS 3-2-4; speaker tags 门卫一/门卫二 = Guard 1/Guard 2). [ARS/3-2-4] |
| 恶斋门卫 | Gate Thug | ARS 3-2-10 (dev label 'evil-house guard'). [ARS/3-2-10] |
| goods商人 | Merchant | ARS 3-2-11 (mixed dev label). [ARS/3-2-11] |
| 药店商人 | Herbalist | ARS 3-2-12, herb shop keeper. [ARS/3-2-12] *Alt:* Herb Seller. |
| 掌柜 | Innkeeper | Speaker tag of innkeepers (Jianye, Whitewater, Fengdu). *Alt:* Shopkeeper. |
| 镇长 | Mayor | Mayor of Whitewater. |
| 守宅人 | Watchman | Men guarding the haunted old manor in Whitewater. |
| 游人 | Passerby | Generic speaker tag (pickpocket gang in Jianye, the crazed father in Whitewater, Fengdu townsfolk). 游人甲/乙 = Passerby A/B. *Alt:* Traveler. |
| 三清游人 | Pilgrim | Visitors on Mt. Sanqing (ARS 3-2-13..18, numbered). *Alt:* Visitor. |
| 路人 | Bystander | Speaker tag in Jianye ('Stop, thief!'). |
| 小偷 | Thief | Speaker tag (Pingzhi before she is unmasked). |
| 少女 | Girl | Speaker tag of the captive painter before she is named. *Alt:* Young Woman. |
| 村民 | Villager | Speaker tag; 村民甲/乙 = Villager A/B. |
| 钟山道士 | Zhong Taoist | Speaker tag, disciples of Zhongshan Abbey. *Alt:* Mt. Zhong Taoist. |
| 皮皮 | Pipi | Only in scene name 皮皮家 (Nanbei Village). |
| 神童 | Prodigy | Only in scene name 神童家 (Fengdu). |

## Titles and forms of address

| zh | en | note |
|---|---|---|
| 柳大哥 | Brother Liu | Xiaomei's (and the little painter's) name for the hero; 大哥 = 'big brother', affectionate, not kin. *Alt:* Big Brother Liu. |
| 柳师兄 | Brother Liu | Zhongshan Taoists to the hero (senior disciple of a sister temple). |
| 袁姐姐 | Sister Yuan | Xiaomei's name for Pingzhi. |
| 袁姑娘 | Miss Yuan | How the hero and Chongxu refer to Pingzhi. |
| 鲁先生 | Mr. Lu | The hero to Lu Fu. |
| 霸爷 | the Boss | Li Hu's guards' name for him ('give the girl to the Boss'). *Alt:* Lord Tyrant. |
| 天师 | Celestial Master | Zhang Daoling's title. In 11-byte compounds shortened to 'Sage' (Sage Charm, Sage Robe, Sage Spirit, Sage's Tomb) - see open decisions. *Alt:* Heavenly Master; Tianshi; Sage. |
| 天道祖师 | Patriarch Tiandao | Ghost King: demons demand the ghosts submit to 'Patriarch Tiandao'. |
| 龙护院 | Drake Guard | Dialogue name of the second North Sea guard (1-13-2). *Alt:* Dragon Guard. |
| 雷爷 | Lord Thunder | Thunderling's boast about himself. |
| 异域人 | Outlander | 'Person from another realm': prefix of the dev-team cameo NPCs in the Fool's Hut (异域人通宵虫 -> 'Outlander Allnighter'). *Alt:* Foreigner; Visitor. |
| 大师兄 | Big Brother | Eldest disciple of Sanqing Hall (ARS 3-2-5, room 大师兄居). [ARS/3-2-5] *Alt:* Eldest Brother. |
| 村长 | Elder | Village head (Murong Xuan of Heartsease). *Alt:* Village Head; Village Chief. |
| 道士 | Taoist | Generic Taoist priest/monk (speaker tag in the epilogue). *Alt:* Daoist. |
| 师父 | Master | The hero to Wuji (and Zhongshan disciples to Chongxu). As in the demo dialogue. *Alt:* Shifu. |
| 师傅 | Master | Variant spelling of 师父 in 1-1-1 and the scene/map name 师傅居; same meaning here. INCONSISTENT spelling in source, same English. |
| 为师 | I (your master) | Wuji referring to himself; render as plain 'I' or 'your master'. |
| 师兄 | Brother | Senior fellow disciple. As in the demo ('Brother, so this is where you are!'). *Alt:* Senior Brother. |
| 师弟 | little brother | Junior fellow disciple (address). *Alt:* Junior Brother. |
| 师叔 | Uncle | Master's fellow disciple (Chongxu). 'Uncle Chongxu'. *Alt:* Martial Uncle; Master-Uncle. |
| 掌门 | Sect Head | Head of the sect. Epilogue: a Taoist addresses the hero as 掌门师兄 - he now leads Sanqing. *Alt:* Sect Leader; Headmaster. |
| 掌门师兄 | Brother Sect Head | Epilogue address to the grown-up hero. *Alt:* Head Brother. |
| 掌教 | head | Tiandao is 'head of the Five Pecks of Rice'. *Alt:* patriarch. |
| 祖师 | Patriarch | Founder/ancestral master (天道祖师). |
| 祖师爷 | granddaddy | Last line of the game: '我是你祖师爷！' - a taunt ('I'm your granddaddy!'), lit. 'your grand patriarch'. *Alt:* Grand Patriarch. |
| 道长 | Master Taoist | Polite address for a Taoist used by villagers to the hero ('Thank you, Master Taoist'). *Alt:* Reverend; Taoist sir. |
| 道人 | Taoist | Suffix in names: 冲虚道人 -> Taoist Chongxu, 无机道人 -> Taoist Wuji. |
| 道爷 | this Taoist | Swagger self-reference ('this Taoist is here to sort you out!'). *Alt:* your Taoist granddad. |
| 真人 | the Perfected | Taoist honorific (玄虚真人). *Alt:* True Man. |
| 星君 | Star Lord | 四象星君 = Star Lord of the Four Symbols (the Red Phoenix's rank). |
| 大侠 | hero | Commoners to the hero ('Thank you, hero!'). *Alt:* good sir; great hero. |
| 恩公 | benefactor | Granny Cai and the Mayor to the party. |
| 姑娘 | Miss | Young woman (address); 'that girl' in narration. *Alt:* young lady. |
| 客官 | sir | Innkeepers to guests. *Alt:* honored guest. |
| 婆婆 | Granny | Old woman (address). |
| 姐姐 | Sister | Older girl (Xiaomei to Pingzhi). |
| 大哥 | Brother | Affectionate 'big brother' (柳大哥). |
| 老夫 | I | Old man's self-reference (Murong Xuan); plain 'I' with an old-fashioned tone. |

## Sects and groups

| zh | en | note |
|---|---|---|
| 三清 | Sanqing | The Three Pure Ones of Taoism; name of the mountain and the hero's temple/sect. Pinyin (real place, Mt. Sanqing in Jiangxi). *Alt:* Three Pure Ones. |
| 五斗米道 | Way of the Five Pecks of Rice | Historical Taoist movement founded by Zhang Daoling at Mt. Heming; Tiandao is its head. *Alt:* Five Pecks Sect; Wudoumi Dao. |
| 茅山 | Maoshan | Taoist exorcist school (Sage Charm description; 矛山 typo in the 天师符法 description). |
| 百花派 | Hundred Flowers Sect | Martial sect in the Hibiscus description. |
| 诡踪堡 | Ghosttrack Fort | Clan in the Night Garb description. |
| 魔族 | demonkind | The demons as a people ('the demonkind keep harassing the ghosts'). *Alt:* demon clan; the Demon Tribe. |
| 鬼族 | ghostkind | The ghosts of Fengdu as a people. *Alt:* ghost clan. |
| 道门 | the Taoist order | Taoism as an institution ('a disgrace to the Taoist order'). |

## Places (map names, scene names, places in dialogue)

| zh | en | note |
|---|---|---|
| 三清宫 | Sanqing Hall | The hero's temple and sect ('I'm a disciple of Wuji of Sanqing Hall'); map/scene name. 'Sanqing Temple/Palace' (14) exceeds the 12-byte map field. [MAP/2-1-1] *Alt:* Sanqing Temple; Sanqing Palace. |
| 魔界 | Demon Realm | Realm of demons (Violet Lamp description). |
| 三界 | Three Realms | Gods, demons, mortals (Tiandao's ambition). |
| 人间 | the mortal world | 'brought down to the mortal world'. *Alt:* the human world. |
| 天界 | Heaven | Heavenly court (Dragonbind description). |
| 三清山 | Mt. Sanqing | The hero's mountain (real place). *Alt:* Sanqing Mountain. |
| 三清山入口 | Sanqing Gate | Foot of the mountain path; map + scene name. [MAP/2-1-20] *Alt:* Mt. Sanqing Entrance. |
| 无机阁 | Wuji Tower | Wuji's hall (map 2-2-7/2-2-8). The demo dialogue uses 'Wuji Pavilion' (13), too long for the 12-byte map field. [MAP/2-2-7; MAP/2-2-8] *Alt:* Wuji Pavilion. |
| 无机洞 | Wuji Cave | Final scene where Wuji is fought (1-1-4/5). |
| 百草地 | Herb Meadow | Where the hero chases butterflies in the opening. [MAP/2-1-2] *Alt:* Hundred Herbs Field. |
| 竹林山道 | Bamboo Path | Mountain path through bamboo. [MAP/2-1-3] *Alt:* Bamboo Mountain Path. |
| 后山浮桥 | Float Bridge | Floating bridge on the back of the mountain. [MAP/2-1-4] *Alt:* Back-Mountain Floating Bridge. |
| 后山 | back mountain | Rear slopes of a mountain (Sanqing; Zhongshan's bell cave). *Alt:* rear hill. |
| 伏魔山道 | Demon Trail | Path to Demon Cave. [MAP/2-1-5] *Alt:* Demonbane Trail. |
| 伏魔洞口 | Cave Mouth | Entrance of Demon Cave. [MAP/2-1-6] *Alt:* Demon Cave Mouth. |
| 伏魔洞 | Demon Cave | Cave on Sanqing's back mountain where demons are sealed and the sword is kept. [MAP/2-3-1] *Alt:* Demonbane Cave (14). |
| 三清坟场 | Hill Graves | Sanqing's graveyard. [MAP/2-1-7] *Alt:* Sanqing Graveyard. |
| 前山步云桥 | Cloudstep | Map name of the front-mountain bridge (same place as scene 步云桥). [MAP/2-1-8] *Alt:* Front-Mountain Cloudstep Bridge. |
| 步云桥 | Cloudstep | Bridge maze on the front of the mountain ('stepping on clouds'). *Alt:* Cloudstep Bridge. |
| 前山 | front mountain | Appears in: map name. |
| 摩天顶 | Sky Summit | Peak with the Four Symbols Godslayer Array. [MAP/2-1-9] *Alt:* Skytop. |
| 观星亭 | Star Gazebo | Pavilion on the bridge maze (locked; needs a Picklock). [MAP/2-1-12] *Alt:* Stargazing Pavilion. |
| 通用横桥 | Bridge H | Generic horizontal bridge map (dev label). [MAP/2-1-10] |
| 通用竖桥 | Bridge V | Generic vertical bridge map (dev label). [MAP/2-1-11] |
| 横桥 | Bridge | Scene name of horizontal bridges (player sees no H/V distinction). |
| 竖桥 | Bridge | Scene name of vertical bridges. |
| 歇息台子 | Rest Ledge | Resting platforms in the bridge mazes (map 2-1-13..19 numbered). *Alt:* Rest Stop. |
| 台子 | Ledge | Platform scenes (Zhongshan, Heming bridge mazes). *Alt:* Platform. |
| 原野阡 | Fields N-S | Wild fields maze, north-south paths (阡). [MAP/2-1-21] *Alt:* Wilds (north road). |
| 原野陌 | Fields E-W | Wild fields maze, east-west paths (陌). [MAP/2-1-22] *Alt:* Wilds (east road). |
| 忘忧村 | Heartsease | Xiaomei's village ('forget-sorrow'); heartsease is a flower named for peace of mind. Add 'village' in prose when needed. [MAP/2-1-23] *Alt:* Wangyou Village; Carefree Village. |
| 忘忧坟场 | Graveyard | Heartsease graveyard, where the Snake Demon's tunnel comes out. [MAP/2-1-32] *Alt:* Heartsease Graveyard. |
| 慕容玄家 | Murong Home | Map name of the elder's house. [MAP/2-1-24] *Alt:* Murong Xuan's House. |
| 村长家 | Elder's House | Scene name (Heartsease; also used for the Whitewater mayor's house - source reuse). |
| 慕容厨房 | Kitchen | Murong kitchen. [MAP/2-2-14] *Alt:* Murong Kitchen. |
| 慕容主房 | Main Room | Murong main room. [MAP/2-2-15] *Alt:* Murong Main Room. |
| 东东家 | Dongdong's House | Appears in: scene name. |
| 老孟家 | Old Meng's House | Appears in: scene name. |
| 疯子家 | Madman's House | Appears in: scene name. |
| 阿霞家 | Ah Xia's House | Appears in: scene name. |
| 蔡婆家 | Granny Cai's House | Appears in: scene name. |
| 野外斜路 | Wild Slope | Map name (diagonal road). [MAP/2-1-25] |
| 转折路口 | Crossroads | Junction maps/scenes (numbered maps 2-1-26..30). |
| 愚人居 | Fool's Hut | Hideout of the dev-team cameos. [MAP/2-1-31] *Alt:* Fools' Lodge. |
| 瘴气林 | Miasma Wood | Poison forest south of Heartsease (needs both Reed Mails). *Alt:* Miasma Forest. |
| 毒瘴林 | Miasma Wood | Same forest (毒瘴林 vs 瘴气林: two names, one place). |
| 毒瘴林入口 | Miasma Gate | Entrance of the Miasma Wood. [MAP/2-1-33] *Alt:* Miasma Wood Entrance. |
| 猎人居 | Hunter's Lodge | Appears in: scene name. |
| 森林道路 | Forest Road | Map 2-1-34/2-1-38 and scenes (森林道路2 = Forest Road 2). [MAP/2-1-34; MAP/2-1-38] |
| 人蛇窟 | Snakeman Den | Lair of the Snake Demon. |
| 人蛇窟入口 | Snake Gate | Entrance of the Snakeman Den. [MAP/2-1-35] *Alt:* Snakeman Den Entrance. |
| 蛇窟 | Snake Den | Appears in: scene name, map name. |
| 蛇窟山洞 | Snake Den | Cave maps 2-3-6..8 (scenes 蛇窟山洞2/3 = Snake Den 2/3). [MAP/2-3-6; MAP/2-3-7; MAP/2-3-8] |
| 蛇窟宝洞 | Den Vault | Treasure cave of the Snake Den. *Alt:* Snake Den Treasure Cave. |
| 蛇窟隐洞 | Hidden Den | Hidden cave of the Snake Den. |
| 石梦城 | Stonedream | Town ruled by Li Hu ('stone dream'). [MAP/2-1-37] *Alt:* Shimeng City. |
| 李府 | Li Manor | Li Hu's mansion (dialogue). |
| 李俯 | Li Manor | Scene names spell it 李俯 (typo for 李府). INCONSISTENT in source, same English. Rooms: 西厢房 West Wing, 客厅 Parlor, 东厢房 East Wing, 密道 Secret Passage, 下人房 Servants' Room, 厨房 Kitchen, 下房 Back Room, 宝库 Vault. |
| 李虎家主房 | Li Hu's Hall | Map name. [MAP/2-2-20] |
| 老王家 | Old Wang's House | Appears in: scene name. |
| 鲁斧家 | Lu Fu's House | Appears in: scene name. |
| 周处庙 | Zhou Shrine | Zhou Chu's shrine in Nanbei Village. [MAP/2-1-36] *Alt:* Zhou Chu Shrine. |
| 建业城 | Jianye | City (historical name of Nanjing). [MAP/2-1-39] *Alt:* Jianye City. |
| 建业客栈 | Jianye Inn | Appears in: scene name, map name. [MAP/2-2-22] |
| 新野客栈 | Xinye Inn | Map 2-2-21; the scene shown is 建业客栈 - leftover dev name, flagged. [MAP/2-2-21] |
| 钟山 | Mt. Zhong | Mountain of Chongxu's abbey, where the Tyrant Bell is kept (real Zhongshan near Nanjing). *Alt:* Zhongshan; Bell Mountain. |
| 钟山入口 | Zhong Gate | Map + scene name. [MAP/2-1-40] *Alt:* Mt. Zhong Entrance. |
| 钟山道院 | Zhong Abbey | Chongxu's abbey. [MAP/2-1-44] *Alt:* Zhongshan Abbey. |
| 参虚阁 | Canxu Tower | Zhongshan's main hall (cf. Wuji Tower). *Alt:* Canxu Pavilion. |
| 冲虚居 | Chongxu's Room | Appears in: scene name. |
| 弟子居 | Dormitory | Disciples' quarters (Zhongshan). |
| 普通弟子居 | Dormitory | Sanqing disciples' quarters (map 2-2-4; scenes 普通弟子居1/2 = Dormitory 1/2). [MAP/2-2-4] |
| 师傅居 | Abbot's Room | Wuji's quarters (map 2-2-1). "Master's Room" is 13 bytes, over the 12-byte map field. [MAP/2-2-1] *Alt:* Master's Room. |
| 大师兄居 | Senior Room | Eldest disciple's room. [MAP/2-2-2] *Alt:* Big Brother's Room. |
| 清风居 | My Room | The hero's own room (rest point). [MAP/2-2-3] *Alt:* Qingfeng's Room. |
| 三清宫厨房 | Kitchen | Appears in: scene name, map name. [MAP/2-2-5] |
| 厨房 | Kitchen | Appears in: scene name, map name. |
| 三清宫药房 | Dispensary | Temple medicine shop. [MAP/2-2-9] *Alt:* Sanqing Dispensary. |
| 药房 | Dispensary | Zhongshan medicine shop. |
| 三清宫丹房 | Elixir Room | Alchemy room (scene). |
| 三清练丹房 | Elixir Room | Map 2-2-6 (练 for 炼 typo). [MAP/2-2-6] |
| 炼丹房 | Elixir Room | Zhongshan alchemy room. |
| 霸王钟洞口 | Bell Cave Mouth | Scene at Zhongshan. |
| 霸王钟洞 | Bell Cave | Cave where the Tyrant Bell is kept. *Alt:* Tyrant Bell Cave. |
| 霸王迷宫 | Bell Maze | Maze before the bell cave. *Alt:* Tyrant Maze. |
| 白水镇 | Whitewater | Town where children disappear. [MAP/2-1-42] *Alt:* Baishui Town. |
| 老宅子 | Old Manor | Haunted house in Whitewater. *Alt:* Old House. |
| 老宅主房 | Manor Hall | Appears in: scene name. |
| 枯井迷宫 | Dry Well Maze | Appears in: scene name. |
| 南北村 | Nanbei Village | Village between South Hill and North Sea (lit. 'South-North'); Zhou Chu's home. *Alt:* Northsouth Village. |
| 酆都城 | Fengdu | The 'ghost city' (real Fengdu, Chongqing). [MAP/2-1-43] *Alt:* Fengdu City. |
| 酆都 | Fengdu | Appears in: dialogue, scene name, map name. |
| 城隍庙 | City God Temple | Where the Ghost King waits, south of Fengdu. |
| 南山 | South Hill | Lair of the White Tiger. *Alt:* Nanshan. |
| 南山入口 | South Hill Gate | Appears in: scene name. |
| 南山迷宫 | South Hill Maze | Appears in: scene name. |
| 南山虎穴 | Tiger's Den | Appears in: scene name. |
| 北海 | North Sea | Lair of the Blue Dragon (whirlpool entrance). [MAP/2-1-45] |
| 北海迷宫 | North Sea Maze | Appears in: scene name. |
| 北海龙潭 | Dragon Pool | Appears in: scene name. |
| 鹤鸣山 | Mt. Heming | Tiandao's mountain (real Heming Shan, birthplace of the Five Pecks of Rice). *Alt:* Crane Cry Mountain. |
| 鹤鸣山入口 | Heming Gate | Map name. [MAP/2-1-41] |
| 鹤鸣山脚 | Heming Foot | Scene name: devastated village at the foot of the mountain. |
| 鹤鸣山洞口 | Heming Cave | Map + scene: cave mouth where Tiandao and the Red Phoenix die. [MAP/2-1-46] *Alt:* Heming Cave Mouth. |
| 鹤鸣山洞 | Heming Cavern | Inside the cave (Dark Turtle). |
| 陵墓迷宫 | Tomb Maze | Appears in: scene name. |
| 天师陵墓 | Sage's Tomb | Tomb of the Celestial Master. [MAP/2-3-11] *Alt:* Tomb of the Celestial Master. |
| 灯洞 | Lamp Cave | Eight lamp caves inside Demon Cave (maps 2-3-2..5, scenes 灯洞1..8). |
| 通用山洞 | Cave | Generic cave map (dev label). [MAP/2-3-9] |
| 通用迷宫 | Maze | Generic maze map (dev label). [MAP/2-3-10] |
| 杂货店 | Goods Shop | General store. [MAP/2-2-16] *Alt:* General Store. |
| 杂货铺 | Goods Shop | Same as 杂货店 (Jianye). |
| 武器店 | Weapon Shop | Appears in: scene name, map name. [MAP/2-2-17] |
| 药店 | Herb Shop | Appears in: scene name, ARS name. |
| 药铺 | Herb Shop | Appears in: scene name, map name. [MAP/2-2-18] |
| 当铺 | Pawnshop | Appears in: scene name, dialogue, map name. [MAP/2-2-19] |
| 客栈 | Inn | Appears in: scene name, dialogue, map name. |
| 小客栈 | Small Inn | Appears in: scene name, map name. [MAP/2-2-26] |
| 客栈客房 | Guest Room | Appears in: scene name. |
| 客栈厨房 | Inn Kitchen | Appears in: scene name. |
| 民宅 | House | Generic houses (scenes 民宅1..5 = House 1..5). |
| 农舍 | Farmhouse | Map names (农舍1..4 numbered). [MAP/2-2-23; MAP/2-2-24] |
| 豪华居 | Mansion | Map name. [MAP/2-2-25] |
| 龙泉 | Longquan | Sword-making town (Longquan sword). |
| 华山 | Mt. Hua | Item description. |
| 太白山 | Mt. Taibai | Item description. |
| 天山 | Tianshan | Item description. |
| 火焰山 | Flaming Mountain | Item description. |
| 瀛洲 | Yingzhou | Isle of immortals (Galeweed). |
| 西域 | the Western Regions | Appears in: item name. |
| 塞北 | the northern frontier | Appears in: item descriptions. |
| 八仙洞 | Eight Immortals Cave | Fairy Stone description. |
| 李俯西厢房 | Li Manor West Wing | Scene name (李俯 = typo for 李府). |
| 李俯客厅 | Li Manor Parlor | Scene name; Li Hu's boss fight. |
| 李俯东厢房 | Li Manor East Wing | Scene name; the painter is held here (Gold Key). |
| 李俯密道 | Li Manor Secret Passage | Scene name. |
| 李俯下人房 | Li Manor Servants' Room | Scene name; Old Wang. |
| 李俯厨房 | Li Manor Kitchen | Scene name. |
| 李俯下房 | Li Manor Back Room | Scene name. |
| 李俯宝库 | Li Manor Vault | Scene name. |
| 皮皮家 | Pipi's House | Scene name (Nanbei Village). |
| 神童家 | Prodigy's House | Scene name (Fengdu). |

## Monsters and bosses (ARS names shown in battle)

| zh | en | note |
|---|---|---|
| 小偷袁 | Thief Yuan | ARS monster record for Pingzhi in her thief fight in Jianye (1-7-14). [ARS/3-3-20] |
| 鲁大憨 | Lu Dahan | ARS monster 3-3-26 ('Big Oaf Lu'); not named in dialogue. [ARS/3-3-26] *Alt:* Lu the Oaf. |
| 天师魂魄 | Sage Spirit | ARS monster 3-3-45 (the tomb fight). Same entity as 天师精魄. [ARS/3-3-45] *Alt:* Celestial Master's Soul. |
| 赤血 | Crimson | The great demon 赤血天魔; fought Wuji 20 years ago, steals the Tyrant Bell at Zhongshan, runs the Soulsnare Array. ARS boss 3-3-18; speaker tag. [ARS/3-3-18] *Alt:* Chixue; Redblood. |
| 真阎罗 | True Yama | ARS monster 3-3-39, the Ghost King's battle name. Dialogue only says 鬼王; consider 'Ghost King' for the battle name too. [ARS/3-3-39] *Alt:* Ghost King; Yama. |
| 白无常 | Bai Wuchang | White Impermanence, underworld escort of souls; fights the party in Fengdu (ARS 3-3-38). [ARS/3-3-38] *Alt:* White Impermanence; White Reaper. |
| 钢叉牛头 | Ox-Head | ARS monster 3-3-37 (steel-fork Ox-Head). [ARS/3-3-37] *Alt:* Fork Ox-Head. |
| 伥鬼 | Tiger Thrall | Ghosts of tiger victims serving the White Tiger (为虎作伥); speaker tag in the South Hill maze. *Alt:* Changgui. |
| 苍龙 | Blue Dragon | Azure Dragon of the East, one of the Four Symbols; revived at North Sea, uses Blood Rain. ARS 3-3-41. 'Azure Dragon' (12) is too long for ARS. [ARS/3-3-41] *Alt:* Azure Dragon. |
| 白虎 | White Tiger | White Tiger of the West, Four Symbols; revived at South Hill, uses the Reek Wind. ARS 3-3-40. [ARS/3-3-40] |
| 朱雀 | Red Phoenix | Vermilion Bird of the South, Four Symbols; Pingzhi's true identity (朱雀（袁萍芷）). ARS 3-3-42. 'Vermilion Bird' (14) too long. [ARS/3-3-42] *Alt:* Vermilion Bird; Zhuque. |
| 玄武 | Dark Turtle | Black Tortoise of the North, Four Symbols; guards the Sage's Tomb on Mt. Heming. ARS 3-3-43. 'Black Tortoise' (14) too long. [ARS/3-3-43] *Alt:* Black Tortoise; Black Turtle (12). |
| 诛仙 | Godslayer | Spirit of the Four Symbols Godslayer Array at Sky Summit ('Who dares enter my Godslayer Array?'). ARS 3-3-46. 诛仙 lit. 'slay immortals'. [ARS/3-3-46] *Alt:* Zhuxian; Immortal Slayer. |
| 蛟护院 | Wyrm Guard | ARS 3-3-35; Blue Dragon calls them 'my Wyrm Guard and Drake Guard'. [ARS/3-3-35] *Alt:* Jiao Guard. |
| 蛇护院 | Drake Guard | ARS 3-3-36. zh says 蛇 'snake', but dialogue calls this guard 龙护院 / 北海龙. INCONSISTENT in source; unified with dialogue (reviewer decision). [ARS/3-3-36] *Alt:* Snake Guard (literal). |
| 小雷公 | Thunderling | Little thunder god who mistakes the party for demons at Zhongshan (ARS 3-3-14). [ARS/3-3-14] *Alt:* Little Thunder. |
| 护剑神 | Swordwarden | Guardian spirit of the Demonbane Sword in Demon Cave; recurring sparring partner (ARS 3-3-11). [ARS/3-3-11] *Alt:* Sword Guardian. |
| 护剑兽 | Swordwarden | Wuji's name for the same guardian in 1-2-2 ('defeat the sword-guarding beast'). INCONSISTENT with 护剑神; unified. *Alt:* Sword Beast. |
| 超护剑神 | Archwarden | Powered-up Swordwarden of the epilogue rematch (ARS 3-3-63). [ARS/3-3-63] *Alt:* Super Swordwarden. |
| 护灯兽 | Lampwarden | Guardian beasts of the eight lamps in the Lamp Caves (ARS 3-3-10; speaker tags 护灯兽一..八 = Lampwarden 1..8). [ARS/3-3-10] *Alt:* Lamp Beast. |
| 蛇妖 | Snake Demon | Half-man half-snake demon terrorizing Heartsease; speaker tag; ARS scene object 3-4-24. [ARS/3-4-24] *Alt:* Snake Fiend. |
| 蛇妖男 | Snake Demon | ARS monster 3-3-5 (battle form of the Snake Demon). Unified with 蛇妖. [ARS/3-3-5] *Alt:* Snake Man. |
| 天道手下 | Henchman | Tiandao's men (ARS 3-2-28..31, numbered). *Alt:* Tiandao's Man. |
| 打手 | Thug | ARS 3-3-6, Li Hu's hired muscle. [ARS/3-3-6] |
| 飞龙腿 | Flying Kick | ARS 3-3-7, kicker thug ('flying dragon legs'). [ARS/3-3-7] *Alt:* Dragon Legs. |
| 无赖飞锤 | Hammer Thug | ARS 3-3-8, rogue with a flying hammer. [ARS/3-3-8] *Alt:* Rogue Hammer. |
| 龟头虫 | Turtle Bug | Turtle-head bug; zh has a crude double meaning (龟头) the dev team surely intended - reviewer may want a cheeky name. [ARS/3-3-1] *Alt:* Turtlehead. |
| 小蜜蜂 | Little Bee | Monster. Appears in: ARS name. [ARS/3-3-2] |
| 风草堆 | Windstack | Wind-blown haystack monster (cf. the White Tiger's haystack disguise). [ARS/3-3-3] *Alt:* Wind Haystack. |
| 酒坛怪 | Jar Fiend | Living wine jar. [ARS/3-3-4] *Alt:* Wine Jar Imp. |
| 蟑螂 | Cockroach | Monster. Appears in: ARS name. [ARS/3-3-12] |
| 小火怪 | Fire Imp | Monster. Appears in: ARS name. [ARS/3-3-13] |
| 小蛇 | Small Snake | Monster. Appears in: ARS name. [ARS/3-3-15] |
| 蝎子 | Scorpion | Monster. Appears in: ARS name. [ARS/3-3-16] |
| 五彩蜘蛛 | Iris Spider | Five-colored spider. 'Rainbow Spider' is 14. [ARS/3-3-17] *Alt:* Rainbow Spider. |
| 公背婆 | Piggyback | Folk figure of an old man carrying an old woman on his back (one costume, two heads). [ARS/3-3-21] *Alt:* Piggyback Pair. |
| 小蜈蚣 | Centipede | Monster. Appears in: ARS name. [ARS/3-3-22] *Alt:* Little Centipede. |
| 僵尸 | Zombie | Chinese hopping corpse. [ARS/3-3-23] *Alt:* Jiangshi. |
| 骷髅兵 | Skeleton | Monster. Appears in: ARS name. [ARS/3-3-24] *Alt:* Bone Soldier. |
| 恶猩猩 | Evil Ape | Monster. Appears in: ARS name. [ARS/3-3-25] |
| 怨妇幻妖 | Banshee | Spirits of the pregnant women buried head-down around the Soulsnare Array; they wail at night. Numbered 1..8 (ARS 3-3-27..34). *Alt:* Grudge Wraith. |
| 高粱酒坛 | Sorghum Jar | Sorghum-liquor jar monster. [ARS/3-3-48] |
| 毒蜘蛛 | Bane Spider | Poison spider (element set: Bane/Bolt/Gale/Fire/Rock/Ice). 'Venom Spider' is 12. [ARS/3-3-49] *Alt:* Venom Spider. |
| 雷蜘蛛 | Bolt Spider | Thunder spider. [ARS/3-3-50] *Alt:* Thunder Spider. |
| 风蜘蛛 | Gale Spider | Wind spider. [ARS/3-3-51] |
| 火蜘蛛 | Fire Spider | Monster. Appears in: ARS name. [ARS/3-3-52] |
| 土蜘蛛 | Rock Spider | Earth spider. [ARS/3-3-53] *Alt:* Earth Spider. |
| 冰蜘蛛 | Ice Spider | Monster. Appears in: ARS name. [ARS/3-3-54] |
| 怪妖坛子 | Demon Jar | Monster. Appears in: ARS name. [ARS/3-3-55] |
| 蝴蝶仙子 | Butterfly | Butterfly fairy (callback to the opening butterfly). [ARS/3-3-56] *Alt:* Butterfly Fairy. |
| 大头怪 | Bighead | Monster. Appears in: ARS name. [ARS/3-3-57] |
| 小可爱 | Cutie | Monster. Appears in: ARS name. [ARS/3-3-58] |
| 恶鱼 | Evil Fish | Monster. Appears in: ARS name. [ARS/3-3-59] |
| 章鱼 | Octopus | Monster. Appears in: ARS name. [ARS/3-3-60] |
| 贝壳 | Seashell | Monster. Appears in: ARS name. [ARS/3-3-61] *Alt:* Clam. |
| 血云雾 | Blood Mist | Monster. Appears in: ARS name. [ARS/3-3-62] |

## Key items and story objects

| zh | en | note |
|---|---|---|
| 无机乾坤剑 | Wuji Sword | Key item GRS 6-14-12 ('a super sword you can't equip - ha!'). SAME sword as ARS 无极乾坤剑: the game spells 无机 (Wuji the master) vs 无极 (the Taoist 'limitless'); both are pinyin Wuji, so English unifies them for free. Full name >11 bytes. [GRS/6-14-12 desc: 你不能装备的超级好剑，气死你。哈哈……] *Alt:* Wuji Cosmos Sword; Wuji Qiankun Sword. |
| 无极乾坤剑 | Wuji Sword | ARS scene object 3-4-8 (the sword in its cave). Alternate spelling of 无机乾坤剑 - flagged inconsistency, same English. [ARS/3-4-8] *Alt:* Wuji Cosmos Sword. |
| 芦藤甲 | Reed Mail | The pair as named in dialogue. *Alt:* Reed-Vine Armor. |
| 霸王钟 | Tyrant Bell | The bell guarded at Zhongshan, stolen by the Crimson Demon for Tiandao; also an accessory (GRS 6-6-15), a monster spell (MRS 4-1-57) and a scene object. [GRS/6-6-15 desc: 魔器之一，极为霸气的法宝。攻击+100、灵力-20、吉运-40。; MRS/4-1-57; ARS/3-4-21] *Alt:* Overlord Bell (13). |
| 蔡婆婆的信 | Cai Letter | Desc: Granny Cai's letter to Lockmaster (unused?). [GRS/6-14-1 desc: 蔡婆婆寄给万锁开的信。] *Alt:* Granny Cai's Letter. |
| 万能钥匙 | Picklock | One-use master key made by Lockmaster. [GRS/6-14-2 desc: 建业城中开锁能手“万锁开”制造的，可打开加锁的宝箱。由于做工问题，使用一次后会毁掉。] *Alt:* Skeleton Key; Master Key. |
| 老孟情书 | Love Letter | Old Meng's letter to Ah Jun. [GRS/6-14-3 desc: 住在忘忧村的老孟写给他在建业打工的男朋友阿军的情书。] |
| 金色钥匙 | Gold Key | Opens Li Manor's east wing. [GRS/6-14-4 desc: 可以打开李虎家东厢房的钥匙。] |
| 虫子卡片 | Bug Card | Allnighter's card. [GRS/6-14-5 desc: 神秘卡片之一，用途不明。] |
| 小鬼卡片 | Imp Card | South Imp's card. [GRS/6-14-6 desc: 神秘卡片之二，用途不明。] |
| 不点卡片 | Tot Card | Tiny Tot's card. [GRS/6-14-7 desc: 神秘卡片之三，用途不明。] |
| 苍龙之精 | Dragon Orb | Essence of the Blue Dragon; one of four used on Sky Summit. [GRS/6-14-8 desc: 四象之一，苍龙的精魄。] *Alt:* Blue Dragon Essence. |
| 白虎之精 | Tiger Orb | Essence of the White Tiger. [GRS/6-14-9 desc: 四象之一，白虎的精魄。] |
| 朱雀之精 | Phoenix Orb | Essence of the Red Phoenix. [GRS/6-14-10 desc: 四象之一，朱雀的精魄。] |
| 玄武之精 | Turtle Orb | Essence of the Dark Turtle. [GRS/6-14-11 desc: 四象之一，玄武的精魄。] |
| 混元金斗 | Chaos Urn | Primordial golden bushel that swallows souls; placed in the Primal Demonbane Array at the end. Also ARS object 3-4-41. [GRS/6-14-13 desc: 可以吸取任何生命体魂魄的仙家至宝。; ARS/3-4-41] *Alt:* Hunyuan Golden Bushel. |

## Weapons

| zh | en | note |
|---|---|---|
| 伏魔剑 | Demonbane Sword | The sword the hero pulls from Demon Cave in chapter 1 (also 伏魔宝剑); pulling it breaks the seal and frees the demons. Probably the same object as ARS 无极乾坤剑 - see open decisions. |
| 伏魔宝剑 | Demonbane Sword | Swordwarden's name for it. |
| 木剑 | Wood Sword | Weapon. Appears in: item name. [GRS/6-7-1 desc: 用木材雕刻的剑，小孩玩具。攻击+2。] |
| 铁剑 | Iron Sword | Weapon. Appears in: item name, item descriptions. [GRS/6-7-2 desc: 一般铁匠大量生产的剑，打造得颇为粗劣。攻击+8。] |
| 长剑 | Long Sword | Weapon. Appears in: item name. [GRS/6-7-3 desc: 一般铁匠接受订造的剑，比铁剑精致锋利。攻击+18，身法-3。] |
| 玄铁剑 | Black Sword | Black (meteoric) iron. [GRS/6-7-4 desc: 用玄铁矿打造的剑，制作工匠的手艺一般，威力也受到了影响。攻击+32、身法-10。] *Alt:* Black Iron Sword. |
| 青锋剑 | Blue Steel | Weapon. Appears in: item name. [GRS/6-7-5 desc: 名家精心打造的剑，轻薄锋利。攻击+45、身法+5。] |
| 龙泉剑 | Longquan | Sword from Longquan. [GRS/6-7-6 desc: 龙泉的水质非常适合造剑，当地生产的剑叫龙泉剑。攻击+66、身法+8。] *Alt:* Longquan Sword. |
| 斩妖剑 | Fiendslayer | Weapon. Appears in: item name. [GRS/6-7-7 desc: 此剑是专门为道士降妖伏魔所打造的兵器，剑刃锋利，有避邪之功效。攻击+72、吉运+10。] |
| 龙吟剑 | Dragonsong | Hums like a dragon when drawn. [GRS/6-7-8 desc: 宝剑出鞘，有龙吟之声，故有“龙吟”之称。攻击+88、灵力+6、防御+4。] |
| 钨龙剑 | Dark Dragon | 钨 'tungsten' probably for 乌 'black'. [GRS/6-7-9 desc: 同样用玄铁打造，但这次的做工就明显好的多了。攻击+108、身法+6。] *Alt:* Tungsten Dragon. |
| 辟魔剑 | Peachwood | Thousand-year peachwood sword that wards off demons. [GRS/6-7-10 desc: 用千年的桃木所制，可避过邪魔妖道施法。攻击+80、身法+5，可能产生混乱3回合。] *Alt:* Demonward Sword. |
| 催眠剑 | Sleep Sword | Weapon. Appears in: item name. [GRS/6-7-11 desc: 可将敌人催眠的剑，打造工匠不详。攻击+100、吉运-3。可能产生5昏睡回合。] |
| 七星剑 | Star Sword | Weapon. Appears in: item name. [GRS/6-7-12 desc: 剑身镶七颗金黄色的宝石，可吸取北斗七星之精气。攻击120灵力15身法12吉运12防御15，可能产生5回合咒封。] *Alt:* Seven Star Sword. |
| 嗜血剑 | Bloodthirst | Weapon. Appears in: item name. [GRS/6-7-13 desc: 屡经战乱，嗜血成性的剑，会吞噬装备者的生命。攻击+250、灵力-40、防御-30、吉运-30，生命上限-50。] |
| 九龙道剑 | Nine Dragon | Zhang Daoling's sword. [GRS/6-7-14 desc: 相传张道陵用此剑诛杀了九条恶龙，龙魂聚在剑上不散而成。可全体攻击，其它属性不详细。] *Alt:* Nine Dragon Sword. |
| 匕首 | Dagger | Weapon. Appears in: item name. [GRS/6-7-15 desc: 携带方便，且可以当水果刀用。削水果的话，效果不错哟。攻击+4。] |
| 砍刀 | Machete | Weapon. Appears in: item name. [GRS/6-7-16 desc: 普通的生铁打造，可用来防身。攻击+10、身法-2。] |
| 佩刀 | Saber | 刀 = saber/blade, 剑 = sword. [GRS/6-7-17 desc: 刀身宽而长，刃部锋利背部厚重。攻击+16、防御+1。] |
| 旋风刀 | Whirlblade | Weapon. Appears in: item name. [GRS/6-7-18 desc: 刀身宽而短，攻击敌人时可旋转。攻击+28、身法+3。] |
| 弯月刀 | Crescent | Weapon. Appears in: item name. [GRS/6-7-19 desc: 一般的刀形状像弯弯的月亮。攻击+49、身法+4、吉运-9。] *Alt:* Crescent Blade. |
| 莲花刀 | Lotus Blade | Weapon. Appears in: item name. [GRS/6-7-20 desc: 以上等的精铁打造，刀尖向上翘，刀背略弯曲。攻击+64、身法+3、灵力+4。] |
| 魔哭刀 | Demonwail | Weapon. Appears in: item name. [GRS/6-7-21 desc: 出鞘之声犹如魔鬼哭泣，令人不寒而栗。攻击+80、防御+10、灵力+3。] |
| 屠魔刀 | Demonslayer | Weapon. Appears in: item name. [GRS/6-7-22 desc: 此刀以六合精英打造，浑厚有力，是所有妖魔的克星。攻击+124、防御+30、身法+5、灵力+6。] |
| 移魂刀 | Soulshift | Weapon. Appears in: item name. [GRS/6-7-23 desc: 神兵就是神兵，绝对的厉害。攻击+124、身法+10，全体攻击。可能产生5回合混乱。] |
| 双手剑 | Twin Swords | Xiaomei's twin swords start here. [GRS/6-7-24 desc: 一尺长的双手剑，适合女子使用。攻击+8、防御+13。] |
| 明目双剑 | Keen Twins | Weapon. Appears in: item name. [GRS/6-7-25 desc: 以中等生铁打造的双剑。攻击+19、防御+17。] |
| 姐妹剑 | Sister Pair | Weapon. Appears in: item name, item descriptions. [GRS/6-7-26 desc: 以上等的精铁铸造而成，此剑为一对，故称[姐妹剑]。攻击+27、防御+20。] *Alt:* Sister Swords. |
| 碧玉双剑 | Jade Twins | Weapon. Appears in: item name. [GRS/6-7-27 desc: 此双剑精巧别致，灵气逼人。攻击+36、身法+4、防御+24。] |
| 芙蓉刀 | Hibiscus | Twin curved sabers of the Hundred Flowers Sect. [GRS/6-7-28 desc: 百花派独门兵器双手弯刀。攻击+48、身法+6、防御+28。] |
| 无影双剑 | Shadowless | Weapon. Appears in: item name. [GRS/6-7-29 desc: 用此剑攻击人时，剑光闪闪使人看不清剑在那里，故称[无影剑]。攻击+60、身法+10、防御+36、吉运+6。] |
| 阴阳双剑 | Yin Yang | Weapon. Appears in: item name. [GRS/6-7-30 desc: 相传是名匠蒲良打造，人间难觅的武器。攻击+85、灵力+10、防御+44、身法+10、吉运+12。] *Alt:* Yin-Yang Twins. |
| 幽真双剑 | Enigma | Origin unknown, 'a riddle'. [GRS/6-7-31 desc: 整个剑就是一个谜，无人知晓它的来历。攻击+125、防御+56、灵力+15、身法+15、吉运+15，真气上限+80。] *Alt:* Mystic Twins. |
| 尺骨双剑 | Bone Twins | 尺骨 = ulna. [GRS/6-7-32 desc: 剑是不怎么样，可它有最大的一个好处――可能产生3回合中毒。攻击+50、防御-10、身法-10。] |

## Armor and accessories

| zh | en | note |
|---|---|---|
| 发带 | Hair Band | Head. Cloth hair tie. [GRS/6-1-1 desc: 绑头发的一根布条。防御+1。] |
| 头巾 | Headscarf | Head. [GRS/6-1-2 desc: 普通人戴的头巾，不但可以防灰，还有保暖作用。防御+2。] |
| 避雨帽 | Rain Hat | Head. Leather rain hat. [GRS/6-1-3 desc: 牛皮制成的帽子，用来防雨防雪。防御+4。] |
| 法帽 | Taoist Hat | Head. Worn by accomplished Taoists. [GRS/6-1-4 desc: 有修为的道士所戴的帽子。防御+11、灵力+3、避咒封。] |
| 将军盔 | Battle Helm | Head. A general's helmet. [GRS/6-1-5 desc: 是立下过赫赫战功的大将，所护头的东西。防御+28、身法+5、灵力+3、吉运+3。] *Alt:* General's Helm. |
| 紫金冠 | Royal Crown | Head. Purple-gold crown, top-tier. [GRS/6-1-6 desc: 此物本应天上有，人间能得几回见，绝对的极品。真气上限+15、攻击-4、防御+20、灵力+12、避乱、避眠。] *Alt:* Purple-Gold Crown. |
| 彩带 | Ribbon | Head. Colored ribbon (girls). [GRS/6-1-7 desc: 彩色的布条，女孩子比较喜欢。防御+2。] |
| 头饰 | Crane Clasp | Head. Silver crane-shaped hair ornament. [GRS/6-1-8 desc: 银制的仙鹤形状发饰。防御+3。] *Alt:* Hair Ornament. |
| 头簪 | Hairpin | Head. [GRS/6-1-9 desc: 头上插的发簪。防御+5。] |
| 天鸡毛 | Dawn Plume | Head. Feather of the heavenly rooster that wakes the sun. [GRS/6-1-10 desc: 每天叫醒太阳的天鸡身上的毛。防御+2  灵力+2  吉运+2。] *Alt:* Sky Rooster Feather. |
| 宝石头簪 | Gem Hairpin | Head. Sapphire hairpin. [GRS/6-1-11 desc: 镶有蓝宝石的头簪。防御+9、吉运+6。] |
| 避邪冠 | Ward Crown | Head. 避邪 'ward off evil' -> Ward. [GRS/6-1-12 desc: 黎族姑娘戴的头冠，据传可护身避邪。防御+10、避乱。] |
| 蓝玉冠 | Azure Crown | Head. Silver crown with blue jade. [GRS/6-1-13 desc: 以白银铸成，外饰以珍贵蓝玉石。防御+18 灵力+6 吉运+4。] *Alt:* Blue Jade Crown. |
| 天蚕丝带 | Silk Band | Head. Heavenly-silkworm silk band. [GRS/6-1-14 desc: 以极珍贵的天蚕丝织成，轻薄柔韧。防御+25、身法+8、避封。] *Alt:* Sky Silk Band. |
| 防毒面罩 | Toxin Mask | Head. Weird-looking anti-poison mask. [GRS/6-1-15 desc: 造型怪异，能防毒的面罩。] *Alt:* Gas Mask. |
| 白衣 | White Robe | Body. [GRS/6-2-1 desc: 粗布缝制的交领长袖白衣。防御+3。] |
| 皮甲 | Hide Armor | Body. Buffalo leather. [GRS/6-2-2 desc: 用水牛皮制做的护甲。防御+7。] |
| 铁锁衣 | Chain Mail | Body. [GRS/6-2-3 desc: 以铁环扣锁制成的护甲。防御+20、身法-3。] |
| 罗汉袍 | Arhat Robe | Body. Fighting monk's robe. [GRS/6-2-4 desc: 有武功、有修为的和尚所穿的衣服。防御+15、吉运+5、灵力+5。] |
| 百练衣 | Snakeskin | Body. Made from 百练 snake skin, resists poison. [GRS/6-2-5 desc: 用百练蛇皮做的衣服，具有防毒的效果。防御+35、避毒。] |
| 天师法衣 | Sage Robe | Body. Zhang Daoling's vestment. [GRS/6-2-6 desc: 张道陵升仙前所穿的法衣。防御+40、灵力+12、避封。] *Alt:* Celestial Master's Vestment. |
| 金缕衣 | Jade Suit | Body. Gold-threaded jade suit (金缕玉衣). [GRS/6-2-7 desc: 以金线穿玉片编制而成，又称[金缕玉衣]。防御+40、吉运+10、身法-10。避乱。] *Alt:* Gold-Thread Jade Suit. |
| 丝衣 | Silk Dress | Body. [GRS/6-2-8 desc: 富贵人家小姐的家常衣服，对穷人就不一样哟！只有过年的时候才能穿上一穿呀！防御+10。] |
| 贵妃衣 | Noble Gown | Body. Imperial consort's gown. [GRS/6-2-9 desc: 是有身份的达官显贵女子所穿的衣服。防御+18、吉运+2。] *Alt:* Consort's Gown. |
| 渺影衣 | Shadowsilk | Body. [GRS/6-2-10 desc: 使用天蚕丝纺成的衣服，轻盈且防御效果不错。防御+24、身法+8。] |
| 火羽衣 | Flame Robe | Body. Red feather robe that looks like fire. [GRS/6-2-11 desc: 红颜色的羽衣，远看像一团火而得名。防御+30，身法+4、避乱。] *Alt:* Fire Feather Robe. |
| 朝圣衣 | Holy Robe | Body. DEF+100. [GRS/6-2-12 desc: 内有护身法宝“如影随行”，该衣具有超高的防御效果。防御+100。] *Alt:* Pilgrim Robe. |
| 鬼针胃 | Barbed Mail | Body. Barbed bronze armor. 胃 'stomach' is a typo for 胄 'armor'; flagged. [GRS/6-2-13 desc: 长满倒刺的铜制盔肌，防御+55，攻击+19。] *Alt:* Ghost Spike Armor. |
| 天蛛丝衣 | Spider Silk | Body. [GRS/6-2-14 desc: 使用蜘蛛神吐的丝织成，轻薄柔韧。防御+40、避毒。] |
| 珍珠衫 | Pearl Shirt | Body. (Description calls it 珍珠衣.) [GRS/6-2-15 desc: 此衣全部饰用上等珍珠穿编而成，故称珍珠衣。防御+60、身法-3、吉运+10。] |
| 避毒衣 | Swan Robe | Body. White swan feathers; resists poison. [GRS/6-2-16 desc: 此衣用白天鹅的羽毛织成，透气保暖亦可避毒。防御+64、身法+6、避毒。] *Alt:* Antitoxin Robe. |
| 诡踪衣 | Night Garb | Body. Black garb of the Ghosttrack Fort. [GRS/6-2-17 desc: 诡踪堡特有的黑色衣服，来无影、去无踪。防御+35、身法+22、吉运-6。] *Alt:* Stealth Garb. |
| 潮海衣 | Tide Robe | Body. Ultimate robe. [GRS/6-2-18 desc: 天蚕抽丝，仙鹤织就，穿上可以不落沉沦、不堕地狱，坐有万佛朝礼、行有七佛随身。是宝物中的宝物呀!] *Alt:* Ocean Robe. |
| 草鞋 | Straw Shoes | Feet. [GRS/6-3-1 desc: 以蔺草编织而成，十分便宜，穿起来很轻便，适宜行走。防御+1。] |
| 布鞋 | Cloth Shoes | Feet. [GRS/6-3-2 desc: 粗布缝制的长统靴。防御+3、身法+1。] |
| 道靴 | Tao Boots | Feet. Taoist boots. [GRS/6-3-3 desc: 道士穿的长靴子。防御+5、身法+2。] *Alt:* Taoist Boots. |
| 长寿靴 | Life Boots | Feet. Longevity boots, max HP+10. [GRS/6-3-4 desc: 王侯将相所穿，精雕细做的靴子。防御+8、身法+6、生命上限+10。] *Alt:* Longevity Boots. |
| 霸王靴 | Steel Boots | Feet. Steel-wire lined. [GRS/6-3-5 desc: 此靴底及靴面内层都加有特铸的金钢丝，可防刀剑。防御+22、身法+5。] *Alt:* Tyrant Boots (12). |
| 追风靴 | Windchasers | Feet. [GRS/6-3-6 desc: 以薄如云雾的蝉纱织成，助穿者疾行如风。防御+10、身法+18。] |
| 花布鞋 | Print Shoes | Feet. Floral cotton shoes. [GRS/6-3-7 desc: 用普通的花纹布所做的鞋子。防御+4、身法+2。] *Alt:* Floral Shoes. |
| 闺秀鞋 | Lady Shoes | Feet. [GRS/6-3-8 desc: 大家闺秀所穿的带有精致花纹的鞋子。防御+8、身法+3。] |
| 鹿皮靴 | Deerskins | Feet. [GRS/6-3-9 desc: 鞋面以麋鹿鹿皮毛缝缝制，质地轻柔，行动可如麋鹿般迅捷。防御+11、身法+5。] |
| 莲花靴 | Lotus Boots | Feet. [GRS/6-3-10 desc: 饰以金莲的长统绣花鞋。防御+10、身法+8。] |
| 夜光靴 | Glow Boots | Feet. Luminous pearl boots. [GRS/6-3-11 desc: 水晶制作而成的，镶嵌夜明珠，晚上不用打灯笼也能看到路。防御+15、身法+12。] |
| 灵狐靴 | Fox Boots | Feet. Spirit-fox fur. [GRS/6-3-12 desc: 用九天灵狐的皮做的鞋子，价格不菲，绝对是值钱的东西。防御+20、身法+16。] |
| 登天泥鞋 | Skyclimbers | Feet. Divine clay shoes. [GRS/6-3-13 desc: 神泥做的鞋子，可以适应不同的脚而成不同的形状。生命上限+20、防御+16、身法+22。] |
| 御风草鞋 | Windriders | Feet. Straw sandals for riding the wind. [GRS/6-3-14 desc: 可以御风而行的草鞋。生命真气上限+20、防御+4、身法+26。] |
| 乾坤游步 | Cosmos Walk | Feet. Tour the world in a day. [GRS/6-3-15 desc: 穿上此鞋可于一日内游遍三山五岳。防御+30、身法+24、灵力+12、吉运+10。] |
| 披风 | Cape | Cape slot (UI 肩披 = Cape). [GRS/6-4-1 desc: 挡风御寒的东西。防御+2。] *Alt:* Cloak. |
| 肩甲 | Pauldrons | Cape. [GRS/6-4-2 desc: 用于护两肩的铠甲。防御+6。] |
| 青铜铠 | Bronze Mail | Cape. [GRS/6-4-3 desc: 防御效果不错的铠甲，只是重量可不轻呀！穿上去一定很笨重。防御+12、身法-7。] |
| 软蛟披风 | Wyrm Cape | Cape. Jiao (wyrm) hide. [GRS/6-4-4 desc: 利用蛟龙的皮制作成的披风，防御效果不错。防御+12。] |
| 铁鳞甲 | Scale Mail | Cape. [GRS/6-4-5 desc: 以鱼鳞形甲片编缀而成的铠甲。防御+18、身法-4。] |
| 金钢肌 | Steel Plate | Cape. 肌 'muscle' likely a typo for 甲; flagged. [GRS/6-4-6 desc: 以稀有的上等金钢铁铸造而成。防御+19。] *Alt:* Vajra Plate. |
| 圣斗甲 | Saint Mail | Cape. Saint Seiya joke (圣斗士). [GRS/6-4-7 desc: 此甲以一张血汗宝马的皮制成。防御+28。] *Alt:* Saint Cloth. |
| 青雷战衣 | Storm Coat | Cape. [GRS/6-4-8 desc: 以十张同兽龄青蛇的皮制成，柔软灵活。防御+32。] *Alt:* Green Thunder Coat. |
| 圣洁披风 | Holy Cape | Cape. [GRS/6-4-9 desc: 以菊黄色的雄鹰的羽毛编织成的。防御+32、灵力+16。] |
| 御灵道袍 | Spirit Robe | Cape. Powerful Taoist's outer robe. [GRS/6-4-10 desc: 法力高强的道士所穿的外袍。防御+31、灵力+16。] |
| 神龙披风 | Dragon Cape | Cape. [GRS/6-4-11 desc: 相传是李天王未登天庭以前穿过的，带有他的神气。防御+66、灵力+15。] |
| 凤纹披风 | Plume Cape | Cape. Phoenix-embroidered; 'Phoenix Cape' is 12. [GRS/6-4-12 desc: 相传为织女缝织的披风，绣凤织锦，光彩夺目。防御+52、灵力+15。] *Alt:* Phoenix Cape. |
| 芦藤雌甲 | Reed Mail F | Cape. Female half of Lu Ban's anti-poison reed armor (worn by Xiaomei; both halves needed for the Miasma Wood). [GRS/6-4-13 desc: 相传为鲁班用云南能避百毒的白芦所造，共有雌雄两件，这件为雌的。防御+3，避毒。] *Alt:* Female Reed Mail. |
| 芦藤雄甲 | Reed Mail M | Cape. Male half (worn by the hero). [GRS/6-4-14 desc: 相传为鲁班用云南能避百毒的白芦所造，共有雌雄两件，这件为雄的。防御+3，避毒。] *Alt:* Male Reed Mail. |
| 布护腕 | Cloth Cuffs | Wrist. [GRS/6-5-1 desc: 衣服袖子上的装饰品，可以起到将人体热气保留在衣服内的效果，能增加保暖功能。防御+2。] |
| 铁护腕 | Iron Cuffs | Wrist. [GRS/6-5-2 desc: 纯铁打造的腕上防具，只是会影响身法。防御+12、身法-3。] |
| 雕龙护腕 | Gold Cuffs | Wrist. Carved-dragon gold cuffs. [GRS/6-5-3 desc: 装饰的不错的金护腕。防御+10。] *Alt:* Dragon Cuffs. |
| 避血手腕 | Blood Cuffs | Wrist. Must not see blood or its demon wakes. [GRS/6-5-4 desc: 不能见到鲜血，不然会激起它的魔性。攻击+10、防御+24、灵力+4。] |
| 赤镯 | Red Bangle | Wrist. [GRS/6-5-5 desc: 红布缝制的护腕。防御+4。] |
| 玉镯 | Jade Bangle | Wrist. [GRS/6-5-6 desc: 普通的玉镯子。防御+10。] |
| 飞天镯 | Sky Bangle | Wrist. [GRS/6-5-7 desc: 用飞天白玉做成的镯子。防御+16、吉运+4。] *Alt:* Apsara Bangle. |
| 吸灵镯 | Soul Bangle | Wrist. Drains MP into AGI/Luck. [GRS/6-5-8 desc: 会吸食佩带者的灵气，转化为身法和吉运的镯子。防御+8、真气上限-10、身法+10、吉运+10。] *Alt:* Leech Bangle. |
| 平安符 | Peace Charm | Accessory. [GRS/6-6-1 desc: 人们经常在神的面前诚心许愿，求一道符用来保护自己小孩的平安，据说只要许愿的人心诚，真会有用！吉运+4。] |
| 香袋 | Sachet | Accessory. [GRS/6-6-2 desc: 填充木屑，香粉的小布包，常用来装饰兼避邪的物品。灵力+4   吉运+2。] |
| 长命锁 | Life Lock | Accessory. Longevity lock. [GRS/6-6-3 desc: 一根红头绳，经过高人开光后就具有了灵性。据说佩带可保长命。防御+3、灵力+3、吉运+3。] |
| 铜镜 | Mirror | Accessory. Bronze mirror. [GRS/6-6-4 desc: 青铜制造的照容用具。防御+6。] *Alt:* Bronze Mirror. |
| 避邪袋 | Ward Pouch | Accessory. [GRS/6-6-5 desc: 用优质的丝绸缝制的小布袋，里面装有艾草、及香料等。防御+6、灵力+3、吉运+5。] |
| 象牙坠 | Ivory Tusk | Accessory. Ivory pendant. [GRS/6-6-6 desc: 用大象的牙做的坠子。防御+12。] *Alt:* Ivory Pendant. |
| 八卦镜 | Bagua Glass | Accessory. Trigram mirror. [GRS/6-6-7 desc: 用朱砂在镜面画八卦，可借用自然界的灵气。灵力+5、防御+5。] *Alt:* Bagua Mirror. |
| 督化笛 | Mercy Flute | Accessory. Flute that converts demons. [GRS/6-6-8 desc: 此笛为九孔笛，笛声悠扬独特，可感化魔妖。吉运+18。] |
| 乾坤镜 | Taiji Glass | Accessory. Mirror with the taiji diagram. [GRS/6-6-9 desc: 铜镜背面铸有太极乾坤图，可吸取天地阴阳之灵气。灵力+9、防御+9。] *Alt:* Cosmos Mirror. |
| 寒冰玉佩 | Frost Jade | Accessory. [GRS/6-6-10 desc: 用寒冰雕刻而成的玉佩，具有很强的灵力。灵力+20。] |
| 定神珠 | Focus Pearl | Accessory. MP regen. [GRS/6-6-11 desc: 具有聚精汇神作用的一颗珠子。每回合恢复真气10。] |
| 富贵珠 | Luck Pearl | Accessory. Luck+99. [GRS/6-6-12 desc: 拥有此珠者便可大富大贵，给人带来福气。吉运+99。] *Alt:* Fortune Pearl. |
| 紫瞳魔灯 | Violet Lamp | Accessory. Demon-realm treasure hidden in Nanbei Village. [GRS/6-6-13 desc: 本为魔界的一大法宝，后在神魔大战时，被不遗落到了人间。攻击防御身法灵力吉运各+15。] *Alt:* Violet-Eye Demon Lamp. |
| 天心灯 | Heaven Lamp | Accessory. Gonggong's lamp; protects against the Chaos Urn on Sky Summit (named in dialogue). [GRS/6-6-14 desc: 上古传下的神器，为共工的护身法宝。每回合恢复生命真气30点，身法+5。] *Alt:* Heart of Heaven Lamp. |
| 玄冰玉如意 | Frost Ruyi | Accessory. [GRS/6-6-16 desc: 用千年的玄冰玉雕刻而成的法宝，每回合恢复真气30点。] *Alt:* Black Ice Jade Ruyi. |
| 七星灯 | Star Lamp | Accessory. Zhuge Liang's seven-star lamp. [GRS/6-6-17 desc: 相传是孔明禳星祈命之灯，每回合可恢复生命30点，只是携带不方便。身法-3。] *Alt:* Seven Star Lamp. |
| 周处除三害 | Three Banes | Accessory: a storybook 'Zhou Chu Rids the Three Banes', Zhou Chu's reward. [GRS/6-6-18 desc: 记载着“周处除三害”故事的一本小说，据说有很玄的作用。防御+2。] *Alt:* Zhou Chu's Tale. |

## Consumables (thrown, healing, boosters)

| zh | en | note |
|---|---|---|
| 梅花镖 | Plum Dart | Thrown. [GRS/6-8-1 desc: 形如梅花的暗器，敌人hp-90。] |
| 雷火珠 | Thunderball | Thrown bomb. [GRS/6-8-2 desc: 充火药的铁珠，投掷撞击后会爆裂伤人。伤敌250。] |
| 天师符 | Sage Charm | Thrown Maoshan charm. [GRS/6-8-3 desc: 茅山道士用来对付妖怪的符咒\x0d\x0a。伤敌150。] *Alt:* Celestial Charm. |
| 袖里剑 | Sleeveblade | Thrown. [GRS/6-8-4 desc: 暗藏在衣袖中的飞剑。伤敌250。] |
| 透骨钉 | Bonepiercer | Thrown. [GRS/6-8-5 desc: 精铁打造、三寸长的铁针是很锋利的暗器。敌人hp-250。] |
| 无影神针 | Unseen Pin | Thrown. [GRS/6-8-6 desc: 细如牛毛，伤人于无形。敌人Hp-400。] *Alt:* Shadowless Needle. |
| 旋魂铊 | Soulspinner | Thrown. [GRS/6-8-7 desc: 此物青光闪闪，旋转极快伤人于无形之中。敌方全体hp-300。] |
| 风灵符 | Wind Charm | Thrown. [GRS/6-8-8 desc: 产生凤系法术的符咒。] |
| 雷灵符 | Bolt Charm | Thrown. 雷 = Bolt in 11-byte names, Thunder elsewhere. [GRS/6-8-9 desc: 产生雷系法术的符咒\x0d\x0a。] *Alt:* Thunder Charm. |
| 水灵符 | Water Charm | Thrown. [GRS/6-8-10 desc: 产生水系法术的符咒。] |
| 土灵符 | Earth Charm | Thrown. [GRS/6-8-11 desc: 产生土系法术的符咒咒。] |
| 火灵符 | Fire Charm | Thrown. [GRS/6-8-12 desc: 产生火系法术的符咒\x0d\x0a。] |
| 青蛇卵 | Snake Egg | Thrown, poison. [GRS/6-8-13 desc: 毒蛇的卵，可能产生2回合毒效果。] |
| 童尸肉 | Corpse Meat | Thrown, poison. [GRS/6-8-14 desc: 童年僵尸身上的肉，可能产生2回合毒效果。] |
| 红蝎卵 | Sting Egg | Thrown, poison (red scorpion egg). [GRS/6-8-15 desc: 毒蝎的卵，可能产生2回合毒效果。] *Alt:* Scorpion Egg. |
| 蜘蛛卵 | Spider Egg | Thrown, poison. [GRS/6-8-16 desc: 毒蜘蛛的卵，可能产生2回合毒效果。] |
| 毒铁菱 | Caltrops | Thrown, poison. [GRS/6-8-17 desc: 带毒的暗器，被伤到者虽不会立即毙命，但若延误医治的话，则必死无疑。伤敌80，可能产生2回合毒效果。] *Alt:* Poison Caltrops. |
| 孔雀胆 | Gall Poison | Thrown. 'Peacock gall', a classic poison. [GRS/6-8-18 desc: 七大毒蛊。可是敌人产生5回合中毒状态。] *Alt:* Peacock Gall. |
| 蝮蛇涎 | Viper Spit | Thrown. [GRS/6-8-19 desc: 蝮蛇的毒涎，可使敌方全体中毒5回合。] |
| 蚀毒砂 | Venom Sand | Thrown. [GRS/6-8-20 desc: 以六毒蚀脏粉配以铁砂。伤害全体敌人150。可能5回合中毒效果。] |
| 迷魂香 | Sleep Smoke | Thrown. [GRS/6-8-21 desc: 点燃蒙汗药散发迷香，可使敌人昏睡五回合。] *Alt:* Knockout Incense. |
| 醍醐香 | Heady Bloom | Thrown, confusion. [GRS/6-8-22 desc: 紫叶小白花，散发浓郁香气，闻到香气便如酒醉一般，混乱5回合。] |
| 缠魂丝 | Soul Silk | Thrown, confusion. [GRS/6-8-23 desc: 千年蜘蛛的毒丝。可使人混乱5回合。] |
| 定魂旗 | Bind Banner | Thrown, silence. [GRS/6-8-24 desc: 将人的魂魄定在体内3回合，不能施展法术。咒封3回合。] |
| 缚龙索 | Dragonbind | Thrown, silence. [GRS/6-8-25 desc: 原本是天界用来捆绑恶龙的绳索，不知被谁偷盗后卖到了人间。咒封5回合。] *Alt:* Dragon Rope. |
| 太极符 | Taiji Charm | Thrown. [GRS/6-8-26 desc: 具有和太极符法相同的作用。伤敌350、咒封3回合。] |
| 忘魂花 | Lethe Bloom | Thrown, sleep. [GRS/6-8-27 desc: 青蓝色小花，散发淡淡香气，闻到香气，便会昏睡三回合，闻到会使人昏睡3回合。] |
| 火毛虫 | Fire Grub | Thrown, sleep. [GRS/6-8-28 desc: 生长在火焰山附近的一种小虫，可以用来攻击敌人。可使敌人昏睡5回合。] |
| 罗喉针 | Rahu Needle | Thrown, drains HP. [GRS/6-8-29 desc: 铁制钢针，尾端系以灵蛊蚕丝，可吸取敌人hp180。] |
| 石矶珠 | Shiji Pearl | Mystery item tied to Nuwa. [GRS/6-8-30 desc: 神秘物品之一，相传和女娲炼石补天有关的一件东西，功用不详。] |
| 止血草 | Bloodwort | HP+50. [GRS/6-9-1 desc: 嚼碎后敷在伤口上，可迅速止血。恢复生命50。] *Alt:* Styptic Herb. |
| 青阴君 | Shadeleaf | HP+150. [GRS/6-9-2 desc: 生长于华山悬崖陡壁之间，对阴阳失调败心火有奇效。hp+150。] *Alt:* Qingyin Herb. |
| 玉蓝草 | Jadegrass | HP+280. [GRS/6-9-3 desc: 生长于沙漠之中、极为罕见的一种植物，可治疗刀伤、剑伤、砸伤等多种外伤。hp+280。] |
| 赤玉断续膏 | Ruby Salve | HP+450 bone-mending salve. [GRS/6-9-4 desc: 颜色赤黄透明如玉、可治疗骨头损伤的一种药。Hp+450。] |
| 观音符 | Mercy Charm | HP+700. 观音 Guanyin, Goddess of Mercy. [GRS/6-9-5 desc: 以观音圣水书写的灵符\x0d\x0a。hp+700。] *Alt:* Guanyin Charm. |
| 行军丹 | March Pill | HP+1000. [GRS/6-9-6 desc: 特制的一种活血顺气的黑色药丸。Hp+1000。] |
| 圣灵符 | Holy Charm | Party HP+300 (Nuwa). [GRS/6-9-7 desc: 具有女娲神强大灵力的符咒。全体hp+300。] |
| 鼠儿果 | Mouse Fruit | MP+36. [GRS/6-9-8 desc: 产于山间野地，多为鼠类所食，经人发现移种平地。Mp+36。] |
| 还神丹 | Spirit Pill | MP+50. [GRS/6-9-9 desc: 提神醒脑、养脑养神的药丸。Mp+50。] |
| 菊花酒 | Mum Wine | MP+110. Chrysanthemum wine. [GRS/6-9-10 desc: 撒点菊花在酒中，保存十年而成。Mp+110。] |
| 魔王甲 | King Beetle | MP+250. 'Demon-king beetle'. [GRS/6-9-11 desc: 周身青黑色，极其难看的一种甲虫，但可增加真气。Mp+250。] *Alt:* Demon Beetle. |
| 蟠果 | Holy Peach | MP+450. From the Queen Mother's peach garden. [GRS/6-9-12 desc: 西王母蟠桃园遗种，籽小肉厚，汁液香甜\x0d\x0a。Mp+450。] |
| 西域奇糯 | Exotic Rice | MP+800. [GRS/6-9-13 desc: 产于西藏的一种糯米。Mp+800。] |
| 紫菁玉蓉膏 | Royal Salve | Full MP. [GRS/6-9-14 desc: 依宫廷秘方，采珍贵药材炼制，是疗伤药的极品。真气补满。] |
| 黑狐甲 | Fox Beetle | Party MP+240. [GRS/6-9-15 desc: 人为饲养的一种小甲虫，非常有灵气。全体Mp+240。] |
| 鸡蛋 | Egg | Consumable. Appears in: item name. [GRS/6-9-16 desc: 便宜而常见的食物。HpMp+10。] |
| 烧肉 | Roast Pork | Consumable. Appears in: item name. [GRS/6-9-17 desc: 以炭火熏烤的酱汁猪肉，可恢复体力。HpMp+45。] |
| 蜂王蜜 | Royal Honey | Consumable. Appears in: item name. [GRS/6-9-18 desc: 蜜蜂所酿最好的蜜，恢复生命150 真气50。] |
| 千里飘 | Farscent | Wine whose scent carries a thousand li. [GRS/6-9-19 desc: 以多种极品鲜果酿制五十年的美酒，打开之后香飘千里。可解毒，HpMp+180。] |
| 冰糖葫芦 | Candy Haws | Tanghulu. [GRS/6-9-20 desc: 以竹签串李子，裹上麦芽糖，形如葫芦，故称糖葫芦。HpMp+400。] |
| 鬼枯藤 | Ghost Vine | Cures poison. [GRS/6-9-21 desc: 具毒性的黑褐色野生藤蔓，可解毒。] |
| 盐巴 | Salt | Consumable. Appears in: item name. [GRS/6-9-22 desc: 取海水煎熬或暴晒而成，用来调味，有时可解毒。] |
| 九节菖蒲 | Calamus | Cures poison. [GRS/6-9-23 desc: 一种水草，叶子狭长如剑，可解毒。] |
| 净衣符 | Pure Charm | Party poison cure. [GRS/6-9-24 desc: 具有祛病、驱邪的法力、可全体解毒。] |
| 雄黄 | Realgar | Consumable. Appears in: item name, item descriptions. [GRS/6-9-25 desc: 天然产的矿物，块状、色黄，，可解毒，hp+350。] |
| 雄黄酒 | Duanwu Wine | Realgar wine, drunk at the Dragon Boat (Duanwu) festival. [GRS/6-9-26 desc: 一点点的雄黄，撒在酒中，习俗在端午节喝这种酒。可解除乱、眠。] *Alt:* Realgar Wine (12). |
| 定心符 | Calm Charm | Cures confusion/silence/sleep. [GRS/6-9-27 desc: 具有安气宁神、增加定力、防止走火入魔之功效。可解乱、封、眠。] |
| 灵山仙芝 | Lingzhi | Revive 15%. [GRS/6-10-1 desc: 寄生于枯木上的菌类，俗称瑞草，具有养气培元之神效。Hp恢复15%。] |
| 赎魂灯 | Ransom Lamp | Revive 30%; bargains with the Wuchang for a soul. [GRS/6-10-2 desc: 用此灯再施以法术可以和黑白无尝交涉，释放已被带走的魂魄。Hp恢复30%。] |
| 孟婆汤 | Mengpo Soup | Revive 50%. [GRS/6-10-3 desc: 服用之后消除死者平生所犯之罪孽，使死者复活hp恢复50%。] |
| 天香续命露 | Heaven Dew | Revive 100%. [GRS/6-10-4 desc: 以八十一种顶级精秘药，用三冥真火炼九九八十一天而成，可引住魂魄，滋养肉体延长寿命Hp恢复100%。] |
| 枸杞仙果 | Goji Berry | Max HP+5. [GRS/6-11-1 desc: 增大生命上限5点。] |
| 八仙石 | Fairy Stone | DEF+2. From the Eight Immortals Cave. [GRS/6-11-2 desc: 八仙洞中仙石，可增强防御2点。] |
| 霸王花 | Cereus | Night-blooming cereus. [GRS/6-11-3 desc: 食用者武术上限+2。] |
| 试炼果 | Trial Fruit | Spirit+3. [GRS/6-11-4 desc: 药王神农氏尝百草时，最早发现的珍药。可提高灵力3点。] |
| 金鍪 | Gold Cap | Rare herb of Mt. Sanqing. [GRS/6-11-5 desc: 三清山上一种名贵的药材，可增强灵力2点。] |
| 无忧仙丹 | Bliss Pill | Max HP/MP+10. Zhou Chu's 无忧丹 in dialogue is the same pill. [GRS/6-11-6 desc: 太上老君的灵丹之一，可提升生命上限10点，真气上限10点。] *Alt:* Carefree Pill. |
| 无忧丹 | Bliss Pill | Dialogue name (1-10-2). |
| 珠仙草 | Pearlweed | Spirit+3. [GRS/6-11-7 desc: 红色叶子，三大仙草之一，提升灵力3点。] |
| 玄冥草 | Netherweed | AGI+3. [GRS/6-11-8 desc: 黑色叶子，三大仙草之二，提升身法3点。] |
| 无妄草 | Fateweed | Luck+3. [GRS/6-11-9 desc: 黄色叶子，三大仙草之三，提升吉运3点。] |
| 佛天圆 | Sarira | Max MP+2. [GRS/6-11-10 desc: 有成就的高僧西归后、遗体火化时结成的形如圆球带有灵性的东西。最大真气值+2。] |
| 天玉菩提 | Bodhi Seed | Max MP+3. [GRS/6-11-11 desc: 天山菩提树的树种籽，八十年才结一次籽。最大真气值+3。] |
| 玉银杏宝 | Ginkgo Nut | Consumable. Appears in: item name. [GRS/6-11-12 desc: 东华上仙居后院的一棵银杏树所结的果子。最大体力值+3。] |
| 罗汉笑 | Arhat Smile | Consumable. Appears in: item name. [GRS/6-11-13 desc: 塞北药王‘笑天下’亲手培育的奇药。灵力最大值+2。] |
| 雪蛤蟆 | Snow Toad | Consumable. Appears in: item name. [GRS/6-11-14 desc: 世间罕见，只生长在太白山寒冰洞的洞底。武术上限+2，防御上限+2。] |
| 金毛虫 | Gold Grub | Consumable. Appears in: item name. [GRS/6-11-15 desc: 浑身通红并付有灵气的一种小甲虫，人服食后可增加真气2。] |
| 生龙活虎丹 | Vigor Pill | Consumable. Appears in: item name. [GRS/6-12-1 desc: 使用后犹如生龙活虎般，增强攻击力。攻击提升1回合。] |
| 龟甲散 | Shell Dust | Consumable. Appears in: item name. [GRS/6-12-2 desc: 使用后如身覆龟甲，刀枪不入。防御提升5回合。] |
| 飘飘香 | Airy Scent | Consumable. Appears in: item name. [GRS/6-12-3 desc: 可以释放出一种特异的香味，使人产生飘飘欲仙的感觉，故又名“欲仙丹”。身法提升4回合。] |
| 战狂石 | Rage Stone | Consumable. Appears in: item name. [GRS/6-12-4 desc: 使用后，使人进入暴劲状态，攻击力增强一倍，持续5回合。] |
| 子金光符 | Glare Charm | Consumable. Appears in: item name. [GRS/6-12-5 desc: 符咒显灵后、金光四射刺眼非凡，使敌人看不清自己。增加防御一倍，持续七回合。] |
| 飓行草 | Galeweed | Consumable. Appears in: item name. [GRS/6-12-6 desc: 在海外的瀛洲仙岛的阴暗处生长一种草，使用后犹如乘飓风而行，身法提升一倍，持续9回合。] |
| 引路石 | Guide Stone | Escapes a maze. [GRS/6-13-1 desc: 当你在迷宫中迷路时，它可一帮你回到起始点。] |

## Magic (MRS names, 19-byte limit)

| zh | en | note |
|---|---|---|
| 御剑术 | Flying Sword | Hero, basic sword control. [MRS/4-1-1 desc: 意念驱剑进行攻击，是剑术的入门功夫。] |
| 剑气术 | Sword Qi | Hero, sword energy on all enemies. [MRS/4-1-2 desc: 由剑身驱出剑气伤人，攻击敌方全体。] *Alt:* Sword Aura. |
| 万剑归一 | All Swords As One | Magic. Appears in: magic name. [MRS/4-1-3 desc: 许多剑从不同的方向刺向一个敌人，威力可想而知。] *Alt:* Myriad Swords. |
| 无双剑咒 | Peerless Sword | Magic. Appears in: magic name. [MRS/4-1-4 desc: 全体攻击的剑咒的一种，比较稀松平常。] |
| 人剑合一 | One With the Sword | Magic. Appears in: magic name, magic descriptions. [MRS/4-1-5 desc: 古来能修炼到人剑合一的又有几人呢？] |
| 破天一剑 | Sky-Rending Sword | The hero's self-made move ('my own kung fu'). [MRS/4-1-6 desc: 自创的武功招式。放出飞剑穿破天空，威力无穷。] |
| 神剑御魔 | Divine Demonward | Derived from 御魔诀. [MRS/4-1-7 desc: 源自御魔诀的超强剑招，几乎可以一剑御魔。] |
| 天师符法 | Sage Charm Art | Maoshan charm attack (desc typo 矛山). [MRS/4-1-8 desc: 矛山道士所创的一种攻击符法，能对妖魔鬼怪进行有效的攻击。] *Alt:* Celestial Charm Art. |
| 太极符法 | Taiji Charm Art | Magic. Appears in: item descriptions, magic name. [MRS/4-1-9 desc: 利用太极的力量形成强力攻击的符咒。可能产生3回合咒封。] |
| 御魔诀 | Demonward Mantra | Magic. Appears in: magic descriptions, magic name. [MRS/4-1-10 desc: 除了它的攻击效果外，还可使敌人产生3回合的混乱状态。] |
| 百虫欺天 | Swarm Over Heaven | Taught by Allnighter. [MRS/4-1-11 desc: 异域人通宵虫最恐怖的招式，吸取全体敌人每人生命300。] *Alt:* Hundred Bugs. |
| 双剑斩 | Twin Sword Slash | Murong twin-sword style. [MRS/4-1-12 desc: 双剑平行齐出，攻击敌人。为慕容家双剑术的起手式。] |
| 傲剑诀 | Proud Sword Mantra | Magic. Appears in: magic name. [MRS/4-1-13 desc: 双剑分前后飞出，攻击敌人。] |
| 剪刀剑气 | Scissor Sword Qi | Magic. Appears in: magic name. [MRS/4-1-14 desc: 双剑交叉飞出，攻击敌人。] |
| 凤舞九天 | Phoenix Dance | Magic. Appears in: magic name. [MRS/4-1-15 desc: 一只凤飞上九天之上，落下凤羽箭攻击全体敌人。] *Alt:* Phoenix Over Nine Heavens. |
| 独孤刀 | Lone Blade | Desc says 孤独刀 (swapped characters). [MRS/4-1-16 desc: 单刀御敌，攻击敌方单人。] |
| 狂刀斩 | Mad Blade Slash | Magic. Appears in: magic name. [MRS/4-1-17 desc: 孤独刀的暴劲招式，攻击单个敌人。] |
| 霸王横刀 | Tyrant Sweep | Magic. Appears in: magic name. [MRS/4-1-18 desc: 大刀一挥，斩妖除魔。攻击全体。] |
| 火旋灯 | Fire Pinwheel | Magic. Appears in: magic name. [MRS/4-1-19 desc: 召唤火灯，旋转攻击单个敌人。] *Alt:* Spinning Fire Lamp. |
| 烈火旋灯 | Blazing Pinwheel | Magic. Appears in: magic name. [MRS/4-1-20 desc: 召唤火灯，旋转攻击全体敌人。] |
| 天火击 | Skyfire Strike | Magic. Appears in: magic name. [MRS/4-1-21 desc: 天降烈火，攻击单个敌人。] |
| 天火烈焰 | Skyfire Blaze | Magic. Appears in: magic name. [MRS/4-1-22 desc: 天降烈火，攻击全体敌人。] |
| 魔域炼火 | Demon Realm Fire | Magic. Appears in: magic name. [MRS/4-1-23 desc: 召唤地下魔域的炼火攻击所有敌人。] |
| 火雷破空 | Fire Thunder Burst | Magic. Appears in: magic name. [MRS/4-1-24 desc: 火系魔法和雷系魔法相结合所形成的魔法，威力无穷。攻击敌方全体。] |
| 炎龙覆天 | Flame Dragon | Magic. Appears in: magic name. [MRS/4-1-25 desc: 召唤天上的炎龙俯冲到地上，攻击全体敌人。] |
| 雷咒 | Thunder Spell | Magic. Appears in: magic name. [MRS/4-1-26] |
| 五雷破空 | Five Thunders Burst | Magic. Appears in: magic name. [MRS/4-1-27] |
| 五雷轰顶 | Five Thunder Crash | Magic. Appears in: magic name. [MRS/4-1-28] |
| 地裂术 | Earth Split | Magic. Appears in: magic name. [MRS/4-1-29] |
| 龟裂天下 | Shatter the World | Magic. Appears in: magic name. [MRS/4-1-30] |
| 风咒 | Wind Spell | Magic. Appears in: magic name. [MRS/4-1-31] |
| 狂风术 | Gale | Magic. Appears in: magic name. [MRS/4-1-32] |
| 飞沙走石 | Sandstorm | Magic. Appears in: magic name. [MRS/4-1-33] |
| 横刀斩 | Sweeping Slash | Magic. Appears in: magic name. [MRS/4-1-34] |
| 气剑指 | Qi Sword Finger | Magic. Appears in: magic name. [MRS/4-1-35] |
| 魔音 | Demon Song | Magic. Appears in: magic name. [MRS/4-1-36] |
| 瘴气 | Miasma | Monster spell, and the poisonous vapor of the Miasma Wood (lowercase 'miasma' in prose). [MRS/4-1-37] |
| 毒吞天下 | World-Eating Venom | Magic. Appears in: magic name. [MRS/4-1-38] |
| 噬灵蛇咒 | Snake Soul Curse | Magic. Appears in: magic name. [MRS/4-1-39] |
| 霸王狮子吼 | Tyrant Lion Roar | Magic. Appears in: magic name. [MRS/4-1-40 desc: 利用吼声降低敌人攻击力和防御力。] |
| 火龙掌 | Fire Dragon Palm | Magic. Appears in: magic name. [MRS/4-1-41] |
| 大火龙掌 | Great Dragon Palm | Magic. Appears in: magic name. [MRS/4-1-42] *Alt:* Great Fire Dragon Palm (20). |
| 五煞齐出 | Five Fiends Strike | Magic. Appears in: magic name. [MRS/4-1-43] |
| 御蜂咒 | Bee Swarm | Magic. Appears in: magic name. [MRS/4-1-44] |
| 御虫咒 | Bug Swarm | Magic. Appears in: magic name. [MRS/4-1-45] |
| 天崩地裂 | Cataclysm | Magic. Appears in: magic name. [MRS/4-1-46] |
| 蚀骨毒咒 | Bone-Rot Curse | Magic. Appears in: magic name. [MRS/4-1-47] |
| 罗煞咒 | Rakshasa Curse | Magic. Appears in: magic name. [MRS/4-1-48] |
| 玄月斩 | Dark Moon Slash | Magic. Appears in: magic name. [MRS/4-1-49] |
| 大玄月斩 | Great Moon Slash | Magic. Appears in: magic name. [MRS/4-1-50] |
| 冰咒 | Ice Spell | Magic. Appears in: magic name. [MRS/4-1-51] |
| 火咒 | Fire Spell | Magic. Appears in: magic name. [MRS/4-1-52] |
| 天女散花 | Petal Rain | Magic. Appears in: magic name. [MRS/4-1-53] *Alt:* Heavenly Maiden's Flowers. |
| 飞岩术 | Flying Rocks | Magic. Appears in: magic name. [MRS/4-1-54] |
| 血魔神功 | Blood Demon Art | Magic. Appears in: magic name. [MRS/4-1-55] |
| 地爪术 | Earth Claw | Magic. Appears in: magic name. [MRS/4-1-56] |
| 幽冥鬼爪 | Nether Ghost Claw | Magic. Appears in: magic name. [MRS/4-1-58] |
| 魔掌天下 | Demon Palm Sweep | Magic. Appears in: magic name. [MRS/4-1-59] |
| 风云变色 | Shifting Storm | Magic. Appears in: magic name. [MRS/4-1-60] |
| 神鬼乱舞 | Spirit Frenzy | Magic. Appears in: magic name. [MRS/4-1-61] |
| 鬼哭神号 | Wailing Spirits | Magic. Appears in: magic name. [MRS/4-1-62] |
| 乌手术 | Black Hand | Poison. [MRS/4-1-63 desc: 一种发毒手法。单体中毒3回合。] |
| 万毒手 | Myriad Poison Hand | Magic. Appears in: magic name. [MRS/4-1-64 desc: 一种可将任合毒药以快、狠、准的身手投向敌人的法术。全体敌人中毒5回合。] |
| 苦口婆心 | Endless Nagging | Confuses (idiom: earnest nagging). [MRS/4-1-65 desc: 造成敌人混乱5回合。] |
| 玄籁之音 | Mystic Echo | Murong family art. [MRS/4-1-66 desc: 慕容家的家传绝学，可使全体敌人混乱3回合。] |
| 五鬼乱神 | Five Ghost Chaos | Magic. Appears in: magic name. [MRS/4-1-67 desc: 魔族的一种邪术，可使人丧失心志5回合。] |
| 笑里藏刀 | Smiling Dagger | Idiom 'a dagger hidden in a smile'. [MRS/4-1-68 desc: 很阴险的招数，让人不知不觉中被咒封，持续4回合。] |
| 八门金锁 | Eight Gate Lock | Magic. Appears in: magic name. [MRS/4-1-69 desc: 运用休、生、伤、杜、景、死、惊、开八门的力量将敌人全体咒封10回合。] |
| 回梦 | Return to Dream | Sleep. [MRS/4-1-70 desc: 将人催眠的魔法，眠4回合。] |
| 九天困乏咒 | Weariness Curse | Magic. Appears in: magic name. [MRS/4-1-71 desc: 可以另全体敌人都进入睡眠状态的魔法，持续2回合。] *Alt:* Nine Heavens Fatigue (20). |
| 御梦心经 | Dream Sutra | Magic. Appears in: magic name. [MRS/4-1-72 desc: 可将人带入梦境中的特殊魔法，单体眠5回合。] |
| 卸劲诀 | Sap Strength | Magic. Appears in: magic name. [MRS/4-1-73 desc: 敌方单人攻击减弱5回合。] |
| 破兵卸劲 | Shatter Arms | Magic. Appears in: magic name. [MRS/4-1-74 desc: 敌方全体攻击减弱3回合。] |
| 血魔噬主 | Blood Demon Bite | Magic. Appears in: magic name. [MRS/4-1-75 desc: 单人防御降低5回合。] |
| 血魔破甲 | Blood Armorbreak | Magic. Appears in: magic name. [MRS/4-1-76 desc: 敌方全体防御降低，持续5回合。] |
| 丹凤解甲 | Phoenix Disarm | Magic. Appears in: magic name. [MRS/4-1-77 desc: 敌方单人防御大幅度降低，持续3回合。] |
| 抽丝剥茧 | Unravel | Magic. Appears in: magic name, magic descriptions. [MRS/4-1-78 desc: 将施展对象的防御像抽丝剥茧似的层层吸去，可极大的降低防御，持续4回合。] |
| 定影神咒 | Shadowbind Spell | Magic. Appears in: magic name. [MRS/4-1-79 desc: 对着敌人的影子念动咒语，可降低他的身法5回合。] |
| 地气锁 | Earth Lock | Magic. Appears in: magic name. [MRS/4-1-80 desc: 利用大地的吸附能力，降低所有敌人的身法，6回合内有效。] |
| 御魔剑诀 | Demonward Sword | Zhang Daoling's sword mantra. [MRS/4-1-81 desc: 张道陵所创的一种攻击剑诀，能对妖魔鬼怪进行有效的攻击。] |
| 金刚咒 | Diamond Spell | Magic. Appears in: magic name. [MRS/4-2-1 desc: 增强防御能力50%，持续5回合。] *Alt:* Vajra Spell. |
| 金钟护身 | Golden Bell | Magic. Appears in: magic name. [MRS/4-2-2 desc: 使用后有如金钟铁罩护身，加倍防御9回合。] |
| 固若金汤 | Iron Bastion | Magic. Appears in: magic name. [MRS/4-2-3 desc: 全体人员5回合内，防御提高一倍。] |
| 望月步 | Moongaze Step | Magic. Appears in: magic name. [MRS/4-2-4 desc: 一种轻盈的战斗步法，可使一个人5回合内，身法提升提升50%。] |
| 御风行 | Wind Walk | Magic. Appears in: magic name. [MRS/4-2-5 desc: 单人身法提升1倍，持续8回合。] |
| 天罡战气 | Heavenly War Qi | Magic. Appears in: magic name. [MRS/4-2-6 desc: 被施展者普通攻击效果上升7回合。] |
| 六祖战经 | Six Patriarch Sutra | Magic. Appears in: magic name. [MRS/4-2-7 desc: 我方全体人员，5回合内普通攻击威力加倍。] |
| 气疗术 | Qi Heal | Magic. Appears in: magic name. [MRS/4-3-1 desc: 修道之人疗伤的基本法术，恢复生命75。] |
| 归心术 | Mind Restore | Magic. Appears in: magic name. [MRS/4-3-2 desc: 中级疗伤法术，单人恢复生命400。] |
| 老子回天术 | Laozi's Revival | Magic. Appears in: magic name. [MRS/4-3-3 desc: 太上老君秘传的恢复法术，我方单人恢复生命1000。] |
| 观音咒 | Mercy Spell | Xiaomei's basic heal. [MRS/4-3-4 desc: 初级疗伤心法，单人恢复生命150。] *Alt:* Guanyin Mantra. |
| 凝神归元 | Restore Essence | Magic. Appears in: magic name. [MRS/4-3-5 desc: 中级疗伤心法，单人恢复生命220。] |
| 元灵归心术 | Spirit Return | Magic. Appears in: magic name. [MRS/4-3-6 desc: 高级疗伤心法，单人恢复生命560。] |
| 五朝元气 | Fivefold Qi | Magic. Appears in: magic name. [MRS/4-3-7 desc: 特殊疗伤心法，全体恢复生命360。] |
| 泽伟补命术 | Zewei's Life Mend | Named after cameo Chen Zewei; taught by South Imp. [MRS/4-3-8 desc: 异域人陈泽伟传授的强力恢复魔法，而且耗费真气极少。全体恢复生命1000。解除毒、乱、封、眠] |
| 百火练金术 | Hundred Fire Forge | Magic. Appears in: magic name. [MRS/4-3-9 desc: 我方单人恢复生命900的强力法术。] |
| 凝神诀 | Focus Mantra | Magic. Appears in: magic name. [MRS/4-3-10 desc: 三清心法的一种，使人处于明镜状态。解除乱、眠状态。] |
| 净衣咒 | Purify Spell | Magic. Appears in: magic name. [MRS/4-3-11 desc: 净化身体的元气，解除中毒状态。] |
| 冰心决 | Icy Heart Mantra | 决 for 诀 (typo). [MRS/4-3-12 desc: 可解除混乱状态的一种咒语。] |
| 华佗化封诀 | Hua Tuo's Unseal | Magic. Appears in: magic name. [MRS/4-3-13 desc: 根据华佗的身体穴位图，催动真气念真言，单体解除封招的咒语。] |
| 马师皇针灸 | Ma Shihuang Needles | Magic. Appears in: magic name. [MRS/4-3-14 desc: 神医马师皇传下来的一种针灸方法，能令人解除疲乏，恢复精神。单体解除眠状态。] *Alt:* Acupuncture. |
| 五禽戏咒 | Five Animals Spell | Magic. Appears in: magic name. [MRS/4-3-15 desc: 华佗创造的五禽戏，经历代名医道士的演习所形成具有相同作用的咒语，可解除毒乱封眠。] |
| 还魂咒 | Revive Spell | Magic. Appears in: magic name. [MRS/4-4-1 desc: 使脱离人体的魂魄回归本身的咒语。起死回生，恢复15%的生命。] |
| 唤灵术 | Soul Call | Magic. Appears in: magic name. [MRS/4-4-2 desc: 寻找脱离本位的魂魄，使其回归原位。起死回生，恢复30%的生命。] |
| 赎魂 | Soul Ransom | Magic. Appears in: item name, magic name. [MRS/4-4-3 desc: 从鬼差手中讨回被索取的魂魄。起死回生，恢复50%的生命。] |

## Skills and named arts

| zh | en | note |
|---|---|---|
| 魔功 | demonic arts | Evil cultivation (Wuji, White Tiger, Red Phoenix). |
| 万魔幻化 | Myriad Demon Metamorphosis | Wuji's forbidden art; at level 10 it turns anything into undying demons. *Alt:* Ten-Thousand Demon Transformation. |
| 摄魂术 | Soulsnare | The Crimson Demon's soul-draining art. *Alt:* Soul-Snaring Art. |
| 腥风魔功 | Reek Wind art | White Tiger's art. |
| 妙手空空 | Deft Hands | Name Pingzhi gives the steal skill when she teaches it (1-14-8); the magic record is 飞龙探云手. INCONSISTENT names in source; reviewer: use 'Dragon Cloud Grab' in the line? *Alt:* Light Fingers. |
| 飞龙探云手 | Dragon Cloud Grab | Steal skill taught by Pingzhi as 妙手空空 (MRS 4-5-1; a nod to Chinese Paladin). [MRS/4-5-1 desc: 偷取敌人身上的物品。] *Alt:* Flying Dragon Cloud Hand. |

## Story terms, scene objects, other

| zh | en | note |
|---|---|---|
| 小画家被绑 | Bound Girl | ARS scene object: the painter tied up in Li Manor (not displayed). [ARS/3-4-22] *Alt:* Painter (tied). |
| 天师尸体 | Sage Corpse | ARS scene object (not displayed). [ARS/3-4-36] |
| 天道Npc | Tiandao NPC | ARS NPC sprite for Tiandao in cut-scenes (dev label). [ARS/3-4-31] |
| 赤血Npc | Crimson NPC | ARS NPC sprite for the Crimson Demon (dev label). [ARS/3-2-27] |
| 朱雀现身 | Phoenix | ARS scene object: Pingzhi revealing her Red Phoenix form (not displayed). [ARS/3-4-42] *Alt:* Phoenix Form. |
| 步步高 | BBK | Manufacturer (credits: 步步高游戏组 = BBK Game Team). |
| 伏魔记 | Demonbane Chronicle | Game title (not in the string table; for the title screen/readme). Reviewer decision. *Alt:* Record of Demon Quelling; Fu Mo Ji. |
| 伏魔 | Demonbane | 'Subduing demons'; in Demon Cave, the Demonbane Sword, the Primal Demonbane Array. Place compounds use the shorter 'Demon' to fit 12-byte map names (Demon Cave, Demon Trail). *Alt:* demon-quelling; demon-subduing. |
| 道 | the Way | Philosophical sense (道魔不两立 'the Way and the demonic cannot coexist'; 道非道，魔非魔 echoes the Tao Te Ching). Count is inflated by compounds (知道, 道长...). [ARS/3-4-35] *Alt:* Tao; the Dao. |
| 魔 | demon | Demon/demonic; opposite of 道 in the intro. Count inflated by compounds. *Alt:* devil. |
| 妖 | fiend | Monster spirit; kept distinct from 魔 'demon' where it matters (Fiendslayer vs Demonslayer). *Alt:* yao; monster. |
| 妖魔 | demons | Generic 'demons and monsters' (18x). *Alt:* fiends and demons. |
| 妖怪 | monster | Generic creature/monster (14x). *Alt:* fiend. |
| 魔头 | archfiend | Great villain ('the real archfiend is Wuji'). *Alt:* demon lord. |
| 心魔 | inner demon | Wuji's corruption ('my inner demon has been dispelled'). |
| 魔道 | the demonic path | 'fallen to the demonic path'. |
| 江湖 | the martial world | Opening scroll ('anyone in the martial world with ears...'). *Alt:* jianghu. |
| 除魔卫道 | slay demons and defend the Way | The hero's duty, said by Wuji, Lu Fu and the hero. |
| 替天行道 | do Heaven's justice | Battle cry vs Li Hu and Tiandao. Also spelled out by four ARS scene objects named 替 / 天 / 行 / 道 (3-4-32..35, a banner in Tiandao's lair; not displayed) - give those 'Banner 1/4'..'Banner 4/4' if a name is needed; they are left out as single-character terms. *Alt:* act on Heaven's behalf. |
| 先天伏魔阵 | Primal Demonbane Array | The ancient array in Demon Cave that holds the sealed demons; the Chaos Urn placed at its center ends the game. *Alt:* Primordial Demon-Subduing Formation. |
| 阵 | Array | Magic formation (Soulsnare Array, Godslayer Array). *Alt:* Formation. |
| 四象 | Four Symbols | Blue Dragon, White Tiger, Red Phoenix, Dark Turtle. *Alt:* Four Images. |
| 四象诛仙阵 | Four Symbols Godslayer Array | Array on Sky Summit built by the Red Phoenix for Wuji; broken by returning the four Orbs. |
| 诛仙阵 | Godslayer Array | Short form. |
| 摄魂阵 | Soulsnare Array | The Crimson Demon's array under the old manor in Whitewater; also a scene name. |
| 七大邪阵 | Seven Evil Arrays | Pingzhi's lore. |
| 腥风 | reek wind | White Tiger's foul wind. |
| 醒风 | reek wind | Typo for 腥风 in 1-10-x ('白虎醒风'). INCONSISTENT spelling in source, same English. |
| 血雨 | Blood Rain | Blue Dragon's blight (血雨大法 = Blood Rain technique). |
| 神魔大战 | War of Gods and Demons | Ancient war (Violet Lamp lore). |
| 魂魄 | soul | Souls drawn into the Chaos Urn, etc. |
| 妖气 | evil aura | 'a strong evil aura around Miss Yuan'. *Alt:* demonic aura. |
| 正气 | righteousness | Opposite of 妖气. |
| 法宝 | treasure | Magic artifact. *Alt:* magic treasure. |
| 符 | Charm | Taoist paper talisman; 'Charm' in item names to fit 11 bytes (Sage Charm, Wind Charm...). *Alt:* Talisman. |
| 符咒 | charm | In descriptions. *Alt:* talisman. |
| 咒 | Spell | In magic names (雷咒 Thunder Spell); 'Curse' for evil ones (蚀骨毒咒 Bone-Rot Curse). *Alt:* Mantra; Incantation. |
| 诀 | Mantra | Technique formula in magic names (御魔诀 Demonward Mantra). *Alt:* Verse; Secret. |
| 功夫 | kung fu | The hero's word for his self-made moves. *Alt:* martial arts. |
| 武功 | martial arts | Appears in: dialogue, item descriptions, magic descriptions. |
| 比武大会 | tournament | Wuji: 'you came second-to-last in the tournament'. |
| 三清宫门左 | Hall Gate L | Scene object (dev label). [ARS/3-4-1] |
| 三清宫门中 | Hall Gate M | Scene object. [ARS/3-4-2] |
| 三清宫门右 | Hall Gate R | Scene object. [ARS/3-4-3] |
| 横向栏杆 | Railing | Scene object. [ARS/3-4-4] |
| 树1 | Tree 1 | Scene object. [ARS/3-4-5] |
| 机关门 | Puzzle Door | Mechanism door guarding the sword ('open the mechanism door'). [ARS/3-4-6] *Alt:* Trick Door. |
| 伏魔灯 | Demon Lamp | The eight lamps of the Lamp Caves (scene object). [ARS/3-4-7] *Alt:* Demonbane Lamp. |
| 宝箱1 | Chest 1 | Scene object. [ARS/3-4-9] |
| 挡路石 | Boulder | Scene object. [ARS/3-4-10] |
| 迷宫楼梯 | Maze Stairs | Scene object. [ARS/3-4-11] |
| 云彩 | Cloud | Scene object. [ARS/3-4-12] |
| 山洞隐层 | Cave Cover | Scene object (hidden cave overlay). [ARS/3-4-13] |
| 传送点 | Warp Point | Scene object. [ARS/3-4-14] |
| 大箱子 | Big Chest | Scene object. [ARS/3-4-15] |
| 玉马 | Jade Horse | Scene object. [ARS/3-4-16] |
| 文物 | Antique | Scene object. [ARS/3-4-17] |
| 透明宝箱 | Ghost Chest | Invisible chest (scene object). [ARS/3-4-18] *Alt:* Hidden Chest. |
| 房门 | Door | Scene object. [ARS/3-4-19] |
| 商店招牌 | Shop Sign | Scene object. [ARS/3-4-20] |
| 无头尸体 | Headless | Headless body (scene object). [ARS/3-4-23] *Alt:* Headless Body. |
| 烟雾左 | Smoke L | Scene object. [ARS/3-4-25] |
| 烟雾右 | Smoke R | Scene object. [ARS/3-4-26] |
| 旋涡 | Whirlpool | Scene object (entrance to the North Sea). [ARS/3-4-27] |
| 蛟对象 | Wyrm | Scene object of the North Sea Wyrm. [ARS/3-4-28] |
| 小狗 | Puppy | The North Sea Drake in disguise ('what a cute puppy!'). [ARS/3-4-29] |
| 草堆 | Haystack | The White Tiger disguised as haystacks. [ARS/3-4-30] |
| 盘龙柱 | Dragon Post | Coiled-dragon pillar (scene object). [ARS/3-4-40] *Alt:* Coiled Dragon Pillar. |
| 百虫秘籍 | Bug Manual | Scene object; cf. magic 百虫欺天 taught by Allnighter. [ARS/3-4-43] *Alt:* Hundred Bugs Manual. |
| 小孩僵尸 | Ghoul Kid | Child zombies (ARS scene objects 3-4-37..39, numbered). *Alt:* Zombie Kid. |
| 天鸡 | Sky Rooster | Appears in: item name, item descriptions. |

## UI, stats, status effects, choices

| zh | en | note |
|---|---|---|
| 告示 | Notice | Sign text prefix ('告示：三清山' -> 'Notice: Mt. Sanqing'). |
| 生命 | HP | Stat (engine label + item descriptions). *Alt:* Life. |
| 真气 | MP | Stat. *Alt:* Qi. |
| 攻击 | Attack | Stat in descriptions (engine label 攻击力 = Attack). Abbreviate ATK only if a description overflows 102 bytes. *Alt:* ATK. |
| 防御 | Defense | Stat in descriptions (label 防御力 = Defense). EXCEPTION: the battle command slot ENG/1f8aa.2 (same zh) is the action 'Guard' (engine_demo) - deliberate context split. *Alt:* DEF; Guard (battle command). |
| 身法 | Agility | Stat (engine label and descriptions). *Alt:* AGI (tight descriptions); Speed. |
| 灵力 | Spirit | Stat (engine label and descriptions); magic power. *Alt:* SPI (tight descriptions). |
| 吉运 | Luck | Luck in item descriptions (the engine status label says 幸运, also Luck). *Alt:* LCK. |
| 武术 | Attack | Only in 霸王花/雪蛤蟆 descriptions ('武术上限'); apparently = attack. *Alt:* Martial. |
| 体力 | HP | Stamina = HP ('休息片刻 体力恢复' -> 'You rest. HP restored.'). |
| 回合 | turns | Battle rounds in descriptions ('3 turns'). *Alt:* rounds. |
| 上限 | max | '生命上限+10' -> 'Max HP+10'. |
| 中毒 | Poison | Status (engine short 毒 = Psn). |
| 混乱 | Confuse | Status (engine short 乱 = Cnf). *Alt:* Confusion. |
| 咒封 | Silence | Status: cannot cast (engine short 封 = Sil). *Alt:* Seal. |
| 昏睡 | Sleep | Status (engine short 眠 = Slp). |
| 避毒 | resist Poison | Equipment immunity (also 避乱/避封/避眠/避咒封). *Alt:* Immune: Psn. |
| 加入队列 | joins the party | System message 'X加入队列' (e.g. 'Murong Xiaomei joins the party'). |
| 没有钥匙 | You have no key. | Message. |
| 没此物品 | You don't have it. | Message (also 无此物品). |
| 取消 | Cancel | Choice option. |
| 使用钥匙 | Use Key | Choice option (Li Manor). |
| 使用万能钥匙 | Use Picklock | Choice option (<=19 bytes). |
| 免战 | Truce | Choice vs Swordwarden in the epilogue. *Alt:* Decline. |
| 欠扁 | Bring it on | Choice: lit. 'asking for a beating'. *Alt:* Fight. |
| 不给 | Refuse | Choice. *Alt:* Keep it. |
| 奉还 | Give back | Choice. |
| 交出 | Hand over | Choice. |
| 不换 | No deal | Choice. |
| 交换 | Trade | Choice. |
| 放走 | Let go | Choice (Old Wang). |
| 杀死 | Kill | Choice (Old Wang). |
| 允许存盘 | SaveOK | Script menu 1-0-6 (debug?): allow saving. <=6 chars. *Alt:* Allow saving. |
| 禁止存盘 | NoSave | Script menu 1-0-6: disallow saving. *Alt:* Disallow saving. |
| 使用苍龙之精 | Use Dragon Orb | Choice on Sky Summit (<=19 bytes). |
| 使用白虎之精 | Use Tiger Orb | Choice on Sky Summit. |
| 使用朱雀之精 | Use Phoenix Orb | Choice on Sky Summit. |
| 使用玄武之精 | Use Turtle Orb | Choice on Sky Summit. |
| 空档案 | Empty | Empty save slot. Engine string (ENG/0247e). |
| 错误指令... | Bad command... | Engine error message. Engine string (ENG/07b6f). |
| 已满载！ | Inventory full! | Inventory/shop: bag is full. Engine string (ENG/07b7b, ENG/3b469). |
| 获得: | Got:  | Chest pickup prefix: 'Got: <item>'. Engine string (ENG/07b84). |
| 档案储存中…  | Saving...  | Shown while saving. Engine string (ENG/0f615). |
| 耗真气: | MP cost: | Magic menu: MP cost. Engine string (ENG/137c6). |
| 等级 | Lv | Status label: level. Engine string (ENG/13818). |
| 攻击力 | Attack | Status label. Engine string (ENG/13827). |
| 防御力 | Defense | Status label. Engine string (ENG/1382e). |
| 经验值 | EXP | Status label. Engine string (ENG/13835). |
| 幸运 | Luck | Status label (descriptions say 吉运; both Luck). Engine string (ENG/13846). |
| 免疫 | Immune | Status page 2: immunities. Engine string (ENG/1384b). |
| 毒 | Psn | Status abbreviation: Poison (中毒). Engine string (ENG/13858). |
| 乱 | Cnf | Status abbreviation: Confuse (混乱). Engine string (ENG/1385b). |
| 封 | Sil | Status abbreviation: Silence (咒封, cannot cast). Engine string (ENG/1385e). |
| 眠 | Slp | Status abbreviation: Sleep (昏睡). Engine string (ENG/13861). |
| 无 | - | 'None' in the immunity row. Engine string (ENG/13864). |
| 属性 | Stats | Main map menu (EXIT key). Engine string (ENG/13891.0), packed menu slot 32 px. |
| 魔法 | Magic | Main map menu. Engine string (ENG/13891.1), packed menu slot 32 px. |
| 物品 | Items | Main map menu. Engine string (ENG/13891.2), packed menu slot 32 px. |
| 系统 | Game | Main map menu: save/load/options/quit. Engine string (ENG/13891.3), packed menu slot 32 px. |
| 状态 | Status | Submenu of 属性 and battle wheel item. Engine string (ENG/138a3.0, ENG/1f8aa.4), packed menu slot 32 px. |
| 穿戴 | Gear | Submenu of 属性: equipment screen. Engine string (ENG/138a3.1), packed menu slot 32 px. |
| 使用 | Use | Item submenu / battle 道具 submenu. Engine string (ENG/138ad.0, ENG/1f8e4.2), packed menu slot 32 px. |
| 装备 | Equip | Item submenu / battle 道具 submenu. Engine string (ENG/138ad.1, ENG/1f8e4.0), packed menu slot 32 px. |
| 读入进度 | Load | System menu. Engine string (ENG/138b7.0), packed menu slot 64 px. |
| 存储进度 | Save | System menu. Engine string (ENG/138b7.1), packed menu slot 64 px. |
| 游戏设置 | Setup | System menu. Engine string (ENG/138b7.2), packed menu slot 64 px. Shortened from the engine_demo draft to meet the 6-character menu-label rule. *Alt:* Options (engine_demo; 7 chars). |
| 结束游戏 | Quit | System menu. Engine string (ENG/138b7.3), packed menu slot 64 px. |
| 音乐开 | Music | Options toggle: music on. Engine string (ENG/138d9.0), packed menu slot 48 px. Shortened from the engine_demo draft to meet the 6-character menu-label rule. *Alt:* Music On (engine_demo; 8 chars, fits 48 px). |
| 音乐关 | Mute | Options toggle: music off. Engine string (ENG/138d9.1), packed menu slot 48 px. Shortened from the engine_demo draft to meet the 6-character menu-label rule. *Alt:* Music Off (engine_demo; 9 chars, fits 48 px). |
| 金钱： | Money: | Money label (menu, shops). Engine string (ENG/138e7, ENG/37931, ENG/3b457). |
| 目前不能存档! | Can't save now! | Save disabled by script. Engine string (ENG/13912). |
| 真气不足! | Not enough MP! | Battle: not enough MP. Engine string (ENG/1f8a0). |
| 围攻 | Rush | Battle wheel (DOWN menu): auto/all-out attack. 'Rush' kept from engine_demo; confirm behavior. Engine string (ENG/1f8aa.0), packed menu slot 32 px. |
| 道具 | Item | Battle wheel: items. Engine string (ENG/1f8aa.1), packed menu slot 32 px. |
| 逃跑 | Flee | Battle wheel. Engine string (ENG/1f8aa.3), packed menu slot 32 px. |
| 投掷 | Throw | Battle 道具 submenu: throw an item. Engine string (ENG/1f8e4.1), packed menu slot 32 px. |
| 获得经验 | EXP | Battle result: 'EXP <n>'. Engine string (ENG/2facd). |
| 战斗获得  | Earned  | Battle result: 'Earned <n> (money)'. Engine string (ENG/2fad6). |
| 得到  | Got  | Battle result: 'Got <item> xN'. Engine string (ENG/2fae3). |
| 修行提升 | Level up! | Level-up popup '<name> Level up!'. Engine string (ENG/2faec). |
| 偷得  | Stole  | Steal result. Engine string (ENG/2fb65). |
| 装饰 | Acc. | Equip slot: accessory. Engine string (ENG/3398b, ENG/33990). |
| 护腕 | Wrist | Equip slot: wrist. Engine string (ENG/33995). |
| 脚蹬 | Feet | Equip slot: feet. Engine string (ENG/3399a). |
| 手持 | Hand | Equip slot: weapon. Engine string (ENG/3399f). |
| 身穿 | Body | Equip slot: body. Engine string (ENG/339a4). |
| 肩披 | Cape | Equip slot: cape. Engine string (ENG/339a9). |
| 头戴 | Head | Equip slot: head. Engine string (ENG/339ae). |
| 不能装备！ | Can't equip! | Equip error. Engine string (ENG/339f3, ENG/3789f). |
| 已装备！ | Equipped! | Already equipped. Engine string (ENG/378c6). |
| 战斗中才能使用！ | Only in battle! | Item use error. Engine string (ENG/378cf). |
| 无效！ | No effect! | Item/magic had no effect. Engine string (ENG/378e0). |
| 真气不足！ | Not enough MP! | Map: not enough MP. Engine string (ENG/378ff). |
| 此处无法使用！ | Can't use that here! | Item use error. Engine string (ENG/3790a). |
| 卖出个数  ： | Sell how many: | Shop sell quantity. Engine string (ENG/3793a). |
| 买入个数  ： | Buy how many: | Shop buy quantity. Engine string (ENG/37947). |
| 金钱不足！ | Not enough money! | Shop: not enough money. Engine string (ENG/3795c, ENG/3b45e). |
| 没携带物品！ | No items! | Shop sell: no items. Engine string (ENG/3796f). |
| 不可卖物品！ | Can't sell that! | Shop sell: key item. Engine string (ENG/3797c). |
| 数量： | Qty: | Shop/item list column. Engine string (ENG/3b446). |
| 价： | Price: | Shop list column. Engine string (ENG/3b44d). |
| 名： | Name: | Shop list column. Engine string (ENG/3b452). |
