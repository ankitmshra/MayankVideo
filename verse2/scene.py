"""
verse2/scene.py — UNIFIED VERSE 2 SCENE  (v4)
==============================================
RENDERING APPROACH:
  • Custom 5-row block font — each letter is 5 rows of block chars.
    No pyfiglet. Full control. Always readable.
  • 2 words shown at a time, dead-centred on screen.
  • Fill character shifts with emotional tone:
      cyan   → ▓  (solid, hopeful)
      grey   → ░  (faded, frustrated)
      white  → █  (dense, suppressed anger)
      orange → ▒  (burning, restless)
      red    → █  (rage, bold)
      green  → ▓  (free, released)
  • New chunk SLAMS in: grows from a thin ▄ bar → full 5 rows over 0.15s
  • Old chunk DISSOLVES: shrinks back to ▄ bar → gone over 0.15s
  • Ghost echo: previous chunk's text lingers as dim ░ behind current
  • Background: matrix rain columns + drifting noise bands + ember sparks
  • Character: silhouette walker at bottom, emotional arc L→R
"""

import math
import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C, LineAnimator, term_size, clear, flush

# ═══════════════════════════════════════════════════════════════════════════════
# 5-ROW BLOCK FONT
# Each glyph: list of 5 strings, each exactly 5 chars wide (pad with spaces).
# The fill character '▓' is replaced at draw time with the emotional fill char.
# ═══════════════════════════════════════════════════════════════════════════════
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
    '0': [' ▓▓▓ ','▓  ▓▓','▓ ▓ ▓','▓▓  ▓',' ▓▓▓ '],
    '1': ['  ▓  ',' ▓▓  ','  ▓  ','  ▓  ','▓▓▓▓▓'],
    '2': [' ▓▓▓ ','▓   ▓','  ▓▓ ',' ▓   ','▓▓▓▓▓'],
    '3': ['▓▓▓▓ ','    ▓','  ▓▓ ','    ▓','▓▓▓▓ '],
    '4': ['▓   ▓','▓   ▓','▓▓▓▓▓','    ▓','    ▓'],
    '5': ['▓▓▓▓▓','▓    ','▓▓▓▓ ','    ▓','▓▓▓▓ '],
    '6': [' ▓▓▓▓','▓    ','▓▓▓▓ ','▓   ▓',' ▓▓▓ '],
    '7': ['▓▓▓▓▓','    ▓','   ▓ ','  ▓  ','  ▓  '],
    '8': [' ▓▓▓ ','▓   ▓',' ▓▓▓ ','▓   ▓',' ▓▓▓ '],
    '9': [' ▓▓▓ ','▓   ▓',' ▓▓▓▓','    ▓',' ▓▓▓ '],
    ' ': ['   ','   ','   ','   ','   '],
    "'": ['▓▓ ','▓  ','   ','   ','   '],
    ',': ['   ','   ','   ',' ▓▓',' ▓ '],
    '.': ['   ','   ','   ','   ','  ▓'],
    '!': [' ▓ ',' ▓ ',' ▓ ','   ',' ▓ '],
    '-': ['   ','   ','▓▓▓','   ','   '],
    '/': ['    ▓','   ▓ ','  ▓  ',' ▓   ','▓    '],
    '?': [' ▓▓▓ ','▓   ▓','  ▓▓ ','     ','  ▓  '],
}

GLYPH_W   = 5   # every glyph is padded to this width
GLYPH_GAP = 1   # 1 space between glyphs
GLYPH_H   = 5   # rows per glyph

# Emotional fill chars mapped by C.* color constant prefix
_FILL_FOR = {
    C.CYAN:    '▓',
    C.GREY:    '░',
    C.WHITE:   '█',
    C.ORANGE:  '▒',
    C.RED:     '█',
    C.GREEN:   '▓',
}

def _fill_char(color: str) -> str:
    for k, v in _FILL_FOR.items():
        if k in color:
            return v
    return '▓'


# Every block is padded to this fixed width so left_x = (100-88)//2 = 6
# always — regardless of chunk length. No horizontal jitter ever.
FIXED_BLOCK_W = 88

def render_block(text: str, fill: str = '▓') -> list[str]:
    """
    Render text as 5 rows of block characters.
    ALL rows are padded to exactly FIXED_BLOCK_W so the block anchor
    (left_x) is identical for every chunk — eliminating horizontal jitter.
    Characters that would exceed FIXED_BLOCK_W are hard-clipped.
    """
    rows = ['', '', '', '', '']
    for ch in text.upper():
        g = _G.get(ch, _G[' '])
        for r in range(GLYPH_H):
            rows[r] += g[r].replace('▓', fill) + ' ' * GLYPH_GAP
    # Hard-clip at FIXED_BLOCK_W, then pad to exactly FIXED_BLOCK_W
    rows = [r[:FIXED_BLOCK_W].ljust(FIXED_BLOCK_W) for r in rows]
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# VERSE TIMELINE — 2-word chunks
# ═══════════════════════════════════════════════════════════════════════════════
_RAW = [
    (0.0,   'My bandmate',          C.CYAN),
    (0.6,   'now flatmate',         C.CYAN),
    (2.0,   'I thought',            C.CYAN),
    (2.6,   'we will',              C.CYAN),
    (3.1,   'work hard',            C.CYAN),
    (3.7,   'on our tracks',        C.CYAN),
    (4.6,   'Yet all he did',              C.CYAN),
    (5.6,   'was sleep',            C.CYAN),
    (6.1,   'and waste',            C.CYAN),
    (6.6,   'time and',             C.CYAN),
    (7.1,   'talk cap',             C.CYAN),
    (7.6,   'I held back',          C.WHITE),
    (8.3,   'my anger',             C.WHITE),
    (8.9,   'tried to',             C.WHITE),
    (9.4,   'understand him',       C.WHITE),
    (10.4,  'I gave him',           C.WHITE),
    (11.1,  'all the chances',      C.WHITE),
    (11.9,  'and dealt it',         C.WHITE),
    (12.6,  'with patience',        C.WHITE),
    (13.4,  'I bite',               C.ORANGE),
    (13.9,  'my own words',         C.ORANGE),
    (14.6,  'from the second',      C.ORANGE),
    (15.3,  'verse of',             C.ORANGE),
    (15.8,  'the first',            C.ORANGE),
    (16.4,  'Track I know',         C.ORANGE),
    (17.1,  "its my bad",           C.ORANGE),
    (17.7,  'to think',             C.ORANGE),
    (18.2,  "that well",            C.ORANGE),
    (18.7,  'make it',              C.ORANGE),
    (19.4,  'now',                  C.RED),
    (19.8,  'FUCK THAT',            C.RED),
    (21.0,  'Deep down',            C.RED),
    (21.6,  'I knew',               C.RED),
    (22.1,  'that you',             C.RED),
    (22.6,  'will leave',           C.RED),
    (23.1,  'you will quit',        C.RED),
    (24.0,  'a weak mind',          C.RED),
    (24.7,  'you lack will',        C.RED),
    (26.2,  'I cut ties',           C.GREEN),
    (26.8,  'I moved on',           C.GREEN),
    (27.4,  "didnt look back",      C.GREEN),
    (28.8,  'I felt bad',           C.GREEN),
    (29.4,  'I felt good',          C.GREEN),
    (30.0,  'I felt free',          C.GREEN),
    (30.6,  'at last',              C.GREEN),
]

CHUNKS = _RAW
TOTAL_DURATION = 32.0


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND CONFIGS (stable random, generated once)
# ═══════════════════════════════════════════════════════════════════════════════
_rs = random.Random(77)
_RAIN_TRACKS = [
    (_rs.random(), _rs.uniform(3, 11), _rs.randint(0, 99), _rs.uniform(0, 12))
    for _ in range(50)
]
_RAIN_CHARS = list('ｦｧｨｩｪｫｬｭｮｯｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿタチツテトナニヌネノハヒフヘホ'
                   '0123456789ABCDEFabcdef░▒▓│╎╏┊╭╮╯╰')

_bs = random.Random(13)
_BANDS = [
    (_bs.uniform(0,1), _bs.uniform(-0.3,0.3), _bs.uniform(0.04,0.15), _bs.randint(1,3))
    for _ in range(7)
]
_BAND_CHARS = list('·:;|/\\+=~^°•‧')

# Walk frames
_WALK = [
    ['  o  ',' /|\\ ',' / \\ '],
    ['  o  ',' /|  ',' /|  '],
    ['  o  ','  |  ',' /|\\ '],
    ['  o  ','  |\\ ','  |\\ '],
    ['  o  ',' /|  ','  |\\ '],
]
_SLUMP = [['  o  ','/|   ','|    ']]
_CHEER = [
    ['\\o/ ','  |  ',' / \\ '],
    [' o  ','\\|  ',' | \\ '],
]


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE
# ═══════════════════════════════════════════════════════════════════════════════
class Verse2Scene(LineAnimator):
    FPS = 60

    def play(self, text: str, color: str, duration: float):
        dt = 1.0 / self.FPS
        elapsed = 0.0
        while elapsed < TOTAL_DURATION:
            t0 = time.time()
            tw, th = term_size()
            clear()
            sys.stdout.write(self.frame(text, color, elapsed, tw, th))
            flush()
            took = time.time() - t0
            time.sleep(max(0, dt - took))
            elapsed += dt

    def frame(self, _t: str, _c: str, t: float, tw: int, th: int) -> str:
        # ── Fixed viewport — never reflows, never word-wraps ─────────────────
        # Canvas is always exactly W×H cells. _canvas_str pads every row to
        # exactly W chars so the terminal sees a uniform grid and never wraps.
        W = 100
        H = 28
        canvas = [[(' ', '')] * W for _ in range(H)]

        def px(y, x, ch, col=''):
            if 0 <= y < H and 0 <= x < W:
                canvas[y][x] = (ch, col)

        # ── 1. MATRIX RAIN ──────────────────────────────────────────────────
        for xf, spd, cseed, phase in _RAIN_TRACKS:
            cx = int(xf * W)
            hy = int((phase + t * spd) % H)
            for d in range(14):
                ry = (hy - d) % H
                ci = (cseed + d + int(t * 5)) % len(_RAIN_CHARS)
                if d == 0:
                    col = C.WHITE
                elif d < 3:
                    col = C.DIM + C.GREEN
                elif d < 8:
                    col = C.DIM + C.GREY
                else:
                    col = C.DIM + '\033[38;5;235m'
                px(ry, cx, _RAIN_CHARS[ci], col)

        # ── 2. NOISE BANDS ──────────────────────────────────────────────────
        _br = random.Random(int(t * 7) % 8888)
        for yf, drift, dens, thick in _BANDS:
            by = int(((yf + drift * t) % 1.0) * H)
            for dy in range(thick):
                ry = (by + dy) % H
                for x in range(W):
                    if _br.random() < dens:
                        px(ry, x, _br.choice(_BAND_CHARS),
                           C.DIM + '\033[38;5;239m')

        # ── 3. EMBER SPARKS ─────────────────────────────────────────────────
        _er = random.Random(int(t * 11) % 5555)
        for _ in range(18):
            ex = _er.randint(0, W-1)
            ey = int((_er.random() * H - t * 2.5 * _er.uniform(0.3, 1)) % H)
            ec = _er.choice(['·','✦','✧','*','+','×','◦','°','˙'])
            ei = _er.choice([208, 214, 220, 226, 196, 202])
            px(ey, ex, ec, C.DIM + f'\033[38;5;{ei}m')

        # ── 4. WALKING FIGURE ───────────────────────────────────────────────
        period = 9.0
        wt  = t % period
        fx  = int((wt / period) * (W + 16)) - 8
        fy  = H - 4
        if 7.6 <= t <= 19.4:
            frames = _SLUMP if int(t * 2) % 4 == 0 else _WALK[:2]
            fc = C.DIM + C.RED
        elif t > 26.0:
            frames = _CHEER if int(t * 3) % 6 < 2 else _WALK
            fc = C.GREEN + C.BOLD
        else:
            frames = _WALK
            fc = C.WHITE
        wf = frames[int(t * 8) % len(frames)]
        for wy, wl in enumerate(wf):
            for wx, wc in enumerate(wl):
                if wc != ' ':
                    px(fy + wy, fx + wx, wc, fc)
        for s in range(1, 10):
            tx = fx - s * 2
            px(fy + 2, tx, '·' if s < 5 else '.', C.DIM + C.GREY)


        # ── 5. LYRIC RENDERING ─────────────────────────────────────────────
        # One chunk at a time, dead-centred in the fixed 100x28 viewport.
        # No scale animation — just a clean colour fade-in / fade-out.
        # Previous chunk ghosts behind current during 0.15s crossfade.

        fired = [i for i, (s, _, __) in enumerate(CHUNKS) if t >= s]
        if not fired:
            return _canvas_str(canvas, W)

        ci           = fired[-1]
        cs, ctxt, ccol = CHUNKS[ci]
        cfill        = _fill_char(ccol)
        age          = t - cs

        # Slot duration until next chunk
        ns    = CHUNKS[ci + 1][0] if ci + 1 < len(CHUNKS) else TOTAL_DURATION
        slot  = ns - cs
        FADE  = 0.12   # fade-in / fade-out window

        # Alpha for current chunk
        fade_out_start = slot - FADE
        if age < FADE:
            cur_alpha = age / FADE
        elif age < fade_out_start:
            cur_alpha = 1.0
        else:
            cur_alpha = max(0.0, 1.0 - (age - fade_out_start) / FADE)

        # Ghost of previous chunk during fade-in of current
        if ci > 0 and age < FADE:
            _, ptxt, pcol = CHUNKS[ci - 1]
            pfill        = _fill_char(pcol)
            ghost_alpha  = 1.0 - age / FADE
            prev_rows    = render_block(ptxt, pfill)
            _draw_centred(canvas, prev_rows, H, W, pcol, ghost_alpha, ghost=True)

        cur_rows = render_block(ctxt, cfill)
        _draw_centred(canvas, cur_rows, H, W, ccol, cur_alpha, ghost=False)

        return _canvas_str(canvas, W)


# ═══════════════════════════════════════════════════════════════════════════════
# DRAW HELPER — always draws all 5 rows consecutively, no gaps
# ═══════════════════════════════════════════════════════════════════════════════
def _draw_centred(canvas, rows, H, W, color, alpha, ghost=False):
    """
    Centre rows on the fixed canvas. Always 5 consecutive rows.
    Wipes backdrop first so nothing bleeds through.
    Alpha controls brightness: 1.0=bold, >0.5=normal, <=0.5=dim.
    """
    if not rows or alpha <= 0:
        return

    block_h = len(rows)
    block_w = max(len(r) for r in rows)

    # Strictly centre — if block wider than canvas, left-clip
    top_y  = max(0, (H - block_h) // 2)
    left_x = max(0, (W - block_w) // 2)

    # Colour choice
    if ghost:
        draw_col = C.DIM + '\033[38;5;238m'
    elif alpha > 0.85:
        draw_col = color + C.BOLD
    elif alpha > 0.4:
        draw_col = color
    else:
        draw_col = C.DIM + color

    # Wipe backdrop — solid blank rectangle, no background bleed
    for by in range(top_y, min(H, top_y + block_h)):
        for bx in range(left_x, min(W, left_x + block_w)):
            canvas[by][bx] = (' ', '')

    # Draw every row in order — row 0 at top_y, row 4 at top_y+4
    for ri, row in enumerate(rows):
        gy = top_y + ri
        if gy >= H:
            break
        # Only draw up to W columns — hard clip, no wrap
        for xi in range(min(len(row), W - left_x)):
            ch = row[xi]
            if ch != ' ':
                canvas[gy][left_x + xi] = (ch, draw_col)


def _canvas_str(canvas, W) -> str:
    """
    Render canvas to string. Every row is exactly W visible chars —
    padded with spaces so the terminal never sees a short line and
    decides to reflow or insert extra newlines.
    """
    lines = []
    for row in canvas:
        s = ''
        for ch, col in row:
            if ch != ' ':
                s += (col + ch + C.RESET) if col else ch
            else:
                s += ' '
        # Ensure row is exactly W visible chars (ANSI codes don't count)
        # The row was built from exactly W cells so this is guaranteed,
        # but we pad just in case any cell was skipped.
        lines.append(s)
    return '\n'.join(lines)