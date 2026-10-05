# 英雄坛说 (Heroes' Altar) - story notes for translators

A 2005 hobby RPG by 才子工作室 (Caizi Studio) on the BBKRPG engine: design 金远见 (Jin Yuanjian), adaptation 柴梓
(Chai Zi), dated 2005-08-01 in the credits (1-0-1). The end note (1-0-2) says it is probably his last game because he
is about to start his second year of senior high school (马上升高二), thanks the many helpers without naming them,
and points to the 健康游戏忠告 (Healthy Gaming Advice) notice. Terms: `docs/yxts/glossary.md`. Brief:
`docs/yxts/translating.md`.

It is **not** a Jin Yong game. It is a goofy time-travel story told by a teenager to his forum friends: a modern
kid switches on a time machine and wakes up as a 14-year-old boy in a wuxia town, Safehaven (平安镇). Around a thin
main quest (take six sect heads' tokens, lure out the Archdemon, get home) sits a MUD-style sandbox: NPC "look"
texts, potential points, element stats, skill ranks, fame, a bank, a casino, founding your own sect, crafting,
a training realm. Expect constant fourth-wall jokes, 2005 Chinese net slang, BBK Club forum in-jokes and
pop-culture parody names.

## How to read the scripts

- Script keys are `1-C-N` (file `work/yxts_gut/1-C-N.gut`); `startchapter C, N` jumps to script `1-C-N`,
  `callchapter 9, N` runs a shared handler (1-9-x) and returns.
- `say P, "text"`: P is the **portrait**, not the speaker. `pic=0` = no portrait: either an NPC with a
  `Name:` tag, an untagged NPC (the one you are talking to), or **the hero** (most untagged lines in story scenes
  are the hero: "可恶,我非宰了他!"). `pic=4` = Yuxin (陈雨馨), `pic=5` = Bingyan (赵冰雁), `pic=1` = Dugu Sheng's
  portrait, used twice for hero lines whatever hero you picked (1-1-17 "多谢巡捕", 1-4-1 "靠!打八折吧!").
  Read the .gut file around a line when the speaker is unclear: villain/NPC tags precede their lines, and the hero
  answers untagged.
- `message` is a system box; `menu` a space-separated list (keep the item count; no spaces inside items);
  `choice "A", "B", L` a two-option menu (<= 19 chars each; B jumps to L).
- Flags: `if N` / `setevent N` / `clrevent N` are events; `set/add/sub V, n` and `ifcmp V, n` / `discmp V, n, Llow,
  Lhigh` are variables (`discmp` jumps to the first label when V < n, otherwise to the second / falls through).
- `enterfight 0, a, b, c, ...` fights ARS monsters 3-3-a/b/c; `initfight` sets an area's random encounters.
  **Many story fights use unrelated monster records** (Li Qingzhao's fight shows "Peddler"; see glossary).
- Dedupe: `dump.py` shows a repeated line once; the six sect-head scenes, the shop lines and the reward
  messages are shared, so the first translation is copied everywhere. 只有夺她的令牌 (Li Qingzhao, Yu Hongru: both
  female) and 只有夺他的令牌 (the other four) are separate rows.

## The hero (1-1-1, 1-1-20)

Opening (1-1-1): two timemsg lines ("Caizi Studio's full version of Heroes' Altar takes you into a virtual
game world"), then the intro scroll in the first person: "Before this happened I lived a calm, slightly dull
life... the moment I pressed the button I activated the space-time device of the Heroes' Altar of the ancient
continent... I learned the place was called Safehaven, and when I looked at myself I found I had become a
fourteen-year-old boy! Is this a furnace that forges heroes or fertile soil for demons? I don't know." Then
"开始游戏之前，请先确定你的身份" ("Before you start, choose who you are") and the menu:

| choice | name | var 0 | actor | element (start 25) | Snowpeak mentor (1-4-1) teaches |
|---|---|---|---|---|---|
| 1 | 独孤圣 Dugu Sheng | 1 | 1 | Fire (var 38) | Clean Spell, True Fire, Meteor Rain, Inferno |
| 2 | 欧阳剑 Ouyang Jian | 2 | 2 | Wind (var 35) | Warm Mist, Cloud Body, Dust Gale, Heaven Gale |
| 3 | 唐静 Tang Jing | 3 | 3 | Earth (var 36) | Flying Rock, True Guard, Earth Grace, Avalanche |

- The choice only changes the starting element, which mentor will teach you, and which actor gets stat and
  spell rewards (`ifcmp 0, ...` branches everywhere). There is **no other story difference**.
- **All three are the same boy**: 少年 in the intro, 小伙子 / 小子 / 少侠 from NPCs, "你小子" from Bingyan, and the
  villain mocks him for leading girls (MM) to their deaths. 唐静 sounds like a girl's name but is "he". The hero's
  name never appears in dialogue except the mentors' "我是欧阳剑导师" ("I'm Ouyang Jian's mentor") and the refusals
  "你不是欧阳剑!" ("You're not Ouyang Jian!"). Write the hero in second person in messages, first person in his
  lines; "he" if needed.
- He knows he is in a game-like world and talks like a 2005 netizen: "靠!", "汗~~", "晕死!", "偶" for 我, "嘎嘎";
  cocky to villains ("小样我还对付不了YOU!"), whiny with Chai Zi, greedy ("好,我要发财了").

Start (1-1-20, the hero's house): the kid **Prodigy** (小神童) introduces himself as "the adapter of this game" and
**Chai Zi** shoves him aside ("Shit! You stole my line! Hand over the Sect Codex and scram!"). Chai Zi gives the
**Sect Codex** and explains: when you started the time machine, a great demon came through too and took control of
the six great sects; defeat the six sects, put the sect heads' tokens into the time machine on the right of your
room, and the demon will be forced out; kill it and you can go home. Choice "Who is the demon?" / "Is it that
serious?" (the first adds 2 to var 50, see Endings). Starter pack menu: 1888 RMB / manuals (Fist Book, Blade Book) /
super medicine (Big BBQ x5, War God x5, Cosmos x5... ) / starter gear / low-level magic (Basic Sword, Basic Staff,
Bloom Whip). Then "System: OK, start your journey, have fun!" - "Player: Why does this sound so familiar????" -
"...copied from the opening of 纯蓝." - "Player: I'm gonna puke~~ ? Where'd everyone go?"

## Characters and voices

| who | where | voice |
|---|---|---|
| Chai Zi 柴梓 | everywhere (tag `柴梓:`) | the author as a character: bossy, mocking, rescues you, cheats you ("deducts 1000 RMB and some stats" for oversleeping), self-aware ("I'm the current board moderator, why didn't you ask me?"). Dies in the Demonspire, returns as a ghost |
| Yuxin 陈雨馨 (pic 4) | joins 1-1-18 | orphan girl kidnapped by the possessed Gu Yanwu; spunky, bossy, cute ("本女侠" = "yours truly"; "不嘛,我要,给我撒" whiny); threatens the Soldier ("Don't argue with him, just kill him!") |
| Bingyan 赵冰雁 (pic 5) | joins 1-11-2 | a girl from the hero's real world who used his time machine; snappy ("滚!敢打搅本姑娘,就是死!"), bickers with him like a schoolmate; family secret: equipment forging |
| Archdemon 大恶魔 / ??? / 我是谁 | 1-1-3, 1-1-18, 1-6-2, 1-10-1, 1-255-32, 1-1-17 | sneering villain, then reveals he is the evil half of the hero's own heart |
| Gu Yanwu 顾炎武 | Safehaven | learned schoolmaster ("Work hard! Off you go!"), sells lessons, level-ups, qi refills and the Dream Cape; while possessed he is a sleazy "hypocrite" ("小样,敢碰我女人?") |
| Elder 村长 | Safehaven | old man errand-giver ("老夫不是叫你去...了吗?" "Didn't I tell you to...?") |
| Matron 中年妇人 | Safehaven | polite fetch quests in humble 妾身 |
| Granny 老婆婆 | Safehaven | doddery; chores with rhyming work songs (1-1-19: keep them rhyming in English) |
| Pan Xiaolian, Butcher Hu, tailors, page boy, urchin, flower girl, Monk Daode | Safehaven | one-liners; tofu double entendre for Pan Xiaolian |
| Mr. Wenshi 闻世先生 | 1-9-4 | ancient know-it-all; appraises your stats, "Heaven's secrets must not be revealed..." |
| sect heads | six sect seats | one formula each: "滚!" ("Get lost!"), fight, "...看来我武功下降了......啊!......" |
| Soldier 官兵 | Yamen | corrupt, cowardly ("Ah! Heroine, I won't dare! 5555~~"), mutters threats |
| Inspector 巡捕 | Yamen | gruff ("我就是巡捕!看什么看!"); confesses the town's secret |
| forum cameos | see below | each is a BBK Club member playing himself; silly, greedy or preachy |

BBK Club cameos (the antidote chain and the treasure): **Xiaoyao** 逍遥 (former RPG-board moderator, sings a
Chinese Paladin song, "YES" - "Yes? What did you eat?" pun 噎死), **Deng Shiyu** 邓世禹 (info broker: "1000 RMB a
question... 10000 for everything, no discount!"), **Liang** 亮 (sends you to kill beasts, runs off "886"),
**Flatline Love** 爱情没心跳 (sermon on love), **SSK** (super moderator: "I can just edit my money"; "94不给你" = "just
not giving it to you"), **Bubble Pal** 泡泡友 (sells a fake elixir: "a pack of arsenic, two spoons of bezoar, a bucket
of horse dung...").

## Main quest

1. **Arrival** (1-1-20): Chai Zi's briefing, Sect Codex, starter pack. Quest log (1-0-9): "Full-version quest:
   return to the real world. Hint: find two girls."
2. **Safehaven errands** (optional, rewards): the Elder's chain (buy wine; take a letter to the Inspector - if you
   open it, it reads "Looks like this can't be hidden any more; better to make it public. - the Elder"; visit Monk
   Daode, the Old Tailor, the Cook, Ping Yizhi, He Tieshou, the Quarry Boss, Granny, the Snow Leopard, the Lone
   Bandit); the Matron's item fetches (Hide Coat, Hide Shoes, Cape, Hide Cuff, White Rose, Fishpole, Dagger, Shears,
   Hemp Rope, Jade Tofu, Pork, Drumstick; reward at Gu Yanwu's). The Inspector reveals "a great demon lives in the
   Hundred Flowers Array in Prodigy Park" and later teaches a secret move.
3. **Yuxin** (1-1-18, Gu Yanwu's house): she is held there; Gu Yanwu, possessed, attacks; something crawls out of
   him ("Kid, you got lucky this time"); it was all a misunderstanding; her parents are dead, she joins and teaches
   the **Lingbo Step** (accept "Yes, teach me!" +3 to var 51 / "No thanks" -2).
4. **The six sects** (any order): Flower Sect (Li Qingzhao, Jade Peak 1-3-5), Snow Sect (Rhett Butler, Snowpeak
   1-4-3), Red Lotus (Yu Hongru, Mt. Wuzhi 1-5-4), Wudang (Taoist Qingxu, Mt. Wudang 1-6-5), Bagua (Wang Weiyang,
   Shang Fort 1-7-8), Iga Valley (He Zhongyang, Icefire Isle 1-8-6). Each: "滚!" - "Looks like Chai Zi was right. I'll
   have to take her/his token." - choice Challenge / Leave - win: "...my kung fu has slipped... Argh!" and the
   token; lose: Chai Zi: "You'd better train some more." Leaving: "A gentleman's revenge can wait ten years. I'm
   outta here, 886!"
5. **The antidote side story** (Yuxin poisoned): on Mt. Wudang Bubble Pal sells an immortality elixir; Yuxin grabs
   it, collapses; "???: Hehe, one brat down." Chai Zi: it is Demon Powder; ask Xiaoyao. Chain: Xiaoyao (Prodigy
   Park) -> "ask that Deng kid" -> Deng Shiyu (Shang Fort, charges 10000, "actually I don't know, ask Liang") ->
   Liang (Snowpeak: skin a tiger for him; tigers ambush) -> "ask Flatline Love" -> Flatline Love (Wuzhi Cave: "SSK
   and I made it; you'll have to persuade him") -> SSK (Jade Room 1: refuses for fun, fights with his "brothers"
   and "guards", gets a stomach ache and hands it over; Chai Zi gives you half of SSK's fortune). Yuxin rejoins.
6. **The club treasure** (optional, 1-10-1/1-7-6): Deng Shiyu sells the Love Ring (10000); Xiaoyao trades the map
   and master key for it; the treasure in Safehaven is guarded (Treasure Guardian, then "???" and his men).
7. **Bingyan** (1-11-2): requires your own sect (found one via 1-0-9: Lv 30, fame 66, qi 50, potential 200, 30K
   EXP). She is in its rooms: fights you, recognises the hero ("You found my time machine too? Serves you right!"),
   joins, and teaches Forging if you have a Prism Silk. Choices: "Go look" (+2) / "Ask"; "Explain properly" (+3) /
   "Forget it" (-5); learning Forging -3 (all var 51).
8. **The time machine** (1-1-3, hero's home): insert the six tags (menu Flower Iga Snow Lotus Wudang Bagua
   Activate; "you can't go alone, take some girls!" if the party is short) -> darkness, the Archdemon appears ("You
   attack me while I train? No more mercy!"), knocks you out; Chai Zi's voice: "Don't be afraid, I'm coming."
   Yuxin wakes you. System: the Archdemon went to the Demon Cave, Chai Zi is locked in the Demonspire. Choice
   "Kill the demon first" (+2 var 50) / "Save Chai Zi first" (+1). Event 400.
9. **To the Demonspire** (1-1-17, Yamen): the Soldier wants 50K RMB for the teleport ("that costs me loads of qi").
   Pay, or refuse and Yuxin threatens him (+3 var 51) - he "obeys" but drains your qi and money to zero ("Damn, he
   used MY qi! My money!").
10. **Demonspire** (1-12-1): a mechanism needs **88 Body Parts** to reach the basement. Chai Zi, dying, teaches
    **Cash Cannon** and gives the **Quellblade**. Choice "Don't worry, I'm here" (+2 var 50; if var 50 >= 5 he
    passes on his power: all stats +10) / "......" (sets event 1999: bad ending). "Life and death are fated; our
    bond ends here." -> Demon Cave.
11. **Demon Cave** (1-10-2): the Demon Guard ("I'm not the Archdemon! I'm just training to become a demon!") -
    fight, he drops the **Fly Card**. Using it (1-255-32) pulls you into the Archdemon's space: "Now Chai Zi is
    dead too... I am the evil in your heart. I left your body when you crossed time; kill me and you kill
    yourself!" A scripted defeat; one girl dies saving you: **Bingyan if var 51 >= 50, otherwise Yuxin** ("She gave
    her life to save you. She said the demon is heading for the Demonspire." "But if it really is you...").
    Event 405.
12. **Final battle** (1-1-17 via the Soldier, at the Demonspire): messages "Fighting the Archdemon at the
    Demonspire / Congratulations on getting here / The grand finale / It depends on your earlier choices... /
    Ready to face it? / First, a commercial break." Players: "@#$%^#%^#!!!" Who Am I: "Who dares disturb my
    commercials?" Chai Zi's ghost seals the demon's power; the demon possesses the surviving girl (she leaves the
    party), then "Chai Zi: Freed! Let's fight together!" (both girls rejoin for the last fight - script quirk);
    "???: If I must die, we die together! I am your inner self!" ... "You killed your other half - how will you
    live!?" The demon fades and your body stops obeying you.

## Endings (1-1-17)

| condition | ending |
|---|---|
| event 1999 (you answered "......" to dying Chai Zi) | "You killed half of yourself and drift through the void... at the end of the universe you become subatomic soup and form a new universe." Player: "Damn, what is this nonsense." Chai Zi: "In short: GAME OVER!" |
| var 50 >= 5 (you cared: "Who is the demon?" +2, "Kill the demon first" +2 / "Save Chai Zi first" +1, "Don't worry, I'm here" +2) | Chai Zi: "Borrow my body, I'll send you back." You black out; "??: Chai Zi, stop sleeping in!" "(to self): I'm finally back!" "You returned to the future world, now named Chai Zi, and began a new life. The whole game ends here; thanks for playing." |
| var 50 < 5 | Chai Zi: "My power can keep you alive. I'm leaving. Take care." - "...I can't go back." "The story ends here; thanks for playing." (play continues) |
| losing the final fights | System: "The demon really is hard. You may end the game here; better luck next time." |

## Sandbox systems (what the menus and messages mean)

- **System menus** 1-0-6..1-0-9 (opened from items or the engine; the trigger is not in the scripts):
  1-0-6 Instant Transfer (teleport to Safehaven / Shang Fort / Jade Peak / Mt. Wuzhi / Icefire Isle / Mt. Wudang /
  Snowpeak / Prodigy Park / My Sect; costs qi); 1-0-7 pay-to-heal (500 RMB: 20% HP or 100 MP; Chai Zi: "Damn,
  you'd cheat the system? No money, get lost!"), forging (gold/silver/bronze/iron swords, robes, Panther, Quellblade,
  Quellstone, Purestone, Sky Silk, Drake Robe, Dragonbane, Deerslayer; "you threw some RMB in and it melted into
  junk"), check potential; 1-0-8 Dreamscape, qi training (check qi / meditate / heal with qi, with qi-deviation
  failure), fame, **bank** (A/B/C class banks, "10K per deposit, max 2M, no interest"); 1-0-9 allocate potential
  (100 potential -> +5 to one element), level up with battle exp (needs a Level Tome), quest log (story / sect /
  Elder / Matron), sect functions (found, recruit 100 disciples for 1000 RMB + 20 qi, view size, research an art
  for 1 year + 80 qi).
- **Age**: var 1 starts at 14; research and some training cost a year; 1-0-5 ends the game if you get too old ("You
  have lived too long - past your destined span; time to die of old age. Please start again.").
- **Qi** (内力, 0-100) vs **MP** (真气): separate; see glossary.
- **Notice board** (1-1-2, needs fame 10, 1000 RMB): Kill the tiger / Defeat the wyrm / Drive out the ruffian
  (each speaks: "Kill me? Bring it! (Translation: awoo awoo...)" - "Damn, what bird-talk is that! Kill!"),
  Throw a banquet (50K), Open a martial school (20K, Lv 20). Fame +1/+2 or "no one believed your notice".
- **Hero's bed** (1-1-3): sleeping shows ten "Two hours pass." boxes, Players complain, Chai Zi randomly gifts
  stats or fines you 1000 RMB ("Sleeping all day! No progress! How will you ever get back?!").
- **Granny's chores** (1-1-19): rhyming songs, reward 50 taels, 20 EXP, 10 essence; allocate essence to a skill
  (menu of 12 skills); 1-9-14 reports "Your <Skill> improved!".
- **Mr. Wenshi's appraisal** (1-9-4, 100 taels): age, talent, fame, forging, lightness, qi, parry, fist, sword,
  blade, staff, whip -> rank words (glossary ladders). His four books: Blade Book, Fist Book (for diligent
  training), Leech Art ("Got money? Here!"), Beiming (needs the Leech Art).
- **NPC look texts** (★ lines): MUD format "★X看起来约30多岁 ★武艺看起来初学乍练 ★出手似乎很轻" / "★带著：布衣 ★
  description". Keep the ★ and the three-part layout: "★X looks about 30. ★Skill: a novice. ★Hits: light." / "★Wears:
  Plain Robe. ★...". These are messages: 4 rows max.
- **Element arts**: element stats (Thunder, Wind, Earth, Water, Fire) gate the mentors' spells (Lv 5/12/20/30 and
  element 60/95/130/180) or buy all four for 200K ("Damn! 20% off!" - "Fine! 160K!"); the five element books teach
  the basic spells; Yuxin learns thunder at Shang Fort (EXP 2000/5000/8000/15000); Demonwing is a black art only
  a girl can learn.
- **Hexblade purification** (1-255-5/6): purify the Hexblade with Purestones (0-9 times), then fuse a fully
  purified Hexblade with a Quellblade on a Forgestone: the two sword spirits moan, monsters steal or you win the
  **God-Demon**.
- **Dreamscape** (1-11-3): Dream Guardians 1-5 and the Dream Boss offer level-N monster fights for battle exp; "no
  saving in the Dreamscape".
- **Nether** (1-2-1, 1-10-3): hang yourself with the Hemp Rope on the West Wilds tree ("This world is too
  heartless!"), the Nether Guard charges 2000 ("Even suicide costs money?"); he sells goods and ferries you to Nether
  2 / Mine 1 / Mine 2 for 1000 ("Stay in the underworld forever if you're broke").
- **King of Hearts** (1-11-2): bet money, potential, battle exp, EXP or a stat.
- **My Sect** (1-11-1): disciples greet "掌门好!", purge troublemakers for 2000 hero coins, discount pharmacy.

## Branching summary

1. Hero (1-1-1): element, mentor, reward actor. No dialogue changes.
2. var 50 (bond with Chai Zi): three choices decide the stat gift in the Demonspire and the good vs bittersweet
   ending; "......" to the dying Chai Zi gives the GAME OVER ending.
3. var 51 (Yuxin vs Bingyan): which girl sacrifices herself in 1-255-32 (and which one the demon possesses).
4. Small choices (believe the Beast or Chen Xiao, pay or threaten the Soldier, buy or haggle) change rewards and
   flavour lines only.

## Running jokes to keep

- Fourth wall: "Players" complaining, Chai Zi addressing the players, "a commercial break", "Since this is the demo
  version...", "this game has so many pointless characters", "Why does this sound so familiar?".
- Greed: every NPC overcharges ("10000 RMB, no discount!"), the hero haggles ("20% off?"), bank and casino.
- Item descriptions arguing with themselves: "(duh, it's not a belt)", "(it's not THAT heavy)", "Everything
  unknown (then don't write it!)", "Junk - who'd sell this?", "Junk weapon, essential for suicide".
- Gibberish translations: "(直译:嗷嗷呜...)" "(Literally: awoo awoo...)"; the ruffian's "translation" is the same
  sentence ("Hey, I can understand that!").
- Parody names (Rhett Butler, Tien Shrimp...) and the tofu double entendre.
