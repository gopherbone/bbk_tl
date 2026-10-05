# 侠客行 (xkx) - story notes for translators

A 2005 fan game for BBK's handheld, made with the BBKRPG kit ("BBKRPG开发包V1.3版", 伏魔记's engine) by **Chunlan
Studio (纯蓝工作室)**: script, planning and story by **Chunlan Guardian (纯蓝守护者)**, maps by **SSK**, engine by
**Nightbug (通宵虫)** and **Southern Imp (南方小鬼)**, testers Leng Yi, ZF, QQ 315200242 "and many netizens"
(credits 1-0-2, 1-0-5, 1-0-6; dated June 17 / July 1, 2005). In the intro it calls itself 《侠客正传》 ("The True
Tale of the Xiake"); at boot it is the 侠客完美版 "perfect edition". Terms: `docs/xkx/glossary.md`. Brief:
`docs/xkx/translating.md`.

## How to read the scripts

- Script keys are `1-G-N` (file `work/xkx_gut/1-G-N.gut`); `startchapter G, N` jumps to `1-G-N`, `callchapter`
  calls it and returns. `.event N L_x` maps map event / NPC N to a label. `loadmap T, N, x, y` loads map `2-T-N`.
- **Speaker tags are in the text**: `say 0, "剑圣：..."`. `pic` is only the portrait: **pic=1 is always the hero, Mo
  Ming**, and his lines have no tag; **pic=0 lines carry the speaker's tag** (or are system tips, 系统提示：). Write
  the tag as `Name: ` (glossary). A pic=0 line without a tag is usually a grunt ("呼呼……" in the haunted house, "哎。。。"
  from the beaten thief); check the .gut.
- `message` = centred narration / system box ("一时间天蹦地裂" "In an instant heaven shook and the earth split").
  `showgut` = scrolling text (intro, credits, sect descriptions, letters). `timemsg` = timed box (two, 1-3-5).
- `choice "A", "B", L`: two options, B jumps to L. `menu V, "a b c"`: space-separated, `ifcmp V, n` picks.
- `enterfight 0, ..., L_lose, L_win`: the first label is the **loss** (usually "System: You got killed. GAME OVER!"),
  the second the win.
- Variables: **var 1 = age** (+1 every 7200 ticks of play, about an hour: `seteventtimer 250, 7200`, event 250 in
  every script = "System: You're a year older." then 1-1-99), **var 2 = Essence Points**, var 19 = mazes beaten
  (the finale waits for 4), events 601-604 = maze guardians beaten, event 500 = Martial Lord, event 1000 = data
  repaired.
- `dump.py` shows a repeated line once. The five sect halls (1-4-1..5) are copies with the master's name changed,
  so each of their lines is a separate row: translate them identically apart from the name.

## The game in one paragraph

You are **Mo Ming**, son of **Mo Jingchou** in **Worryfree Village**. Your father collapses; the miracle doctor
needs five rare herbs (stolen with Pickpocket from monsters on the Wild Goose Pagoda's third floor), the **Dragon
Cauldron** (Rock Hill, guarded) and **Samadhi Fire** (or the mall's 50,000-yuan copy). Cured, your father sends you
into the world; your parents vanish, leaving a letter (an enemy wounded Father and took the **Minghan Manual**) and
Father's note: "Destroy the five great sects. Climb Bright Peak. Take the Minghan Manual." The game then opens up
into a raising sim across five regions: join a sect and climb its task ladder, win the **Martial Tournament**
(**Martial Lord**), marry, found your own sect, destroy the five sects. On **Bright Peak** you beat **Hua
Yingxiong**, who tells you he was once your father's pawn too; Mo Jingchou, head of the **Five Poisons Cult**,
appears, healthy, to take the manual and kill you both. Hua flies you home and dies. The imprisoned **Sword Saint**
explains: your father went astray training the manual; to stop him, seal every demon in the world into the well at
the village's west end with the **Electronic Dictionary Array** of five BBK e-dictionaries, powered by the manual's
ultimate move **Sky Thunder** (Nine Heavens Thunder). You lay the array; your father counters with the **Bagua
Array** and four Five-Element mazes. Break them, then choose: save your trapped father or not. Either way the author
ends the game in person.

## World, characters and voices

| who | tag / pic | voice |
|---|---|---|
| **Mo Ming** 莫名 | pic=1, no tag | Teen hero, cocky and jokey: net slang (汗, 靠, 嘎嘎, 9494, 88), English words in capitals (HELLO, OK, WAIT A MINUTE, THANK YOU), bracketed asides ("(Sweat... why did I ask that... he'd never admit it anyway...)"). Soft with kids and grannies, rude to profiteers and villains, shaken by his father's betrayal ("It can't be... it can't be..."). Calls his parents 爹 / 娘 (Dad / Mom), 父亲 / 母亲 in formal lines. Thoughts: 莫名心想 "Mo Ming thinks:". |
| **Mo Jingchou** 莫靖仇 | 莫靖仇： / 爹： | Coughing invalid at first; then the gloating villain ("Ha ha, good son, thanks for doing all this for me - but today is your last day!"; "To achieve great things you must stop at nothing!"). |
| **Mother** 娘亲 / 母亲 | 娘亲： | Worried, brief. Her first line is a deliberate glitch: "俺们美，俺们靓，俺们作文盖XX" (a garbled school slogan, "We're pretty, we're fine, our essays beat XX") and Mo Ming says "Sheesh... Chunlan wrote the dialogue wrong, didn't he?". Keep the joke: nonsense line, then the fourth-wall complaint. |
| **Doctor Wan** 万神医 | 万神医： | Pompous pseudo-scientific ("intermittent anaemia, as modern medicine calls it. In other words..."). |
| **Sword Saint** 剑圣 | 剑圣： | Grave mentor with sighs (。。唉。。); drily amused at the hero's haste; ends "Good luck!". |
| **Hua Yingxiong** 华英雄 | 华英雄： | Proud master of Bright Peak, then a weary, regretful old fighter ("Ah... these young people. You'll see soon enough!"; "Ha ha, that's the world. Accept your fate."). |
| **Chunlan Guardian** 纯蓝守护者 | 纯蓝守护者： | The author: breaks in with asides ("The hint's obvious enough, ha ha."; "Not written yet." at the inn's rumours), defends his computer in his studio, ends the game with a verdict. Casual, net-slangy (偶 = I, 丫 = particle). |
| **System** 系统提示 | 系统提示： | Instructions and rewards, but with attitude: "Damn, no money and you want to post a notice?", "Trying to mess with the system? Want me to GAME OVER you?", "A grown-up still playing with pets? Thrown out! The system deleted your pet!". |
| Sect masters 公治一, 何铁手, 岳不群, 独孤鸿, 冷傲天 | name： | Identical scripts: "Oh? You've got talent, kid. Interested in joining the X?", fetch tasks (bandits in the pagoda, a Peace Cake, candied haws for your little brother, a letter to Yi Tianchou, a pet egg for Madam), skill lessons, "Not a disciple? Get lost!", and the death line "I can't believe I was killed by a little noob like you! I won't accept it!!". |
| Villagers and forum users | name： | Each house has one person with a one-line "famous saying" (see Quotes), often plus a small errand. Forum users (SSK, Paladin, solfen, andygzq, Flooder, Xiyu, King of Comedy, Chengxin Electric, Chunlan Guardian, Flybug) also get the Top Ten notice exchange ("HELLO, are you X?" / "Mm, that's me. What's up?" / "Wow, really? That's great, thanks." / "I know, thanks for telling me."). |
| Bigeye 大眼怪 | 大眼怪： | Monster who turns out to be a sad orphan seeking revenge on Green Blight; dies in the Bloom Maze. Tragic beats are played half-straight. |
| Green / Red Blight 毒瘤青 / 毒瘤红 | | Gamer braggarts (CS, BnB, StarCraft); "GO GO GO GO". |
| Japanese NPCs | 木次一郎： etc. | Cartoon villains: "Wakakaka~", curse each other (狗日的 "son of a dog", 王八 "bastard"). The hero is openly jingoistic here (see glossary Decision 10). |

## Story by script group

The key's middle number is the group (`--chapters N`). The new game runs 1-1-1 (boot note) -> 1-20-6.

### 20 - Worryfree Village (prologue and the return)

- **1-20-6** (New Game): "Mother, I'm back - what happened to Father?" Choose the starting skill **Mo Fist** or
  **Mo Mind Art** ("only one chance"); Chunlan Guardian offers two newbie packs: **8888 yuan** or **beginner magic**.
- **1-20-7 / 1-20-4** Doctor Wan: the five herbs (Wake Fruit, Butter Tea, Jade Peony, Red Azalea, Red Whisk), then
  the Dragon Cauldron and Samadhi Fire; the medicine (Cure-All).
- **1-20-2** the family home (Serene Lodge): the Mother glitch line; the cure; "You're old enough, time to see the
  world"; "System: Join any sect, then come back to report." Later the empty house, the letter on the table.
- **1-20-5** the hidden **Chunlan Studio** room (the intro's "hidden storyline at the start"): Mo Ming plays the
  Xiake beta on Chunlan's computer, Chunlan fights him; outcomes give Essence Points and 888 / 8888 / 88888 yuan and
  a pet bug.
- **1-20-3** the Forbidden Room ("Father said never to enter this room"): the **Sword Saint**'s revelations and the
  Dictionary Array plan; the 9188 must come from Zhang Zhanqing and needs BBK forum support between 0 and 150.
- **1-20-1** the well: "Laying the Dictionary Array is what matters now!" -> "The Electronic Dictionary Array is
  open." -> Mo Jingchou: "Kid, I knew you'd try this. Hmph! Behold my Five-Element Bagua Array!" -> the system
  explains the four mazes (a guardian each, a teleport every 60 seconds). 1-20-8 "The next morning."

### 1 - the regions, Bright Peak, tournament

- **1-1-1** boot showgut: "This is the Xiake Perfect Edition. Press INSERT to repair the character data, and don't
  enter the Wood Maze when you do the four great mazes; that way you'll see the game's perfect ending. Thanks for
  all your support!" (The INSERT repair, 1-0-8, sets the maze counter to 1, so only three mazes are needed.)
- **1-1-2 Central Plains** (hub): Xiaohong among the flowers; Mr. Pu's letter home; the thief in shades ("did you
  steal Ah San's computer last night?"); **Zhao Si** and Xiaoxian's bun romance (spicy bun = "her love is so
  intense!", sweetest bun needs a banana leaf); the beggar's 1000-yuan secret; Paladin and solfen (Top Ten); the
  look/fight monster menus ("A monster. What are you looking at!", "STILL a monster"); wells ("System: Try another
  well~~").
- **1-1-3** the Nameless Elder's Hermitage: tips (the manual is with Hua Yingxiong on Bright Peak; the tournament;
  talk to every NPC for hidden plots) and the **Coming-of-Age Rite** (age 18; training maze, 5000 yuan, 88 Soul
  Wisps in 10 minutes; 1-100-1).
- **1-1-4 North**: the haunted house rumour, odd monsters ("Unknown object... still can't tell what it is...", "All
  players: (retch)"), Flybug's locked door.
- **1-1-5 South**: Xiaoxian; the Huashan Big Brother's black water (Water Demon -> SSK's Tianshan Water); Bigeye
  sightings; the **Bright Peak gate** checks (Martial Lord? five sects destroyed? own sect?) and, after the
  revelation, "A place of sorrow, why go back..." / "Laying the Dictionary Array is what matters now!".
- **1-1-6 West**: the wounded soldier who eats the medicine wrapper (slapstick, "I've eaten more crap than you've
  eaten rice!"); the young monk (Qin Guan quote) whose senior Bigeye carried off.
- **1-1-7 East**: the guard and his lord's rewards, Bigeye ("I'm from the north."), the boy's-urine hawker, chase
  or not; the old man's Japanese phrasebook (10000 yuan) and the locked crossing.
- **1-1-8 Japan Island**: help the **Red Carp** leap the Dragon Gate (three stone fights).
- **1-1-9 / 1-1-10 Hua Manor**: the strange well; **Hua Yingxiong**'s fight, the betrayal by Mo Jingchou, Sword
  Control back to the village. Two versions of some lines exist (before / after).
- **1-1-97** the Martial Tournament (ages 10, 20, ...; ten wins in a row = Martial Lord, +100 Essence, +50
  Renown). **1-1-98** quest rewards and the free choice menu (Essence / Sect / Story Points / Renown).

### 2 - Central Plains houses

Errand chains: candied haws for Xiaohu (his mother pays), Young Wang's letter to Old Wang (who makes fishing
rods), the Old Fisher's rod, **Zhang Zhanqing** (BBK marketing: deliver the Top Ten notices to Paladin, solfen,
SSK, Flybug, Chengxin Electric, Chunlan Guardian, andygzq, Flooder, Xiyu, King of Comedy -> the Waiyutong 9188;
the new machine "early April, about 1000-ish" - "Wow... is that a robbery?"), Mrs. Pu, the drunk Village Chief,
Ah San's computer, Mingming's letter, the Little Prodigy's treasure maps ("People as bored as you are why China
develops so slowly."), Xiaomei's water, Uncle Xiong's BBK question, Granny Ah Wang's incense for the Dragon King,
the Fat Chef's cleaver, Nightbug's RPG dev kit and the hunt for Flybug.

### 3 - shops and services

Pawnshop (the Dragon Cauldron rumour: "one of the Five Divine Artifacts, brought to the world by Dongyouzi"), inn
(rest 100 yuan; rob the cook; barkeep's Sevenmile 200), mall (Oresmith, the Profiteer: Jay's CD 150, roses 100,
Samadhi Fire 50,000), pharmacy (herb lore; Life Joss / Poison 5000, Repel / Lure Joss 1000 / 2000; "You've bought
it 19 times already"), **Martial Hall** (buy a level for 5000, learn **Pickpocket** for 10000, AFK training),
Fun City (pet eggs 5000, weapon forging from ores), regional merchants (North helmets & clothes, South shoes &
armor, West wrist gear & accessories & weapons), Big Rabbit's lost wallet (East), the Chinese merchant in Japan.

### 4 - sect halls and city services

- **1-4-1..5** the five sect halls: showgut description (sect lore with Jin Yong arts), join (once; must be grown
  up to betray or destroy), task menu `找点事做 完成任务 放弃任务 学习技能 灭门派` ("Find-work Turn-in Give-up
  Learn-skill Destroy-sect"), skill levels 5..60 for 20..200 Sect Points, destroy the sect (fight the master).
- **1-4-6** the Matchmaker's wedding (88888 yuan; "Already married? Looking for a mistress?").
- **1-4-7** the Sect Hall: "Marriage is the mark of a successful man - behind every successful man there's a
  woman"; 88 Stones + 88 Cleavers build your own sect.
- **1-4-8** the Net Cafe: 100 RMB a session; browse the BBK forum / BBK Fan Club (support +1) or clean up forum
  trolls; the A-series dictionaries glow; a big reward box.

### 5 - dungeons

1-5-1 the pagoda bandits and the runaway baby pet; 1-5-2 Rock Hill: the Dragon Cauldron's Guardian ("Who dares
touch my bed?" ... "I'm filing a complaint against Chunlan Guardian!"); 1-5-4 the Bloom Maze: Bigeye's story and
death (Master Xuanji's reply is gibberish; "the Master told me not to seek revenge..."), you're sent to Huashan;
1-5-5 Well Bottom: the **Water Beast** and its absurd lore system tip ("...even the Buddha can't do anything
about it..." / Mo Ming: "Damn, will this ever end? What kind of system tip barges in now...").

### 6 / 7 / 8 / 9 - North, South, West, East houses

- **North (6)**: Xiaoxue's Peace Cake, Code Nut's USB stick, the Wise Elder's letter, the Charmer's flowers, Ah
  Xiu's runaway sister, the Super Jay Fan's CD, **SSK** (Tianshan Water; Flybug "digging a secret tunnel to store
  oil and make a killing when World War Three breaks out"; "fake = real, real = fake!"), the **Wushan Two**
  (Old Codger and Codger Old), the Shopaholic, the **Old Granny** whose daughter (MM) was kidnapped -> rescue in the
  Bandit Den (password scene: "Answer the password!" -> "Correct. Please enter your username and password." ->
  "Wrong password, returning to the login page." -> "The page cannot be displayed!"), court her with roses
  (Affection 0-100), propose, wed at the Matchmaker's; as your wife she offers the bridal chamber (10 Essence: "a
  daughter is born...", "this game strictly forbids a second child!"), rest, knitting; Old Wu; the Haunted House
  (ghost; the servant's riddle "How are fake and real related?" leads to Flybug's maze).
- **South (7)**: Yi Tianchou (sect letter), Chengxin Electric, the Old Uncle's pet egg, **Xiaobao**'s "secret"
  (1000 yuan: "my secret is that I have no secret") and the real secret of the Bright Peak well treasure, Ah Dai's
  cold, PC Nut, Libai, Shadow Pig, Chunlan Guardian's house, **Blight's Den** (Bigeye vs Green Blight).
- **West (8)**: Master Xuanji, andygzq (Flood King), Pingping, Shin-chan, Zhuofeng, **Big Rabbit's mother** (about
  to hang herself; his heirloom Glow Pearl), TAD (his RPG site and QQ), Yaya, Flooder, Windchime, Silly King, Leng
  Yi.
- **East (9)**: Xiyu, **Dugu Zheng** and the **Old Uncle** (the Wushan Two killed his family 30 years ago: help or
  "less trouble is better"), Ye Lingling and Doudou (exam doggerel), Fangfang / Qin'er / Douzi (the "you can't...
  but you can..." chain), **Tipsy Sword** (gibberish spell lets you past the miasma to the Bright Peak well), King
  of Comedy, Ding Feng, the Philosopher, the Mad Patriot.
- **10**: Flybug's tunnel: pay all your money for his art (Delete Post).

### 30 - Japan Island

Uncle Tu (latrine aphorism), Xiaowang (Lu Xun), the three feuding Japanese (Kitsugi Ichiro pays 10000 yen = 2500
yuan "What a rip-off!"), the Consulate ("We're applying for a permanent seat on the Security Council, don't
bother me!" - the 2005 UN bid; kick him or GAME OVER "for shaming the Chinese people").

### 40 - the Bagua Array (finale)

1-40-1..4 the four mazes, each guardian "Enter the Metal Gate and you'll never leave, ha ha!"; 1-40-5 the array
breaks: "Mo Ming, save me, it hurts so much." Choice **Save / Don't save**:
- Don't save -> Chunlan Guardian: "Ho ho, how heartless, not even saving your own father. The game ends here, thanks
  for playing." (`gameover`)
- Save -> "Ha ha, free at last! Die, boy!" -> fight -> "Watch me transform!" -> fight -> Chunlan Guardian: "A man
  like that deserved to die - he wouldn't even spare his own son. The game ends here, thanks for playing."
- Losing any fight -> GAME OVER and the credits.
Messages "The Metal Gate has been broken." etc. when re-entering a beaten maze.

### 0, 50, 100, 255 - systems and items

- **1-0-1** intro showgut (序): the game pitch, "all NPC dialogue is famous quotes, so read them carefully", "use
  Pickpocket a lot", "finding the hidden storyline at the start makes things easier". **1-0-2 / 1-0-5 / 1-0-6**
  credits (and death by old age: "You have lived past the span Heaven allots; it's time to pass away peacefully.
  Please start a new game."). **1-0-6** the status menu (allot Essence / check Renown / check age / check Sect
  Points / minimap) and the age and point read-outs. **1-0-7** the second menu (teleport / manage sect: post a
  recruitment notice for 1000 yuan / switch Free-Contest mode / play ringtones 1-11). **1-0-8** INSERT repair, **1-0-9**
  DEL unused.
- **50**: the teleport menus (100 yuan; house lists per region).
- **100**: the training maze (Coming-of-Age): Soul Guardian, "use magic to collect them", coming of age clears your
  sect data and deletes your pet.
- **255**: item scripts: point scrolls, Mother's letter (1-255-39, a showgut starting "莫名：" = "Mo Ming,"), Father's
  note (1-255-40), the Minghan Manual (Sky Thunder), Life Joss / Poison (age +-1 year, game clock -+1 hour), Soul
  Orb, Big Rabbit's letter (1-255-59, signed "★不孝子--大兔子★" "Your unfilial son, Big Rabbit"), Repel / Lure Joss.

## Systems

- **Stats**: free allocation from **Essence Points** (10 per point of Attack / Defense / Agility / Spirit / Luck, 2
  for Max HP / Max MP), via the status menu.
- **Age**: starts at 0, +1 per hour of play; checks at 18 (adulthood: tournament fights, betraying / destroying
  sects, the Warrior), tournament at 10, 20, 30, 40, 50; death past the 90s. Life Joss / Poison shift it.
- **Sects**: join one of five; tasks give Sect Points; skills at levels 5-60; once grown up you can destroy them
  (needed for Bright Peak), and build your own after marriage.
- **Renown** ranks, **Story Points**, **Affection**, **BBK forum support** (0-150, for the 9188).
- **Pickpocket**: the only way to get the herbs; the intro's "secret tip". Enemy look screens list what they carry
  ("Carrying: X").
- **Money**: yuan. Teleport 100, inn 100, levels 5000, wedding 88888.

## Running jokes and things to keep

- The fourth wall: "Chunlan wrote the dialogue wrong", "I'll delete you as an NPC!", "I'm filing a complaint
  against Chunlan Guardian!", "Why do all the monsters in Xiake love sleeping?", "how did Qigong Wave get into
  Xiake?", "Look at you, how will you continue the story now?".
- BBK product placement, played straight by the NPCs (the 6980 "strongly recommended by Chunlan Guardian").
- The reward numbers 8 / 88 / 888 / 8888 / 88888 (lucky eights).
- 汗 sweat-drops, 555 crying, 靠, GAME OVER spelled GAMEOVER (write "GAME OVER"), English shouted in capitals.
- The Top Ten notice exchange repeated ten times (keep it identical).
- The masters' repeated lines (keep identical).

## Quotes

The intro promises that all NPC dialogue is 名人名言 "famous sayings". In practice it means **one motto line per
minor NPC** (the line they say before or instead of their errand): about **45 lines**, nearly all in groups 1-2,
1-3, 1-6..1-9 and 1-30. A full survey of the script (all 1884 say rows) found **no line attributed to a named
Western figure** (no Edison, Franklin, Einstein or Shakespeare by name). Most mottos are anonymous modern Chinese
aphorisms of the kind circulated in 2000s essay collections, QQ signatures and BBS posts; about ten can be traced
with confidence. Proverbs, parodies and set phrases are a second, larger group.

How to translate them:
- **Identified quotations**: use the English given below (an established translation where one exists, otherwise
  a faithful line that keeps the famous wording recognisable). Keep the speaker tag; no attribution in the text
  (the source gives none).
- **Unidentified mottos**: translate as a crisp English aphorism: faithful, one or two sentences, no padding, no
  invented source. Where the Chinese is florid prose, keep the imagery but tighten.
- **Proverbs and set phrases**: an English idiom of the same force if there is one, else a plain rendering.

### Identified quotations

| id | speaker | zh | source | English |
|---|---|---|---|---|
| 1-1-6@0652 | Young Monk | 两情若是长久时，又岂在朝朝暮暮。 | Qin Guan 秦观, "Immortals at the Magpie Bridge" (鹊桥仙), Song dynasty (original 久长时) | Xu Yuanchong's version: "If love between both sides can last for aye, / Why need they stay together night and day?" (plain alternative: "If love is to last, why must lovers be together day and night?") |
| 1-7-1@027b | Yi Tianchou | 黑夜给了我黑色的眼睛，我却用它来寻找光明。 | Gu Cheng 顾城, "A Generation" (一代人, 1979) | "The dark night gave me dark eyes, / yet I use them to seek the light." |
| 1-9-2@0518 | Dugu Zheng | 生命诚可贵，爱情价更高，若为自由故，二者皆可抛。 | Sandor Petofi, "Liberty, Love" (Szabadsag, szerelem, 1847), in Yin Fu's famous Chinese version | Follow the Chinese: "Life is dear, love is dearer still; but for freedom's sake I'd give up both." (ASCII "Petofi" if named.) |
| 1-30-2@020a | Xiaowang | 不在沉默中爆发，就在沉默中死亡。 | Lu Xun 鲁迅, "In Memory of Miss Liu Hezhen" (记念刘和珍君, 1926) | Yang Xianyi and Gladys Yang: "Unless we burst out in the silence, we shall perish in this silence." |
| 1-6-4@0281 | Charmer | ...乐的逍遥，乐得自在，面朝大海春暖花开，这就是幸福。 | the ending quotes Hai Zi 海子, "Facing the Sea, with Spring Blossoms" (面朝大海，春暖花开, 1989); the rest is modern prose | end with "...facing the sea, with spring blossoms. That's happiness." |
| 1-4-6@0214 | Matchmaker | 愿天下有情人终成眷属。 | Wang Shifu 王实甫, The Romance of the Western Chamber (西厢记) | "May all lovers under heaven be joined in marriage." |
| 1-6-6@02e6 | Super Jay Fan | 快使用双节棍，哼哼哈嘿！ | Jay Chou, "Nunchucks" (双截棍, 2001), the chorus | "Quick, use the nunchucks! Hng hng ha hei!" (Mo Ming: "Waaah, my poor ears.") |
| 1-9-13@020c | Mad Patriot | 中国，中国我爱你，就像老鼠爱大米。 | parody of Yang Chengang's hit "Mouse Loves Rice" (老鼠爱大米, 2004: 我爱你，爱着你，就像老鼠爱大米) | "China, China, I love you, like a mouse loves rice!" |
| 1-4-7@025e | Warrior | ...每个成功的男人背后都有一个女人... | English proverb "Behind every successful man there is a woman" | use the proverb's English wording |
| 1-6-13@024a / @0268 | Bandit / Mo Ming | 天龙盖地虎！ / 宝塔镇河妖 | the bandits' password and countersign in Qu Bo's novel Tracks in the Snowy Forest (林海雪原, 1957) and the opera Taking Tiger Mountain by Strategy (原文 天王盖地虎) | "The Heavenly King covers the earth tiger!" / "The pagoda holds down the river demon." Mo Ming's aside "(how corny can you get)" explains it. |
| 1-5-1@02b7 | Mo Ming | 替-天-行-道！ | the Water Margin rebels' banner 替天行道 | "Doing - Heaven's - justice!" (keep the dashes) |
| 1-1-10@05d6 | Hua Yingxiong | 后生可畏 | Analects 9.23 (子罕) | "The young are to be held in awe." (Legge: "A youth is to be regarded with respect.") |
| 1-7-2@0218 | Chengxin Electric | ...黑夜无论有多长，总有天亮的时候。 | echoes the popular Chinese line from Macbeth IV.iii (黑夜无论怎样悠长，白昼总会到来, Zhu Shenghao's version of "The night is long that never finds the day") | the first sentence plain; the second may use "The night is long that never finds the day." or "However long the night, the day will come." |
| 1-6-9@0255 | Shopaholic | 前生五百次回眸，换来今生的擦肩而过。 | popular saying, often credited to Buddhist scripture (no such sutra line); the source writes 五白 | "Five hundred glances back in a past life buy one brush of shoulders in this one." |
| 1-8-6@03f4 | Mother Rabbit | 只为成功找方法，不为失败找理由。 | 2000s business slogan, no author | "Look for ways to succeed, not excuses for failing." |
| 1-9-5/6/7@020a | Fangfang / Qin'er / Douzi | 你不能选择容貌，但你可以展现笑容... (three lines) | a widely circulated inspirational list (it also circulates in English, unattributed) | "You can't choose your looks, but you can show your smile. You can't lengthen your life, but you can decide its width." / "You can't win everything, but you can give everything your best. You can't control the weather, but you can change your mood." / "You can't control others, but you can control yourself. You can't foresee tomorrow, but you can make the most of today." |
| 1-8-9@0216 | Flooder | 我每想你一次，上帝就掉一粒沙，于是有了撒哈拉... | 2000s internet love line (anonymous) | "Every time I think of you, God drops a grain of sand: hence the Sahara. Every time I miss you, God sheds a tear: hence the four oceans." |
| 1-3-10@0213 | Big Rabbit | 小学生是一队一队的，中学生是一堆一堆的，高中生是一伙一伙的，大学生是一对一对的。 | net joke | "Primary kids go around in lines, middle schoolers in heaps, high schoolers in gangs, and college kids in pairs." |
| 1-9-4@020c, 1-9-12@020a | Ye Lingling, Doudou | 应试教育你别喜... / 应试教育被你弃... | 2000s student doggerel against exam-oriented education (应试教育) | translate as rhyming couplets, e.g. "Exam-cram schooling, don't be glad: China's dropping you, too bad..." |

### Unidentified mottos (translate as aphorisms; do not attribute)

1-1-2@07a4 Zhao Si (命运可以夺走你活得高贵的权利...), 1-1-2@0a22 Paladin (梦想属于自己...; 声春 = 青春), 1-1-2@0b4d
solfen (Venus de Milo: "Flaws make beauty; that's why the Venus is so unforgettable."), 1-2-10@02d8 Young Wang
(the shallow God), 1-2-11@0296 Xiaomei (everything has two sides; even a beggar has joys and sorrows), 1-2-12@02a9 /
@02d2 Uncle Xiong (helping others; "I'd brashly claim second place under heaven - who dares claim first?"),
1-2-13@029e Granny Ah Wang (spring and goose-yellow buds), 1-2-14@028e Fat Chef (you don't know yourself),
1-3-2@062c the Cook (we weep, God smiles), 1-3-5@037d the Instructor (life borne by time, chasing eternity),
1-6-1@0289 Xiaoxue (art poeticises, love deifies), 1-6-2@02a3 Code Nut (his motto: "When you're unhappy, try to be
happy; believe that everything now is Heaven's best plan for you."), 1-6-3@0296 Wise Elder (depressed without a
reason), 1-6-5@0280 Ah Xiu (song-like: "I'm searching for my first love..."), 1-6-7@0227 SSK ("Skip the small jobs
and you'll toil at smaller ones."), 1-6-11@020c Old Wu (life's road, step by step), 1-7-3@0327 Old Uncle (men who
do / don't understand romance), 1-7-4@02cf Xiaobao ("Opportunity is a thief: it comes without a sound and leaves
you robbed."), 1-7-9@0214 Chunlan Guardian ("Life is full of contradictions; nobody can help it."), 1-8-1@0218
Master Xuanji ("If my existence is a mistake, I'd rather keep making it."), 1-8-2@0214 andygzq (youth without
smiles / tears), 1-8-5@020a Zhuofeng (song-like lines across the Milky Way: keep the lyric rhythm), 1-8-8@020a
Yaya (hurting one life), 1-9-1@0214 Xiyu (you can't run from yourself: your faults, guilt, duty - like a mirror,
like your shadow), 1-9-3@0337 Old Uncle (a miracle is a miracle because it's rare), 1-9-9@0218 King of Comedy
(refusing at the right time is true friendship), 1-9-10@020a Ding Feng (a life that suits you is the best
happiness), 1-9-11@020a Philosopher (stubbornness costs you), 1-30-1@020c Uncle Tu (latrine proverb twisted: "People
say hogging the latrine without using it is bad; worse is finishing and still hogging it.").

Small talk that is not a motto (平平 "peace", 风铃 "wind", 傻王, 冷义, 小新, 电脑狂, 立白, 影子猪) is ordinary
dialogue.

### Proverbs, idioms and set phrases

| id | zh | English |
|---|---|---|
| 1-1-2@10b6 | 君子报仇，十年不晚 | "A gentleman can wait ten years for revenge." |
| 1-3-2@0792 | 三十六记(计)，走为上策 | "Of the thirty-six stratagems, running is the best!" |
| 1-20-5@0589 | 不打不相识 / 相识一场也算是缘分 | "No fight, no friendship" / "meeting like this was fate" |
| 1-1-3@04d6 | 亲兄弟还明算帐 | "Even brothers keep clear accounts." |
| 1-1-6@0478 | 我吃的屎还多过你吃米 (parody of 我吃的盐比你吃的米还多) | "I've eaten more crap than you've eaten rice!" |
| 1-1-7@03d6 | 撒泡尿去照照镜子吧 | "Go take a good look at yourself in a puddle of piss!" |
| 1-7-4@03a8 | 狗眼看人低 | "Don't you look down on me!" |
| 1-2-9@020a | 上知天文，下晓地理 | "I know the stars above and the earth below." |
| 1-2-7@0230 | 一个字"好"，两个字"很好"，三个字"非常好"，四个字。。。 | count words in English: "One word: 'good'. Two words: 'very good'. Three words: 'really very good'. Four words..." |
| 1-4-6 | 一拜天地 / 二拜月老 / 夫妻对拜 / 送入洞房 | "First, bow to Heaven and Earth!" / "Second, bow to the Matchmaker!" (parody of 二拜高堂 "bow to the parents") / "Bride and groom, bow to each other!" / "To the bridal chamber!" |
| 1-0-5, 1-0-6 | 已超过天命之数，该寿终正寝了 | "lived past the span Heaven allotted you; time to die peacefully in bed" |
| 1-6-7@0483 | 虚虚实实... 虚=实，实=虚！ | "Fake fake real real, real real fake fake... fake = real, real = fake!" (fake/real to match the answer choice "Fake=fake,real=real") |
| 1-1-2@0747 | 帮人帮到底 | "In for a penny, in for a pound." |
| 1-1-8@0672 | 跳龙门 | "leap the Dragon Gate" (the carp that leaps it becomes a dragon) |
