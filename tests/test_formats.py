"""Round-trip and relocation tests over the four archives in BBKRPGSimulator.

Run: python3 -m unittest discover -s tests
The archives come from refs/BBKRPGSimulator (git clone
https://github.com/stratosblue/BBKRPGSimulator refs/BBKRPGSimulator).
"""

import os
import tempfile
import unittest

from bbkrpg import gam, gut, lib, lint, strings

ASSETS = os.path.join(os.path.dirname(__file__), "..", "refs", "BBKRPGSimulator", "src",
                      "BBKRPGSimulator.Winform", "Assets")
ARCHIVES = ["fmj.LIB", "jy.lib", "cb.lib", "xkx.lib"]


def load(name):
    with open(os.path.join(ASSETS, name), "rb") as f:
        return f.read()


@unittest.skipUnless(os.path.isdir(ASSETS), "reference archives not cloned")
class RoundTrip(unittest.TestCase):
    def test_lib_pack_identity(self):
        for name in ARCHIVES:
            with self.subTest(name):
                raw = load(name)
                self.assertEqual(lib.pack(lib.parse(raw)), raw)

    def test_lib_dir_identity(self):
        for name in ARCHIVES:
            with self.subTest(name), tempfile.TemporaryDirectory() as t:
                raw = load(name)
                lib.unpack(lib.parse(raw), t)
                self.assertEqual(lib.pack(lib.load_dir(t)), raw)

    def test_gut_listing_identity(self):
        for name in ARCHIVES:
            L = lib.parse(load(name))
            for k in L.keys_of(1):
                with self.subTest(name=name, key=k):
                    blob = L.res[k]
                    g = gut.parse(blob)
                    self.assertEqual(gut.build(g, gut.target_map(g)), blob)
                    self.assertEqual(gut.asm(gut.disasm(g)), blob)

    def test_strings_noop_import_identity(self):
        for name in ARCHIVES:
            with self.subTest(name):
                raw = load(name)
                L = lib.parse(raw)
                rows = strings.export(L)
                self.assertTrue(rows)
                built, problems = strings.apply(L, rows)   # no en filled in
                self.assertEqual(problems, [])
                self.assertEqual(lib.pack(built), raw)


@unittest.skipUnless(os.path.isdir(ASSETS), "reference archives not cloned")
class Relocation(unittest.TestCase):
    def _shape(self, g):
        """Instruction stream with jumps as instruction indexes and strings dropped."""
        tm = gut.target_map(g)
        out = []
        for i in g.code:
            args = []
            for k, v in zip(i.kinds, i.args):
                if k == "a":
                    args.append(("->", tm[v]) if v else 0)
                elif k != "s":
                    args.append(v)
            out.append((i.op, tuple(args)))
        ev = [tm[a] if a else None for a in g.events]
        return out, ev

    def test_longer_text_relocates(self):
        for name in ARCHIVES:
            with self.subTest(name):
                L = lib.parse(load(name))
                rows = strings.export(L)
                for r in rows:
                    if r["id"].startswith("gut/") and r["kind"] != "menu":
                        r["en"] = "Lorem ipsum dolor sit amet " * 2
                built, problems = strings.apply(L, rows)
                self.assertEqual(problems, [])
                packed = lib.pack(built)
                again = lib.parse(packed)
                for k in L.keys_of(1):
                    old, new = gut.parse(L.res[k]), gut.parse(again.res[k])
                    self.assertEqual(self._shape(old), self._shape(new), k)
                # untouched resources survive byte for byte
                for k in L.order:
                    if k[0] != 1:
                        self.assertEqual(again.res[k], L.res[k], k)

    def test_name_field_limits(self):
        L = lib.parse(load("fmj.LIB"))
        rows = [r for r in strings.export(L) if r["kind"] == "grs.name"][:2]
        rows[0]["en"] = "Headband"
        rows[1]["en"] = "Much Too Long Name"
        built, problems = strings.apply(L, rows)
        self.assertEqual(len(problems), 1)
        self.assertIn("field holds 11", problems[0])
        k = lib.parse_key(rows[0]["id"].split("/")[1])
        self.assertEqual(built.res[k][6:15], b"Headband\0")

    def test_lint_flags_hanzi_and_menu(self):
        L = lib.parse(load("fmj.LIB"))
        rows = strings.export(L)
        say = next(r for r in rows if r["kind"] == "say")
        say["en"] = "Hello 你好"
        errors, _ = lint.lint(L, [say])
        self.assertTrue(any("non-ASCII" in e for e in errors))


GAMES = os.path.join(os.path.dirname(__file__), "..", "gam4980", "retroarch", "downloads", "bbk")


@unittest.skipUnless(os.path.isdir(GAMES), "gam4980 game set not present")
class RealGames(unittest.TestCase):
    def read(self, name):
        with open(os.path.join(GAMES, name), "rb") as f:
            return f.read()

    def test_fmj_gam(self):
        data = self.read("伏魔记.gam")
        blob, h = gam.split(data)
        self.assertEqual((h.offset, h.name, h.entry), (0x48000, "伏魔记", 0x5046))
        L = lib.parse(blob)
        self.assertEqual(lib.pack(L), blob)
        self.assertEqual(gam.join(data, lib.pack(L)), data)
        for k in L.keys_of(1):
            g = gut.parse(L.res[k])
            self.assertEqual(gut.asm(gut.disasm(g)), L.res[k], k)

    def test_fmj_gam_grows(self):
        data = self.read("伏魔记.gam")
        L = lib.parse(gam.split(data)[0])
        rows = strings.export(L)
        for r in rows:
            if r["kind"] == "say":
                r["en"] = "The quick brown fox jumps over the lazy dog. " * 3
        built, problems = strings.apply(L, rows)
        self.assertEqual(problems, [])
        out = gam.join(data, lib.pack(built))
        self.assertGreater(len(out), len(data))
        self.assertEqual(out[:0x48000], data[:0x48000])
        again = lib.parse(gam.split(out)[0])
        self.assertEqual(len(again.order), len(L.order))

    def test_all_bbkrpg_archives_round_trip(self):
        n = 0
        for name in sorted(os.listdir(GAMES)):
            data = self.read(name)
            hits = gam.find(data)
            if not hits:
                continue
            n += 1
            with self.subTest(name):
                blob = data[hits[0].offset:]
                self.assertEqual(lib.pack(lib.parse(blob)), blob)
        self.assertGreater(n, 90)


if __name__ == "__main__":
    unittest.main()
