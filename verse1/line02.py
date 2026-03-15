"""
Line02 — "My pen kung fu like bruce lee go ahead and zoom zoom"
Effect: Falling pens background + text sliding in as ASCII pyfiglet chunks.
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v


class Line02(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 20
        top = center_v(rows + 4, th)
        
        grid = [[(" ", "")] * tw for _ in range(rows)]
        pen_emoji = "🖊️"
        
        def set_grid(gy, gx, gchar, gcol):
            if grid[gy][gx][0] == pen_emoji:
                if gx < tw - 1 and grid[gy][gx+1][0] == "":
                    grid[gy][gx+1] = (" ", "")
            elif grid[gy][gx][0] == "":
                if gx > 0 and grid[gy][gx-1][0] == pen_emoji:
                    grid[gy][gx-1] = (" ", "")
            grid[gy][gx] = (gchar, gcol)

        # Background: falling pens
        for x in range(0, tw, 8):
            offset = (x * 13) % 100
            speed = 8 + (x % 5)
            y_pos = (t * speed + offset) % rows
            y_idx = int(y_pos)
            if 0 <= y_idx < rows:
                if x < tw - 1:
                    grid[y_idx][x] = (pen_emoji, "")
                    grid[y_idx][x+1] = ("", "")
                    
        chunks = [
            (0.0, ["MY PEN", "KUNG FU"]),
            (0.8, ["LIKE", "BRUCE LEE"]),
            (1.6, ["GO AHEAD", "AND"]),
            (2.4, ["ZOOM", "ZOOM"])
        ]
        
        active_chunk = []
        chunk_t = 0.0
        for start_time, lines in reversed(chunks):
            if t >= start_time:
                active_chunk = lines
                chunk_t = t - start_time
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
        
        slide_prog = min(1.0, max(0.0, chunk_t / 0.3))
        slide_prog = 1 - (1 - slide_prog) ** 3
        
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                start_x = -len(text_line_str)
                current_pad = int(start_x + (target_pad - start_x) * slide_prog)
                
                if slide_prog < 1.0:
                    streak_len = int((1 - slide_prog) * 15)
                    for i, ch in enumerate(text_line_str):
                        if ch != " ":
                            for s in range(streak_len):
                                sx = current_pad + i - s - 1
                                if 0 <= sx < tw:
                                    set_grid(text_row, sx, "─", C.DIM + color if s > streak_len // 2 else color)
                
                for i, ch in enumerate(text_line_str):
                    px = current_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        
        for row in grid:
            s_row = ""
            for char, col in row:
                if char != "":
                    if col:
                        s_row += col + char + C.RESET
                    else:
                        s_row += char
            out.append(s_row)
            
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        
        return "\n".join(out)
