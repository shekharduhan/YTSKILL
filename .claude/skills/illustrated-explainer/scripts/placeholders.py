#!/usr/bin/env python3
"""placeholders.py - draw stand-in 1920x1080 images (needs Pillow) so you can test the whole
pipeline - timing, motion, titles, captions, audio - before paying for real AI images.

Each image is a flat-colour scene with a block-head stick figure drawn in code and the shot
number in the corner. Six scene looks are cycled (landscape, sea, dark spotlight, paper card,
map, palace).

  python placeholders.py --shots shots.json          # one image per shot, at its "image" path
  python placeholders.py --count 6 --dir images      # images/shot_001.png .. shot_006.png
"""
import argparse
import json
import math
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("placeholders: Pillow is required (pip install pillow)")

W, H = 1920, 1080
PAPER, INK = (252, 248, 227), (10, 12, 9)
PAL = {"sand": (215, 193, 159), "ochre": (169, 146, 106), "terracotta": (187, 112, 78), "maroon": (114, 58, 48),
       "olive": (142, 149, 84), "stone": (142, 144, 138), "sky": (154, 209, 234), "sea": (47, 103, 138),
       "dark": (36, 36, 31), "mapred": (193, 105, 77), "brown": (105, 93, 70)}


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def figure(d, cx, ground, scale=1.0, robe=PAL["maroon"], mood="neutral", hair=INK):
    s = scale
    head = 150 * s
    hx0, hy0 = cx - head * 0.55, ground - 430 * s
    # legs and arms (thin stick lines)
    lw = max(4, int(9 * s))
    hip = (cx, ground - 170 * s)
    d.line([hip, (cx - 45 * s, ground)], fill=INK, width=lw)
    d.line([hip, (cx + 45 * s, ground)], fill=INK, width=lw)
    for fx in (-45, 45):
        d.ellipse([cx + fx * s - 22 * s, ground - 10 * s, cx + fx * s + 22 * s, ground + 8 * s], fill=INK)
    sh = (cx, hy0 + head + 40 * s)
    d.line([(cx, hy0 + head), sh], fill=INK, width=lw)
    # robe (flat colour cut-out with outline)
    d.polygon([(cx - 70 * s, sh[1]), (cx + 70 * s, sh[1]), (cx + 95 * s, ground - 120 * s), (cx - 95 * s, ground - 120 * s)],
              fill=robe, outline=INK, width=max(3, int(6 * s)))
    d.line([(cx - 10 * s, sh[1] + 20 * s), (cx - 25 * s, ground - 130 * s)], fill=INK, width=max(2, int(3 * s)))
    d.line([(cx - 70 * s, sh[1] + 15 * s), (cx - 150 * s, sh[1] + 110 * s)], fill=INK, width=lw)
    d.line([(cx + 70 * s, sh[1] + 15 * s), (cx + 160 * s, sh[1] - 40 * s)], fill=INK, width=lw)
    d.ellipse([cx - 165 * s, sh[1] + 95 * s, cx - 135 * s, sh[1] + 125 * s], fill=INK)
    d.ellipse([cx + 145 * s, sh[1] - 55 * s, cx + 175 * s, sh[1] - 25 * s], fill=INK)
    # head: rounded white square, ears, hair, eyes, brows, mouth
    hx1, hy1 = hx0 + head * 1.1, hy0 + head
    for ex in (hx0 - 14 * s, hx1 - 14 * s):
        d.ellipse([ex, hy0 + head * 0.4, ex + 28 * s, hy0 + head * 0.62], fill=PAPER, outline=INK, width=max(3, int(5 * s)))
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=int(28 * s), fill=PAPER, outline=INK, width=max(3, int(7 * s)))
    for i in range(7):
        a = math.pi * (i / 6)
        bx = (hx0 + hx1) / 2 - math.cos(a) * head * 0.45
        d.ellipse([bx - 30 * s, hy0 - 40 * s - math.sin(a) * 18 * s, bx + 30 * s, hy0 + 18 * s], fill=hair)
    ey = hy0 + head * 0.52
    lx, rx = hx0 + head * 0.33, hx1 - head * 0.33
    for x in (lx, rx):
        d.ellipse([x - 10 * s, ey - 15 * s, x + 10 * s, ey + 15 * s], fill=INK)
    by = ey - 34 * s
    tilt = {"angry": (12, -8), "worried": (-10, 8), "neutral": (0, 0)}[mood]
    d.line([(lx - 22 * s, by - tilt[0] * s), (lx + 18 * s, by - tilt[1] * s)], fill=INK, width=max(4, int(10 * s)))
    d.line([(rx - 18 * s, by - tilt[1] * s), (rx + 22 * s, by - tilt[0] * s)], fill=INK, width=max(4, int(10 * s)))
    my = hy0 + head * 0.8
    if mood == "worried":
        d.line([(cx - 25 * s, my), (cx - 8 * s, my - 6 * s), (cx + 8 * s, my + 4 * s), (cx + 25 * s, my)], fill=INK, width=max(3, int(5 * s)))
    else:
        d.chord([cx - 22 * s, my - 14 * s, cx + 22 * s, my + 14 * s], 0, 180, fill=INK)


def scene(k):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    look = k % 6
    if look == 0:  # landscape with hills and brick town
        d.rectangle([0, 0, W, 700], fill=PAL["sky"])
        d.polygon([(0, 700), (500, 420), (900, 700)], fill=PAL["stone"])
        d.polygon([(700, 700), (1300, 360), (1920, 700)], fill=PAL["brown"])
        d.polygon([(1180, 430), (1300, 360), (1420, 430)], fill=PAPER)
        d.rectangle([0, 700, W, H], fill=PAL["sand"])
        for i in range(6):
            x = 1150 + i * 120
            d.rectangle([x, 600, x + 100, 760], fill=PAL["terracotta"], outline=(97, 62, 47), width=4)
        figure(d, 520, 980, 1.0, PAL["olive"], "neutral")
    elif look == 1:  # sea with a boat
        d.rectangle([0, 0, W, 560], fill=PAL["sky"])
        d.rectangle([0, 560, W, H], fill=PAL["sea"])
        for i in range(14):
            y = 620 + (i % 7) * 60
            x = (i * 260) % W
            d.arc([x, y, x + 120, y + 30], 200, 340, fill=(88, 145, 173), width=5)
        d.polygon([(1100, 640), (1560, 640), (1500, 720), (1160, 720)], fill=PAL["brown"], outline=INK, width=6)
        d.line([(1330, 640), (1330, 380)], fill=INK, width=8)
        d.polygon([(1340, 390), (1340, 610), (1500, 600)], fill=PAPER, outline=INK, width=5)
        figure(d, 420, 900, 0.9, PAL["terracotta"], "worried")
    elif look == 2:  # dark spotlight
        d.rectangle([0, 0, W, H], fill=PAL["dark"])
        d.polygon([(800, 0), (1120, 0), (1350, H), (570, H)], fill=(58, 58, 50))
        d.ellipse([620, 900, 1300, 1040], fill=(78, 76, 66))
        figure(d, 960, 980, 1.05, PAL["maroon"], "worried", hair=(200, 200, 200))
    elif look == 3:  # cream paper card with a big zero and two figures
        d.ellipse([760, 220, 1160, 820], outline=INK, width=70)
        figure(d, 450, 960, 0.85, PAL["olive"], "neutral")
        figure(d, 1470, 960, 0.85, PAL["terracotta"], "angry")
    elif look == 4:  # map
        d.rectangle([0, 0, W, H], fill=PAL["sea"])
        d.polygon([(560, 120), (1380, 110), (1500, 360), (1240, 520), (1060, 980), (900, 990), (760, 560), (520, 380)],
                  fill=PAL["sand"], outline=(97, 62, 47), width=6)
        d.polygon([(640, 180), (1300, 170), (1360, 380), (1150, 520), (820, 520), (650, 360)], fill=PAL["mapred"])
        d.line([(560, 120), (1380, 110)], fill=PAPER, width=26)
    else:  # palace hall, two-shot
        d.rectangle([0, 0, W, H], fill=PAL["ochre"])
        for x in (300, 860, 1420):
            d.rectangle([x, 120, x + 200, 640], fill=PAL["sky"], outline=(97, 62, 47), width=8)
            d.pieslice([x, 20, x + 200, 220], 180, 360, fill=PAL["sky"], outline=(97, 62, 47), width=8)
        d.rectangle([0, 760, W, H], fill=PAL["brown"])
        figure(d, 640, 1000, 1.0, PAL["maroon"], "angry")
        figure(d, 1300, 1000, 1.0, PAL["olive"], "worried")
    f = font(46)
    d.rounded_rectangle([W - 260, H - 110, W - 30, H - 30], radius=16, fill=INK)
    d.text((W - 240, H - 100), "SHOT %02d" % (k + 1), font=f, fill=PAPER)
    d.text((40, H - 60), "PLACEHOLDER - replace with AI image", font=font(28), fill=INK if look not in (2, 4) else PAPER)
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shots", help="shots.json: write one placeholder to each shot's image path")
    ap.add_argument("--count", type=int, help="number of images when not using --shots")
    ap.add_argument("--dir", default="images", help="output folder for --count (default images)")
    ap.add_argument("--force", action="store_true", help="overwrite existing images")
    args = ap.parse_args()
    if args.shots:
        with open(args.shots, encoding="utf-8") as f:
            data = json.load(f)
        shots = data["shots"] if isinstance(data, dict) else data
        base = os.path.dirname(os.path.abspath(args.shots))
        paths = [s["image"] if os.path.isabs(s["image"]) else os.path.join(base, s["image"]) for s in shots]
    elif args.count:
        paths = [os.path.join(args.dir, "shot_%03d.png" % (i + 1)) for i in range(args.count)]
    else:
        ap.error("pass --shots or --count")
    n = 0
    for k, p in enumerate(paths):
        if os.path.exists(p) and not args.force:
            continue
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        scene(k).save(p)
        n += 1
    print("placeholders: wrote %d image(s)" % n)


if __name__ == "__main__":
    main()
