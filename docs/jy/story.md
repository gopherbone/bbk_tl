# 金庸群侠传 (Heroes of Jin Yong) - story notes for translators

A BBK hobby game by "BOSS Studio" (the end credits apologise that the author was busy with the gaokao). It runs
on the same engine and template as 伏魔记, so some fmj ARS names survive as unused leftovers. Not a linear RPG:
it is a small open world of four cities, eleven sects and a dozen wild areas, with one short main quest built
from *The Legend of the Condor Heroes*, one long sect quest line for Huashan (*The Smiling, Proud Wanderer*),
and many fetch/crafting side quests. Terms: `docs/jy/glossary.md`.

## How to read the scripts

- Script keys are `1-C-N` (file `work/jy_gut/1-C-N.gut`); `startchapter C, N` jumps to script `1-C-N`.
- `say 0, "Name:text"` is an NPC or narration line; the speaker is the `Name:` prefix (sometimes with a
  full-width `：`). Untagged `say 0` lines are narration or the shopkeeper/NPC you are talking to.
- `say 1, "text"` is the player character (no name ever appears; the hero is never named in dialogue).
  A few player lines are mistakenly `say 0` (1-5-12, 1-9-14); translate them as the player speaking.
- `message` is a system box (Join/learn/sell notices). `choice "A", "B"` is a two-option menu (<= 19 chars each).
- `if N` / `setevent N` are quest flags; `attribtest 1, 0, L` checks the player's level (sect lessons unlock at
  Lv 11/21/31/41/51/61; the Mount Hua finale needs Lv 70).
- `enterfight 0, X, 0` fights ARS monster 3-3-X. The game also uses fights as a trick: crafting "fights" the
  crafted item's ARS (3-3-1..37) to award it, and the casino "fights" 赌具 (dice).

## The two protagonists (1-1-1)

The game opens with Yue Fei's poem 满江红 scrolling (`showgut`), one intro line, then "Choose your hero":

| choice | name | flag | can join |
|---|---|---|---|
| 1 | 幻吟风 Yinfeng (Huan Yinfeng), male | event 1 | Beggars' Sect, Shaolin, Wudang, Quanzhen, Huashan, Xingxiu, Xuedao |
| 2 | 紫灵儿 Ling'er (Zi Ling'er), female | event 2 | Hengshan, Ancient Tomb, Lingjiu Palace, Emei |

Both start with 100 taels and a Waystone (引路石: returns you to the nearest city; the world-map prompt
"Use / Examine"). He starts in the Capital, she in Dali. They have no personality text of their own: player
lines are generic "young knight-errant" talk (polite to elders, cocky to bandits: "Let them go, or you'll be
sorry!"). Keep player lines gender-neutral; sect quests are gender-locked anyway.

Sect gates (1-4-x) refuse the wrong gender ("Sorry, our sect takes no women / no men") and refuse anyone who
already joined another sect ("Sorry, you are not one of us"): **one sect per playthrough**.

## Chapter map (script key -> content)

| key | what | places / scene banner |
|---|---|---|
| 1-1-1 | opening, protagonist choice | - |
| 1-2-1..4 | outskirts of the four cities; Waystone prompt; 1-2-4 boatman to Peach Blossom Island | Capital / Xixia / Dali / Yangzhou (野外) |
| 1-3-1..11 | sect courtyards: disciples' chatter (one line each, lore flavour) | Beggars, Shaolin, Hengshan, Wudang, Ancient Tomb, Quanzhen, Huashan, Lingjiu, Xingxiu, Xuedao, Emei |
| 1-4-1..11 | sect mountains: gate check, herb gatherer (Ping Yizhi quest), Mt. Hua finale (1-4-7) | Beggars, Mt. Song, Mt. Heng, Mt. Wudang, Zhongnan, Mt. Hua, Lingjiu, Star Sea, Xuedao, Mt. Emei |
| 1-5-1..12 | wild areas: Yanmen Pass (main quest), Heartland (Huashan bandit quest), Peach Blossom Island, Passionless Valley, Gaochang Maze, Mt. Qingcheng, Snow Peaks, Flower Vale (tigers), Sword Tomb, Xiaoyao Cave, Snow Cave, Peach Cave (Zhou Botong) | as listed |
| 1-6-1..4 | the four altars: Blue Dragon, White Tiger, Vermilion Bird, Black Tortoise | Dragon / Tiger / Vermilion / Tortoise |
| 1-6-5 | Huang Yaoshi's home on Peach Blossom Island (Huang Rong teaches Dog Beater) | Huang's |
| 1-7-1..5 | Beggars' Sect masters | Hong Qigong, Teaching Elder, Clean/Ragged Elders |
| 1-8-1..5 | Shaolin masters | Abbot (unnamed) |
| 1-9-1..5 | Hengshan masters | Abbess Dingyi |
| 1-9-11..30 | **the Capital** (city + shops + quests) | The Capital |
| 1-10-1..5 | Wudang masters | Zhang Sanfeng, Yu Daiyan |
| 1-10-11..30 | **Xixia** | Xixia |
| 1-11-1..5 | Ancient Tomb masters | Xiaolongnu |
| 1-11-11..30 | **Dali** | Dali |
| 1-12-1..5 | Quanzhen masters | Wang Chongyang |
| 1-12-11..30 | **Yangzhou** | Yangzhou |
| 1-13-1..5 | Huashan masters + Repentance Cliff cave | Yue Buqun, Liang Fa, Lu Dayou, Ying Bailuo, Feng Qingyang |
| 1-14-1..5 | Lingjiu Palace | Tong Lao |
| 1-15-1..5 | Xingxiu Sect | Ding Chunqiu |
| 1-16-1..5 | Xuedao Sect | Blood Patriarch |
| 1-17-1..5 | Emei | Abbess Miejue |

City scripts share one layout (N = 11 city, 12 coach station, 13 general store, 14 inn, 15 Tongren Hall
pharmacy, 16 martial instructor, 17 armour shop, 18 Fuwei Escort Agency, 19 blacksmith, 20 weaver + hunter, 21
weapon shop + swordsmith, 24 magistrate, 25 underground casino, 26-28 townsfolk quests, 29-30 mysterious
jeweller/tailor). The same shop lines repeat in all four cities: translate once, reuse verbatim.

## Main quest (Condor Heroes), both protagonists

1. **Yanmen Pass** (1-5-1): Jin soldiers raid Huazheng's village ("my father is still in the desert"); the
   player beats them. She sends you to her anda Guo Jing's teachers, the Seven Freaks of Jiangnan.
2. **Yangzhou** (1-12-29): blind Ke Zhen'e invites you along to check on Guo Jing beyond the pass.
3. **Yanmen Pass, cliff top**: Cyclone Mei has seized Guo Jing to practise the Nine Yin Manual; fight. The Freaks
   leave for the Jiaxing duel.
4. **The Capital** (1-9-16): Mu Yi's marriage tournament; Wanyan Kang beats Mu Nianci and refuses to marry her;
   the player calls him out and fights; Wang Chuyi stops it.
5. **The Capital inn** (1-9-14): Wang Chuyi lies poisoned; needs the antidote from a physician in Xixia
   (Ping Yizhi's Dragon Dew). He reports that Yang Tiexin and his wife are dead and laments missing Guiyun Manor.
6. **Dali, Guiyun Manor** (1-11-28): Qiu Qianren urges everyone to submit to the Jin; Cyclone Mei attacks Guo
   Jing; someone with great lightness skill carries her off; Huang Rong leaves for Peach Blossom Island.
7. **Peach Blossom Island** (boat from Yangzhou): Huang Yaoshi bars the way; in the cave (1-5-12) Zhou Botong,
   bored and childish, teaches the Nine Yin phrase that opens the door and invites you to Mount Hua. System
   note: the Mount Hua quest needs Lv 70.
8. **Mt. Hua summit** (1-4-7): the Greats (Eastern Heretic, Western Venom, Southern Emperor, Northern Beggar) and
   Qiu Qianren are dueling; Guo Jing beats Qiu; Ouyang Feng refuses to accept Guo Jing as the best and you join
   the fight (three Ouyang Fengs). Ouyang Feng flees raving in Sanskrit. Guo Jing gives you the **Nine Yin
   Manual** (learn Nine Yin). Random branch: the player cannot read it ("!@#$%^&* what is this? Better tear it
   up") and instead the **Dragon Saber** (Dragonbane) "reappears in the world". Then the end note.

## Huashan quest line (male only, 1-13-x and cities)

- Yue Buqun (pompous "Gentleman Sword") takes you in, then asks you to investigate rumours that the Sword
  School's Feng Qingyang lives. The Capital innkeeper mentions an old man and two disciples flying about Mt. Hua;
  Yue gives you the key to the passage to the Repentance Cliff cave.
- Side lessons: Liang Fa (clear the Heartland bandits -> Hua Sword), Lu Dayou ("Sixth Brother", loves monkeys;
  mend the Tiger Kasaya with a tiger skin from Flower Vale -> Tiger Fist), Ying Bailuo (Dragon Dew for a
  snakebitten disciple -> Prime Palm; find Yue Fei's Sword in Dali, 20,000 taels in 2,000-tael notes, deliver it
  to the palace -> Stone Fist).
- Lao Denuo: Yue suspects him; in Yangzhou (1-12-26) you see him with Songshan men; Yue's Violet Mist Manual
  was swapped; you confront Lao, a poisoned arrow kills him (silencing a witness); you recover the real manual ->
  Violet Mist. Yue rages at "Zuo Lengchan" (source typo 左冷蝉).
- Linghu Chong (wine-lover, casual) and Yue Lingshan's lost sword: Lu Dayou says it fell into the Mt. Hua valley;
  the herb gatherer on Mt. Hua has it; Linghu sends you with a letter to Feng Qingyang -> **Nine Swords of Dugu**.
- **Branch at Repentance Cliff (1-13-5)**: Feng Qingyang reveals the Qi School drove out the Sword School. Yue
  Buqun appears and offers to make you senior Qi disciple if you help kill the three.
  - "Join forces": fight the Sword School; messages "Sword School destroyed", "Now senior Qi School disciple".
  - "Refuse": "So this is your true face! Grand-uncle Feng, I'm with you." Fight Yue Buqun; he flees; Feng takes
    you as a Sword School disciple; later Huashan disciples say "he's not my master any more". Cheng Buyou then
    teaches Fatal Trio once you bring a Zhenwu.

## Sect lessons (who teaches what)

| sect | teacher(s) | arts (MRS) |
|---|---|---|
| Beggars' Sect | Hong Qigong; Teaching Elder; Huang Rong | 18 Dragons (deliver the map of the north to the Capital); Taizu Fist (buy five Jiangnan wines at the Yangzhou inn); Mad Staff (Dali intelligence), Lotus Palm (warn the Capital Beggars of a Jin invasion); Dog Beater (riddle: 清圣浊贤 = wine) |
| Shaolin | Abbot | Long Fist, Arhat Fist, Damo Sword, Dragon Claw, Nine Yang (by level) |
| Wudang | Zhang Sanfeng; Yu Daiyan | Pure Yang (six herbs), Taiji Fist or Taiji Sword ("fist or sword?"); Wudang Fist (Tao Te Ching quiz), Coil Sword (a Platinum), Cloud Sword (a Zhenwu) |
| Quanzhen | Wang Chongyang | Quanzhen, Sky Palm, Doom Sword, Crown Palm, Dual Hands |
| Huashan | see above | Hua Sword, Tiger Fist, Prime Palm, Stone Fist, Violet Mist, Fatal Trio, Dugu Nine |
| Xingxiu | Ding Chunqiu | Venom Cast, Marrow Palm, Centipede, Tian Staff, Qi Dissolve |
| Xuedao | Blood Patriarch | Blood Blade, Godslayer, Snow Step, Blood Sea |
| Hengshan (F) | Abbess Dingyi | healing arts Minor/Mid/Major/Grand/Heng Heal + Heng Sword, Ever Palm, Bloom Sword, Heng Array |
| Ancient Tomb (F) | Xiaolongnu | Jade Maiden, Beauty Fist, Sky Net, Red Serpent, Sorrow Palm |
| Lingjiu (F) | Tong Lao | Sky Feather, Plum Hand, Eight Wilds, Death Charm |
| Emei (F) | Abbess Miejue | Cloud Palm, Wind Willow, Extinction, Severance, Buddha Glow |

Everyone: Basic Sword (Capital instructor), Basic Step (Xixia), Basic Qi (Yangzhou), Basic Heal (Dali); each
instructor first asks for a Ginseng (Pill). Joining any sect gives a Grand Pill. Masters' lines are short and
formulaic ("You must be Lv 10 or higher to join", "Would you like to join?", "Next art at Lv 31", "Learned a
new art!").

## Enemy and boss skills

MRS 4-1-2..16 are enemy arts, also drawn as text banners in the skill animations (must stay <= 11): Mad Cat,
Cleave Palm, Grappling, Swift Sword, All Buddhas, Dragon Palm, Qi Dissolve (Ding Chunqiu), Evil Ward (Yue
Buqun), Venom Staff (Ouyang Feng), Sunflower (Dongfang Bubai), Blood Blade (Shengdi), Snow Sword (Shi Zhongyu),
Gale Blade (Tian Boguang), Dark Palm (He Biweng), Bone Claw (Cyclone Mei). Bosses 3-3-87..95 are field bosses;
only Ouyang Feng and Cyclone Mei appear in the story.

## City side quests

- **Capital**: Ah Fang's dowry (earrings from the general store, 20 taels); Su Zhong wants to enlist - dissuade
  him or back him and talk his mother (Auntie Su) round; Huzi wants lessons (his dad, the instructor) and a
  slingshot (blacksmith needs an Ox Skin); palace guard receives Yue Fei's Sword / the map of the north.
- **Xixia**: Squire Liu buys ore; Niuniu wants to be a hero (dissuade or encourage); lovesick Li Yu (quotes Liu
  Yong) sends a lotus fan to Chunxiang; Ping Yizhi gives six Dragon Dew for six herbs (Mugwort - Mt. Song,
  Skyreach - Mt. Heng, Sesame - Mt. Wudang, Rainflower - Zhongnan, Poria - Mt. Hua, Peace Herb - Mt. Emei).
- **Dali**: Wu Jieshan wants tiger skins; Yue Fei's Sword seller; Old Mr. Wang needs Jade Salve; Zhang Jing
  (Ah Hong's mother).
- **Yangzhou**: Ah Hong is homesick (letters to and from Dali); Squire Li buys ore; the inn sells the five wines;
  boat to Peach Blossom Island from the pier.
- **Every city**: escort agency delivery (500 taels), magistrate's casino investigation (the casino is always in
  the next city), underground casino (10 taels, pays 10:1; "the officials won't find out"), crafting.

## Crafting chain (all cities)

Field "enemies" drop raw materials (ore veins, charcoal, ox/snake/tiger, flax/cotton/silk). Blacksmith: 5 ore ->
1 metal; Weaver: 5 fibre -> 1 cloth; Hunter: 5 skins -> 1 hide; each 100 taels. Swordsmith: Greatsword -> Zhanlu
-> Sky Sword (each needs the previous sword). Tailor/Jeweller: boots, helms, armour, cuffs, capes, rings,
necklaces. The four altar Immortals (1-6-x) each demand 6 x three crafted items, then fight; the prize is their
altar treasure (Dragon Cap, Tiger Cuff, Vermilion cape, Dark Boots). Recipe lines ("Greatsword: 4 Platinum 6
Black Gold 5 Charcoal 1 Zhenwu") must use the exact item names.

## Recurring characters and voice

| who | register |
|---|---|
| Hong Qigong | gruff, kind, old-man "I" (老夫); patriotic (resisting the Jin) |
| Teaching Elder (Beggars) | boisterous drunk: "Big bowls of wine, big hunks of meat!" |
| Huang Rong | teasing, clever ("Brush up your IQ and come back") |
| Zhou Botong | childish, giggly, wants a playmate; "Gotcha!" style |
| Seven Freaks / Ke Zhen'e | blunt, proud; Ke is blind and courteous |
| Cyclone Mei | snarling villain ("Get lost or I'll send you to hell") |
| Wanyan Kang | smug Jin princeling |
| Yue Buqun | pompous, sanctimonious, then exposed ("You little...! Very well!") |
| Linghu Chong | easygoing, wine-loving, warm to juniors |
| Lu Dayou | clumsy, likeable ("Don't tell Master!") |
| Feng Qingyang | terse, archaic-ish, contemptuous of Yue ("a hypocrite") |
| Lao Denuo | nervous liar ("Yes... yes, very stupid") |
| Zhang Sanfeng / Yu Daiyan | gentle teachers, philosophical quizzes |
| Ping Yizhi | cranky old physician of the "Demon Cult" |
| sect disciples | one-line lore; Shaolin/Hengshan monks and nuns speak in Buddhist maxims; Xuedao disciples are thugs |
| shopkeepers, townsfolk | stock phrases; "sir" (客官), "hero" (大侠) for the player |

Rogues: Xuedao disciples (Shengmao boasts of extortion), the bandits in the Heartland ("This little lady will
make a fine bandit wife"), Wanyan Kang, Lao Denuo. Monks/nuns: Shaolin (Kongxing, Qingle...), Hengshan (Yilin,
Yihe...), Abbess Dingyi, Abbess Miejue.

## Branching summary

1. Protagonist (1-1-1) -> which sects can be joined; one sect only.
2. Huashan Repentance Cliff: join Yue Buqun (Qi School) or side with Feng Qingyang (Sword School).
3. Mount Hua ending: random - learn Nine Yin, or tear it up and get the Dragon Saber.
4. Small quest choices (dissuade/encourage Su Zhong and Niuniu; Zhang Sanfeng's fist/sword; quiz answers)
   change only the reward or the dialogue.
