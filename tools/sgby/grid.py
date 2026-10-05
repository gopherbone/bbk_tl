"""Tile screenshots: grid.py out.png a.png b.png ... (2 columns)"""
import sys
from PIL import Image
out, paths = sys.argv[1], sys.argv[2:]
ims = [Image.open(p) for p in paths]
w, h = ims[0].size
cols = 2
rows = (len(ims) + cols - 1) // cols
g = Image.new("L", (w * cols + 10 * (cols - 1), h * rows + 10 * (rows - 1)), 255)
for i, im in enumerate(ims):
    g.paste(im, ((i % cols) * (w + 10), (i // cols) * (h + 10)))
g.save(out)
