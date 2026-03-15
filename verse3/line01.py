"""
Line01 — "I got the universe in my hand i can do anything"
Effect: GALAXY SPIN — stars orbit a central point, text floats in the cosmos
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(11)
STARS_V3 = [
    {"angle": _rng.uniform(0, math.pi * 2),
     "radius": _rng.uniform(0.1, 0.9),
     "speed":  _rng.uniform(0.2, 0.8),
     "ch":     _rng.choice(["·", "∘", "✦", "*", "°"])}
    for _ in range(40)
]


class Line01(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        for s in STARS_V3:
            angle = s["angle"] + t * s["speed"]
            rx    = int(cx + math.cos(angle) * s["radius"] * tw * 0.45)
            ry    = int(rmid + math.sin(angle) * s["radius"] * rows * 0.42)
            if 0 <= rx < tw and 0 <= ry < rows:
                grid[ry][rx]  = s["ch"]
                cgrid[ry][rx] = C.DIM + C.BLUE if s["radius"] > 0.6 else C.MAGENTA

        # Central glow
        grid[rmid][cx]  = "◎"
        cgrid[rmid][cx] = C.YELLOW + C.BOLD

        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = color

        top = center_v(rows + 4, th)
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        for ri, row in enumerate(grid):
            line_str = ""
            for ci, ch in enumerate(row):
                col = cgrid[ri][ci] or ""
                line_str += (col + ch + C.RESET) if ch != " " else " "
            out.append(line_str)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        return "\n".join(out)
