"""
Line10 — "Diamonds in my ceiling"
Effect: CRYSTAL GROWTH — diamond shapes crystallize downward from top
"""
import math
from common import C, LineAnimator, center_v

DIAMOND_CHARS = ["◆", "◇", "✦", "✧", "⬡", "·"]


class Line10(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Diamond positions across ceiling
        diamond_xs = list(range(4, tw - 4, 8))
        for dx in diamond_xs:
            # Each diamond grows at slightly different speed
            speed    = 0.7 + math.sin(dx * 0.3) * 0.3
            grow_len = min(rows // 2 - 1, int(t * speed * 3))
            for dl in range(grow_len):
                dy = dl
                if 0 <= dy < rows:
                    # Sparkle: bigger char at tip
                    ch  = DIAMOND_CHARS[0] if dl == grow_len - 1 else DIAMOND_CHARS[min(dl + 1, len(DIAMOND_CHARS) - 1)]
                    col = C.CYAN if dl == grow_len - 1 else (C.BLUE if dl % 2 == 0 else C.DIM + C.BLUE)
                    if 0 <= dx < tw:
                        grid[dy][dx]  = ch
                        cgrid[dy][dx] = col

                    # Side glints
                    for sx_off in (-1, 1):
                        sx = dx + sx_off
                        if 0 <= sx < tw and dl == grow_len - 1:
                            grid[dy][sx]  = "·"
                            cgrid[dy][sx] = C.WHITE

        # Text
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid + 2][gx]  = ch
                cgrid[rmid + 2][gx] = color

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
