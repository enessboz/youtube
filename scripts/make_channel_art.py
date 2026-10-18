#!/usr/bin/env python3
"""make_channel_art: iki kanal için avatar, banner ve filigranı üretir.

Çıktı: channels/<kanal>/launch/art/{avatar-800.png, banner-2560x1440.png, watermark-300.png}
Fontlar (OFL) ilk çalıştırmada github.com/google/fonts'tan .cache/fonts'a indirilir.
Boyutlar YouTube yardım sayfasından: profil (render 98 px; PNG/JPG ≤15 MB), banner 2560x1440
(min 2048x1152, güvenli alan 1235x338 @ min boyut, ≤6 MB), filigran ≥150x150 kare ≤1 MB.

Kullanım: python3 scripts/make_channel_art.py [--preview]   (--preview: 98 px daire önizlemesi de yazar)
"""
import argparse
import math
import os
import random
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, ".cache", "fonts")
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS = {
    "Bitter": ("bitter/Bitter%5Bwght%5D.ttf", "Bitter[wght].ttf"),
    "Oswald": ("oswald/Oswald%5Bwght%5D.ttf", "Oswald[wght].ttf"),
    "Playfair": ("playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf", "PlayfairDisplay[wght].ttf"),
    "LatoBold": ("lato/Lato-Bold.ttf", "Lato-Bold.ttf"),
    "LatoRegular": ("lato/Lato-Regular.ttf", "Lato-Regular.ttf"),
}

CHANNELS = {
    "gestern-gabs-das": dict(
        name="Gestern gab's das", mono="G", title_font=("Bitter", 800), sub_font="LatoBold",
        sub="Läden, Berufe und Alltag von damals – regelmäßig neue Geschichten",
        paper="#F3EBDD", ink="#22303C", main="#B24A33", second="#2F6F73", accent="#D9A441",
    ),
    "quando-eravamo-noi": dict(
        name="Quando Eravamo Noi", mono="Q", title_font=("Playfair", 800), sub_font="LatoBold",
        sub="Botteghe, mestieri e ricordi di una volta – nuove storie ogni settimana",
        paper="#F4ECDD", ink="#23344E", main="#C8643B", second="#6B7A3A", accent="#D98F8F",
    ),
}


def ensure_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    for _, (url, fname) in FONTS.items():
        path = os.path.join(FONT_DIR, fname)
        if not os.path.exists(path):
            urllib.request.urlretrieve(GF + url, path)


def font(key, size, wght=None):
    f = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[key][1]), size)
    if wght is not None:
        f.set_variation_by_axes([wght])
    return f


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def text_size(draw, txt, f):
    l, t, r, b = draw.textbbox((0, 0), txt, font=f)
    return r - l, b - t, l, t


def fit_font(draw, txt, key, wght, max_w, start):
    size = start
    while size > 20:
        f = font(key, size, wght)
        if text_size(draw, txt, f)[0] <= max_w:
            return f
        size -= 4
    return font(key, 20, wght)


def halftone(draw, box, color, step=22, max_r=9, direction="down", seed=1):
    """Yarım ton nokta deseni: yöne doğru büyüyen noktalar (serigrafi hissi)."""
    x0, y0, x1, y1 = box
    for yi, y in enumerate(range(y0, y1, step)):
        for xi, x in enumerate(range(x0, x1, step)):
            if direction == "down":
                k = (y - y0) / max(1, (y1 - y0))
            elif direction == "up":
                k = 1 - (y - y0) / max(1, (y1 - y0))
            elif direction == "right":
                k = (x - x0) / max(1, (x1 - x0))
            else:
                k = 1 - (x - x0) / max(1, (x1 - x0))
            ox = step // 2 if yi % 2 else 0
            r = max_r * k
            if r >= 1:
                draw.ellipse((x + ox - r, y - r, x + ox + r, y + r), fill=color)


def disc_with_mono(size, c, scale=2):
    s = size * scale
    img = Image.new("RGBA", (s, s), rgb(c["paper"]) + (255,))
    d = ImageDraw.Draw(img)
    margin = int(s * 0.04)
    d.ellipse((margin, margin, s - margin, s - margin), fill=rgb(c["main"]))
    # ince iç halka (damga hissi)
    ring = int(s * 0.075)
    d.ellipse((ring, ring, s - ring, s - ring), outline=rgb(c["paper"]), width=max(3, s // 130))
    key, wght = c["title_font"]
    f = font(key, int(s * 0.62), wght)
    w, h, l, t = text_size(d, c["mono"], f)
    x = (s - w) // 2 - l
    y = (s - h) // 2 - t - int(s * 0.01)
    d.text((x, y), c["mono"], font=f, fill=rgb(c["paper"]))
    # vurgu: küçük işaret (DE: kesme işareti, IT: zeytin)
    if c["mono"] == "G":
        ax, ay = x + w + int(s * 0.015), y + t + int(s * 0.03)
        pts = [(ax, ay), (ax + s * 0.075, ay), (ax + s * 0.045, ay + s * 0.17), (ax + s * 0.01, ay + s * 0.17)]
        d.polygon(pts, fill=rgb(c["accent"]))
    else:
        # küçük zeytin: halkanın içinde, Q'nun sağ üstünde
        r = int(s * 0.05)
        cx, cy = int(s * 0.73), int(s * 0.29)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb(c["second"]))
    return img.resize((size, size), Image.LANCZOS)


def banner(c):
    W, H = 2560, 1440
    scale = W / 2048
    safe_w, safe_h = int(1235 * scale), int(338 * scale)  # 1544 x 423
    sx0, sy0 = (W - safe_w) // 2, (H - safe_h) // 2
    img = Image.new("RGB", (W, H), rgb(c["paper"]))
    d = ImageDraw.Draw(img)
    # üst ve alt dekoratif bantlar (yarım ton), ortası sade
    halftone(d, (0, 0, W, sy0 - 40), rgb(c["second"]), step=28, max_r=11, direction="up")
    halftone(d, (0, sy0 + safe_h + 40, W, H), rgb(c["second"]), step=28, max_r=11, direction="down")
    d.rectangle((0, sy0 - 12, W, sy0 - 4), fill=rgb(c["main"]))
    d.rectangle((0, sy0 + safe_h + 4, W, sy0 + safe_h + 12), fill=rgb(c["main"]))
    # monogram diski (güvenli alanın solunda)
    disc = disc_with_mono(safe_h - 40, c).convert("RGBA")
    img.paste(disc, (sx0 + 10, sy0 + 20), disc)
    tx0 = sx0 + safe_h + 40
    max_w = safe_w - safe_h - 60
    key, wght = c["title_font"]
    ft = fit_font(d, c["name"], key, wght, max_w, 150)
    tw, th, tl, tt = text_size(d, c["name"], ft)
    fs = fit_font(d, c["sub"], c["sub_font"], None, max_w, 46)
    sw, sh, sl, st = text_size(d, c["sub"], fs)
    gap = 26
    total = th + gap + sh
    ty = sy0 + (safe_h - total) // 2
    d.text((tx0 - tl, ty - tt), c["name"], font=ft, fill=rgb(c["ink"]))
    d.text((tx0 - sl, ty + th + gap - st), c["sub"], font=fs, fill=rgb(c["main"]))
    return img


def watermark(c, size=300):
    img = disc_with_mono(size, c, scale=3)
    # kağıt zemini şeffaf yap (yalnızca disk kalsın)
    px = img.load()
    bg = rgb(c["paper"])
    for y in range(size):
        for x in range(size):
            r, g, b, a = px[x, y]
            if (r, g, b) == bg:
                px[x, y] = (r, g, b, 0)
    return img


def circle_preview(img, px=98):
    small = img.resize((px, px), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    out = Image.new("RGBA", (px, px), (255, 255, 255, 0))
    out.paste(small, (0, 0), mask)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    ensure_fonts()
    for slug, c in CHANNELS.items():
        out = os.path.join(ROOT, "channels", slug, "launch", "art")
        os.makedirs(out, exist_ok=True)
        av = disc_with_mono(800, c)
        av.convert("RGB").save(os.path.join(out, "avatar-800.png"), optimize=True)
        banner(c).save(os.path.join(out, "banner-2560x1440.png"), optimize=True)
        watermark(c).save(os.path.join(out, "watermark-300.png"), optimize=True)
        if a.preview:
            circle_preview(av).save(os.path.join(out, "_preview-avatar-98.png"))
        print(slug, "->", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
