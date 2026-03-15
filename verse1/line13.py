"""
Line13 — "My estate is building day by day it'll be huge"
Effect: CONSTRUCTION RISE — skyscraper blocks stack upward floor by floor under pyfiglet text
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v

FLOORS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
WINDOWS = ["▪", "□", "▫"]

class Line13(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 35
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Buildings grow
        buildings = [
            {"cx": tw // 2 - 35, "w": 12,  "max_h": 14,  "speed": 0.9},
            {"cx": tw // 2 - 15,  "w": 10,  "max_h": 18, "speed": 1.1},
            {"cx": tw // 2,      "w": 16,  "max_h": 22, "speed": 1.3},
            {"cx": tw // 2 + 18, "w": 9,  "max_h": 16, "speed": 0.95},
            {"cx": tw // 2 + 32, "w": 14,  "max_h": 12,  "speed": 0.8},
        ]

        for b in buildings:
            current_h = min(b["max_h"], int(t * b["speed"] * 8))
            for row_i in range(current_h):
                ry = rows - 1 - row_i
                for wx in range(b["w"]):
                    bx = b["cx"] + wx
                    if 0 <= bx < tw and 0 <= ry < rows:
                        # Window pattern
                        is_window = (wx % 2 == 1) and (row_i % 2 == 1)
                        ch        = "□" if is_window else "█"
                        wc        = (C.YELLOW if int(t * 3 + wx + row_i) % 4 != 0
                                     else C.DIM + C.GREY)
                        set_grid(ry, bx, ch, wc if is_window else C.GOLD)

            # Crane on top of tallest block being built
            crane_y = rows - 1 - current_h
            crane_x = b["cx"] + b["w"] // 2
            if current_h > 0 and current_h < b["max_h"]:
                if 0 <= crane_y - 1 < rows and 0 <= crane_x < tw:
                    set_grid(crane_y - 1, crane_x, "┬", C.ORANGE)
                    for arm in range(1, 8):
                        if 0 <= crane_x + arm < tw:
                            set_grid(crane_y - 1, crane_x + arm, "─", C.ORANGE)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["MY ESTATE IS", "BUILDING"]),
            (1.0, ["DAY BY DAY"]),
            (2.0, ["IT'LL BE", "HUGE"])
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
        start_y = 2

        # Text at top over skyscrapers
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
