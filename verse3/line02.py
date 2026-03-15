"""
Line02 — "Once flew close to the sun got my wings burnt"
Duration: 2.8s

LYRICS TIMELINE (2–3 word chunks, natural speech rhythm):
  0.00 → "ONCE FLEW"
  0.50 → "CLOSE TO"
  0.95 → "THE SUN"
  1.40 → "GOT MY"
  1.80 → "WINGS BURNT"

BACKGROUND ANIMATION (runs continuously underneath):
  Detailed ASCII angel with large feathered wings rises toward
  a blazing sun. Wings catch fire from tips inward over the
  duration. The lyric text is always present — animation is backdrop.

Viewport: W=160, H=45  (16:9)
FPS: 60
"""

import math
import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C, LineAnimator, term_size, clear, flush

# ══════════════════════════════════════════════════════════════
# VIEWPORT
# ══════════════════════════════════════════════════════════════
W = 160
H = 45

# ══════════════════════════════════════════════════════════════
# LYRIC CHUNKS  (t_start, text, fill_char)
# ══════════════════════════════════════════════════════════════
CHUNKS = [
    (0.00, "ONCE FLEW",     '░'),
    (0.50, "CLOSE TO",      '▒'),
    (0.95, "THE SUN",       '▓'),
    (1.40, "GOT MY",        '▒'),
    (1.80, "WINGS BURNT",   '░'),
]
TOTAL_DURATION = 2.8

# ══════════════════════════════════════════════════════════════
# BLOCK FONT
# ══════════════════════════════════════════════════════════════
_G = {
    'A': [' ▓▓▓ ','▓   ▓','▓▓▓▓▓','▓   ▓','▓   ▓'],
    'B': ['▓▓▓▓ ','▓   ▓','▓▓▓▓ ','▓   ▓','▓▓▓▓ '],
    'C': [' ▓▓▓▓','▓    ','▓    ','▓    ',' ▓▓▓▓'],
    'D': ['▓▓▓▓ ','▓   ▓','▓   ▓','▓   ▓','▓▓▓▓ '],
    'E': ['▓▓▓▓▓','▓    ','▓▓▓▓ ','▓    ','▓▓▓▓▓'],
    'F': ['▓▓▓▓▓','▓    ','▓▓▓▓ ','▓    ','▓    '],
    'G': [' ▓▓▓▓','▓    ','▓  ▓▓','▓   ▓',' ▓▓▓▓'],
    'H': ['▓   ▓','▓   ▓','▓▓▓▓▓','▓   ▓','▓   ▓'],
    'I': ['▓▓▓▓▓','  ▓  ','  ▓  ','  ▓  ','▓▓▓▓▓'],
    'J': ['  ▓▓▓','    ▓','    ▓','▓   ▓',' ▓▓▓ '],
    'K': ['▓   ▓','▓  ▓ ','▓▓▓  ','▓  ▓ ','▓   ▓'],
    'L': ['▓    ','▓    ','▓    ','▓    ','▓▓▓▓▓'],
    'M': ['▓   ▓','▓▓ ▓▓','▓ ▓ ▓','▓   ▓','▓   ▓'],
    'N': ['▓   ▓','▓▓  ▓','▓ ▓ ▓','▓  ▓▓','▓   ▓'],
    'O': [' ▓▓▓ ','▓   ▓','▓   ▓','▓   ▓',' ▓▓▓ '],
    'P': ['▓▓▓▓ ','▓   ▓','▓▓▓▓ ','▓    ','▓    '],
    'Q': [' ▓▓▓ ','▓   ▓','▓ ▓ ▓','▓  ▓▓',' ▓▓▓▓'],
    'R': ['▓▓▓▓ ','▓   ▓','▓▓▓▓ ','▓  ▓ ','▓   ▓'],
    'S': [' ▓▓▓▓','▓    ',' ▓▓▓ ','    ▓','▓▓▓▓ '],
    'T': ['▓▓▓▓▓','  ▓  ','  ▓  ','  ▓  ','  ▓  '],
    'U': ['▓   ▓','▓   ▓','▓   ▓','▓   ▓',' ▓▓▓ '],
    'V': ['▓   ▓','▓   ▓','▓   ▓',' ▓ ▓ ','  ▓  '],
    'W': ['▓   ▓','▓   ▓','▓ ▓ ▓','▓▓ ▓▓','▓   ▓'],
    'X': ['▓   ▓',' ▓ ▓ ','  ▓  ',' ▓ ▓ ','▓   ▓'],
    'Y': ['▓   ▓',' ▓ ▓ ','  ▓  ','  ▓  ','  ▓  '],
    'Z': ['▓▓▓▓▓','   ▓ ','  ▓  ',' ▓   ','▓▓▓▓▓'],
    ' ': ['     ','     ','     ','     ','     '],
    "'": ['▓▓   ','▓    ','     ','     ','     '],
    '.': ['     ','     ','     ','     ','  ▓  '],
}
GLYPH_H = 5; GLYPH_W = 5; GLYPH_GAP = 1

def _glyph(ch):
    return _G.get(ch.upper(), _G[' '])

def _render_block(text, fill='▓'):
    rows = [''] * 5
    for ch in text:
        g = _glyph(ch)
        for r in range(5):
            rows[r] += g[r].replace('▓', fill) + ' ' * GLYPH_GAP
    return rows

def _draw_block_centred(cv, text, fill, color, top_y, alpha):
    if alpha <= 0: return
    rows5   = _render_block(text, fill)
    block_w = max(len(r) for r in rows5)
    left_x  = (W - block_w) // 2
    col     = (C.BOLD + color if alpha > 0.85
               else color if alpha > 0.4
               else C.DIM + color)
    for ri, row_str in enumerate(rows5):
        gy = top_y + ri
        if gy >= H: break
        for xi in range(min(len(row_str), W - left_x)):
            cv[gy][left_x + xi] = (' ', '')
        for xi, gc in enumerate(row_str):
            if gc != ' ' and left_x + xi < W:
                _px(cv, gy, left_x + xi, gc, col)

# ══════════════════════════════════════════════════════════════
# CANVAS
# ══════════════════════════════════════════════════════════════
def _canvas():
    return [[(' ', '')] * W for _ in range(H)]

def _px(cv, y, x, ch, col=''):
    if 0 <= y < H and 0 <= x < W:
        cv[y][x] = (ch, col)

def _render(cv):
    lines = []
    for row in cv:
        s = ''
        for ch, col in row:
            s += (col + ch + C.RESET) if (ch != ' ' and col) else (ch if ch != ' ' else ' ')
        lines.append(s)
    return '\n'.join(lines)

# ══════════════════════════════════════════════════════════════
# BACKGROUND STARS & CLOUDS
# ══════════════════════════════════════════════════════════════
_bg = random.Random(555)
BG_STARS = [
    {'x': _bg.randint(0,W-1), 'y': _bg.randint(5,H-1),
     'ch': _bg.choice(['·','·','∙','˙']),
     'ci': _bg.choice([17,18,19,54,57,236,238])}
    for _ in range(180)
]
_cw = random.Random(222)
CLOUDS = [
    {'xf':   _cw.uniform(0, 1.0),
     'y':    _cw.randint(5, H - 16),
     'spd':  _cw.uniform(0.015, 0.05),
     'pat':  _cw.choice(['~≈~~≈~','≈~~≈≈~','~~≈≈~~','≈≈~~≈≈']),
     'col':  C.DIM + '\033[38;5;18m'}
    for _ in range(14)
]

# ══════════════════════════════════════════════════════════════
# SUN
# ══════════════════════════════════════════════════════════════
SUN_Y = 3
SUN_X = W // 2

def _draw_sun(cv, t, heat):
    disc_r = int(2 + heat * 5)
    for dy in range(-disc_r, disc_r + 1):
        for dx in range(-disc_r * 2, disc_r * 2 + 1):
            dist = math.sqrt((dx / 2) ** 2 + dy ** 2)
            if dist <= disc_r:
                ch  = ('█' if dist < disc_r * 0.5
                        else '▓' if dist < disc_r * 0.75
                        else '░')
                col = (C.BOLD + C.YELLOW if dist < disc_r * 0.5
                        else C.YELLOW if dist < disc_r * 0.75
                        else C.ORANGE)
                _px(cv, SUN_Y + dy, SUN_X + dx, ch, col)

    # Core
    core_ch = '◎' if int(t * 6) % 2 == 0 else '●'
    _px(cv, SUN_Y, SUN_X, core_ch, C.BOLD + C.YELLOW)

    # Corona rays — 16, animated
    n_rays   = 16
    ray_base = 5 + int(heat * 14)
    for ri in range(n_rays):
        ang     = (ri / n_rays) * math.tau + t * 0.5
        ray_len = ray_base + int(math.sin(t * 3 + ri * 0.7) * 3)
        for step in range(2, ray_len):
            rx   = int(SUN_X + math.cos(ang) * step * 2)
            ry   = int(SUN_Y + math.sin(ang) * step)
            fade = step / ray_len
            ch   = ('▒' if fade < 0.4 else '·')
            col  = (C.BOLD + C.YELLOW if fade < 0.4
                    else C.YELLOW if fade < 0.65
                    else C.DIM + C.ORANGE)
            _px(cv, ry, rx, ch, col)

    # Heat shimmer
    _hr = random.Random(int(t * 20) % 9999)
    for _ in range(int(4 + heat * 25)):
        sx = _hr.randint(SUN_X - 22, SUN_X + 22)
        sy = SUN_Y + _hr.randint(disc_r + 1, disc_r + 9)
        _px(cv, sy, sx, _hr.choice(['·','∙','°','˙']),
            C.DIM + '\033[38;5;220m')

# ══════════════════════════════════════════════════════════════
# ANGEL ART — two flap frames
# Wings are ~40 chars wide; centred on angel_cx
# Each entry: (row_index, art_string, zone_tag)
# ══════════════════════════════════════════════════════════════
ANGEL_A = [
    ( 0, r"             ◌◯◌              ",           'halo'  ),
    ( 1, r"              (·)              ",           'head'  ),
    ( 2, r"              \|/              ",           'neck'  ),
    ( 3, r"         ≋≋≋≋≋\|/≋≋≋≋≋        ",           'upper' ),
    ( 4, r"      ≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋     ",           'upper' ),
    ( 5, r"   ≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋  ",           'mid'   ),
    ( 6, r" ≋≋≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋≋≋",           'mid'   ),
    ( 7, r"≋≋≋≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋≋≋≋",           'lower' ),
    ( 8, r"≋≋≋≋≋≋≋≋≋≋≋≋≋  |  ≋≋≋≋≋≋≋≋≋≋≋≋≋",           'lower' ),
    ( 9, r" ≋≋≋≋≋≋≋≋≋≋≋   |   ≋≋≋≋≋≋≋≋≋≋≋ ",           'lower' ),
    (10, r"  ≋≋≋≋≋≋≋≋≋    |    ≋≋≋≋≋≋≋≋≋  ",           'tip'   ),
    (11, r"   ≋≋≋≋≋≋≋     |     ≋≋≋≋≋≋≋   ",           'tip'   ),
    (12, r"    ≋≋≋≋≋      |      ≋≋≋≋≋    ",           'tip'   ),
    (13, r"     ≋≋≋       |       ≋≋≋     ",           'tip'   ),
    (14, r"               |               ",           'body'  ),
    (15, r"              /|\              ",           'body'  ),
    (16, r"             / | \             ",           'body'  ),
    (17, r"           /~~~~~~~\           ",           'robe'  ),
    (18, r"          /~~~~~~~~~\          ",           'robe'  ),
    (19, r"         /~~~~~~~~~~~\         ",           'robe'  ),
    (20, r"          \_________/          ",           'robe'  ),
]

ANGEL_B = [
    ( 0, r"             ◌◯◌              ",           'halo'  ),
    ( 1, r"              (·)              ",           'head'  ),
    ( 2, r"              \|/              ",           'neck'  ),
    ( 3, r"      ≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋     ",           'upper' ),
    ( 4, r"   ≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋  ",           'upper' ),
    ( 5, r" ≋≋≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋≋≋",           'mid'   ),
    ( 6, r"≋≋≋≋≋≋≋≋≋≋≋≋≋≋\|/≋≋≋≋≋≋≋≋≋≋≋≋≋≋",           'mid'   ),
    ( 7, r"≋≋≋≋≋≋≋≋≋≋≋≋≋  |  ≋≋≋≋≋≋≋≋≋≋≋≋≋",           'lower' ),
    ( 8, r" ≋≋≋≋≋≋≋≋≋≋≋   |   ≋≋≋≋≋≋≋≋≋≋≋ ",           'lower' ),
    ( 9, r"  ≋≋≋≋≋≋≋≋≋    |    ≋≋≋≋≋≋≋≋≋  ",           'lower' ),
    (10, r"   ≋≋≋≋≋≋≋     |     ≋≋≋≋≋≋≋   ",           'tip'   ),
    (11, r"    ≋≋≋≋≋      |      ≋≋≋≋≋    ",           'tip'   ),
    (12, r"     ≋≋≋       |       ≋≋≋     ",           'tip'   ),
    (13, r"      ≋        |        ≋      ",           'tip'   ),
    (14, r"               |               ",           'body'  ),
    (15, r"              /|\              ",           'body'  ),
    (16, r"             / | \             ",           'body'  ),
    (17, r"           /~~~~~~~\           ",           'robe'  ),
    (18, r"          /~~~~~~~~~\          ",           'robe'  ),
    (19, r"         /~~~~~~~~~~~\         ",           'robe'  ),
    (20, r"          \_________/          ",           'robe'  ),
]

ANGEL_H  = 21
FIRE_CHARS = ['▓','▒','░','*','^','°','~']
FIRE_COLS  = [C.BOLD+C.YELLOW, C.BOLD+C.ORANGE, C.ORANGE, C.BOLD+C.RED, C.RED, C.DIM+C.RED]
ZONE_COL   = {
    'halo':  C.BOLD + C.YELLOW,
    'head':  C.BOLD + C.WHITE,
    'neck':  C.BOLD + C.WHITE,
    'upper': C.BOLD + C.WHITE,
    'mid':   C.WHITE,
    'lower': C.WHITE,
    'tip':   C.DIM + C.WHITE,
    'body':  C.BOLD + C.WHITE,
    'robe':  C.CYAN,
}
ZONE_BURN_T = {'tip': 0.0, 'lower': 0.2, 'mid': 0.45, 'upper': 0.65, 'body': 0.85}

def _draw_angel(cv, anchor_y, anchor_cx, t, burn):
    flap_t = (t % 0.9) / 0.9
    art    = ANGEL_B if flap_t > 0.5 else ANGEL_A
    _fr    = random.Random(int(t * 15) % 7777)

    for row_idx, row_str, zone in art:
        gy      = anchor_y + row_idx
        if not (0 <= gy < H): continue
        row_len = len(row_str)
        gx0     = anchor_cx - row_len // 2
        b_thresh = ZONE_BURN_T.get(zone, 1.1)
        zone_on  = burn >= b_thresh
        intensity = max(0.0, min(1.0, (burn - b_thresh) / 0.25)) if zone_on else 0.0

        for xi, ch in enumerate(row_str):
            if ch == ' ': continue
            gx = gx0 + xi
            if zone_on and ch in '≋~/\\|()·◌◯':
                if _fr.random() < intensity:
                    fch  = _fr.choice(FIRE_CHARS[:max(1, int(intensity * len(FIRE_CHARS)))])
                    fcol = FIRE_COLS[int(intensity * (len(FIRE_COLS) - 1))]
                    _px(cv, gy, gx, fch, fcol)
                else:
                    bcol = C.BOLD + C.ORANGE if intensity < 0.5 else C.ORANGE
                    _px(cv, gy, gx, ch, bcol)
            else:
                col = ZONE_COL.get(zone, C.WHITE)
                if burn > 0.75 and zone in ('body', 'robe'):
                    col = C.DIM + C.GREY
                _px(cv, gy, gx, ch, col)

    # Halo always pulses gold, overwrite
    halo_str = art[0][1]
    halo_row = anchor_y
    hp       = (math.sin(t * 4) + 1) / 2
    hcol     = C.BOLD + C.YELLOW if hp > 0.5 else C.YELLOW
    gx0_h    = anchor_cx - len(halo_str) // 2
    for xi, ch in enumerate(halo_str):
        if ch != ' ':
            _px(cv, halo_row, gx0_h + xi, ch, hcol)

# ══════════════════════════════════════════════════════════════
# EMBER PARTICLES
# ══════════════════════════════════════════════════════════════
_em = random.Random(888)
EMBERS = [
    {'x0f': _em.uniform(0.3, 0.7),
     'vy':  _em.uniform(3, 9),
     'vx':  _em.uniform(-4, 4),
     't0':  _em.uniform(1.4, 2.6),
     'ch':  _em.choice(['·','°','*','∙','˙'])}
    for _ in range(80)
]

# ══════════════════════════════════════════════════════════════
# MAIN ANIMATOR
# ══════════════════════════════════════════════════════════════
class Line02(LineAnimator):
    FPS = 60

    def play(self, text: str, color: str, duration: float):
        dt = 1.0 / self.FPS
        elapsed = 0.0
        while elapsed < duration:
            t0 = time.time()
            tw, th = term_size()
            clear()
            sys.stdout.write(self.frame(text, color, elapsed, tw, th))
            flush()
            took = time.time() - t0
            time.sleep(max(0, dt - took))
            elapsed += dt

    def frame(self, text: str, color: str, t: float, tw: int, th: int) -> str:
        cv = _canvas()

        heat = max(0.0, min(1.0, (t - 0.8) / 1.0))   # sun grows from t=0.8
        burn = max(0.0, min(1.0, (t - 1.4) / 1.0))   # wings burn from t=1.4

        # Angel position: rises from near-bottom to row 8 over first 1.4s
        angel_top = int((H - ANGEL_H - 2) * (1.0 - min(1.0, t / 1.4)) + 8 * min(1.0, t / 1.4))
        angel_cx  = W // 2

        # ── 1. BACKGROUND STARS ───────────────────────────────────────────────
        for s in BG_STARS:
            if heat < 0.8:
                _px(cv, s['y'], s['x'], s['ch'], C.DIM + f"\033[38;5;{s['ci']}m")

        # ── 2. CLOUD WISPS ────────────────────────────────────────────────────
        for cloud in CLOUDS:
            if heat < 0.9:
                cx_ = int(((cloud['xf'] + cloud['spd'] * t) % 1.0) * W)
                for qi, qc in enumerate(cloud['pat']):
                    _px(cv, cloud['y'], (cx_ + qi) % W, qc, cloud['col'])

        # ── 3. SUN ────────────────────────────────────────────────────────────
        _draw_sun(cv, t, heat)

        # ── 4. ANGEL ─────────────────────────────────────────────────────────
        _draw_angel(cv, angel_top, angel_cx, t, burn)

        # ── 5. EMBERS ────────────────────────────────────────────────────────
        for em in EMBERS:
            if t >= em['t0']:
                et = t - em['t0']
                ex = int(em['x0f'] * W + em['vx'] * et)
                ey = int(angel_top + 5 + em['vy'] * et)
                if int(t * 12 + em['t0'] * 7) % 3 != 0:
                    eci = random.Random(int(em['t0']*100)).choice([208,214,196,220])
                    _px(cv, ey, ex, em['ch'], C.DIM + f'\033[38;5;{eci}m')

        # ── 6. LYRIC CHUNKS — always on, timed to speech ─────────────────────
        # Text lives in the bottom strip: rows H-8 to H-3
        # Kept well below the angel so it never clashes
        TEXT_Y = H - 9
        FADE   = 0.10

        fired = [i for i, (ts, _, __) in enumerate(CHUNKS) if t >= ts]
        if fired:
            ci             = fired[-1]
            ts, ctxt, cfill = CHUNKS[ci]
            age            = t - ts
            next_ts        = CHUNKS[ci+1][0] if ci+1 < len(CHUNKS) else TOTAL_DURATION
            slot           = next_ts - ts
            fade_out_start = slot - FADE

            if age < FADE:
                alpha = age / FADE
            elif age < fade_out_start:
                alpha = 1.0
            else:
                alpha = max(0.0, 1.0 - (age - fade_out_start) / FADE)

            if ci > 0 and age < FADE:
                _, ptxt, pfill = CHUNKS[ci-1]
                _draw_block_centred(cv, ptxt, pfill, C.DIM + color, TEXT_Y, (1.0 - age/FADE) * 0.4)

            _draw_block_centred(cv, ctxt, cfill, color, TEXT_Y, alpha)

        # ── Centre in terminal ─────────────────────────────────────────────────
        h_pad    = max(0, (tw - W) // 2)
        v_pad    = max(0, (th - H) // 2)
        pad      = ' ' * h_pad
        rows_out = _render(cv).split('\n')
        out      = [''] * v_pad
        out     += [pad + r for r in rows_out]
        out     += [''] * v_pad
        return '\n'.join(out)