"""Make every channel image for YouTube, Instagram, Facebook and TikTok, plus episode thumbnails.

    python3 brand_assets.py            # channel images -> brand/out/
    python3 brand_assets.py thumb 1 [image] [cx]   # episode thumbnail -> brand/out/thumbnails/
                                                   # cx 0..1 moves the crop left/right; add 'top' or 'left' to move the words

Artwork comes from brand/raw/ (logo.png, banner.png, made with Google's image model). Hindi text is
drawn here with Noto Serif Devanagari, because image models can't spell Hindi reliably.
"""
import glob, os, re, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW, OUT = os.path.join(HERE, "brand", "raw"), os.path.join(HERE, "brand", "out")
FONT = "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Regular.ttf"
GOLD, CREAM, CRIMSON, DARK = (246, 196, 83), (255, 240, 214), (110, 14, 10), (40, 6, 4)
NAME, TAGLINE, SCHEDULE = "सूर्यवंश कथा", "हर कथा, स्रोत के साथ", "नए एपिसोड: हर मंगलवार और शुक्रवार"
KINGS = ["शुरुआत", "इक्ष्वाकु", "मान्धाता", "त्रिशंकु", "हरिश्चंद्र", "सगर", "भगीरथ", "रघु", "अज-दशरथ", "श्रीराम", "लव-कुश"]


def font(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_R, size, layout_engine=ImageFont.Layout.RAQM)


def cover(im, w, h, cy=0.5, cx=0.5):
    """Scale to fill w x h and crop (cx, cy = centre of the crop, 0..1)."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * cx - w / 2)), im.width - w)
    y = min(max(0, round(im.height * cy - h / 2)), im.height - h)
    return im.crop((x, y, x + w, y + h))


def text(img, xy, s, size, fill=GOLD, bold=True, anchor="mm", shadow=True, stroke=0):
    d = ImageDraw.Draw(img)
    f = font(size, bold)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + size // 18, xy[1] + size // 18), s, font=f, fill=(0, 0, 0, 200), anchor=anchor)
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(size // 14)))
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=DARK)


def band(img, box, alpha=150):
    """Soft dark band behind text so it reads on any part of the art."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=40, fill=(20, 4, 2, alpha))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(30)))


def logo_square():
    im = Image.open(os.path.join(RAW, "logo.png")).convert("RGB")
    w = im.width
    c = int(w * 0.62)                       # crop in so the sun face fills the circle
    return im.crop(((w - c) // 2, (w - c) // 2, (w + c) // 2, (w + c) // 2)).resize((1080, 1080), Image.LANCZOS)


def circle(im):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, im.width - 1, im.height - 1), fill=255)
    out = im.convert("RGBA"); out.putalpha(m)
    return out


def save(im, *parts):
    p = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    (im.convert("RGB") if p.endswith(".jpg") else im).save(p, quality=92)
    print("wrote", os.path.relpath(p, HERE), im.size)


def channel():
    logo = logo_square()
    save(logo.resize((800, 800), Image.LANCZOS), "youtube", "profile-picture-800x800.png")
    save(circle(logo.resize((150, 150), Image.LANCZOS)), "youtube", "watermark-150x150.png")
    save(logo, "instagram", "profile-picture-1080x1080.png")
    save(logo.resize((720, 720), Image.LANCZOS), "facebook", "profile-picture-720x720.png")
    save(logo, "tiktok", "profile-picture-1080x1080.png")

    art = Image.open(os.path.join(RAW, "banner.png")).convert("RGB")
    # YouTube banner: 2560x1440; everything important inside the centre 1546x423 (visible on every device)
    yt = cover(art, 2560, 1440, cy=0.52).convert("RGBA")
    band(yt, (507, 520, 2053, 920), 140)
    text(yt, (1280, 650), NAME, 190)
    text(yt, (1280, 800), TAGLINE, 70, fill=CREAM)
    text(yt, (1280, 885), SCHEDULE, 44, fill=CREAM, bold=False)
    save(yt, "youtube", "banner-2560x1440.jpg")
    # Facebook cover: 1640x624 upload; phones show only the centre, so keep text in the middle ~1100px
    fb = cover(art, 1640, 624, cy=0.5).convert("RGBA")
    band(fb, (420, 150, 1220, 480), 140)
    text(fb, (820, 280), NAME, 140)
    text(fb, (820, 410), TAGLINE, 54, fill=CREAM)
    save(fb, "facebook", "cover-1640x624.jpg")

    # Instagram story highlight covers: 1080x1920, only the centre circle shows
    for i, k in enumerate(KINGS):
        hc = Image.new("RGBA", (1080, 1920), CRIMSON + (255,))
        d = ImageDraw.Draw(hc)
        d.ellipse((140, 560, 940, 1360), outline=GOLD, width=18)
        size = 170
        while ImageDraw.Draw(hc).textlength(k, font=font(size)) > 600: size -= 4
        text(hc, (540, 950), k, size, shadow=False)
        save(hc, "instagram", "highlight-covers", f"{i:02d}-cover-1080x1920.png")

    # Channel trailer / first post: square image for Instagram & Facebook "intro" post
    post = cover(art, 1080, 1080, cy=0.5).convert("RGBA")
    band(post, (90, 380, 990, 720), 150)
    text(post, (540, 500), NAME, 130)
    text(post, (540, 630), "मनु से लव-कुश तक  |  84 एपिसोड", 50, fill=CREAM)
    save(post, "instagram", "first-post-1080x1080.jpg")
    save(post, "facebook", "first-post-1080x1080.jpg")


def unletterbox(im):
    from assemble import bars
    return im.crop(bars(im))


def thumbnail(ep, image=None, cx=0.5, top=False, left=False):
    """1280x720 YouTube thumbnail: the episode's strongest image + its thumbnail words from the script."""
    md = open(glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0], encoding="utf-8").read()
    words = re.search(r"^थंबनेल:\s*(.+)$", md.split("## कॉपी ब्लॉक")[-1], re.M).group(1).strip("` ")
    src = image or os.path.join(HERE, "images", f"ep{ep:02d}", "01.png")
    t = cover(unletterbox(Image.open(src).convert("RGB")), 1280, 720, cx=cx).convert("RGBA")
    grad = Image.new("RGBA", t.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    if left:                                # two lines in the top-left corner, darkened diagonally
        for x in range(1280):
            a = int(max(0, (700 - x) / 700) * 200)
            gd.line([(x, 0), (x, 420)], fill=(10, 2, 0, a))
        t.alpha_composite(grad.filter(ImageFilter.GaussianBlur(60)))
        lines = [l.strip() + "।" for l in words.split("।") if l.strip()] or [words]
        for i, l in enumerate(lines):
            text(t, (60, 120 + i * 140), l, 120, anchor="lm", stroke=6)
    else:
        for y in range(720):                # darken the bottom (or top) for the words
            a = int(max(0, ((340 - y) if top else (y - 380)) / 340) * 210)
            gd.line([(0, y), (1280, y)], fill=(10, 2, 0, a))
        t.alpha_composite(grad)
        text(t, (640, 120 if top else 600), words, 130 if len(words) <= 10 else 104, stroke=6)
    text(t, (1240, 50), f"{ep}", 46, fill=CREAM, anchor="rm")
    save(t, "thumbnails", f"ep{ep:02d}-thumbnail-1280x720.jpg")


if __name__ == "__main__":
    if sys.argv[1:2] == ["thumb"]:
        thumbnail(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None,
                  float(sys.argv[4]) if len(sys.argv) > 4 else 0.5, "top" in sys.argv[5:], "left" in sys.argv[5:])
    else:
        channel()
