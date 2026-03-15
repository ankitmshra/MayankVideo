"""
Line02 — "Van gogh, nightscapes, dark towers"
Effect: STARRY NIGHT — swirling vortex of stars, Van Gogh style turbulence
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(9)
STAR_POOL = [
    {"x": _rng.uniform(0, 1), "y": _rng.uniform(0, 1),
     "size": _rng.choice(["·", "∘", "○", "✦", "*"]),
     "phase": _rng.uniform(0, math.pi * 2)}
    for _ in range(50)
]


class Line02(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Swirling star field — curl noise approximation
        for s in STAR_POOL:
            # Swirl: each star orbits a moving center
            sx_base = s["x"] * tw
            sy_base = s["y"] * rows
            dx      = sx_base - cx
            dy      = sy_base - rmid
            angle   = math.atan2(dy, dx) + t * 0.8 + s["phase"] * 0.1
            dist    = math.sqrt(dx * dx + dy * dy * 4) * 0.9
            sx      = int(cx + math.cos(angle) * dist)
            sy      = int(rmid + math.sin(angle) * dist * 0.5)
            if 0 <= sx < tw and 0 <= sy < rows:
                twinkle = int(t * 5 + s["phase"] * 3) % 3 == 0
                ch  = "*" if twinkle else s["size"]
                col = C.YELLOW if twinkle else (C.BLUE if s["y"] > 0.5 else C.DIM + C.CYAN)
                grid[sy][sx]  = ch
                cgrid[sy][sx] = col

        # Dark towers silhouette at bottom
        tower_xs = [tw // 5, tw * 2 // 5, tw * 3 // 5, tw * 4 // 5]
        for tx in tower_xs:
            th_tower = _rng.randint(3, 6)
            for ty in range(rows - th_tower, rows):
                for tw_off in range(-1, 2):
                    gx = tx + tw_off
                    if 0 <= gx < tw and 0 <= ty < rows:
                        grid[ty][gx]  = "█"
                        cgrid[ty][gx] = C.DIM + C.GREY

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = color + C.BOLD

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
