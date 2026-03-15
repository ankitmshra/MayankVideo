#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  verse3 / line01 — "I got the universe in my hand i can do      ║
║                      anything"                                   ║
║                                                                  ║
║  3D UNIVERSE — Retro Pixel Art Lyrics Video                      ║
║  Output : verse3_line01_UNIVERSE_3D.mp4  (1920×1080 @ 60fps)    ║
║                                                                  ║
║  INSTALL (one-time):                                             ║
║    pip install numpy opencv-python                               ║
║                                                                  ║
║  RUN:                                                            ║
║    python verse3_line01_universe.py                              ║
╚══════════════════════════════════════════════════════════════════╝

SCENE LAYERS (back → front)
  1. Deep space void background
  2. 3D Warp Tunnel  — 400 stars with perspective projection +
                        depth-scaled streaks, accelerating warp
  3. Volumetric Nebula Clouds — 7 additive colour blobs, slow drift
  4. Distant Galaxies — 8 tiny pixel sprite galaxies at the edges
  5. Galaxy Spiral  — 560 stars in two logarithmic arms, 3D tilted
                       disk with slow Y-axis spin, additive core glow
  6. 3D Planets  — Lambertian-shaded gas giant (with rings +
                    Jupiter bands), orbiting blue world, ice moon
  7. Cosmic Hand — two cupped hands rise at "IN MY HAND" (t=1.10s)
  8. Lyric Text  — big pixel-bitmap font, chunk-by-chunk flash
  9. CRT Scanlines
"""

import math
import random
import os
import numpy as np
import cv2

# ──────────────────────────────────────────────────────────────
# OUTPUT PATH  — change this if you want the file somewhere else
# ──────────────────────────────────────────────────────────────
OUT_FILE = "verse3_line01_UNIVERSE_3D.mp4"

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────
W, H   = 1920, 1080      # final output resolution
FPS    = 60
PX     = 4               # each virtual pixel = 4×4 real pixels
GW, GH = W // PX, H // PX   # virtual canvas: 480 × 270

# ──────────────────────────────────────────────────────────────
# RETRO PALETTE  (NES / CGA inspired)
# ──────────────────────────────────────────────────────────────
PAL = {
    'BLACK':    (0,   0,   0  ),
    'WHITE':    (252, 252, 252),
    'YELLOW':   (248, 216, 0  ),
    'GOLD':     (252, 188, 0  ),
    'ORANGE':   (228, 92,  16 ),
    'RED':      (188, 0,   32 ),
    'CYAN':     (0,   232, 216),
    'LTCYAN':   (120, 252, 252),
    'BLUE':     (0,   80,  188),
    'DKBLUE':   (0,   0,   80 ),
    'LTBLUE':   (108, 148, 252),
    'MAGENTA':  (188, 0,   188),
    'PURPLE':   (80,  0,   140),
    'DKPURPLE': (30,  0,   60 ),
    'PINK':     (252, 80,  200),
    'GREEN':    (0,   168, 0  ),
    'LTGREEN':  (80,  252, 80 ),
    'GREY':     (100, 100, 120),
    'DKGREY':   (30,  30,  45 ),
    'LTGREY':   (180, 180, 200),
    'NEBRED':   (180, 40,  80 ),
    'NEBBLUE':  (20,  60,  180),
    'NEBPURP':  (120, 20,  160),
    'NEBCYAN':  (20,  140, 180),
    'STARDIM':  (60,  60,  90 ),
    'STARBRT':  (220, 220, 255),
    'STARGOLD': (255, 200, 80 ),
    'STARBLUE': (80,  160, 255),
}

# ──────────────────────────────────────────────────────────────
# PIXEL FONT  5×7 bitmap  (uppercase A-Z, digits, punctuation)
# ──────────────────────────────────────────────────────────────
FONT = {
    'A': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    'C': [0b01111, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b01111],
    'D': [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    'E': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    'G': [0b01111, 0b10000, 0b10000, 0b10011, 0b10001, 0b10001, 0b01111],
    'H': [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'I': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b11111],
    'J': [0b00111, 0b00001, 0b00001, 0b00001, 0b10001, 0b10001, 0b01110],
    'K': [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10001, 0b10001, 0b10001, 0b10001],
    'N': [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    'S': [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
    'X': [0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b01010, 0b10001],
    'Y': [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    '0': [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b11111],
    '2': [0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
    '3': [0b11111, 0b00001, 0b00010, 0b00110, 0b00001, 0b10001, 0b01110],
    ' ': [0] * 7,
    '.': [0, 0, 0, 0, 0, 0b00110, 0b00110],
    '!': [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
    "'": [0b00110, 0b00110, 0b00100, 0, 0, 0, 0],
}

# ──────────────────────────────────────────────────────────────
# LYRIC CHUNKS  (t_start, text, foreground, shadow)
# ──────────────────────────────────────────────────────────────
CHUNKS = [
    (0.00, "I GOT THE",  PAL['LTCYAN'],  PAL['BLUE']),
    (0.55, "UNIVERSE",   PAL['MAGENTA'], PAL['PURPLE']),
    (1.10, "IN MY HAND", PAL['LTCYAN'],  PAL['BLUE']),
    (1.80, "I CAN DO",   PAL['GOLD'],    PAL['ORANGE']),
    (2.35, "ANYTHING",   PAL['WHITE'],   PAL['LTGREY']),
]
DUR = 3.0   # total animation duration in seconds

def active_chunk(t):
    cur = CHUNKS[0]
    for ch in CHUNKS:
        if t >= ch[0]:
            cur = ch
    return cur

# ──────────────────────────────────────────────────────────────
# CANVAS UTILITIES
# ──────────────────────────────────────────────────────────────

def new_canvas():
    """Return a blank GW×GH RGB uint8 numpy array."""
    return np.zeros((GH, GW, 3), dtype=np.uint8)

def spx(c, x, y, col):
    """Set a single virtual pixel (bounds-checked)."""
    if 0 <= x < GW and 0 <= y < GH:
        c[y, x] = col

def spx_add(c, x, y, col):
    """Additive blend a pixel — used for glows."""
    if 0 <= x < GW and 0 <= y < GH:
        c[y, x] = np.clip(c[y, x].astype(int) + col, 0, 255)

def upscale(c):
    """
    Nearest-neighbour upscale: GW×GH  →  W×H.
    Returns BGR array ready for cv2.VideoWriter.
    """
    big = np.repeat(np.repeat(c, PX, axis=0), PX, axis=1)
    return cv2.cvtColor(big.astype(np.uint8), cv2.COLOR_RGB2BGR)

def draw_rect(c, x, y, w, h, col):
    y1, y2 = max(0, y),   min(GH, y + h)
    x1, x2 = max(0, x),   min(GW, x + w)
    if x2 > x1 and y2 > y1:
        c[y1:y2, x1:x2] = col

def draw_char(c, ch, cx, cy, col, sc=1):
    bits = FONT.get(ch.upper(), FONT[' '])
    for row, b in enumerate(bits):
        for col_i in range(5):
            if b & (1 << (4 - col_i)):
                for dy in range(sc):
                    for dx in range(sc):
                        spx(c, cx + col_i * sc + dx, cy + row * sc + dy, col)

def text_w(txt, sc=1):
    return len(txt) * (5 * sc + sc)

def draw_text_c(c, txt, cy, col, sc=1):
    """Draw text centred horizontally."""
    tw = text_w(txt, sc)
    x  = (GW - tw) // 2
    for ch in txt.upper():
        draw_char(c, ch, x, cy, col, sc)
        x += 5 * sc + sc

def draw_text_shadow_c(c, txt, cy, fg, sh, sc=1):
    draw_text_c(c, txt, cy + 1, sh, sc)
    draw_text_c(c, txt, cy,     fg, sc)

def scanlines(c, a=0.20):
    """Darken every other row — CRT effect."""
    c[1::2] = (c[1::2] * (1 - a)).astype(np.uint8)

# ──────────────────────────────────────────────────────────────
# LAYER 1 — DEEP SPACE BACKGROUND
# ──────────────────────────────────────────────────────────────

def draw_background(c, t):
    for gy in range(GH):
        frac = gy / GH
        r = int(2 + frac * 4)
        g = int(0 + frac * 2)
        b = int(8 + frac * 16 + math.sin(t * 0.3) * 4)
        c[gy, :] = (min(255, r), min(255, g), min(255, b))

# ──────────────────────────────────────────────────────────────
# LAYER 2 — 3D WARP TUNNEL
#   400 stars stored as 3D points (x, y, z).
#   Each frame: z advances → stars fly toward the camera.
#   Perspective projection: sx = cx + x/z * FOCAL
#   Closer stars are brighter, bigger, and draw longer streaks.
# ──────────────────────────────────────────────────────────────

class WarpTunnel:
    N     = 400
    FOCAL = 180
    SPEED = 50   # z-units consumed per second at 1× speed

    def __init__(self, seed=7):
        rng = np.random.default_rng(seed)
        self.x      = rng.uniform(-220, 220, self.N)
        self.y      = rng.uniform(-130, 130, self.N)
        self.base_z = rng.uniform(1, 500, self.N)
        self.stype  = rng.integers(0, 4, self.N)   # 0=dim 1=white 2=blue 3=gold

    def draw(self, c, t, speed_mul=1.0):
        cx, cy = GW // 2, GH // 2
        z_shift = (t * self.SPEED * speed_mul) % 500
        z = ((self.base_z - z_shift - 1) % 499) + 1

        order = np.argsort(z)[::-1]   # back-to-front
        COLS  = [PAL['STARDIM'], PAL['STARBRT'], PAL['STARBLUE'], PAL['STARGOLD']]

        for i in order:
            zi = z[i]
            sx = int(cx + self.x[i] / zi * self.FOCAL)
            sy = int(cy + self.y[i] / zi * self.FOCAL)
            if not (0 <= sx < GW and 0 <= sy < GH):
                continue

            depth_frac = 1.0 - zi / 500.0
            col        = COLS[self.stype[i]]
            brightness = depth_frac ** 1.5
            col_s      = tuple(int(col[k] * brightness) for k in range(3))

            # Streak toward previous position
            prev_zi    = min(zi + self.SPEED * speed_mul * (1 / FPS) * 5, 500)
            if prev_zi > 1:
                psx = int(cx + self.x[i] / prev_zi * self.FOCAL)
                psy = int(cy + self.y[i] / prev_zi * self.FOCAL)
                streak_len = max(1, int(depth_frac * 8))
                dx, dy = sx - psx, sy - psy
                for s in range(streak_len):
                    frac  = s / streak_len
                    fade  = tuple(int(col_s[k] * (1 - frac * 0.7)) for k in range(3))
                    spx(c, int(sx - dx * frac), int(sy - dy * frac), fade)

            # Core dot (larger when close)
            spx(c, sx, sy, col_s)
            if depth_frac > 0.7:
                spx(c, sx + 1, sy, col_s)
                spx(c, sx, sy + 1, col_s)
            if depth_frac > 0.85:
                spx(c, sx - 1, sy, col_s)
                spx(c, sx, sy - 1, col_s)

# ──────────────────────────────────────────────────────────────
# LAYER 3 — GALAXY SPIRAL  (3D tilted rotating disk)
#   Two logarithmic arms + diffuse halo.
#   3D rotation: Y-axis spin (slow) + X-axis tilt (constant ~22°)
#   so the disk is seen in perspective rather than face-on.
# ──────────────────────────────────────────────────────────────

class Galaxy:
    N_ARM  = 280
    N_HALO = 120
    TILT   = 0.38   # X-axis tilt in radians
    FOCAL  = 300

    def __init__(self, seed=42):
        rng   = np.random.default_rng(seed)
        stars = []

        for arm in range(2):
            arm_off = arm * math.pi
            for i in range(self.N_ARM):
                frac    = i / self.N_ARM
                r       = 2 + frac * 90
                theta   = frac * 4.5 * math.pi + arm_off
                scatter = rng.uniform(0, 6) * (1 + frac)
                r      += rng.normal(0, scatter * 0.3)
                theta  += rng.normal(0, 0.15)

                x3 = r * math.cos(theta)
                y3 = r * math.sin(theta) * 0.18   # thin disk
                z3 = r * math.sin(theta) * 0.95

                brt = min(1.3, 0.3 + 0.7 * (1 - frac) + rng.uniform(0, 0.3))
                ct  = (3 if frac < 0.2
                       else int(rng.choice([1, 2, 3])) if frac < 0.5
                       else int(rng.choice([1, 2])))
                stars.append((x3, y3, z3, brt, ct))

        for _ in range(self.N_HALO):
            r     = rng.uniform(60, 120)
            theta = rng.uniform(0, 2 * math.pi)
            phi   = rng.uniform(0, 2 * math.pi)
            x3 = r * math.cos(theta) * math.cos(phi)
            y3 = r * math.sin(phi) * 0.4
            z3 = r * math.sin(theta) * math.cos(phi)
            stars.append((x3, y3, z3, rng.uniform(0.1, 0.35), 0))

        self.stars = stars
        self.cx    = GW // 2
        self.cy    = GH // 2 - 20

    def _project(self, x3, y3, z3, rot_y, tilt_x):
        # Y-axis rotation (spin)
        x2 =  x3 * math.cos(rot_y) + z3 * math.sin(rot_y)
        z2 = -x3 * math.sin(rot_y) + z3 * math.cos(rot_y)
        y2 = y3
        # X-axis rotation (tilt → 3D look)
        y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
        z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
        x3_ = x2
        depth = z3_ + 300
        if depth < 1:
            depth = 1
        sx = self.cx + int(x3_ / depth * self.FOCAL)
        sy = self.cy + int(y3_ / depth * self.FOCAL)
        return sx, sy, depth

    def draw(self, c, t):
        rot_y  = t * 0.4
        tilt_x = self.TILT
        COLS   = [PAL['STARDIM'], PAL['STARBRT'], PAL['STARBLUE'], PAL['STARGOLD']]

        projected = []
        for x3, y3, z3, brt, ct in self.stars:
            sx, sy, depth = self._project(x3, y3, z3, rot_y, tilt_x)
            projected.append((depth, sx, sy, brt, ct))
        projected.sort(reverse=True)

        for depth, sx, sy, brt, ct in projected:
            if not (0 <= sx < GW and 0 <= sy < GH):
                continue
            col   = COLS[ct]
            col_s = tuple(min(255, int(col[k] * brt)) for k in range(3))
            spx(c, sx, sy, col_s)
            if brt > 0.8:
                spx(c, sx + 1, sy, col_s)
                spx(c, sx, sy + 1, col_s)

        # Additive core glow
        cx_s, cy_s, _ = self._project(0, 0, 0, rot_y, tilt_x)
        core_rings = [
            (20, PAL['WHITE']),
            (14, PAL['GOLD']),
            (8,  PAL['YELLOW']),
            (4,  PAL['WHITE']),
        ]
        for r, col in core_rings:
            for a_step in range(32):
                a = a_step * math.pi * 2 / 32
                for ri in range(r):
                    frac = 1 - ri / r
                    px_  = cx_s + int(math.cos(a) * ri)
                    py_  = cy_s + int(math.sin(a) * ri * 0.5)   # flattened
                    gc   = tuple(int(col[k] * frac * 0.4) for k in range(3))
                    spx_add(c, px_, py_, gc)

# ──────────────────────────────────────────────────────────────
# LAYER 4 — VOLUMETRIC NEBULA CLOUDS
#   Pre-computed elliptical pixel blobs, alpha-composited
#   each frame with slight drift and depth-pulse.
# ──────────────────────────────────────────────────────────────

class Nebula:
    def __init__(self, seed=99):
        cloud_defs = [
            # cx_frac  cy_frac  rx  ry  colour_key   intensity
            (0.50, 0.45, 80, 40, 'NEBPURP', 0.18),
            (0.35, 0.35, 60, 30, 'NEBBLUE', 0.14),
            (0.65, 0.55, 55, 28, 'NEBRED',  0.12),
            (0.50, 0.50, 40, 20, 'NEBCYAN', 0.16),
            (0.25, 0.60, 45, 22, 'NEBPURP', 0.10),
            (0.75, 0.40, 50, 25, 'NEBBLUE', 0.11),
            (0.50, 0.30, 35, 18, 'NEBRED',  0.13),
        ]
        self.clouds = []
        for cx_f, cy_f, rx, ry, col_key, intensity in cloud_defs:
            cx_  = int(cx_f * GW)
            cy_  = int(cy_f * GH)
            col  = PAL[col_key]
            pxls = []
            for dy in range(-ry, ry + 1, 2):
                for dx in range(-rx, rx + 1, 2):
                    d2 = (dx / rx) ** 2 + (dy / ry) ** 2
                    if d2 < 1.0:
                        alpha = (1 - d2) ** 1.5 * intensity
                        pxls.append((dx, dy, alpha))
            self.clouds.append((cx_, cy_, col, pxls))

    def draw(self, c, t):
        for i, (cx_, cy_, col, pxls) in enumerate(self.clouds):
            drift_x = int(math.sin(t * 0.15 + i) * 3)
            drift_y = int(math.cos(t * 0.12 + i * 0.7) * 2)
            pulse   = 1 + 0.08 * math.sin(t * 0.5 + i * 1.3)
            for dx, dy, alpha in pxls:
                px_ = cx_ + dx + drift_x
                py_ = cy_ + dy + drift_y
                if 0 <= px_ < GW and 0 <= py_ < GH:
                    existing = c[py_, px_].astype(int)
                    blend    = tuple(int(existing[k] + col[k] * alpha * pulse)
                                     for k in range(3))
                    c[py_, px_] = [min(255, v) for v in blend]

# ──────────────────────────────────────────────────────────────
# LAYER 5 — DISTANT GALAXIES  (tiny pixel sprites)
# ──────────────────────────────────────────────────────────────

_GSPRITES = {
    'spiral': ["  *  ", " *** ", "*****", " *** ", "  *  "],
    'ellip':  [" *** ", "*****", " *** "],
    'bar':    ["*   *", " *** ", "*****", " *** ", "*   *"],
}

def draw_distant_galaxies(c, t):
    defs = [
        (40,  30,  'spiral', 'LTBLUE',  0.60),
        (420, 50,  'ellip',  'GOLD',    0.50),
        (80,  200, 'bar',    'PINK',    0.40),
        (440, 180, 'spiral', 'LTCYAN',  0.55),
        (20,  140, 'ellip',  'LTGREY',  0.30),
        (460, 240, 'spiral', 'MAGENTA', 0.45),
        (200, 15,  'bar',    'LTBLUE',  0.35),
        (380, 260, 'ellip',  'GOLD',    0.40),
    ]
    for gx, gy, stype, col_key, brt in defs:
        col  = PAL[col_key]
        gx_  = gx + int(math.sin(t * 0.1 + gx) * 1)
        gy_  = gy + int(math.cos(t * 0.08 + gy) * 1)
        for row, line in enumerate(_GSPRITES[stype]):
            for ci, ch in enumerate(line):
                if ch == '*':
                    spx(c, gx_ + ci, gy_ + row,
                        tuple(int(col[k] * brt) for k in range(3)))

# ──────────────────────────────────────────────────────────────
# LAYER 6 — 3D SHADED PLANETS
#   Lambertian + specular lighting, quantised to 4 shading bands
#   (authentic pixel-art look). Gas giant gets horizontal bands
#   and a Saturn-style ring drawn back and front separately.
# ──────────────────────────────────────────────────────────────

def _shaded_sphere(c, cx, cy, r, base_col, light_col, dark_col):
    ld = (-0.6, -0.7, 0.4)
    ld_len = math.sqrt(sum(v ** 2 for v in ld))
    ld = tuple(v / ld_len for v in ld)

    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            d2 = dx * dx + dy * dy
            if d2 > r * r:
                continue
            nz  = math.sqrt(max(0, r * r - d2)) / r
            nx_ = dx / r
            ny_ = dy / r
            dot  = nx_ * ld[0] + ny_ * ld[1] + nz * ld[2]
            dot  = max(0, dot)
            spec = max(0, dot) ** 8 * 0.5

            if dot > 0.65 or spec > 0.3:
                col = light_col
            elif dot > 0.35:
                col = base_col
            elif dot > 0.1:
                col = tuple(int(base_col[k] * 0.6) for k in range(3))
            else:
                col = dark_col

            if spec > 0.3:
                col = tuple(min(255, int(col[k] * 1.5 + 60)) for k in range(3))

            spx(c, cx + dx, cy + dy, col)


def _planet_ring(c, cx, cy, r_in, r_out, col, tilt=0.25):
    for rx in range(-r_out - 1, r_out + 2):
        d = abs(rx)
        if d < r_in or d > r_out:
            continue
        spx(c, cx + rx, cy + int(-d * tilt), col)
        spx(c, cx + rx, cy + int( d * tilt), col)


def draw_planets(c, t):
    # ── Gas Giant (with rings + Jupiter bands) ────────────────
    gj_x = GW // 2 - 90 + int(math.sin(t * 0.3) * 4)
    gj_y = GH // 2 + 15 + int(math.cos(t * 0.2) * 3)
    gj_r = 22

    _planet_ring(c, gj_x, gj_y, gj_r + 3, gj_r + 12, PAL['GOLD'],   tilt=0.22)
    _planet_ring(c, gj_x, gj_y, gj_r + 4, gj_r + 10, PAL['ORANGE'], tilt=0.22)

    _shaded_sphere(c, gj_x, gj_y, gj_r,
                   base_col=(180, 110, 60),
                   light_col=(240, 190, 130),
                   dark_col=(80, 40, 20))

    # Horizontal cloud bands
    for band_col, fy in [(PAL['ORANGE'], 0.15), ((160, 80, 30), 0.35),
                          (PAL['GOLD'], 0.5), ((140, 70, 25), 0.65),
                          (PAL['ORANGE'], 0.80)]:
        by_ = gj_y - gj_r + int(fy * gj_r * 2)
        for dx in range(-gj_r, gj_r + 1):
            if dx * dx + (by_ - gj_y) ** 2 < gj_r * gj_r:
                existing = c[by_, gj_x + dx].astype(int)
                blended  = tuple(int(existing[k] * 0.55 + band_col[k] * 0.45)
                                 for k in range(3))
                spx(c, gj_x + dx, by_, blended)

    # Front half of ring (redrawn over planet)
    _planet_ring(c, gj_x, gj_y + 2, gj_r + 4, gj_r + 12, PAL['GOLD'], tilt=0.22)

    # ── Blue Orbiting World ───────────────────────────────────
    orb_r = 75
    orb_t = t * 0.55
    mp_x  = GW // 2 + 80 + int(math.cos(orb_t) * orb_r)
    mp_y  = GH // 2 - 30 + int(math.sin(orb_t) * orb_r * 0.35)
    mp_r  = 13
    _shaded_sphere(c, mp_x, mp_y, mp_r,
                   base_col=(20, 60, 160),
                   light_col=(80, 160, 252),
                   dark_col=(5, 15, 50))
    for cp in range(3):
        cpx = mp_x - 6 + cp * 5 + int(math.sin(t * 0.4 + cp) * 2)
        cpy = mp_y - 3 + int(math.cos(t * 0.3 + cp) * 2)
        if (cpx - mp_x) ** 2 + (cpy - mp_y) ** 2 < mp_r * mp_r:
            spx(c, cpx, cpy, (160, 200, 252))

    # ── Ice Moon ──────────────────────────────────────────────
    moon_t = t * 1.2
    sm_x   = GW // 2 + 100 + int(math.cos(moon_t) * 40)
    sm_y   = GH // 2 + 40  + int(math.sin(moon_t) * 16)
    sm_r   = 7
    _shaded_sphere(c, sm_x, sm_y, sm_r,
                   base_col=(140, 140, 160),
                   light_col=(210, 215, 240),
                   dark_col=(40, 40, 60))
    spx(c, sm_x - 2, sm_y - 1, PAL['DKGREY'])
    spx(c, sm_x - 3, sm_y - 1, PAL['GREY'])

    # Dotted orbit path
    for a_step in range(64):
        a  = a_step * math.pi * 2 / 64
        ox = int(GW // 2 + 80 + math.cos(a) * orb_r)
        oy = int(GH // 2 - 30 + math.sin(a) * orb_r * 0.35)
        if a_step % 3 == 0:
            spx(c, ox, oy, PAL['DKGREY'])

# ──────────────────────────────────────────────────────────────
# LAYER 7 — COSMIC HAND
#   Two mirrored pixel-art hands rise from the bottom of the
#   frame after "IN MY HAND" (t = 1.10s), cupping the galaxy.
# ──────────────────────────────────────────────────────────────

_HAND = [
    "........####....",
    ".......######...",
    "......########..",
    ".....##########.",
    "....############",
    "....############",
    "...#############",
    "...##.##.##.####",
    "...##.##.##.####",
    "....############",
    ".....###########",
    "......##########",
    ".......#########",
    "........########",
    ".........#######",
    "..........######",
]

def draw_hand(c, t, alpha):
    if alpha <= 0:
        return
    hw  = len(_HAND[0])
    hh  = len(_HAND)
    rise = int((1 - alpha) * 40)
    bx   = GW // 2 - hw - 2
    by   = GH - hh - 8 + rise
    lc   = (100, 130, 180)

    for row, line in enumerate(_HAND):
        for ci, ch in enumerate(line):
            if ch == '#':
                shade = 1 - (row + ci) / (hh + hw) * 0.5
                spx(c, bx + ci, by + row,
                    tuple(int(lc[k] * shade * alpha) for k in range(3)))

    bx2 = GW // 2 + 2
    for row, line in enumerate(_HAND):
        mir = line[::-1]
        for ci, ch in enumerate(mir):
            if ch == '#':
                shade = 1 - (row + (hw - ci)) / (hh + hw) * 0.5
                spx(c, bx2 + ci, by + row,
                    tuple(int(lc[k] * shade * alpha) for k in range(3)))

    # Fingertip energy glow
    if alpha > 0.5:
        glow_y = by + 3
        for gx in range(bx - 2, bx2 + hw + 3):
            if int(t * 6 + gx) % 3 == 0:
                gc = tuple(int(PAL['CYAN'][k] * (alpha - 0.5) * 2 * 0.4)
                           for k in range(3))
                spx_add(c, gx, glow_y, gc)

# ──────────────────────────────────────────────────────────────
# MASTER FRAME RENDERER
# ──────────────────────────────────────────────────────────────

def render_frame(t, warp, galaxy, nebula):
    c = new_canvas()

    draw_background(c, t)                           # Layer 1
    warp.draw(c, t, speed_mul=1.0 + t * 0.8)        # Layer 2
    nebula.draw(c, t)                               # Layer 3
    draw_distant_galaxies(c, t)                     # Layer 4
    galaxy.draw(c, t)                               # Layer 5
    draw_planets(c, t)                              # Layer 6

    hand_alpha = min(1.0, max(0.0, (t - 1.10) / 0.8))
    draw_hand(c, t, hand_alpha)                     # Layer 7

    # ── Lyric text ────────────────────────────────────────────
    t_start, text, fg, shadow = active_chunk(t)
    chunk_age = t - t_start
    flash     = chunk_age < 0.08
    scl       = 4 if len(text) <= 8 else (3 if len(text) <= 12 else 2)
    ty        = GH - 52

    if flash:
        draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
    else:
        draw_text_shadow_c(c, text, ty, fg, shadow, scl)

    # Pixel-art side brackets
    tw_ = text_w(text, scl)
    lx_ = (GW - tw_) // 2 - 5
    rx_ = (GW + tw_) // 2 + 1
    for bdy in range(scl * 7 + 2):
        spx(c, lx_,     ty - 1 + bdy, fg)
        spx(c, lx_ + 1, ty - 1 + bdy, fg)
        spx(c, rx_,     ty - 1 + bdy, fg)
        spx(c, rx_ + 1, ty - 1 + bdy, fg)

    scanlines(c, 0.20)                              # Layer 9
    return c

# ──────────────────────────────────────────────────────────────
# TITLE CARD FRAME
# ──────────────────────────────────────────────────────────────

def title_frame(ft, warp):
    tc = new_canvas()
    for gy in range(GH):
        tc[gy, :] = (2, 0, int(10 + gy * 0.04))
    warp.draw(tc, ft * 0.5, 0.4)

    bord = PAL['MAGENTA'] if int(ft * 4) % 2 == 0 else PAL['DKGREY']
    draw_rect(tc, 2, 2,      GW - 4, 1,      bord)
    draw_rect(tc, 2, GH - 3, GW - 4, 1,      bord)
    draw_rect(tc, 2, 2,      1,      GH - 4, bord)
    draw_rect(tc, GW - 3, 2, 1,      GH - 4, bord)

    draw_text_shadow_c(tc, "VERSE  3",          GH // 2 - 30, PAL['MAGENTA'], PAL['PURPLE'], 4)
    draw_text_shadow_c(tc, "I GOT THE UNIVERSE", GH // 2 + 12, PAL['LTCYAN'],  PAL['BLUE'],   2)

    if int(ft * 3) % 2 == 0:
        draw_rect(tc, GW // 2 - 2, GH // 2 + 32, 4, 7, PAL['WHITE'])

    scanlines(tc)
    return tc

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    # Determine output path (same folder as this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path   = os.path.join(script_dir, OUT_FILE)

    print("=" * 60)
    print("  verse3/line01 — 3D Universe  |  Pixel Art Retro")
    print("=" * 60)
    print(f"  Virtual canvas : {GW} × {GH}")
    print(f"  Output         : {W} × {H}  ({PX}× upscale)")
    print(f"  Frame rate     : {FPS} fps")
    print(f"  Duration       : {DUR:.1f}s  +  1.5s title card")
    print(f"  Output file    : {out_path}")
    print()

    # Pre-build scene objects (do this once, not per-frame)
    warp   = WarpTunnel(seed=7)
    galaxy = Galaxy(seed=42)
    nebula = Nebula(seed=99)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_path, fourcc, FPS, (W, H))

    if not writer.isOpened():
        print("ERROR: Could not open VideoWriter.")
        print("  Make sure opencv-python is installed:  pip install opencv-python")
        return

    # Title card (1.5 s)
    title_frames = int(1.5 * FPS)
    print(f"  Rendering title card ({title_frames} frames)...")
    for f in range(title_frames):
        writer.write(upscale(title_frame(f / FPS, warp)))

    # Main animation
    total = int(DUR * FPS)
    print(f"  Rendering main animation ({total} frames)...")
    for f in range(total):
        t     = f / FPS
        frame = render_frame(t, warp, galaxy, nebula)
        writer.write(upscale(frame))
        if f % FPS == 0:
            pct = int(100 * f / total)
            bar = "#" * (pct // 5) + "-" * (20 - pct // 5)
            print(f"  [{bar}] {pct:3d}%", end="\r", flush=True)

    writer.release()
    print(f"\n  Done!  →  {out_path}")
    print()
    print("  Tip: if the mp4 looks washed-out in Windows Media Player,")
    print("  try VLC or rename to .avi (change fourcc to 'XVID').")


if __name__ == "__main__":
    main()