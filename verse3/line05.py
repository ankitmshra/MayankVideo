#!/usr/bin/env python3
"""
verse3/line05.py
"""

import math
import os
import numpy as np
import cv2

from constants import *

OUT_FILE = "verse3_line05_DIAMONDS.mp4"

CHUNKS = [
    (0.00, "DIAMONDS IN MY CEILING",       PAL['LTCYAN'], PAL['DKBLUE']),
    (1.50, "IRONY OF A MAN WITH FEELINGS", PAL['WHITE'],  PAL['DKGREY']),
    (2.50, "GOT A CAROUSEL FULL OF DREAMS AND", PAL['LTCYAN'], PAL['DKBLUE']),
    (3.50, "A ROLLER COASTER FULL OF HEATERS", PAL['WHITE'], PAL['DKGREY']),
    (4.50, "ALL OF MY HOMIES ARE WINNERS", PAL['LTCYAN'], PAL['DKBLUE']),
    (5.50, "FUCK THE POLICE THEY CAN'T REACH US.", PAL['WHITE'], PAL['DKGREY']),
]
DUR = 7.0   # total animation duration in seconds

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

# ──────────────────────────────────────────────────────────────
# 3D DIAMOND
# ──────────────────────────────────────────────────────────────

class Diamond3D:
    def __init__(self):
        # 3D Coordinates
        self.points = []
        r_table = 35
        y_table = -50
        
        r_girdle = 75
        y_girdle = -15
        
        y_culet = 75
        
        # 8-sided diamond
        sides = 8
        
        # Table vertices (0 to 7)
        for i in range(sides):
            a = i * 2 * math.pi / sides
            self.points.append((math.cos(a)*r_table, y_table, math.sin(a)*r_table))
            
        # Girdle vertices (8 to 15)
        # Offset slightly for faceting
        for i in range(sides):
            a = i * 2 * math.pi / sides + (math.pi / sides)
            self.points.append((math.cos(a)*r_girdle, y_girdle, math.sin(a)*r_girdle))
            
        # Culet (Bottom tip) (16)
        self.points.append((0, y_culet, 0))
        
        self.edges = []
        # Table edges
        for i in range(sides):
            self.edges.append((i, (i+1)%sides))
        # Girdle edges
        for i in range(sides):
            self.edges.append((i+sides, ((i+1)%sides)+sides))
        # Table to Girdle
        for i in range(sides):
            self.edges.append((i, i+sides))
            # Cross facet
            prev_girdle = ((i-1)%sides)+sides
            self.edges.append((i, prev_girdle))
        # Girdle to Culet
        for i in range(sides):
            self.edges.append((i+sides, 16))
            
        self.cx = GW // 2
        self.cy = GH // 2 - 10
        self.focal = 300

    def draw(self, c, t):
        rot_y = t * 2.5 # fast rotate
        tilt_x = 0.2    # Slight down tilt to see table
        
        projected = []
        # Rotate and project points
        for x3, y3, z3 in self.points:
            # Y Axis rot
            x2 = x3 * math.cos(rot_y) + z3 * math.sin(rot_y)
            z2 = -x3 * math.sin(rot_y) + z3 * math.cos(rot_y)
            y2 = y3
            
            # X Axis rot (tilt)
            y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
            z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
            x3_ = x2
            
            depth = z3_ + 250
            if depth < 1: depth = 1
            
            sx = int(self.cx + x3_ / depth * self.focal)
            sy = int(self.cy + y3_ / depth * self.focal)
            projected.append((sx, sy, depth, x3_)) # x3_ holds local x position to detect glint

        # Sort edges by average Z depth so back lines are drawn first (and darker)
        depth_edges = []
        for e in self.edges:
            p1, p2 = e
            avg_z = (projected[p1][2] + projected[p2][2]) / 2.0
            depth_edges.append((avg_z, p1, p2))
            
        depth_edges.sort(reverse=True)
            
        # Draw edges
        for z, p1, p2 in depth_edges:
            sx1, sy1, _, _ = projected[p1]
            sx2, sy2, _, _ = projected[p2]
            
            # If Z > 250 it is in back, if < 250 it is in front
            is_front = z < 250
            
            if is_front:
                color = PAL['LTCYAN']
                thickness = 2
            else:
                color = PAL['DKBLUE']
                thickness = 1
                
            cv2.line(c, (sx1, sy1), (sx2, sy2), color, thickness)
            
        # Add Glints
        # Glints occur on vertices that are crossing exactly the front center
        # i.e z is small, and local x is near 0.
        for sx, sy, depth, lx in projected:
            if depth < 250 and abs(lx) < 5:
                # Big flash
                flash_str = max(0, 1.0 - abs(lx)/5.0)
                # Outer glow
                radius = int(flash_str * 30)
                if radius > 0:
                    for r in range(radius, 0, -3):
                        gc = tuple(int(PAL['WHITE'][k] * flash_str * (r/radius) * 0.4) for k in range(3))
                        cv2.circle(c, (sx, sy), r, gc, -1)
                        # Star shape
                        cv2.line(c, (sx-r, sy), (sx+r, sy), PAL['WHITE'], 1)
                        cv2.line(c, (sx, sy-r), (sx, sy+r), PAL['WHITE'], 1)
                        spx(c, sx, sy, PAL['WHITE'])

# ──────────────────────────────────────────────────────────────
# 3D CAROUSEL
# ──────────────────────────────────────────────────────────────

class Carousel3D:
    def __init__(self):
        self.points = []
        r_top = 70
        y_top = -60

        r_base = 75
        y_base = 50

        y_roof_peak = -90

        sides = 8
        
        # Canopy Base (0..7)
        for i in range(sides):
            a = i * 2 * math.pi / sides
            self.points.append((math.cos(a)*r_top, y_top, math.sin(a)*r_top))
            
        # Roof Peak (8)
        self.points.append((0, y_roof_peak, 0))
        
        # Floor (9..16)
        for i in range(sides):
            a = i * 2 * math.pi / sides
            self.points.append((math.cos(a)*r_base, y_base, math.sin(a)*r_base))
            
        # Central Pillar top (17), bot (18)
        self.points.append((0, y_top, 0))
        self.points.append((0, y_base, 0))

        self.edges = []
        # Canopy rim
        for i in range(sides):
            self.edges.append((i, (i+1)%sides))
        # Canopy to roof
        for i in range(sides):
            self.edges.append((i, 8))
        # Floor rim
        for i in range(sides):
            self.edges.append((i+9, ((i+1)%sides)+9))
        
        # Poles (from canopy to floor)
        for i in range(sides):
            self.edges.append((i, i+9))
            
        # Center pillar
        self.edges.append((17, 18))

        self.cx = GW // 2
        self.cy = GH // 2 - 10
        self.focal = 300

    def draw(self, c, t):
        rot_y = t * 1.5 # slower gentle rotation
        tilt_x = 0.2
        
        projected = []
        for x3, y3, z3 in self.points:
            x2 = x3 * math.cos(rot_y) + z3 * math.sin(rot_y)
            z2 = -x3 * math.sin(rot_y) + z3 * math.cos(rot_y)
            y2 = y3
            
            y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
            z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
            x3_ = x2
            
            depth = z3_ + 250
            if depth < 1: depth = 1
            
            sx = int(self.cx + x3_ / depth * self.focal)
            sy = int(self.cy + y3_ / depth * self.focal)
            projected.append((sx, sy, depth, x3_))

        depth_edges = []
        for e in self.edges:
            p1, p2 = e
            avg_z = (projected[p1][2] + projected[p2][2]) / 2.0
            depth_edges.append((avg_z, p1, p2))
            
        depth_edges.sort(reverse=True)
            
        for z, p1, p2 in depth_edges:
            sx1, sy1, _, _ = projected[p1]
            sx2, sy2, _, _ = projected[p2]
            
            is_front = z < 250
            if is_front:
                color = PAL['LTCYAN']
                thickness = 2
            else:
                color = PAL['DKBLUE']
                thickness = 1
                
            cv2.line(c, (sx1, sy1), (sx2, sy2), color, thickness)
            
            # Draw decorative "horses" at the midpoints of the front poles
            if is_front and p1 < 8 and p2 >= 9 and p2 < 17:
                mx = (sx1 + sx2) // 2
                my = (sy1 + sy2) // 2
                bounce = int(math.sin(t * 8 + p1) * 10)
                # simple diamond shape for horse
                cv2.circle(c, (mx, my + bounce), 4, PAL['WHITE'], -1)

# ──────────────────────────────────────────────────────────────
# 3D PODIUM
# ──────────────────────────────────────────────────────────────

class Podium3D:
    def __init__(self):
        self.points = []
        sides = 8
        
        rings_def = [
            (-40, 30), # 0: Top tier top
            (0, 30),   # 1: Top tier bot
            (0, 60),   # 2: Mid tier top
            (40, 60),  # 3: Mid tier bot
            (40, 90),  # 4: Base tier top
            (80, 90)   # 5: Base tier bot
        ]
        
        for y, r in rings_def:
            for i in range(sides):
                a = i * 2 * math.pi / sides
                self.points.append((math.cos(a)*r, y, math.sin(a)*r))
                
        self.edges = []
        
        # Horizontal rings
        for r_idx in range(6):
            start = r_idx * sides
            for i in range(sides):
                self.edges.append((start + i, start + ((i+1)%sides)))
                
        # Vertical walls
        for pair in [(0,1), (2,3), (4,5)]:
            top_start = pair[0] * sides
            bot_start = pair[1] * sides
            for i in range(sides):
                self.edges.append((top_start + i, bot_start + i))
                
        # Horizontal Steps
        for pair in [(1,2), (3,4)]:
            inner_start = pair[0] * sides
            outer_start = pair[1] * sides
            for i in range(sides):
                self.edges.append((inner_start + i, outer_start + i))
                
        self.cx = GW // 2
        self.cy = GH // 2 - 10
        self.focal = 300

    def draw(self, c, t):
        rot_y = t * 1.5 # rotate speed
        tilt_x = 0.2
        
        projected = []
        for x3, y3, z3 in self.points:
            x2 = x3 * math.cos(rot_y) + z3 * math.sin(rot_y)
            z2 = -x3 * math.sin(rot_y) + z3 * math.cos(rot_y)
            y2 = y3
            
            y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
            z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
            x3_ = x2
            
            depth = z3_ + 250
            if depth < 1: depth = 1
            
            sx = int(self.cx + x3_ / depth * self.focal)
            sy = int(self.cy + y3_ / depth * self.focal)
            projected.append((sx, sy, depth, x3_))

        depth_edges = []
        for e in self.edges:
            p1, p2 = e
            avg_z = (projected[p1][2] + projected[p2][2]) / 2.0
            depth_edges.append((avg_z, p1, p2))
            
        depth_edges.sort(reverse=True)
            
        for z, p1, p2 in depth_edges:
            sx1, sy1, _, _ = projected[p1]
            sx2, sy2, _, _ = projected[p2]
            
            is_front = z < 250
            if is_front:
                color = PAL['LTCYAN']
                thickness = 2
            else:
                color = PAL['DKBLUE']
                thickness = 1
                
            cv2.line(c, (sx1, sy1), (sx2, sy2), color, thickness)

# ──────────────────────────────────────────────────────────────
# 3D POLICE SIREN
# ──────────────────────────────────────────────────────────────

class Siren3D:
    def __init__(self):
        self.points = []
        sides = 12
        
        rings_def = [
            (-60, 20), # 0: Dome peak
            (-20, 50), # 1: Dome curve
            (20, 60),  # 2: Dome base
            (30, 65),  # 3: Mount rim
            (40, 65)   # 4: Mount base
        ]
        
        for y, r in rings_def:
            for i in range(sides):
                a = i * 2 * math.pi / sides
                self.points.append((math.cos(a)*r, y, math.sin(a)*r))
                
        self.edges = []
        
        # Horizontal rings
        for r_idx in range(5):
            start = r_idx * sides
            for i in range(sides):
                self.edges.append((start + i, start + ((i+1)%sides)))
                
        # Vertical walls
        for r_idx in range(4):
            top_start = r_idx * sides
            bot_start = (r_idx+1) * sides
            for i in range(sides):
                self.edges.append((top_start + i, bot_start + i))
                
        # Inner rotating light bulb
        self.bulb_idx = len(self.points)
        for i in range(4):
            a = i * 2 * math.pi / 4
            self.points.append((math.cos(a)*10, 0, math.sin(a)*10))
            self.points.append((math.cos(a)*10, 20, math.sin(a)*10))
            self.edges.append((self.bulb_idx + i*2, self.bulb_idx + i*2 + 1))
            
        self.cx = GW // 2
        self.cy = GH // 2 - 10
        self.focal = 300

    def draw(self, c, t):
        rot_y = t * 6.0 # Fast rotation for siren light beam
        tilt_x = 0.3
        
        projected = []
        for i, (x3, y3, z3) in enumerate(self.points):
            # Bulb rotates fast, shell rotates slow
            if i >= self.bulb_idx:
                x2 = x3 * math.cos(rot_y*2) + z3 * math.sin(rot_y*2)
                z2 = -x3 * math.sin(rot_y*2) + z3 * math.cos(rot_y*2)
            else:
                x2 = x3 * math.cos(rot_y*0.2) + z3 * math.sin(rot_y*0.2)
                z2 = -x3 * math.sin(rot_y*0.2) + z3 * math.cos(rot_y*0.2)
                
            y2 = y3
            
            y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
            z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
            x3_ = x2
            
            depth = z3_ + 250
            if depth < 1: depth = 1
            
            sx = int(self.cx + x3_ / depth * self.focal)
            sy = int(self.cy + y3_ / depth * self.focal)
            projected.append((sx, sy, depth, x3_))

        depth_edges = []
        for e in self.edges:
            p1, p2 = e
            avg_z = (projected[p1][2] + projected[p2][2]) / 2.0
            depth_edges.append((avg_z, p1, p2))
            
        depth_edges.sort(reverse=True)
            
        # Flashing color logic
        flash_red = math.sin(t * 15) > 0
        front_color = PAL['RED'] if flash_red else PAL['BLUE']
        back_color  = (40, 0, 0) if flash_red else (0, 0, 40)
            
        for z, p1, p2 in depth_edges:
            sx1, sy1, _, _ = projected[p1]
            sx2, sy2, _, _ = projected[p2]
            
            is_front = z < 250
            if is_front:
                color = front_color
                thickness = 2
            else:
                color = back_color
                thickness = 1
                
            cv2.line(c, (sx1, sy1), (sx2, sy2), color, thickness)
            
        # Draw huge screen tint glow based on the light bounds
        glow_color = (60, 0, 0) if flash_red else (0, 0, 60)
        c[:] = np.clip(c.astype(int) + glow_color, 0, 255).astype(np.uint8)

# ──────────────────────────────────────────────────────────────
# MASTER FRAME RENDERER
# ──────────────────────────────────────────────────────────────

def render_frame(t, diamond, carousel, podium, siren):
    c = new_canvas()

    # Background pulsing deep blue void
    pulse = (math.sin(t * 5) + 1) * 0.5
    for gy in range(GH):
        b = int(10 + gy * 0.1 + pulse * 10)
        c[gy, :] = (0, 0, min(255, b)) # dark blue

    # Subject
    if t < 2.50:
        diamond.draw(c, t)
    elif t < 4.50:
        carousel.draw(c, t)
    elif t < 5.50:
        podium.draw(c, t)
    else:
        siren.draw(c, t)

    # ── Lyric text ────────────────────────────────────────────
    t_start, text, fg, shadow = active_chunk(t)
    chunk_age = t - t_start
    flash     = chunk_age < 0.08
    scl       = 2 if len(text) > 15 else 3
    ty        = GH - 35
    
    if flash:
        draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
    else:
        draw_text_shadow_c(c, text, ty, fg, shadow, scl)
        
    scanlines(c, 0.20)
    return c

# ──────────────────────────────────────────────────────────────
# TITLE CARD FRAME
# ──────────────────────────────────────────────────────────────

def title_frame(ft, diamond):
    tc = new_canvas()
    for gy in range(GH):
        tc[gy, :] = (0, int(gy * 0.1), int(gy * 0.2))
        
    diamond.draw(tc, ft * 0.2) # slow rotate
        
    bord = PAL['LTCYAN'] if int(ft * 4) % 2 == 0 else PAL['DKGREY']
    draw_rect(tc, 2, 2,      GW - 4, 1,      bord)
    draw_rect(tc, 2, GH - 3, GW - 4, 1,      bord)
    draw_rect(tc, 2, 2,      1,      GH - 4, bord)
    draw_rect(tc, GW - 3, 2, 1,      GH - 4, bord)

    draw_text_shadow_c(tc, "VERSE  3",            GH // 2 - 30, PAL['LTCYAN'], PAL['DKBLUE'], 4)
    draw_text_shadow_c(tc, "DIAMONDS",            GH // 2 + 12, PAL['WHITE'],  PAL['GREY'],   2)

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
    print("  verse3/line05 — DIAMONDS  |  Pixel Art Retro")
    print("=" * 60)
    print(f"  Output : {out_path}")
    print(f"  Size   : {W}x{H} @ {FPS}fps")
    print()
    sys.stdout.flush()
    
    diamond = Diamond3D()
    carousel = Carousel3D()
    podium = Podium3D()
    siren = Siren3D()

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
    start_time   = time.time()

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
        bgr = upscale(title_frame(f / FPS, diamond))
        writer.write(bgr)
        progress(f + 1, title_frames, "Title ")

    print()
    # ── Main animation ────────────────────────────────────
    print(f"  Rendering animation ({main_frames} frames)...")
    for f in range(main_frames):
        t   = f / FPS
        bgr = upscale(render_frame(t, diamond, carousel, podium, siren))
        writer.write(bgr)
        progress(f + 1, main_frames, "Anim  ")
    print()

    writer.release()

    elapsed = time.time() - start_time
    size_mb = os.path.getsize(out_path) / 1_000_000

    print()
    print("=" * 60)
    print(f"  DONE in {elapsed:.1f}s")
    print(f"  File : {out_path}  ({size_mb:.1f} MB)")
    print("=" * 60)

if __name__ == "__main__":
    main()
