"""
Line03 — "I play doom doom FPS with my gun i go and shoot shoot"
Effect: GUNFIRE — ASCII text shakes violently, bullet chars spray, doom references in background.
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

_rng = random.Random(42)

# Pre-generate bullet particles
BULLETS = [
    {
        "x": _rng.uniform(0, 1),
        "y": _rng.uniform(0.2, 0.8),
        "vx": _rng.uniform(0.3, 1.0) * _rng.choice([-1, 1]),
        "vy": _rng.uniform(-0.1, 0.1),
        "ch": _rng.choice(["•", "·", "∙", "°", "*"]),
        "t0": _rng.uniform(0, 2.5),
    }
    for _ in range(40)
]

class Line03(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 24
        top = center_v(rows + 4, th)
        
        grid = [[(" ", "")] * tw for _ in range(rows)]
        doom_emojis = ["👹", "💀", "💥", "🔫"]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                current_char = grid[gy][gx][0]
                if current_char in doom_emojis:
                    if gx < tw - 1 and grid[gy][gx+1][0] == "":
                        grid[gy][gx+1] = (" ", "")
                elif current_char == "":
                    if gx > 0 and grid[gy][gx-1][0] in doom_emojis:
                        grid[gy][gx-1] = (" ", "")
                grid[gy][gx] = (gchar, gcol)

        # Background: Doom emojis floating around
        for x in range(0, tw, 14):
            for y in range(0, rows, 6):
                offset = (x * 7 + y * 11) % 100
                speed = 2
                y_pos = (y + t * speed + offset) % rows
                y_idx = int(y_pos)
                emoji = doom_emojis[(x + y) % len(doom_emojis)]
                if 0 <= y_idx < rows and x < tw - 1:
                    grid[y_idx][x] = (emoji, "")
                    grid[y_idx][x+1] = ("", "")

        # Bullets spraying
        for b in BULLETS:
            age = (t - b["t0"]) % 3.2
            if age < 0:
                continue
            bx = int((b["x"] + b["vx"] * age * 2) * tw)
            by = int((b["y"] + b["vy"] * age * 2) * rows)
            if 0 <= bx < tw and 0 <= by < rows:
                set_grid(by, bx, b["ch"], C.YELLOW if int(t * 10) % 2 == 0 else C.ORANGE)

        # Shake recoil for text
        shake_x = int(math.sin(t * 40) * 2 * (0.5 + 0.5 * math.sin(t * 7)))
        shake_y = int(math.cos(t * 35) * 1)
        
        chunks = [
            (0.0, ["I PLAY", "DOOM DOOM", "FPS"]),
            (1.0, ["WITH MY GUN", "I GO AND"]),
            (2.0, ["SHOOT", "SHOOT"])
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
        start_y = (rows - text_height) // 2 + shake_y
        
        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2) + shake_x
                
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            text_col = C.RED if int(t * 8) % 2 == 0 else C.WHITE
                            set_grid(text_row, px, ch, text_col)

        # Muzzle flash
        if int(t * 12) % 3 == 0:
            fx = tw // 2 + shake_x
            fy = start_y + text_height // 2
            if 0 <= fy < rows and 0 <= fx < tw:
                set_grid(fy, fx, "★", C.YELLOW)

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
