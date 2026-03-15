"""
Line14 — "I avoid news like the flu" / "Feeding information which is not true"
Effect: TV STATIC — noise fills screen, large pyfiglet text cuts through like a signal break
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

_rng = random.Random(55)
STATIC = list("▓▒░█▄▀■□▪▫:;.,·")

class Line14(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 26
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Static noise background
        noise_intensity = 0.35 + 0.15 * math.sin(t * 7)
        for r in range(rows):
            for c in range(tw):
                if _rng.random() < noise_intensity:
                    set_grid(r, c, _rng.choice(STATIC), C.DIM + C.GREY)

        # Horizontal scan lines interference
        scan_y = int((t * 6) % rows)
        for c in range(tw):
            set_grid(scan_y, c, "─", C.DIM + C.WHITE)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["I AVOID", "NEWS"]),
            (0.8, ["LIKE THE", "FLU"]),
            (1.4, ["FEEDING", "INFO"]),
            (2.0, ["WHICH IS", "NOT TRUE"])
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
        start_y = (rows - text_height) // 2
        
        # Clear band around text
        clear_y_start = max(0, start_y - 2)
        clear_y_end   = min(rows, start_y + text_height + 2)

        # Determine maximum line width to create a stable box
        max_line_len = max((len(l) for l in rendered_lines), default=0)
        box_pad = max(0, (tw - max_line_len) // 2)
        
        # Clear the entire rectangle for the text
        for r in range(clear_y_start, clear_y_end):
            for c in range(max(0, box_pad - 4), min(tw, box_pad + max_line_len + 4)):
                set_grid(r, c, " ", None)

        # Text — signal strength flicker
        signal = 0.7 + 0.3 * math.sin(t * 11)
        text_col = color if signal > 0.6 else C.GREY

        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                # Draw pyfiglet chars, ensuring background is fully wiped for visibility
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, text_col)
                        else:
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
