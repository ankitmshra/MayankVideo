"""
Line08 — "now fuck that"
Effect: EXPLOSION — text slams in, shockwave radiates outward, debris flies
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(88)
DEBRIS = [
    {"angle": _rng.uniform(0, math.pi * 2),
     "speed": _rng.uniform(0.3, 1.0),
     "ch":    _rng.choice(list("*+×✕✗#@!"))}
    for _ in range(24)
]


class Line08(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text.upper())   # caps for impact
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Slam-in: text drops from top
        drop_prog = min(1.0, t / 0.3)
        drop_prog = 1 - (1 - drop_prog) ** 4
        ty = int((1 - drop_prog) * (-rows) + drop_prog * rmid)
        ty = max(0, min(rows - 1, ty))

        # Shockwave ring
        wave_r = t * 18
        for angle_step in range(80):
            angle = angle_step * math.pi * 2 / 80
            wx = int(tw // 2 + math.cos(angle) * wave_r * 1.8)
            wy = int(rmid + math.sin(angle) * wave_r * 0.5)
            if 0 <= wx < tw and 0 <= wy < rows:
                fade = max(0.0, 1.0 - t * 1.5)
                if fade > 0.1:
                    grid[wy][wx]  = "·"
                    cgrid[wy][wx] = C.YELLOW

        # Debris
        for d in DEBRIS:
            dx = int(tw // 2 + math.cos(d["angle"]) * d["speed"] * t * tw * 0.4)
            dy = int(rmid + math.sin(d["angle"]) * d["speed"] * t * rows * 0.7)
            if 0 <= dx < tw and 0 <= dy < rows:
                grid[dy][dx]  = d["ch"]
                cgrid[dy][dx] = C.RED

        # Text
        for i, ch in enumerate(chars):
            cx = base_x + i
            if 0 <= cx < tw:
                grid[ty][cx]  = ch
                cgrid[ty][cx] = C.RED + C.BOLD

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
