#!/usr/bin/env python3
"""Compose the news-image-20261125 front page (1024x1024 PNG) with PIL.

Variants: hero in {ship, kyiv, riyadh, number}, density in {36, 40, 44},
layout in {A, B, C}. All art is drawn here with PIL (no external images).
Usage: python3 compose.py <hero> <density> <layout> <out.png>
"""
import sys
from PIL import Image, ImageDraw, ImageFont
from stories import STORIES, ALTERNATES, TIMELINE, REGION_ORDER, REGION_COLORS

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 22)
NAVY = (20, 36, 61)
GOLD = (201, 162, 39)
RED = (138, 47, 47)
GREY = (90, 88, 82)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def stories_for(density):
    base = list(STORIES)
    if density == 36:
        drop = {"Libya denies colluding in Benghazi ship attack",
                "MSF halts work in South Sudan after abduction",
                "Radar fault delays flights at Chicago O'Hare",
                "Asteroid eclipse seen from deep space"}
        base = [s for s in base if s[1] not in drop]
    elif density == 44:
        base = base + ALTERNATES[:4]
    return base


HERO_COPY = {
    "ship": ("UKRAINE HITS RUSSIA'S SHIPS ON TWO SEAS",
             "Zelenskiy confirms drone strikes on a cargo ship in the Gulf of "
             "Finland and a warship off Benghazi; Moscow calls it terrorism.",
             ["Sparta II towed to St Petersburg after fire",
              "Norway urges Kyiv to show caution"]),
    "kyiv": ("RESCUERS DIG THROUGH THE RUBBLE IN KYIV",
             "Russian drones hit an apartment block near the capital; "
             "11 killed as crews search for survivors through the night.",
             ["700,000+ Russian soldiers killed, new study finds",
              "NATO to send early-warning jets to Poland"]),
    "riyadh": ("RIYADH'S TALLEST TOWER HIT AGAIN",
               "A Houthi drone strikes the PIF Tower for the second time in a "
               "week; 11 people are wounded in the financial district.",
               ["Houthis now 60 km from Aden, Yemen military says",
                "Three tankers hit by mines in the Strait of Hormuz"]),
    "number": ("700,000: THE COST, COUNTED",
               "A new analysis puts the Russian soldiers killed in Ukraine "
               "above 700,000 — the war's toll, laid bare in one number.",
               ["RFE/RL returns to shortwave for Afghan girls",
                "Kyiv flats hit by drones; 11 killed"]),
}


def art_ship(d, x, y, w, h):
    # dusk sky
    for i in range(h):
        t = i / h
        r = int(24 + (214 - 24) * t * t)
        g = int(36 + (110 - 36) * t * t)
        b = int(74 + (60 - 74) * t * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # low sun
    sx, sy = x + int(w * 0.72), y + int(h * 0.42)
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(232, 150, 60))
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(13, 30, 52))
    for i in range(5):
        yy = y + int(h * 0.66) + i * int(h * 0.07)
        d.line([(x + 10 + i * 30, yy), (x + w - 20 - i * 40, yy)],
               fill=(40, 70, 105), width=2)
    # cargo ship
    hx, hy = x + int(w * 0.10), y + int(h * 0.44)
    hw, hh = int(w * 0.52), int(h * 0.16)
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(28, 28, 34))
    d.rectangle([hx + hw - 14, hy - int(h * 0.10), hx + hw, hy], fill=(28, 28, 34))
    for j, c in enumerate([(178, 62, 52), (60, 110, 140), (201, 162, 39),
                           (90, 130, 90), (178, 62, 52)]):
        cx = hx + 12 + j * int(hw * 0.17)
        d.rectangle([cx, hy - int(h * 0.09), cx + int(hw * 0.14),
                     hy - 2], fill=c)
    # flames + smoke above midship
    fx = hx + int(hw * 0.45)
    for k, (dx, dy, s) in enumerate([(0, 0, 34), (16, -10, 26), (-14, -12, 24),
                                     (6, -22, 18)]):
        d.polygon([(fx + dx - s // 2, hy - int(h * 0.09) - dy),
                   (fx + dx, hy - int(h * 0.09) - dy - s),
                   (fx + dx + s // 2, hy - int(h * 0.09) - dy)],
                  fill=(240, 140, 40) if k % 2 == 0 else (250, 200, 80))
    for k, (dx, dy, s) in enumerate([(18, -44, 20), (34, -66, 26), (52, -88, 32)]):
        d.ellipse([fx + dx - s // 2, hy - int(h * 0.09) - dy - s,
                   fx + dx + s // 2, hy - int(h * 0.09) - dy], fill=(70, 70, 78))
    # drones
    for dx, dy in [(int(w * 0.78), int(h * 0.18)), (int(w * 0.86), int(h * 0.30))]:
        d.ellipse([x + dx - 5, y + dy - 3, x + dx + 5, y + dy + 3], fill=(15, 15, 18))
        d.line([(x + dx - 12, y + dy), (x + dx + 12, y + dy)], fill=(15, 15, 18), width=2)
    d.text((x + 10, y + h - 18), "DRAWN SCENE — GULF OF FINLAND",
           font=F(DJB, 11), fill=(220, 220, 210))


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 30))
    # damaged block, broken top edge
    bx, by = x + int(w * 0.08), y + int(h * 0.18)
    bw, bh = int(w * 0.42), int(h * 0.62)
    pts = [(bx, by + bh), (bx, by + 30), (bx + 40, by + 8), (bx + 90, by + 26),
           (bx + 150, by), (bx + bw, by + 18), (bx + bw, by + bh)]
    d.polygon(pts, fill=(52, 52, 60))
    # lit / dark windows
    for r in range(4):
        for c in range(4):
            wx = bx + 14 + c * 34
            wy = by + 40 + r * 34
            if (r * 4 + c) % 3 == 0:
                d.rectangle([wx, wy, wx + 20, wy + 22], fill=(240, 190, 90))
            else:
                d.rectangle([wx, wy, wx + 20, wy + 22], fill=(24, 24, 32))
    # rubble
    for k, (dx, dy, s, col) in enumerate(
            [(30, 8, 46, (88, 84, 78)), (80, 16, 60, (70, 68, 64)),
             (150, 4, 40, (100, 96, 88)), (210, 18, 52, (80, 76, 70))]):
        rx = x + int(w * 0.52) + dx * w // 620
        ry = y + h - 46 + dy
        d.polygon([(rx, ry), (rx + s // 2, ry - s // 2), (rx + s, ry)],
                  fill=col)
    # rescuer silhouette + lamp beam
    rx, ry = x + int(w * 0.68), y + int(h * 0.52)
    d.ellipse([rx - 10, ry - 34, rx + 10, ry - 14], fill=(8, 8, 10))  # helmet
    d.polygon([(rx - 12, ry - 12), (rx + 12, ry - 12), (rx + 16, ry + 34),
               (rx - 16, ry + 34)], fill=(8, 8, 10))
    d.polygon([(rx + 8, ry - 4), (rx + int(w * 0.30), ry - 26),
               (rx + int(w * 0.30), ry + 6)], fill=(250, 220, 130))
    d.ellipse([rx + int(w * 0.30) - 8, ry - 16, rx + int(w * 0.30) + 8,
               ry + 2], fill=(255, 240, 170))
    d.text((x + 10, y + h - 18), "DRAWN SCENE — KYIV, AFTER THE DRONES",
           font=F(DJB, 11), fill=(220, 220, 210))


def art_riyadh(d, x, y, w, h):
    for i in range(h):
        t = i / h
        r = int(30 + (200 - 30) * t * t)
        g = int(40 + (120 - 40) * t * t)
        b = int(80 + (70 - 80) * t * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # skyline
    base = y + h
    for k, (bx, bw, bh, col) in enumerate(
            [(0.02, 0.10, 0.42, (38, 44, 62)), (0.14, 0.08, 0.55, (30, 36, 54)),
             (0.60, 0.09, 0.50, (36, 42, 60)), (0.71, 0.12, 0.62, (30, 36, 54)),
             (0.85, 0.10, 0.38, (40, 46, 64))]):
        x0 = x + int(w * bx)
        d.rectangle([x0, base - int(h * bh), x0 + int(w * bw), base], fill=col)
        for wy in range(4):
            for wx in range(2):
                d.rectangle([x0 + 8 + wx * 16, base - int(h * bh) + 12 + wy * 18,
                             x0 + 18 + wx * 16, base - int(h * bh) + 24 + wy * 18],
                            fill=(250, 210, 120))
    # PIF tower: tall, slightly twisted (two offset slabs)
    tx = x + int(w * 0.36)
    tw = int(w * 0.13)
    d.polygon([(tx, base), (tx + tw, base), (tx + tw - 8, base - int(h * 0.86)),
               (tx + 8, base - int(h * 0.86))], fill=(52, 58, 82))
    for r in range(9):
        wy = base - int(h * 0.80) + r * int(h * 0.085)
        d.line([(tx + 6, wy), (tx + tw - 6, wy)], fill=(250, 210, 120), width=2)
    # scorch + smoke at mid-tower
    sy = base - int(h * 0.45)
    d.ellipse([tx - 6, sy - 14, tx + tw + 6, sy + 14], fill=(60, 40, 30))
    for k, (dx, dy, s) in enumerate([(10, -30, 26), (26, -56, 34), (44, -82, 42)]):
        d.ellipse([tx + dx - s // 2, sy - dy - s, tx + dx + s // 2, sy - dy],
                  fill=(80, 78, 74))
    d.text((x + 10, y + h - 18), "DRAWN SCENE — RIYADH FINANCIAL DISTRICT",
           font=F(DJB, 11), fill=(220, 220, 210))


def art_number(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 16, 18))
    d.rectangle([x, y, x + w, y + 6], fill=RED)
    d.text((x + 22, y + 12), "700,000+", font=F(DJB, 88), fill=(245, 240, 230))
    d.text((x + 24, y + 116), "RUSSIAN SOLDIERS KILLED IN UKRAINE",
           font=F(DJB, 20), fill=(232, 190, 90))
    d.text((x + 24, y + 142), "— new analysis, reported today",
           font=F(DJ, 16), fill=(200, 190, 180))
    # rows of dots = the counted dead (3 rows, inside the panel)
    for r in range(3):
        for c in range(34):
            cx = x + 22 + c * int((w - 44) / 34)
            cy = y + 178 + r * 14
            col = (200, 60, 50) if (r * 34 + c) % 9 == 0 else (120, 90, 88)
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)


ART = {"ship": art_ship, "kyiv": art_kyiv, "riyadh": art_riyadh,
       "number": art_number}


def render(hero, density, layout, out_path):
    stories = stories_for(density)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    n = len(stories)

    # ---- masthead ----
    if layout == "C":
        d.rectangle([0, 0, W, 100], fill=GOLD)
        tcol, dcol = (20, 20, 22), (60, 45, 10)
    else:
        d.rectangle([0, 0, W, 100], fill=NAVY)
        tcol, dcol = (245, 240, 228), (201, 182, 120)
    d.text((24, 10), "THE WORLD IN ONE DAY", font=F(SERIF, 46), fill=tcol)
    d.text((24, 62), "WEDNESDAY 25 NOVEMBER 2026", font=F(DJB, 30), fill=dcol)
    d.text((W - 24, 16), "%d STORIES · 7 REGIONS" % n, font=F(DJB, 15),
           fill=tcol, anchor="ra")
    d.text((W - 24, 40), "FIRST REPORTED TODAY", font=F(DJB, 13),
           fill=dcol, anchor="ra")
    d.text((W - 24, 62), "make.fun daily news image", font=F(DJ, 12),
           fill=tcol, anchor="ra")

    # ---- hero ----
    hy0, hy1 = 100, 340
    head, stand, minis = HERO_COPY[hero]
    if layout == "B":
        ART[hero](d, 16, hy0 + 8, W - 32, 140)
        d.text((24, 256), head, font=F(DJB, 26), fill=INK)
        d.text((24, 288), stand, font=F(DJ, 14), fill=(50, 50, 54))
        d.text((24, 312), " •  ".join(minis), font=F(DJB, 12), fill=RED)
    else:
        ax, aw = (16, 600) if layout != "C" else (408, 600)
        tx = 640 if layout != "C" else 24
        ART[hero](d, ax, hy0 + 8, aw, hy1 - hy0 - 16)
        lines = wrap(d, head, F(DJB, 26), 360)
        yy = hy0 + 20
        for ln in lines:
            d.text((tx, yy), ln, font=F(DJB, 26), fill=INK)
            yy += 31
        yy += 4
        for ln in wrap(d, stand, F(DJ, 15), 360):
            d.text((tx, yy), ln, font=F(DJ, 15), fill=(50, 50, 54))
            yy += 19
        yy += 8
        for m in minis:
            d.text((tx, yy), "▸ " + m, font=F(DJB, 12), fill=RED)
            yy += 18
    d.line([(0, hy1), (W, hy1)], fill=(180, 175, 165), width=2)

    # ---- story grid: 3 columns ----
    cols = [[], [], []]
    for s in stories:
        if s[0] in ("EUROPE", "MIDDLE EAST"):
            cols[0].append(s)
        elif s[0] in ("ASIA-PACIFIC", "AFRICA", "SCIENCE · TECH · SPORT"):
            cols[1].append(s)
        else:
            cols[2].append(s)
    gx0, gy0, gy1 = 16, 354, 928
    cw = 320
    for ci, col in enumerate(cols):
        x = gx0 + ci * (cw + 16)
        y = gy0
        cur_region = None
        tight = len(col) > 14
        for s in col:
            if s[0] != cur_region:
                cur_region = s[0]
                d.rectangle([x, y, x + 10, y + 10], fill=REGION_COLORS[s[0]])
                d.text((x + 16, y - 2), s[0], font=F(DJB, 15),
                       fill=REGION_COLORS[s[0]])
                y += 21
            hl = wrap(d, s[1], F(DJB, 12), cw - 4)[:2]
            for ln in hl:
                d.text((x, y), ln, font=F(DJB, 12), fill=INK)
                y += 13
            if not tight:
                d.text((x, y), s[2] + "  [" + s[3] + "]", font=F(DJ, 10),
                       fill=GREY)
                y += 12
            y += 3
    d.line([(0, gy1), (W, gy1)], fill=(180, 175, 165), width=2)

    # ---- UTC timeline strip ----
    d.text((16, gy1 + 6), "THE DAY IN UTC — FIRST REPORTS",
           font=F(DJB, 13), fill=NAVY)
    xx = 16
    for t, ev in TIMELINE:
        d.text((xx, gy1 + 24), t, font=F(DJB, 14), fill=RED)
        d.text((xx, gy1 + 42), ev, font=F(DJ, 11), fill=INK)
        xx += 250
    d.line([(0, 990), (W, 990)], fill=(180, 175, 165), width=1)

    # ---- date-check footer (one line, fits inside the page) ----
    foot = ("DATE CHECK: every story was first reported on Wed 25 Nov 2026 in some time zone. "
            "Built 01:30 UTC 25 Nov — second sweep before the 27 Nov deadline adds later stories.")
    d.text((16, 1002), foot, font=F(DJ, 10), fill=GREY)
    img.save(out_path, optimize=True)
    return out_path


if __name__ == "__main__":
    hero, density, layout, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    render(hero, density, layout, out)
    print(out)
