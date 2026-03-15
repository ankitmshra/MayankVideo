"""
Line13 — "My estate is building day by day it'll be huge"
Effect: GRAND EMPIRE RISE — a sprawling skyline erupts from the ground,
        towering skyscrapers with golden spires, cranes, glowing windows,
        completion bursts, and a shimmering ground horizon.
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

FLOORS  = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
WINDOWS = ["▪", "□", "▫", "◈"]
_rng    = random.Random(7)

# More buildings, taller, wider — a true empire skyline
BUILDINGS = [
    {"cx_off": -52, "w": 10, "max_h": 16, "speed": 1.1, "col": C.BLUE},
    {"cx_off": -40, "w": 14, "max_h": 24, "speed": 1.4, "col": C.GOLD},
    {"cx_off": -24, "w": 11, "max_h": 20, "speed": 1.2, "col": C.CYAN},
    {"cx_off": -11, "w": 18, "max_h": 30, "speed": 1.6, "col": C.GOLD},  # centrepiece
    {"cx_off":   9, "w": 13, "max_h": 26, "speed": 1.5, "col": C.MAGENTA},
    {"cx_off":  24, "w": 11, "max_h": 21, "speed": 1.3, "col": C.CYAN},
    {"cx_off":  37, "w": 15, "max_h": 25, "speed": 1.4, "col": C.GOLD},
    {"cx_off":  54, "w":  9, "max_h": 15, "speed": 1.0, "col": C.BLUE},
]


class Line13(LineAnimator):
    FPS = 60   # ← 60 fps

    def frame(self, text, color, t, tw, th):
        rows = 38
        grid  = [[(" ", "")] * tw for _ in range(rows)]

        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        cx = tw // 2

        for b in BUILDINGS:
            bx_start = cx + b["cx_off"]
            current_h = min(b["max_h"], int(t * b["speed"] * 9))

            for row_i in range(current_h):
                ry = rows - 2 - row_i          # leave ground row
                for wx in range(b["w"]):
                    bx = bx_start + wx
                    if 0 <= bx < tw and 0 <= ry < rows:
                        is_window = (wx % 2 == 1) and (row_i % 3 != 0)
                        if is_window:
                            lit = int(t * 4 + wx * 3 + row_i * 2) % 5 != 0
                            ch  = "□" if lit else "▪"
                            wc  = C.YELLOW if lit else C.DIM + C.GREY
                            set_grid(ry, bx, ch, wc)
                        else:
                            set_grid(ry, bx, "█", b["col"])

            # ── Spire on completed buildings ────────────────────────────────
            if current_h >= b["max_h"]:
                spire_x = bx_start + b["w"] // 2
                spire_top = rows - 2 - current_h
                for sp in range(1, 5):
                    sy = spire_top - sp
                    if 0 <= sy < rows and 0 <= spire_x < tw:
                        ch = ["▲", "△", "╤", "╧"][sp - 1]
                        set_grid(sy, spire_x, ch, C.GOLD + C.BOLD)
                # Completion starburst — glowing crown
                crown_y = spire_top - 5
                for dx in range(-3, 4):
                    if 0 <= crown_y < rows and 0 <= spire_x + dx < tw:
                        pulse = int(t * 8) % 2
                        set_grid(crown_y, spire_x + dx, "★" if dx == 0 else ("·" if pulse else "✦"),
                                 C.GOLD if dx == 0 else C.YELLOW)

            # ── Crane on buildings still rising ─────────────────────────────
            elif current_h > 0:
                crane_y = rows - 2 - current_h
                crane_x = bx_start + b["w"] // 2
                if 0 <= crane_y - 1 < rows:
                    set_grid(crane_y - 1, crane_x, "┬", C.ORANGE)
                    for arm in range(1, 10):
                        ax = crane_x + arm
                        if 0 <= ax < tw:
                            set_grid(crane_y - 1, ax, "─", C.ORANGE)
                    # Dangling hook (animates)
                    hook_arm = 6
                    hx = crane_x + hook_arm
                    hook_drop = int(t * 5) % 4
                    for hd in range(hook_drop + 1):
                        hy = crane_y - 1 + hd
                        if 0 <= hy < rows and 0 <= hx < tw:
                            set_grid(hy, hx, "│" if hd < hook_drop else "⌐", C.ORANGE)

        # ── Glowing ground line ─────────────────────────────────────────────
        ground_row = rows - 1
        for gx in range(tw):
            pulse = int(t * 6 + gx * 0.3) % 3
            ch    = ["▀", "▄", "█"][pulse]
            col   = [C.GOLD, C.ORANGE, C.YELLOW][pulse]
            set_grid(ground_row, gx, ch, col)

        # ── Pyfiglet lyrics ─────────────────────────────────────────────────
        chunks = [
            (0.0, ["MY ESTATE IS", "BUILDING"]),
            (1.0, ["DAY BY DAY"]),
            (2.0, ["IT'LL BE", "HUGE"]),
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
        start_y = 1
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw and ch != " ":
                        set_grid(text_row, px, ch, color)

        # ── Render ──────────────────────────────────────────────────────────
        top = center_v(rows + 4, th)
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        for row in grid:
            s_row = ""
            for char, col in row:
                if char != " ":
                    s_row += (col + char + C.RESET) if col else char
                else:
                    s_row += " "
            out.append(s_row)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        return "\n".join(out)