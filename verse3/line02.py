"""
Line02 — "Once flew close to the sun got my wings burnt"
Effect: ICARUS — figure rises toward a blazing sun, wings catch fire
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(44)


class Line02(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 15
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Sun at top center
        sun_y = 1
        grid[sun_y][cx]  = "☀"
        cgrid[sun_y][cx] = C.YELLOW + C.BOLD
        # Sun rays
        for ray in range(8):
            angle = ray * math.pi / 4
            for dist in range(1, 4):
                rx = int(cx + math.cos(angle) * dist * 2)
                ry = int(sun_y + math.sin(angle) * dist)
                if 0 <= rx < tw and 0 <= ry < rows:
                    grid[ry][rx]  = "·"
                    cgrid[ry][rx] = C.DIM + C.YELLOW

        # Figure rising
        fig_y = max(2, int(rows - 2 - t * (rows / 3.0)))
        fire_mode = fig_y <= 4   # close enough to burn

        # Wings
        wing_ch = "≋" if fire_mode and int(t * 8) % 2 == 0 else "〜"
        wing_col = C.ORANGE if fire_mode else C.WHITE
        if 0 <= cx - 2 < tw and 0 <= fig_y < rows:
            grid[fig_y][cx - 2]  = wing_ch
            cgrid[fig_y][cx - 2] = wing_col
        if 0 <= cx + 2 < tw and 0 <= fig_y < rows:
            grid[fig_y][cx + 2]  = wing_ch
            cgrid[fig_y][cx + 2] = wing_col

        # Body
        body_chars = ["o", "│"]
        for bi, bc in enumerate(body_chars):
            by = fig_y + bi
            if 0 <= cx < tw and 0 <= by < rows:
                grid[by][cx]  = bc
                cgrid[by][cx] = C.WHITE

        # Fire sparks when burning
        if fire_mode:
            for _ in range(6):
                sx = cx + _rng.randint(-4, 4)
                sy = fig_y + _rng.randint(-1, 2)
                if 0 <= sx < tw and 0 <= sy < rows:
                    grid[sy][sx]  = _rng.choice(["*", "·", "°"])
                    cgrid[sy][sx] = C.RED

        # Text at bottom
        text_row = rows - 2
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[text_row][gx]  = ch
                cgrid[text_row][gx] = color

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
