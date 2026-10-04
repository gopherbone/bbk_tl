"""Assembler, font, fitter and font-patch tests (no emulator needed)."""

import os
import unittest

from bbkrpg import asm6502, fit, font_sans, fontpatch

GAM = os.path.join(os.path.dirname(__file__), "..", "gam4980", "retroarch", "downloads", "bbk", "伏魔记.gam")


class Asm(unittest.TestCase):
    def test_encodings(self):
        _, b, s = asm6502.assemble("""
        .org $5000
start:  lda #$2e
        ldx #<tbl
        stx $26
        lda ($28),y
        sta $2081
        lda $20,x
        asl a
        jmp (vec)
loop:   dey
        bne loop
vec:    .word start
tbl:    .byte >start, "A"
        """)
        self.assertEqual(b.hex(), "a92ea21686 26 b128 8d8120 b520 0a 6c1450 88 d0fd 0050 50 41".replace(" ", ""))
        self.assertEqual(s["tbl"], 0x5016)

    def test_branch_range(self):
        with self.assertRaises(asm6502.AsmError):
            asm6502.assemble(".org $5000\nl: .res 200\n bne l")


class Font(unittest.TestCase):
    def test_glyph_set(self):
        self.assertEqual(len(font_sans.GLYPHS), 95)
        for ch, g in font_sans.GLYPHS.items():
            self.assertEqual(len(g), font_sans.H, ch)
            self.assertLessEqual(len(g[0]), 7, ch)   # renderer: advance <= 8

    def test_fit_respects_widths(self):
        text = "Brother, so this is where you are! Master couldn't find you, and he's furious. " * 3
        for portrait, widths in ((True, fontpatch.ROW_WIDTHS_PORTRAIT), (False, fontpatch.ROW_WIDTHS_PLAIN)):
            ps = fit.pages(text, portrait)
            words = []
            for p in ps:
                self.assertLessEqual(len(p), 3)
                for i, row in enumerate(p):
                    self.assertLessEqual(font_sans.text_width(row), widths[i])
                    words += row.split()
            self.assertEqual(words, text.split())

    def test_forced_breaks(self):
        self.assertEqual(fit.pages("One\ntwo\fThree", False), [["One", "two"], ["Three"]])

    def test_token(self):
        for n in (0, 1, 127, 128, 16383):
            t = fontpatch.token(n)
            self.assertNotIn(0, t)
            self.assertEqual(((t[1] & 0x7F) << 7) | (t[3] & 0x7F), n)


@unittest.skipUnless(os.path.exists(GAM), "game set not present")
class Patch(unittest.TestCase):
    def test_patch_layout(self):
        data = open(GAM, "rb").read()
        out, info = fontpatch.patch(data, [b"Hello\nworld"])
        self.assertEqual(info["sites"], 55)
        off = int.from_bytes(out[0x42:0x46], "little")
        self.assertEqual(off, 0x48000 + 2 * 0x4000)
        self.assertEqual(out[off:], data[0x48000:])
        self.assertEqual(out[0x48000 + fontpatch.ENTRY_SEG_OFFSET + 2], 0xF2)
        self.assertEqual(out[0x4C000:0x4C00C], b"Hello\nworld\0")
        self.assertNotIn(fontpatch.CALL_RE.pattern, out[:0x48000])


if __name__ == "__main__":
    unittest.main()


class EngineText(unittest.TestCase):
    def test_export_ids_unique(self):
        from bbkrpg import engine_text
        rows = engine_text.export()
        self.assertEqual(len({r["id"] for r in rows}), len(rows))
        menu = [r for r in rows if r["id"].startswith("ENG/13891.")]
        self.assertEqual([r["zh"] for r in menu], ["属性", "魔法", "物品", "系统"])

    def test_inline_tokens(self):
        from bbkrpg import engine_text
        bank = [b""] * engine_text.RESERVED_SHORT
        self.assertEqual(engine_text.inline_token(bank, b"-", 2), bytes([0xFD, 0x80]))
        t = engine_text.inline_token(bank, b"Load", 8)
        self.assertEqual(len(t), 8)
        self.assertEqual(t[4:], b"\xfc\x80\xfc\x80")
        i = ((t[1] & 0x7F) << 7) | (t[3] & 0x7F)
        self.assertEqual(bank[i], b"Load")

    @unittest.skipUnless(os.path.exists(GAM), "game set not present")
    def test_original_bytes_present(self):
        from bbkrpg import engine_text
        data = open(GAM, "rb").read()
        for off, zh, _ in engine_text.ENTRIES:
            raw = zh.encode("gb2312")
            self.assertEqual(data[off:off + len(raw)], raw, hex(off))


class Bps(unittest.TestCase):
    def test_round_trip_and_checks(self):
        import random
        from bbkrpg import bps
        rnd = random.Random(1)
        src = bytes(rnd.randrange(256) for _ in range(5000))
        tgt = src[:1000] + b"inserted" * 50 + src[1000:3000] + bytes(200) + src[3500:]
        p = bps.create(src, tgt, b"meta")
        self.assertEqual(bps.apply(p, src), tgt)
        self.assertLess(len(p), 1000)
        with self.assertRaises(ValueError):
            bps.apply(p, tgt)
