"""
Line01 — "I got the universe in my hand i can do anything"
Duration: 3.0s

LYRICS TIMELINE (2–3 word chunks, natural speech rhythm):
  0.00 → "I GOT THE"
  0.55 → "UNIVERSE"
  1.10 → "IN MY HAND"
  1.80 → "I CAN DO"
  2.35 → "ANYTHING"

BACKGROUND ANIMATION (runs continuously underneath):
  Big Bang expansion — warp star streams from centre,
  three shockwave rings, nebula wash, rotating corona.
  Animation phases do NOT gate the text — text is always present.

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
W  = 160
H  = 45
CX = W // 2       # 80
CY = H // 2 - 4   # 18  — upper half, text zone is lower half

# ══════════════════════════════════════════════════════════════
# LYRIC CHUNKS  (t_start, text, fill_char)
# fill_char drives the block-font density
# ══════════════════════════════════════════════════════════════
CHUNKS = [
    (0.00, "I GOT THE",   '░'),
    (0.55, "UNIVERSE",    '▓'),
    (1.10, "IN MY HAND",  '▒'),
    (1.80, "I CAN DO",    '░'),
    (2.35, "ANYTHING",    '▓'),
]
TOTAL_DURATION = 3.0

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
    '!': [' ▓   ',' ▓   ',' ▓   ','     ',' ▓   '],
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

# ══════════════════════════════════════════════════════════════
# STATIC BACKGROUND ASSETS  (seeded — stable every frame)
# ══════════════════════════════════════════════════════════════
_nb = random.Random(7777)
BG_STARS = [
    {'x': _nb.randint(0,W-1), 'y': _nb.randint(0,H-1),
     'ch': _nb.choice(['·','·','∙','˙']),
     'ci': _nb.choice([236,238,239,54,57,17,18])}
    for _ in range(300)
]
_nc = random.Random(1234)
NEBULA = [
    {'x': _nc.randint(0,W-1), 'y': _nc.randint(0,H-1),
     'ch': _nc.choice(['░','▒','·','∙']),
     'ci': _nc.choice([54,57,93,91,53,19,55,18,236,238])}
    for _ in range(150)
]

_ep = random.Random(42)
PARTICLES = [
    {'ang':   _ep.uniform(0, math.tau),
     'spd':   _ep.uniform(8, 28),
     'delay': _ep.uniform(0, 0.25),
     'ch':    _ep.choice(['✦','★','·','∙','*','°','◆','▪','•','∗']),
     'trail': _ep.choice(['·','∙','.',]),
     'fast':  False}
    for _ in range(200)
]
for p in PARTICLES:
    p['fast'] = p['spd'] > 18

_cr = random.Random(999)
CORONA = [
    {'a0':  _cr.uniform(0, math.tau),
     'spd': _cr.uniform(0.6, 1.4),
     'r':   _cr.uniform(3.5, 6.0),
     'ch':  _cr.choice(['✦','★','◆','◈','●','○','◎'])}
    for _ in range(24)
]

SHOCKWAVES = [
    {'t_start': 0.0,  'speed': 22, 'col': C.BOLD + C.YELLOW},
    {'t_start': 0.08, 'speed': 16, 'col': C.CYAN},
    {'t_start': 0.16, 'speed': 11, 'col': C.MAGENTA},
]

_PCOLS_NEAR = [C.BOLD + C.YELLOW, C.BOLD + C.WHITE, C.BOLD + C.GOLD]
_PCOLS_MID  = [C.CYAN, C.MAGENTA, C.BOLD + C.BLUE, C.ORANGE]
_PCOLS_FAR  = [C.DIM + C.BLUE, C.DIM + C.MAGENTA, C.DIM + '\033[38;5;57m']

# ══════════════════════════════════════════════════════════════
# CANVAS HELPERS
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

def _draw_ring(cv, r, col):
    if r <= 0: return
    steps = max(60, int(r * 6))
    for i in range(steps):
        ang = (i / steps) * math.tau
        x = int(CX + math.cos(ang) * r)
        y = int(CY + math.sin(ang) * r / 2.2)
        _px(cv, y, x, '·', col)

def _draw_block_centred(cv, text, fill, color, top_y, alpha):
    """Render block-font text centred horizontally at top_y. alpha controls brightness."""
    if alpha <= 0:
        return
    rows5 = _render_block(text, fill)
    block_w = max(len(r) for r in rows5)
    left_x  = (W - block_w) // 2

    if alpha > 0.85:
        col = C.BOLD + color
    elif alpha > 0.4:
        col = color
    else:
        col = C.DIM + color

    for ri, row_str in enumerate(rows5):
        gy = top_y + ri
        if gy >= H: break
        # wipe backdrop first
        for xi in range(min(len(row_str), W - left_x)):
            cv[gy][left_x + xi] = (' ', '')
        for xi, gc in enumerate(row_str):
            if gc != ' ' and left_x + xi < W:
                _px(cv, gy, left_x + xi, gc, col)

# ══════════════════════════════════════════════════════════════
# MAIN ANIMATOR
# ══════════════════════════════════════════════════════════════
class Line01(LineAnimator):
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

        EXPLODE_T = 0.0    # bang starts immediately
        SETTLE_T  = 1.2    # particles slow down

        # ── 1. NEBULA BACKGROUND ─────────────────────────────────────────────
        for s in BG_STARS:
            _px(cv, s['y'], s['x'], s['ch'], C.DIM + f"\033[38;5;{s['ci']}m")
        for p in NEBULA:
            _px(cv, p['y'], p['x'], p['ch'], C.DIM + f"\033[38;5;{p['ci']}m")

        # ── 2. SHOCKWAVE RINGS ────────────────────────────────────────────────
        for sw in SHOCKWAVES:
            if t >= sw['t_start']:
                age = t - sw['t_start']
                r   = age * sw['speed']
                fade_t = age / 1.2
                if fade_t < 1.0:
                    ring_col = sw['col'] if fade_t < 0.4 else C.DIM + sw['col']
                    _draw_ring(cv, r, ring_col)

        # ── 3. EXPLOSION PARTICLES ────────────────────────────────────────────
        for p in PARTICLES:
            pt = t - EXPLODE_T - p['delay']
            if pt <= 0:
                continue
            dist  = pt * p['spd']
            px_x  = int(CX + math.cos(p['ang']) * dist)
            px_y  = int(CY + math.sin(p['ang']) * dist / 2.2)

            if t < SETTLE_T:
                if dist < 15:
                    col = _PCOLS_NEAR[int(dist) % len(_PCOLS_NEAR)]
                elif dist < 35:
                    col = _PCOLS_MID[int(dist) % len(_PCOLS_MID)]
                else:
                    col = _PCOLS_FAR[int(dist) % len(_PCOLS_FAR)]
                _px(cv, px_y, px_x, p['ch'], col)
                for step in range(1, 4):
                    td  = max(0, dist - step * (p['spd'] * 0.05 + 1.5))
                    tx  = int(CX + math.cos(p['ang']) * td)
                    ty  = int(CY + math.sin(p['ang']) * td / 2.2)
                    tc  = C.DIM + '\033[38;5;238m' if step > 1 else col
                    _px(cv, ty, tx, p['trail'], tc)
            else:
                _px(cv, px_y, px_x, '·', C.DIM + '\033[38;5;240m')

        # ── 4. GALACTIC CENTRE ────────────────────────────────────────────────
        pulse = (math.sin(t * 8) + 1) / 2
        core_ch  = '◎' if pulse > 0.6 else ('○' if pulse > 0.3 else '·')
        core_col = C.BOLD + C.YELLOW
        _px(cv, CY, CX, core_ch, core_col)

        for dy, dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            ch  = '▒' if t > 0.3 else '·'
            gc  = C.YELLOW if abs(dy)+abs(dx)==1 else C.DIM+C.YELLOW
            _px(cv, CY+dy, CX+dx, ch, gc)

        # Corona (appears from t=0, grows in)
        corona_alpha = min(1.0, t / 0.8)
        for s in CORONA:
            a   = s['a0'] + t * s['spd']
            cx_ = int(CX + math.cos(a) * s['r'])
            cy_ = int(CY + math.sin(a) * s['r'] / 2.2)
            depth = math.sin(a)
            col   = (C.BOLD + C.YELLOW if depth > 0.3
                     else C.CYAN if depth > -0.3
                     else C.DIM + C.BLUE)
            if corona_alpha < 0.5:
                col = C.DIM + col
            _px(cv, cy_, cx_, s['ch'], col)

        # ── 5. LYRIC CHUNKS — always on, timed to speech ─────────────────────
        # Text zone: rows 28–34 (lower third, clear of the explosion centre)
        TEXT_Y = H - 14    # top of the 5-row block text

        FADE = 0.10

        fired = [i for i, (ts, _, __) in enumerate(CHUNKS) if t >= ts]
        if fired:
            ci = fired[-1]
            ts, ctxt, cfill = CHUNKS[ci]
            age = t - ts

            # Next chunk start (for fade-out)
            next_ts = CHUNKS[ci + 1][0] if ci + 1 < len(CHUNKS) else TOTAL_DURATION
            slot = next_ts - ts
            fade_out_start = slot - FADE

            if age < FADE:
                alpha = age / FADE
            elif age < fade_out_start:
                alpha = 1.0
            else:
                alpha = max(0.0, 1.0 - (age - fade_out_start) / FADE)

            # Ghost of previous chunk during crossfade
            if ci > 0 and age < FADE:
                _, ptxt, pfill = CHUNKS[ci - 1]
                ghost_alpha = 1.0 - age / FADE
                _draw_block_centred(cv, ptxt, pfill, C.DIM + color, TEXT_Y, ghost_alpha * 0.4)

            _draw_block_centred(cv, ctxt, cfill, color, TEXT_Y, alpha)

        # ── Centre W×H in actual terminal ─────────────────────────────────────
        h_pad    = max(0, (tw - W) // 2)
        v_pad    = max(0, (th - H) // 2)
        pad      = ' ' * h_pad
        rows_out = _render(cv).split('\n')
        out      = [''] * v_pad
        out     += [pad + r for r in rows_out]
        out     += [''] * v_pad
        return '\n'.join(out)