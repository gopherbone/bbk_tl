"""Fill name/label rows straight from the glossary -> <parts>/auto.jsonl.  [--game fmj]"""
import json, os
from common import rows, glossary, PARTS

gl = glossary()
ENG_FIX = {"游戏设置": "Setup", "音乐开": "Music", "音乐关": "Mute"}
out = []
for r in rows():
    if r["kind"] in ("grs.name", "mrs.name", "ars.name", "map.name", "setscenename") and r["zh"] in gl:
        out.append({"id": r["id"], "en": gl[r["zh"]]["en"]})
os.makedirs(PARTS, exist_ok=True)
with open(os.path.join(PARTS, "auto.jsonl"), "w") as f:
    for d in out:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
print(len(out), "rows")
