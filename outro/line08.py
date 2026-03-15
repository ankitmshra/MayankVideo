"""
Line08 — "We in it like it's ride or die." (FINAL)
Effect: GOLDEN FADE OUT — text glows gold, particles dissolve upward into void
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(1)
PARTICLES = [
    {"x": _rng.uniform(0, 1), "y": _rng.uniform(0.3, 1.0),
     "speed": _rng.uniform(0.2, 0.7), "ch": _rng.choice(["·", "∘", "✦", "°", "*"]),
     "phase": _rng.uniform(0, math.pi * 2)}
    for _ in range(35)
]


class Line08(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Particles float upward and fade
        for p in PARTICLES:
            age = (t * p["speed"] + p["phase"]) % (rows * 1.5)
            px  = int(p["x"] * tw + math.sin(age * 1.5 + p["phase"]) * 3)
            py  = int(rows - age)
            if 0 <= px < tw and 0 <= py < rows:
                high = py < rows * 0.4
                col  = C.GOLD if high else C.DIM + C.ORANGE
                grid[py][px]  = p["ch"]
                cgrid[py][px] = col

        # Text glows — shimmer between gold and white
        shimmer = math.sin(t * 4)
        tc      = C.GOLD + C.BOLD if shimmer > 0 else C.WHITE + C.BOLD
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = tc

        # Fade-out vignette on last second
        fade_start = 2.0
        if t > fade_start:
            fade = min(1.0, (t - fade_start) / 1.0)
            vign_chars = ["░", "▒", "▓", "█"]
            vc = vign_chars[min(len(vign_chars) - 1, int(fade * len(vign_chars)))]
            for r in range(rows):
                for c in range(int(fade * tw // 2)):
                    for gx in [c, tw - 1 - c]:
                        if 0 <= gx < tw and grid[r][gx] == " ":
                            grid[r][gx]  = vc
                            cgrid[r][gx] = C.DIM + C.GREY

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
