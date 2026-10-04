"""Tile grayscale PNG screenshots (from bbkemu) into one contact sheet."""
import struct, sys, zlib

def load(p):
    d = open(p, "rb").read(); i = 8; idat = b""
    while i < len(d):
        n = struct.unpack(">I", d[i:i + 4])[0]; t = d[i + 4:i + 8]
        if t == b"IHDR": w, h = struct.unpack(">II", d[i + 8:i + 16])
        if t == b"IDAT": idat += d[i + 8:i + 8 + n]
        i += 12 + n
    raw = zlib.decompress(idat)
    return w, h, [raw[y * (w + 1) + 1:(y + 1) * (w + 1)] for y in range(h)]

def sheet(names, out, cols=2, pad=6):
    ims = [load(n) for n in names]; w, h = ims[0][0], ims[0][1]; rn = (len(ims) + cols - 1) // cols
    W = cols * w + (cols + 1) * pad; H = rn * h + (rn + 1) * pad; rows = []
    for r in range(H):
        row = bytearray([0x80] * W)
        for k, (_, _, im) in enumerate(ims):
            cx = pad + (k % cols) * (w + pad); cy = pad + (k // cols) * (h + pad)
            if cy <= r < cy + h: row[cx:cx + w] = im[r - cy]
        rows.append(bytes(row))
    raw = b"".join(b"\0" + r for r in rows)
    ch = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    open(out, "wb").write(b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 0, 0, 0, 0))
                          + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))

if __name__ == "__main__":
    cols = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2
    names = [a for a in sys.argv[3 if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2:]]
    sheet(names, sys.argv[1], cols)
