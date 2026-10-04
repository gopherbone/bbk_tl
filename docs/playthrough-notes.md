# 伏魔记 agent playthrough — notes

Route: `routes/fmj.agent.route.jsonl` (stopped cleanly, ends at frame 280844,
~78 min game time; `bbkplay --verify` hash 9c9dae066571d793).
Coverage of the route (`tools/play/route_coverage.py` -> `route_seen.json`):
97 / 632 `say` rows (15.3%), 101 gut rows. `seen.json` is cumulative over all
attempts incl. rewound ones (also counts GRS/MRS names/descs).

The three emulator bugs found in session 1 (IRQ I flag, save-marker overwrite,
auto power-off) are fixed in the official `bbkemu/target/release/bbkemu`;
`work/bbkemu_irqfix/` and `emu_fixes.patch` are obsolete.

## Where we are

- **Chapter 4 just started**: script 1-4-1 (转折路口5, map (1,33)), player (5,3),
  frame 280844. Party 柳清风 lv10 (HP 262, MP 195, atk 181, def 63) + 慕容小梅.
  Money ~1069.
- Session 2 did: 护剑神 boss (see battle notes) -> 1-2-17 movie -> 无机子 takes
  the sword (event 21) -> 三清宫 gate -> 步云桥 -> 摩天顶 -> bridge maze
  (events 100-128) -> 三清山入口 2-43/2-44 (all 4 boxes, sign) -> 原野 maze
  (events 101-105) -> `startchapter 3,1` 忘忧村: all boxes except (6,2)
  (unreachable), 东东 x2, 阿霞 (long line, needs 205), 蔡婆 (207), 老孟 (letter,
  201), 疯子, 武器店 + 杂货店 lists browsed, 村长 (小梅 joins, 202), 厨房, 主房
  box -> 原野 -> 1-2-50 tile 4 -> `startchapter 4,1`.
- **Next (chapter 4)**: 1-4-1 says the 瘴气林 can't be entered; 1-4-2 毒瘴林入口:
  a hunter says you need 芦藤甲. Then 1-4-8 通用山洞: 蛇妖 (ARS 3-3-5 蛇妖男:
  HP 2000, atk 200, def 150 — physical hits will do little; use 战狂石 (atk x2,
  5 rounds, have 1), 御剑术 (76 dmg/8 MP), 灵符s (~150-200), 小梅's healing).
- Skipped side content: 石梦城 / 李虎 quest for 蔡婆's daughter (1-2-52/53 via the
  原野 maze, 1-3-12), 观星亭 box, 歇息台子 boxes 2-39..2-42, 忘忧村 box (6,2).

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

Money: not pinned down (heap). Screen shows it in the EXIT menu.

## Tools (tools/play/)

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
They are tagged with whatever script position ran last, so `script` ids for
them are meaningless. Also: shop lists (金钱：/名：/价：/买入个数  ：, the
count line `<item> :`), 告示 signs (`say 0`), and GRS descriptions that embed
`\r\n` (天师符, 雷灵符, 火灵符: "符咒\r\n。") are drawn with the CR/LF bytes in
the 2-row description window. Item/magic names and the first row of descriptions come
from GRS/MRS (2-row windows; long descriptions are cut, not scrolled).
