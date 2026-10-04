"""bbkrpg command line."""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import gam as gammod
from . import gut as gutmod
from . import lib as libmod
from . import lint as lintmod
from . import strings as strmod


def _load_lib(path: str) -> libmod.Lib:
    if os.path.isdir(path):
        return libmod.load_dir(path)
    with open(path, "rb") as f:
        data = f.read()
    if data[:3] != b"LIB":
        data, _ = gammod.split(data)
    return libmod.parse(data)


def _write(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def cmd_lib_unpack(a):
    L = _load_lib(a.lib)
    libmod.unpack(L, a.out)
    print(json.dumps({"name": L.name, "resources": len(L.order), "banks": len(L.banks), "out": a.out},
                     ensure_ascii=False))


def cmd_lib_pack(a):
    data = libmod.pack(libmod.load_dir(a.dir))
    _write(a.out, data)
    print(json.dumps({"out": a.out, "bytes": len(data)}))


def cmd_lib_info(a):
    L = _load_lib(a.lib)
    counts = {}
    for k in L.order:
        t = libmod.RES_TYPES.get(k[0], str(k[0]))
        counts[t] = counts.get(t, 0) + 1
    print(json.dumps({"name": L.name, "resources": counts, "banks": [b.tag for b in L.banks]},
                     ensure_ascii=False))


def cmd_gut_disasm(a):
    L = _load_lib(a.lib)
    keys = L.keys_of(1) if a.all else [libmod.parse_key(a.key)]
    if a.all:
        os.makedirs(a.out, exist_ok=True)
    for k in keys:
        text = gutmod.disasm(gutmod.parse(L.res[k]), libmod.key_str(k))
        if a.all:
            with open(os.path.join(a.out, libmod.key_str(k) + ".gut"), "w", encoding="utf-8") as f:
                f.write(text)
        elif a.out:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            sys.stdout.write(text)


def cmd_gut_asm(a):
    with open(a.src, encoding="utf-8") as f:
        blob = gutmod.asm(f.read())
    _write(a.out, blob)
    print(json.dumps({"out": a.out, "bytes": len(blob)}))


def cmd_strings_export(a):
    rows = strmod.export(_load_lib(a.lib))
    strmod.write_jsonl(rows, a.out)
    print(json.dumps({"out": a.out, "rows": len(rows)}))


def cmd_strings_import(a):
    L = _load_lib(a.lib)
    rows = strmod.read_jsonl(a.table)
    built, problems = strmod.apply(L, rows)
    for p in problems:
        print("error:", p, file=sys.stderr)
    if problems and not a.force:
        sys.exit(1)
    data = libmod.pack(built)
    if a.gam:
        with open(a.gam, "rb") as f:
            data = gammod.join(f.read(), data)
    _write(a.out, data)
    print(json.dumps({"out": a.out, "bytes": len(data),
                      "applied": sum(1 for r in rows if r.get("en")), "problems": len(problems)}))


def cmd_lint(a):
    errors, warnings = lintmod.lint(_load_lib(a.lib), strmod.read_jsonl(a.table))
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    sys.exit(1 if errors else 0)


def cmd_detect(a):
    with open(a.gam, "rb") as f:
        data = f.read()
    hits = gammod.find(data)
    print(json.dumps({"file": a.gam, "bbkrpg": bool(hits),
                      "archives": [h.__dict__ for h in hits]}, ensure_ascii=False))


def cmd_gam_split(a):
    with open(a.gam, "rb") as f:
        data = f.read()
    blob, h = gammod.split(data)
    _write(a.out, blob)
    print(json.dumps({"out": a.out, **h.__dict__}, ensure_ascii=False))


def cmd_gam_join(a):
    with open(a.gam, "rb") as f:
        data = f.read()
    with open(a.lib, "rb") as f:
        new = f.read()
    _write(a.out, gammod.join(data, new))
    print(json.dumps({"out": a.out}))


def main(argv=None):
    p = argparse.ArgumentParser(prog="bbkrpg", description="BBKRPG archive toolkit")
    sub = p.add_subparsers(dest="group", required=True)

    def group(name, help_):
        g = sub.add_parser(name, help=help_).add_subparsers(dest="cmd", required=True)
        return g

    lib_g = group("lib", "archive unpack/pack")
    s = lib_g.add_parser("unpack"); s.add_argument("lib"); s.add_argument("out"); s.set_defaults(fn=cmd_lib_unpack)
    s = lib_g.add_parser("pack"); s.add_argument("dir"); s.add_argument("out"); s.set_defaults(fn=cmd_lib_pack)
    s = lib_g.add_parser("info"); s.add_argument("lib"); s.set_defaults(fn=cmd_lib_info)

    gut_g = group("gut", "script disassembler/assembler")
    s = gut_g.add_parser("disasm"); s.add_argument("lib"); s.add_argument("key", nargs="?")
    s.add_argument("--all", action="store_true"); s.add_argument("-o", "--out"); s.set_defaults(fn=cmd_gut_disasm)
    s = gut_g.add_parser("asm"); s.add_argument("src"); s.add_argument("out"); s.set_defaults(fn=cmd_gut_asm)

    st_g = group("strings", "translation table")
    s = st_g.add_parser("export"); s.add_argument("lib"); s.add_argument("out"); s.set_defaults(fn=cmd_strings_export)
    s = st_g.add_parser("import"); s.add_argument("lib"); s.add_argument("table"); s.add_argument("out")
    s.add_argument("--gam", help="write a .gam with the new archive spliced in")
    s.add_argument("--force", action="store_true", help="build even if some rows fail")
    s.set_defaults(fn=cmd_strings_import)

    gam_g = group("gam", ".gam container")
    s = gam_g.add_parser("split"); s.add_argument("gam"); s.add_argument("out"); s.set_defaults(fn=cmd_gam_split)
    s = gam_g.add_parser("join"); s.add_argument("gam"); s.add_argument("lib"); s.add_argument("out"); s.set_defaults(fn=cmd_gam_join)

    s = sub.add_parser("detect", help="is this .gam a BBKRPG game?"); s.add_argument("gam"); s.set_defaults(fn=cmd_detect)
    s = sub.add_parser("lint", help="check a translation table"); s.add_argument("lib"); s.add_argument("table")
    s.set_defaults(fn=cmd_lint)

    a = p.parse_args(argv)
    if a.group == "gut" and a.cmd == "disasm" and not a.all and not a.key:
        p.error("gut disasm needs a key (e.g. 1-1-1) or --all")
    try:
        a.fn(a)
    except (libmod.LibError, gutmod.GutError) as e:
        print("error:", e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
