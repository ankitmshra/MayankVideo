"""
Line15 — "Fuck the police they can't reach us."
Effect: POLICE SIREN — red/blue strobe flashes, text escapes off-screen right
"""
import math
from common import C, LineAnimator, center_v


class Line15(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 11
        rmid   = rows // 2
        chars  = list(text)
        n      = len(chars)
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        # Strobe: alternate red / blue columns
        strobe_phase = int(t * 6) % 2
        for c in range(tw):
            zone = (c // (tw // 6)) % 2
            if zone == strobe_phase:
                flash_col = C.RED if strobe_phase == 0 else C.BLUE
                for r in range(rows):
                    if grid[r][c] == " ":
                        grid[r][c]  = "░"
                        cgrid[r][c] = C.DIM + flash_col

        # Siren lights top bar
        siren_chars = ["▓", "▒", "░"]
        for c in range(tw):
            sc = siren_chars[int((c + t * 10)) % len(siren_chars)]
            sc_col = C.RED if (c + int(t * 8)) % 2 == 0 else C.BLUE
            grid[0][c]  = sc
            cgrid[0][c] = sc_col

        # Text escapes to the right
        escape_x = int(t * tw * 0.55)
        base_x   = (tw - n) // 2 + escape_x

        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[rmid][gx]  = ch
                cgrid[rmid][gx] = C.WHITE + C.BOLD

        # Speed lines behind text
        for sl in range(1, 8):
            sx = base_x - sl * 3
            if 0 <= sx < tw:
                grid[rmid][sx]  = "─"
                cgrid[rmid][sx] = C.DIM + C.WHITE

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
