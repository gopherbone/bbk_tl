"""Replace the OS DrawString call with our own proportional-font renderer.

How the engine draws text (docs/recon.md): it pushes y and a string pointer on
the cc65 C stack ($28), loads x into A, points $26/$27 at an OS jump-table
entry (0xE79A = DrawString) and calls the far-call dispatcher at $D2F6. A
table entry is 3 bytes: target address and a 16 KiB page; pages >= 0xE0 are
the game's own segments (page 0xE0 + n maps .gam offset n * 0x4000 at
$5000-$8FFF).

The patch:
  * inserts one 16 KiB segment at the end of the engine (.gam 0x48000, page
    0xF2) holding the renderer and the font, and moves the archive back
    16 KiB (header data offset), which the engine follows;
  * writes a 3-byte table entry {renderer, page 0xF2} into the 0xFF padding
    at the end of every segment that draws text, and at the same offset in
    the font segment (the dispatcher reads the page through the caller's
    mapping but the address after switching to the target page);
  * repoints each DrawString call site's $26/$27 at that entry.

The renderer draws ASCII strings in bbk_tl Sans straight into LCD RAM, opaque
over a 16-pixel cell like the OS. A string with any byte >= 0x80 (untranslated
Chinese) is handed to the original OS DrawString unchanged.
"""

from __future__ import annotations

import re

from . import font_sans
from .asm6502 import assemble

SEG = 0x4000
OS_DRAWSTRING_VEC = 0xE79A
DISPATCH = 0xD2F6
ENTRY_SEG_OFFSET = 0x3FF0          # table entry inside each caller's trailing padding
GLYPH_TOP = 3                      # glyph rows start this far below the OS cell top
CELL = 16                          # rows cleared per character, like the OS cell
TOKEN_TOP = 57                     # token pages: first row top, 12 px pitch, 3 rows
TOKEN_PITCH = 12
PORTRAIT_X = 46                    # rows 0-1 beside a portrait
LEFT_X = 14
ROW_WIDTHS_PORTRAIT = (101, 101, 133)   # keep 2 px clear of the right border (x=151)
ROW_WIDTHS_PLAIN = (133, 133, 133)
GAM_PHYS = 0x20D000                # physical address of .gam offset 0

CALL_RE = re.compile(rb"\xa2\x9a\x86\x26\xa2\xe7\x86\x27\x20\xf6\xd2")


def font_tables():
    chars = [chr(c) for c in range(0x20, 0x7F)]
    widths = bytes(font_sans.width(c) for c in chars)
    rows = bytearray()
    for c in chars:
        g = font_sans.GLYPHS[c]
        for r in g:
            v = 0
            for i, p in enumerate(r[:8]):
                if p == "#":
                    v |= 0x80 >> i
            rows.append(v)
    return widths, bytes(rows)


RENDERER = r"""
; bbk_tl DrawString replacement. Called through the OS far-call dispatcher
; with A = x and the C stack ($28) holding [y, ptr lo, ptr hi].
;  * plain ASCII strings are drawn in bbk_tl Sans on a 16-row cell (like the OS);
;  * a page token FF 8h FF 8l (14-bit page id) draws that page of the text
;    bank: up to 3 rows, 12 px apart, read from flash through DMA channel 1;
;  * anything else (Chinese) goes to the OS DrawString.
X      = $2081      ; pen x (OS DrawString's own scratch)
Y0     = $2082      ; cell top
ADV    = $2083
ROW    = $2084
SH     = $2085
D0     = $2086
D1     = $2087
M0     = $2088
M1     = $2089
K0     = $208a
K1     = $208b
BITS   = $208c
GT     = $208d      ; glyph top within the cell
CH     = $208e      ; cell height (rows cleared)
TROW   = $208f      ; token mode: row 0..2
PORT   = $2090      ; token mode: portrait box (row 0/1 start at x=46)
TP     = $2091      ; token mode: 3-byte physical text pointer
SAVED  = $2094      ; saved DMA channel 1 address (3) + INCR (1)
STR    = $2f
GP     = $31        ; glyph pointer   (saved/restored)
LP     = $33        ; LCD row pointer (saved/restored)
INCR   = $207
ADDR1  = $208
DATA1  = $00

.org $5000
drawstring:
        sta X
        ldy #0
        lda ($28),y
        sta Y0
        iny
        lda ($28),y
        sta STR
        iny
        lda ($28),y
        sta STR+1
        ldy #0
        lda (STR),y
        cmp #$ff
        bne scan
        jmp token
scan:   lda (STR),y
        beq ascii
        bmi to_os
        iny
        bne scan
to_os:  lda #<OSVEC
        sta $26
        lda #>OSVEC
        sta $27
        lda X
        jmp DISPATCH            ; tail call: the OS returns to our caller

ascii:  jsr savezp
        lda #GLYPH_TOP
        sta GT
        lda #CELL
        sta CH
strlp:  ldy #0
        lda (STR),y
        beq strdone
        jsr drawch
        inc STR
        bne strlp
        inc STR+1
        jmp strlp
strdone: jmp restzp

; ---- token: draw one page from the text bank
token:  jsr savezp
        ldy #1
        lda (STR),y
        and #$7f
        sta TP+1            ; id hi (7 bits)
        ldy #3
        lda (STR),y
        and #$7f
        asl a               ; id = hi << 7 | lo  -> (hi:lo<<1) >> 1
        lsr TP+1
        ror a
        sta TP              ; TP:TP+1 = id
        ; GP = pages + id * 3
        lda TP
        sta GP
        lda TP+1
        sta GP+1
        asl GP
        rol GP+1
        clc
        lda GP
        adc TP
        sta GP
        lda GP+1
        adc TP+1
        sta GP+1
        clc
        lda GP
        adc #<pages
        sta GP
        lda GP+1
        adc #>pages
        sta GP+1
        ldy #0
        lda (GP),y
        sta TP
        iny
        lda (GP),y
        sta TP+1
        iny
        lda (GP),y
        sta TP+2
        ; save DMA channel 1
        lda ADDR1
        sta SAVED
        lda ADDR1+1
        sta SAVED+1
        lda ADDR1+2
        sta SAVED+2
        lda INCR
        sta SAVED+3
        lda #0
        sta PORT
        lda X
        cmp #30
        bcc noport
        inc PORT
noport: lda #0
        sta GT
        lda #TCELL
        sta CH
        lda #0
        sta TROW
        jsr rowstart
toklp:  jsr fetch
        beq tokdone
        cmp #$0a
        bne tokch
        inc TROW
        jsr rowstart
        jmp toklp
tokch:  jsr drawch
        jmp toklp
tokdone:
        lda SAVED
        sta ADDR1
        lda SAVED+1
        sta ADDR1+1
        lda SAVED+2
        sta ADDR1+2
        lda SAVED+3
        sta INCR
        jmp restzp

; pen position for token row TROW
rowstart:
        lda TROW
        asl a
        asl a
        sta Y0              ; 4 * row
        asl a               ; 8 * row
        clc
        adc Y0              ; 12 * row
        adc #TOP
        sta Y0
        lda PORT
        beq left
        lda TROW
        cmp #2
        bcs left
        lda #PX
        sta X
        rts
left:   lda #LX
        sta X
        rts

; next text byte from flash (physical TP), Z set at NUL
fetch:  php
        sei
        lda TP
        sta ADDR1
        lda TP+1
        sta ADDR1+1
        lda TP+2
        sta ADDR1+2
        lda INCR
        ora #1
        sta INCR
        lda DATA1
        tax
        plp
        inc TP
        bne fetch2
        inc TP+1
        bne fetch2
        inc TP+2
fetch2: txa
        rts

savezp: pla                 ; keep our return address on top
        tax
        pla
        tay
        lda GP
        pha
        lda GP+1
        pha
        lda LP
        pha
        lda LP+1
        pha
        tya
        pha
        txa
        pha
        rts

restzp: pla
        sta LP+1
        pla
        sta LP
        pla
        sta GP+1
        pla
        sta GP
        rts

; ---- draw character A at (X, Y0) with cell height CH, glyph top GT
drawch: sec
        sbc #$20
        bcc badch
        cmp #95
        bcc okch
badch:  lda #31                 ; '?'
okch:   tax
        lda widths,x
        clc
        adc #1
        sta ADV
        clc
        adc X
        bcs clip
        cmp #160
        bcc fits
clip:   rts
fits:   lda glyph_lo,x
        sta GP
        lda glyph_hi,x
        sta GP+1
        lda X
        and #7
        sta SH
        lda X
        lsr a
        lsr a
        lsr a
        tax
        beq c0
        dex
        stx K0
        inx
        cpx #19
        bcc k1ok
        lda #$ff
        sta K1
        jmp cols
k1ok:   stx K1
        jmp cols
c0:     lda #19
        sta K0
        lda #0
        sta K1
cols:   lda #0
        sta ROW
rowlp:  lda #0
        sta BITS
        lda ROW
        sec
        sbc GT
        bcc nobits
        cmp #GLYPH_H
        bcs nobits
        tay
        lda (GP),y
        sta BITS
nobits: lda #0
        ldx ADV
mk:     sec
        ror a
        dex
        bne mk
        sta M0
        lda #0
        sta M1
        lda BITS
        sta D0
        lda #0
        sta D1
        ldx SH
        beq shdone
shl:    lsr D0
        ror D1
        lsr M0
        ror M1
        dex
        bne shl
shdone: lda Y0
        clc
        adc ROW
        cmp #96
        bcs nextrow
        cmp #66
        bcs lower
        sta LP
        lda #65
        sec
        sbc LP
lower:  sta LP
        lda #0
        sta LP+1
        ldx #5
mul:    asl LP
        rol LP+1
        dex
        bne mul
        lda LP+1
        clc
        adc #4
        sta LP+1
        ldy K0
        lda M0
        eor #$ff
        and (LP),y
        ora D0
        sta (LP),y
        ldy K1
        cpy #$ff
        beq nextrow
        lda M1
        eor #$ff
        and (LP),y
        ora D1
        sta (LP),y
nextrow: inc ROW
        lda ROW
        cmp CH
        bcs chdone
        jmp rowlp
chdone: lda X
        clc
        adc ADV
        sta X
        rts

widths:
{widths}
glyph_lo:
{glyph_lo}
glyph_hi:
{glyph_hi}
glyphs:
{glyphs}
pages:
{pages}
"""


def _bytes_lines(b: bytes) -> str:
    return "\n".join("        .byte " + ", ".join(f"${x:02x}" for x in b[i:i + 16]) for i in range(0, len(b), 16))


def build_segment(page_addrs: list[int] = ()) -> tuple[bytes, int]:
    """Assemble the font segment with a page table of physical addresses;
    returns (16 KiB segment, renderer address)."""
    widths, rows = font_tables()
    table = b"".join(a.to_bytes(3, "little") for a in page_addrs) or b"\0"
    syms = {"OSVEC": OS_DRAWSTRING_VEC, "DISPATCH": DISPATCH, "GLYPH_TOP": GLYPH_TOP,
            "GLYPH_H": font_sans.H, "CELL": CELL, "TCELL": TOKEN_PITCH, "TOP": TOKEN_TOP,
            "PX": PORTRAIT_X, "LX": LEFT_X}

    def src(lo, hi):
        return RENDERER.format(widths=_bytes_lines(widths), glyph_lo=_bytes_lines(lo), glyph_hi=_bytes_lines(hi),
                               glyphs=_bytes_lines(rows), pages=_bytes_lines(table))

    _, _, s = assemble(src(bytes(95), bytes(95)), syms)   # learn where `glyphs` lands
    base = s["glyphs"]
    addrs = [base + i * font_sans.H for i in range(95)]
    org, code, s = assemble(src(bytes(a & 0xFF for a in addrs), bytes(a >> 8 for a in addrs)), syms)
    assert org == 0x5000 and s["glyphs"] == base
    if len(code) > SEG:
        raise ValueError("font segment overflow")
    return code + b"\xff" * (SEG - len(code)), s["drawstring"]


def token(page_id: int) -> bytes:
    """The 4 bytes a script string carries to show text-bank page `page_id`."""
    if not 0 <= page_id < 1 << 14:
        raise ValueError("page id out of range")
    return bytes([0xFF, 0x80 | page_id >> 7, 0xFF, 0x80 | page_id & 0x7F])


def patch(gam: bytes, pages: list[bytes] = ()) -> tuple[bytes, dict]:
    """Return a .gam with the font segment (and a text bank holding `pages`,
    each NUL-free, rows separated by 0x0A) inserted and DrawString rerouted."""
    data_off = int.from_bytes(gam[0x42:0x46], "little")
    if data_off % SEG:
        raise ValueError(f"data offset {data_off:#x} is not segment aligned")
    nseg = data_off // SEG
    page = 0xE0 + nseg
    if page > 0xFF:
        raise ValueError("no page number left for a font segment")
    bank = bytearray()
    offs = []
    for p in pages:
        if b"\0" in p:
            raise ValueError("page text contains NUL")
        offs.append(len(bank))
        bank += p + b"\0"
    nbank = -(-len(bank) // SEG)
    bank_off = data_off + SEG                      # text bank follows the font segment
    seg, entry = build_segment([GAM_PHYS + bank_off + o for o in offs])
    # The dispatcher reads the page byte through the caller's mapping, then
    # switches pages and reads the target address at the same CPU address, so
    # the entry must also exist at that offset in the font segment.
    seg = bytearray(seg)
    if seg[ENTRY_SEG_OFFSET:ENTRY_SEG_OFFSET + 3] != b"\xff\xff\xff":
        raise ValueError("font segment too large for the table entry")
    seg[ENTRY_SEG_OFFSET:ENTRY_SEG_OFFSET + 3] = bytes([entry & 0xFF, entry >> 8, page])
    engine = bytearray(gam[:data_off])
    sites = [m.start() for m in CALL_RE.finditer(engine)]
    if not sites:
        raise ValueError("no DrawString call sites found (already patched?)")
    segs = sorted({s // SEG for s in sites})
    for n in segs:
        at = n * SEG + ENTRY_SEG_OFFSET
        if engine[at:at + 3] != b"\xff\xff\xff":
            raise ValueError(f"segment {n}: no free padding at {at:#x}")
        engine[at:at + 3] = bytes([entry & 0xFF, entry >> 8, page])
    cpu_entry = 0x5000 + ENTRY_SEG_OFFSET
    for s in sites:
        engine[s + 1] = cpu_entry & 0xFF
        engine[s + 5] = cpu_entry >> 8
    bank += b"\xff" * (nbank * SEG - len(bank))
    out = bytearray(engine) + seg + bank + gam[data_off:]
    out[0x42:0x46] = (data_off + SEG * (1 + nbank)).to_bytes(4, "little")
    return bytes(out), {"sites": len(sites), "segments": segs, "page": page, "entry": entry,
                        "pages": len(pages), "bank_bytes": len(bank.rstrip(b"\xff")), "bank_segments": nbank}
