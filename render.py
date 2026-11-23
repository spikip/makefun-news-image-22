#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026 as a deterministic PNG."""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
BG = (250, 247, 240)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RULE = (30, 30, 30)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 48  # margin

def center(text, y, font, fill=INK):
    d.text(((W - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)
    return y + font.size

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines

def para(text, x, y, width, font, leading=1.25, fill=INK):
    for ln in wrap(text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * leading)
    return y

def hrule(y, x0=M, x1=W - M, wdt=2):
    d.line([(x0, y), (x1, y)], fill=RULE, width=wdt)

# ---- Masthead ----
y = 30
center("THE GLOBAL LEDGER", y, F(SERIF_B, 66)); y += 82
center("Sunday, 22 November 2026  ·  The world's news of one day, on one page  ·  Vol. I, No. 22",
       y, F(SANS, 18), GREY); y += 30
hrule(y, wdt=4); y += 6; hrule(y, wdt=1); y += 22

# ---- Lead story ----
kicker = F(SANS_B, 20)
d.text((M, y), "CLIMATE  ·  ANTALYA, TURKEY", font=kicker, fill=(150, 30, 30)); y += 32
lead_font = F(SERIF_B, 54)
for ln in wrap("COP31 climate talks collapse without a deal over fossil fuels", lead_font, W - 2 * M):
    center(ln, y, lead_font); y += 63
y += 4
y = para("Nearly 200 countries left the UN summit in Antalya with no overarching agreement after "
         "the European Union and vulnerable nations rejected a final text that would not name fossil "
         "fuels. UN chief António Guterres said he was \"deeply disappointed\" as two weeks of talks "
         "ended in division over phase-out language and climate finance.",
         M, y, W - 2 * M, F(SERIF, 21))
y += 8
hrule(y, wdt=2); y += 14

# ---- Two columns of supporting stories ----
col_w = (W - 2 * M - 28) // 2
x2 = M + col_w + 28

stories_left = [
    ("WAR AT SEA",
     "Sea drones strike Russian corvette in Benghazi",
     "A suspected Ukrainian sea-drone attack hit the Russian corvette Merkury at Benghazi naval "
     "base in eastern Libya early on Sunday, causing an explosion and fire. Kyiv said seven "
     "naval drones struck the warship."),
    ("THE HAGUE",
     "World court: Myanmar committed genocide against Rohingya",
     "The International Court of Justice ruled that Myanmar committed genocide against its "
     "Rohingya minority, a landmark judgment over the 2017 crackdown that drove hundreds of "
     "thousands to flee."),
]
stories_right = [
    ("GULF",
     "Two tankers struck near Hormuz; Bahrain reports Iranian attack",
     "Two supertankers were hit near the Strait of Hormuz as Bahrain said an Iranian attack "
     "damaged an industrial facility in Sitra and injured two people, keeping the Gulf on edge."),
    ("SPORT  ·  CRICKET",
     "India pile up 720 against New Zealand",
     "India declared at 720 for 9 in Wellington to take a 352-run lead in the first Test against "
     "New Zealand, a commanding position built on a record-breaking batting display."),
]

def story(x, y, kick, head, body):
    d.text((x, y), kick, font=F(SANS_B, 16), fill=(150, 30, 30)); y += 24
    for ln in wrap(head, F(SERIF_B, 24), col_w):
        d.text((x, y), ln, font=F(SERIF_B, 24), fill=INK); y += 29
    y += 2
    y = para(body, x, y, col_w, F(SERIF, 17), leading=1.2)
    return y + 14

yl = yr = y
for s in stories_left:
    yl = story(M, yl, *s)
for s in stories_right:
    yr = story(x2, yr, *s)
d.line([(M + col_w + 14, y), (M + col_w + 14, max(yl, yr) - 10)], fill=RULE, width=1)
y = max(yl, yr) + 2
hrule(y, wdt=2); y += 16

# ---- Bottom strip ----
y = para("ALSO ON SUNDAY — Democrats won their largest US House majority since 1992 after a North "
         "Carolina recount, setting up divided government in Washington. · A fire at a confectionery "
         "factory in Cikande, Indonesia, killed three people, with 36 workers unaccounted for. · "
         "Nepal's Prime Minister Balendra Shah began a two-day state visit to India.",
         M, y, W - 2 * M, F(SANS, 17))
y += 6
hrule(y, wdt=1); y += 6
center("Compiled from the day's reporting by wire services and newsrooms worldwide.", y, F(SANS, 15), GREY)

img.save("/home/hatch/workspace/makefun/new-bounties/news-image-22-bot/entry.png", optimize=True)
print("saved", img.size)
