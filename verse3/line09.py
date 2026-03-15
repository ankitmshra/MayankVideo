"""
Line09 — "Art like Basquiat pieces"
Effect: PAINT SPLATTER — colored splatters appear around raw expressive text
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(55)
SPLAT_CHARS = ["*", "·", "°", "∘", "✦", "×", "+", "o", "O"]
COLORS = [C.RED, C.YELLOW, C.CYAN, C.MAGENTA, C.WHITE, C.ORANGE, C.GREEN]

SPLATTERS = [
    {
        "cx": _rng.uniform(0.05, 0.95),
        "cy": _rng.uniform(0.1, 0.9),
        "t0": _rng.uniform(0, 1.5),
        "col": _rng.choice(COLORS),
        "size": _rng.randint(2, 6),
    }
    for _ in range(20)
]


class Line09(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Paint splatters that appear over time
        for sp in SPLATTERS:
            if t < sp["t0"]:
                continue
            age  = t - sp["t0"]
            radius = min(sp["size"], int(age * 8))
            scx  = int(sp["cx"] * tw)
            scy  = int(sp["cy"] * rows)
            for _ in range(radius * 3):
                angle = _rng.uniform(0, math.pi * 2)
                dist  = _rng.uniform(0, radius)
                sx    = scx + int(math.cos(angle) * dist * 2)
                sy    = scy + int(math.sin(angle) * dist * 0.7)
                if 0 <= sx < tw and 0 <= sy < rows:
                    grid[sy][sx]  = _rng.choice(SPLAT_CHARS)
                    cgrid[sy][sx] = sp["col"]

        # Text — raw, bold, no clean framing
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = C.WHITE + C.BOLD

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
