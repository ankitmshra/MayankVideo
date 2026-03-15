"""
Line10 — "My shawty pretty like Zendaya she my boo boo"
Effect: FLOATING HEARTS — hearts drift upward around large pyfiglet text
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

_rng = random.Random(99)
HEARTS = ["♥", "♡", "❤", "✿", "✦", "·"]

PARTICLES = [
    {"x": _rng.uniform(0.1, 0.9), "speed": _rng.uniform(0.3, 0.8),
     "wobble": _rng.uniform(0.5, 2.0), "ch": _rng.choice(HEARTS),
     "phase": _rng.uniform(0, math.pi * 2)}
    for _ in range(35)
]


class Line10(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 32
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Floating hearts
        for p in PARTICLES:
            ry_f = rows - 1 - (t * p["speed"] * rows * 0.4 + p["phase"]) % rows
            rx_f = p["x"] * tw + math.sin(t * p["wobble"] + p["phase"]) * 3
            ry = int(ry_f)
            rx = int(rx_f)
            if 0 <= rx < tw and 0 <= ry < rows:
                fade = C.PINK if p["ch"] in "♥❤" else C.DIM + C.MAGENTA
                set_grid(ry, rx, p["ch"], fade)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["MY SHAWTY", "PRETTY LIKE"]),
            (1.0, ["ZENDAYA", "SHE MY", "BOO BOO"])
        ]
        
        active_chunk = []
        for start_time, lines_text in reversed(chunks):
            if t >= start_time:
                active_chunk = lines_text
                break
                
        rendered_lines = []
        for lt in active_chunk:
            rendered = pyfiglet.figlet_format(lt, font="small").strip("\n").split("\n")
            rendered_lines.extend(rendered)
            rendered_lines.append("")
        if rendered_lines and rendered_lines[-1] == "":
            rendered_lines.pop()

        text_height = len(rendered_lines)
        start_y = (rows - text_height) // 2

        # Text
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        top = center_v(rows + 4, th)
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        for row in grid:
            s_row = ""
            for char, col in row:
                if char != " ":
                    if col:
                        s_row += col + char + C.RESET
                    else:
                        s_row += char
                else:
                    s_row += " "
            out.append(s_row)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        return "\n".join(out)
