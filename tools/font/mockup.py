"""Render font mockups into real dialogue-box screenshots (159x96 LCD)."""
import struct, sys, zlib
sys.path.insert(0, "bbkemu/cli/py"); sys.path.insert(0, ".")
from bbkemu import BBKEmu
from bbkrpg import font_sans as F

W, H = 159, 96
FG, BG = (0x14, 0x18, 0x14), (0xa8, 0xb8, 0xa0)


def capture(e):
    import base64
    png = base64.b64decode(e.screen(scale=1)["png_base64"])
    i, idat = 8, b""
    while i < len(png):
        n = struct.unpack(">I", png[i:i + 4])[0]
        if png[i + 4:i + 8] == b"IDAT":
            idat += png[i + 8:i + 8 + n]
        i += 12 + n
    raw = zlib.decompress(idat)
    return [[raw[y * (W + 1) + 1 + x] < 0x80 for x in range(W)] for y in range(H)]


def fill(px, x0, y0, x1, y1, v=False):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[y][x] = v


def draw(px, x, y, s):
    for ch in s:
        g = F.GLYPHS.get(ch, F.GLYPHS["?"])
        for r, row in enumerate(g):
            for c, p in enumerate(row):
                if p == "#" and 0 <= x + c < W and 0 <= y + r < H:
                    px[y + r][x + c] = True
        x += len(g[0]) + 1
    return x


def wrap(text, widths):
    """Greedy word wrap into rows of the given pixel widths."""
    rows, cur, i = [], "", 0
    for word in text.split(" "):
        cand = (cur + " " + word) if cur else word
        if F.text_width(cand) <= widths[min(i, len(widths) - 1)]:
            cur = cand
        else:
            rows.append(cur)
            i += 1
            cur = word
    rows.append(cur)
    return rows


def save(path, frames, scale=3, pad=6):
    n = len(frames)
    Wt, Ht = n * W * scale + (n + 1) * pad, H * scale + 2 * pad
    out = bytearray()
    for Y in range(Ht):
        out.append(0)
        for X in range(Wt):
            k, xx = divmod(X - pad, W * scale + pad)
            yy = Y - pad
            inside = 0 <= k < n and 0 <= xx < W * scale and 0 <= yy < H * scale
            c = (FG if frames[k][yy // scale][xx // scale] else BG) if inside else (0x60, 0x60, 0x60)
            out += bytes(c)
    ch = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", Wt, Ht, 8, 2, 0, 0, 0))
                           + ch(b"IDAT", zlib.compress(bytes(out))) + ch(b"IEND", b""))


if __name__ == "__main__":
    R = "gam4980/retroarch/system/gam4980"
    with BBKEmu() as e:   # the stress build: OS font, current look
        e.load_gam("work/fmj_stress.gam", rom_dir=R)
        e.run_frames(1000)
        for k, w in [("ENTER", 60), ("EXIT", 240)]:
            e.tap(k); e.run_frames(w)
        e.tap("ENTER"); e.run_frames(150)
        os_font = capture(e)
    with BBKEmu() as e:   # original game: a portrait box to draw into
        e.load_gam("gam4980/retroarch/downloads/bbk/伏魔记.gam", rom_dir=R)
        e.run_frames(1000)
        for k, w in [("ENTER", 60), ("EXIT", 240), ("ENTER", 100)]:
            e.tap(k); e.run_frames(w)
        base = capture(e)
    line = "Little butterfly, don't fly away! Where did you go? Come back here..."
    two = [r[:] for r in base]
    fill(two, 44, 57, 150, 75); fill(two, 12, 75, 150, 94)
    rows = wrap(line, [104, 136])
    draw(two, 46, 60, rows[0]); draw(two, 14, 79, rows[1] if len(rows) > 1 else "")
    three = [r[:] for r in base]
    fill(three, 44, 57, 150, 75); fill(three, 12, 75, 150, 94)
    rows = wrap(line, [104, 104, 136])
    for (x, y), r in zip([(46, 56), (46, 68), (14, 80)], rows):
        draw(three, x, y, r)
    save("work/shots/font_mockup.png", [os_font, two, three])
    print("rows:", rows)
