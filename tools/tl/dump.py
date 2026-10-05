"""Print rows to translate, in story order, with context.

  python3 tools/tl/dump.py [--game fmj] --chapters 2,3   script rows of those chapters (key 1-<chapter>-n)
  python3 tools/tl/dump.py --kinds grs.desc,mrs.desc
  python3 tools/tl/dump.py --keys 1-4-1,1-4-2       script rows of those scripts only
Rows that repeat an earlier row's kind and text are left out (build_en copies
the first one's translation to them); --all lists them too.
"""
import argparse
from common import rows, canonical

ap = argparse.ArgumentParser()
ap.add_argument("--chapters"); ap.add_argument("--kinds"); ap.add_argument("--keys"); ap.add_argument("--all", action="store_true")
a = ap.parse_args()
chs = set(a.chapters.split(",")) if a.chapters else None
kinds = set(a.kinds.split(",")) if a.kinds else None
keys = set(a.keys.split(",")) if a.keys else None
SCRIPT = {"say", "message", "choice", "showgut", "menu", "timemsg"}
last = None
table = rows()
canon = canonical(table)
for r in table:
    if not a.all and canon[r["id"]] != r["id"]:
        continue
    if chs is not None:
        if not r["id"].startswith("gut/") or r["kind"] not in SCRIPT or r["id"].split("/")[1].split("-")[1] not in chs:
            continue
    if keys is not None and (not r["id"].startswith("gut/") or r["kind"] not in SCRIPT
                             or r["id"].split("/")[1].split("@")[0] not in keys):
        continue
    if kinds is not None and r["kind"] not in kinds:
        continue
    key = r["id"].split("@")[0]
    if key != last:
        print(f"\n## {key}  scene: {r['ctx'].get('scene')}")
        last = key
    ctx = f" pic={r['ctx']['pic']}" if "pic" in r.get("ctx", {}) else ""
    print(f"{r['id']}\t{r['kind']}{ctx}\t{r['zh']}")
