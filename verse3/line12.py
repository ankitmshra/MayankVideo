"""
Line12 — "Got a carousel full of dreams and"
Effect: CAROUSEL SPIN — dream words orbit in a circle around center text
"""
import math
from common import C, LineAnimator, center_v

DREAMS = ["✦ ambition", "✦ glory", "✦ legacy", "✦ freedom", "✦ power", "✦ love"]


class Line12(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        cx     = tw // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Orbiting dream words
        n_dreams = len(DREAMS)
        radius_x = tw * 0.35
        radius_y = rows * 0.35
        for di, dream in enumerate(DREAMS):
            angle = (di / n_dreams) * math.pi * 2 + t * 1.2
            dx    = int(cx + math.cos(angle) * radius_x)
            dy    = int(rmid + math.sin(angle) * radius_y)
            # Depth cue: dim when "behind"
            depth = math.sin(angle)
            dcol  = color if depth > 0 else C.DIM + color
            for ci, dc in enumerate(dream):
                gx = dx + ci - len(dream) // 2
                if 0 <= gx < tw and 0 <= dy < rows:
                    grid[dy][gx]  = dc
                    cgrid[dy][gx] = dcol

        # Center text
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
