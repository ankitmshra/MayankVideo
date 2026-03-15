"""
Line07 — "Dune soundtrack playing in my ears on loop"
Effect: DESERT WAVE — giant sand dune silhouette rises beneath big pyfiglet text, slow deep pulse
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v


class Line07(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 40
        top = center_v(rows + 4, th)

        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["DUNE", "SOUNDTRACK"]),
            (0.8, ["PLAYING", "IN MY EARS"]),
            (1.6, ["ON LOOP"])
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
        
        # Text floats slowly
        drift = int(math.sin(t * 0.8) * 2)
        start_y = max(0, 4 + drift)
        
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        # BIG Dune silhouettes
        dune_chars = ["▂", "▃", "▄", "▅", "▆", "▇", "█"]
        for x in range(tw):
            # Scale dune height and make them taller overall
            dune_h = int(10 + 6 * math.sin(x * 0.04 + t * 0.6)
                         + 4 * math.sin(x * 0.1 - t * 0.3))
            dune_h = max(2, min(20, dune_h))
            
            for dy in range(dune_h):
                ry = rows - 1 - dy
                if 0 <= ry < rows:
                    if grid[ry][x][0] == " ":
                        dc = dune_chars[min(len(dune_chars) - 1, dy)]
                        shade = C.ORANGE if dy < dune_h * 0.3 else C.GOLD
                        set_grid(ry, x, dc, shade)

        # Soundwave bars across the bottom, slightly taller now
        for x in range(0, tw, 3):
            amp = abs(math.sin(x * 0.2 + t * 6))
            bar_h = int(amp * 5)
            for bh in range(bar_h):
                ry = rows - 1 - bh
                if 0 <= ry < rows:
                    # Overwrite dunes smoothly at bottom
                    set_grid(ry, x, "│", C.BLUE)
                    
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
