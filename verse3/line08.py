"""
Line08 — "Straight outta the best kept secret"
Effect: DECODE — text starts as cipher/noise, characters resolve one by one
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(77)
CIPHER = list("@#$%&?!0123456789ABCDEF∆Ω∑≠≈")


class Line08(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 7
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        for i, ch in enumerate(chars):
            cx       = base_x + i
            reveal_t = i * (2.2 / n)
            if t >= reveal_t:
                # Revealed
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = color
            else:
                # Still scrambled
                grid[rmid][cx]  = _rng.choice(CIPHER)
                cgrid[rmid][cx] = C.DIM + C.GREEN

        # Scan line moving left to right
        scan_x = int((t / 2.2) * n) + base_x
        if 0 <= scan_x < tw:
            for r in range(rows):
                if grid[r][scan_x] == " ":
                    grid[r][scan_x]  = "│"
                    cgrid[r][scan_x] = C.GREEN

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
