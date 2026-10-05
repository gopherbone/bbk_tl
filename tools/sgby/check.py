"""Check 三国霸业 translations against their fit specs.

    python3 tools/sgby/check.py [translations/sgby/en.jsonl]
    python3 tools/sgby/check.py --width "Some English"      # pixel width
    python3 tools/sgby/check.py --wrap 90 "Some long English line"
"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from sgby import strings  # noqa: E402

a = sys.argv[1:]
if a and a[0] == "--width":
    print(strings.width(a[1]))
elif a and a[0] == "--wrap":
    for line in strings.wrap(a[2], int(a[1])):
        print(f"{strings.width(line):4d}  {line}")
else:
    path = a[0] if a else os.path.join(ROOT, "translations/sgby/en.jsonl")
    rows = strings.load_rows(path)
    bad = 0
    for r in rows:
        p = strings.check(r)
        if p:
            bad += 1
            print(f"{r['id']}: {p}\n    zh: {r['zh']}\n    en: {r['en']}")
    done = sum(1 for r in rows if r.get("en"))
    print(f"{done}/{len(rows)} translated, {bad} problems")
