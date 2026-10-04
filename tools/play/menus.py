"""Main-menu navigation by looking at the screen (the selected item is inverted)."""
import base64, struct, zlib

W, H = 159, 96
MAIN_ROWS = [(27, 42), (43, 58), (59, 74), (75, 90)]   # 属性 魔法 物品 系统, x 21..50


def pixels(e):
    png = base64.b64decode(e.screen(scale=1)["png_base64"])
    i, idat = 8, b""
    while i < len(png):
        n = struct.unpack(">I", png[i:i + 4])[0]
        if png[i + 4:i + 8] == b"IDAT":
            idat += png[i + 8:i + 8 + n]
        i += 12 + n
    raw = zlib.decompress(idat)
    return [[raw[y * (W + 1) + 1 + x] < 0x80 for x in range(W)] for y in range(H)]


def dark(px, x0, x1, y0, y1):
    n = sum(px[y][x] for y in range(y0, y1) for x in range(x0, x1))
    return n / ((x1 - x0) * (y1 - y0))


def main_selected(e, x0=21, x1=50):
    px = pixels(e)
    scores = [dark(px, x0, x1, a, b) for a, b in MAIN_ROWS]
    best = max(range(4), key=lambda i: scores[i])
    return best if scores[best] > 0.45 else None


def idle(e):
    r = e.regs()
    return r["pc_phys"] == "e9e317" and r["sp"] == "e8"


def wait_idle(e, frames=600):
    for _ in range(frames // 10):
        if idle(e):
            return True
        e.run_frames(10)
    return idle(e)


def main_menu_select(e, index, tries=8):
    """Open the main menu (EXIT on the map) and move the highlight to `index`."""
    if not wait_idle(e):
        return False
    e.tap("EXIT", hold=2, wait=30)
    for _ in range(tries):
        cur = main_selected(e)
        if cur == index:
            return True
        e.tap("DOWN", hold=2, wait=20)
    return False
