# 伏魔记 agent playthrough — notes

Route: `routes/fmj.agent.route.jsonl` (stopped cleanly after session 5, ends
at frame 894182, ~248 min game time; `bbkplay --verify` hash f6ae9da0eb91a8bf).
Coverage of the route (`tools/play/route_coverage.py` -> `route_seen.json`):
269 / 632 `say` rows (42.6%), 285 gut rows. `seen.json` is cumulative over all
attempts incl. rewound ones (also counts GRS/MRS names/descs).

The three emulator bugs found in session 1 (IRQ I flag, save-marker overwrite,
auto power-off) are fixed in the official `bbkemu/target/release/bbkemu`;
`work/bbkemu_irqfix/` and `emu_fixes.patch` are obsolete.

## Session 4 blocker: fixed

The OS-flash-write bug (Emulator problems #3) is fixed in the official build
(commit "core: flash writes use the same address map as reads"). Session 5
verified: `deleteactor 2` in 1-3-12, the solo 蛇妖男 fight, `createactor 2`
(小梅 restored from the OS file in 1-3-11), an in-game 存储进度 save and a
读入进度 load all leave the game image byte-identical to the .gam (0 bytes
differ over the whole 832 KiB). In-game saving is safe now. The session-3
"double level-up / exp < 1105" rule was a misdiagnosis: ignore it.

## Where we are (end of session 5)

- Route ends at 霸王钟洞口 (script 1-8-2, map (1,35), tile (11,3)) on the
  free map, right after 冲虚道人's speech (event 224 set: 霸王钟 stolen by
  赤血, 袁萍芷 gone). In-game saves: slot 1 = 建业城 (before 钟山), slot 2 =
  here. Party 柳清风 Lv15 (HP 310/342, MP 276/276, atk 210, def 82) +
  慕容小梅 Lv12 (HP 207/214, MP 275/285). Money 2589. Coverage/verify: see
  the top of this file and the session-5 report.
- **Next**: 8-2 tile 1 -> 钟山道院 8-1 -> tile 1 (224 set) -> 6-12 -> back down
  the 6-8/6-9 bridges -> 6-13 -> 6-4 -> 6-1 hub -> 建业城 (7-1, tile 1 enters
  from 6-2 with 104, or 6-1 tile 1 with 106) -> 建业客栈 7-2 counter (tile 5):
  掌柜 sets 225 (袁萍芷 went toward 白水镇) -> 6-1 hub -> 白水镇 (chapter 9,
  events 226-234). If 1117 is set (we returned the money bag), the 7-2 init
  ambush fight (3 游人, ARS 9/20/26) triggers on entering the inn unless 221 is
  set (it is): skipped now.
- Story flags (setevent): 217 小梅 rejoins (1-3-11), 218 建业城 thief scene
  (1-7-14), 219 小雷公 / 袁萍芷 joins (1-8-11), 220 参虚阁 fights (1-8-3), 221
  赤血 (1-8-12), 224 冲虚道人 (1-8-2), 225 inn keeper (1-7-2), 226-234 白水镇
  (chapter 9), 235-246 周处庙/北海 (10, 12, 13), 247-250 酆都 (11), 251-254
  陵墓/鹤鸣山 (14), 255-259 摩天顶 2-32 (endgame back at 三清山).

### Session 5 route (frame 537510 -> ~894200)

1-3-12 `deleteactor 2` (no crash) -> solo 蛇妖男 (the session-4 line did
*not* repeat: the boss heals itself on this RNG; new line found by beam:
无影神针, 火灵符, 剑气术, 观音符, 土灵符, 风灵符, 水灵符, 玉蓝草, 水灵符, 千里飘,
雷灵符, 雷灵符, 玉蓝草, 剑气术 x3) -> 野外斜路 talks -> 2-43 -> bridge maze up ->
三清宫 talks -> 无机阁 (216) -> maze down -> 原野 maze (`mwalk`) -> 忘忧村:
东东家, 蔡婆家 (gift 七星灯, 222), 村长家 -> 慕容主房: 小梅 rejoins (217,
`createactor 2` restores her stashed stats) -> 原野 -> 2-50 tile 3 ->
startchapter 6,1 -> ch6 hub maze -> 7-14 小偷袁 fight (1500 HP; lost once
to auto-attack = game over; beam win with 剑气术 + 迷魂香/忘魂花 sleep) ->
建业客栈 talks -> 建业城: 钱袋 box (chose 奉还, 1117), shops browsed
(武器店, 杂货铺, 当铺, 药铺; bought 5 魔王甲, 4 玉蓝草), 民宅3 阿军 (情书 ->
3 万能钥匙, 264), save slot 1 -> 6-1 -> 6-4 -> 8-11: 袁萍芷 joins, 3x 小雷公
(lost once to auto-attack; game over -> 读入进度 slot 1 is in the route; then
beam win as a trio) -> 6-8/6-9/6-12 -> 钟山道院 8-1 (box, 炼丹房, 冲虚居,
药房 browsed + 2 魔王甲) -> 参虚阁 8-3: three chained fights (高粱酒坛+雷/风蜘蛛,
火/土/冰蜘蛛, 怪妖坛子+大头怪+小可爱) won by a staged trio beam (~50 rounds) ->
8-12 cut-scene -> 赤血 (8000 HP): **losing is scripted** (both enterfight
labels continue at L_043d; only the win line gut/1-8-12@040f is missed) ->
袁萍芷 leaves -> 霸王钟洞 -> 霸王迷宫 8-9 (4 of 6 boxes: 雄黄, 枸杞仙果,
还神丹, 飘飘香; (27,43) and (10,41) skipped) -> stairs (43,19) -> 8-2 (224).

### Older history

- Session 4 did: diagnosis only (the crash), plus the 1-3-12 opening says
  (0060-0158). Repro: `routes/repro/flash_save_corrupts_gam.script.jsonl`.
- After 1-3-12: `say`s, 忘忧坟场/村 scenes, tile 2 -> 2-43 (三清山入口) -> back
  up the mountain (bridge maze, `maze_walk`) to 无机阁 1-2-2: talking to
  无机子 with 215 set sets 216 (钟山 request) = end of this story arc; 2-50
  tile 3 with 216 -> `startchapter 6,1`.
- Session 3 did: 毒瘴林入口 box, 瘴气 message (203), 猎人居 hunter (204),
  原野 maze -> 石梦城 (1-5-x): all NPCs, houses, 药店/杂货店/武器店/当铺
  browsed, 鲁斧 (208), gate guards fight (209), 李府 rooms + boxes, 李虎 boss
  (210; 芦藤雌甲/雄甲 + 金色钥匙), 老王 spared (211), 东厢房 with the key (小画家
  rescued, 214), 老王家 (212), 鲁斧 again (223), 密道 -> 李府宝库 (all boxes,
  +1000 money), stat items used on the hero, 6 玉蓝草 bought; 原野 maze ->
  1-4-1 -> 森林道路 1/2 -> 人蛇窟入口 -> 蛇窟山洞 1 (boxes 21-29, then tile 3
  -> 蛇窟隐洞 1-4-10 boxes) -> 蛇窟山洞 2 (all boxes) -> 蛇窟山洞 3: 蛇妖 boss
  (215) -> box 22 (behind the moved 挡路石) skipped on the final line to avoid
  exp -> 蛇窟宝洞.
- Skipped: 忘忧村 revisit (小画家 back home: new 蔡婆 lines?), 1-4-6 box 30
  (21,36) (it sets 1055, which also disables the 蛇窟隐洞 entrance: either/or),
  1-4-8 box 22 (佛天圆) on the final line, 石梦城 杂货店/武器店 purchases.

## Game/script facts found in session 5

- The battle RNG is not a pure function of the in-battle actions: the
  session-4 winning line vs 蛇妖男 gave different damage here (the boss also
  healed itself, 1418 -> 1638). Re-search each time the pre-fight route differs.
- Party members: 3rd member 袁萍芷 (Lv9, 250 HP, attack only; LEFT+ENTER on her
  wheel just attacks). Heap stat blocks `75 6e 1c 00` also exist for non-party
  data; `party()` now filters by sane level/HP.
- Magic lists (battle LEFT): 柳清风 0 气疗术, 1 御剑术, 2 天师符法, 3 凝神诀,
  4 剑气术 (30 MP, "攻击敌方全体", ~180-280 to each enemy), 5 卸劲诀 (Lv13).
  慕容小梅 0 观音咒 (150), 1 金刚咒 (def +50% 5 rds), 2 苦口婆心 (confuse 5
  rds), 3 还魂咒 (revive), 4 血魔噬主, 5 马师皇针灸, 6 御风行, 7 乌手术,
  8 凝神归元 (heal 220), 9 净衣咒.
- Good buys: 魔王甲 (Mp+250, 750 at 建业城药铺 / 钟山药房) = 8 剑气术.
  GRS record: +0x12 buy price, +0x16 hp effect (items/throwables),
  equipment +0x18 def, +0x19 atk, +0x1b speed (BBKRPGSimulator BaseGoods).
- Enemies: 小偷袁 (ARS 20) 1500 HP hits ~250; 小雷公 (14) 800 HP; 参虚阁
  wave 1 ARS 48/50/51, wave 2 52/53/54, wave 3 55/57/58 (700-1440 HP);
  赤血 (18) 8000 HP atk 350 (meant to be lost). 霸王迷宫 randoms (恶猩猩 25,
  毒蜘蛛 49, 护灯兽 10, 小蜈蚣 22, 小火怪 13) kill a Lv14 duo: **flee them**
  (`play.FLEE=True`; 逃跑 worked every time).
- Game over -> title. The title menu cursor remembers 再续前缘 after a load,
  so `adv()`'s ENTER spam after a game over silently loads the last in-game
  save (or starts a new game when the cursor is on 新的故事). Always check
  `party()`/`mapid()` after a long auto walk.
- 1-3-1 (忘忧村) tile 2 needs 217 once 216 is set ("先去看看小梅"); 原野 maze to
  chapter 6: reach 2-50 with event 102 (2-46 tile 2 with 104), then tile 3.
- The ch6 hub (6-1..6-7, flags 101-113) reaches 7-14 (建业城 first visit,
  sets 218) via 6-1 t2, 6-3 t2, 6-1 t2, 6-4 t2, 6-2 t2, 6-7 t2, 6-1 t2, 6-3 t2 x2,
  6-4 t2, 6-2 t2; 钟山 via 7-1 tile 2 (sets 105) -> 6-1 t2 -> 6-4 t2.
- 1-7-1 box 21 (钱袋): choice 不给 = fight 3 游人 (1118); 奉还 = lose 250 money
  (1117) and the 游人 ambush in 1-7-2 later (only while 221 is unset).
- 8-9 霸王迷宫 tiles 1-13 have no script handlers; tile 11 -> 8-10, tile 14
  (the 迷宫楼梯 object at (43,19), walk DOWN into it from (43,18)) -> 8-2.

## Game/script facts found in session 3

- `if 2000` / `if 2001` in 1-4-1: equipment GRS +0x84 is an event id set
  while worn (BBKRPGSimulator `BaseGoods.EventId`): 芦藤雌甲 = 2000 (小梅),
  芦藤雄甲 = 2001 (hero). Both must be worn to enter 瘴气林.
- Game bugs: 1-5-20 (李府下房) box 25 sets event 1065, which 1-4-10 box 2
  also uses, so that 蛇窟隐洞 box is always "taken". 1-4-7 box 21 sets 1056
  but init checks 1057 (harmless).
- 李虎 (ARS 3-3-9): learns 7 magics incl. 凝神归元 (heals ~200) and 五雷轰顶
  (all, 250); immune to 封 (buff byte 4). 蛇妖男 (3-3-5) immune to 眠 (8).
  Monster magic chain: ARS +0x2f -> MLR (12,1,n); +0x02 = number learned.
- Physical attacks always missed 李虎 (spd 50). Thrown 雷火珠/袖里剑 (250),
  无影神针 (400), 灵符 (风170 雷150 水160 土180 火200), 剑气术 (30 MP, 200-280),
  天师符法 (13 MP, ~160) are what work.
- Level table: MLR (12,2,1) hero / (12,2,2) 小梅, 20 bytes per level:
  +0 maxHP, +4 maxMP, +8 atk, +10 def, +14 next-level exp, +16 speed,
  +19 number of magics known.
- Enemies in random fights can be fled: wheel DOWN, ENTER, DOWN x3 (逃跑), ENTER.

## Battle tooling (session 3)

- Party fights: the hero's sword hits a group (UP, ENTER: no target step);
  小梅 needs a target (`A_ATK(ix)` = UP, ENTER, RIGHT*ix, ENTER). After the
  hero's command 小梅's wheel shows at once; the round runs after the last
  command (`act_as`, `duo_round`). Magic on an enemy `A_MAG(idx, ix)`; on a
  party member: target starts at the caster, LEFT/RIGHT moves.
- 封 (seal) makes LEFT+ENTER on the wheel do nothing (magic list won't open);
  the status screen (DOWN, 状态) shows 攻防身毒乱封眠 counters.
- In-battle dialogue (enterfight events 39/40) appears as a key wait without
  the wheel; `duo_round` ENTERs through it.
- `duo_beam(target, hero_cands, mei_cands, value)`: beam search over rounds
  (RNG depends only on the action sequence). It explores by loading sibling
  snapshots, which corrupts the recorded route (see Emulator problems), so at
  the end it reloads the root (an ancestor) and replays the chosen actions:
  only that replay ends up in the route. `duo_greedy` (one-round lookahead)
  also only loads ancestors. Never `snapshot.load` a non-ancestor and then
  keep playing.
- Map menu helpers: `equip(name, who)` (物品/装备 list), `menu_use(name, n,
  who)` (物品/使用 list), `map_heal(target, times)` (小梅's 观音咒, 10 MP, 150),
  `shop_buy(tile, {name: n})`, `money()` (u16 at 0x1a8f), `battle_list()`.
  Item lists: the first key after a list draws is dropped; a list end draws
  nothing (`equip_list_goto` tolerates one missed key).
- `tools/play/rebuild.py`: re-records a known-good prefix of a route through
  bbkemu's own recorder (route.record resume=False + input.press/release/
  route.mark at the same frames). Used twice this session to cut the route
  back after the problems below; the result is byte-identical to the source
  prefix. Old routes kept for the repros: `work/playthrough/
  broken_session3.route.jsonl`, `work/playthrough/hang_3_12.route.jsonl`.

## Emulator problems (sessions 3-4)

(1 and 2 are fixed in the current build: snapshot.load restores the route
exactly; an undefined opcode stops the run with reason `illegal_opcode`.)


1. **snapshot.load truncates the route by event count only.** Loading a
   snapshot that is not an ancestor of the current state keeps the wrong
   events. Minimal repro (`bbkemu --script`): load_gam; route.record
   (new file); run.frames 100; snapshot.save A; input.tap LEFT; snapshot.save
   B; snapshot.load A; input.tap RIGHT; snapshot.load B; route.stop -> the
   route says `{"f":100,"k":"RIGHT"}` while the state is B (after LEFT).
   The 李虎/蛇妖 beam searches of session 3 first produced routes whose replay
   lost the 李虎 fight (and went to game over -> new game).
2. **Undefined opcode $9B hangs run.frames forever.** Replay
   `work/playthrough/hang_3_12.route.jsonl` (load_gam, input.replay run:false,
   run.frames 566586) and `run.frames 1` never returns (100% CPU); `run.until`
   with max_instructions shows PC stuck at $f5ae (phys e275ae, byte $9b) with
   0 frames advancing. Cause upstream: OS routine at phys e8a48b loops x=$a5
   times bumping $0c/$0d/$0e; when $0d reaches $27 the $f000 window (bank
   index 15) switches from e8a to e27 under the running code, which then runs
   data. Session 4 found the real cause upstream: problem 3 (the engine code
   was already corrupted by the OS file write at `deleteactor 2`), not the
   double level-up.
3. **Flash program/erase addresses were shifted by +0x8000 (FIXED in commit
   "core: flash writes use the same address map as reads"; verified session 5).** `core/src/memory.rs`: `read_flash` rotates only the last
   32 KiB (`addr >= FLASH_SIZE - 0x8000`), but `write_flash` applies
   `(addr + 0x8000) % FLASH_SIZE` to *every* byte-program and sector/block
   erase. The OS file system lives below the game (flash 0x5000-0xcfff, phys
   0x205000-0x20cfff; the game is at 0xd000), so its writes land 32 KiB higher,
   inside the game image (gam offset = flash addr - 0x5000), while the OS
   reads back unchanged 0xff (so it re-formats on every write). One file
   write erases gam 0x0000-0x0fff (header + engine code) and 0x6000-0x6fff and
   sets gam 0x30ff to 0x03 (also: a byte-program assigns instead of AND-ing).
   Minimal repro (`bbkemu --script routes/repro/flash_save_corrupts_gam.script.jsonl`):
   replay the agent route to frame 26800 (三清宫), EXIT, DOWN x3 (系统),
   ENTER (存储进度), ENTER, ENTER (save to slot 1), 200 frames: `mem.read gam
   0x30f8 len 8` goes `18a52069d38520a5` -> `18a52069d3852003`, gam 0x0 goes
   `47414d00...` (`GAM\0`) -> `ffff...`, while `phys 0x2080f8` (where the OS
   wrote) still reads `ff`. In the playthrough the same happens at frame
   ~537560 when 1-3-12 runs `deleteactor 2` (OS file call from engine code
   at phys 21c245, `jsr $d2f6` with $26/$27 = e9e9, filename built from
   "伏魔记" at 0x1938); the crash follows ~1.5k-18k frames later depending on
   input (`illegal_opcode` at e275ae). Likely fix: in `write_flash` rotate
   only when `addr >= FLASH_SIZE - 0x8000` (as `read_flash`), and program as
   `flash &= val`. bbkplay shares the core, so **in-game saves in bbkplay
   corrupt the game too** (PLAYING.md says saving is fine; it is not with
   this build). The load_gam save-marker fix of session 1 was a symptom of
   the same mapping.

## Battle notes (session 2)

- The battle RNG does **not** depend on input timing: the same action sequence
  gives the same result whatever the frame delays. Different actions (or an
  extra round) change later outcomes. So save-scum by trying *different
  actions* per round (`try_actions` / `boss_greedy` in play.py).
- The command wheel: `UP, ENTER` attacks at once (no target step). The hero's
  physical attack sometimes hits 2-3 adjacent enemies. Vs 护剑神 alone it
  missed almost every time; magic and thrown items always hit.
- 道具 lists (投掷/使用) are re-sorted as items are used/gained: never use fixed
  indices, pick by drawn name (`A_USE_N(name)`, `A_THROW_N(name, right)`).
  The first key after a list opens is dropped unless you wait ~30 frames; list
  keys need ~26 frames each. Throw targets: default = first enemy, RIGHT moves.
- 护剑神 fight won by: buying 21 青阴君 (hp+150, 150 each) at 三清宫药房
  (walk back 伏魔洞->洞口->山道->浮桥->竹林->百草地->三清宫 tile 4, ~3 min),
  then: 天师符 on a beast, attack while HP >= 150, else 青阴君/气疗术 (whichever
  leaves more HP, chosen by trying both). Beasts died by round ~6; the boss
  then mostly dodged physical attacks; it fell to 风灵符 at round ~93. Level
  10 after the fight (+exp 950).
- Enemy stats are in ARS type 3 (`3-3-N`): +0x18 maxHP, +0x1a HP, +0x1c/+0x1e
  MP, +0x20 atk, +0x22 def, +0x24 money, +0x26 exp, +0x12 level, +0x13 speed.
- Shop UI: list -> ENTER opens 买入个数 (UP increments, screen lags one tap) ->
  ENTER buys. Counts start at 0 or 1; ENTER with 0 buys nothing.

## Game/engine facts

- Script keys `1-C-N`: `startchapter C, N` loads script 1-C-N. Chapter 2 = 三清山.
- Map tile events: tile event k triggers script event 40+k. Script events 1..39
  are object (NPC/box) ids, triggered by facing the object and pressing ENTER.
  Doors are usually unwalkable tiles: walk *into* them.
- Map `(a,b)` of `loadmap a, b, x, y` is MAP resource (2,a,b); x,y = view origin.
- Controls: ENTER = talk/confirm/advance; **EXIT opens the main menu** on the map
  (属性/魔法/物品/系统); PGUP/PGDN page the status screen. Walking: one tile per
  tap (hold 2 + wait 8 frames); holding does not repeat.
- Battle wheel: UP attack, LEFT magic, DOWN misc (围攻/道具/防御/逃跑/状态;
  道具 → 装备/投掷/使用), RIGHT 合击 (needs 2+ party members). The wheel
  remembers the last choice, so ENTER alone may open the magic menu.
- Game bug: 灯洞6 (1-2-24) box 22 at (28,5) runs `deletebox 21` (should be 22);
  if box 21 is already gone the engine shows `RunErr:11` and the game exits.
  The route skips that box.
- 灯洞3/7 (map 3,4) are split mazes: tile 3 at (7,6) teleports to the top part.
- Stepping *off* nothing triggers events, but paths must not cross other event
  cells (e.g. arrival on 竹林山道's tile 2): `goto` now blocks all event cells
  except the target.
- Flag mazes (三清山 bridges 100-128, 原野 101-105): `tools/play/maze.py`
  simulates the tile handlers from the .gut listings and BFSes (script, flags);
  `maze_walk("4-1", lo, hi)` re-solves after each step from the live flags
  (the simulator's prediction was off once; re-solving recovers).
- Game over returns to the title screen (and ENTER spam starts a new game).

## RAM (A4988 build, this engine)

| what | where |
|---|---|
| map id (a, b) | 0x1979, 0x197a |
| view origin x, y (player = origin + (4,3)) | 0x197c, 0x197d |
| map width, height | 0x197e, 0x197f |
| NPC/box records | heap blocks tagged `75 6e 20 00` in 0x3000-0x7fff: +4 kind (2 NPC, 4 box), +5 type, +9/+10 x/y, +11/+12 initial x/y, +13 name |
| hero stats | heap block `75 6e 1c 00` after the name block "柳清风": +6 maxHP, +8 HP, +10 maxMP, +12 MP, +14 atk, +16 def (u16) |
| idle/dialogue | OS key wait at phys 0xe9e317; hw sp 0xe8 = free on the map, lower = box/menu/battle |
| battle | key-wait call stack contains far-call frame `12d3e709` (random fights) or `12d3e33b` (scripted); command wheel visible ⇔ LCD RAM row 69 bytes 9-13 = ff |
| LCD RAM | 0x400 + 32*row |
| RTC / alarm / idle countdown | 0x234.. / 0x230.. / 0x2028 |
| script event flags | 0x2c04: event n = bit (n % 8) of byte 0x2c04 + n // 8 (`flags()`) |
| battle monsters | 3 records of 0x33 bytes at 0x1826 (ARS type-3 layout, HP at +0x1a); a dead monster's record is zeroed (`mons()`) |
| player tile | origin + (4,3) is wrong in maps smaller than the screen (view clamps); objects' +11/+12 follow x/y (not initial positions), so identify NPCs by record address (`talk_obj`) |
| money | u16 at 0x1a8f (`money()`) |
| hero record (0x35e4 this save) | after `75 6e 1c 00`: +0 level, +6 maxHP, +8 HP, +10 maxMP, +12 MP, +14 atk, +16 def, +18 exp, +20 next-level exp (u16) |
| 小梅 record | the next `75 6e 1c 00` block (0x36dc); `party()` reads both |
| equipment events | worn items with GRS +0x84 != 0 set that event (2000/2001 = 芦藤甲) |
| hero exp | +18 is exp *within the level* (reset by the level-up: 1911 -> 246 at Lv13), +20 next = 1965 at Lv13 |
| heap | 0x2c00-0x3fff, blocks `75 6e <u16 size>` used, `62 6e` free, `62 65` last free block; 0x2e38 (1940 B) = the 20x96-byte back buffer at 0x2e3c (`$1936`) |
| map object pointer table | 0x19d3 + 2*i -> NPC/box records (index = object slot) |
| OS file system | below the game in flash (0x205000-0x20cfff); directory byte at phys 0x2080ff. Writes are broken in bbkemu (Emulator problems #3) |

## Tools (tools/play/)

- Session 5 additions in play.py: `mwalk(goal, mask)` (maze solver with
  story flags in the mask; goal must be a maze node, e.g. "6-13" not "8-11",
  because script init code is not simulated), `send`, `pair(mei, yuan)` (trio
  battles through `duo_beam`'s mei_cands), `MEI_MAG(idx, side)`, `use_item`,
  `topup`, `safe_adj`. `party()` skips non-party `75 6e 1c 00` blocks.
  `fight()` now also answers a battle wheel shown while the CPU is outside the
  OS key wait (2nd member's wheel at pc 227d3c), which used to hang auto
  fights. For chained enterfights use a staged value in `duo_beam` (bonus per
  wave reached; otherwise finishing a wave looks like a loss). `duo_beam`
  returns None without replaying when no child survives: load the last kept
  `bmN` snapshot (`snapshot.list`) and continue from there.

- Session 4: `duo_beam` declared a win when the hero had died (a game over
  also zeroes the monster records); it now needs a living party member.
  `poll()` keeps watchpoint hits (`watch.add log=True`) in `play.WATCH_LOG`
  instead of crashing on them. Careful: `poll()` drains `break.log`, so
  your own silent breakpoints' hits only survive in `LAST_HIT`; and after
  `snapshot.load` drain once (`poll(True); log.clear()`) before trusting
  `goto`/`adv`, or stale text from the abandoned branch looks like an event.
- Session 3 additions in play.py: `engage`, `party`, `pstate`, `mons_all`,
  `alive_index`, `A_ATK`, `A_MAG`, `A_MAG_SELF`, `act_as`, `duo_round`,
  `duo_greedy`, `duo_beam` (+`_beam_replay`), `battle_list`, `equip`,
  `equip_list_goto`, `menu_use`, `map_heal`, `shop_buy`, `money`; flags
  `AUTO_FIGHT` (adv stops at a battle wheel when False) and `FLEE` (fight()
  flees). `goto` now also avoids map objects. `__all__` is at the end of the
  file so new helpers are exported by `rl()`. `rebuild.py` (see above).
- `daemon.py` + `run.py`: keep one emulator alive; `python3 tools/play/run.py 'code'`
  execs in a namespace with `from play import *` (`rl()` reloads play.py).
  `restart.sh` restarts it (then `start()` resumes the route). Snapshots live in
  the daemon only.
- `play.py`: `start()`, `poll()`, `adv()` (advance dialogue, fights if a battle
  appears), `goto(x,y)` (BFS, fights random battles), `enter_door(k)`,
  `talk_npc((x0,y0))`, `open_box(x,y)`, `loot(key)`, `lamp_cave(n)`, `fight()`,
  `fight2()`/`fight3(plan)` (heal policy), `act_item(kind, idx)`, `stats()`,
  `objs()`, `show()`, `coverage()`, `mark()`, `stop()`.
- `maps.py`: MAP parser + BFS (`python3 tools/play/maps.py 1 1` prints a map).
- `route_coverage.py`: replays the route and writes `route_seen.json`.
- Session 2 additions in play.py: `wait_wheel`, `act(keys|callable)`,
  `A_ATTACK`, `A_HEAL`, `A_USE_N`, `A_THROW_N`, `try_actions`, `boss_greedy`,
  `bstate`, `mons`, `flags`, `maze_walk`, `talk_obj`/`talk_all`, `visit(tile,
  key)`, `shop_browse(tile=..)`, `enter_door(once=True)`. `maze.py` (solver).
- Careful in the daemon namespace: don't assign `h` (it shadows the Hooks
  object; restore with `import builtins; h = builtins.h`).

## Text outside the dialogue box (for translation)

Engine/OS-drawn strings (not in the string table): main menu 金钱：/属性/魔法/
物品/系统, 状态/穿戴, 使用/装备, 读入进度/存储进度/游戏设置/结束游戏, status
labels 等级/生命/真气/攻击力/防御力/经验值/身法/灵力/幸运/免疫/无, item screen
名：/价：/数量：, shop 金钱：/买入个数：, magic 耗真气:, battle 围攻/道具/防御/
逃跑/状态/装备/投掷/使用, results 获得经验 N / 战斗获得 N钱 / 得到 X xN /
<name>修行提升, box pickup 获得:<item>, and the engine error `RunErr:N`.
Session 3 adds: the map-menu equip/use screens (`等级 生命 真气 攻击力 防御力`,
`/`, the who-wears-it popup listing party names, page 2 `经验值 身法 灵力 幸运
免疫` with immunity names like `毒`), 观音咒 caster/target screens, the
choice boxes `取消/使用钥匙` and `放走/杀死` (these two are script `choice`
rows), `<name>修行提升` + newly learned magic name after a level-up. The
battle status window (命/运/攻/身 numbers and the 攻防身毒乱封眠 row) is drawn
as bitmaps: nothing reaches the draw-string hook, so it is not in text.log.
They are tagged with whatever script position ran last, so `script` ids for
them are meaningless. Also: shop lists (金钱：/名：/价：/买入个数  ：, the
count line `<item> :`), 告示 signs (`say 0`), and GRS descriptions that embed
`\r\n` (天师符, 雷灵符, 火灵符: "符咒\r\n。") are drawn with the CR/LF bytes in
the 2-row description window. Item/magic names and the first row of descriptions come
from GRS/MRS (2-row windows; long descriptions are cut, not scrolled).
Session 4: the level-up popup `<name> / 练成 / <magic>` draws the name and
magic through draw-string but `练成` is a bitmap (not in text.log); the
存储进度 screen (title in a decorative font, slots `空档案`) was seen only in
a scratch emulator without hooks.
Session 5 (with hooks): the 存储进度/读入进度 slot lists draw each slot as the
saved scene name (e.g. `建业城`, via setscenename text) or `空档案`; saving
draws ` 档案储存中…`; the screen titles 存储进度/读入进度 are bitmaps (not in
text.log). The title menu 新的故事/再续前缘 and `完美版 v1.0` are bitmaps too.
Choice boxes `不给/奉还` (1-7-1 钱袋) are script rows.
