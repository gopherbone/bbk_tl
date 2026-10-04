"""Print rows to translate, in story order, with context.

  python3 tools/tl/dump.py [--game fmj] --chapters 2,3   script rows of those chapters (key 1-<chapter>-n)
  python3 tools/tl/dump.py --kinds grs.desc,mrs.desc
"""
import argparse
from common import rows

ap = argparse.ArgumentParser()
ap.add_argument("--chapters"); ap.add_argument("--kinds")
a = ap.parse_args()
chs = set(a.chapters.split(",")) if a.chapters else None
kinds = set(a.kinds.split(",")) if a.kinds else None
SCRIPT = {"say", "message", "choice", "showgut", "menu"}
last = None
for r in rows():
    if chs is not None:
        if not r["id"].startswith("gut/") or r["kind"] not in SCRIPT or r["id"].split("/")[1].split("-")[1] not in chs:
            continue
    if kinds is not None and r["kind"] not in kinds:
        continue
    key = r["id"].split("@")[0]
    if key != last:
        print(f"\n## {key}  scene: {r['ctx'].get('scene')}")
        last = key
    ctx = f" pic={r['ctx']['pic']}" if "pic" in r.get("ctx", {}) else ""
    print(f"{r['id']}\t{r['kind']}{ctx}\t{r['zh']}")
