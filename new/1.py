import os
import sys
import math
import pyfiglet

# Add parent directory to sys.path to import common
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C, LineAnimator, center_v

# Timing constants for easy adjustment
BOOM1_START   = 0.0     # When the left BOOM appears
BOOM2_START   = 0.8     # When the right BOOM appears
EXPLODE_START = 1.6     # When BOTH BOOMs explode simultaneously
REST_START    = 2.4     # When the rest of the lyrics start appearing

class Line01(LineAnimator):
    def frame(self, text, color, t, tw, th):
        content = []
        
        if t < REST_START:
            rows_fixed = 20
            grid = [[" "] * tw for _ in range(rows_fixed)]
            cgrid = [[None] * tw for _ in range(rows_fixed)]
            
            def add_boom(start_t, center_x, center_y):
                # Don't draw if it hasn't started yet
                if t < start_t:
                    return
                    
                boom_art = pyfiglet.figlet_format("BOOM", font="small").strip("\n").split("\n")
                bw = max((len(l) for l in boom_art), default=0)
                bh = len(boom_art)
                
                for ry, row in enumerate(boom_art):
                    for rx, ch in enumerate(row):
                        if ch.strip() == "":
                            continue
                            
                        ox = center_x - bw // 2 + rx
                        oy = center_y - bh // 2 + ry
                        
                        if t < EXPLODE_START:
                            # Shake (increases as explosion nears)
                            shake_intensity = max(0, t - EXPLODE_START + 0.5) * 3
                            shake_x = math.sin(t * 60 + ry * 2) * shake_intensity
                            px = int(ox + shake_x)
                            py = int(oy)
                            if 0 <= py < rows_fixed and 0 <= px < tw:
                                grid[py][px] = ch
                                cgrid[py][px] = C.RED if (int(t * 20) % 2) == 0 else C.ORANGE
                        else:
                            # Explode both at the exact same time
                            et = t - EXPLODE_START
                            
                            dx = rx - bw // 2
                            dy = ry - bh // 2
                            dist = math.hypot(dx, dy) + 0.1
                            
                            rand_speed = 35 + ((rx * 37 + ry * 19) % 20)
                            
                            px = int(ox + (dx / dist) * rand_speed * et)
                            py = int(oy + (dy / dist) * rand_speed * et * 0.5 + 25 * et * et)
                            
                            if 0 <= py < rows_fixed and 0 <= px < tw:
                                if et > 0.4:
                                    continue
                                elif et > 0.3:
                                    out_ch = "."
                                elif et > 0.15:
                                    out_ch = "*"
                                else:
                                    out_ch = ch
                                    
                                col = C.ORANGE if out_ch == ch else (C.YELLOW if out_ch == "*" else C.DIM + C.RED)
                                grid[py][px] = out_ch
                                cgrid[py][px] = col

            add_boom(BOOM1_START, tw // 4, rows_fixed // 2)
            add_boom(BOOM2_START, 3 * tw // 4, rows_fixed // 2)
            
            for y in range(rows_fixed):
                s = ""
                for x in range(tw):
                    ch = grid[y][x]
                    if ch != " " and cgrid[y][x]:
                        s += cgrid[y][x] + ch + C.RESET
                    else:
                        s += " "
                content.append(s.rstrip())
        else:
            relative_t = t - REST_START
            lines_to_render = []
            if relative_t >= 0.0:
                lines_to_render.append("WHEN I COME")
            if relative_t >= 0.5:
                lines_to_render.append("IN THE GAME")
            if relative_t >= 1.0:
                lines_to_render.append("IT GOES")
                lines_to_render.append("BOOM BOOM")
                
            rendered_lines = []
            for lt in lines_to_render:
                rendered = pyfiglet.figlet_format(lt, font="small").strip("\n").split("\n")
                rendered_lines.extend(rendered)
                rendered_lines.append("")
                
            if rendered_lines and rendered_lines[-1] == "":
                rendered_lines.pop()
                
            max_len = max((len(l) for l in rendered_lines), default=0)
            for line in rendered_lines:
                pad = max(0, (tw - max_len) // 2)
                content.append(" " * pad + color + line + C.RESET)
                
        rows = len(content)
        top = center_v(rows + 4, th)
        
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        out.extend(content)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        
        return "\n".join(out)

if __name__ == "__main__":
    animator = Line01()
    print("Starting animation...")
    try:
        # duration 5.0 seconds is enough to see the whole 2.4s + subsequent text
        animator.play(text="line01", color=C.WHITE, duration=5.0)
    except KeyboardInterrupt:
        sys.exit(0)
