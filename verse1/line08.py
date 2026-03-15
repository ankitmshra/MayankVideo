"""
Line08 — "Going on vacations with Villeneuve view"
Effect: CINEMATIC PAN — large pyfiglet text slides in from right like a film title card,
        with subtle film grain noise, letterbox bars, and drifting luxury vacation emojis
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

_rng = random.Random(77)
GRAIN = list("·∙ ·  · ∙  ∙ · ")
VACATION_EMOJIS = ["🌴", "🛥️", "🏖️", "🍹", "🏝️", "🛳️", "🏄", "🌅"]

class Line08(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 30
        
        # Slide in from right
        prog = min(1.0, t / 0.9)
        prog = 1 - (1 - prog) ** 3
        
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                current_char = grid[gy][gx][0]
                if current_char in VACATION_EMOJIS:
                    if gx < tw - 1 and grid[gy][gx+1][0] == "":
                        grid[gy][gx+1] = (" ", "")
                elif current_char == "":
                    if gx > 0 and grid[gy][gx-1][0] in VACATION_EMOJIS:
                        grid[gy][gx-1] = (" ", "")
                grid[gy][gx] = (gchar, gcol)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["GOING ON", "VACATIONS"]),
            (1.0, ["WITH", "VILLENEUVE", "VIEW"])
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

        # Film grain background
        for r in range(1, rows - 1):
            for c in range(tw):
                if _rng.random() < 0.04:
                    set_grid(r, c, _rng.choice(GRAIN).strip() or "·", C.DIM + C.GREY)

        # Drifting Luxury Emojis Background (High Density)
        for i in range(80):  # Increased from 8 to 80 copies of the emojis
            emoji = VACATION_EMOJIS[i % len(VACATION_EMOJIS)]
            # Deterministic pseudo-random drifting
            speed = 3 + (i % 4)
            start_offset = (i * 17) % tw
            y_pos = 2 + ((i * 11) % (rows - 4))
            
            x_pos = int((start_offset + t * speed) % tw)
            
            # Subtly bob up and down
            y_bob = int(math.sin(t * 2 + i) * 1.5)
            final_y = y_pos + y_bob
            
            if 1 <= final_y < rows - 1 and x_pos < tw - 1:
                set_grid(final_y, x_pos, emoji, "")
                set_grid(final_y, x_pos + 1, "", "")

        # Text sliding in
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                start_x = tw
                current_pad = int(start_x + (target_pad - start_x) * prog)
                
                for i, ch in enumerate(text_line_str):
                    px = current_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color + C.BOLD)

        # Letterbox bars
        for c in range(tw):
            set_grid(0, c, "▓", C.DIM + C.GREY)
            set_grid(rows - 1, c, "▓", C.DIM + C.GREY)

        top = center_v(rows + 4, th)
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
