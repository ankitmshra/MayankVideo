"""
Line02 — "I thought we will work hard on our tracks"
Effect: TYPEWRITER — chars type out one by one, cursor blink, like writing a plan
"""
import math
from common import C, LineAnimator, center_v


class Line02(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 7
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2

        # How many chars revealed
        reveal = min(n, int(t * (n / 2.0)))
        cursor = "█" if int(t * 4) % 2 == 0 else " "

        grid  = [[" "] * tw for _ in range(rows)]
        cgrid = [[None] * tw for _ in range(rows)]

        # Typed text
        for i in range(reveal):
            cx = base_x + i
            if 0 <= cx < tw:
                grid[rmid][cx]  = chars[i]
                cgrid[rmid][cx] = color

        # Cursor
        cur_x = base_x + reveal
        if 0 <= cur_x < tw:
            grid[rmid][cur_x]  = cursor
            cgrid[rmid][cur_x] = C.WHITE

        # Ruled lines (notebook paper feel)
        for r in range(rows):
            if r != rmid:
                for c in range(base_x - 2, base_x + n + 2):
                    if 0 <= c < tw and grid[r][c] == " ":
                        grid[r][c]  = "─"
                        cgrid[r][c] = C.DIM + C.GREY

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
