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
OS_MSGBOX_VEC = 0xE953
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
DIALOGUE_Y = 58                    # y of a say box's first row; other page tokens are blocks
BLOCK_PITCH = 11

# OS calls we take over: (OS jump-table vector, renderer routine, padding offset
# of the 3-byte entry in every calling segment and in the font segment).
REROUTES = [
    (0xE79A, "drawstring", 0x3FF0),     # DrawString
    (0xE953, "msgbox", 0x3FF3),         # message box
]


def call_re(vec: int):
    """ldx #lo / stx $26 / ldx #hi / stx $27 / jsr $D2F6 for an OS vector."""
    return re.compile(bytes([0xA2, vec & 0xFF, 0x86, 0x26, 0xA2, vec >> 8, 0x86, 0x27, 0x20, 0xF6, 0xD2]))


CALL_RE = call_re(0xE79A)


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
;  * inline tokens inside a string: FE 8h FE 8l (4 bytes) or FD 8i (2 bytes,
;    id < 128) draw a text-bank string at the pen, advancing at least the
;    slot's original width (32 / 16 px); FC xx is a blank 16 px filler;
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
MINADV = $2098      ; inline token: pen x the slot must reach
TLEN   = $2099      ; inline token: bytes it occupies
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
        bne scan0
        jmp token
        ; any byte >= $80 that is not an inline token -> let the OS draw it
scan0:  ldy #0
scan:   lda (STR),y
        beq ascii
        bpl scan1
        cmp #$fe
        beq skip4
        cmp #$fc
        bcc to_os
        iny                     ; $fc / $fd: 2 bytes
scan1:  iny
        bne scan
        beq ascii
skip4:  iny
        iny
        iny
        iny
        bne scan
        beq ascii
to_os:  lda #<OSVEC
        sta $26
        lda #>OSVEC
        sta $27
        lda X
        jmp DISPATCH            ; tail call: the OS returns to our caller

ascii:  jsr savezp
        lda #0
        sta NOWRAP
        lda #GLYPH_TOP
        sta GT
        lda #CELL
        sta CH
        jsr dmasave
        jsr drawstr
        jsr dmarest
        jmp restzp

; draw the string at STR (ASCII + inline tokens) at (X, Y0) with GT/CH.
; Unless NOWRAP, wrap like the OS DrawString does, on its 8 px grid: OSX
; counts 8 px per byte; at OSX >= 153 the pen moves to x=0 and 16 px down,
; and drawing stops once y >= 81. Engine layouts that rely on the OS wrap
; (the opening scroll) keep their rows; glyphs are still proportional.
drawstr:
        lda X
        sta OSX
strlp:  ldy #0
        lda (STR),y
        beq strdone
        pha
        lda NOWRAP
        bne nowrap
        lda OSX
        cmp #153
        bcc nowrap
        jsr padrow
        lda #0
        sta OSX
        sta X
        lda Y0
        clc
        adc #16
        sta Y0
        cmp #81
        bcc nowrap
        pla
        rts
strdone: lda NOWRAP
        bne sdr
        jsr padrow
sdr:    rts

; clear the rest of the OS grid span (the OS's 8 px cells would have covered it)
padrow: lda X
        cmp OSX
        bcs padx
        cmp #155
        bcs padx
        lda #$20
        jsr drawch
        jmp padrow
padx:   rts
nowrap: pla
        cmp #$fc
        bcs special
        jsr drawch
        lda OSX
        clc
        adc #8
        sta OSX
        lda #1
advstr: clc
        adc STR
        sta STR
        bcc strlp
        inc STR+1
        jmp strlp
special:
        cmp #$fc
        bne inl
        lda X                   ; $fc: blank 16 px
        clc
        adc #16
        sta X
        lda OSX
        clc
        adc #16
        sta OSX
        lda #2
        jmp advstr
inl:    ; $fd id (2 bytes, min 16 px) or $fe hi $fe lo (4 bytes, min 32 px)
        cmp #$fe
        beq inl4
        ldy #1
        lda (STR),y
        and #$7f
        sta TP
        lda #0
        sta TP+1
        lda #16
        sta MINADV
        lda #2
        sta TLEN
        jmp inlgo
inl4:   ldy #1
        lda (STR),y
        and #$7f
        sta TP+1
        ldy #3
        lda (STR),y
        and #$7f
        asl a
        lsr TP+1
        ror a
        sta TP
        lda #32
        sta MINADV
        lda #4
        sta TLEN
inlgo:  lda X
        clc
        adc MINADV
        sta MINADV              ; now: minimum pen x after the slot
        jsr lookup
inllp:  jsr fetch
        beq inlend
        cmp #$0a
        beq inlend
        jsr drawch
        jmp inllp
inlend: lda X
        cmp MINADV
        bcs inlx
        lda MINADV
        sta X
inlx:   lda TLEN            ; OSX += 8 px per byte of the token
        asl a
        asl a
        asl a
        clc
        adc OSX
        sta OSX
        lda TLEN
        jmp advstr

; TP:TP+1 = page id  ->  TP..TP+2 = physical address of its text (clobbers GP)
lookup: lda TP
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
        rts

dmasave: lda ADDR1
        sta SAVED
        lda ADDR1+1
        sta SAVED+1
        lda ADDR1+2
        sta SAVED+2
        lda INCR
        sta SAVED+3
        rts

dmarest: lda SAVED
        sta ADDR1
        lda SAVED+1
        sta ADDR1+1
        lda SAVED+2
        sta ADDR1+2
        lda SAVED+3
        sta INCR
        rts

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
        jsr lookup
        jsr dmasave
        lda #0
        sta PORT
        sta BLOCK
        lda Y0
        cmp #DLG_Y
        beq dlgmode
        ; block mode: rows from the call's own (x, y), 11 px apart
        inc BLOCK
        lda X
        sta BLKX
        ldx Y0
        dex
        stx BLKY
        lda #BLK_PITCH
        sta CH
        jmp tokgo
dlgmode: lda X
        cmp #30
        bcc noport
        inc PORT
noport: lda #TCELL
        sta CH
tokgo:  lda #0
        sta GT
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
        jsr dmarest
        jmp restzp

; pen position for token row TROW
rowstart:
        lda BLOCK
        beq rsdlg
        lda #0              ; block: y = BLKY + 11 * row (16-bit), x = BLKX
        sta RW
        lda TROW
        asl a
        rol RW
        sta Y0              ; 2r
        asl a
        rol RW
        asl a
        rol RW              ; 8r (RW = high byte)
        clc
        adc Y0              ; 10r
        bcc rs1
        inc RW
rs1:    clc
        adc TROW            ; 11r
        bcc rs2
        inc RW
rs2:    clc
        adc BLKY
        bcc rs3
        inc RW
rs3:    sta Y0
        lda RW
        beq rs4
        lda #$ff            ; past the bottom: rows are skipped
        sta Y0
rs4:    lda BLKX
        sta X
        rts
rsdlg:  lda TROW
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
        lda #PX0
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
        cpy #19                 ; x 0-7: byte 19 of the previous memory row
        bne k0go
        jsr lpup
k0go:   lda M0
        eor #$ff
        and (LP),y
        ora D0
        sta (LP),y
        cpy #19
        bne k0done
        jsr lpdown
k0done: ldy K1
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

; The LCD reads each display row as 20 bytes starting 13 bytes before its
; memory row: x 0-7 are byte 19 of the previous row (as the OS clears them),
; x 8-159 bytes 0-18 of the row itself. Y is preserved.
lpup:   lda LP
        sec
        sbc #32
        sta LP
        bcs lpu1
        dec LP+1
lpu1:   rts
lpdown: lda LP
        clc
        adc #32
        sta LP
        bcc lpd1
        inc LP+1
lpd1:   rts

; ---- msgbox: replacement for the OS message box (vector E953).
; C stack: [text ptr lo, hi, mode lo, hi]. Draws a centred framed box with the
; text and waits like the OS (mwait). Text: an FE token alone (rows from the bank,
; separated by \n) or a one-row string (ASCII + inline tokens).
MW     = $209a      ; widest row (px, incl. trailing 1 px spacing)
NR     = $209b      ; rows
BX     = $209c      ; box left
BY     = $209d      ; box top
BW     = $209e      ; box width
BH     = $209f      ; box height
PX     = $20a0      ; plot x
PY     = $20a1      ; plot y
RW     = $20a2      ; row width accumulator
TP0    = $20a3      ; saved bank pointer (3)
BANKMODE = $20a6
BLOCK  = $20a7      ; token page drawn as a block at the call's (x, y)
BLKX   = $20a8
BLKY   = $20a9
OSX    = $20aa      ; OS-grid pen x for wrapping
NOWRAP = $20ab      ; nonzero: never wrap (msgbox)

msgbox: ldy #0
        lda ($28),y
        sta STR
        iny
        lda ($28),y
        sta STR+1
        ldy #0
mscan:  lda (STR),y
        beq msgok
        bpl mscan1
        cmp #$fe
        beq mskip4
        cmp #$fc
        bcc msg_os
        iny
mscan1: iny
        bne mscan
        beq msgok
mskip4: iny
        iny
        iny
        iny
        bne mscan
        beq msgok
msg_os: lda #<OSMSG
        sta $26
        lda #>OSMSG
        sta $27
        jmp DISPATCH

msgok:  jsr savezp
        jsr dmasave
        lda #0
        sta MW
        sta BANKMODE
        lda #1
        sta NR
        ; bank mode: the string is exactly FE hi FE lo NUL
        ldy #0
        lda (STR),y
        cmp #$fe
        bne minline
        ldy #4
        lda (STR),y
        bne minline
        inc BANKMODE
        jsr tokid4
        jsr lookup
        lda TP
        sta TP0
        lda TP+1
        sta TP0+1
        lda TP+2
        sta TP0+2
        lda #0
        sta NR
mbrow:  lda #0
        sta RW
mbch:   jsr fetch
        beq mbend
        cmp #$0a
        beq mbnl
        jsr chwidth
        jmp mbch
mbnl:   jsr rowmax
        inc NR
        jmp mbrow
mbend:  jsr rowmax
        inc NR
        jmp mdims
minline:
        jsr strwidth
        lda RW
        sta MW
mdims:  ; BW = MW + 7 (4 px padding each side, minus trailing spacing), max 155
        lda MW
        clc
        adc #7
        bcs mwide
        cmp #156
        bcc mwok
mwide:  lda #155
mwok:   sta BW
        lda #159
        sec
        sbc BW
        lsr a
        sta BX
        ; BH = NR * 12 + 7
        lda NR
        asl a
        asl a
        sta BH
        asl a
        clc
        adc BH
        adc #7
        sta BH
        lda #95
        sec
        sbc BH
        lsr a
        sta BY
        jsr drawbox
        ; text
        lda #0
        sta GT
        lda #GLYPH_H
        sta CH
        lda BY
        clc
        adc #4
        sta Y0
        lda BX
        clc
        adc #4
        sta X
        lda BANKMODE
        beq mtxt_inline
        lda TP0
        sta TP
        lda TP0+1
        sta TP+1
        lda TP0+2
        sta TP+2
mtb:    jsr fetch
        beq mdone
        cmp #$0a
        bne mtbch
        lda Y0
        clc
        adc #12
        sta Y0
        lda BX
        clc
        adc #4
        sta X
        jmp mtb
mtbch:  jsr drawch
        jmp mtb
mtxt_inline:
        lda #1
        sta NOWRAP
        jsr drawstr
mdone:  jsr dmarest
        jsr mwait
        jmp restzp

; ---- mwait: wait like the OS box does (OS page 9 $8195): a key (message 1)
; closes it; a nonzero timeout (C-stack arg 2, in timer ticks: message 6, about
; 100 a second) closes it too, e.g. "Got: X" notices and scene banners (100).
; A zero timeout waits for a key (script message boxes). Frame of 12 bytes on
; the C stack: [0..7] message buffer, [8] old timer, [9..10] ticks; the caller's
; timeout is then at [14..15].
mwait:  php
        sei
        sec
        lda $28
        sbc #12
        sta $28
        lda $29
        sbc #0
        sta $29
        plp
        ldy #9
        lda #0
        sta ($28),y
        iny
        sta ($28),y
        jsr mwto
        beq mwloop
        ldx #$b8                ; current timer
        ldy #$e7
        jsr farcall
        ldy #8
        sta ($28),y
        cmp #1
        bcc mwt1
        ldx #$b5                ; stop it
        ldy #$e7
        jsr farcall
mwt1:   lda #1                  ; start ours
        ldx #$b2
        ldy #$e7
        jsr farcall
mwloop: ldx #$35                ; get message into the buffer
        jsr msgcall
        beq mwloop
        ldy #0
        lda ($28),y
        cmp #1
        beq mwend               ; key
        cmp #$0a
        bne mwtick
        ldy #1                  ; system event 3: let the OS handle it, then close
        lda ($28),y
        cmp #3
        bne mwloop
        iny
        lda ($28),y
        bne mwloop
        ldx #$2f
        jsr msgcall
        jmp mwend
mwtick: cmp #6
        bne mwloop
        jsr mwto
        beq mwloop
        ldy #9
        lda ($28),y
        clc
        adc #1
        sta ($28),y
        iny
        lda ($28),y
        adc #0
        sta ($28),y
        ldy #15                 ; ticks >= timeout?
        cmp ($28),y
        bcc mwloop
        bne mwend
        ldy #9
        lda ($28),y
        ldy #14
        cmp ($28),y
        bcc mwloop
mwend:  jsr mwto
        beq mwfree
        ldx #$b5                ; stop our timer, restart the old one
        ldy #$e7
        jsr farcall
        ldy #8
        lda ($28),y
        beq mwfree
        ldx #$b2
        ldy #$e7
        jsr farcall
mwfree: php
        sei
        clc
        lda $28
        adc #12
        sta $28
        lda $29
        adc #0
        sta $29
        plp
        rts

; Z clear when the caller's timeout is nonzero
mwto:   ldy #14
        lda ($28),y
        iny
        ora ($28),y
        rts

; OS call $E9xx (low byte in X) with the frame's message buffer as its C-stack
; argument; returns its A (Z set when zero)
msgcall:
        lda $28
        sta $20
        lda $29
        sta $21
        jsr $daca               ; push the buffer pointer
        ldy #$e9
        jsr farcall
        tax
        php
        sei
        clc
        lda $28
        adc #2
        sta $28
        lda $29
        adc #0
        sta $29
        plp
        txa
        rts

; far call to the OS jump-table entry Y:X (A passes through)
farcall:
        stx $26
        sty $27
        jmp DISPATCH

; RW = max(RW, ...) helpers
rowmax: lda RW
        cmp MW
        bcc rmx
        sta MW
rmx:    rts

; RW += width(A) + 1
chwidth:
        sec
        sbc #$20
        bcc cwbad
        cmp #95
        bcc cwok
cwbad:  lda #31
cwok:   tax
        lda widths,x
        sec
        adc RW
        sta RW
        rts

; RW = width of the one-row string at STR (ASCII + inline tokens)
strwidth:
        lda #0
        sta RW
        lda STR
        sta GP
        lda STR+1
        sta GP+1
        ldy #0
swl:    lda (GP),y
        beq swdone
        cmp #$fc
        bcs swspec
        sty TROW
        jsr chwidth
        ldy TROW
        iny
        bne swl
swdone: rts
swspec: cmp #$fc
        bne swtok
        lda RW
        clc
        adc #16
        sta RW
        iny
        iny
        bne swl
        rts
swtok:  ; FD (2 bytes) or FE (4 bytes): add the bank text width
        sty TROW
        cmp #$fe
        beq swt4
        iny
        lda (GP),y
        and #$7f
        sta TP
        lda #0
        sta TP+1
        lda #2
        jmp swtgo
swt4:   iny
        lda (GP),y
        and #$7f
        sta TP+1
        iny
        iny
        lda (GP),y
        and #$7f
        asl a
        lsr TP+1
        ror a
        sta TP
        lda #4
swtgo:  clc
        adc TROW
        sta TROW            ; index after the token
        lda GP
        pha
        lda GP+1
        pha
        jsr lookup
swtl:   jsr fetch
        beq swte
        cmp #$0a
        beq swte
        jsr chwidth
        jmp swtl
swte:   pla
        sta GP+1
        pla
        sta GP
        ldy TROW
        jmp swl

; TP:TP+1 = id of the FE token at STR
tokid4: ldy #1
        lda (STR),y
        and #$7f
        sta TP+1
        ldy #3
        lda (STR),y
        and #$7f
        asl a
        lsr TP+1
        ror a
        sta TP
        rts

; box: white inside, 1 px black border, 1 px shadow right and bottom
drawbox:
        lda BY
        sta PY
dbrow:  lda BX
        sta PX
dbcol:  ldy #0              ; 0 = white
        lda PY
        cmp BY
        beq dbblack
        lda BY
        clc
        adc BH
        sec
        sbc #1
        cmp PY
        beq dbblack
        lda PX
        cmp BX
        beq dbblack
        lda BX
        clc
        adc BW
        sec
        sbc #1
        cmp PX
        bne dbplot
dbblack: ldy #1
dbplot: jsr plot
        inc PX
        lda BX
        clc
        adc BW
        cmp PX
        bne dbcol
        ; shadow pixel at the right edge (rows below the top)
        lda PY
        cmp BY
        beq dbnosh
        ldy #1
        jsr plot
dbnosh: inc PY
        lda BY
        clc
        adc BH
        cmp PY
        bne dbrow
        ; bottom shadow row
        lda BX
        sta PX
        inc PX
dbsh:   ldy #1
        jsr plot
        inc PX
        lda BX
        clc
        adc BW
        clc
        adc #1
        cmp PX
        bne dbsh
        rts

; set (Y=1) or clear (Y=0) pixel (PX, PY)
plot:   sty BITS
        lda PX
        cmp #159
        bcs plotx
        lda PY
        cmp #96
        bcs plotx
        cmp #66
        bcs plow
        sta LP
        lda #65
        sec
        sbc LP
plow:   sta LP
        lda #0
        sta LP+1
        ldx #5
plm:    asl LP
        rol LP+1
        dex
        bne plm
        lda LP+1
        clc
        adc #4
        sta LP+1
        lda PX
        lsr a
        lsr a
        lsr a
        tay
        beq plc0
        dey
        jmp plby
plc0:   jsr lpup                ; x 0-7: byte 19 of the previous memory row
        ldy #19
plby:   lda PX
        and #7
        tax
        lda #$80
plsh:   cpx #0
        beq plmask
        lsr a
        dex
        jmp plsh
plmask: ldx BITS
        beq plclr
        ora (LP),y
        sta (LP),y
plotx:  rts
plclr:  eor #$ff
        and (LP),y
        sta (LP),y
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


def build_segment(page_addrs: list[int] = (), top: int = TOKEN_TOP) -> tuple[bytes, dict]:
    """Assemble the font segment with a page table of physical addresses;
    returns (16 KiB segment, symbols). `top` is the first dialogue row's top
    (games draw the say box at slightly different heights)."""
    widths, rows = font_tables()
    table = b"".join(a.to_bytes(3, "little") for a in page_addrs) or b"\0"
    syms = {"OSVEC": OS_DRAWSTRING_VEC, "DISPATCH": DISPATCH, "GLYPH_TOP": GLYPH_TOP,
            "GLYPH_H": font_sans.H, "CELL": CELL, "TCELL": TOKEN_PITCH, "TOP": top,
            "PX0": PORTRAIT_X, "LX": LEFT_X, "OSMSG": OS_MSGBOX_VEC, "DLG_Y": DIALOGUE_Y, "BLK_PITCH": BLOCK_PITCH}

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
    return code + b"\xff" * (SEG - len(code)), s


def token(page_id: int) -> bytes:
    """The 4 bytes a script string carries to show text-bank page `page_id`."""
    if not 0 <= page_id < 1 << 14:
        raise ValueError("page id out of range")
    return bytes([0xFF, 0x80 | page_id >> 7, 0xFF, 0x80 | page_id & 0x7F])


def patch(gam: bytes, pages: list[bytes] = (), top: int = TOKEN_TOP) -> tuple[bytes, dict]:
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
    seg, syms = build_segment([GAM_PHYS + bank_off + o for o in offs], top)
    # The dispatcher reads the page byte through the caller's mapping, then
    # switches pages and reads the target address at the same CPU address, so
    # each entry must also exist at that offset in the font segment.
    seg = bytearray(seg)
    engine = bytearray(gam[:data_off])
    report = {}
    for vec, routine, slot in REROUTES:
        entry = syms[routine]
        ent = bytes([entry & 0xFF, entry >> 8, page])
        if seg[slot:slot + 3] != b"\xff\xff\xff":
            raise ValueError("font segment too large for the table entries")
        seg[slot:slot + 3] = ent
        sites = [m.start() for m in call_re(vec).finditer(engine)]
        if not sites:
            raise ValueError(f"no call sites for OS vector {vec:#x} (already patched?)")
        segs = sorted({x // SEG for x in sites})
        for n in segs:
            at = n * SEG + slot
            if engine[at:at + 3] != b"\xff\xff\xff":
                raise ValueError(f"segment {n}: no free padding at {at:#x}")
            engine[at:at + 3] = ent
        cpu_entry = 0x5000 + slot
        for x in sites:
            engine[x + 1] = cpu_entry & 0xFF
            engine[x + 5] = cpu_entry >> 8
        report[routine] = {"sites": len(sites), "segments": segs}
    bank += b"\xff" * (nbank * SEG - len(bank))
    out = bytearray(engine) + seg + bank + gam[data_off:]
    out[0x42:0x46] = (data_off + SEG * (1 + nbank)).to_bytes(4, "little")
    return bytes(out), {"sites": report["drawstring"]["sites"], "reroutes": report, "page": page,
                        "pages": len(pages), "bank_bytes": len(bank.rstrip(b"\xff")), "bank_segments": nbank}
