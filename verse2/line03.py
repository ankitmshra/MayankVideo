"""
Line03 — "Yet all he did was sleep and waste time and talk cap"
Effect: SLEEP SAG — text droops/sags like falling asleep, Z's float up
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(12)
ZS = [
    {"x": _rng.uniform(0.3, 0.7), "phase": _rng.uniform(0, 6), "size": _rng.choice(["z", "Z", "Zz"])}
    for _ in range(8)
]


class Line03(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows  = 13
        rmid  = rows // 2
        chars = list(text)
        n     = len(chars)
        grid  = [[" "] * tw for _ in range(rows)]
        cgrid = [[None] * tw for _ in range(rows)]

        # Text sags: each char droops proportionally over time
        sag_amount = min(3.0, t * 0.8)
        for i, ch in enumerate(chars):
            sag    = math.sin(i / n * math.pi) * sag_amount
            cx     = (tw - n) // 2 + i
            cy     = int(rmid + sag)
            cy     = max(0, min(rows - 1, cy))
            if 0 <= cx < tw:
                grid[cy][cx]  = ch
                cgrid[cy][cx] = C.DIM + color if sag_amount > 1.5 else color

        # Floating Z's
        for z in ZS:
            age   = (t * 0.6 + z["phase"]) % 4.0
            zx    = int(z["x"] * tw + math.sin(age * 2) * 3)
            zy    = int(rows - 1 - age * (rows / 4.0))
            if 0 <= zx < tw and 0 <= zy < rows:
                for j, zc in enumerate(z["size"]):
                    if 0 <= zx + j < tw:
                        grid[zy][zx + j]  = zc
                        cgrid[zy][zx + j] = C.DIM + C.BLUE

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
