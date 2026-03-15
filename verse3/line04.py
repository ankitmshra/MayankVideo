#!/usr/bin/env python3
"""
verse3/line04.py
"""

import math
import random
import os
import string
import numpy as np
import cv2

from constants import *

OUT_FILE = "verse3_line04_LEADER.mp4"

CHUNKS = [
    (0.00, "I'M A BORN LEADER",             PAL['WHITE'], PAL['DKGREY']),
    (1.00, "",                              PAL['GREEN'], PAL['DKGREY']), # Custom text in phase 2
    (2.00, "ART LIKE BASQUIAT PIECES",      PAL['WHITE'], PAL['BLACK']),
]
DUR = 3.0   # total animation duration in seconds

def active_chunk(t):
    cur = CHUNKS[0]
    for ch in CHUNKS:
        if t >= ch[0]:
            cur = ch
    return cur

def new_canvas():
    return np.zeros((GH, GW, 3), dtype=np.uint8)

def spx(c, x, y, col):
    if 0 <= x < GW and 0 <= y < GH:
        c[int(y), int(x)] = col

def spx_add(c, x, y, col):
    if 0 <= x < GW and 0 <= y < GH:
        c[int(y), int(x)] = np.clip(c[int(y), int(x)].astype(int) + col, 0, 255)

def upscale(c):
    big = np.repeat(np.repeat(c, PX, axis=0), PX, axis=1)
    return cv2.cvtColor(big.astype(np.uint8), cv2.COLOR_RGB2BGR)

def draw_rect(c, x, y, w, h, col):
    y1, y2 = max(0, int(y)),   min(GH, int(y + h))
    x1, x2 = max(0, int(x)),   min(GW, int(x + w))
    if x2 > x1 and y2 > y1:
        c[y1:y2, x1:x2] = col

def draw_char(c, ch, cx, cy, col, sc=1):
    bits = FONT.get(ch.upper(), FONT.get(' ', []))
    for row, b in enumerate(bits):
        for col_i in range(5):
            # check if bit is set
            bit_set = False
            if isinstance(b, int):
                 bit_set = b & (1 << (4 - col_i))
            else:
                 if col_i < len(b) and b[col_i] == '#':
                     bit_set = True
            if bit_set:
                for dy in range(sc):
                    for dx in range(sc):
                        spx(c, cx + col_i * sc + dx, cy + row * sc + dy, col)

def text_w(txt, sc=1):
    return len(txt) * (5 * sc + sc)

def draw_text_c(c, txt, y, col, sc=1):
    tw = text_w(txt, sc)
    x = (GW - tw) // 2
    for ch in txt.upper():
        draw_char(c, ch, x, y, col, sc)
        x += 5 * sc + sc

def draw_text_shadow_c(c, txt, cy, fg, sh, sc=1):
    draw_text_c(c, txt, cy + 1 if sc == 1 else cy + 2, sh, sc)
    draw_text_c(c, txt, cy, fg, sc)

def scanlines(c, a=0.20):
    c[1::2] = (c[1::2] * (1 - a)).astype(np.uint8)

def blend_asset(c, img, cx, cy, alpha=1.0):
    if img is None: return
    bh, bw = img.shape[:2]
    x1 = int(cx - bw / 2)
    y1 = int(cy - bh / 2)
    x2 = x1 + bw
    y2 = y1 + bh

    cx1 = max(0, x1)
    cy1 = max(0, y1)
    cx2 = min(GW, x2)
    cy2 = min(GH, y2)

    if cx1 >= cx2 or cy1 >= cy2:
        return

    ix1 = cx1 - x1
    iy1 = cy1 - y1
    ix2 = ix1 + (cx2 - cx1)
    iy2 = iy1 + (cy2 - cy1)

    src = img[iy1:iy2, ix1:ix2]
    dst = c[cy1:cy2, cx1:cx2]

    if src.shape[2] == 4:
        mask = (src[:, :, 3] / 255.0) * alpha
        mask = np.stack([mask]*3, axis=-1)
        c[cy1:cy2, cx1:cx2] = (src[:, :, :3] * mask + dst * (1 - mask)).astype(np.uint8)
    else:
        c[cy1:cy2, cx1:cx2] = src

# ──────────────────────────────────────────────────────────────
# ASSETS AND STATE
# ──────────────────────────────────────────────────────────────

assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
crown_path = os.path.join(assets_dir, "crown.png")
crown_img = cv2.imread(crown_path, cv2.IMREAD_UNCHANGED)
if crown_img is not None:
    # Scale width to 80, height to 100
    crown_img = cv2.resize(crown_img, (120, 80), interpolation=cv2.INTER_AREA)
    crown_img = cv2.cvtColor(crown_img, cv2.COLOR_BGRA2RGBA)

CHARSET = string.ascii_uppercase + string.digits + "!@#$%^&*"
DECIPHER_TARGET = "STRAIGHT OUTTA THE BEST KEPT SECRET"

basquiat_canvas = np.zeros((GH, GW, 3), dtype=np.uint8)
basquiat_canvas[:] = PAL['YELLOW']
last_basquiat_t = 0

# ──────────────────────────────────────────────────────────────
# SCENE PHASES
# ──────────────────────────────────────────────────────────────

def draw_phase1_bg(c, t):
    # Empty background
    cx, cy = GW // 2, GH // 2 - 20

    # Crown (Static)
    if crown_img is not None:
        alpha = min(1.0, t * 2.5) 
        blend_asset(c, crown_img, cx, cy, alpha)


def draw_phase2_bg(c, t):
    c[:] = (0, 10, 0)
    
def draw_phase3_bg(c, t):
    global last_basquiat_t, basquiat_canvas
    local_t = t - 2.0
    
    if local_t <= 0.05:
        basquiat_canvas[:] = (200, 180, 100)
    
    if t - last_basquiat_t > 0.03:
        last_basquiat_t = t
        for _ in range(3):
            colors = [PAL['BLACK'], PAL['RED'], PAL['WHITE'], PAL['BLUE']]
            col = random.choice(colors)
            x1 = random.randint(0, GW)
            y1 = random.randint(0, GH)
            x2 = x1 + random.randint(-40, 40)
            y2 = y1 + random.randint(-40, 40)
            thickness = random.randint(1, 4)
            cv2.line(basquiat_canvas, (x1, y1), (x2, y2), col, thickness=thickness)
            
    c[:] = basquiat_canvas


# ──────────────────────────────────────────────────────────────
# MASTER FRAME RENDERER
# ──────────────────────────────────────────────────────────────

def render_frame(t):
    c = new_canvas()

    if t < 1.0:
        draw_phase1_bg(c, t)
    elif t < 2.0:
        draw_phase2_bg(c, t)
    else:
        draw_phase3_bg(c, t)

    # ── Lyric text ────────────────────────────────────────────
    t_start, text, fg, shadow = active_chunk(t)
    chunk_age = t - t_start
    flash     = chunk_age < 0.08
    scl       = 2 if len(text) > 15 else 3
    ty        = GH - 40
    
    # Custom effect for phase 2
    if t >= 1.0 and t < 2.0:
        local_t = t - 1.0
        progress = max(0.0, min(1.0, local_t * 1.5))
        display_str = ""
        for i, char in enumerate(DECIPHER_TARGET):
            if char == " ":
                display_str += " "
                continue
            char_thresh = i / len(DECIPHER_TARGET)
            if progress >= char_thresh:
                display_str += char
            else:
                display_str += random.choice(CHARSET)
        
        scl = 2
        tw = text_w(display_str, scl)
        if tw > GW - 10:
            scl = 1
        
        draw_text_shadow_c(c, display_str, GH // 2 - 10, PAL['GREEN'], PAL['DKGREY'], scl)
            
    elif t >= 2.0:
        # Phase 3 lyrics need to be very clearly evident
        scl = 3
        draw_text_shadow_c(c, text, GH // 2 + 30, fg, shadow, scl)
    else:
        # standard global text
        if flash:
            draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
        else:
            draw_text_shadow_c(c, text, ty, fg, shadow, scl)
            
        # brackets
        tw_ = text_w(text, scl)
        lx_ = (GW - tw_) // 2 - 5
        rx_ = (GW + tw_) // 2 + 1
        for bdy in range(scl * 7 + 2):
            spx(c, lx_,     ty - 1 + bdy, fg)
            spx(c, lx_ + 1, ty - 1 + bdy, fg)
            spx(c, rx_,     ty - 1 + bdy, fg)
            spx(c, rx_ + 1, ty - 1 + bdy, fg)

    scanlines(c, 0.20)
    return c

# ──────────────────────────────────────────────────────────────
# TITLE CARD FRAME
# ──────────────────────────────────────────────────────────────

def title_frame(ft):
    tc = new_canvas()
    for gy in range(GH):
        tc[gy, :] = (int(gy * 0.1), 0, 0) # dark red
        
    bord = PAL['RED'] if int(ft * 4) % 2 == 0 else PAL['DKGREY']
    draw_rect(tc, 2, 2,      GW - 4, 1,      bord)
    draw_rect(tc, 2, GH - 3, GW - 4, 1,      bord)
    draw_rect(tc, 2, 2,      1,      GH - 4, bord)
    draw_rect(tc, GW - 3, 2, 1,      GH - 4, bord)

    draw_text_shadow_c(tc, "VERSE  3",            GH // 2 - 30, PAL['RED'], PAL['DKGREY'], 4)
    draw_text_shadow_c(tc, "BORN LEADER", GH // 2 + 12, PAL['WHITE'],  PAL['GREY'],   2)

    if int(ft * 3) % 2 == 0:
        draw_rect(tc, GW // 2 - 2, GH // 2 + 32, 4, 7, PAL['WHITE'])

    scanlines(tc)
    return tc

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    import sys
    import time

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path   = os.path.join(script_dir, OUT_FILE)

    print("=" * 60)
    print("  verse3/line04 — LEADER  |  Pixel Art Retro")
    print("=" * 60)
    print(f"  Output : {out_path}")
    print(f"  Size   : {W}x{H} @ {FPS}fps")
    print()
    sys.stdout.flush()

    # ── Try to open a live preview window ────────────────────
    PREV_W, PREV_H = 960, 540
    preview_ok = False
    try:
        cv2.namedWindow("Rendering — Press Q to cancel", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Rendering — Press Q to cancel", PREV_W, PREV_H)
        preview_ok = True
        print("  Live preview window opened.")
        print("  Press Q (in the preview window) to cancel.")
    except Exception:
        print("  (Headless mode — no preview window)")
    sys.stdout.flush()

    # ── Open VideoWriter ──────────────────────────────────────
    for fourcc_str, ext in [('mp4v', '.mp4'), ('XVID', '.avi')]:
        final_path = out_path if ext == '.mp4' else out_path.replace('.mp4', '.avi')
        fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
        writer = cv2.VideoWriter(final_path, fourcc, FPS, (W, H))
        if writer.isOpened():
            out_path = final_path
            print(f"  VideoWriter opened ({fourcc_str}) → {out_path}")
            break
        writer.release()
    else:
        print()
        print("  ERROR: Could not open any VideoWriter codec.")
        return

    sys.stdout.flush()

    title_frames = int(1.5 * FPS)
    main_frames  = int(DUR * FPS)
    total_frames = title_frames + main_frames
    cancelled    = False
    start_time   = time.time()
    frame_count  = [0]

    def show_preview(bgr):
        if not preview_ok:
            return True
        if frame_count[0] % 4 != 0:          # show every 4th frame
            return True
        small = cv2.resize(bgr, (PREV_W, PREV_H), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Rendering — Press Q to cancel", small)
        key = cv2.waitKey(1) & 0xFF
        return key not in (ord('q'), ord('Q'), 27)   # ESC or Q = cancel

    def progress(f, total, label):
        pct  = int(100 * f / max(total, 1))
        done = pct // 5
        bar  = "#" * done + "-" * (20 - done)
        elapsed = time.time() - start_time
        if f > 0:
            eta = int(elapsed / f * (total - f))
            time_str = f"ETA {eta}s"
        else:
            time_str = "ETA --s"
        fps_cur = f / elapsed if elapsed > 0 else 0
        print(f"  {label} [{bar}] {pct:3d}%  {fps_cur:.1f} fps  {time_str}   ", end="\r", flush=True)

    # ── Title card ────────────────────────────────────────────
    print(f"\n  Rendering title card ({title_frames} frames)...")
    for f in range(title_frames):
        bgr = upscale(title_frame(f / FPS))
        writer.write(bgr)
        frame_count[0] += 1
        if not show_preview(bgr):
            cancelled = True
            break
        progress(f + 1, title_frames, "Title ")

    if not cancelled:
        print()
        # ── Main animation ────────────────────────────────────
        print(f"  Rendering animation ({main_frames} frames)...")
        for f in range(main_frames):
            t   = f / FPS
            bgr = upscale(render_frame(t))
            writer.write(bgr)
            frame_count[0] += 1
            if not show_preview(bgr):
                cancelled = True
                break
            progress(f + 1, main_frames, "Anim  ")
        print()

    writer.release()
    if preview_ok:
        cv2.destroyAllWindows()

    if cancelled:
        print("\n  Cancelled by user.")
        return

    elapsed = time.time() - start_time
    size_mb = os.path.getsize(out_path) / 1_000_000

    print()
    print("=" * 60)
    print(f"  DONE in {elapsed:.1f}s")
    print(f"  File : {out_path}  ({size_mb:.1f} MB)")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
