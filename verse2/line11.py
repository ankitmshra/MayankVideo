"""
Line11 — "I cut ties, i moved on, didn't look back"
Effect: SCISSORS CUT — a line connects words, scissors travel across snipping it
"""
import math
from common import C, LineAnimator, center_v

SCISSORS_OPEN  = "✂"
SCISSORS_CLOSE = "✄"


class Line11(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 9
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Scissors position
        scx = int((t / 2.3) * (tw + 4) - 2)
        scx = min(tw + 1, scx)

        # Thread line — only draw right of scissors
        thread_y = rmid - 1
        for c in range(max(0, scx + 1), tw):
            if grid[thread_y][c] == " ":
                grid[thread_y][c]  = "─"
                cgrid[thread_y][c] = C.DIM + C.GREY

        # Scissors icon
        sc_char = SCISSORS_OPEN if int(t * 8) % 2 == 0 else SCISSORS_CLOSE
        if 0 <= scx < tw:
            grid[thread_y][scx]  = sc_char
            cgrid[thread_y][scx] = C.GREEN + C.BOLD

        # Text
        for i, ch in enumerate(chars):
            cx = base_x + i
            if not (0 <= cx < tw):
                continue
            # Text to the right of scissors fades
            if cx > scx:
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = C.DIM + C.GREY
            else:
                grid[rmid][cx]  = ch
                cgrid[rmid][cx] = color

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
