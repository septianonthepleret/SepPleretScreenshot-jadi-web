#!/usr/bin/env python3
"""Render an HTML file to a PNG so it can be compared with the source image.

Usage: python3 render_preview.py page.html out.png [--width 1440] [--height 900] [--full]
"""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--full", action="store_true", help="capture full page height")
    a = ap.parse_args()

    url = Path(a.html).resolve().as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": a.height})
        pg.goto(url)
        pg.wait_for_timeout(400)
        pg.screenshot(path=a.out, full_page=a.full)
        b.close()
    print(f"Saved {a.out}")


if __name__ == "__main__":
    main()
