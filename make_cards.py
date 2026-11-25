"""Build-time card renderer (Pillow only, never imported by main.py).

Produces the three README visuals for the roast-gadget entry:
  cover.png         — hero card: the winning line, big and centred
  card-winner.png   — winner card: line + score + char count
  card-finalists.png — finalists card: the top-4 lines of the tournament

Run:  python3 make_cards.py        (writes PNGs next to this file)
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (18, 18, 24)
PANEL = (32, 32, 44)
GOLD = (212, 175, 55)
INK = (240, 240, 235)
MUTED = (160, 160, 150)
ACCENT = (120, 200, 255)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

WINNER = "My fridge texts me that I'm out of milk while I'm standing in front of it holding the milk."
FINALISTS = [
    ("#19 · WINNER · 25/25", WINNER),
    ("#6 · 24/25", "My earbuds connect to my neighbour's TV faster than to my own phone, and honestly they seem happier there."),
    ("#23 · 23/25", "My smart speaker heard 'play jazz' as 'buy jazz'; I now own twelve albums and zero regrets it will admit to."),
    ("#9 · 23/25", "My phone has 4% battery, 47 notifications, and the confidence of a man with a full tank and no map."),
]


def font(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_REG, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, spacing=8):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def cover():
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=PANEL, outline=GOLD, width=3)
    d.text((80, 78), "ONE-LINE ROAST", font=font(34), fill=GOLD)
    d.text((80, 122), "The Gadget You Use Every Day  ·  make.fun", font=font(24, bold=False), fill=MUTED)
    # Fridge glyph, drawn as a simple panel with a note
    d.rounded_rectangle([560, 185, 720, 415], radius=18, fill=(52, 52, 68), outline=ACCENT, width=3)
    d.line([640, 185, 640, 415], fill=ACCENT, width=3)
    d.line([560, 295, 720, 295], fill=ACCENT, width=2)
    d.rounded_rectangle([694, 205, 712, 245], radius=6, fill=ACCENT)
    d.rounded_rectangle([694, 315, 712, 355], radius=6, fill=ACCENT)
    d.text((560, 428), "the fridge, mid-text", font=font(22, bold=False), fill=MUTED)
    lines = wrap(d, WINNER, font(34), width=48)
    y = draw_centered(d, W // 2, 470, lines, font(34), INK, spacing=8)
    d.text((80, H - 72), "91 characters  ·  40 candidates  ·  knockout tournament winner 25/25", font=font(22, bold=False), fill=GOLD)
    img.save("cover.png")


def winner_card():
    W, H = 1280, 640
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=PANEL, outline=GOLD, width=3)
    d.text((80, 76), "WINNER  ·  25/25  ·  91 characters", font=font(30), fill=GOLD)
    lines = wrap(d, WINNER, font(38), width=38)
    y = draw_centered(d, W // 2, 190, lines, font(38), INK, spacing=10)
    d.text((80, H - 110), "Judge criteria, in order: daily gadget ✓  funny on first read ✓  fresh angle ✓", font=font(22, bold=False), fill=MUTED)
    d.text((80, H - 76), "neatly worded ✓  one person's specific gripe ✓", font=font(22, bold=False), fill=MUTED)
    img.save("card-winner.png")


def finalists_card():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28, fill=PANEL, outline=GOLD, width=3)
    d.text((80, 76), "TOURNAMENT FINALISTS  ·  top 4 of 40 candidates", font=font(30), fill=GOLD)
    y = 150
    for label, text in FINALISTS:
        d.text((80, y), label, font=font(24), fill=ACCENT if "WINNER" in label else GOLD)
        y += 40
        for line in wrap(d, text, font(26, bold=False), width=62):
            d.text((80, y), line, font=font(26, bold=False), fill=INK)
            y += 36
        y += 26
    img.save("card-finalists.png")


if __name__ == "__main__":
    cover()
    winner_card()
    finalists_card()
    print("cover.png, card-winner.png, card-finalists.png written")
