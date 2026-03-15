"""
Line06 — "Omnipotent with my dynasty mind palace is big like Caesar"
Effect: MIND PALACE — expanding room/box wireframe perspective
"""
import math
from common import C, LineAnimator, center_v


class Line06(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Nested expanding boxes (perspective illusion)
        n_boxes = 5
        for b in range(n_boxes):
            scale  = (b + 1 + t * 0.5) % (n_boxes + 1)
            scale /= n_boxes
            bw     = int(scale * tw * 0.9)
            bh     = int(scale * rows * 0.85)
            bx0    = cx - bw // 2
            bx1    = cx + bw // 2
            by0    = rmid - bh // 2
            by1    = rmid + bh // 2
            box_col = C.DIM + C.GOLD if b % 2 == 0 else C.DIM + C.MAGENTA

            for c in range(bx0, bx1 + 1):
                for r in (by0, by1):
                    if 0 <= c < tw and 0 <= r < rows:
                        grid[r][c]  = "─"
                        cgrid[r][c] = box_col
            for r in range(by0, by1 + 1):
                for c in (bx0, bx1):
                    if 0 <= c < tw and 0 <= r < rows:
                        grid[r][c]  = "│"
                        cgrid[r][c] = box_col

            # Corner connectors to center (vanishing lines)
            for (bx, by) in [(bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)]:
                dx = cx - bx
                dy = rmid - by
                steps = max(abs(dx), abs(dy), 1)
                for s in range(0, steps, 2):
                    lx = bx + int(dx * s / steps)
                    ly = by + int(dy * s / steps)
                    if 0 <= lx < tw and 0 <= ly < rows and grid[ly][lx] == " ":
                        grid[ly][lx]  = "·"
                        cgrid[ly][lx] = C.DIM + C.GREY

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = color

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
