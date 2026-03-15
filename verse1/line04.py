"""
Line04 — "You need to show ID at the club we are not the same dude"
Effect: VELVET ROPE — text behind a bouncer gate, pyfiglet chunks sliding in, large blinking cross at the end.
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v

class Line04(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 20
        rmid = rows // 2

        # Gate opens over first 0.8s
        open_prog = min(1.0, t / 0.8)
        open_prog = 1 - (1 - open_prog) ** 2  # ease out

        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Chunks for Pyfiglet
        chunks = [
            (0.0, ["YOU NEED", "TO SHOW ID"]),
            (0.8, ["AT THE", "CLUB"]),
            (1.4, ["WE ARE NOT", "THE SAME"]),
            (2.0, ["DUDE"])
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
        
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        # Velvet rope posts (widened for ascii text)
        base_x = tw // 2 - 25
        n_width = 50
        post_l = base_x - 4
        post_r = base_x + n_width + 3
        
        for r in range(rows):
            set_grid(r, post_l, "║", C.GOLD)
            set_grid(r, post_r, "║", C.GOLD)

        # Rope swings: top end fixed, bottom end swings outward
        rope_len = rows - 2
        for seg in range(rope_len):
            progress = seg / rope_len
            swing = int(open_prog * 15 * progress)
            lx = post_l + swing
            rx = post_r - swing
            ry = 1 + seg
            rope_char = "─" if seg == 0 else ("╰" if seg == rope_len - 1 else "│")
            set_grid(ry, lx, rope_char, C.GOLD)
            set_grid(ry, rx, rope_char, C.GOLD)

        # "ID CHECK" sign
        sign = "[ ID CHECK ]"
        sx = (tw - len(sign)) // 2
        if open_prog < 0.5:
            for si, sc in enumerate(sign):
                set_grid(0, sx + si, sc, C.RED + C.BOLD)

        # Blinking huge cross symbol at the end (t > 2.5)
        # blinks twice: 2.5-2.6 (ON), 2.6-2.7 (OFF), 2.7-2.8 (ON), 2.8-2.9 (OFF)
        is_cross_visible = False
        if 2.5 <= t < 2.6 or 2.7 <= t < 2.8:
            is_cross_visible = True
            
        if is_cross_visible:
            center_x = tw // 2
            center_y = rows // 2
            # Draw a massive X
            for cy in range(rows):
                for cx in range(tw):
                    dx = cx - center_x
                    dy = cy - center_y
                    # Check distance from diagonals dx = 2*dy and dx = -2*dy
                    if abs(dx - 2 * dy) < 4 or abs(dx + 2 * dy) < 4:
                        # Add some constraints to not make it infinitely wide
                        if abs(dy) < 8:
                            set_grid(cy, cx, "█", C.RED)

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
