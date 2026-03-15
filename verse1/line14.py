"""
Line14 — "I avoid news like the flu" / "Feeding information which is not true"
Effect: PROPAGANDA OVERLOAD — dense TV static floods the screen, corrupt news
        tickers crawl across, glitch bars tear the image, a ghost anchor sits
        behind the text, and binary rain bleeds down the edges. Pyfiglet lyrics
        cut through like an emergency broadcast.
"""
import math
import random
import pyfiglet
from common import C, LineAnimator, center_v

_rng   = random.Random(55)
_rng2  = random.Random(13)

# ── Character pools ────────────────────────────────────────────────────────────
STATIC       = list("▓▒░█▄▀■□▪▫:;.,·~%@#&")
BINARY       = list("01")
GLITCH_CHARS = list("╬╪╫╞╡╤╧╥╨╦╩╠╣║═╔╗╚╝")
NEWS_WORDS   = [
    "BREAKING", "ALERT", "LIVE", "EXCLUSIVE", "UNVERIFIED",
    "SOURCES SAY", "DEVELOPING", "CRISIS", "UPDATE", "PROPAGANDA",
    "SPONSORED", "NOT TRUE", "DISTRACTION", "CONTROL", "OBEY",
]

# Pre-generate static pixel seed table for deterministic noise per cell
_NOISE_TABLE = [_rng2.random() for _ in range(300 * 80)]

# Pre-bake ticker content
_TICKER = "  ★  " + "  ◆  ".join(NEWS_WORDS) + "  ★  "
_TICKER = (_TICKER * 6)[:300]   # long enough for any terminal width

# ASCII anchor figure (sits behind text like a ghost)
ANCHOR = [
    r"  .--.  ",
    r" ( •• ) ",
    r"  \__/  ",
    r"  |  |  ",
    r" _|__|_ ",
    r"|______|",
]


class Line14(LineAnimator):
    FPS = 60   # ← 60 fps

    def frame(self, text, color, t, tw, th):
        rows = 28
        grid = [[(" ", "")] * tw for _ in range(rows)]

        def set_grid(gy, gx, gchar, gcol):
            if 0 <= gy < rows and 0 <= gx < tw:
                grid[gy][gx] = (gchar, gcol)

        # ── 1. Base static noise ───────────────────────────────────────────
        noise_intensity = 0.30 + 0.12 * math.sin(t * 9)
        for r in range(rows):
            for c in range(tw):
                idx = (r * 80 + c) % len(_NOISE_TABLE)
                # Offset by time bucket so noise shifts every ~0.05 s
                bucket = int(t * 20)
                val = _NOISE_TABLE[(idx + bucket * 37) % len(_NOISE_TABLE)]
                if val < noise_intensity:
                    ch  = STATIC[int(val * len(STATIC) * (1 / noise_intensity)) % len(STATIC)]
                    col = C.DIM + C.GREY
                    set_grid(r, c, ch, col)

        # ── 2. Binary rain columns on left & right edges ───────────────────
        for col_x in list(range(0, 6)) + list(range(tw - 6, tw)):
            for r in range(rows):
                drop = int((t * 12 + col_x * 7 + r * 3)) % (rows * 2)
                if drop < rows:
                    ry = (r + int(t * 14 + col_x * 5)) % rows
                    ch = BINARY[int(t * 20 + r + col_x) % 2]
                    brightness = 1 - abs(ry - rows // 2) / (rows // 2 + 1)
                    col = C.GREEN if brightness > 0.5 else C.DIM + C.GREEN
                    set_grid(ry, col_x, ch, col)

        # ── 3. Glitch horizontal tear bars ────────────────────────────────
        n_glitch = 3
        for g in range(n_glitch):
            bar_y = int((t * (5 + g * 2.3) + g * rows / n_glitch) % rows)
            bar_w = int(tw * (0.3 + 0.2 * math.sin(t * 7 + g)))
            bar_x = int((t * 40 * (g % 2 == 0 and 1 or -1) + g * 30) % tw)
            for dx in range(bar_w):
                bx = (bar_x + dx) % tw
                ch = GLITCH_CHARS[int(t * 30 + dx + g * 11) % len(GLITCH_CHARS)]
                col = [C.RED, C.CYAN, C.MAGENTA][g % 3]
                set_grid(bar_y, bx, ch, C.DIM + col)

        # ── 4. Horizontal scan line ────────────────────────────────────────
        scan_y = int((t * 8) % rows)
        for c in range(tw):
            set_grid(scan_y, c, "─", C.DIM + C.WHITE)

        # ── 5. Crawling news ticker (bottom two rows) ──────────────────────
        ticker_offset = int(t * 30) % len(_TICKER)
        ticker_row1   = rows - 2
        ticker_row2   = rows - 1
        # Ticker background bar
        for c in range(tw):
            set_grid(ticker_row1, c, "▄", C.DIM + C.RED)
            set_grid(ticker_row2, c, " ", C.DIM + C.RED)
        # Ticker text
        for c in range(tw):
            ch = _TICKER[(ticker_offset + c) % len(_TICKER)]
            col = C.WHITE if ch not in (" ", "★", "◆") else C.YELLOW
            set_grid(ticker_row2, c, ch, col)

        # ── 6. Ghost anchor figure (centred, dimly behind text) ───────────
        anchor_cx = tw // 2 - len(ANCHOR[0]) // 2
        anchor_cy = (rows - len(ANCHOR)) // 2 - 1
        for ay, aline in enumerate(ANCHOR):
            for ax, ach in enumerate(aline):
                gx = anchor_cx + ax
                gy = anchor_cy + ay
                if ach != " " and 0 <= gx < tw and 0 <= gy < rows:
                    set_grid(gy, gx, ach, C.DIM + C.GREY)

        # ── 7. Pyfiglet lyrics ─────────────────────────────────────────────
        chunks = [
            (0.0, ["I AVOID", "NEWS"]),
            (0.7, ["LIKE THE", "FLU"]),
            (1.3, ["FEEDING", "INFO"]),
            (1.9, ["WHICH IS", "NOT TRUE"]),
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

        text_height  = len(rendered_lines)
        start_y      = max(0, (rows - text_height) // 2)
        max_line_len = max((len(l) for l in rendered_lines), default=0)
        box_pad      = max(0, (tw - max_line_len) // 2)

        # Clear clean rectangle behind the text
        for r in range(max(0, start_y - 1), min(rows - 2, start_y + text_height + 1)):
            for c in range(max(0, box_pad - 2), min(tw, box_pad + max_line_len + 2)):
                set_grid(r, c, " ", None)

        # Signal strength flicker — text flashes between full color and dim
        signal = 0.65 + 0.35 * math.sin(t * 13)
        text_col = color if signal > 0.55 else C.GREY

        for y, text_line_str in enumerate(rendered_lines):
            text_row = start_y + y
            if 0 <= text_row < rows:
                target_pad = max(0, (tw - len(text_line_str)) // 2)
                for i, ch in enumerate(text_line_str):
                    px = target_pad + i
                    if 0 <= px < tw:
                        if ch != " ":
                            set_grid(text_row, px, ch, text_col)
                        else:
                            set_grid(text_row, px, " ", None)

        # ── 8. "LIVE" badge top-left ───────────────────────────────────────
        live_blink = int(t * 2) % 2 == 0
        if live_blink:
            for bx, bch in enumerate("● LIVE"):
                set_grid(0, bx + 1, bch, C.RED + C.BOLD)

        # ── Render ─────────────────────────────────────────────────────────
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