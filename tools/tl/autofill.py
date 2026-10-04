"""Fill name/label rows straight from the glossary -> <parts>/auto.jsonl.  [--game fmj]

A term's `short` form is used where its `en` breaks the row's display limit."""
import json, os
from common import rows, glossary, PARTS, problems

gl = glossary()
by_source = {sid: t for t in gl.values() for sid in t.get("source_ids") or []}   # e.g. GBK-encoded names
out = []
for r in rows():
    t = gl.get(r["zh"]) or by_source.get(r["id"])
    if r["kind"] in ("grs.name", "mrs.name", "ars.name", "map.name", "setscenename") and t:
        en = t["en"]
        if problems(r, en) and t.get("short"):
            en = t["short"]
        out.append({"id": r["id"], "en": en})
os.makedirs(PARTS, exist_ok=True)
with open(os.path.join(PARTS, "auto.jsonl"), "w") as f:
    for d in out:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
print(len(out), "rows")
