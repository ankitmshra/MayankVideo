"""
Line06 — "Who knew, In Halloween i'll play mmm....food"
Effect: MASKS — text displayed in pyfiglet on the right, animated mask cycle on the left.
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v
from .mask import p1, p2, p3, p4, p5, p6, p7

# Mask sequence: cycle from p1 to p7, then back down to p2 (p1 is start of next cycle)
MASK_FRAMES = [p1, p2, p3, p4, p5, p6, p7, p6, p5, p4, p3, p2]

class Line06(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 40
        top = center_v(rows + 4, th)

        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Draw the mask on the left
        # Cycle fast, e.g. 15 frames per second
        mask_idx = int(t * 15) % len(MASK_FRAMES)
        current_mask = MASK_FRAMES[mask_idx].strip("\n").split("\n")
        
        mask_w = max((len(l) for l in current_mask), default=0)
        mask_h = len(current_mask)
        mask_start_y = max(0, (rows - mask_h) // 2)
        mask_start_x = max(0, tw // 4 - mask_w // 2)

        for my, mline in enumerate(current_mask):
            for mx, mch in enumerate(mline):
                if mch != " ":
                    set_grid(mask_start_y + my, mask_start_x + mx, mch, C.ORANGE)

        # Draw lyrics on the right
        chunks = [
            (0.0, ["WHO", "KNEW,"]),
            (0.8, ["IN HALLOWEEN", "I'LL PLAY"]),
            (1.6, ["MMM....", "FOOD"])
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
        
        text_w = max((len(l) for l in rendered_lines), default=0)
        text_start_x = min(tw - text_w - 2, tw * 3 // 4 - text_w // 2)
        # Prevent overlapping with the mask
        if text_start_x < mask_start_x + mask_w + 2:
            text_start_x = mask_start_x + mask_w + 2

        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            for i, ch in enumerate(text_line_str):
                px = text_start_x + i
                if ch != " ":
                    # Spooky glitch/flicker coloring
                    flicker_col = C.WHITE if int(t * 15 + i) % 5 != 0 else C.GREY
                    set_grid(text_row, px, ch, flicker_col)

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
