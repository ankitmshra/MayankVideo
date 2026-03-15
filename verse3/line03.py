"""
Line03 — "Had to become Brutus had to kill the king"
Effect: KNIFE DROP — a dagger descends from top, text below throne/crown
"""
import math
from common import C, LineAnimator, center_v


class Line03(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Crown at center
        crown_y = rmid - 1
        crown   = "♛"
        grid[crown_y][cx]  = crown
        cgrid[crown_y][cx] = C.GOLD + C.BOLD

        # Dagger falls
        dagger_y = max(0, min(crown_y - 1, int(t * (rows / 1.8)) - rows // 3))
        dagger_chars = ["▼", "│"]
        for di, dc in enumerate(dagger_chars):
            dy = dagger_y - di
            if 0 <= dy < rows and 0 <= cx < tw:
                grid[dy][cx]  = dc
                cgrid[dy][cx] = C.RED + C.BOLD

        # Blood drip after impact
        if dagger_y >= crown_y - 1 and t > 1.0:
            drip_len = int((t - 1.0) * 4)
            for dr in range(min(drip_len, rows - crown_y - 1)):
                dy = crown_y + 1 + dr
                if 0 <= dy < rows:
                    grid[dy][cx]  = "│" if dr < drip_len - 1 else "·"
                    cgrid[dy][cx] = C.RED

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rows - 2][gx]  = ch
                cgrid[rows - 2][gx] = color

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
