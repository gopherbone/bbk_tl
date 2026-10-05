"""Which translated rows a tour drew: coverage.py TEXTS.jsonl [...]"""
import collections, glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from sgby import strings  # noqa: E402

texts = []
for p in sys.argv[1:]:
    texts += [json.loads(l)["text"] for l in open(p)]
blob = "\n".join(texts)
merged = {r["id"]: r["en"] for r in strings.load_rows(os.path.join(ROOT, "translations/sgby/en.jsonl"))}
for f in sorted(glob.glob(os.path.join(ROOT, "translations/sgby/fix*.jsonl"))):
    merged.update({r["id"]: r["en"] for r in strings.load_rows(f)})
rows = strings.load_rows(os.path.join(ROOT, "translations/sgby/strings.jsonl"))
seen, miss = collections.Counter(), collections.defaultdict(list)
for r in rows:
    en = merged.get(r["id"], "").strip(" \x1e\x1f")
    kind = r["id"].split("/")[0]
    if en and en in blob:
        seen[kind] += 1
    else:
        miss[kind].append(r["id"])
for k in sorted(set(seen) | set(miss)):
    print(f"{k:10s} {seen[k]:4d} seen, {len(miss[k]):4d} not seen", " ".join(miss[k][:12]) if k in ("e", "s") else "")
