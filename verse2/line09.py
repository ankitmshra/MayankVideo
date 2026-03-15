"""
Line09 — "Deep down i knew that you will leave, you will quit"
Effect: FOOTSTEPS — figure walks off-screen leaving footprint trail behind
"""
import math
from common import C, LineAnimator, center_v

FOOTPRINTS = ["⌐", "¬"]   # alternating left/right foot
FIGURE     = ["o", "╪", "∧"]   # head, body, legs (top to bottom)


class Line09(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Text
        for i, ch in enumerate(chars):
            cx = base_x + i
            if 0 <= cx < tw:
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = color

        # Figure walks from center to right edge
        fig_x = int(tw // 2 + t * (tw / 3.0))

        # Footprints already left
        step_interval = 4
        steps_taken   = int(t * (tw / 3.0) / step_interval)
        for s in range(steps_taken):
            fx = tw // 2 + s * step_interval
            fy = rmid + 2
            fc = FOOTPRINTS[s % 2]
            if 0 <= fx < tw and 0 <= fy < rows:
                grid[fy][fx]  = fc
                cgrid[fy][fx] = C.DIM + C.GREY

        # Draw figure (if on screen)
        for fi, fch in enumerate(FIGURE):
            fy = rmid - len(FIGURE) + 1 + fi
            if 0 <= fig_x < tw and 0 <= fy < rows:
                grid[fy][fig_x]  = fch
                cgrid[fy][fig_x] = C.GREY

        # Ellipsis "..." fading behind
        for d in range(3):
            dx = fig_x - 3 - d * 2
            if 0 <= dx < tw and 0 <= rmid - 1 < rows:
                grid[rmid - 1][dx]  = "."
                cgrid[rmid - 1][dx] = C.DIM + C.GREY

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
