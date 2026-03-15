"""
Line11 — "Irony of a man with feelings"
Effect: HEARTBEAT EKG — flat line then spikes with emotion, text centered
"""
import math
from common import C, LineAnimator, center_v


class Line11(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        ekg_row = rmid - 2

        # EKG line scrolls left
        for c in range(tw):
            # x in "time" coordinates
            x = (c / tw * 8 - t * 3) % 8
            # PQRST wave shape
            if 0.0 < x < 0.2:
                y = math.sin(x / 0.2 * math.pi) * 0.5
            elif 0.3 < x < 0.4:
                y = -0.4
            elif 0.4 < x < 0.5:
                y = 2.5   # R spike
            elif 0.5 < x < 0.6:
                y = -0.6
            elif 0.8 < x < 1.2:
                y = math.sin((x - 0.8) / 0.4 * math.pi) * 0.6
            else:
                y = 0.0

            ry = int(ekg_row - y * 2.5)
            ry = max(0, min(rows - 1, ry))
            if 0 <= ry < rows:
                spike = abs(y) > 1.5
                grid[ry][c]  = "█" if spike else "─"
                cgrid[ry][c] = (C.RED + C.BOLD) if spike else (C.DIM + C.GREEN)

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid + 1][gx]  = ch
                cgrid[rmid + 1][gx] = color

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
