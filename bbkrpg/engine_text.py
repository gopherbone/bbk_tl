"""Strings in the 伏魔记 engine code (menus, labels, battle and shop messages).

They are not in the archive, so they get their own rows (ENG/<gam offset>).
Each entry is a NUL-terminated string or a packed menu: N fixed-width items
copied as one block and sliced by the engine. The replacement must keep the
byte layout, so translations go in as renderer tokens (fontpatch):
  * a slot of 2 bytes  -> FD 8i            (id < 128)
  * a slot of 4+ bytes -> FE 8h FE 8l, padded with FC 80 fillers (16 px each)
    so the slot keeps its original pixel width;
  * a NUL-terminated string -> plain ASCII when it fits the original bytes,
    else a token + NUL.
Offsets are for engine build c81b80 (伏魔记 Ver1.3); `apply` checks the
original bytes before writing.
"""

from __future__ import annotations

from . import fontpatch

# (gam offset, zh, packed item byte widths or None for a C string)
ENTRIES: list[tuple[int, str, list[int] | None]] = [
    (0x0247E, "空档案", None),
    (0x07B6F, "错误指令...", None),
    (0x07B7B, "已满载！", None),
    (0x07B84, "获得:", None),
    (0x0F615, "档案储存中… ", None),
    (0x137C6, "耗真气:", None),
    (0x13818, "等级", None),
    (0x1381D, "生命", None),
    (0x13822, "真气", None),
    (0x13827, "攻击力", None),
    (0x1382E, "防御力", None),
    (0x13835, "经验值", None),
    (0x1383C, "身法", None),
    (0x13841, "灵力", None),
    (0x13846, "幸运", None),
    (0x1384B, "免疫", None),
    (0x13858, "毒", None),
    (0x1385B, "乱", None),
    (0x1385E, "封", None),
    (0x13861, "眠", None),
    (0x13864, "无", None),
    (0x13891, "属性魔法物品系统", [4, 4, 4, 4]),
    (0x138A3, "状态穿戴", [4, 4]),
    (0x138AD, "使用装备", [4, 4]),
    (0x138B7, "读入进度存储进度游戏设置结束游戏", [8, 8, 8, 8]),
    (0x138D9, "音乐开音乐关", [6, 6]),
    (0x138E7, "金钱：", None),
    (0x13912, "目前不能存档!", None),
    (0x1F8A0, "真气不足!", None),
    (0x1F8AA, "围攻道具防御逃跑状态", [4, 4, 4, 4, 4]),
    (0x1F8E4, "装备投掷使用", [4, 4, 4]),
    (0x2FACD, "获得经验", None),
    (0x2FAD6, "战斗获得 ", None),
    (0x2FAE3, "得到 ", None),
    (0x2FAEC, "修行提升", None),
    (0x2FB65, "偷得 ", None),
    (0x3398B, "装饰", None),
    (0x33990, "装饰", None),
    (0x33995, "护腕", None),
    (0x3399A, "脚蹬", None),
    (0x3399F, "手持", None),
    (0x339A4, "身穿", None),
    (0x339A9, "肩披", None),
    (0x339AE, "头戴", None),
    (0x339F3, "不能装备！", None),
    (0x3789F, "不能装备！", None),
    (0x378C6, "已装备！", None),
    (0x378CF, "战斗中才能使用！", None),
    (0x378E0, "无效！", None),
    (0x378FF, "真气不足！", None),
    (0x3790A, "此处无法使用！", None),
    (0x37931, "金钱：", None),
    (0x3793A, "卖出个数  ：", None),
    (0x37947, "买入个数  ：", None),
    (0x3795C, "金钱不足！", None),
    (0x3796F, "没携带物品！", None),
    (0x3797C, "不可卖物品！", None),
    (0x3B446, "数量：", None),
    (0x3B44D, "价：", None),
    (0x3B452, "名：", None),
    (0x3B457, "金钱：", None),
    (0x3B45E, "金钱不足！", None),
    (0x3B469, "已满载！", None),
]

FILLER = b"\xfc\x80"
RESERVED_SHORT = 128          # bank ids 0..127 are for 2-byte (FD) slots


def _rows():
    for off, zh, items in ENTRIES:
        if items is None:
            yield f"ENG/{off:05x}", off, zh, None
        else:
            raw = zh.encode("gb2312")
            pos = 0
            for n, w in enumerate(items):
                yield f"ENG/{off:05x}.{n}", off + pos, raw[pos:pos + w].decode("gb2312"), w
                pos += w


def export() -> list[dict]:
    out = []
    for rid, _, zh, slot in _rows():
        limits = {"max_px": slot * 8} if slot else {"max_bytes": None}
        out.append({"id": rid, "kind": "engine", "zh": zh, "en": "", "ctx": {}, "limits": limits,
                    "status": "todo", "note": ""})
    return out


def inline_token(bank: list[bytes], text: bytes, width: int) -> bytes:
    """Bytes for a slot of `width` bytes showing `text` from the bank."""
    if width == 2:
        try:
            i = bank.index(b"")            # a free reserved short id
        except ValueError:
            raise ValueError("more than 128 two-byte engine strings") from None
        if i >= RESERVED_SHORT:
            raise ValueError("more than 128 two-byte engine strings")
        bank[i] = text
        return bytes([0xFD, 0x80 | i])
    if width < 4 or width % 2:
        raise ValueError(f"cannot fit a token in a {width}-byte slot")
    bank.append(text)
    i = len(bank) - 1
    return bytes([0xFE, 0x80 | i >> 7, 0xFE, 0x80 | i & 0x7F]) + FILLER * ((width - 4) // 2)


def apply(gam: bytes, rows: list[dict], bank: list[bytes]) -> tuple[bytes, list[str]]:
    """Write translated engine strings into the .gam's engine code."""
    if len(bank) < RESERVED_SHORT:
        bank.extend([b""] * (RESERVED_SHORT - len(bank)))
    en = {r["id"]: r["en"] for r in rows if r.get("en") and r["id"].startswith("ENG/")}
    out = bytearray(gam)
    problems = []
    for rid, off, zh, slot in _rows():
        orig = zh.encode("gb2312")
        if bytes(out[off:off + len(orig)]) != orig and rid in en:
            problems.append(f"{rid}: original bytes not found (different engine build?)")
            continue
        if rid not in en:
            continue
        text = en[rid].encode("ascii", errors="replace")
        if slot:
            data = inline_token(bank, text, slot)
        elif len(text) <= len(orig):
            data = text + b"\0" * (len(orig) - len(text))
        elif len(orig) >= 4:
            data = inline_token(bank, text, 4) + b"\0" * (len(orig) - 4)
        elif len(orig) == 2:
            data = inline_token(bank, text, 2)
        else:
            problems.append(f"{rid}: {len(text)} bytes do not fit {len(orig)}")
            continue
        out[off:off + len(data)] = data
    return bytes(out), problems
