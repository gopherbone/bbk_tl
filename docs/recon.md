# Phase 1 recon

Generated from the gam4980 game set (152 `.gam` files) with `bbkrpg`. BIOS: `8.BIN` and `E.BIN`, 2 MiB each (A4988 dumps).

## 伏魔记.gam byte map

File size 851,968 bytes (832 KiB).

| Range | Size | Contents |
| --- | --- | --- |
| 0x00000-0x0003f | 64 B | Header: `GAM\0`, name `伏魔记` at 0x06, `BBK LTD.` at 0x26, `Ver1.3` at 0x37 |
| 0x00040-0x00045 | 6 B | Entry point 0x5046 (u16), data offset 0x48000 (u32) |
| 0x00046-0x47fff | 294,842 B | Engine: 6502 code and its own data (menus, battle text, font use) |
| 0x48000-0xcffff | 557,056 B | BBKRPG archive: 1228 resources in 33 banks |

Archive banks, in file order:

| Banks | Tag | File offset |
| --- | --- | --- |
| 1-5 | GUT | 0x4c000 |
| 6-11 | MAP | 0x60000 |
| 12 | ARS | 0x78000 |
| 13 | MRS | 0x7c000 |
| 14-17 | SRS | 0x80000 |
| 18-19 | GRS | 0x90000 |
| 20-21 | TIL | 0x98000 |
| 22-28 | ACP | 0xa0000 |
| 29 | GDP | 0xbc000 |
| 30-32 | SUN | 0xc0000 |
| 33 | MLR | 0xcc000 |

Nothing in the header records the archive size, and the archive runs to the end of the file, so a larger archive is written by extending the file. The archive is stored raw; it differs from BBKRPGSimulator's `fmj.LIB` (a different build) in about 40,000 bytes.

## Engine builds

Games grouped by a hash of the engine region (0x46 up to the archive). Same hash = same engine code, so `text.log` and `script.where` hooks found for one game work for the whole group. Different hashes may still share most code (the region is 288 KiB and may hold per-game data), so phase 3 should diff within the larger families before re-finding hooks.

100 BBKRPG games in 33 engine builds; 52 native games.

| Engine | Games | Count |
| --- | --- | --- |
| `acbade0405` | 伏魔记, 牛妞历险记, 英雄剑, 英雄剑1, 英雄剑2, 英雄坛说 | 6 |
| `24941e1b32` | 仙剑三, 仙剑奇侠传二之虎啸飞剑, 伏魔记-伏魔记外传, 伏魔记-游戏王, 伏魔迷宫, 侠客行, 冒险岛, 剑缘-第一部, 基督山传奇, 天之骄子, 娱乐无极限之无影奸细, 将门风云, 少年行, 屠魔, 异时空游记, 异时空游记2-纵横之旅, 志在青云, 新仙剑奇侠传, 新伏魔记, 新能源危机, 梦幻校园, 混战三国, 烈中轶事, 王氏传, 疯狂校园, 白中传奇, 紫璇刀, 纯蓝记, 蓝色天际, 蜘蛛侠三, 诸神黄昏, 释厄传 | 32 |
| `5d7def8d94` | 侠客行4988(终曲版), 天之骄子终曲版, 妖·传说终曲版, 新伏魔S终曲版, 英雄坛说终曲版, 赤壁之战乱世枭雄终曲版, 过关斩将4988(终曲版), 过关斩将4988改主角, 遗忘传说终曲版, 金庸群侠传终曲版, 金庸群侠黑暗时代终曲版 | 11 |
| `c2df2719a0` | 一中传奇, 一中传奇2, 地牢围攻, 生命女神之暗之诅咒, 赤壁之战 乱世枭雄, 过关斩将, 魔法学院 | 7 |
| `7616b1522c` | 大话三国, 封魔录, 最终幻想, 校园传奇, 梦幻西游, 英雄战士 | 6 |
| `4e139b96c1` | DIYtheGAME, 仙剑奇侠传四回梦游仙, 战国争霸, 抗日小兵, 疯狂盗墓人 | 5 |
| `b26d7161c8` | 七剑, 热血传奇, 问道 | 3 |
| `37dd3ead60` | 伏魔记之圆梦间奏曲v0.1, 伏魔记圆梦前奏曲(公测版), 伏魔记怀旧终曲v1.0(原版精修) | 3 |
| `03a6c06b35` | 伏魔记 加秘籍, 老观寺传奇 加秘籍 | 2 |
| `e68a28473c` | 伏魔记-清风传, 伏魔记-王柱人传奇 | 2 |
| `80ad9d6159` | 仙三外传 | 1 |
| `562ad6cb84` | 仙界传说 | 1 |
| `5f9aac3926` | 伏魔记(有声版) | 1 |
| `51eb9be10e` | 伏魔记-新护神记 | 1 |
| `5de4574c26` | 伏魔记-魔道传奇 | 1 |
| `0dfec5b64b` | 十字之门 | 1 |
| `2aa4b3bcf0` | 同福奇缘 | 1 |
| `33ad579cf4` | 大乱斗之火影忍者 | 1 |
| `d3a5b67f21` | 妖 传说 | 1 |
| `378a77534b` | 异世大陆 | 1 |
| `dee35e8825` | 我的世界 | 1 |
| `a2da93e657` | 新仙剑奇侠传终曲版 | 1 |
| `e8ba6652e8` | 末日传说 | 1 |
| `bbf1791b9e` | 步步高网友俱乐部 | 1 |
| `217b331e6d` | 武林新传 | 1 |
| `515963bc61` | 洛克人 | 1 |
| `7a7db50083` | 洛特传奇 | 1 |
| `d15b25ee96` | 老观寺传奇终曲版 | 1 |
| `650b2955ec` | 英雄坛 | 1 |
| `2e4bb85c05` | 落世沉浮 | 1 |
| `5c55accdc8` | 遗忘传说 | 1 |
| `fcef8d9af2` | 金庸群侠传 | 1 |
| `dbf25910bd` | 黑暗之心 | 1 |

Native (tier 3): Eros方块, 三国霸业, 中国象棋, 丰收, 乒乓球, 二十一点, 二十四点, 五子棋, 体闲麻将, 公路快车, 升级, 华容道, 坦克大战, 宠物精灵, 对对碰, 平面魔方, 幸运花, 恶龙传说, 扫雷, 投篮游戏, 拱猪, 挖金子, 接龙, 搬运工, 智多星, 比大小, 泡泡侠 加速版, 泡泡侠, 海盗船, 滑雪, 潜艇大战, 炸弹小子, 猪小弟, 猫狗大战, 电子宠物, 碰碰车, 秘密潜入, 螃蟹回家, 豪斯, 贪食蛇, 赛马, 跟花, 跳蛋, 迷宫游戏, 钓鱼, 钓鲨鱼, 阶梯小子, 飞行特训, 魔塔, 魔塔BT版, 魔塔超级版, 黑白子.
