"""Draft English for engine strings + demo dialogue -> work/fmj_demo.gam."""
import json, sys
sys.path.insert(0, ".")
from bbkrpg import build, engine_text
sys.path.insert(0, "tools/font")
from build_demo import DEMO

ENG = {
    "空档案": "Empty", "错误指令...": "Bad command...", "已满载！": "Inventory full!", "获得:": "Got: ",
    "档案储存中… ": "Saving... ", "耗真气:": "MP cost:", "等级": "Lv", "生命": "HP", "真气": "MP",
    "攻击力": "Attack", "防御力": "Defense", "经验值": "EXP", "身法": "Agility", "灵力": "Spirit",
    "幸运": "Luck", "免疫": "Immune", "毒": "Psn", "乱": "Cnf", "封": "Sil", "眠": "Slp", "无": "-",
    "属性": "Stats", "魔法": "Magic", "物品": "Items", "系统": "Game", "状态": "Status", "穿戴": "Gear",
    "使用": "Use", "装备": "Equip", "读入进度": "Load", "存储进度": "Save", "游戏设置": "Options",
    "结束游戏": "Quit", "音乐开": "Music On", "音乐关": "Music Off", "金钱：": "Money:",
    "目前不能存档!": "Can't save now!", "真气不足!": "Not enough MP!", "围攻": "Rush", "道具": "Item",
    "防御": "Guard", "逃跑": "Flee", "投掷": "Throw", "获得经验": "EXP", "战斗获得 ": "Earned ",
    "得到 ": "Got ", "修行提升": "Level up!", "偷得 ": "Stole ", "装饰": "Acc.", "护腕": "Wrist",
    "脚蹬": "Feet", "手持": "Hand", "身穿": "Body", "肩披": "Cape", "头戴": "Head",
    "不能装备！": "Can't equip!", "已装备！": "Equipped!", "战斗中才能使用！": "Only in battle!",
    "无效！": "No effect!", "真气不足！": "Not enough MP!", "此处无法使用！": "Can't use that here!",
    "卖出个数  ：": "Sell how many:", "买入个数  ：": "Buy how many:", "金钱不足！": "Not enough money!",
    "没携带物品！": "No items!", "不可卖物品！": "Can't sell that!", "数量：": "Qty:", "价：": "Price:",
    "名：": "Name:",
}

if __name__ == "__main__":
    rows = [json.loads(l) for l in open("work/fmj.strings.jsonl")]
    for r in rows:
        if r["id"] in DEMO:
            r["en"] = DEMO[r["id"]]
    eng = engine_text.export()
    for r in eng:
        r["en"] = ENG.get(r["zh"], "")
    missing = [r["zh"] for r in eng if not r["en"]]
    assert not missing, missing
    out, info, problems = build.build(open("gam4980/retroarch/downloads/bbk/伏魔记.gam", "rb").read(), rows + eng)
    assert not problems, problems
    open("work/fmj_demo.gam", "wb").write(out)
    print(info)
