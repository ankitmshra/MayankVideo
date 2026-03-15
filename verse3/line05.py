"""
Line05 — "Put Rome in the ground i'm the ruler"
Effect: THRONE RISE — pillars grow from bottom, text sits atop like a ruler
"""
import math
from common import C, LineAnimator, center_v


class Line05(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 15
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Pillars rise
        pillar_xs = [tw // 2 - 16, tw // 2 - 8, tw // 2, tw // 2 + 8, tw // 2 + 16]
        for px in pillar_xs:
            ph = min(rows - 3, int(t * 6))
            for py in range(rows - 1, rows - 1 - ph, -1):
                if 0 <= px < tw and 0 <= py < rows:
                    grid[py][px]  = "║"
                    cgrid[py][px] = C.GOLD
            # Capital
            cap_y = rows - 1 - ph
            if 0 <= cap_y >= 0 and cap_y < rows and 0 <= px < tw:
                grid[cap_y][px]  = "╦"
                cgrid[cap_y][px] = C.GOLD

        # Entablature (horizontal beam)
        beam_h = int(t * 6)
        if beam_h >= 4:
            beam_y = rows - 1 - beam_h
            if 0 <= beam_y < rows:
                for c in range(pillar_xs[0], pillar_xs[-1] + 1):
                    if 0 <= c < tw:
                        grid[beam_y][c]  = "═"
                        cgrid[beam_y][c] = C.GOLD

        # Text sits on top of beam
        text_y = max(0, rows - 1 - int(t * 6) - 1)
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw and 0 <= text_y < rows:
                grid[text_y][gx]  = ch
                cgrid[text_y][gx] = color

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
