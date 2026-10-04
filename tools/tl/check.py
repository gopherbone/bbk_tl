"""Check translation part files: python3 tools/tl/check.py [--game fmj] translations/parts/x.jsonl [...]"""
import sys
from common import rows, glossary, load_part, problems, warnings

table = {r["id"]: r for r in rows()}
gl = glossary()
bad = 0
for path in sys.argv[1:]:
    part = load_part(path)
    for rid, en in part.items():
        r = table.get(rid)
        if r is None:
            print(f"ERROR {rid}: no such row"); bad += 1; continue
        for p in problems(r, en):
            print(f"ERROR {rid}: {p}"); bad += 1
        for w in warnings(r, en, gl):
            print(f"warn  {rid}: {w}")
    print(f"{path}: {len(part)} rows checked")
sys.exit(1 if bad else 0)
