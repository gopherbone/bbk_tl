# 三国霸业 (sgby): format and English patch

Native 4988 game (`Ver1.0`, 622,874 bytes). It does not use the BBKRPG engine.
The iBaye project (`refs/iBaye`, gitee bgwp/iBaye) is a C port of the original
source, so every function named here can be read there; the native code is the
same logic compiled to 6502.

## Layout of the .gam

| Range | Contents |
| --- | --- |
| 0x00000-0x3ffff | 16 code segments of 16 KiB (pages 0xE0-0xEF, mapped at $5000-$8FFF) |
| data offset (header 0x42) | 12x12 font `Gamhzk.bin`, 0x28000 bytes |
| + 0x28000 .. end | `dat.lib`, byte-identical to iBaye `src/dat.lib.orig` |

Every code segment carries the same far-call table at $8B70-$8E23 (3-byte
entries: address, page) followed by 0xFF padding. The dispatcher at $D2F6
reads the page through the caller's mapping and the address after switching,
so an entry must sit at the same offset in caller and target.

## dat.lib (`sgby/lib.py`)

u32 address table (ids 1-116), then resources with a 12-byte RCHEAD
{len, id, count, item_len, key, reserved}. Variable items have u16
offset/length pairs (iBaye's headers say u32). Keyed resources store
plain + key (0xC0 for UI strings, 0xC3 for names, items and descriptions).
The game reads through one 16 KiB window, so a resource must not cross a
16 KiB boundary. Ids 78-99 are unused; the English text bank lives there.

Text: resource 1 (engine strings), 64 (STRING_CONST), 11/12 (skill names and
descriptions), 58 (cities), 62/70/71/72 (officer names per period), 73/74
(item names and descriptions). Pictures: 6-byte header {u16 w, u16 h, u8
count, u8 mask}; SPE animations add a 6-byte header and 5-byte frame records
(`sgby/pic.py`).

## English renderer (`sgby/render.py`)

The native GamStrShow (e1:$5B68) tail-calls our renderer in a new segment
(page 0xF0, inserted at the old data offset; the header's data offset moves
16 KiB). It expands the string into a buffer on the C stack:

- `80+k nn`: text-bank token, item nn of resource 78+k, loaded with the game's
  own ResLoadToMem, so fixed-size fields hold any length of English;
- `1F` and `A0 xx`: zero-width fillers that keep the original byte lengths
  (the game sizes bars, centres text and slices menus by byte count);
- `1E`: month marker, which replaces the preceding number with Jan..Dec;
- `|` (battle help cells) becomes a space.

It then lays the text out in bbk_tl Sans: 11-row glyphs, proportional, with
tabular digits and word wrap inside the clip box. Each glyph is blitted
through the game's own picture calls (LCD or virtual screen). GB2312 still goes
to the native GamChinese.

Entries at $8E24.. in every segment: strshow, GamChinese, midshow
(PlcMidShowStr: centre on the measured width), slotshow (ruler list: one
6-byte slot per line), menushow (PlcSplMenu: one item per line, read pLen from
the caller's frame). Slot breaks blank the rest of the row, like the
original's opaque cells.

## Layout patches

- PlcSplMenu: the box is widened to 12 px per item byte (8 above 4 bytes).
- Ruler selection: the list moves to x 5..68 and the map to x 74.
- Officer lists: the name column is 10 cells. Column widths (resource 2 item 7)
  are re-packed so they still fit the 7 pages of `spcv[7]` (`sgby/layout.py`).
- Map side panel: starts at x 112 over the 8th tile column. The cursor
  scrolls at x + 7.
- Battle status bar: the food value moves to x 24.

## Pictures (`sgby/images.py`)

Calligraphy is kept: on the title and credits screens, small-caps English sits
in blank bands. Plain-font labels are replaced: period cards, the day box and
the status bar.

## Gotchas found on the way

- Calls that bypass GamStrShowS must select the LCD (VSCR = 0) and restore
  the clip when c_ReFlag is set, as its tail does.
- Cursor and menu keys need about 25 frames between presses in scripts. The
  map redraw takes about 20 frames, and earlier presses are dropped.
- The number dialog's HELP-for-maximum key is an iBaye addition, not native.
