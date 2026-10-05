"""Contact sheets of a tour: sheets.py DIR [prefix-filter] -> DIR/sheets/NN.png (12 per sheet)"""
import glob, os, sys
from PIL import Image, ImageDraw
d = sys.argv[1]
flt = sys.argv[2] if len(sys.argv) > 2 else ""
paths = [p for p in sorted(glob.glob(os.path.join(d, "*.png"))) if flt in os.path.basename(p)]
os.makedirs(os.path.join(d, "sheets"), exist_ok=True)
W, H, C = 318, 192, 3
for n in range(0, len(paths), 12):
    batch = paths[n:n + 12]
    rows = (len(batch) + C - 1) // C
    sheet = Image.new("L", (C * (W + 6), rows * (H + 18)), 255)
    dr = ImageDraw.Draw(sheet)
    for i, p in enumerate(batch):
        im = Image.open(p).resize((W, H), Image.NEAREST)
        x, y = (i % C) * (W + 6), (i // C) * (H + 18)
        sheet.paste(im, (x, y + 14))
        dr.text((x + 2, y), os.path.basename(p)[:-4], fill=0)
    sheet.save(os.path.join(d, "sheets", f"{n // 12:02d}.png"))
print(len(paths), "shots")
