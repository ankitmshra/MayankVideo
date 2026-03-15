"""
Line13 — "A roller coaster full of heaters"
Effect: ROLLER COASTER TRACK — sinusoidal track fills screen, cart rides it
"""
import math
from common import C, LineAnimator, center_v

CART = "▶◼"


class Line13(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Track: complex wave
        track_ys = []
        for c in range(tw):
            ty = int(rows * 0.5
                     + math.sin(c * 0.12) * rows * 0.25
                     + math.sin(c * 0.07 + 1.2) * rows * 0.12)
            ty = max(1, min(rows - 2, ty))
            track_ys.append(ty)

        # Draw track
        for c in range(tw):
            ty = track_ys[c]
            # Support pillars
            for py in range(ty + 1, rows - 1):
                if 0 <= py < rows:
                    grid[py][c]  = "│"
                    cgrid[py][c] = C.DIM + C.GREY
            # Rail
            if 0 <= ty < rows:
                grid[ty][c]  = "═"
                cgrid[ty][c] = C.ORANGE

        # Ground
        for c in range(tw):
            grid[rows - 1][c]  = "▀"
            cgrid[rows - 1][c] = C.DIM + C.GREY

        # Rolling cart
        cart_c = int((t * tw * 0.4) % tw)
        cart_y = track_ys[cart_c] - 1
        for ci, cc in enumerate(CART):
            gx = cart_c + ci
            if 0 <= gx < tw and 0 <= cart_y < rows:
                grid[cart_y][gx]  = cc
                cgrid[cart_y][gx] = C.RED + C.BOLD

        # Text floating above midpoint of track
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[0][gx]  = ch
                cgrid[0][gx] = color

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
