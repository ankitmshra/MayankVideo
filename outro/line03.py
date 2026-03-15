"""
Line03 — "We look up in the sky"
Effect: LOOKING UP — perspective zoom into an infinite starfield above
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(3)
SKY_STARS = [
    {"x": _rng.uniform(-1, 1), "y": _rng.uniform(-1, 1),
     "z": _rng.uniform(0.1, 1.0), "ch": _rng.choice(["·", "∘", "✦", "*"])}
    for _ in range(60)
]


class Line03(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Warp-speed stars zooming toward viewer
        cx = tw // 2
        cy = rmid
        for s in SKY_STARS:
            z     = (s["z"] - t * 0.4) % 1.0 + 0.01
            scale = 1.0 / z
            sx    = int(cx + s["x"] * scale * tw * 0.5)
            sy    = int(cy + s["y"] * scale * rows * 0.5)
            size  = min(3, int(1 / z))
            if 0 <= sx < tw and 0 <= sy < rows:
                ch  = "●" if size >= 3 else ("○" if size == 2 else s["ch"])
                col = C.WHITE if z < 0.2 else (C.CYAN if z < 0.5 else C.DIM + C.BLUE)
                grid[sy][sx]  = ch
                cgrid[sy][sx] = col

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid + 3][gx]  = ch
                cgrid[rmid + 3][gx] = color

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
