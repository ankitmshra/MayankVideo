"""
Line04 / Line06 — "We in it like it's ride or die"
Effect: CROWD WAVE — text pulses in unison like a stadium chant
"""
import math
from common import C, LineAnimator, center_v


class Line04(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 9
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # All chars pulse together (stadium wave)
        pulse = math.sin(t * 5) * 2
        ty    = max(0, min(rows - 1, int(rmid + pulse)))

        # Echo copies above and below (crowd effect)
        for echo, alpha in [(-2, C.DIM), (-1, C.DIM), (0, ""), (1, C.DIM), (2, C.DIM)]:
            ey = ty + echo
            if not (0 <= ey < rows):
                continue
            for i, ch in enumerate(chars):
                gx = base_x + i
                if 0 <= gx < tw:
                    grid[ey][gx]  = ch
                    cgrid[ey][gx] = alpha + color

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


"""
Line05 / Line07 — "Ahh ahhhh ahh ahhh ahhh ahh"
Effect: SOUND WAVE — voice waveform visualization, bars pulse to syllables
"""


class Line05(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Waveform bars across full width
        for c in range(tw):
            # Compound wave simulating voice harmonics
            amp = (math.sin(c * 0.15 + t * 7) * 0.5
                   + math.sin(c * 0.08 - t * 4) * 0.3
                   + math.sin(c * 0.25 + t * 11) * 0.2)
            bar_h = int(abs(amp) * (rows // 2 - 1))
            for bh in range(bar_h):
                for ry in [rmid + bh, rmid - bh]:
                    if 0 <= ry < rows:
                        intensity = 1.0 - bh / max(bar_h, 1)
                        bar_ch = "█" if intensity > 0.7 else ("▓" if intensity > 0.4 else "░")
                        bar_col = color if intensity > 0.6 else C.DIM + color
                        grid[ry][c]  = bar_ch
                        cgrid[ry][c] = bar_col

        # Text floats above waveform
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[1][gx]  = ch
                cgrid[1][gx] = C.WHITE

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


# Reuse same classes for repeated lines
Line06 = Line04
Line07 = Line05
