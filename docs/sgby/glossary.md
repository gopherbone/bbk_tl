# 三国霸业 glossary

Term decisions for `translations/sgby/en.jsonl`. Short forms are forced by the
pixel budgets (24 px = about 4-5 letters for 2-hanzi labels).

## Stats

| zh | Full term | Short forms used |
|----|-----------|------------------|
| 等级 | Level | `Level` (list header), `Lvl` (battle panel) |
| 武力 | STR (War) | `War` (officer list header), `STR`, `STR+` elsewhere |
| 智力 | INT | `Int` (list header), `INT`, `INT+` |
| 忠诚 | Loyalty | `Loyalty` |
| 经验 | EXP | `EXP`, `EXP gained:` |
| 体力 | Stamina | `Stamina`, `Low stamina` |
| 生命 (battle) | HP | `HP:` |
| 技力 | SP | `SP:`, `Low SP` |
| 攻击 / 防御 | ATK / DEF | |
| 移动 | Move | `Move+`, `Move +15` |
| 兵种 | Type | `Type` |
| 兵力 | Troops | `Troop` (28 px header; `Troops` is 29), `Men:` in the battle panel (5-byte cell), `Troops -/+` |
| 年龄 | Age | |
| 农业 | Farming | `Farm:` (city panel), `Farming max`, `Farming now` |
| 商业 | Commerce | `Comm:` (city panel), `Commerce max`, `Commerce now` |
| 民忠 | Morale | `Mor:` (city panel, 30 px), `Morale now` |
| 防灾 | Relief | `Relief:`, `Relief max` |
| 人口 | Population | `Pop:` |
| 金钱 / 粮食 | Gold / Food | `Gold:`, `Food:` |
| 后备兵力 | Reserves | `Reserves:` |

City panel labels are glued straight to their numbers, as in the original
(`Farm:120/999`). `Ruler: ` and `Gov: ` keep a space before the name.

## City states (24 px)

正常 `OK`, 饥荒 `Blight`, 旱灾 `Dry`, 水灾 `Flood`, 暴动 `Riot`.
`Famine` and `Drought` are 30-34 px.

## Ranks and status

君主 Ruler, 太守 Governor (`Gov:`), 在野 Free, 俘虏 Captive, 归属 Faction (column header) / `Ruler:` (city panel, 30 px),
所在城市 Location.

## Troop types

Full words in the officer list (s/17-22, 40 px). The 24 px slots (e/12 battle
panel, s/73-75 item column) use the short forms.

| zh | Term | 24 px label |
|----|------|-------------|
| 骑兵 | Cavalry | `Cav.` |
| 步兵 | Infantry | `Inf.` |
| 弓兵 | Archers | `Arch.` |
| 水军 / 水兵 | Navy | `Navy` |
| 极兵 | Elite | `Elite` |
| 玄兵 | Mystic | `Myst.` |

## Menus

- Main: Domestic, Diplomacy, Military, Status.
- Domestic: Farm (开垦), Commerce (招商), Search, Govern, Patrol, Recruit
  (招降), Execute, Exile, Reward, Seize (没收; `Confiscate` is too wide),
  Market (交易), Banquet, Transport, Move.
- Diplomacy: Discord (离间), Entice (招揽, kept apart from 招降 Recruit),
  Incite (策反), Counter (反间; the command does nothing in the source),
  Demand (劝降, demand surrender).
- Military: Scout, Conscript, Assign, Plunder, Attack.
- Market: Buy, Sell. Turn menu: End Turn, Save Game, Quit Game.
- Battle: Attack, Tactic, View, Wait; End Turn, Retreat, Animation,
  Move Speed, Enemy Moves; Off/On; Fast/Slow.

## Terrain (24 px)

草地 Grass, 平原 Plain, 山地 Hills, 森林 `Wood`, 村庄 `Town`, 城池 `Fort`,
营寨 Camp, 河流 River. The terrain help messages use the same words.

## Skills (46 px) and battle states (24 px)

| zh | Skill | State (e/28..35) |
|----|-------|------------------|
| 践踏 | Trample | |
| 冲锋 | Charge | |
| 突击 | Assault | |
| 突袭 | Raid | |
| 火攻 | Fire (`Fire Attack` is 49 px) | |
| 滚木 | Log Roll | |
| 落石 | Rockslide | |
| 奋战 | Fury | |
| 飞矢 | Arrows | |
| 箭雨 | Volley (`Arrow Rain` is 48 px) | |
| 火箭 | Fire Shot (`Fire Arrows` is 52 px) | |
| 水淹 | Flood | |
| 撞击 | Ram | |
| 咒封 / 禁咒 | Silence | Seal |
| 定身 | Hold | Held |
| 流言 / 混乱 | Rumors | Panic |
| 援兵 (small heal) | Support | |
| 援军 (large heal) | Reinforce | |
| 烈火 | Inferno | |
| 海啸 | Tsunami | |
| 奇门 | Shift | Shift |
| 遁甲 | Cloak | Cloak |
| 天变 | Weather | |
| 石阵 | Maze (`Stone Maze` is 52 px) | Maze |
| 陷阱 | Trap | |
| 天籁 | Siren | |
| 潜踪 | Veil (kept to match the 24 px state) | Veil |
| 围攻 | Siege | |
| 急行 | Dash | |
| 谍报 | Intel | |
| 正常 | | OK |

The state message is `<name>: <state>!` (e/27 `": "`, e/36 `"!"`), so a
state works as a noun or an adjective.

## Items (58 px)

Weapons: 方天画戟 Sky Piercer, 七星刀 Seven Stars, 青龙刀 Dragon Blade
(`Green Dragon` is 59 px), 丈八矛 Snake Spear, 双股剑 Twin Swords, 三尖刀
Trident, 双铁戟 Twin Halberd, 倚天剑 Yitian Sword, 青虹剑 Qinghong
(`Qinghong Sword` does not fit), 望月枪 Moon Spear, 古淀刀 Ingot Blade.

Books: 六韬 Liu Tao, 三略 San Lue, 司马法 Sima Fa, 孙子兵法 Art of War,
范蠡兵法 Fan Li, 墨子 Mozi, 吴子兵法 Wuzi, 鬼谷子 Guiguzi, 孙膑兵法 Sun Bin,
尉缭子 Weiliaozi, 商君书 Lord Shang.

Horses: 赤兔 Red Hare, 的卢 Dilu, 绝影 Jueying, 爪黄飞电 Lightning
(`Flying Lightning` does not fit), 王追 Wangzhui, 惊帆 Jingfan, 白鸽 White
Dove, 快航 Kuaihang.

Tallies (兵符): Elite Tally, Mystic Tally, Navy Tally.

Descriptions use the full names: Jiang Taigong (吕尚), Tian Rangju (source has
田骧苴 for 田穰苴), Sun Wu, Fan Li, Mo Di, Wu Qi, Guiguzi, Sun Bin, Wei Liao,
Shang Yang, Huang Shigong.

## Cities (43 px)

Full pinyin, one word: Xiliang, Beiping, Xiangping, Anding, Jinyang, Pingyuan,
Nanpi, Beihai, Tianshui, Henei, Chang'an, Ye, Puyang, Xuzhou, Hanzhong,
Luoyang, Xuchang, Xiaopei, Xiapi, Zitong, Wancheng, Shouchun, Jianye, Wu,
Chengdu, Mianzhu, Xiangyang, Jiangxia, Lujiang, Kuaiji (会稽), Yunnan, Bajun,
Wuling, Changsha, Chaisang, Lingling, Guiyang, Jianning.

## Officer names

Hanyu Pinyin, family name first, ASCII (吕 = Lu). Readings worth noting:

- Custom glyphs in the name table: 李傕 Li Jue (A2E3), 荀彧 Xun Yu (A2E4),
  夏侯惇 Xiahou Dun (A2EF), 曹叡 Cao Rui (A2F0), 费祎 Fei Yi (A5F7),
  张郃 Zhang He (A5F8), 毛玠 Mao Jie (A5F9), 严畯 Yan Jun (A5FA),
  张纮 Zhang Hong (GBK C080). Identified by drawing the glyphs from
  `refs/iBaye/src/Gamhzk.bin`.
- 逢纪 Pang Ji (逢 as a surname is Pang; Koei uses Feng Ji).
- 张嶷 Zhang Ni (conventional reading).
- 毋丘俭 Guanqiu Jian (the surname is 毌丘).
- 博士仁 Fu Shiren (the game's typo for 傅士仁).
- 诸葛谨 Zhuge Jin (the game's typo for 瑾).
- 刑道荣 Xing Daorong, 乐进 Yue Jin, 阚泽 Kan Ze, 阎圃 Yan Pu.
- Nanman: 沙摩柯 Shamoke, 朵思大王 King Duosi, 金环三结 Jinhuan Sanjie,
  祝融夫人 Lady Zhurong, 带来洞主 Dailai, 董荼那 Dong Tuna, 阿会喃 Ahuinan,
  忙牙长 Mangyachang.
- Joke officers: 通宵虫 `Nightbug`, 南方小鬼 `South Imp` (translated, not
  romanised).

Name budget is 62 px. Two names are shortened: 孙尚香 `Lady Sun`, 金环三结
`Jinhuan`.

## Assembled messages

| Message | Pieces |
|---------|--------|
| `<ruler> vs <ruler>` | s/104 `" vs "`, s/105 `" "` |
| `We vs <city>` / `<ruler> vs <city>` | s/98 `We`, s/97 `" vs "` |
| `We won` / `<ruler> won` / `We lost` | s/98, s/91, s/92 |
| `<city>: Blight! Govern it soon.` | s/111 `": "`, s/112 |
| `Farming now 120 (+5).` | s/113, s/114 `" (+"`, s/115 `")."` |
| `Took gold 120, food 300.` | s/149, s/150, s/151 |
| `Ruler <name> died` | s/78, s/79 |
| `<name>: Panic!` | e/27 `": "`, state, e/36 `"!"` |
| ` Fire  failed!` | skill name, e/26 |
| `Found <item or officer>` | s/99 `"Found "` |
| `<year>AD`, `<month> mo` | s/63 `AD`, s/64 `" mo  "` |
