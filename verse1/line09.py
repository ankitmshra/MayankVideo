"""
Line09 — "Chalamet with my energy i feel always new"
Effect: ENERGY AURA — large pyfiglet text radiates outward glow rings, chars shimmer
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v

AURA_CHARS = ["·", "∘", "○", "◌", "◎", "●"]

class Line09(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 34
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Aura rings emanating from text center
        cx_center = tw // 2
        rmid = rows // 2
        for ring in range(5):
            radius = ring * 3 + int(t * 8) % 15
            for angle_step in range(64):
                angle = angle_step * math.pi * 2 / 64
                rx = cx_center + int(math.cos(angle) * radius * 1.8)
                ry = rmid + int(math.sin(angle) * radius * 0.7)
                if 0 <= rx < tw and 0 <= ry < rows:
                    fade_idx = min(len(AURA_CHARS) - 1,
                                   max(0, len(AURA_CHARS) - 1 - ring))
                    set_grid(ry, rx, AURA_CHARS[fade_idx], C.DIM + C.MAGENTA)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["CHALAMET", "WITH MY", "ENERGY"]),
            (1.4, ["I FEEL", "ALWAYS", "NEW"])
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

        # Text with shimmer
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            shimmer = math.sin(t * 6 + i * 0.2 + y * 0.5)
                            col = C.WHITE if shimmer > 0.5 else (C.PINK if shimmer > -0.2 else color)
                            set_grid(text_row, px, ch, col)

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
