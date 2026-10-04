# 伏魔记 agent playthrough — notes

Route: `routes/fmj.agent.route.jsonl` (stopped cleanly, ends at frame 535195,
~149 min game time; `bbkplay --verify` hash 1370459f99d81d20).
Coverage of the route (`tools/play/route_coverage.py` -> `route_seen.json`):
165 / 632 `say` rows (26.1%), 172 gut rows. `seen.json` is cumulative over all
attempts incl. rewound ones (also counts GRS/MRS names/descs).

The three emulator bugs found in session 1 (IRQ I flag, save-marker overwrite,
auto power-off) are fixed in the official `bbkemu/target/release/bbkemu`;
`work/bbkemu_irqfix/` and `emu_fixes.patch` are obsolete.

## Where we are (end of session 3)

- In 蛇窟宝洞 (script 1-4-9, map (3,9)), player (12,8), all 6 boxes looted,
  events 214/215 set (蛇妖 beaten once in 1-4-8, it fled). Party 柳清风 Lv12
  (HP 310, MP 211/244, exp 967, next 1665) + 慕容小梅 Lv7 (HP 185, MP 232).
  Money 3431. 小梅 wears 芦藤雌甲/渺影衣/平安符/鹿皮靴, hero 芦藤雄甲/香袋.
- **Next**: the 传送点 box at (15,3) sits on tile 2: `goto(15,4)` then tap UP
  -> `startchapter 3,12`: cut-scene, 小梅 faints (`deleteactor 2`), then a
  **solo** fight vs 蛇妖男 (2000 HP, full). Set `play.AUTO_FIGHT=False` first
  so `adv()` stops at the wheel. Session 3 won it twice with
  `duo_beam(..., mei_cands=lambda ix, ps: [("-", None)])` (hero alone):
  无影神针, 火/土/风/水灵符, 剑气术 (magic idx 4), 玉蓝草, 魔王甲. Items left:
  无影神针 x1, 灵符 x5 kinds, 观音符, 玉蓝草 x5, 魔王甲, 还神丹, 定心符.
- **Watch out (game crash)**: if this battle levels the hero up *twice*
  (12->13->14), the engine corrupts its heap (garbage NPC names, hero HP
  48449) and ~2600 frames later runs into code in the wrong bank and hangs
  the emulator (see Emulator problems). Hero exp must stay < 1105 before the
  fight (967 now; the fight gives 860). That is why random fights on the way
  were fled (`play.FLEE=True`). With exp 900 or 0 (RAM poke test) no crash.
- A second, unexplained emulator hang happened inside one beam-search *sim*
  of this solo fight (not on the recorded line). Because snapshots die with
  the emulator, the beam was lost; see "Beam search" below for a guard idea.
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

## Emulator problems (session 3)

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
   data. That loop count comes from the corrupted heap after the double
   level-up (above), so the game itself is probably at fault; the emulator
   problem is only that an unknown opcode stalls the frame loop instead of
   advancing (a real 65C02 treats $9B as a 1-byte NOP).

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

## Tools (tools/play/)

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
