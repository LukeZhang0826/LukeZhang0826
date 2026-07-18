import sys
from PIL import Image, ImageOps, ImageEnhance

SRC = sys.argv[1]
WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 70
# darkest -> lightest; on GitHub dark theme dense chars read bright,
# so map SUBJECT (dark pixels) to dense chars and background to space
RAMP = "@%#*+=:-. "

img = Image.open(SRC).convert("L")
img = ImageOps.autocontrast(img, cutoff=2)
img = ImageEnhance.Contrast(img).enhance(1.15)

w, h = img.size
aspect = 0.5  # char cell height/width compensation
new_h = max(1, int(h / w * WIDTH * aspect))
img = img.resize((WIDTH, new_h))

n = len(RAMP)
lines = []
for y in range(img.height):
    row = []
    for x in range(img.width):
        p = img.getpixel((x, y))
        row.append(RAMP[min(n - 1, p * n // 256)])
    lines.append("".join(row).rstrip())
print("\n".join(lines))
