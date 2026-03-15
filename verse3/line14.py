"""
Line14 — "All of my homies are winners"
Effect: PODIUM — three platforms rise, each with a crown, confetti rains
"""
import math
import random
from common import C, LineAnimator, center_v

_rng = random.Random(66)
CONFETTI = [
    {"x": _rng.uniform(0, 1), "speed": _rng.uniform(0.3, 0.9),
     "ch": _rng.choice(["*", "·", "✦", "+", "°", "✿"]),
     "col": _rng.choice([C.YELLOW, C.CYAN, C.MAGENTA, C.GREEN, C.ORANGE]),
     "phase": _rng.uniform(0, math.pi * 2)}
    for _ in range(30)
]


class Line14(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows   = 15
        chars  = list(text)
        n      = len(chars)
        base_x = (tw - n) // 2
        grid   = [[" "] * tw for _ in range(rows)]
        cgrid  = [[None] * tw for _ in range(rows)]

        cx = tw // 2
        # Three podiums: 1st center, 2nd left, 3rd right
        podiums = [
            {"x": cx,      "target_h": 7, "label": "1st", "col": C.GOLD},
            {"x": cx - 14, "target_h": 5, "label": "2nd", "col": C.WHITE},
            {"x": cx + 14, "target_h": 4, "label": "3rd", "col": C.ORANGE},
        ]

        for pod in podiums:
            pod_h = min(pod["target_h"], int(t * 5))
            pod_w = 9
            px0   = pod["x"] - pod_w // 2
            for r in range(rows - 1, rows - 1 - pod_h, -1):
                for c in range(px0, px0 + pod_w):
                    if 0 <= c < tw and 0 <= r < rows:
                        grid[r][c]  = "█"
                        cgrid[r][c] = pod["col"]
            # Crown on top
            crown_y = rows - 1 - pod_h
            if 0 <= crown_y < rows and 0 <= pod["x"] < tw:
                grid[crown_y][pod["x"]]  = "♛"
                cgrid[crown_y][pod["x"]] = pod["col"] + C.BOLD
            # Label
            label_y = rows - 1 - pod_h // 2
            lx      = pod["x"] - len(pod["label"]) // 2
            for li, lc in enumerate(pod["label"]):
                if 0 <= lx + li < tw and 0 <= label_y < rows:
                    grid[label_y][lx + li]  = lc
                    cgrid[label_y][lx + li] = C.DIM + C.WHITE

        # Confetti rain
        for cf in CONFETTI:
            cy = int((t * cf["speed"] * rows * 0.5 + cf["phase"]) % rows)
            cx_cf = int(cf["x"] * tw + math.sin(t * 2 + cf["phase"]) * 2)
            if 0 <= cx_cf < tw and 0 <= cy < rows and grid[cy][cx_cf] == " ":
                grid[cy][cx_cf]  = cf["ch"]
                cgrid[cy][cx_cf] = cf["col"]

        # Text at top
        for i, ch in enumerate(chars):
            gx = base_x + i
            if 0 <= gx < tw:
                grid[0][gx]  = ch
                cgrid[0][gx] = color

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
