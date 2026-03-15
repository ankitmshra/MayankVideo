"""
Line12 — "I felt bad, i felt good, i felt free at last."
Effect: SUNRISE BURST — rays expand outward, text emerges from center glow
"""
import math
from common import C, LineAnimator, center_v

RAY_CHARS = ["│", "╱", "─", "╲", "│", "╱", "─", "╲"]


class Line12(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx_sun = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Expanding rays
        n_rays   = 16
        ray_len  = min(int(t * 12), max(tw, rows) // 2 + 2)
        for ray_i in range(n_rays):
            angle  = ray_i * math.pi * 2 / n_rays + t * 0.3
            rc     = RAY_CHARS[ray_i % len(RAY_CHARS)]
            for step in range(1, ray_len):
                rx = int(cx_sun + math.cos(angle) * step * 2.0)
                ry = int(rmid   + math.sin(angle) * step * 0.75)
                if 0 <= rx < tw and 0 <= ry < rows:
                    if grid[ry][rx] == " ":
                        fade_col = (C.YELLOW if step < ray_len * 0.4
                                    else (C.ORANGE if step < ray_len * 0.7
                                          else C.DIM + C.ORANGE))
                        grid[ry][rx]  = rc
                        cgrid[ry][rx] = fade_col

        # Sun core
        if 0 <= cx_sun < tw and 0 <= rmid < rows:
            grid[rmid][cx_sun]  = "☀"
            cgrid[rmid][cx_sun] = C.YELLOW + C.BOLD

        # Text fades in
        text_fade = min(1.0, t / 1.2)
        text_col  = color if text_fade > 0.6 else C.DIM + color
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid + 2][gx]  = ch
                cgrid[rmid + 2][gx] = text_col

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
