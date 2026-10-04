# 伏魔记 agent playthrough — notes

Route: `routes/fmj.agent.route.jsonl` (stopped cleanly, ends at frame ~180300).
Coverage of the route (replayed by `tools/play/route_coverage.py`): 47 / 632 `say`
rows (7.4%), 49 gut rows. `seen.json` is cumulative over all attempts (incl.
rewound ones: 52 say rows); `route_seen.json` is what the route itself draws.

## !! The route needs a patched emulator !!

Stock `bbkemu`/`bbkplay` cannot play 伏魔记 past ~1 minute. Three core bugs,
fixed in a copy at `work/bbkemu_irqfix/` (patch: `work/playthrough/emu_fixes.patch`,
build: `cd work/bbkemu_irqfix && cargo build --release`). The route was recorded
with that build and replays only on it (or on bbkemu once the same fixes land):

1. **IRQ entry does not set the I flag** (`Emulator::trigger_interrupt`). The
   first IRQ the OS really uses is the RTC alarm (ALM, vector 0x34c), armed for
   minute 1. At frame 3540 it fires, the handler's first instruction is
   interrupted again, forever (sp wraps, game frozen at pc 0x034c). Fix: set
   the interrupt-disable flag after pushing pc/status (`cpu.set_interrupt_disable()`).
2. **`load_gam` overwrites 8 bytes of the game** with the "save area" marker
   `02 02 02 02 02 02 03 02` at flash 0x100F8 (A4988; 0xF0F8 on A4980). Flash
   0x20D000 + gam, so this is gam 0x30F8..0x30FF = engine code. Crash (BRK in RAM
   via a corrupted return address) the first time that code runs, e.g. walking
   down at 三清宫 (15,7). Fix: only write the marker when it is outside the game image.
3. **Auto power-off is not prevented.** `write_ram`'s "Prevent auto power off"
   hack for 0x2028 never fires: 0x2028 >= 0x1000 is written through
   `write_physical`. 0x2028 is the OS idle countdown (reloaded from 0x2027 = 4),
   decremented by the ALM handler each minute; key presses don't reset it (PI is
   HLE'd without the OS keyboard ISR). Once fix 1 lets ALM run, the game exits
   (pc 0x0261) ~4 minutes after boot. Fix: apply the hack in `write_physical`.

`tools/play/play.py` uses `bbkemu/target/release/bbkemu` (override
with `BBKEMU_BIN`). Verify with `bbkemu/target/release/bbkplay ... --verify`.

## Where we are

- Chapter 2 (script keys 1-2-*), 伏魔洞 hall (map 3,1), player (9,24), level 9,
  HP 252, MP 187, frame ~180300 (~50 min game time; ~14 min of it is grinding).
- Done: intro (full scroll), 百草地 boxes, all 8 三清宫 NPCs, 药房 shop list
  browsed, all 三清宫 rooms looted (师傅居, 弟子居1/2, 大师兄居, 清风居 + rest
  beds, 厨房, 丹房), menus browsed (属性 2 pages, 魔法 + cast 气疗术, 物品 browse
  + use 鸡蛋, 装备 钨龙剑/发带/草鞋/平安符, 系统 menu viewed), master talk
  (events), 竹林山道 → 后山浮桥 → 伏魔山道 → 伏魔洞口 → 伏魔洞, all 8 灯洞 lamp
  guardians beaten (events 11-18), most cave boxes.
- **Next: the 护剑神 boss** (box 无极乾坤剑 at (16,11) in 伏魔洞 → script 1-2-18
  L_0131: dialogue + `enterfight 0,10,11,10` = boss + two 护灯兽). Lost 3 times:
  the three deal ~100-120 per round; 气疗术 heals ~75 for 36 MP. Best try (lv9,
  heal below 60%) killed one beast before MP ran out. Ideas: grind more (60
  random fights = +1 level), use 玉蓝草 (hp+280, 物品/使用), 魔王甲 x2 (Mp+250
  each, a *use* item), 迷魂香 (sleep), 蝮蛇涎 (poison all), 天师符 (150 dmg),
  梅花镖 x2 (90), 雷/水/风灵符; check 凝神诀/天师符法 in the magic list (learned
  at level-ups; the battle magic list only showed 气疗术 and 御剑术).
- After the sword: movie, back at 伏魔洞口 (1-2-17: event 19 set, "手好痛哦…"),
  return to 无机阁 master (1-2-2 L_0394, gives the sword, setevent 21), then
  三清宫 tile 1 (gate, (22,43)) → 1-2-31 步云桥 … 1-2-43/44 三清山入口 → 原野
  (1-2-45/46, a maze driven by events 101-105) → `startchapter 3, 1` 忘忧村.

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

## Text outside the dialogue box (for translation)

Engine/OS-drawn strings (not in the string table): main menu 金钱：/属性/魔法/
物品/系统, 状态/穿戴, 使用/装备, 读入进度/存储进度/游戏设置/结束游戏, status
labels 等级/生命/真气/攻击力/防御力/经验值/身法/灵力/幸运/免疫/无, item screen
名：/价：/数量：, shop 金钱：/买入个数：, magic 耗真气:, battle 围攻/道具/防御/
逃跑/状态/装备/投掷/使用, results 获得经验 N / 战斗获得 N钱 / 得到 X xN /
<name>修行提升, box pickup 获得:<item>, and the engine error `RunErr:N`.
They are tagged with whatever script position ran last, so `script` ids for
them are meaningless. Item/magic names and the first row of descriptions come
from GRS/MRS (2-row windows; long descriptions are cut, not scrolled).
