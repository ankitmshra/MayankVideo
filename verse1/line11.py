"""
Line11 — "Mmm hmm that's cute,"
Effect: CUTE BOUNCE — large pyfiglet text bounces like a rubber ball with squish/stretch
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v


class Line11(LineAnimator):
    def frame(self, text, color, t, tw, th):
        rows = 24
        
        grid = [[(" ", "")] * tw for _ in range(rows)]
        
        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # Bounce: parabolic
        bounce_cycle = t % 0.7
        if bounce_cycle < 0.35:
            h_ratio = 4 * bounce_cycle / 0.35 * (1 - bounce_cycle / 0.35)
        else:
            h_ratio = 0

        rendered = pyfiglet.figlet_format("MMM HMM", font="small").strip("\n").split("\n")
        rendered.append("")
        rendered.extend(pyfiglet.figlet_format("THAT'S CUTE", font="small").strip("\n").split("\n"))
        
        text_height = len(rendered)
        max_bounce_h = rows - text_height - 2
        bounce_y_offset = int(h_ratio * max_bounce_h)

        # Squish at bottom
        squish = max(0.0, 1.0 - bounce_cycle / 0.05) if bounce_cycle < 0.05 else 0.0
        shadow_offset = 1 if squish < 0.5 else 0

        target_base_y = (rows - text_height) - 1
        ty = max(0, min(rows - text_height, target_base_y - bounce_y_offset))
        
        # Shadow
        shadow_w = tw // 2
        sx_start = tw // 4 + int(squish * shadow_w // 4)
        for i in range(max(1, shadow_w - int(squish * shadow_w // 2))):
            sy = min(rows - 1, target_base_y + text_height + shadow_offset)
            set_grid(sy, sx_start + i, "─", C.DIM + C.GREY)

        # Text rendered block
        for y, text_line_str in enumerate(rendered):
            # Apply squish selectively by packing text vertically if squishing
            squish_offset = int(y * squish * 0.3)
            text_row = ty + max(0, y - squish_offset)
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, color)

        # Stars around bouncing text
        if int(t * 8) % 3 == 0:
            for offset, star in [(-20, "✦"), (20, "✦"), (-15, "·"), (15, "·")]:
                sx = tw // 2 + offset
                cy = ty + text_height // 2
                set_grid(cy, sx, star, C.PINK)

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
