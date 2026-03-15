"""
Line04 — "I carry us too much"
Effect: WEIGHT CRUSH — text sags under heavy load, compression bars above
"""
import math
from common import C, LineAnimator, center_v


class Line04(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        weight = min(1.0, t / 1.8)
        text_y = int(rows * 0.3 + weight * rows * 0.45)
        text_y = min(rows - 1, text_y)

        # Weight blocks pressing down
        block_h = max(0, int(weight * rows * 0.25))
        for r in range(block_h):
            for c in range(base_x - 1, base_x + n + 1):
                if 0 <= c < tw:
                    grid[r][c]  = "▓" if r == block_h - 1 else "█"
                    cgrid[r][c] = C.DIM + C.GREY if r < block_h - 1 else C.WHITE

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw and 0 <= text_y < rows:
                grid[text_y][gx]  = ch
                cgrid[text_y][gx] = color

        # Crack lines at base
        if weight > 0.7:
            crack_y = text_y + 1
            if 0 <= crack_y < rows:
                for c in range(base_x - 2, base_x + n + 2):
                    if 0 <= c < tw:
                        grid[crack_y][c]  = "╌"
                        cgrid[crack_y][c] = C.DIM + C.RED

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
