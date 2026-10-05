"""Export the 三国霸业 string table with usage context from the iBaye source.

    python3 tools/sgby/export.py   -> translations/sgby/strings.jsonl
"""
import glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from sgby.lib import Lib, split_gam  # noqa: E402
from sgby import strings  # noqa: E402

GAM = "gam4980/retroarch/downloads/bbk/三国霸业.gam"
SRC = "refs/iBaye/src"

srcfiles = {p: open(p, encoding="utf-8", errors="replace").read().splitlines()
            for p in glob.glob(f"{SRC}/*.c")}


def macro_names():
    s = {}
    for line in open(f"{SRC}/baye/sconst.h", encoding="utf-8", errors="replace"):
        m = re.match(r"#define\s+(\w+)\s+(\d+)", line)
        if m:
            s.setdefault(int(m.group(2)), m.group(1))
    e = {}
    body = open(f"{SRC}/data/pstring.h", encoding="utf-8", errors="replace").read()
    names = re.findall(r"^\s*(d\w+)\s*(?:=\s*1)?\s*,", body, re.M)
    for i, n in enumerate(names, 1):
        e[i] = n
    return s, e


def usage(name, limit=4):
    out = []
    for p, lines in srcfiles.items():
        for n, line in enumerate(lines):
            if re.search(rf"\b{re.escape(name)}\b", line) and "#define" not in line:
                out.append(f"{os.path.basename(p)}:{n + 1}: {line.strip()[:140]}")
                if len(out) >= limit:
                    return out
    return out


def main():
    code, font, lib = split_gam(open(GAM, "rb").read())
    L = Lib(lib)
    rows = strings.export(L)
    smac, emac = macro_names()
    for r in rows:
        pre, _, rest = r["id"].partition("/")
        n = rest.split("#")[0]
        name = None
        if pre == "s" and n.isdigit():
            name = smac.get(int(n))
        elif pre == "e" and n.isdigit():
            name = emac.get(int(n))
        if name:
            r["macro"] = name
            r["usage"] = usage(name)
    os.makedirs("translations/sgby", exist_ok=True)
    strings.save_rows("translations/sgby/strings.jsonl", rows)
    hz = sum(sum(1 for c in r["zh"] if ord(c) > 0x2e80) for r in rows)
    print(len(rows), "rows,", hz, "hanzi")


main()
