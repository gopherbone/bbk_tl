# 金庸群侠传 (Heroes of Jin Yong) English v0.1 - QA playthrough notes

Build: frozen `work/jy/playthrough/jy_en_v01.gam` (not rebuilt). Route: `routes/jy.en.route.jsonl`
(recorded by the play daemon; snapshots were loaded only onto ancestors, see "Route" below).
Hero: male (Huan Yinfeng). Sect: Huashan, Qi School branch (Sword School branch played from a
snapshot and then discarded). Main story finished (Mt. Hua summit, Dragonbane ending; the Nine Yin
ending was also played from the same snapshot).

## Where we are

- Main story **ended** at frame ~1046100 (script 1-4-7, map (4,1), Mt. Hua, flag 1009 set),
  then Yue Buqun's Violet Mist lesson (flag 121) - Huashan Qi line complete.
- After that, a "sect tour" for coverage (not something a player can do): with the sect flags
  (101/151/171/181/191-197) cleared and, for the female sects, flag 1 -> 2 swapped by `setflag`,
  I visited the courtyards of Lingjiu, Xingxiu (+ Ding Chunqiu, who taught five arts),
  Qingcheng, Xuedao, Emei, the Gaochang maze. Flags were restored at the end (101 and 1 set,
  other sect flags and the shared 182-186 cleared). Earlier tours of Wudang, Quanzhen, Ancient
  Tomb, Shaolin, Hengshan, Beggars and the Dragon altar were played from a snapshot and discarded
  (text seen, not in the route): a male hero talking to a female sect master crashes with
  `RunErr:7` (`attribtest 2` on the missing heroine), and a random fight at the Dragon altar
  (1-6-1) killed the 999-HP hero.
- Route ends at frame 1191331 on Mt. Emei (script 1-4-11, map (4,3)), with a route mark.
- Party: Yinfeng only, kept at 999 HP/MP/ATK/DEF with `cheat()` (HP/MP display cap is 999).
- One in-game save in slot 1 ("Yangzhou", Yangzhou outskirts, before the Mt. Hua ending), saved and
  loaded once successfully (Game > Load). Careful: the Game submenu remembers its cursor;
  one blind UP+ENTER picked Quit, which restarts the game at the opening poem.

## Coverage

Coverage is measured by matching drawn English text against `translations/jy.en.jsonl`
(the EN build's script addresses differ from the source row ids, so poll()'s `gut/<key>@<addr>`
tags are EN-build positions, not row ids; `tools/play/route_coverage.py` replays on the
Chinese gam and does not work for EN routes). Seen row ids: `work/jy/playthrough/jy_en_seen_rows.json`.

- say rows 568 / 851 (66.7%), gut rows 808 / 1338, all rows 978 / 1817 (counting only rows whose
  English text was actually drawn, incl. the discarded side branches).
- Not seen: the female hero's start and the female sects' masters (Hengshan, Ancient Tomb,
  Lingjiu, Emei), most master quest lines of the other sects (Beggars: northern map, five wines,
  Huang Rong's riddle; Wudang quiz/herbs; Shaolin...), the four altar Immortals' fights, the
  unreachable Palace Guard scene, shop "make it" branches in the cities not visited, and a few
  level-gated "You need Lv N" lines.

## Problems found (most important first)

### 1. `message` boxes do not wait for a key (renderer bug) - MAJOR

In the original the OS message box stays on screen until a key is pressed. In the EN build the
replacement `msgbox` in `bbkrpg/fontpatch.py` draws the box and returns at once (it ignores the
`mode` argument of the OS call), so the script runs on immediately:

- When the next command redraws the map or opens another box, the message is **never readable**
  (it is on screen for ~5-10 frames). Examples seen: 1-1-1 "Choose your hero" (the hero choice box
  draws over it before it finishes; compare `shots/jy_P1_intro_orig_message_waits.png` - original
  shows 请选择游戏主角 until ENTER - with `jy_P1_intro_en_message_skipped.png` and the 2-frame
  sequence `jy_P1_intro_en_msgbox_frames.png`); 1-13-1 "You are now a disciple of the Huashan
  Sect!" + "Got: Grand Pill" (`jy_P1_huashan_join_message_invisible.png`); casino "Paid 10 taels",
  "Too bad! You lost!", "Congratulations! You won!" (`jy_P1_casino_messages_flash_6frame_steps.png`,
  6-frame steps); 1-11-11 "Paid 20,000 taels in banknotes" / "Got Yue Fei's Sword"; 1-13-5
  "Sword School destroyed" / "You are now senior disciple of the Qi School!" / "Yue Buqun
  defeated"; 1-12-26 "Found the real Violet Mist Manual"; 1-12-29 "The Freaks have gone beyond the
  pass"; every "Got: <item>" from `gaingoods` (Dagger, Ring, Dragon Dew x6...).
- When the next command is a `say`, the message stays visible above the dialogue box by luck
  (1-5-1 "You reach the cliff top.", `jy_P1_cliff_message_left_under_say.png`).
- The intro "Got: Waystone" + scene name also never show.
Fix belongs in the renderer (wait for a key like the OS does, honouring the mode argument), not in
the translation. Battle result boxes (Got EXP / You earn / Got: X xN) and the learn-art popup are
drawn by other code and do wait.

### 2. Game bugs seen (script/engine, not translation; presumably also in the original)

- **RunErr:3 crash when using a material from Items > Use.** Selecting Raw Silk (top of the Use
  list) and pressing ENTER shows `RunErr:3` in the top-left corner and the emulator stops
  (`shots/jy_runerr.png` in Yue Buqun's room 1-13-1, `jy_runerr2.png` on Mt. Hua 1-4-7). Recovered
  by loading a snapshot. A player who tries "Use" on any crafting material will lose the game.
- **Palace gate never triggers** (1-9-11 tile 12, handler L_018f): the `if 163` / `if 114` checks
  come after `startchapter 9, 11`, which ends the handler, so the Palace Guard scene (rows
  gut/1-9-11@01a9..0258) is unreachable and flags 115/164 are never set (Ying Bailuo's Stone Fist
  and the Beggars' map quest are stuck). I poked 114 off / 115 on to continue.
- Yangzhou inn rumour (1-12-14, `if 113`) clears 113, which the Dali sword seller (1-11-11 L_041e)
  needs: if you hear the rumour first you can never buy Yue Fei's Sword (114 is already set, so the
  quest still continues). I set 113 again to see the seller's lines.
- The Mt. Hua summit note (1-5-12 "...only once you reach Lv 70") is not enforced: 1-4-7 runs the
  finale on entry whenever 1008 is set.
- Crafting at the Odd Jeweller (1-11-29 Holy Chain) consumed 3 Platinum and 100 taels, the
  "fight" ended with Got EXP 1 / You earn 1 taels, but no Holy Chain was given (drop failed).
  Smelting (Platinum x1 each) and tanning (Ox Hide x1) worked.
- Source data quirks visible in battle: the Wanyan Kang fight is ARS 95 (Cyclone Mei); the "Yue
  Buqun" fight at Repentance Cliff (both branches) is ARS 81-83 (Ex-Huashan/Ex-Wudang/Ex-Shaolin).
- The Capital inn refuses guests of Lv >= 10 ("Sorry, we're full"): original logic.
- Player lines written as `say 0` (no portrait): 1-9-14 "Master Taoist, what happened to you?",
  1-5-12 "You were right. I'll be going now. Bye-bye!", "Where?" (already noted in story.md).

### 3. Text issues

- gut/1-4-7@0285 and @0516: "the Contest of Mount Hua" - glossary 华山论剑 is "Mount Hua Summit"
  (1-5-12@036b uses it). Fix in `translations/jy/parts/zz_qa.jsonl`.
- 乌金矿 "Gold Ore" (GRS/6-14-16, 11-byte limit) smelts into 乌金 "Black Gold"; Squire Li/Liu
  "pay 500 taels for Plat Ore and 1000 for Gold Ore" reads as gold. Glossary decision; no fix
  proposed (no 11-byte name keeps both "black" and "gold"; "BlkGold Ore" would).
- Instructors ask for "a Ginseng Pill" (1-9-16@0146 and the other three) while the item is
  "Ginseng" (GRS/6-9-3, 11-byte limit). Understandable; left as is.
- Battle money line "You earn     1 taels" (engine string, number right-aligned in a 5-char field,
  no singular). Cosmetic.
- Dialogue paging leaves single words on a page (e.g. 1-9-16 "learn?", 1-9-26 "taels.",
  1-13-1 "been there.", 1-4-7 "me!"). Accepted ("double pages OK").

No Chinese text was seen on any screen in this playthrough (menus, shops, status, battle, world
map, save/load, title all English).

### 4. Rendering

- Items > Use: moving from a 3-line description (Waystone) to a 1-line one (Ginseng) leaves stray
  pixels just under the description box's top border and a gap in the border's right end
  (`shots/jy_m_items_use0.png`). Cosmetic.

## Screens checked (screenshots under `work/jy/playthrough/shots/jy_*`)

Title (New Game / Continue), intro poem + hero choice, scene banners, dialogue with/without
portrait, choice boxes, shops (buy list, Buy how many, sell list), inn, coach (Where to? chain),
escort, casino, instructors + "Yinfeng / Learned / <art>" popup, blacksmith/weaver/hunter/tailor/
jeweller/swordsmith (recipes), main menu (Stats/Arts/Items/Game), Status pages 1-2, Gear, Arts
list ("MP cost:"), Items Use/Equip, Game submenu (Load/Save/Setup/Quit), Save Game / Load Game
slot lists (slot shows the scene name "Yangzhou"), " Saving...", battle wheel, battle results
(Got EXP / You earn / Got: X xN), "Yinfeng levels up!", world map (Waystone > Examine:
abbreviated English labels), game over -> title.

## Game facts for replaying

- Male start: Capital (9,1). Fights in the wilds are random; with `cheat()` every fight is won by
  UP+ENTER. Peach Blossom Island randoms (Royal Lama, Royal Guard, ... ARS 75-80) and Cyclone Mei
  hit hard enough to kill a 999-HP hero over a long walk: heal every round (my `_fight3`).
- Escort cargo (event 8/9/10/11) blocks the coach ("too much cargo") until delivered on foot.
- Coach tickets: Capital 1 Xixia, 2 Dali, 3 Yangzhou (800 each; buy at the station, then
  Take coach > Where to? > city/Next city chain). General stores sell Waystone (1500),
  Note 1000, Note 2000 (the list does not start on the Waystone in Xixia).
- Counters are triggered by walking into them; the bump itself opens the box, so an extra ENTER
  picks the first choice.
- Waystone "Use" returns to the area's city; "Examine" shows the world map. Not available
  where the script has no event 255 (rooms, Peach Isle 1-5-3, Peach Cave 1-5-12).
- Snow Peaks (1-5-7) is split; go through the Snow Cave (1-5-11, ore/charcoal fights) to reach
  Flower Vale (1-5-8, tigers drop Tiger/Ox/Snake Skin). Flower Vale's only way to Xixia is the
  Waystone.
- Huashan chain (male): Yue join (101, Lv>=11) -> Liang Fa Lv21 (102, Heartland bandits 103, Hua
  Sword 104) -> Lu Dayou Lv31 (105, Tiger Skin -> Tiger Fist 106) -> Ying Bailuo Lv41 (107, Dragon
  Dew -> Prime Palm 108) -> Yue (109) -> Capital inn Talk (110) -> Yue key (111) -> Repentance
  Cliff = Huashan courtyard tile 6 (13-5). Qi branch: 112 -> Ying Lv51 (113) -> Yangzhou inn
  rumour (114) / Dali seller (10 x Note 2000) -> palace (broken, poke 115) -> Ying Stone Fist
  (116) -> Yue Lv61 (117) -> Yangzhou Lao Denuo (118) -> Yue (119) -> Yangzhou (120) -> Yue
  Violet Mist (121). Sword branch: 140 -> Cheng Buyou Lv51 (141, needs a Zhenwu -> Fatal Trio
  142) -> Yue Lingshan Lv61 (143) -> Lu Dayou (144) -> Mt. Hua herb gatherer (145) -> Linghu
  (146) -> Feng Qingyang Dugu Nine (147).
- Main quest: Yanmen (1001) -> Yangzhou Ke Zhen'e (1002) -> Yanmen cliff, Cyclone Mei (1003) ->
  Capital instructor building = tournament (1004) -> Capital inn Wang Chuyi (1005) -> Ping Yizhi
  in Xixia (18, six herbs from the herb gatherers of Mt. Song/Heng/Wudang/Zhongnan/Hua/Emei ->
  6 Dragon Dew) -> Capital inn (1006) -> Dali Guiyun Manor = talk to the NPC (1007) -> Yangzhou
  outskirts boatman -> Peach Isle -> Huang's home -> Peach Cave Zhou Botong (1008) -> enter Mt. Hua
  (finale vs 3 Ouyang Feng, 1009; random Nine Yin / Dragonbane).
- Inventory: (type, index, count) triples from 0x4a0f; memory writes land on the next frame
  (read-modify-write twice in one frame loses the first).
- Battle detection: the key-wait stack has `3112d3083856` + `12d3e7xx` as its 3rd frame in battle
  (dialogue `12d3e21f`, choice `12d3ee80`); `wheel_shown()` alone also fires on the learn-art popup.

## Tools

Helpers for this session: `work/jy/playthrough/jy_qa_helpers.py`, loaded into the daemon with
`python3 tools/play/run.py --game jy -f work/jy/playthrough/jy_qa_helpers.py` (it patches
`play.poll`/`play.fight`/`play.in_battle`; its `SP` path points at a scratch dir - change it). EN text
coverage by matching drawn text to the translation table, auto-screenshots at each key wait,
`tk(name)` / `ch(i)` / `tile_talk(tile)` (choice-aware dialogue), `go("C-N")` (walk to the tile
whose handler starts script 1-C-N), `waystone()`, `setflag(n)`, buy helpers.
