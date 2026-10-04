"""Merge translation parts and build the English .gam.

  python3 tools/tl/build_en.py [--out work/fmj_en.gam]
Writes translations/fmj.en.jsonl (merged id -> en) and reports coverage.
"""
import argparse, glob, json, os, sys
from common import ROOT, PARTS, MERGED, rows, load_part, problems
sys.path.insert(0, ROOT)
from bbkrpg import build, engine_text

ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join(ROOT, "work", "fmj_en.gam"))
a = ap.parse_args()

table = rows() + engine_text.export()
by_id = {r["id"]: r for r in table}
merged = {}
src = {}
for path in sorted(glob.glob(os.path.join(PARTS, "*.jsonl"))):   # later files override (zz_* = overrides)
    name = os.path.basename(path)
    for rid, en in load_part(path).items():
        if rid in merged and merged[rid] != en and not name.startswith("zz_") and src[rid] != "auto.jsonl":
            print(f"conflict {rid} ({src[rid]} vs {name})")
        merged[rid] = en
        src[rid] = name
errs = 0
for rid, en in merged.items():
    for p in problems(by_id[rid], en) if rid in by_id and not rid.startswith("ENG/") else []:
        print(f"ERROR {rid}: {p}"); errs += 1
with open(MERGED, "w") as f:
    for r in table:
        if r["id"] in merged:
            f.write(json.dumps({"id": r["id"], "en": merged[r["id"]]}, ensure_ascii=False) + "\n")
for r in table:
    r["en"] = merged.get(r["id"], "")
todo = [r for r in table if not r["en"]]
kinds = {}
for r in todo:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
print(f"translated {len(table) - len(todo)}/{len(table)}; missing by kind: {kinds}")
out, info, probs = build.build(open(os.path.join(ROOT, "gam4980/retroarch/downloads/bbk/伏魔记.gam"), "rb").read(), table)
for p in probs:
    print("BUILD", p)
open(a.out, "wb").write(out)
json.dump({"bank": info["bank"]}, open(os.path.splitext(a.out)[0] + ".bank.json", "w"))
print(f"wrote {a.out}: {len(out)} bytes, {info['pages']} bank pages, {info['bank_bytes']} bank bytes")
sys.exit(1 if errs or probs else 0)
