"""
Line07 — "Track i know that it's my bad to think that we'll make it"
Effect: VHS REWIND — text glitches horizontally like a tape rewinding
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(67)


class Line07(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 9
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Horizontal glitch offset per row
        for ri in range(rows):
            glitch = int(math.sin(t * 15 + ri * 2.3) * 3 * (_rng.random() * 0.4 + 0.8))
            for ci in range(tw):
                src = (ci - glitch) % tw
                if ri == rmid:
                    # Text row: apply glitch shift
                    ch_idx = src - base_x
                    if 0 <= ch_idx < n:
                        ch = chars[ch_idx]
                        if _rng.random() < 0.05:
                            ch = _rng.choice(list("▓▒░"))
                        grid[ri][ci]  = ch
                        cgrid[ri][ci] = color if _rng.random() > 0.1 else C.WHITE
                else:
                    # Noise rows
                    if _rng.random() < 0.06:
                        grid[ri][ci]  = _rng.choice(list("─━═·"))
                        cgrid[ri][ci] = C.DIM + C.GREY

        # VHS timestamp bottom-left
        ts = f"REC ▶◀ {t:.1f}s"
        for ti, tc in enumerate(ts):
            if ti < tw:
                grid[rows - 1][ti]  = tc
                cgrid[rows - 1][ti] = C.RED

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
