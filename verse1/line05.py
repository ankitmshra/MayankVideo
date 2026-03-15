"""
Line05 — "Who knew,"
Effect: THOUGHT BUBBLE — small text drifts upward with ellipsis thought dots
"""
import math
from common import C, LineAnimator, center_v


class Line05(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 9
        rmid = rows // 2

        drift = int(math.sin(t * 1.5) * 1.5)
        ty    = max(0, min(rows - 1, rmid + drift))

        # Thought dots
        dot_count = (int(t * 3) % 4)
        dots      = "·" * dot_count

        chars  = list(text + "  " + dots)
        n      = len(chars)
        base_x = (tw - n) // 2

        grid = [[" "] * tw for _ in range(rows)]
        for i, ch in enumerate(chars):
            cx = base_x + i
            if 0 <= cx < tw:
                grid[ty][cx] = ch

        # Floating thought bubbles above
        for b in range(3):
            bx = tw // 2 + (b - 1) * 4
            by = ty - 2 - b
            if 0 <= by < rows and 0 <= bx < tw:
                bubble_size = 3 - b
                grid[by][bx] = "○" if bubble_size > 1 else "·"

        top = center_v(rows + 4, th)
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        for row in grid:
            out.append(C.DIM + color + "".join(row) + C.RESET)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        return "\n".join(out)
