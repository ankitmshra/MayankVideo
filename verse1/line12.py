"""
Line12 — "I flew across state to see you"
Effect: FLIGHT PATH — large plane icon streaks across screen leaving a dotted trail past pyfiglet text
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v

# Making plane bigger using a simple ASCII plane shape
PLANE_LINES = [
    r"      __|__",
    r"*---o--(_)--o---*"
]

class Line12(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 24
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["I FLEW", "ACROSS STATE"]),
            (1.5, ["TO SEE YOU"])
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
        start_y = (rows - text_height) // 2 + 2

        # Plane flies left to right quickly
        plane_w = max(len(l) for l in PLANE_LINES)
        plane_x = int((t / 2.4) * (tw + plane_w) - plane_w)
        plane_y = max(0, start_y - 6)

        # Trail
        trail_len = min(plane_x, 60)
        trail_y = plane_y + 1
        for ti in range(trail_len):
            tx = plane_x - ti - 1
            if 0 <= tx < tw:
                ch = "·" if ti % 3 != 0 else "─"
                set_grid(trail_y, tx, ch, C.DIM + C.CYAN)

        # Plane
        for py, pline in enumerate(PLANE_LINES):
            for px, pch in enumerate(pline):
                abs_x = plane_x + px
                if 0 <= abs_x < tw:
                    if pch != " ":
                        set_grid(plane_y + py, abs_x, pch, C.CYAN)

        # Text below plane
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        # Cloud puffs
        for cx, cy, cch in [(tw // 4, start_y - 1, "〜"),
                             (tw * 3 // 4, start_y - 2, "≈"),
                             (tw // 2, start_y - 1, "〜")]:
            drift = int(math.sin(t * 0.4 + cx) * 2)
            rx = cx + drift
            if 0 <= rx < tw and 0 <= cy < rows:
                set_grid(cy, rx, cch, C.DIM + C.WHITE)

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
