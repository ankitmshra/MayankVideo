"""
Line04 — "I held back my anger tried to understand him"
Effect: PRESSURE COOKER — text is boxed in, steam vents pulse at edges
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(33)
STEAM = ["~", "≈", "∿", "〜", "⌇"]


class Line04(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Pressure builds over time
        pressure = min(1.0, t / 2.5)

        # Containment box — shrinks inward as pressure rises
        margin    = max(0, int((1 - pressure) * 6))
        box_left  = base_x - 3 + margin
        box_right = base_x + n + 2 - margin
        box_top   = rmid - 2 + margin
        box_bot   = rmid + 2 - margin

        for c in range(box_left, min(box_right + 1, tw)):
            if 0 <= box_top < rows:
                grid[box_top][c]  = "─"
                cgrid[box_top][c] = C.RED
            if 0 <= box_bot < rows:
                grid[box_bot][c]  = "─"
                cgrid[box_bot][c] = C.RED
        for r in range(box_top, min(box_bot + 1, rows)):
            if 0 <= box_left < tw:
                grid[r][box_left]  = "│"
                cgrid[r][box_left] = C.RED
            if 0 <= box_right < tw:
                grid[r][box_right]  = "│"
                cgrid[r][box_right] = C.RED

        # Steam vents shooting upward from box top
        n_vents = int(pressure * 6) + 1
        for v in range(n_vents):
            vx = box_left + int((box_right - box_left) * (v + 1) / (n_vents + 1))
            for sy in range(1, int(pressure * 5) + 1):
                vy = box_top - sy
                drift = int(math.sin(t * 5 + v + sy) * 1.5)
                if 0 <= vy < rows and 0 <= vx + drift < tw:
                    grid[vy][vx + drift]  = _rng.choice(STEAM)
                    cgrid[vy][vx + drift] = C.WHITE

        # Text — color shifts redder under pressure
        text_col = C.WHITE if pressure < 0.4 else (C.ORANGE if pressure < 0.7 else C.RED)
        for i, ch in enumerate(chars):
            cx = base_x + i
            if 0 <= cx < tw and 0 <= rmid < rows:
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = text_col

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
