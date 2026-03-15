"""
Line15 — "You got no clue how they control you."
Effect: PUPPET STRINGS — fingers descend from top pulling each chunk of pyfiglet text
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v

# Hand ASCII Art Array for the top of the strings
HANDS = [
    r"   _|\   /|_   ",
    r"   \ \\ // /   ",
    r"    | || | |   ",
    r"   / /  \  \   ",
]


class Line15(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 30
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["YOU GOT", "NO CLUE"]),
            (0.9, ["HOW THEY", "CONTROL YOU."])
        ]
        
        active_chunk = []
        for start_time, lines_text in reversed(chunks):
            if t >= start_time:
                active_chunk = lines_text
                break
                
        rendered_lines = []
        for lt in active_chunk:
            rendered = pyfiglet.figlet_format(lt, font="small").split("\n")
            rendered_lines.extend(rendered)
            rendered_lines.append("")

        text_height = len(rendered_lines)
        
        # Base string positions spanning the text width
        max_len = max((len(l) for l in rendered_lines), default=0)
        base_x = (tw - max_len) // 2

        # Draw puppet strings spanning across the chunk
        string_positions = [max(0, base_x + int(max_len * dx)) for dx in [0.1, 0.3, 0.5, 0.7, 0.9]]
        
        # Top container for hand positions
        hand_cxs = [sx for i, sx in enumerate(string_positions) if i % 2 == 0]

        for sx in string_positions:
            sway = math.sin(t * 2 + sx * 0.3) * 2.5
            start_y = int((rows - text_height) // 2 + sway)
            start_y = max(3, min(rows - text_height - 1, start_y))
            
            # Draw string down to text
            for sy in range(4, start_y):
                if 0 <= sx < tw:
                    set_grid(sy, sx, "│", C.DIM + C.RED)
                    
        # Draw floating/moving Hands
        for hx in hand_cxs:
            hand_y_offset = int(math.sin(t * 4 + hx) * 1)
            for hy, hline in enumerate(HANDS):
                draw_y = hy + hand_y_offset
                start_x = hx - 7
                for px, pch in enumerate(hline):
                    abs_x = start_x + px
                    if 0 <= abs_x < tw and 0 <= draw_y < rows:
                        if pch != " ":
                            set_grid(draw_y, abs_x, pch, C.ORANGE)

        # Draw text at bottom of strings
        # Average sway to apply to whole block
        avg_sway = int(math.sin(t * 2 + (tw // 2) * 0.3) * 2.5)
        text_start_y = int((rows - text_height) // 2 + avg_sway)
        text_start_y = max(6, min(rows - text_height - 1, text_start_y))

        for y, text_line_str in enumerate(rendered_lines):
            text_row = text_start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)
                        else:
                            # Also clear puppet strings where there are spaces between letters
                            set_grid(text_row, px, " ", None)

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
