"""
Line07 — "I'm a born leader"
Effect: SPOTLIGHT — single beam illuminates text from above, darkness around
"""
import math
from common import C, LineAnimator, center_v


class Line07(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Spotlight cone from top center
        spotlight_w = n + 4
        for r in range(rows):
            cone_half = int(spotlight_w / 2 * (r + 1) / rows)
            for c in range(tw):
                dist = abs(c - tw // 2)
                in_cone = dist <= cone_half
                if in_cone and r == rmid and base_x <= c < base_x + n:
                    pass  # text row
                elif in_cone:
                    grid[r][c]  = "·" if r % 2 == 0 else " "
                    cgrid[r][c] = C.DIM + C.YELLOW
                else:
                    grid[r][c]  = "░"
                    cgrid[r][c] = C.DIM + C.GREY

        # Beam edges
        for r in range(rows):
            cone_half = int(spotlight_w / 2 * (r + 1) / rows)
            for edge in [tw // 2 - cone_half, tw // 2 + cone_half]:
                if 0 <= edge < tw:
                    grid[r][edge]  = "│"
                    cgrid[r][edge] = C.DIM + C.YELLOW

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = C.WHITE + C.BOLD

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
