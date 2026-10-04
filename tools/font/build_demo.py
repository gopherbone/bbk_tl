"""Build a demo .gam: a few hand-translated opening lines, paged renderer."""
import json, sys
sys.path.insert(0, ".")
from bbkrpg import fontpatch, gam, lib, strings

G = "gam4980/retroarch/downloads/bbk/伏魔记.gam"
DEMO = {
    "gut/1-1-1@039b": "Little butterfly, don't fly away...",
    "gut/1-1-1@03b8": "Little butterfly, don't fly away...",
    "gut/1-1-1@03d5": "Little butterfly, come on out...",
    "gut/1-1-1@03f2": "Little butterfly... where did you go??",
    "gut/1-1-1@0422": ("Brother, so this is where you are! Master couldn't find you, and he's "
                       "furious over in Wuji Pavilion. Hurry to Wuji Pavilion and see him."),
    "gut/1-1-1@0476": "All right, you go ahead. I'll be right there.",
    "gut/1-1-1@04bb": "Huh? Where did my little butterfly go??",
    "gut/1-1-1@04d7": "I'd better go see Master first.",
}

if __name__ == "__main__":
    orig = open(G, "rb").read()
    L = lib.parse(gam.split(orig)[0])
    rows = [json.loads(l) for l in open("work/fmj.strings.jsonl")]
    for r in rows:
        if r["id"] in DEMO:
            r["en"] = DEMO[r["id"]]
    bank = []
    built, problems = strings.apply(L, rows, bank=bank)
    assert not problems, problems
    out, info = fontpatch.patch(gam.join(orig, lib.pack(built)), bank)
    open("work/fmj_demo.gam", "wb").write(out)
    print(info)
    for i, p in enumerate(bank):
        print(i, p.decode().replace("\n", " | "))
