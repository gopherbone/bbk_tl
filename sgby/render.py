"""Proportional English text for 三国霸业: a replacement for the native GamStrShow.

How the game draws text (iBaye src/comOut.c, native code in segment 0xE1):
GamStrShow(x, y, buf) at e1:$5B68 walks the string inside the clip box
c_Sx/c_Sy/c_Ex/c_Ey ($1812-$1815), drawing ASCII as 6x12 cells (GamAscii,
x += 6) and GB2312 as 12x12 cells (GamChinese, e1:$5DC9, x += 12), and wraps
per character at c_Ex. It is called near from GamStrShowS/V in the same
segment; everything else reaches it through those FAR wrappers. Arguments use
the C stack at $28: A = x, ($28)[0] = y, [1..2] = buf; the caller pops 3.

The patch:
  * inserts a 16 KiB code segment at the old data offset (page 0xF0) and moves
    the header's data offset back 16 KiB (the game follows it);
  * copies the common far-call table ($8B70-$8E23, identical in every segment)
    into the new segment and appends our entries at $8E24 in every segment
    (the dispatcher at $D2F6 reads the page through the caller's mapping and
    the address after switching, so both copies must agree);
  * replaces the body of e1:$5B68 with a tail call into our renderer.

The renderer first expands the string into a 224-byte buffer on the C stack:
  * 80+k nn (k < 0x16, nn >= 1): text-bank token, item nn of lib resource
    BANK_RES + k, loaded with the game's own ResLoadToMem (keyed, any length);
  * A0 xx: zero-width filler (2 bytes), and bytes 01-09, 0B-1F, 7F: zero-width
    filler (1 byte). Fixed-size fields and menus use these to keep their byte
    layout;
  * GB2312 pairs (lead >= A1) are kept and drawn by the original GamChinese.
Then it lays out the result: ASCII in bbk_tl Sans (proportional, 11 rows on
the 12-row line) with word wrap inside the clip box; '\n' starts a new line
at c_Sx. Each glyph is blitted as an opaque (width + 1) x 12 box through the
game's own picture calls: the OS SysPicture vector $E78E for the LCD, or the
game's virtual-screen blit (table entry $8CF9) when a virtual screen is
selected ($180F/$1810 != 0), exactly as the native GamAscii does.
"""

from __future__ import annotations

import struct

from bbkrpg import font_sans
from bbkrpg.asm6502 import assemble

SEG = 0x4000
PAGE0 = 0xE0
NEW_PAGE = 0xF0
TABLE_LO, TABLE_HI = 0x8B70, 0x8E24          # common far-call table (CPU addresses)
STRSHOW = 0x5B68                             # native GamStrShow in segment 0xE1
GAMCHINESE = 0x5DC9                          # native GamChinese in segment 0xE1
ENT_STRSHOW = 0x8E24                         # our table entries (in every segment)
ENT_CHINESE = 0x8E27
ENT_MIDSHOW = 0x8E2A
ENT_SLOTSHOW = 0x8E2D
ENT_MENUSHOW = 0x8E30
MENUSHOW_SITES = (0x66F8, 0x6BAE)            # PlcSplMenu's ldx #<$8C45: first draw, scroll redraw (0xE5)
MENU_PLEN = 3 + 0x0C                         # pLen in PlcSplMenu's frame, seen from the callee
SHOWS_VEC = 0x8C45                           # GamStrShowS (FAR, segment 0xE1)
MIDSHOW_SITE = 0x6CB8                        # PlcMidShowStr's ldx #<$8C45 (segment 0xE5)
FOOD_X_SITE = 0x6B0F                         # FgtShowState: lda #STA_LCX (segment 0xE2)
FOOD_X = 24
RESLOAD_VEC = 0x8C5D                         # ResLoadToMem(ResId u16, idx u8, ptr)
VBLIT_VEC = 0x8CF9                           # virtual-screen SysPicture
OS_BLIT = 0xE78E                             # OS SysPicture (LCD)
DISPATCH = 0xD2F6
BANK_RES = 78                                # text-bank resources 78-99 (unused ids)
TOKEN_LO, TOKEN_HI = 0x80, 0x95
FILL2 = 0xA0                                 # A0 xx: zero-width
FILL1 = 0x1F                                 # 1-byte zero-width filler
MONTH = 0x1E                                 # control: preceding 1-2 digits -> month name
BUF = 224                                    # expansion buffer on the C stack
TOKEN_MAX = 120                              # longest bank string the expander takes
LINE = 12

TABULAR = "0123456789"                        # digits share one advance


def glyph_rows(c: str) -> tuple[int, list[int]]:
    """(advance, 12 row bytes, MSB = leftmost pixel) for one character."""
    g = font_sans.GLYPHS[c]
    w = font_sans.width(c)
    shift = 0
    if c in TABULAR:
        shift = (5 - w) // 2
        w = 5
    rows = []
    for r in g:
        v = 0
        for i, p in enumerate(r[:7]):
            if p == "#":
                v |= 0x40 >> (i + shift)      # column 0 of the cell is the spacing column
        rows.append(v)
    rows += [0] * (LINE - len(rows))
    return w + 1, rows


NGLYPH = 0x7F - 0x20


def font_tables() -> tuple[bytes, bytes]:
    """(advances, rows): rows is 11 tables of NGLYPH bytes, one per glyph row."""
    adv, per = bytearray(), []
    for code in range(0x20, 0x7F):
        a, r = glyph_rows(chr(code))
        adv.append(a)
        per.append(r)
    rows = bytearray()
    for row in range(11):
        rows += bytes(p[row] for p in per)
    return bytes(adv), bytes(rows)


def advance(c: str) -> int:
    return glyph_rows(c)[0]


SRC = r"""
CSX    = $1812
CSY    = $1813
CEX    = $1814
CEY    = $1815
VSCR   = $180f
SP     = $28
PUSHA  = $daaa
PUSHW  = $daca          ; pushes $20/$21

; frame (offsets from $28 after allocation)
FBUF   = 0              ; expansion buffer, BUF bytes
FGLY   = BUF            ; glyph bitmap, 12 bytes
FX     = BUF+12         ; pen x
FY     = BUF+13         ; pen y
FI     = BUF+14         ; read index into the buffer
FW     = BUF+15         ; scratch: word width / advance
FSRC   = BUF+16         ; 2: source pointer (expansion)
FC     = BUF+18         ; current char
FAUTO  = BUF+19         ; 1 = the last line break was automatic
FR     = BUF+20         ; scratch
FSLOT  = BUF+21         ; slot mode: line break every FSLOT source bytes (0 = off)
FCNT   = BUF+22         ; source bytes since the last slot break
FRAME  = BUF+23
ARGY   = FRAME          ; caller's y, then buf ptr
ARGP   = FRAME+1

.org $5000
strshow:
        ldy #0
        beq common
; slotshow and menushow replace calls to GamStrShowS, so like it they draw
; to the LCD (gam_selectscr(NULL): VSCR = 0)
slotshow:                       ; GamShowKing: one 6-byte name slot per line
        ldy #6
        bne lcd
menushow:                       ; PlcSplMenu: one pLen-byte item per line
        tax
        ldy #MENU_PLEN
        lda (SP),y
        tay
        txa
lcd:    ldx #0
        stx VSCR
        stx VSCR+1
common: sty $27
        tax                     ; x
        php
        sei
        sec
        lda SP
        sbc #FRAME
        sta SP
        lda SP+1
        sbc #0
        sta SP+1
        plp
        lda $27
        ldy #FSLOT
        sta (SP),y
        lda #0
        ldy #FCNT
        sta (SP),y
        txa
        ldy #FX
        sta (SP),y
        ldy #ARGY
        lda (SP),y
        ldy #FY
        sta (SP),y
        ; if y + 12 > c_Ey: nothing fits
        clc
        adc #12
        cmp CEY
        beq ok0
        bcc ok0
        jmp leave
ok0:    ldy #ARGP
        lda (SP),y
        tax
        iny
        lda (SP),y
        ldy #FSRC+1
        sta (SP),y
        dey
        txa
        sta (SP),y
        jsr expand
        jsr layout
leave:  ; slotshow / menushow stand in for GamStrShowS: like its tail
        ; (GamResumeSet), restore the full-screen clip when c_ReFlag is set
        ldy #FSLOT
        lda (SP),y
        beq leave1
        lda $1811
        beq leave1
        lda #0
        sta CSX
        sta CSY
        lda #$9e
        sta CEX
        lda #$5f
        sta CEY
leave1: php
        sei
        clc
        lda SP
        adc #FRAME
        sta SP
        lda SP+1
        adc #0
        sta SP+1
        plp
        rts

; ---------------------------------------------------------------------------
; expand: copy the source string into FBUF, expanding bank tokens.
; $22/$23 = source, $24 = output index (both reloaded after far calls).
expand:
        lda #0
        sta $24
exlp:   ldy #FSLOT
        lda (SP),y
        beq exlp1
        ldy #FCNT
        cmp (SP),y
        bne exlp1
        lda #0
        sta (SP),y
        lda #$0a
        jsr exput
exlp1:  ldy #FSRC
        lda (SP),y
        sta $22
        iny
        lda (SP),y
        sta $23
        ldy #0
        lda ($22),y
        beq exend
        cmp #MONTH
        bne exlp2
        jmp exmon
exlp2:  cmp #TOKEN_LO
        bcc exone
        cmp #TOKEN_HI+1
        bcs exhz
        jmp extok
exhz:                           ; GB2312 pair or $a0 filler pair: copy both bytes
        jsr exput               ; lead byte
        jsr exadv
        ldy #FSRC
        lda (SP),y
        sta $22
        iny
        lda (SP),y
        sta $23
        ldy #0
        lda ($22),y
        beq exend
exone:  cmp #$7c                ; '|' cell separator (battle help panel): a space
        bne exone1
        lda #$20
exone1: jsr exput
        jsr exadv
        jmp exlp
exend:  ldy $24
        lda #0
        sta (SP),y
        rts

; MONTH control: replace the 1-2 digits just written with a month name
exmon:  lda #0
        sta $25                 ; value
        ldy $24
        beq exmon8
        dey
        lda (SP),y
        sec
        sbc #$30
        cmp #10
        bcs exmon8
        sta $25
        sty $24
        cpy #0
        beq exmon5
        dey
        lda (SP),y
        sec
        sbc #$30
        cmp #10
        bcs exmon5
        sty $24
        tax                     ; tens digit: value += 10 * x
exmon4: lda $25
        clc
        adc #10
        sta $25
        dex
        bne exmon4
exmon5: lda $25
        beq exmon8
        cmp #13
        bcs exmon8
        sec
        sbc #1
        sta $25
        asl a
        clc
        adc $25                 ; (n - 1) * 3
        tax
        lda MONTHS,x
        jsr exput2
        lda MONTHS+1,x
        jsr exput2
        lda MONTHS+2,x
        jsr exput2
exmon8: jsr exadv
        jmp exlp

; exput keeping X
exput2: stx $26
        jsr exput
        ldx $26
        rts

MONTHS: .byte "JanFebMarAprMayJunJulAugSepOctNovDec"

; put A at FBUF[$24] if there is room (keep the last byte for the NUL)
exput:  ldx $24
        cpx #BUF-2
        bcs exput9
        pha
        txa
        tay
        pla
        sta (SP),y
        inc $24
exput9: rts

; advance the source pointer by one (and count it for slot mode)
exadv:  ldy #FCNT
        lda (SP),y
        clc
        adc #1
        sta (SP),y
        ldy #FSRC
        lda (SP),y
        clc
        adc #1
        sta (SP),y
        iny
        lda (SP),y
        adc #0
        sta (SP),y
        rts

; bank token: lead in A, item at source+1
extok:  sec
        sbc #TOKEN_LO
        clc
        adc #<BANK_RES
        sta $25                 ; resource id (low; high is 0)
        ldy #1
        lda ($22),y
        bne extok1
        jmp exend               ; truncated token
extok1: tax                     ; item index
        ; skip the two token bytes now (far call clobbers $20-$27)
        jsr exadv
        jsr exadv
        lda $24
        cmp #BUF-TOKEN_MAX-2
        bcc extok2
        jmp exlp                ; no room: drop it
extok2: ldy #FR
        sta (SP),y              ; output index, saved across the call
        tay
        lda #0
        sta (SP),y              ; empty if the load fails
        tya
        ; ResLoadToMem(id, idx, SP + out)
        clc
        adc SP
        sta $20
        lda SP+1
        adc #0
        sta $21
        lda $25
        pha
        txa
        pha
        jsr PUSHW               ; ptr
        pla
        jsr PUSHA               ; idx
        pla
        sta $20
        lda #0
        sta $21
        jsr PUSHW               ; resource id
        ldx #<RESLOAD_VEC
        stx $26
        ldx #>RESLOAD_VEC
        stx $27
        jsr DISPATCH
        php
        sei
        clc
        lda SP
        adc #5
        sta SP
        lda SP+1
        adc #0
        sta SP+1
        plp
        ; find the NUL it wrote
        ldy #FR
        lda (SP),y
        tay
extok3: lda (SP),y
        beq extok4
        iny
        cpy #BUF-2
        bcc extok3
        lda #0
        sta (SP),y
extok4: sty $24
        jmp exlp

; ---------------------------------------------------------------------------
; layout: draw FBUF at (FX, FY) inside the clip box.
layout:
        lda #0
        ldy #FI
        sta (SP),y
        ldy #FAUTO
        sta (SP),y
lylp:   ldy #FI
        lda (SP),y
        tay
        lda (SP),y
        bne ly1
        rts
ly1:    ldy #FC
        sta (SP),y
        cmp #$0a
        bne ly2
        jsr cleareol            ; menus and slot lists: blank the rest of the row
        lda #0
        ldy #FAUTO
        sta (SP),y
        jsr newline
        bcc lyn1
        rts
lyn1:   jmp lynext1
ly2:    cmp #$a0
        bne ly3
        jmp lynext2             ; zero-width pair
ly3:    bcc ly4
        jmp lyhz
ly4:    cmp #$20
        bcs ly5
        jmp lynext1             ; control byte: zero width
ly5:    cmp #$7f
        bcc ly6
        jmp lynext1
ly6:    cmp #$20
        bne lyword
        ; space: dropped at the start of a wrapped line
        ldy #FAUTO
        lda (SP),y
        beq lysp
        ldy #FX
        lda (SP),y
        cmp CSX
        bne lysp
        jmp lynext1
lysp:   jmp lyglyph
lyword: ; first letter of a word? (previous byte is not a printable letter)
        ldy #FI
        lda (SP),y
        beq lyw1
        tay
        dey
        lda (SP),y
        cmp #$21
        bcc lyw1
        cmp #$7f
        bcs lyw1
        jmp lyglyph             ; inside a word
lyw1:   jsr wordwidth           ; -> FW
        ldy #FX
        lda (SP),y
        cmp CSX
        beq lyglyph             ; already at line start
        clc
        ldy #FW
        adc (SP),y
        bcs lyw2                ; past 255: wrap
        sec
        sbc #1
        cmp CEX
        beq lyglyph
        bcc lyglyph
lyw2:   lda #1
        ldy #FAUTO
        sta (SP),y
        jsr newline
        bcc lyglyph
        rts
lyglyph:
        ; character-level wrap for words wider than the line
        ldy #FC
        lda (SP),y
        sec
        sbc #$20
        tax
        lda ADV,x
        ldy #FW
        sta (SP),y
        ldy #FX
        clc
        adc (SP),y
        bcs lyg1
        sec
        sbc #1
        cmp CEX
        beq lyg2
        bcc lyg2
lyg1:   ldy #FX
        lda (SP),y
        cmp CSX
        beq lyg2                ; nothing to gain
        lda #1
        ldy #FAUTO
        sta (SP),y
        jsr newline
        bcc lyglyph
        rts
lyg2:   jsr drawglyph
        ldy #FW
        lda (SP),y
        ldy #FX
        clc
        adc (SP),y
        sta (SP),y
        lda #0
        ldy #FAUTO
        sta (SP),y
lynext1:
        ldy #FI
        lda (SP),y
        clc
        adc #1
        sta (SP),y
        jmp lylp
lynext2:
        ldy #FI
        lda (SP),y
        clc
        adc #2
        sta (SP),y
        jmp lylp

; GB2312 pair: wrap like the original (12 px), draw with GamChinese
lyhz:   ldy #FX
        lda (SP),y
        clc
        adc #11
        bcs lyh1
        cmp CEX
        beq lyh2
        bcc lyh2
lyh1:   ldy #FX
        lda (SP),y
        cmp CSX
        beq lyh2
        lda #1
        ldy #FAUTO
        sta (SP),y
        jsr newline
        bcc lyhz
        rts
lyh2:   ldy #FI
        lda (SP),y
        tay
        lda (SP),y
        sta $21                 ; high byte = lead
        iny
        lda (SP),y
        sta $20
        jsr PUSHW               ; Hz
        ldy #FY+2
        lda (SP),y
        jsr PUSHA               ; y
        ldy #FX+3
        lda (SP),y              ; A = x
        ldx #<ENT_CHINESE
        stx $26
        ldx #>ENT_CHINESE
        stx $27
        jsr DISPATCH
        php
        sei
        clc
        lda SP
        adc #3
        sta SP
        lda SP+1
        adc #0
        sta SP+1
        plp
        ldy #FX
        lda (SP),y
        clc
        adc #12
        sta (SP),y
        lda #0
        ldy #FAUTO
        sta (SP),y
        jmp lynext2

; cleareol: blank from the pen to c_Ex (opaque rows, like the original's
; full-width cells), in boxes of up to 8 px
cleareol:
        ldy #FX
        lda (SP),y
        cmp CEX
        beq ce1
        bcs ce9
ce1:    lda CEX
        sec
        ldy #FX
        sbc (SP),y
        clc
        adc #1                  ; pixels left
        cmp #9
        bcc ce2
        lda #8
ce2:    ldy #FW
        sta (SP),y
        lda #$20
        ldy #FC
        sta (SP),y
        jsr drawglyph
        ldy #FW
        lda (SP),y
        ldy #FX
        clc
        adc (SP),y
        bcs ce9
        sta (SP),y
        jmp cleareol
ce9:    rts

; newline: x = c_Sx, y += 12; carry set when the next line does not fit
newline:
        lda CSX
        ldy #FX
        sta (SP),y
        ldy #FY
        lda (SP),y
        clc
        adc #12
        sta (SP),y
        clc
        adc #11
        bcs nl9
        cmp CEY
        beq nl8
        bcs nl9
nl8:    clc
        rts
nl9:    sec
        rts

; wordwidth: FW = advance sum of the printable run starting at FI
wordwidth:
        lda #0
        sta $24
        ldy #FI
        lda (SP),y
        tay
ww1:    lda (SP),y
        cmp #$21
        bcc ww9
        cmp #$7f
        bcs ww9
        sty $25
        sec
        sbc #$20
        tax
        lda ADV,x
        clc
        adc $24
        bcc ww2
        lda #$ff
ww2:    sta $24
        ldy $25
        iny
        bne ww1
ww9:    lda $24
        ldy #FW
        sta (SP),y
        rts

; drawglyph: blit FC at (FX, FY), FW wide, 12 rows
drawglyph:
        ; rows -> FGLY (row 11 blank). ROWS holds 11 tables of NGLYPH bytes,
        ; one per row, so row r of glyph i is ROWS + r*NGLYPH + i.
        ldy #FC
        lda (SP),y
        sec
        sbc #$20
        clc
        adc #<ROWS
        sta $22
        lda #>ROWS
        adc #0
        sta $23
        ldx #0
dg1:    ldy #0
        lda ($22),y
        pha
        txa
        clc
        adc #FGLY
        tay
        pla
        sta (SP),y
        lda $22
        clc
        adc #NGLYPH
        sta $22
        lda $23
        adc #0
        sta $23
        inx
        cpx #11
        bne dg1
        ldy #FGLY+11
        lda #0
        sta (SP),y
        ; ex = x + w - 1, ey = y + 11 (kept in $24/$25)
        ldy #FX
        lda (SP),y
        clc
        ldy #FW
        adc (SP),y
        sec
        sbc #1
        sta $24
        ldy #FY
        lda (SP),y
        clc
        adc #11
        sta $25
        lda VSCR
        ora VSCR+1
        beq dglcd
        ; virtual screen: (x, y, ex, ey, pic, vscr, mode 0)
        lda $24
        pha
        lda $25
        pha
        lda #0
        jsr PUSHA               ; mode
        lda VSCR
        sta $20
        lda VSCR+1
        sta $21
        jsr PUSHW               ; vscr
        clc
        lda SP
        adc #FGLY+3
        sta $20
        lda SP+1
        adc #0
        sta $21
        jsr PUSHW               ; pic
        pla
        jsr PUSHA               ; ey
        pla
        jsr PUSHA               ; ex
        ldy #FY+7
        lda (SP),y
        jsr PUSHA               ; y
        ldy #FX+8
        lda (SP),y
        ldx #<VBLIT_VEC
        stx $26
        ldx #>VBLIT_VEC
        stx $27
        jsr DISPATCH
        lda #8
        jmp dgpop
dglcd:  lda $24
        pha
        lda $25
        pha
        lda #0
        jsr PUSHA               ; mode
        clc
        lda SP
        adc #FGLY+1
        sta $20
        lda SP+1
        adc #0
        sta $21
        jsr PUSHW               ; pic
        pla
        jsr PUSHA               ; ey
        pla
        jsr PUSHA               ; ex
        ldy #FY+5
        lda (SP),y
        jsr PUSHA               ; y
        ldy #FX+6
        lda (SP),y
        ldx #<OS_BLIT
        stx $26
        ldx #>OS_BLIT
        stx $27
        jsr DISPATCH
        lda #6
dgpop:  php
        sei
        clc
        adc SP
        sta SP
        lda SP+1
        adc #0
        sta SP+1
        plp
        rts

; ---------------------------------------------------------------------------
; midshow: PlcMidShowStr's call to GamStrShowS lands here. A = x already moved
; left by strlen * 3 (the native byte-width estimate); ($28) = [y, buf].
; Re-centre on the measured pixel width of the first line, then tail-call
; GamStrShowS.
midshow:
        tax
        php
        sei
        sec
        lda SP
        sbc #FRAME
        sta SP
        lda SP+1
        sbc #0
        sta SP+1
        plp
        lda #0
        ldy #FSLOT
        sta (SP),y
        txa
        ldy #FX
        sta (SP),y
        ldy #ARGP
        lda (SP),y
        sta $22
        tax
        iny
        lda (SP),y
        sta $23
        ldy #FSRC+1
        sta (SP),y
        dey
        txa
        sta (SP),y
        ; centre = x + strlen * 3 (kept in FY/FW: low/high)
        ldy #0
ms1:    lda ($22),y
        beq ms2
        iny
        bne ms1
ms2:    tya                     ; strlen (< 256)
        sta $24
        lda #0
        sta $25
        lda $24
        asl a
        rol $25
        clc
        adc $24
        sta $24
        lda $25
        adc #0
        sta $25                 ; strlen * 3
        ldy #FX
        lda (SP),y
        clc
        adc $24
        ldy #FY
        sta (SP),y
        lda $25
        adc #0
        ldy #FW
        sta (SP),y
        jsr expand
        ; width of the first line of FBUF -> $24/$25
        lda #0
        sta $24
        sta $25
        ldy #0
mw1:    lda (SP),y
        beq mw9
        cmp #$0a
        beq mw9
        cmp #$a0
        beq mw2b
        bcs mwhz
        cmp #$21-1
        bcc mw2                 ; control byte: zero width
        cmp #$7f
        bcs mw2
        sty $26
        sec
        sbc #$20
        tax
        lda ADV,x
        ldy $26
        clc
        adc $24
        sta $24
        bcc mw2
        inc $25
mw2:    iny
        bne mw1
        beq mw9
mw2b:   iny
        iny
        bne mw1
        beq mw9
mwhz:   lda $24
        clc
        adc #12
        sta $24
        bcc mw2b
        inc $25
        jmp mw2b
mw9:    ; x = centre - width / 2, clamped at 0
        lsr $25
        ror $24
        ldy #FY
        lda (SP),y
        sec
        sbc $24
        sta $24
        ldy #FW
        lda (SP),y
        sbc $25
        bcs mw10
        lda #0
        sta $24
mw10:   php
        sei
        clc
        lda SP
        adc #FRAME
        sta SP
        lda SP+1
        adc #0
        sta SP+1
        plp
        lda $24
        ldx #<SHOWS_VEC
        stx $26
        ldx #>SHOWS_VEC
        stx $27
        jmp DISPATCH

ADV:
"""


def build_segment() -> tuple[bytes, dict[str, int]]:
    adv, rows = font_tables()
    src = SRC + ".byte " + ", ".join(str(b) for b in adv) + "\nROWS:\n"
    for i in range(0, len(rows), 16):
        src += ".byte " + ", ".join(str(b) for b in rows[i:i + 16]) + "\n"
    syms_in = {"BUF": BUF, "TOKEN_LO": TOKEN_LO, "TOKEN_HI": TOKEN_HI, "BANK_RES": BANK_RES,
               "TOKEN_MAX": TOKEN_MAX, "RESLOAD_VEC": RESLOAD_VEC, "VBLIT_VEC": VBLIT_VEC,
               "OS_BLIT": OS_BLIT, "DISPATCH": DISPATCH, "ENT_CHINESE": ENT_CHINESE,
               "NGLYPH": NGLYPH, "SHOWS_VEC": SHOWS_VEC, "MONTH": MONTH,
               "MENU_PLEN": MENU_PLEN}
    org, code, syms = assemble(src, syms_in)
    assert org == 0x5000
    if len(code) > TABLE_LO - 0x5000:
        raise ValueError(f"renderer is {len(code)} bytes, overlaps the far-call table")
    return code, syms


def entries(syms) -> bytes:
    return bytes([syms["strshow"] & 0xFF, syms["strshow"] >> 8, NEW_PAGE,
                  GAMCHINESE & 0xFF, GAMCHINESE >> 8, 0xE1,
                  syms["midshow"] & 0xFF, syms["midshow"] >> 8, NEW_PAGE,
                  syms["slotshow"] & 0xFF, syms["slotshow"] >> 8, NEW_PAGE,
                  syms["menushow"] & 0xFF, syms["menushow"] >> 8, NEW_PAGE])


def hook() -> bytes:
    """New body of e1:$5B68: tail call into the renderer (A = x is kept)."""
    return bytes([0xA2, ENT_STRSHOW & 0xFF, 0x86, 0x26, 0xA2, ENT_STRSHOW >> 8, 0x86, 0x27,
                  0x4C, DISPATCH & 0xFF, DISPATCH >> 8])


# PlcSplMenu (segment 0xE5) computes the item length pLen = (c_Ex - c_Sx) / 6
# at $6438 and stores it with `ldy #$0c / sta ($28),y` at $6448. We call a stub
# in the segment's padding there instead: it stores pLen, then widens the box
# to 12 px per byte (8 px for items over 4 bytes), keeping c_Ex <= 150 by
# moving the box left. Items keep their byte length, so callers' buffers and
# the item slicing are unchanged; menu strings end each item with '\n'.
MENU_SITE = 0x6448
MENU_STUB = 0x8E40
MENU_MAX_EX = 150
MENU_SRC = r"""
CSX = $1812
CEX = $1814
.org $8e40
        ldy #$0c
        sta ($28),y
        cmp #5
        bcs w8
        asl a
        asl a
        sta $22
        asl a
        clc
        adc $22
        jmp wset
w8:     asl a
        asl a
        asl a
        bcs wcap
wset:   cmp #MAXW
        bcc wok
wcap:   lda #MAXW
wok:    sta $22
        clc
        adc CSX
        bcs shift
        cmp #MAXEX+1
        bcc setex
shift:  lda #MAXEX
        sec
        sbc $22
        sta CSX
        lda #MAXEX
setex:  sta CEX
        rts
"""


def menu_patch(out: bytearray):
    base = (0xE5 - PAGE0) * SEG - 0x5000
    assert out[base + MENU_SITE: base + MENU_SITE + 4] == bytes([0xA0, 0x0C, 0x91, 0x28])
    org, code, _ = assemble(MENU_SRC, {"MAXEX": MENU_MAX_EX, "MAXW": MENU_MAX_EX - 4})
    assert org == MENU_STUB
    stub = base + MENU_STUB
    assert all(b == 0xFF for b in out[stub: stub + len(code)])
    out[stub: stub + len(code)] = code
    out[base + MENU_SITE: base + MENU_SITE + 4] = bytes([0x20, MENU_STUB & 0xFF, MENU_STUB >> 8, 0xEA])


# Ruler selection (GamGetKingInner / GamShowKing, segment 0xE0): the name list
# was 36 px wide (x 16..52) beside the 84 px city map at x 60. Move the list to
# x 5..68 and the map (and its city markers) to x 74, centre the title over the
# map, and draw the names through slotshow (one 6-byte name slot per line).
KING_SX, KING_EX, MAP_X = 5, 68, 74
KING_SITES = [
    # (cpu address, original bytes, new bytes)
    (0x5DCF, b"\xa9\x3c", bytes([0xA9, MAP_X])),
    (0x5E04, b"\xa9\x36", bytes([0xA9, KING_EX + 2])),
    (0x5E0E, b"\xa9\x0d", bytes([0xA9, KING_SX - 3])),
    (0x5EAD, b"\xa9\x34", bytes([0xA9, KING_EX])),
    (0x5F78, b"\xa9\x34", bytes([0xA9, KING_EX])),
    (0x60DD, b"\xa9\x34", bytes([0xA9, KING_EX])),
    (0x5EB9, b"\xa9\x10", bytes([0xA9, KING_SX])),
    (0x5F84, b"\xa9\x10", bytes([0xA9, KING_SX])),
    (0x60E9, b"\xa9\x10", bytes([0xA9, KING_SX])),
    (0x627A, b"\x69\x3c", bytes([0x69, MAP_X])),
    (0x62DC, b"\xa9\x10", bytes([0xA9, KING_SX])),
    (0x62E1, b"\xa9\x34", bytes([0xA9, KING_EX])),
    (0x6320, b"\xa9\x10", bytes([0xA9, KING_SX])),
    (0x6322, bytes([0xA2, SHOWS_VEC & 0xFF, 0x86, 0x26, 0xA2, SHOWS_VEC >> 8]),
     bytes([0xA2, ENT_SLOTSHOW & 0xFF, 0x86, 0x26, 0xA2, ENT_SLOTSHOW >> 8])),
]
KING_TITLE_SITE = 0x5DA8                     # lda #KING_TX (title drawn with GamStrShowS)


def king_patch(out: bytearray, title_w: int):
    base = (0xE0 - PAGE0) * SEG - 0x5000
    for addr, old, new in KING_SITES:
        assert out[base + addr: base + addr + len(old)] == old, hex(addr)
        out[base + addr: base + addr + len(new)] = new
    t = base + KING_TITLE_SITE
    assert out[t: t + 2] == b"\xa9\x48"
    out[t + 1] = max(0, MAP_X + 42 - title_w // 2)


# Officer lists (ShowPersonPro / ShowPersonProStr / ShowPersonControl, segment
# 0xE7): the name column was ASC_WID * 8 = 48 px; widen it to NAME_COL bytes.
# The other columns' widths are data (resource 2 item 7, see sgby.layout).
NAME_COL = 10
NAME_SITES = [
    (0x621B, b"\xa9\x31", bytes([0xA9, 6 * NAME_COL + 1])),     # AddItem(48 + 1) rows
    (0x6E18, b"\xa9\x31", bytes([0xA9, 6 * NAME_COL + 1])),     # AddItem(48 + 1) header
    (0x6276, b"\x69\x18", bytes([0x69, 3 * NAME_COL])),         # PlcMidShowStr(sx + 24)
    (0x6E7F, b"\x69\x18", bytes([0x69, 3 * NAME_COL])),
] + [(a, b"\x69\x30\x38\xe9\x01", bytes([0x69, 6 * NAME_COL, 0x38, 0xE9, 0x01]))   # highlight x0 + 48 - 1
     for a in (0x736C, 0x7496, 0x753C, 0x761B, 0x76D2)]


def name_patch(out: bytearray):
    base = (0xE7 - PAGE0) * SEG - 0x5000
    for addr, old, new in NAME_SITES:
        assert out[base + addr: base + addr + len(old)] == old, hex(addr)
        out[base + addr: base + addr + len(new)] = new


# Strategy map side panel (ShowCityMap / ShowMapClear, segment 0xE8): the
# panel was x 128..158 (30 px), too narrow for city names in pinyin. Start it
# at x 112 instead, over the map's 8th tile column, and keep the cursor out of
# that column: the RIGHT key scrolls when setx >= x + 7 (was 8), and the
# opening view near the east edge starts at x = CITYMAP_W - 7 (12 - 7).
PANEL_DX = 16
PANEL_SITES = [(a, imm) for a, imm in [
    (0x8079, 0x80), (0x871F, 0x80),          # clear / border at x 128
    (0x811D, 0x83),                           # ruler portrait at x 131
    (0x81B4, 0x82), (0x82C0, 0x82),           # city / officer icons at x 130
    (0x826C, 0x8C), (0x8358, 0x8C),           # their counts at x 140
    (0x844E, 0x81), (0x8543, 0x81),           # year / month at x 129
    (0x8657, 0x82),                           # city name at x 130
]]
VIEW_SITES = [  # (segment, cpu address, original lda #imm, new imm)
    (0xE8, 0x72FF, 0x08, 0x07),              # setx >= x + 8
    (0xE8, 0x734B, 0x08, 0x07),              # x = setx - 8 + 1
    (0xE0, 0x562B, 0x04, 0x05),              # x = CITYMAP_W - 8
]


def panel_patch(out: bytearray):
    base = (0xE8 - PAGE0) * SEG - 0x5000
    for addr, imm in PANEL_SITES:
        assert out[base + addr: base + addr + 2] == bytes([0xA9, imm]), hex(addr)
        out[base + addr + 1] = imm - PANEL_DX
    for seg, addr, old, new in VIEW_SITES:
        b = (seg - PAGE0) * SEG - 0x5000 + addr
        assert out[b: b + 2] == bytes([0xA9, old]), hex(addr)
        out[b + 1] = new


def menu_px(nbytes: int) -> int:
    """Pixels per item of an nbytes menu item after the patch."""
    return min(nbytes * (12 if nbytes <= 4 else 8), MENU_MAX_EX - 4)


def patch(gam: bytes, king_title_w: int = 60) -> bytes:
    """Insert the renderer segment and reroute GamStrShow. `gam` is the
    original layout (code up to the data offset)."""
    data_off = struct.unpack_from("<I", gam, 0x42)[0]
    nseg = data_off // SEG
    assert NEW_PAGE == PAGE0 + nseg, "renderer page must follow the last code segment"
    code, syms = build_segment()
    seg = bytearray(b"\xff" * SEG)
    seg[: len(code)] = code
    t0, t1 = TABLE_LO - 0x5000, TABLE_HI - 0x5000
    seg[t0:t1] = gam[t0:t1]
    out = bytearray(gam[:data_off]) + seg + gam[data_off:]
    ent = entries(syms)
    e0 = ENT_STRSHOW - 0x5000
    for s in range(nseg + 1):
        base = s * SEG + e0
        assert all(b == 0xFF for b in out[base: base + len(ent)]), f"segment {s:x} padding in use"
        out[base: base + len(ent)] = ent
    h = (0xE1 - PAGE0) * SEG + STRSHOW - 0x5000
    out[h: h + len(hook())] = hook()
    menu_patch(out)
    # PlcSplMenu draws its items through menushow (slot mode, pLen bytes per line)
    for site in MENUSHOW_SITES:
        m = (0xE5 - PAGE0) * SEG + site - 0x5000
        assert out[m: m + 6] == bytes([0xA2, SHOWS_VEC & 0xFF, 0x86, 0x26, 0xA2, SHOWS_VEC >> 8])
        out[m + 1] = ENT_MENUSHOW & 0xFF
        out[m + 5] = ENT_MENUSHOW >> 8
    king_patch(out, king_title_w)
    name_patch(out)
    panel_patch(out)
    # battle status bar: food value x 14 -> 22, to the right of the English
    # "Food" label (status picture redrawn in sgby.images)
    f = (0xE2 - PAGE0) * SEG + FOOD_X_SITE - 0x5000
    assert out[f: f + 2] == bytes([0xA9, 0x0E])
    out[f + 1] = FOOD_X
    # PlcMidShowStr: send its GamStrShowS call through midshow (pixel centring)
    m = (0xE5 - PAGE0) * SEG + MIDSHOW_SITE - 0x5000
    assert out[m: m + 8] == bytes([0xA2, SHOWS_VEC & 0xFF, 0x86, 0x26, 0xA2, SHOWS_VEC >> 8, 0x86, 0x27])
    out[m + 1] = ENT_MIDSHOW & 0xFF
    out[m + 5] = ENT_MIDSHOW >> 8
    struct.pack_into("<I", out, 0x42, data_off + SEG)
    return bytes(out)
