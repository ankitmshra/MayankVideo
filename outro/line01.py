"""
Line01 — "Sunset dripping in the water"
Effect: SUNSET REFLECTION — gradient sky above, shimmering mirror below
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(19)
SKY_COLS = [C.RED, C.ORANGE, C.YELLOW, C.GOLD]


class Line01(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 15
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        horizon = rmid

        # Sky gradient — upper half
        for r in range(horizon):
            depth = r / horizon
            col   = SKY_COLS[int(depth * (len(SKY_COLS) - 1))]
            for c in range(tw):
                shade = "░" if depth < 0.4 else ("▒" if depth < 0.7 else "▓")
                grid[r][c]  = shade
                cgrid[r][c] = C.DIM + col

        # Sun
        sun_y = horizon // 3
        sun_x = tw // 2
        grid[sun_y][sun_x]  = "●"
        cgrid[sun_y][sun_x] = C.YELLOW + C.BOLD

        # Water ripples — lower half
        for r in range(horizon, rows):
            for c in range(tw):
                wave = math.sin(c * 0.2 + t * 3 + r * 0.5) * 0.5 + 0.5
                shade = "≈" if wave > 0.6 else ("~" if wave > 0.3 else "─")
                depth_col = C.BLUE if r > horizon + 3 else C.DIM + C.ORANGE
                grid[r][c]  = shade
                cgrid[r][c] = depth_col

        # Sun reflection in water
        ref_y = horizon + (horizon - sun_y)
        ref_shimmer = "◎" if int(t * 6) % 2 == 0 else "○"
        if 0 <= ref_y < rows and 0 <= sun_x < tw:
            grid[ref_y][sun_x]  = ref_shimmer
            cgrid[ref_y][sun_x] = C.ORANGE + C.BOLD

        # Text on horizon line
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[horizon][gx]  = ch
                cgrid[horizon][gx] = color + C.BOLD

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
