#!/usr/bin/env python3
"""THE WORLD TODAY - Sunday 22 November 2026.

Draws a one-page newspaper front page summing up the world's news of
Sunday 22 November 2026 and writes it to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png).

Everything is drawn from code: a hand-written 5x7 bitmap font, a
pure-stdlib PNG encoder, and flat vector illustrations. No image, font
or data file is read from disk, no network is used, and the output is
byte-identical on every run. Python 3, standard library only.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
PAPER = (244, 238, 222)   # warm newsprint
PANEL = (255, 253, 247)   # panel paper
INK = (18, 18, 18)        # headline ink
RED = (178, 24, 24)       # kicker / dateline red
GREY = (110, 104, 90)     # secondary text
NAVY = (26, 38, 62)       # night sky
SKY = (186, 214, 235)     # pale sky
SEA = (52, 110, 164)      # sea blue
GREEN = (46, 125, 50)     # land green
GOLD = (214, 158, 24)     # sun / star gold
ORANGE = (232, 116, 28)   # explosion orange
YELLOW = (250, 204, 21)   # explosion core
BROWN = (146, 96, 48)     # ship hull
STEEL = (120, 128, 138)   # ship / radar grey

# --- canvas ----------------------------------------------------------------
buf = bytearray(W * H * 3)
for i in range(0, W * H * 3, 3):
    buf[i] = PAPER[0]
    buf[i + 1] = PAPER[1]
    buf[i + 2] = PAPER[2]


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        buf[o] = c[0]
        buf[o + 1] = c[1]
        buf[o + 2] = c[2]


def rect(x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        o = (yy * W + x0) * 3
        for xx in range(x0, x1):
            buf[o] = c[0]
            buf[o + 1] = c[1]
            buf[o + 2] = c[2]
            o += 3


def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)


def border(x, y, w, h, c, t=2):
    hline(x, y, w, c, t)
    hline(x, y + h - t, w, c, t)
    vline(x, y, h, c, t)
    vline(x + w - t, y, h, c, t)


def line(x0, y0, x1, y1, c, t=1):
    """Bresenham line, thickness t (square brush)."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        rect(x0 - t // 2, y0 - t // 2, t, t, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def circle(cx, cy, r, c, fill=True):
    if fill:
        for dy in range(-r, r + 1):
            half = int(math.sqrt(max(0, r * r - dy * dy)))
            hline(cx - half, cy + dy, half * 2 + 1, c)
    else:
        for a in range(360):
            rad = math.radians(a)
            px(cx + int(r * math.cos(rad)), cy + int(r * math.sin(rad)), c)


def poly(points, c):
    """Scanline fill of a simple polygon given as [(x, y), ...]."""
    if len(points) < 3:
        return
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                t = (y - y0) / (y1 - y0)
                xs.append(x0 + t * (x1 - x0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            hline(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), c)


def starburst(cx, cy, r_outer, r_inner, spikes, c):
    pts = []
    for i in range(spikes * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
    poly(pts, c)


# --- 5x7 bitmap font -------------------------------------------------------
# Each glyph: 7 rows of 5 bits, '1' = ink. Uppercase only; all copy is set
# in capitals, as a newspaper front page would be.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_char(x, y, ch, scale, c):
    g = FONT.get(ch)
    if g is None:
        return
    for r in range(7):
        row = g[r]
        for col in range(5):
            if row[col] == '1':
                rect(x + col * scale, y + r * scale, scale, scale, c)


def draw_text(x, y, s, scale, c, align='left'):
    if align == 'center':
        x -= text_w(s, scale) // 2
    elif align == 'right':
        x -= text_w(s, scale)
    cx = x
    for ch in s:
        draw_char(cx, y, ch, scale, c)
        cx += 6 * scale
    return cx


def wrap(s, max_w, scale):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines = []
    for para in s.split('\n'):
        words = para.split(' ')
        cur = ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            if text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def text_block(x, y, s, scale, c, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = (leading if leading is not None else 8 * scale)
    for ln in wrap(s, max_w, scale):
        draw_text(x, y, ln, scale, c)
        y += lh
    return y


# --- PNG encoder (pure stdlib, deterministic) --------------------------------
def png_bytes(rgb, w, h):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter: None
        raw += rgb[y * w * 3:(y + 1) * w * 3]
    idat = zlib.compress(bytes(raw), 9)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', idat) + chunk(b'IEND', b''))


# --- illustrations -----------------------------------------------------------
# All flat vector art, drawn from code. No image is read or copied.

def ill_ukraine(x, y, w, h):
    """Night sky over a city skyline, explosion and a missile trail."""
    rect(x, y, w, h, NAVY)
    # stars
    for sx, sy in ((12, 8), (60, 20), (120, 6), (200, 16), (300, 8),
                   (380, 22), (470, 10), (540, 18), (30, 34), (250, 30)):
        if sx < w:
            rect(x + sx, y + sy, 2, 2, YELLOW)
    # skyline silhouettes
    base = y + h
    heights = [46, 70, 38, 84, 56, 96, 44, 66, 52, 78, 40, 62]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        rect(bx + 2, base - bh, bw - 4, bh, (12, 20, 36))
        # lit windows
        for wy in range(base - bh + 8, base - 8, 14):
            for wx in range(bx + 6, bx + bw - 6, 12):
                if (wx * 7 + wy * 13) % 5 == 0:
                    rect(wx, wy, 3, 4, YELLOW)
    # explosion over the skyline, right of centre
    ex, ey = x + int(w * 0.68), y + int(h * 0.42)
    starburst(ex, ey, 34, 14, 8, ORANGE)
    starburst(ex, ey, 22, 9, 8, YELLOW)
    circle(ex, ey, 7, (255, 240, 180))
    # missile streaking in from the top left, with smoke puffs
    line(x + 40, y + 6, ex - 30, ey - 18, (255, 255, 255), 2)
    for d in range(0, 5):
        circle(x + 52 + d * 12, y + 12 + d * 5, 4 + d, (200, 200, 210))
    # searchlight beams
    line(x + int(w * 0.2), base, x + int(w * 0.34), y + 10, (250, 240, 190), 2)
    line(x + int(w * 0.85), base, x + int(w * 0.72), y + 8, (250, 240, 190), 2)


def ill_gulf(x, y, w, h):
    """A tanker on a night sea, radar mast sweeping the sky."""
    rect(x, y, w, h, SKY)
    rect(x, y + int(h * 0.62), w, h - int(h * 0.62), SEA)
    # waves
    for wx in range(x, x + w, 26):
        line(wx, y + int(h * 0.68), wx + 13, y + int(h * 0.68) - 5,
             (255, 255, 255), 2)
        line(wx + 13, y + int(h * 0.68) - 5, wx + 26,
             y + int(h * 0.68), (255, 255, 255), 2)
    # tanker hull and superstructure
    hy = y + int(h * 0.52)
    poly([(x + 18, hy), (x + w - 18, hy), (x + w - 34, hy + 22),
          (x + 34, hy + 22)], (30, 30, 34))
    rect(x + int(w * 0.62), hy - 26, 34, 26, (240, 240, 240))
    rect(x + int(w * 0.62) + 6, hy - 38, 22, 12, (240, 240, 240))
    rect(x + int(w * 0.2), hy - 18, 10, 18, RED)  # funnel
    # radar mast with sweep arcs
    mx = x + int(w * 0.14)
    line(mx, hy, mx, y + 12, INK, 3)
    for r in (10, 20, 30):
        for a in range(200, 341, 4):
            rad = math.radians(a)
            px(mx + int(r * math.cos(rad)), y + 12 + int(r * math.sin(rad)),
               RED)
    circle(mx, y + 12, 3, RED)
    # drone dots in the sky
    for dx, dy in ((0.45, 0.18), (0.55, 0.1), (0.72, 0.22), (0.86, 0.12)):
        circle(x + int(w * dx), y + int(h * dy), 3, INK)


def ill_ballot(x, y, w, h):
    """A ballot box with a ballot paper going in."""
    rect(x, y, w, h, PANEL)
    # ballot paper above the slot
    px0, py0 = x + int(w * 0.34), y + 2
    rect(px0, py0, 34, 22, (255, 255, 255))
    border(px0, py0, 34, 22, INK, 1)
    line(px0 + 7, py0 + 8, px0 + 13, py0 + 15, RED, 2)   # check mark
    line(px0 + 13, py0 + 15, px0 + 27, py0 + 5, RED, 2)
    # box
    bx, by = x + int(w * 0.16), y + 26
    bw, bh = int(w * 0.68), h - 30
    rect(bx, by, bw, bh, (29, 78, 216))
    rect(bx, by, bw, 5, INK)  # slot
    draw_text(bx + bw // 2, by + bh // 2 - 7, "VOTE", 2, (255, 255, 255),
              align='center')


def ill_globe(x, y, w, h):
    """A globe with landmasses and a small sun; the climate talks stall."""
    rect(x, y, w, h, PANEL)
    cx, cy, r = x + w // 2 - 12, y + h // 2, min(w, h) // 2 - 6
    circle(cx, cy, r, SKY)
    # latitude chords
    for dy, frac in ((-r // 2, 0.5), (0, 1.0), (r // 2, 0.5)):
        half = int(r * math.sqrt(max(0.0, 1 - (dy / r) ** 2)))
        hline(cx - half, cy + dy, half * 2, (255, 255, 255), 1)
    # land blobs, fully inside the disc
    circle(cx - r // 3, cy - r // 4, r // 4, GREEN)
    circle(cx + r // 4, cy + r // 5, r // 5, GREEN)
    circle(cx - r // 5, cy + r // 3, r // 6, GREEN)
    circle(cx, cy, r, INK, fill=False)
    # small sun, top right
    sx, sy = x + w - 16, y + 14
    circle(sx, sy, 8, GOLD)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        line(sx + int(11 * math.cos(rad)), sy + int(11 * math.sin(rad)),
             sx + int(16 * math.cos(rad)), sy + int(16 * math.sin(rad)),
             GOLD, 2)


def ill_baltic(x, y, w, h):
    """A cargo ship on grey northern water, drones above."""
    rect(x, y, w, h, (210, 220, 228))
    rect(x, y + int(h * 0.6), w, h - int(h * 0.6), SEA)
    for wx in range(x, x + w, 22):
        line(wx, y + int(h * 0.66), wx + 11, y + int(h * 0.66) - 4,
             (255, 255, 255), 2)
        line(wx + 11, y + int(h * 0.66) - 4, wx + 22, y + int(h * 0.66),
             (255, 255, 255), 2)
    # cargo ship with stacked containers
    hy = y + int(h * 0.48)
    poly([(x + 14, hy), (x + w - 14, hy), (x + w - 28, hy + 20),
          (x + 28, hy + 20)], BROWN)
    for i, cc in enumerate((RED, GOLD, GREEN, STEEL)):
        rect(x + 30 + i * 26, hy - 16, 22, 16, cc)
    rect(x + w - 62, hy - 30, 26, 30, (240, 240, 240))
    # two drones with dotted trails
    for dx, dy in ((0.3, 0.14), (0.62, 0.08)):
        ddx, ddy = x + int(w * dx), y + int(h * dy)
        rect(ddx - 5, ddy - 2, 10, 4, INK)
        line(ddx, ddy + 4, ddx - 8, ddy + 16, INK, 1)
        line(ddx, ddy + 4, ddx + 8, ddy + 16, INK, 1)


def ill_estonia_flag(x, y, w, h):
    """The Estonian tricolour: blue, black, white."""
    third = h // 3
    rect(x, y, w, third, (0, 114, 206))
    rect(x, y + third, w, third, INK)
    rect(x, y + 2 * third, w, h - 2 * third, (255, 255, 255))
    border(x, y, w, h, INK, 1)


# --- page layout -------------------------------------------------------------
PAD = 16


def panel(x, y, w, h):
    rect(x, y, w, h, PANEL)
    border(x, y, w, h, INK, 2)
    return x + PAD, y + PAD, w - 2 * PAD, h - 2 * PAD


def kicker(x, y, s, c=RED):
    draw_text(x, y, s, 2, c)
    return y + 18


def headline(x, y, s, scale, max_w):
    for ln in wrap(s, max_w, scale):
        draw_text(x, y, ln, scale, INK)
        y += 8 * scale
    return y + 4


def draw_page():
    # outer frame
    border(8, 8, W - 16, H - 16, INK, 3)

    # masthead
    draw_text(W // 2, 28, "THE WORLD TODAY", 7, INK, align='center')
    hline(24, 92, W - 48, INK, 3)
    draw_text(W // 2, 102, "SUNDAY 22 NOVEMBER 2026", 3, RED, align='center')
    draw_text(W // 2, 128, "SIX STORIES FROM FIVE CONTINENTS", 2, INK,
              align='center')
    hline(24, 152, W - 48, INK, 2)
    hline(24, 156, W - 48, RED, 3)

    # --- row A: lead (Ukraine) + Gulf --------------------------------------
    # lead
    ix, iy, iw, ih = panel(24, 168, 616, 310)
    y = kicker(ix, iy, "WAR IN UKRAINE")
    y = headline(ix, y, "MISSILES RAIN ON UKRAINE OVERNIGHT", 4, iw)
    draw_text(ix, y, "50+ MISSILES, 500 DRONES - FIVE KILLED", 2, RED)
    y += 22
    y = text_block(ix, y,
                   "RUSSIA FIRED MORE THAN 50 MISSILES AND ABOUT 500 "
                   "DRONES OVERNIGHT SATURDAY INTO SUNDAY. FIVE PEOPLE "
                   "WERE KILLED, INCLUDING A FAMILY OF FOUR NEAR LVIV. "
                   "POLAND SCRAMBLED JETS AS MISSILES NEARED ITS AIRSPACE.",
                   2, INK, iw)
    ill_ukraine(ix, y + 8, iw, 168 + 310 - PAD - (y + 8))

    # gulf
    ix, iy, iw, ih = panel(656, 168, 344, 310)
    y = kicker(ix, iy, "THE GULF")
    y = headline(ix, y, "IRAN STRIKES US BASES IN BAHRAIN", 3, iw)
    y = text_block(ix, y,
                   "TEHRAN CLAIMS MISSILES AND DRONES HIT US PATRIOT "
                   "RADARS AT AL-RIFFA AND AWALI. BAHRAIN SAYS ITS "
                   "DEFENCES INTERCEPTED THE ATTACK. REPORTED SUNDAY.",
                   2, INK, iw)
    ill_gulf(ix, y + 8, iw, 168 + 310 - PAD - (y + 8))

    # --- row B: Hong Kong / COP31 / Baltic ---------------------------------
    ix, iy, iw, ih = panel(24, 494, 320, 232)
    y = kicker(ix, iy, "ASIA - THE VOTE")
    y = headline(ix, y, "HONG KONG VOTES FOR 723 SEATS", 3, iw)
    y = text_block(ix, y,
                   "856 CANDIDATES CONTEST 723 SEATS ON THE ELECTION "
                   "COMMITTEE. POLLS 9 AM TO 6 PM.",
                   2, INK, iw)
    ill_ballot(ix, y + 6, iw, 494 + 232 - PAD - (y + 6))

    ix, iy, iw, ih = panel(360, 494, 304, 232)
    y = kicker(ix, iy, "CLIMATE")
    y = headline(ix, y, "COP31 TALKS DEADLOCKED", 3, iw)
    y = text_block(ix, y,
                   "UN CLIMATE TALKS STALL OVER FOSSIL FUELS AND "
                   "FINANCE. NO DEAL YET AS THE SUMMIT NEARS ITS END.",
                   2, INK, iw)
    ill_globe(ix, y + 6, iw, 494 + 232 - PAD - (y + 6))

    ix, iy, iw, ih = panel(680, 494, 320, 232)
    y = kicker(ix, iy, "EUROPE - THE BALTIC")
    y = headline(ix, y, "DRONES HIT SHIP IN THE BALTIC", 3, iw)
    y = text_block(ix, y,
                   "DRONES STRIKE A RUSSIA-BOUND CARGO SHIP IN THE "
                   "GULF OF FINLAND. FINLAND TIGHTENS SECURITY AROUND "
                   "ITS WATERS.",
                   2, INK, iw)
    ill_baltic(ix, y + 6, iw, 494 + 232 - PAD - (y + 6))

    # --- row C: Estonia + briefs -------------------------------------------
    ix, iy, iw, ih = panel(24, 742, 476, 186)
    y = kicker(ix, iy, "EUROPE - THE BORDER")
    y = headline(ix, y, "ESTONIA TO SHUT BORDER WITH RUSSIA", 3, iw)
    y = text_block(ix, y,
                   "TALLINN MOVES TO CLOSE ITS BORDER WITH RUSSIA. "
                   "MOSCOW CALLS THE STEP A 'NEW IRON CURTAIN'.",
                   2, INK, iw)
    ill_estonia_flag(ix, y + 8, iw, 742 + 186 - PAD - (y + 8))

    ix, iy, iw, ih = panel(516, 742, 484, 186)
    y = kicker(ix, iy, "IN BRIEF - SATURDAY")
    draw_text(ix, y, "EU-INDONESIA DEAL:", 2, RED)
    y += 16
    y = text_block(ix, y,
                   "AFTER 10 YEARS OF TALKS, THE EU AND INDONESIA SIGN "
                   "A TRADE PACT SCRAPPING TARIFFS ON 98% OF GOODS.",
                   2, INK, iw)
    y += 6
    draw_text(ix, y, "MEXICO:", 2, RED)
    y += 16
    y = text_block(ix, y,
                   "TROOPS CAPTURE FBI MOST-WANTED DRUG LORD 'CHAPO "
                   "ISIDRO' IN SINALOA. ELEVEN KILLED.",
                   2, INK, iw)

    # --- footer ---------------------------------------------------------------
    hline(24, 944, W - 48, INK, 2)
    draw_text(W // 2, 954,
              "ALL SIX STORIES HAPPENED OR WERE FIRST REPORTED ON",
              2, INK, align='center')
    draw_text(W // 2, 972, "SUNDAY 22 NOVEMBER 2026", 2, RED, align='center')
    draw_text(W // 2, 992,
              "SOURCES: REUTERS, AP, BBC, AL JAZEERA, HONG KONG GOVERNMENT",
              2, GREY, align='center')


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(outdir, exist_ok=True)
    draw_page()
    data = png_bytes(buf, W, H)
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
