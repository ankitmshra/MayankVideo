"""
Line10 — "a weak mind, you lack will"
Effect: DISSOLVE — text crumbles apart, chars fall and scatter downward
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(21)


class Line10(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        for i, ch in enumerate(chars):
            cx = base_x + i
            # Each char starts falling at a slightly different time
            fall_start = i * 0.07
            age        = max(0.0, t - fall_start)
            fall_y     = int(age ** 1.5 * 3)
            sway_x     = int(math.sin(age * 4 + i) * age * 0.8)

            cy = min(rows - 1, rmid + fall_y)
            fx = cx + sway_x

            if 0 <= fx < tw and 0 <= cy < rows:
                # Fade char as it falls
                if fall_y > 4:
                    grid[cy][fx]  = "·"
                    cgrid[cy][fx] = C.DIM + C.GREY
                elif fall_y > 2:
                    grid[cy][fx]  = ch.lower()
                    cgrid[cy][fx] = C.DIM + color
                else:
                    grid[cy][fx]  = ch
                    cgrid[cy][fx] = color

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
