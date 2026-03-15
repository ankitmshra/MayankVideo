"""
Line15 — "You got no clue how they control you."
Effect: PUPPETEER — a puppeteer hand & arm descend from the top of the screen,
        gripping a control bar. Strings hang from the bar down to a marionette
        figure (head, body, arms, legs). The bar jerks with a tug rhythm;
        the marionette bounces and its limbs sway. Pyfiglet lyrics appear below.
"""
import math
import pyfiglet
from common import C, LineAnimator, center_v


class Line15(LineAnimator):
    FPS = 60

    def frame(self, text, color, t, tw, th):
        rows = 36
        grid  = [[(" ", "")] * tw for _ in range(rows)]

        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        def draw_text(gy, gx, s, gcol):
            for i, ch in enumerate(s):
                set_grid(gy, gx + i, ch, gcol)

        cx = tw // 2

        # ── Tug rhythm ────────────────────────────────────────────────
        tug_freq  = 2.0
        tug_phase = t * tug_freq * 2 * math.pi
        bar_lift  = int(-abs(math.sin(tug_phase)) * 2)
        doll_lag  = int(-abs(math.sin(tug_phase - 0.5)) * 2)

        second_chunk = t >= 1.0

        # ════════════════════════════════════════════════════════════
        # 1. PUPPETEER ARM & HAND (top-centre)
        # ════════════════════════════════════════════════════════════
        ARM_COL    = C.ORANGE + C.BOLD
        FINGER_COL = C.ORANGE

        # Arm shaft coming from top
        for ay in range(0, 3):
            set_grid(ay + bar_lift, cx, "║", ARM_COL)

        # Palm / wrist
        palm_y   = 3 + bar_lift
        palm_art = [" _╨_ ", "(   )", " \\_/ "]
        for ry, line in enumerate(palm_art):
            draw_text(palm_y + ry, cx - 2, line, ARM_COL)

        # Fingers gripping
        finger_y = palm_y + len(palm_art)
        fingers  = "| | | | |"
        draw_text(finger_y, cx - 4, fingers, FINGER_COL)

        # ════════════════════════════════════════════════════════════
        # 2. CONTROL BAR
        # ════════════════════════════════════════════════════════════
        bar_y  = finger_y + 1
        bar_w  = 28
        bar_lx = cx - bar_w // 2
        bar_rx = cx + bar_w // 2
        BAR_COL = C.GOLD + C.BOLD

        for bx in range(bar_lx, bar_rx + 1):
            set_grid(bar_y, bx, "═", BAR_COL)
        set_grid(bar_y, bar_lx,  "╠", BAR_COL)
        set_grid(bar_y, bar_rx,  "╣", BAR_COL)
        # Knob positions where strings attach
        knob_cols = [cx - 8, cx, cx + 8]
        for kx in knob_cols:
            set_grid(bar_y, kx, "╦", BAR_COL)

        # ════════════════════════════════════════════════════════════
        # 3. MARIONETTE POSITION
        # ════════════════════════════════════════════════════════════
        doll_head_y  = bar_y + 7 + doll_lag
        doll_body_y  = doll_head_y + 3
        doll_kneel_y = doll_body_y + 6

        # ════════════════════════════════════════════════════════════
        # 4. STRINGS  (bar knob → body part)
        # ════════════════════════════════════════════════════════════
        STRING_COL = C.DIM + C.WHITE

        string_routes = [
            (cx - 8, cx,      doll_head_y - 1),   # head string
            (cx,     cx,      doll_head_y - 1),   # head centre
            (cx + 8, cx,      doll_head_y - 1),   # head right
            (cx - 8, cx - 5,  doll_kneel_y),      # left knee
            (cx + 8, cx + 5,  doll_kneel_y),      # right knee
        ]

        tension = abs(math.sin(tug_phase))
        str_ch  = "│" if tension > 0.5 else "╎"
        str_col = C.WHITE if tension > 0.6 else STRING_COL

        for bx, dx, dy in string_routes:
            sy_start = bar_y + 1
            sy_end   = dy - 1
            if sy_end < sy_start:
                continue
            span = max(1, sy_end - sy_start)
            for sy in range(sy_start, sy_end + 1):
                prog = (sy - sy_start) / span
                sway = math.sin(tug_phase + prog * math.pi + bx * 0.2) * 0.7
                sx   = max(0, min(tw - 1, int(bx + (dx - bx) * prog + sway)))
                set_grid(sy, sx, str_ch, str_col)

        # ════════════════════════════════════════════════════════════
        # 5. MARIONETTE FIGURE
        # ════════════════════════════════════════════════════════════
        DOLL_COL  = C.CYAN + C.BOLD
        JOINT_COL = C.YELLOW

        arm_sway = math.sin(tug_phase * 1.1) * 1.5
        leg_sway = math.sin(tug_phase * 0.9 + 0.8) * 1.5

        # Head
        draw_text(doll_head_y,     cx - 1, "(O)", DOLL_COL)
        draw_text(doll_head_y + 1, cx - 1, " ‾ ", DOLL_COL)

        # Neck
        set_grid(doll_body_y, cx, "┃", DOLL_COL)

        # Body
        body_art = ["╔═╗", "║☆║", "╚═╝"]
        for ry, line in enumerate(body_art):
            draw_text(doll_body_y + 1 + ry, cx - 1, line, DOLL_COL)
        body_bottom_y = doll_body_y + 1 + len(body_art)

        # Arms
        arm_y  = doll_body_y + 2
        larm_x = cx - 5 + int(arm_sway)
        rarm_x = cx + 5 - int(arm_sway)
        for ax in range(larm_x, cx - 1):
            set_grid(arm_y, ax, "─", DOLL_COL)
        set_grid(arm_y, larm_x, "╾", DOLL_COL)
        set_grid(arm_y, cx - 1, "┤", JOINT_COL)
        for ax in range(cx + 2, rarm_x + 1):
            set_grid(arm_y, ax, "─", DOLL_COL)
        set_grid(arm_y, rarm_x, "╼", DOLL_COL)
        set_grid(arm_y, cx + 1, "├", JOINT_COL)

        # Hip joint
        set_grid(body_bottom_y, cx, "┻", JOINT_COL)

        # Legs
        lleg_x = cx - 3 + int(-leg_sway)
        rleg_x = cx + 3 + int(leg_sway)
        for ly in range(body_bottom_y + 1, doll_kneel_y):
            set_grid(ly, lleg_x, "│", DOLL_COL)
            set_grid(ly, rleg_x, "│", DOLL_COL)

        # Knees
        set_grid(doll_kneel_y, lleg_x, "┘", JOINT_COL)
        set_grid(doll_kneel_y, rleg_x, "└", JOINT_COL)

        # Feet
        foot_y = doll_kneel_y + 1
        for fx in range(lleg_x - 2, lleg_x + 1):
            set_grid(foot_y, fx, "─", DOLL_COL)
        set_grid(foot_y, lleg_x - 3, "J", DOLL_COL)
        for fx in range(rleg_x, rleg_x + 3):
            set_grid(foot_y, fx, "─", DOLL_COL)
        set_grid(foot_y, rleg_x + 3, "L", DOLL_COL)

        # ════════════════════════════════════════════════════════════
        # 6. SECOND SHADOW HAND (fades in at chunk 2)
        # ════════════════════════════════════════════════════════════
        if second_chunk:
            ghost    = C.DIM + C.GREY
            shadow_x = cx - 22
            for ay in range(0, 3):
                set_grid(ay + bar_lift, shadow_x, "│", ghost)
            draw_text(3 + bar_lift, shadow_x - 2, "¦ ¦ ¦", ghost)
            for bx in range(shadow_x, bar_lx):
                set_grid(bar_y, bx, "·", ghost)

        # ════════════════════════════════════════════════════════════
        # 7. PYFIGLET LYRICS
        # ════════════════════════════════════════════════════════════
        chunks = [
            (0.0, ["YOU GOT", "NO CLUE"]),
            (1.0, ["HOW THEY", "CONTROL YOU."]),
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
        text_top    = rows - text_height - 1

        for y, line_str in enumerate(rendered_lines):
            text_row = text_top + y
            if 0 <= text_row < rows:
                pad = max(0, (tw - len(line_str)) // 2)
                for i, ch in enumerate(line_str):
                    px = pad + i
                    if 0 <= px < tw and ch != " ":
                        set_grid(text_row, px, ch, color)

        # ── Render ──────────────────────────────────────────────────
        top = center_v(rows + 4, th)
        out = [C.DIM + "·" * tw + C.RESET]
        out += [""] * top
        for row in grid:
            s_row = ""
            for char, col in row:
                if char != " ":
                    s_row += (col + char + C.RESET) if col else char
                else:
                    s_row += " "
            out.append(s_row)
        out += [""] * top
        out.append(C.DIM + "·" * tw + C.RESET)
        return "\n".join(out)