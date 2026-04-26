#!/usr/bin/env python3
"""Generate placeholder text-based brand assets for BizerOS Chat.

Each output is written at the same path/size as the original Mattermost asset
so no HTML/CSS/manifest references need updating. The aim is "obviously not
the Mattermost logo anymore", not pixel-perfect branding.
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = os.path.join(REPO, "webapp/channels/src/images")
FAV = os.path.join(IMG, "favicon")

# Brand color palette (neutral teal, distinct from Mattermost blue)
BRAND_DARK = (15, 76, 92, 255)     # dark teal
BRAND_LIGHT = (255, 255, 255, 255) # white
BRAND_BG_BLUE = (24, 102, 122, 255)
BRAND_BG_GRAY = (90, 102, 110, 255)
BRAND_BG_DARK = (32, 38, 47, 255)

PRODUCT = "BizerOS Chat"
SHORT = "BC"


def _font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def _fit_text_size(draw: ImageDraw.ImageDraw, text: str, w: int, h: int,
                   max_size: int = 200) -> ImageFont.FreeTypeFont:
    """Binary-search the largest font size that fits the box (with margin)."""
    target_w = int(w * 0.86)
    target_h = int(h * 0.7)
    lo, hi = 6, max_size
    best = _font(lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        f = _font(mid)
        bbox = draw.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw <= target_w and th <= target_h:
            best = f
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def make_wordmark(path: str, fg: tuple, bg: tuple | None) -> None:
    with Image.open(path) as im:
        size = im.size
    img = Image.new("RGBA", size, bg if bg is not None else (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = _fit_text_size(draw, PRODUCT, size[0], size[1])
    bbox = draw.textbbox((0, 0), PRODUCT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - tw) // 2 - bbox[0]
    y = (size[1] - th) // 2 - bbox[1]
    draw.text((x, y), PRODUCT, fill=fg, font=font)
    img.save(path, "PNG")


def make_letter_icon(path: str, fg: tuple, bg: tuple) -> None:
    with Image.open(path) as im:
        size = im.size
    img = Image.new("RGBA", size, bg)
    draw = ImageDraw.Draw(img)
    text = SHORT if min(size) >= 24 else "B"
    font = _fit_text_size(draw, text, size[0], size[1])
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - tw) // 2 - bbox[0]
    y = (size[1] - th) // 2 - bbox[1]
    draw.text((x, y), text, fill=fg, font=font)
    img.save(path, "PNG")


def make_svg_wordmark(path: str) -> None:
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 64" '
        'width="320" height="64">\n'
        '  <rect width="320" height="64" fill="none"/>\n'
        '  <text x="160" y="42" text-anchor="middle" '
        'font-family="Helvetica, Arial, sans-serif" font-size="32" '
        'font-weight="700" fill="#0F4C5C">BizerOS Chat</text>\n'
        '</svg>\n'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def main() -> None:
    # SVG wordmark
    make_svg_wordmark(os.path.join(IMG, "logo.svg"))

    # Wordmark PNGs (transparent background variants)
    make_wordmark(os.path.join(IMG, "logo.png"), BRAND_DARK, None)
    make_wordmark(os.path.join(IMG, "logoWhite.png"), BRAND_LIGHT, None)
    make_wordmark(os.path.join(IMG, "logo-email.png"), BRAND_DARK, None)
    make_wordmark(os.path.join(IMG, "logo_email_gray.png"), BRAND_BG_GRAY, None)
    make_wordmark(os.path.join(IMG, "logo_email_blue.png"), BRAND_BG_BLUE, None)
    make_wordmark(os.path.join(IMG, "logo_email_dark.png"), BRAND_BG_DARK, None)

    # Favicons + app icons (single-letter on solid teal background)
    for name in os.listdir(FAV):
        if name.lower().endswith(".png"):
            make_letter_icon(os.path.join(FAV, name), BRAND_LIGHT, BRAND_DARK)

    print("Placeholder assets written.")


if __name__ == "__main__":
    main()
