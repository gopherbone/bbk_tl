# 十字之门 (Cross Entry) - story notes for translators

A one-person hobby RPG on the BBKRPG engine by **翼王 (Yiwang)**, who credits himself for art, story, design,
setting and production (1-7-10, under the typo "STUFF:"). Western fantasy, short and linear: four cities, four
keys, one gate. Terms: `docs/szzm/glossary.md`. Brief: `docs/szzm/translating.md`.

## How to read the scripts

- Script keys are `1-C-N` (file `work/szzm_gut/1-C-N.gut`); `startchapter C, N` jumps to script `1-C-N`. Every
  story script is reached; there is no 1-6-9. `.event N L_x` maps map event / NPC N to a label; `createnpc N,
  sprite, x, y` puts NPC N on the map, so `.event 3` is "talk to NPC 3".
- `say P, "text"`: P is the **portrait**, not a speaker tag, and this game has almost no tags. **pic=1 = Delat,
  pic=2 = Eluna** (always). **pic=0 = whoever else is talking**: the NPC you spoke to, the boss, the guard, the
  temple keeper. The only tagged line is `翼王：` (1-0-7). When pic=0 is unclear, read the .gut around the line.
- `message` is a system box (narration, actions, item gains: "艾露娜拔剑" = "Eluna draws her sword."). Narration is
  third person, past or present, consistent within a scene; use present tense for stage directions ("Eluna grabs
  the boy and shakes him.").
- `choice "A", "B", L`: a two-option menu (<= 19 chars each; B jumps to L). `menu V, "a b c"`: space-separated.
- Flags: `if N` / `setevent N` are events, `set` / `add` / `ifcmp` variables. **Event 2008 = Special mode.** Var
  199 guards New Game (see the engine-bug notice). Var 23 counts Crests II-III (the Leoz ambush waits for 2).
- `enterfight 0, a, b, c, ...` fights monster records a/b/c; nearly every story fight has a Normal and a Special
  set (`if 2008`). Monster names are placeholders (d1...), so nothing in battle needs translating.
- Dedupe: `dump.py` shows a repeated line once ("快走吧。" "你想要住店吗？..." the inn and shop lines, "没有该物品",
  the key choices). The Leoz confrontation exists twice (1-6-4 and 1-6-5, two places it can trigger); most lines
  dedupe, a few differ by one typo (装/将): translate those identically.

## The world (prologue, 1-1-1 showgut)

"Prologue: Legend says that over two thousand years ago, humans lived happily on the surface..." Humans were the
gods' favourites, masters of a beautiful world of flowers, beasts and fish; greedy, they fought each other and
finally sought the gods' own power to kill each other for land. The angry gods banished them into the dark
underground, never to see true light. Humans repented; the gods did not forgive. After some five hundred years
they had built the great **Kingdom of Okaros** underground, and the gods sent down a decree: one last chance -
somewhere underground stands a "**Cross Entry**" leading to the beautiful surface...

The truth (1-7-10) contradicts the legend: there were no gods. 2000 years ago humans on the surface discovered
**lightstone**, refined it into **Sunstone**, fought a total war with it, and turned people into living Sunstone
weapons, the **Guardians**. The youngest, a giant with huge black wings, destroyed the largest Sunstone reserve in
rage because his little sister was next to be "remade"; the released energy wiped out the surface. The Guardians
carried the survivors underground and became the keepers of the exit, leaving one bracelet as the only key. They
have waited 2000 years. The surface is a grey sky over blood-red ground, with no life.

## Characters and voices

| who | portrait | voice |
|---|---|---|
| **Eluna** 艾露娜 | pic=2 | Foundling raised by Kabras Temple, junior swordswoman, about the same age as Delat (teen). Certain she came from the surface because her bracelet's stone is in no book. Bossy, impatient, fearless, physical ("Tomorrow~~~!!!", drags Delat by the collar, threatens him with her sword), clever with locks and magic circles, has read half the royal library. Calls Delat 笨蛋 "idiot". Gentle with Heath; weeps once at the end, then decides to fix the world. Quick, punchy English. |
| **Delat** 德拉特 | pic=1 | Crown prince of Okaros, a mage, travels incognito as a commoner. Whiny, sarcastic, lazy, low stamina ("Can we rest?"), the voice of sense who always loses. Inner grumbles in brackets: "(Why does a prince have to sneak into his own house...)". Loves her; reads mystery novels instead of helping. Darkens when he learns his father is a murderer, hides it with jokes ("Ha ha ha, that's a great joke, almost sounds real"); refuses the throne ("I don't want it! Facing those ministers every day?"). |
| The temple keeper 大叔 | pic=0 | Raised Eluna. Grumpy, fond; tic 早知道... "If I'd known...", piling up regrets ("If I'd known, I'd have left you outside for the mosquitoes!"). Eluna: "Yes, yes, Uncle is the best man in all Okaros." |
| **Locke Reiter** 洛克斯・雷特 | pic=0 | Former royal historian, hermit outside Snowblade. Curt, rude, theatrical countdowns ("I'll give you five seconds to leave this house." -> when told they are from the palace: "Three seconds. Vanish!"). Softens at the sight of the bracelet. Resigned because the new King had him write the purge out of history. |
| **Heath** 希瑟 | pic=0 | Boy of 12-13 in Silverleaf with Dorowell Syndrome; a cheeky hustler ("I'm serious!", waves a "special pass"), lies that his lost sister leads the Moon's branch. Really his only family died eight years ago; he wants to see the woman who looks like her. Dies the day after Eluna, disguised by an old potion, spends a day as his sister and sings him a lullaby. |
| The doctor 医生 | pic=0 | Heath's doctor and guardian, about thirty; quiet and sad. |
| **Leoz** 莱奥兹 | pic=0 | Moon of Vengeance ringleader, armoured man in his forties, tired and bitter, the King's elder brother. Gruff ("Kid, you're from the palace, right? Then die!"), proud in defeat ("Kill me if you want."). |
| Guards, clerks, townsfolk | pic=0 | Stock fantasy NPCs. A few philosophers ("Am I really alive? There's no reason... but I don't want to die."), a dizzy drunk, an English-sprinkling teacher (1-4-11: "HEY! ... GOOD! ... OK! Watch me. ... OH!": keep the English words in capitals). |
| The Guardians | pic=0 | Four key-keepers (formal challengers: "Show me whether you are able to seek the truth"), the black-winged giant (child-like, mocking, then dying), and the last Guardian at the gate (calm, nostalgic: "I miss them, those pretty little grasses."). |
| Yiwang 翼王 | pic=0 | The author, dug up from a hidden spot (1-0-7): "Damn it, I was lurking down here! Why'd you dig me up?!" (潜水 = forum lurking). Fights you; loses -> "Not bad, take this" (Demon Eye); wins -> "Boring... I'm going back." |

## Main story by script group

### 1-1 Kabras (capital) - prologue, the exam, the library, and returns

- **1-1-1** New Game: "Choose a mode." Normal / Special (event 2008). Prologue scroll. Night in the Royal Library:
  Eluna (snuck in through the palace sewers again) searches books for her bracelet's stone; Delat helps, has to
  read sixty books, and secretly reads *The Strange Fountain Murders*. She takes the swordsmanship exam the day
  after tomorrow. Next morning at the temple the keeper wakes her ("If I'd known..."). If var 199 is already set
  (a second New Game in the same session) the game shows the engine-bug notice and ends.
- **1-1-3 / 1-1-4** temple and Eluna's room: "Done with the exam?" "Mm." "Passed?" "Mm." Sleep until evening,
  then "Off to the Royal Library."
- **1-1-10..12** Swordsmen's Guild: junior swordsman exam in the tower maze she "got bored of when I was eight":
  reach the top in three hours and beat the monster. Pass -> Sword Pin.
- **1-1-7 / 1-1-8 / 1-1-9** palace front, sewers, library: Delat wants the front door, Eluna insists on the sewers
  ("people would gossip about us!"). In the library Delat admits he found Cross Entry news **a month ago**; Eluna
  draws her sword (messages "Side sweep" / "Straight thrust" / "Hyper Wave Sword!"). The lead: a retired court
  historian in Snowblade. Delat can now leave the palace "to train in magic". "The day after tomorrow." "TOMORROW~~~!"
  Next morning outside the temple: "You're five minutes late." They set off west (Delat joins).
- **1-1-5 / 1-1-6** Kabras streets: townsfolk, a man reading **Genesis 1** aloud line by line (1-1-5 @015c..: use
  the King James text), an official waiting for the Nightstar Watch's report (side quest), hints ("Strange things
  are used on strange places. And if one won't work, try Enter."), "Kabras is so big my head's spinning".
- **1-1-14** Workshop: craft (Seer Hat, Holy Robe, Rune Boots, Hope Aegis, Sure Hand, Key, Scroll L) or refine
  lightstone (Shardstone -> Glimstone -> Starstone -> Dawnstone; Blazestone once the recipe is known).
- **1-1-16..19** shops and inn. 1-1-16's shopkeeper: "We've got everything here except what we haven't got."
  (mirrored in Snowblade 1-2-9: "We've got nothing here except what we've got.") Inn: 100 Gold.
- **1-1-20 / 21 / 24 / 25** side NPCs: inn guest (Heal, Special), potion maker (Shardstone -> MP Potion x6, then
  First Aid for a Dawnstone, Special), messy house (clean-up fights for starter gear; losing shows "Clean-up
  failed."), a girl who wants Rune Boots (Scroll G).
- **1-1-13** (return, after the Eternal Darkness) Royal Library: Eluna finds the *Early History of the Kingdom* and
  learns they need a Blazestone. "Idiot! We refine one, of course!" "(Waah... why does a prince have to obey you
  in everything...)"
- **1-1-15** Graveyard: the movable gravestone, opened with Reiter's Odd Key, hides a tunnel.
- **1-1-8 @014f** (finale, after the Forgotten City) in the sewers: "You're really not going to help your
  father?" Delat tears up the notes he stole from the Institute's sealed lab: how to refine the purest lightstone,
  enough to destroy Okaros, which his father wants against the Moon. He doesn't want to be king. A forgotten
  sewer branch, opened now that they have all the keys, leads under the palace.

### 1-2 Snowblade - Reiter, the Magic Institute, Crest I

- **1-2-1** arrival; the Institute guard: "This isn't a place for little girls' fairy tales." "I'm not a little
  girl! I'm a Junior Swordsman!!!" Delat won't use his rank (he has his own investigation). Townsfolk:
  philosophers, a would-be Institute employee (teleport circles run on Homeward scrolls).
- **1-2-2 / 1-2-4** Reiter: "I'm not in!" ... "Get in!" Countdowns, then he sees the bracelet, studies Eluna's
  hand for thirty seconds and tells them: collect one key from every city of Okaros except Kabras. Where? "No
  comment." Eluna reasons the keys are magical, so they need a detector; Delat can't detect magic; ten minutes of
  silence; "Snowblade must have a magic detector!"
- **1-2-3** inn at night: "Get up!! We're borrowing the detector." "They said no!" "So we take it ourselves."
- **1-2-1 @0494** break-in: Delat can't unpick a mechanical lock, a fireball would wake the city; Eluna picks it
  with her hairpin. "Were you really raised in a temple?"
- **1-2-5** the detector is in the lobby; Eluna rebuilds the circle with element-boost stones and a space-weakening
  device ("You want to blow the Institute sky-high?"); it shows every anomaly in the country; she times the guard
  shift ("two minutes until someone comes, run!") and drags him off at full sprint. Three anomalies, but she
  expected four. The first is in the Institute's own restricted basement.
- **1-2-6** maze (sign "Pi" = the door puzzle); Ignite item from the first fight. **1-2-7** first Guardian ("so
  you wear that bracelet; that's how you passed my spell") -> **Crest I**; teleported outside. Delat: the detector
  showed the three cities, the palace, the lightstone mines and the research sites, but no gate.
- Side: 1-2-8 / 1-2-13 a mother's son who wandered outside ("Mom sent you? ...Fine, I'll come home."), 1-2-11 a
  drunk teacher (Light Ward, Special), 1-2-12 the X/Y puzzle man (Fragment B; Haste, Special).
- **1-2-4 @0793** (after Leoz) Delat: "My father... is it true?" Reiter: yes, and that is why he resigned; he was
  newly appointed, who would believe him? Delat laughs it off. Reiter gives the **Odd Key**: the movable gravestone
  in Kabras Graveyard holds the fourth key "and also..."
- **1-2-4 @09db** (after Crest IV) Eluna: "Tell me! Is there really no one on the surface?!" The records say it is
  barren. "Your books must be wrong! Tell me where the Cross Entry is, I'll go see myself!" "...Under Kabras
  palace."

### 1-3 Silverleaf - Heath, the mine, Crest II

- **1-3-1** the anomaly is inside the old mine (sealed since a great explosion years ago; St. Melo Keep's mine,
  one entrance, guarded, pass only). Heath offers a special pass if they find his "lost sister" today: she leads
  the Moon of Vengeance's Silverleaf branch. Narration explains the Moon (two messages: keep each within 4 rows).
  Delat compares Eluna with the terrorists: "Fine. (Feeling a bit safer -_-~~)". Heath knows a secret tunnel.
- **1-3-3** in the hideout Heath hands over the pass, then yells "Moon of Vengeance, you big idiots! Come out!!"
  so they will lure the gang away. Three fights with summoned beasts.
- **1-3-2** the pass expired last month. **1-3-4** the office: a pass needs a palace permit. Then the wanted
  poster: Leoz, "the guy we beat last time" (1-6-1); his ring, which Eluna picked up, is worth a bounty, and the
  office agrees to give a pass instead. Delat: "Lucky right hand." Eluna: why did an "invincible" man lose to us?
- **1-3-6..10** the mine (Dig item; Starstones into four pillars; Cogwheels into machines; Sunblade). **1-3-11**
  second Guardian: "New heroes?" -> **Crest II**.
- **1-3-5** the doctor: Heath wants to see them. He confesses; Eluna already knew (the locket's date is last year,
  he said eight years; the spot on his right ear is Dorowell Syndrome). "How long does he have?" "...Tomorrow."
  She has the doctor gather herbs for an old book's face-changing recipe. Afterwards: "He cried so hard when you
  sang him the lullaby, but he was smiling." Delat: why not use the potion to fake an office clerk? "Idiot!! That
  stuff hurts worse than a knife on your face! Want me to cut you a few times so you can compare?"
- Side: 1-3-15 Special teacher (Skill Lock / Revive), 1-3-16 "a nasty guy outside town" (fight in 1-6-11;
  Scroll K), 1-3-17 apple for 5000 Gold, 1-3-18 hungry man (Rosary; Whirlwind on Special: "the secret art of the
  Whirlwind school!").

### 1-4 Nightstar - the Eternal Darkness, Crest III

- **1-4-3** outside the city it is pitch black and torches give no light: "the Eternal Darkness!" Eluna read about
  it somewhere: back to Kabras library (-> 1-1-13, 1-1-14). With the Blazestone: "It worked!"
- **1-4-5** maze (Climb item). **1-4-6** third Guardian ("you're not the first to reach me; the usual, then") ->
  **Crest III**.
- **1-4-1** city: the Watch captain forgot the report Kabras is waiting for (side quest; Gale Slash on Special),
  Dragonbane in a corner. 1-4-3 townsfolk: "I think, therefore I am... but is that enough?", the ancient stone on
  the city's highest point. 1-4-11 the English-word teacher (Thunderclap / Dazzle, Special), 1-4-12 Cleric Rod for
  5000 Gold, 1-4-13/14 a girl's lost necklace (Bookmark).

### 1-6 The roads between cities

- **1-6-1** Kabras -> Snowblade road: an armoured man (Leoz, unnamed here) attacks Delat as "the palace's kid";
  Eluna: "I'm a girl, and I'm not from the palace." "He obviously didn't mean you!" Beaten, he waits to be killed;
  "No time." He drops a **Ring**.
- **1-6-4 / 1-6-5** after three keys, Leoz ambushes them: "You two thieves! Give back my ring!" He collapses
  (wounded: the army ambushed his group, he alone survived). Eluna returns the real ring (she gave the office a
  fake). His story: he is the King's elder brother and rightful heir; the King killed their mother (the ruler),
  replaced the ministers, tried to kill him, drove Kabras's citizens out, branded them rebels and Leoz a
  matricide; the expelled founded the Moon. Their headquarters has just been raided. Eluna: "Delat, he's your
  uncle, be polite!" They go to ask Reiter (-> 1-2-4 @0793). 1-6-5 also has a bridge guard ("Want to pass? Beat
  me first!").
- **1-6-6** the graveyard tunnel: a door; Delat (who now suspects what lies behind) whispers "Don't open...
  don't open..."; it opens. **1-6-7 / 1-6-8** chests. **1-6-10 / 1-6-11** fields and the nuisance fight.

### 1-5 The Forgotten City - Crest IV

- **1-5-1** guards accept "a letter from Lord Reiter". The steward reads the records: "...on the morning of the
  20th we completed our evacuation from Kabras. Over 16,000 dead; over 7,300 survivors." Delat is silent. They
  stay at the office. Next morning a tired Delat opens his door smiling: "Let's go get the last key. I'm not as
  fragile as you think."
- **1-5-3 / 1-5-4** maze (Smash item; signs "Maze Mk II", "Same to same", "Persistence is victory").
- **1-5-6** fourth Guardian -> **Crest IV**. "The last one, Eluna, your wish is coming true." A giant appears:
  "So you made it, fools seeking the surface?" Beaten, he turns into a child: "The surface isn't as pretty as you
  think. There's no one there." "My parents?!" "I never thought anyone could survive there." "...I'm dying too
  now... two thousand years late..." He vanishes (he is the black-winged Guardian of 1-7-10).

### 1-7 Finale - Kabras falls, the Cross Entry

- **1-7-1..3** "Something feels wrong!" The Moon has taken Kabras in a blitz before reinforcements could arrive and
  wrecked the teleport circles (saving is disabled for the walk in). Leoz is there. The palace is sealed from
  inside: "Then we go through the sewers."
- **1-1-8 @014f** Delat refuses to help his father (see 1-1). Under the palace: maze 1-7-4..9 (Homeward does not
  work now).
- **1-7-10** the Cross Entry won't open; four pillars: set each Crest and refight its Guardian. The last Guardian:
  "Defeat me and you will see the final truth." The true surface (grey sky, red earth, no life) and the history
  (see "The world" above). Eluna: "So I really am just an ordinary orphan? This bracelet just came to me by chance?" ...
  "If this world isn't the one I imagined, I'll make it that way with my own hands!" She smiles and wipes away
  her tears.
- **Epilogue** "Year 6 of the Cross Era." Only the topsoil was poisoned, and only a thin layer: Eluna had all of
  Okaros turn the ground over and replant it. Delat babysits Uncle Leoz's little princes (dodging a hand at his eye,
  prying a hand off his ear). "When are we having some of our own?" "You mean marriage? After I finish the
  surface." "We'll be old by then..." "You could find someone else." "Really?!" "You can try. =_=!" Credits
  ("STAFF:"), end.

### 1-0 and 1-255 - field skills and items

- **1-0-6** Ignite handler: "Nothing to light here."; torch-order puzzle ("Wrong!" for 错\xce). **1-0-7** Dig: chest
  contents, "You dug up nothing.", Yiwang's cameo. **1-0-8** Climb: "Nothing to climb here." **1-0-9** Smash:
  "Nothing to smash here."
- **1-255-1** Homeward scroll (back to the last city; "The Homeward scroll won't work!!" in the finale);
  1-255-2/3/4/17: "Press SEARCH / INSERT / MODIFY / DEL to use this item." (the BBK keys the emulator labels so);
  1-255-5..16 skill scrolls; 1-255-18 Compass (coordinates on/off).

## Systems

- **Party**: Eluna alone at first (actor 2), Delat joins at 1-1-9 (actor 1). A map event in Snowblade (1-2-1 @0925) toggles which hero leads.
- **Modes**: Normal / Special (event 2008). Special: stronger starting stats (attribset), tougher enemy sets
  everywhere, eight extra teachers (1-1-20, 1-1-21, 1-2-11, 1-2-12, 1-3-15, 1-3-18, 1-4-1, 1-4-11) who otherwise
  refuse ("You're not on 'Special', huh?").
- **Field skills** are items used with keyboard keys: Ignite (SEARCH), Dig (INSERT), Climb (MODIFY), Smash (DEL);
  each comes from a dungeon's first fight (1-2-6, 1-3-6, 1-4-5, 1-5-3).
- **Keys**: Key / White Key / Black Key open chests and doors; the four Crests open the Cross Entry.
- **Crafting** (1-1-14): recipe messages "Materials for 'Seer Hat':" then "'Shardstone' x10  'Soft Down' x15",
  "Craft it?" / "Refine it?", "Not enough materials." Keep the quote marks as ASCII `'` or `"`; keep the X counts
  as "x10".
- **Money**: Gold; inns 100 Gold; two 5000-Gold sales.

## Running jokes and things to keep

- The keeper's "If I'd known..." (早知道...), cut off every time.
- Eluna always takes the sewers; "If it's called a passage, it's meant to be passed" (是"道"就是用来走的).
- Delat's bracketed inner protests and his stamina ("Can we rest?" "No! Move it!" "Waaah! Let go! That hurts...").
- Eluna's "idiot!" (笨蛋), her countdown-proof bossiness, and threats with a smile.
- Reiter's countdowns: five seconds, three seconds, and Delat's prediction "ten seconds to get out".
- The mirrored shopkeeper lines (1-1-16 vs 1-2-9).
- Emoticons: `-_-~~` (1-3-1), `=_=!` (1-7-10). The heroes are called 两个主角 "the two heroes" once in narration
  (1-3-1 "The two heroes turn around at once."): keep the slight wink.
