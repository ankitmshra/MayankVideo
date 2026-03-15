"""
Line05 — "I gave him all the chances and dealt it with patience"
Effect: HOURGLASS — sand drips through an hourglass beside the text
"""
import math
from common import C, LineAnimator, center_v


class Line05(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 13
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Hourglass on the right
        hx     = base_x + n + 5
        hy     = 1
        hglass = [
            "╔═══╗",
            "╚═╦═╝",
            "  ║  ",
            "╔═╩═╗",
            "╚═══╝",
        ]
        for ri, hrow in enumerate(hglass):
            for ci, hc in enumerate(hrow):
                gx = hx + ci
                gy = hy + ri
                if 0 <= gx < tw and 0 <= gy < rows:
                    grid[gy][gx]  = hc
                    cgrid[gy][gx] = C.GOLD

        # Sand draining: top chamber empties, bottom fills
        fill_prog  = min(1.0, t / 2.8)
        top_sand   = int((1 - fill_prog) * 3)
        bot_sand   = int(fill_prog * 3)

        for s in range(top_sand):
            for sx in range(1, 4):
                gx = hx + sx
                gy = hy + 1 - s
                if 0 <= gx < tw and 0 <= gy < rows:
                    grid[gy][gx]  = "▓"
                    cgrid[gy][gx] = C.ORANGE

        for s in range(bot_sand):
            for sx in range(1, 4):
                gx = hx + sx
                gy = hy + 4 - s
                if 0 <= gx < tw and 0 <= gy < rows:
                    grid[gy][gx]  = "░"
                    cgrid[gy][gx] = C.ORANGE

        # Falling grain
        grain_y = hy + 2
        grain_x = hx + 2
        if int(t * 8) % 3 != 0 and 0 <= grain_x < tw and 0 <= grain_y < rows:
            grid[grain_y][grain_x]  = "·"
            cgrid[grain_y][grain_x] = C.YELLOW

        # Text
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
