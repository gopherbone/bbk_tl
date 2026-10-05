# 英雄坛说 (Heroes' Altar) English v0.1 - QA playthrough notes

Build: frozen `work/yxts/playthrough/yxts_en_v01.gam` (byte-identical to `work/yxts_en.gam` of 20:52; never
rebuilt). Its text bank and renderer symbols were frozen next to it (`yxts_en_v01.bank.json`,
`yxts_en_v01.syms.json`, and the merged table it was built from, `yxts_en_v01.en.jsonl`), so the play hooks keep
working while `bbkrpg/fontpatch.py` changes. Route: `routes/yxts.en.route.jsonl` (ends at frame 515808 with a
route mark; `bbkplay --verify` on the frozen gam replays it to frame 515808 in 164 s, hash 0c9f7e9dce066c2d).
Hero: **Dugu Sheng** (Fire). Main story **finished** (good ending), then the other two endings and
the sandbox systems were played from snapshots.

## Where we are

- Good ending reached at frame ~223000 (route mark "good ending reached"): var 50 = 6 (Who's the demon? +2,
  Kill the demon first +2, Hang on I'm here +2), var 51 = 62, so **Bingyan** died in the Fly Card scene.
  The game then returns to the title; **Continue** loaded slot 1 ("Demon Cave", saved before the Fly Card) and
  the route continues as a sandbox tour (system menus, bank, Dreamscape, forging, shops, Wenshi, notice board,
  Granny, Prodigy Park puzzle, Nether, mines, treasure chain, Hexblade/God-Demon, item scrolls). It ends in
  Safehaven (Granny's house, 1-1-6) with the full party.
- Played from snapshots and discarded (text seen, not in the route): the **GAME OVER ending** (answer "..." to
  the dying Chai Zi, event 1999), the **bittersweet ending** (var 50 set to 3), losing the final fight
  ("System: The demon really is tough..."), the old-age death (Wenshi appraising age 105), the Ouyang/Tang mentor
  menus, killing a townsperson (Fight on the urchin).
- Party: Dugu Sheng, Yuxin, Bingyan; kept alive with `cheat3()` (HP/MP/ATK/DEF 999, **level 90 and agility
  200** - see "Battles" below).
- In-game save slot 1 "Demon Cave"; saved once and loaded twice (Game > Load and title > Continue).

## How to open the system menus (not in the scripts)

**DEL, then a direction** on the free map: DEL+DOWN = 1-0-6 Instant Transfer, DEL+RIGHT = 1-0-7
Pay-Heal/Forging/Potential, DEL+UP = 1-0-8 Dreamscape/Qi-Train/Fame/Bank, DEL+LEFT = 1-0-9
Potential/Level-Up/Quests/Sect. (The script opens on the key *after* DEL.) Worth adding to `docs/yxts/story.md`,
which says the trigger is unknown; players will need it (My Sect and Bingyan are only reachable through 1-0-6/1-0-9).

## Coverage

Measured like jy: drawn English matched against the frozen merged table (`yxts_en_v01.en.jsonl`); rows tagged
by poll() are EN-build script positions, not row ids. Seen ids: `work/yxts/playthrough/yxts_en_seen_rows.json`.

- **say 503 / 661 (76.1%)**, gut rows 1101 / 1544, all rows 1348 / 2243 (incl. the discarded branches and two
  "flag tours" below). By kind: message 342/546, choice 212/268, menu 30/32, timemsg 6/6, showgut 4/4,
  grs.name 95/168, grs.desc 92/162, mrs.name 14/54. Identical texts (ten "Two hours pass." rows etc.) count once,
  so the real figure is a bit higher.
- Flag tours (not player-reachable in one game, like jy's sect tour): the Elder's 11 random errands and the
  Matron's 12 random fetch quests (flags 298-331 set/cleared one at a time, plus the quest-log entries for each);
  Wenshi's appraisal ladders (age/talent/fame/forging/step set via vars 1/2/3/4/10/14); qi 0..100 and
  potential 0..200 readouts; the five element allocations. All flags/vars were restored.
- Not seen: Ouyang/Tang mentor requirement lines and the other heroes' Snowpeak arts (need the other hero;
  switching var 0 with Dugu in the party crashes with `RunErr:7`, as in jy); most forging outcomes (1-0-7, random,
  ~15 "you forged an X" lines); the King of Hearts' wins (random); Chai Zi's bed gift / fine (random, 2-3% each);
  Yuxin's "not enough EXP" thunder lines; the A/B-bank upgrade and interest paths; the Matron's "you don't have X"
  replies; the scene banners of most maps (setscenename 4/27, map names 1/46); most ARS names (never shown).

## Problems found (most important first)

### 1. Battle status pop-ups are still Chinese (image) - MAJOR

`images_yxts.py` redraws SRS 5-1-3..9 (攻防速毒乱封眠 -> ATK/DEF/AGI/PSN/CNF/SIL/SLP), but the battle draws its
pop-ups from **SRS 5-1-240..246**, byte-identical copies of the originals that are not redrawn (the frozen gam
contains the original 毒 bitmap only once, inside 5-1-243). Seen in game:
`shots/yx_battle_status_popup_chinese_PSN.png` (毒 over the hero after Gu Yanwu's / "Li Yebai" ARS 102 attack,
1-1-18), `yx_battle_status_popup_chinese_ATK_battleaura.png` (攻 after Yuxin casts Battle Aura 天罡战气, MRS
4-2-3), 乱 after Gu Yanwu's attack, 攻 over the final-boss Retainers (ARS 83). Triggers: MRS 4-2-1 Cloud Body,
4-2-2 True Guard, 4-2-3 Battle Aura (buffs), enemy attacks with poison/confusion. Fix: add (5,1,240..246) to
`SRS_IMAGES` (same `_icon` ops), rebuild.

### 2. Other leftover Chinese (images)

- The final fight's enemy spell (Retainer, ARS 83, "Who Am I" fight 1-1-17) animates the eight gates
  **休 生 伤 杜 / 景 死 惊 开** across the screen (`shots/yx_battle_eightgates_spell_chinese_montage.png`, 2nd
  row). Decorative; keep or redraw is a design call (calligraphy rule).
- Stats > Gear screen: the header image **穿戴** (top right) has no English (`shots/yx_stats_gear2.png`).
- "loading..." during Load is an (English) image; fine.

### 3. Renderer / layout (report only; not touched)

- **Highlight bar has no left padding**: in every menu/choice box the first glyph starts in the highlight's
  first column, so its left stroke vanishes into the margin ("Who's the demon?" reads "/ho's", "Yes, teach me!",
  "1888RMB"). A 19-character choice ("Is it that serious?") makes the box span the whole screen width
  (x 2..158). `shots/yx_choice_1-1-20_wide.png`.
- **Boxes of different sizes drawn over each other leave remnants**: the two Healthy Gaming Advice timemsg boxes
  after a load (box 2 narrower and centred: `<H`, `Sa`, `Lo`, `Be`... show on both sides,
  `shots/yx_healthy_advice_box2_remnants.png`), the last ending message over the 3-line one before it
  (`yx_ending_msgbox_remnant.png`), the Instant Transfer menu over its two messages (`yx_sys6_transfer_menu.png`).
  The original's boxes were the same size; the two worst are fixed in text (below).
- Item/shop description window: after a 2-line description, a 3-line one ("Cures Poison/Cnf/Sil/Slp for all.")
  leaves the old top row's pixels under the box's top border (`shots/yx_shop_desc_heartsease_garble.png`; same
  as jy #4).
- Portrait dialogue: the third row runs at full width, flush left under the portrait ("me!" in "Quick, save /
  me!"), `shots/yx_portrait_third_row_flush_left.png`. Probably intended; looks odd on short third rows.
- After choosing Guard in battle, one frame shows the Flee/Status remnant (`yx_battle_menu_remnant_after_guard.png`);
  redrawn at once, cosmetic.
- Good news vs jy: `message` boxes **do wait for a key** in this build ("Got: X", "Got EXP", look texts...).

### 4. Game / script bugs (original logic, not translation)

- **Antidote chain dead end**: Liang (1-4-3) checks events 610/611/612 (the Beast quest) before 622 (antidote).
  If you talked to Liang and finished the Beast quest before the antidote chain reaches him (natural order:
  Snowpeak sect head first), 611/612 stay set forever and he only repeats "Life is full of choices...", so Yuxin
  can never be cured. I cleared 612 to continue.
- Story bosses use strong unrelated ARS records (Gu Yanwu = "Li Yebai" Lv 88, 28888 HP; sect heads = "Peddler" /
  "Ping Yizhi" Lv 75, 33333 HP; finale Retainers 60000 HP, ATK 20000, spells that one-shot 999 HP). With a low
  level/agility *every* attack misses (that is why `cheat()` alone was useless here). Same in the original.
- Money is capped at 99999 by gainmoney, so the mentors' "Pay for all" (160K) can never be afforded legitimately.
- 1-0-7 Check potential: two thresholds test var 3 instead of var 40, so 70+ potential always reads "70-odd"
  (80/90 rows unreachable); the 120 row says 师门点 (translated as Potential).
- Demonwing (1-255-8): choosing Bingyan teaches Yuxin (actor 4 in both branches).
- Gu Yanwu's quest reward L_060a adds Earth +4 but says "4 battle exp".
- Wenshi's talent ladder compares var 2 with 20 six times (only 3 tiers reachable).
- Appraising age at 100+ (1-9-4) prints the old-age message and ends the game (also checked on load, 1-0-5).
- The Dream Cape check (`if 500`) is satisfied by *equipping* the cape (engine item event); buying it is not enough.
- Prodigy Park ring puzzle (1-10-1): 3 clockwise laps then 3 counterclockwise laps, then the monster fights
  (with event 314 from the Inspector's opened letter).
- Equip > who: the member list showed Dugu and Yuxin only with Bingyan in the party (maybe a cape restriction).

### 5. Text issues (fixed in `translations/yxts/parts/zz_qa.jsonl`, 34 rows, check.py clean)

- **Dedupe mistranslation**: 1-6-2@040e choice 给/不给 when Yuxin begs for the elixir was "Pay / Don't pay"
  (copied from the Soldier) -> "Give it to her / Don't" (`shots/yx_choice_1-6-2_pay_mistranslation.png`).
- **Dedupe mistranslation**: 用 in the Purestone (1-255-5@001f) and Prism Silk (1-255-41@0021) prompts was
  "Use qi" (from the qi-healing choice) -> "Use it" (`shots/yx_choice_purestone_use_qi.png`).
- Granny's three chore songs (1-1-19@036a/03be/0412): each verse line was wider than a row, so the 4-line rhymes
  wrapped into 6-7 broken rows over 2-3 pages (`shots/yx_chore_song_wrap.png`). Rewritten with lines that fit,
  2+2 per page ("\f").
- Healthy Gaming Advice box 2 (1-0-5@009c): one line widened ("Gaming addiction hurts you", 118 px >= box 1's
  110 px) so it covers box 1.
- Last ending message (1-1-17@083c): 3 rows / 136 px so it covers the previous 3-row message.
- Orphan last pages (one or two words alone on a page) shortened to one page: 1-1-20@03b2 ("want?"),
  1-1-17@06fa, @0960, @09b0, 1-9-3@0231 ("won't tell.", `yx_orphan_page_wont_tell.png`), 1-10-2@006b, @00f8,
  1-255-1@0003, 1-255-32@0104, 1-4-3@0544, 1-6-2@04ec, 1-3-6@04cf, 1-1-3@03c1, and the Matron's 12 fetch
  requests 1-1-8@0291..0495 ("...Could you help me / out?"). 37 such rows exist (list by `fit.pages`); the rest
  were left (accepted "double pages").

Not changed (judgement calls): battle reward "You earn N gold" (glossary keeps the engine's " gold" although the
game's money is RMB); "taels" where the Chinese says 两 (Granny's reward, Wenshi's fee, Gu Yanwu's lessons);
look texts use "*" for ★ (glossary asked to keep ★; the font may lack it). No Chinese text was seen in any text
box, menu, shop or status screen; the only Chinese on screen is in images (problems 1-2).

## Screens checked (screenshots under `work/yxts/playthrough/shots/yx_*`)

Title (New Game / Continue / Credits / Notice), intro timemsg + scroll, hero choice, dialogue with/without
portrait, choices, menus with 11-character items (Snowpeak mentors for all three heroes
`yx_mentor_menu_{dugu,ouyang,tang}.png`, Fist Book `yx_fistbook_menu.png`, Blade Book, weaver
`yx_weaver_menu_{top,bottom}.png`, King of Hearts `yx_kingofhearts_menu.png`): **no item clips or overlaps its
box**. Shops (buy list, Buy how many `yx_buy_how_many_dreamcape.png`, pawn sell list), inn, Instant Transfer,
Pay-Heal, Forging, Potential, Dreamscape (all 6 guardians, "Can't save now!" `yx_save_disabled_dreamscape.png`,
Return), Qi-Train, Fame, Bank (info, open C, deposit, withdraw), quest log, sect found/recruit/view/research,
Items Use/Equip, Stats status pages and Gear, Magic list, battle wheel / Rush-Item-Guard-Flee-Status / magic
list, learn popup, Save/Load slot lists (`yx_save_slots.png`, `yx_load_slots.png`), " Saving...", the load
sequence (`yx_save_loaded_box.png`, `yx_healthy_advice_box1.png`), all three endings, game over -> title.

## Battles and tools

Helpers: `work/yxts/playthrough/yxts_qa_helpers.py`, loaded with
`python3 tools/play/run.py --game yxts -f work/yxts/playthrough/yxts_qa_helpers.py` after
`BBK_PLAY_GAM=work/yxts/playthrough/yxts_en_v01.gam tools/play/restart.sh yxts --en` and `start()`. It pins the
renderer symbols (`pin_syms`), adds `sysm(n)`/`sysp(n, *path)` (DEL+direction menus), `tp(i)` (Instant
Transfer), `tkp(addr, *path)`, `adv_stop()`/`sel(i)`, `cheat3()`, `boss()`/`story_fights()` (sets the three
enemy slots' HP to 1 and MP to 0: HP words at 0x1840/0x1873/0x18a6), `give(t, i, n)` (inventory triples at 0x4a10,
item count at 0x1a95), `getvar/setvar` (script var N = byte 0x2d38+N), `door(tile)`, `walk_cells`, `wenshi(k)`,
`notice(i)`, `use_item(name)`.

- Pokes in the route: cheat3 (stats, level 90, agility byte +26 of the 75 6e 1c 00 block), enemy HP/MP in boss
  fights, 88 Body Parts for the Demonspire mechanism, 20 Cloth/Stone for the Prism Silk, Hexblade + Purestones,
  the 14 scroll items, flag 612 (Liang), vars 4/40/53 for founding the sect, qi refills before teleports.
- An earlier, looser enemy finder poked non-enemy memory once and caused `RunErr:7` after a won Wudang
  gathering fight (reproduced; without the poke the fight ends normally) - not a game bug. Random fights end
  normally with plain attacks.
- Keys: menus and choices often open with the cursor on the 2nd item when the key that triggered them is still
  held (market door "Go in / Fish"); check the highlight before ENTER.
