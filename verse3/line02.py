#!/usr/bin/env python3
import math
import random
import os
import numpy as np
import cv2

from constants import *

OUT_FILE = "verse3_line02_SUN.mp4"

CHUNKS = [
    (0.00, "ONCE FLEW CLOSE",    PAL['LTCYAN'], PAL['BLUE']),
    (0.50, "TO THE SUN",         PAL['YELLOW'], PAL['ORANGE']),
    (0.90, "GOT MY WINGS BURNT", PAL['WHITE'],  PAL['RED']),
    (1.40, "HAD TO BECOME BRUTUS",      PAL['LTCYAN'], PAL['BLUE']),
    (2.10, "HAD TO KILL THE KING",        PAL['WHITE'],  PAL['DKGREY']),
]
DUR = 2.8

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
        c[y, x] = col

def spx_add(c, x, y, col):
    if 0 <= x < GW and 0 <= y < GH:
        c[y, x] = np.clip(c[y, x].astype(int) + col, 0, 255)

def upscale(c):
    big = np.repeat(np.repeat(c, PX, axis=0), PX, axis=1)
    return cv2.cvtColor(big.astype(np.uint8), cv2.COLOR_RGB2BGR)

def draw_rect(c, x, y, w, h, col):
    y1, y2 = max(0, y),   min(GH, y + h)
    x1, x2 = max(0, x),   min(GW, x + w)
    if x2 > x1 and y2 > y1:
        c[y1:y2, x1:x2] = col

def draw_char(c, ch, cx, cy, col, sc=1):
    bits = FONT.get(ch.upper(), FONT[' '])
    for row, b in enumerate(bits):
        for col_i in range(5):
            if b & (1 << (4 - col_i)):
                for dy in range(sc):
                    for dx in range(sc):
                        spx(c, cx + col_i * sc + dx, cy + row * sc + dy, col)

def text_w(txt, sc=1):
    return len(txt) * (5 * sc + sc)

def draw_text_c(c, txt, cy, col, sc=1):
    tw = text_w(txt, sc)
    x  = (GW - tw) // 2
    for ch in txt.upper():
        draw_char(c, ch, x, cy, col, sc)
        x += 5 * sc + sc

def draw_text_shadow_c(c, txt, cy, fg, sh, sc=1):
    draw_text_c(c, txt, cy + 1, sh, sc)
    draw_text_c(c, txt, cy,     fg, sc)

def scanlines(c, a=0.20):
    c[1::2] = (c[1::2] * (1 - a)).astype(np.uint8)

def draw_background(c, t):
    for gy in range(GH):
        frac = gy / GH
        r = int(10 + frac * 20)
        g = int(0 + frac * 5)
        b = int(10 + frac * 20 + math.sin(t * 0.3) * 4)
        c[gy, :] = (min(255, r), min(255, g), min(255, b))

class WarpTunnel:
    N     = 600
    FOCAL = 180
    SPEED = 50

    def __init__(self, seed=7):
        rng = np.random.default_rng(seed)
        self.x      = rng.uniform(-300, 300, self.N)
        self.y      = rng.uniform(-200, 200, self.N)
        self.base_z = rng.uniform(1, 1000, self.N)
        self.stype  = rng.integers(0, 4, self.N)

    def draw(self, c, t, speed_mul=1.0):
        cx, cy = GW // 2, GH // 2
        zoom = max(0.01, 1.0 - (t / 1.0)) 
        
        z_shift = (t * self.SPEED * speed_mul * (1 + t * 5)) % 1000
        z = ((self.base_z - z_shift - 1) % 999) + 1

        order = np.argsort(z)[::-1]
        COLS  = [PAL['STARDIM'], PAL['STARBRT'], PAL['STARBLUE'], PAL['STARGOLD']]

        for i in order:
            zi = z[i] * zoom
            if zi < 0.1: zi = 0.1
            sx = int(cx + self.x[i] / zi * self.FOCAL)
            sy = int(cy + self.y[i] / zi * self.FOCAL)
            if not (0 <= sx < GW and 0 <= sy < GH):
                continue

            depth_frac = 1.0 - zi / 1000.0
            if depth_frac < 0: depth_frac = 0
            col        = COLS[self.stype[i]]
            brightness = depth_frac ** 1.5
            col_s      = tuple(int(col[k] * brightness) for k in range(3))

            spx(c, sx, sy, col_s)
            if depth_frac > 0.7:
                spx(c, sx + 1, sy, col_s)
                spx(c, sx, sy + 1, col_s)
                
class ZoomingGalaxy:
    N_ARM  = 280
    N_HALO = 120
    TILT   = 0.38
    FOCAL  = 300

    def __init__(self, seed=42):
        rng   = np.random.default_rng(seed)
        stars = []

        for arm in range(2):
            arm_off = arm * math.pi
            for i in range(self.N_ARM):
                frac    = i / self.N_ARM
                r       = 2 + frac * 90
                theta   = frac * 4.5 * math.pi + arm_off
                scatter = rng.uniform(0, 6) * (1 + frac)
                r      += rng.normal(0, scatter * 0.3)
                theta  += rng.normal(0, 0.15)

                x3 = r * math.cos(theta)
                y3 = r * math.sin(theta) * 0.18
                z3 = r * math.sin(theta) * 0.95

                brt = min(1.3, 0.3 + 0.7 * (1 - frac) + rng.uniform(0, 0.3))
                ct  = (3 if frac < 0.2
                       else int(rng.choice([1, 2, 3])) if frac < 0.5
                       else int(rng.choice([1, 2])))
                stars.append((x3, y3, z3, brt, ct))

        for _ in range(self.N_HALO):
            r     = rng.uniform(60, 120)
            theta = rng.uniform(0, 2 * math.pi)
            phi   = rng.uniform(0, 2 * math.pi)
            x3 = r * math.cos(theta) * math.cos(phi)
            y3 = r * math.sin(phi) * 0.4
            z3 = r * math.sin(theta) * math.cos(phi)
            stars.append((x3, y3, z3, rng.uniform(0.1, 0.35), 0))

        self.stars = stars
        self.cx    = GW // 2
        self.cy    = GH // 2

    def _project(self, x3, y3, z3, rot_y, tilt_x, zoom):
        x2 =  x3 * math.cos(rot_y) + z3 * math.sin(rot_y)
        z2 = -x3 * math.sin(rot_y) + z3 * math.cos(rot_y)
        y2 = y3
        y3_ = y2 * math.cos(tilt_x) - z2 * math.sin(tilt_x)
        z3_ = y2 * math.sin(tilt_x) + z2 * math.cos(tilt_x)
        x3_ = x2
        
        depth = (z3_ + 300) * zoom
        if depth < 0.1:
            depth = 0.1
        sx = self.cx + int(x3_ / depth * self.FOCAL)
        sy = self.cy + int(y3_ / depth * self.FOCAL)
        return sx, sy, depth

    def draw(self, c, t):
        if t > 1.2:
            return 
        
        zoom = 1.0
        if t <= 1.0:
            zoom = max(0.01, 1.0 - (t / 1.0))
        else:
            zoom = 0.01
            
        rot_y  = t * 2.0  
        tilt_x = self.TILT
        COLS   = [PAL['STARDIM'], PAL['STARBRT'], PAL['STARBLUE'], PAL['STARGOLD']]

        projected = []
        for x3, y3, z3, brt, ct in self.stars:
            sx, sy, depth = self._project(x3, y3, z3, rot_y, tilt_x, zoom)
            projected.append((depth, sx, sy, brt, ct))
        projected.sort(reverse=True)

        for depth, sx, sy, brt, ct in projected:
            if not (0 <= sx < GW and 0 <= sy < GH):
                continue
            col   = COLS[ct]
            col_s = tuple(min(255, int(col[k] * brt)) for k in range(3))
            spx(c, sx, sy, col_s)
            scale_star = 1
            if zoom < 0.5: scale_star = 2
            if zoom < 0.2: scale_star = 3
            if brt > 0.8:
                for kx in range(scale_star):
                    for ky in range(scale_star):
                        spx(c, sx + kx, sy + ky, col_s)

        cx_s, cy_s, _ = self._project(0, 0, 0, rot_y, tilt_x, zoom)
        
        if zoom < 0.1: return
        
        core_rings = [
            (int(20 / zoom), PAL['WHITE']),
            (int(14 / zoom), PAL['GOLD']),
            (int(8 / zoom),  PAL['YELLOW']),
            (int(4 / zoom),  PAL['WHITE']),
        ]
        
        for r, col in core_rings:
            for a_step in range(max(16, int(32 / zoom))):
                a = a_step * math.pi * 2 / max(16, int(32 / zoom))
                for ri in range(0, r, 2): 
                    frac = 1 - ri / r
                    px_  = cx_s + int(math.cos(a) * ri)
                    py_  = cy_s + int(math.sin(a) * ri * 0.5)
                    gc   = tuple(int(col[k] * frac * 0.2) for k in range(3))
                    spx_add(c, px_, py_, gc)

class BurningSun:
    def __init__(self):
        self.cx = GW // 2
        self.cy = GH // 2
        
    def draw(self, c, t):
        if t < 0.5:
            return
            
        alpha_mult = 1.0
        if t < 1.0:
            scale = (t - 0.5) / 0.5
            r_base = 20 + int(70 * scale)
        else:
            r_base = 90 + int(math.sin(t * 15) * 4) + int(math.cos(t * 23) * 3)

        r = r_base

        for dy in range(-r - 20, r + 21, 2):
            for dx in range(-r - 20, r + 21, 2):
                d2 = dx*dx + dy*dy
                if d2 < r*r:
                    dist = math.sqrt(d2) / r
                    if dist < 0.4:
                        col = PAL['WHITE']
                    elif dist < 0.7:
                        col = PAL['YELLOW']
                    elif dist < 0.9:
                        col = PAL['GOLD']
                    else:
                        col = PAL['ORANGE']
                    
                    spx(c, self.cx + dx, self.cy + dy, col)
                    spx(c, self.cx + dx + 1, self.cy + dy, col)
                    spx(c, self.cx + dx, self.cy + dy + 1, col)
                    spx(c, self.cx + dx + 1, self.cy + dy + 1, col)
                elif d2 < (r + 20)**2:
                    ang = math.atan2(dy, dx)
                    noise = (math.sin(ang * 8 + t * 30) + math.cos(ang * 5 - t * 20)) * 0.5
                    dist = math.sqrt(d2)
                    fire_r = r + 5 + noise * 15
                    
                    if dist < fire_r:
                        dropoff = 1.0 - (dist - r) / (fire_r - r)
                        flicker = 0.5 + 0.5 * math.sin(t * 40 + dx * dy)
                        intensity = dropoff * flicker * alpha_mult
                        
                        if intensity > 0.6:
                            fc = PAL['YELLOW']
                        elif intensity > 0.3:
                            fc = PAL['ORANGE']
                        else:
                            fc = PAL['RED']
                        
                        if intensity > 0.1:
                            fc_int = tuple(int(fc[k] * intensity) for k in range(3))
                            spx_add(c, self.cx + dx, self.cy + dy, fc_int)
                            spx_add(c, self.cx + dx + 1, self.cy + dy, fc_int)
                            spx_add(c, self.cx + dx, self.cy + dy + 1, fc_int)
                            spx_add(c, self.cx + dx + 1, self.cy + dy + 1, fc_int)

def render_frame(t, warp, galaxy, sun):
    c = new_canvas()

    draw_background(c, t)
    warp.draw(c, t, speed_mul=1.0 + t * 5.0)
    galaxy.draw(c, t)
    sun.draw(c, t)

    # ── Lyric text ────────────────────────────────────────────
    t_start, text, fg, shadow = active_chunk(t)
    chunk_age = t - t_start
    flash     = chunk_age < 0.08
    scl       = 4 if len(text) <= 8 else (3 if len(text) <= 12 else 2)
    scl       = min(scl, 3) 
    ty        = GH - 40

    if t < 2.6:
        if flash:
            draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
        else:
            draw_text_shadow_c(c, text, ty, fg, shadow, scl)

    # Blood red wipe transition at the end
    if t >= 2.6:
        duration = 0.2
        progress = min(1.0, (t - 2.6) / duration)
        wipe_y = int(GH * progress)
        for gy in range(wipe_y):
            c[gy, :] = PAL['RED']
            if gy == wipe_y - 1 or gy == wipe_y - 2:
                c[gy, :] = PAL['WHITE']
                
        # Draw lyric on top of the wipe
        if flash:
            draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
        else:
            draw_text_shadow_c(c, text, ty, fg, shadow, scl)

    scanlines(c, 0.20)
    return c

def title_frame(ft, warp):
    tc = new_canvas()
    for gy in range(GH):
        tc[gy, :] = (2, 0, int(10 + gy * 0.04))
    warp.draw(tc, ft * 0.5, 0.4)

    bord = PAL['ORANGE'] if int(ft * 4) % 2 == 0 else PAL['DKGREY']
    draw_rect(tc, 2, 2,      GW - 4, 1,      bord)
    draw_rect(tc, 2, GH - 3, GW - 4, 1,      bord)
    draw_rect(tc, 2, 2,      1,      GH - 4, bord)
    draw_rect(tc, GW - 3, 2, 1,      GH - 4, bord)

    draw_text_shadow_c(tc, "VERSE  3",          GH // 2 - 30, PAL['MAGENTA'], PAL['PURPLE'], 4)
    draw_text_shadow_c(tc, "LINE 02 - SUN",      GH // 2 + 12, PAL['ORANGE'],  PAL['RED'],   2)

    scanlines(tc)
    return tc

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path   = os.path.join(script_dir, OUT_FILE)

    print("=" * 60)
    print("  verse3/line02 — Burning Sun Zoom Zoom | Pixel Art")
    print("=" * 60)
    print(f"  Output : {out_path}")
    print(f"  Size   : {W}x{H} @ {FPS}fps")
    
    warp   = WarpTunnel(seed=4)
    galaxy = ZoomingGalaxy(seed=42)
    sun    = BurningSun()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_path, fourcc, FPS, (W, H))
    if not writer.isOpened():
        print("Fallback to XVID")
        out_path = out_path.replace('.mp4', '.avi')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(out_path, fourcc, FPS, (W, H))

    title_frames = int(1.5 * FPS)
    main_frames  = int(DUR * FPS)
    total_frames = title_frames + main_frames

    print(f"Rendering title card ({title_frames} frames)...")
    for f in range(title_frames):
        bgr = upscale(title_frame(f / FPS, warp))
        writer.write(bgr)

    print(f"Rendering animation ({main_frames} frames)...")
    for f in range(main_frames):
        t   = f / FPS
        bgr = upscale(render_frame(t, warp, galaxy, sun))
        writer.write(bgr)

    writer.release()
    print("DONE")

class Line02:
    pass

if __name__ == "__main__":
    main()
