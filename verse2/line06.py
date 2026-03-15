"""
Line06 — "I bite my own words from the second verse of the first"
Effect: SELF-DESTRUCT TEXT — words get struck through as if being eaten/bitten
"""
import math
from common import C, LineAnimator, center_v


class Line06(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 7
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Strike-through creeps from the end backward
        strike_end = int(n * min(1.0, t / 2.5))

        for i, ch in enumerate(chars):
            cx = base_x + i
            if not (0 <= cx < tw):
                continue
            is_struck = i >= (n - strike_end)
            if is_struck:
                # Show struck-through char
                grid[rmid][cx]     = ch
                cgrid[rmid][cx]    = C.DIM + C.GREY
                # Strike bar
                grid[rmid - 1][cx] = "─" if ch != " " else " "
                cgrid[rmid - 1][cx] = C.RED
            else:
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = color

        # Bite marks (teeth icons) at the strike frontier
        frontier = base_x + (n - strike_end) - 1
        bite_chars = "✕✗"
        for bi, bc in enumerate(bite_chars):
            bx = frontier - bi
            if 0 <= bx < tw:
                grid[rmid + 1][bx]  = bc
                cgrid[rmid + 1][bx] = C.RED + C.BOLD

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
