"""
Line01 — "My bandmate now flatmate"
Effect: SPLIT SCREEN — screen divides in two, left=studio, right=apartment
"""
import math
from common import C, LineAnimator, center_v


class Line01(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows  = 11
        rmid  = rows // 2
        half  = tw // 2
        grid  = [[" "] * tw for _ in range(rows)]
        cgrid = [[None] * tw for _ in range(rows)]

        # Divider line pulses
        div_char = "║" if int(t * 6) % 2 == 0 else "│"
        for r in range(rows):
            grid[r][half]  = div_char
            cgrid[r][half] = C.GREY

        # Left side: studio gear symbols
        studio = ["♪", "♫", "🎵", "▶", "◼", "═", "≋"]
        for i, sym in enumerate(studio):
            sx = half // 2 - 3 + (i % 4) * 2
            sy = rmid - 2 + (i // 4)
            if 0 <= sx < half and 0 <= sy < rows:
                grid[sy][sx]  = sym
                cgrid[sy][sx] = C.CYAN

        # Right side: home symbols
        home = ["⌂", "☕", "Zz", "─", "▭"]
        for i, sym in enumerate(home):
            hx = half + half // 2 - 2 + (i % 3)
            hy = rmid - 1 + (i // 3)
            if 0 <= hx < tw and 0 <= hy < rows:
                for j, sc in enumerate(sym):
                    if 0 <= hx + j < tw:
                        grid[hy][hx + j]  = sc
                        cgrid[hy][hx + j] = C.ORANGE

        # Text centered
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        for i, ch in enumerate(chars):
            cx = base_x + i
            if 0 <= cx < tw:
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
