#!/usr/bin/env python3
"""Print dominant colors (hex + share) of an image, for design tokens.

Usage: python3 color_palette.py image.png [--colors 8]
"""
import argparse
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--colors", type=int, default=8)
    a = ap.parse_args()

    im = Image.open(a.image).convert("RGB")
    im.thumbnail((400, 400))
    q = im.quantize(colors=a.colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: a.colors * 3]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    print("share   hex      role-hint")
    for rank, (c, idx) in enumerate(counts):
        r, g, b = pal[idx * 3: idx * 3 + 3]
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        hint = "likely background" if rank == 0 else ("dark/text?" if lum < 70 else "light/surface?" if lum > 200 else "accent/mid")
        print(f"{c / total:5.1%}   #{r:02x}{g:02x}{b:02x}  {hint}")


if __name__ == "__main__":
    main()
