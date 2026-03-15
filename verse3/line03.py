#!/usr/bin/env python3
import math
import random
import os
import numpy as np
import cv2

from constants import *

OUT_FILE = "verse3_line03_SISYPHUS_2.mp4"

# "I carry us  - too much,
# Put Rome in the ground -  i'm the ruler,
# Omnipotent with my dynasty -  mind palace is big like  - Caesar"
CHUNKS = [
    (0.50, "I CARRY US",             PAL['WHITE'],  PAL['DKGREY']),
    (1.50, "TOO MUCH",               PAL['LTCYAN'], PAL['BLUE']),
    (2.50, "PUT ROME IN THE GROUND", PAL['ORANGE'], PAL['RED']),
    (3.50, "I'M THE RULER",          PAL['GOLD'],   PAL['RED']),
    (4.50, "OMNIPOTENT WITH MY DYNASTY", PAL['LTBLUE'], PAL['DKBLUE']),
    (5.50, "MIND PALACE IS BIG LIKE",PAL['MAGENTA'], PAL['PURPLE']),
    (6.20, "CAESAR",                 PAL['YELLOW'], PAL['ORANGE']),
    (7.20, "I'M A BORN LEADER",                 PAL['YELLOW'], PAL['ORANGE'])
]
DUR = 8.0

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

class Background:
    def __init__(self, seed=42):
        rng = np.random.default_rng(seed)
        self.stars = []
        for _ in range(100):
            self.stars.append((
                rng.integers(0, GW),
                rng.integers(0, int(GH * 0.7)),
                rng.choice([PAL['STARDIM'], PAL['STARBRT'], PAL['STARBLUE']]),
                rng.uniform(0.5, 2.0)  # speed multiplier
            ))

    def draw(self, c, t):
        # Dark red/purple sky gradient
        h_local = c.shape[0]
        for gy in range(h_local):
            frac = gy / GH
            r = int(20 + frac * 40)
            g = int(0)
            b = int(10 + frac * 20)
            c[gy, :] = (min(255, r), 0, min(255, b))
            
        # Draw stars moving left-downwards to match scrolling slope
        for x, y, col, speed in self.stars:
            sx = int((x - t * 15 * speed) % GW)
            sy = int((y + t * 5 * speed) % (GH * 0.7))
            
            # Use `spx` logic but check against `h_local` and GW directly
            if 0 <= sx < GW and 0 <= sy < h_local:
                c[sy, sx] = col

class InfiniteSlope:
    def __init__(self, seed=1):
        rng = np.random.default_rng(seed)
        self.noise = rng.integers(0, 10, (GH, GW))
        
    def draw(self, c, t):
        slope_m = 0
        scroll_x = int(t * 60)
        scroll_y = 0
        
        # We can vectorize this drawing
        h_local = c.shape[0]
        w_local = c.shape[1]
        
        gy_grid, gx_grid = np.mgrid[0:h_local, 0:w_local]
        
        vx = gx_grid + scroll_x
        vy = gy_grid - scroll_y
        
        ground_y = int(GH * 0.85)
        
        # boolean masks
        under_ground = gy_grid > ground_y
        edge = under_ground & (gy_grid - ground_y < 2)
        deep = under_ground & ~edge
        
        # noise texture lookup
        # we tile the noise to cover the active space if needed, 
        # or simply use modulo arithmetic
        nz_x = gx_grid % GW
        nz_y = gy_grid % GH
        nz = self.noise[nz_y, nz_x]
        
        # apply colors
        c[edge] = PAL['DKGREY']
        
        c[deep & (nz < 2)] = PAL['RED']
        c[deep & (nz >= 2) & (nz < 4)] = (80, 20, 20)
        c[deep & (nz >= 4)] = (50, 10, 10)

# We need to alpha-blend assets. Small utility.
def blend_asset(c, img, cx, cy, alpha=1.0):
    bh, bw = img.shape[:2]
    # Place it centered at (cx, cy)
    x1 = cx - bw // 2
    y1 = cy - bh // 2
    x2 = x1 + bw
    y2 = y1 + bh

    # Clipping to screen bounds
    cx1 = max(0, x1)
    cy1 = max(0, y1)
    cx2 = min(GW, x2)
    cy2 = min(GH, y2)

    if cx1 >= cx2 or cy1 >= cy2:
        return

    # Corresponding region in the image
    ix1 = cx1 - x1
    iy1 = cy1 - y1
    ix2 = ix1 + (cx2 - cx1)
    iy2 = iy1 + (cy2 - cy1)

    src = img[iy1:iy2, ix1:ix2]
    dst = c[cy1:cy2, cx1:cx2]

    # Usually BGRA. Unpack
    if src.shape[2] == 4:
        mask = (src[:, :, 3] / 255.0) * alpha
        mask = np.stack([mask]*3, axis=-1)
        c[cy1:cy2, cx1:cx2] = (src[:, :, :3] * mask + dst * (1 - mask)).astype(np.uint8)
    else:
        # No alpha channel, complete overwrite
        c[cy1:cy2, cx1:cx2] = src

class SisyphusAndRock:
    def __init__(self):
        self.cx = GW // 2
        self.cy = int(GH * 0.65)
        
        # Load assets
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        self.moon_img = cv2.imread(os.path.join(assets_dir, "moon.png"), cv2.IMREAD_UNCHANGED)
        self.spr_img = cv2.imread(os.path.join(assets_dir, "sysiphus_sprite.png"), cv2.IMREAD_UNCHANGED)
        
        # Scale moon to 120x120 to match Sisyphus
        if self.moon_img is not None:
             self.moon_img = cv2.resize(self.moon_img, (120, 120), interpolation=cv2.INTER_AREA)
             # OpenCV loads BGRA, convert to RGBA for our RGB canvas
             self.moon_img = cv2.cvtColor(self.moon_img, cv2.COLOR_BGRA2RGBA)
             
        # Sysiphus sprite has 4 frames side-by-side.
        self.frames = []
        if self.spr_img is not None:
             self.spr_img = cv2.cvtColor(self.spr_img, cv2.COLOR_BGRA2RGBA)
             h, w = self.spr_img.shape[:2]
             fw = w // 4
             # Assuming we want to scale him to roughly 120 pixels tall
             target_h = 60
             target_w = int(fw * (target_h / h))
             for i in range(4):
                 f = self.spr_img[:, i*fw:(i+1)*fw]
                 f = cv2.resize(f, (target_w, target_h), interpolation=cv2.INTER_AREA)
                 self.frames.append(f)

    def draw(self, c, t):
        wobble_x = int(math.sin(t * 12) * 2)
        wobble_y = int(math.cos(t * 10) * 1)
        
        # Move across screen
        base_x = int(-40 + (GW + 80) * (t / 7.0))
        px = base_x + wobble_x
        py = int(GH * 0.85) - 20 + wobble_y
        
        # Adjust rock coordinates since the asset is now much bigger
        rock_cx = px + 65
        rock_cy = py - 35
        
        if self.moon_img is not None:
            # Rotate moon as it rolls clockwise (- angle)
            ang = -t * 60.0  # degrees
            h, w = self.moon_img.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), ang, 1.0)
            # Use borderMode=cv2.BORDER_CONSTANT (transparent 0,0,0,0 background)
            rotated_moon = cv2.warpAffine(self.moon_img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
            blend_asset(c, rotated_moon, rock_cx, rock_cy)
        else:
            # Fallback circle
            for dy in range(-60, 61):
                for dx in range(-60, 61):
                    if dx*dx + dy*dy <= 3600:
                        spx(c, rock_cx + dx, rock_cy + dy, PAL['GREY'])
                        
        if self.frames:
            # Animate character based on time
            f_idx = int(t * 8) % 4
            frame = self.frames[f_idx]
            # Center near px, py.
            # Adjust char_x, char_y so he's on the ground pushing the moon
            char_x = px - 25  
            char_y = py - 5
            blend_asset(c, frame, char_x, char_y)
        else:
            # Fallback box
            for dy in range(10):
                for dx in range(10):
                    spx(c, px - 20 + dx, py - 4 + dy, PAL['BLACK'])
                    
def apply_glitch(c, t):
    intensity = (t - 6.6) / 0.4
    intensity = max(0.0, min(1.0, intensity))
    if intensity <= 0: return

    h_local, w_local = c.shape[:2]
    
    # Generate RGB static pixels
    num_static_pixels = int(w_local * h_local * intensity * 0.4)  # Up to 40% of screen becomes static
    
    if num_static_pixels > 0:
        xs = np.random.randint(0, w_local, num_static_pixels)
        ys = np.random.randint(0, h_local, num_static_pixels)
        
        # Random saturated colors for glitch (Red, Green, Blue, Magenta, Cyan, Yellow, White)
        colors = np.array([
            [255, 0, 0], [0, 255, 0], [0, 0, 255], 
            [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255]
        ], dtype=np.uint8)
        
        color_indices = np.random.randint(0, len(colors), num_static_pixels)
        c[ys, xs] = colors[color_indices]
    
    # Random horizontal noise bands
    num_bands = int(intensity * 15)
    for _ in range(num_bands):
        band_y = random.randint(0, h_local - 3)
        band_h = random.randint(1, 3)
        
        # Binary RGB noise for the band
        noise_band = np.random.randint(0, 2, (band_h, w_local, 3), dtype=np.uint8) * 255
        c[band_y:band_y+band_h, :] = noise_band

def render_frame(t, bg, slope, sisyphus):
    c = new_canvas()

    if t < 0.5:
        # Fade from red wipe in previous scene
        progress = t / 0.5
        c[:, :] = PAL['RED']
        # Rect wipe up
        wipe_y = int(GH * progress)
        for gy in range(wipe_y):
            bg.draw(c[gy:gy+1, :], t)
            slope.draw(c, t) # Hacky but works since we override below
        
        c_temp = new_canvas()
        bg.draw(c_temp, t)
        slope.draw(c_temp, t)
        sisyphus.draw(c_temp, t)
        
        c[wipe_y:, :] = PAL['RED']
        if wipe_y < GH:
            c[:wipe_y, :] = c_temp[:wipe_y, :]
    else:
        bg.draw(c, t)
        slope.draw(c, t)
        sisyphus.draw(c, t)

    # ── Lyric text ────────────────────────────────────────────
    if t >= 0.5:
        t_start, text, fg, shadow = active_chunk(t)
        chunk_age = t - t_start
        flash     = chunk_age < 0.08
        scl       = 4 if len(text) <= 8 else (2 if len(text) > 20 else 3)
        ty        = 30

        if flash:
            draw_text_shadow_c(c, text, ty - 1, PAL['WHITE'], PAL['BLACK'], scl)
        else:
            draw_text_shadow_c(c, text, ty, fg, shadow, scl)

    # Pixel glitch removed per user request
    scanlines(c, 0.20)
    return c

def title_frame(ft, bg):
    tc = new_canvas()
    bg.draw(tc, ft)

    bord = PAL['RED'] if int(ft * 4) % 2 == 0 else PAL['DKGREY']
    draw_rect(tc, 2, 2,      GW - 4, 1,      bord)
    draw_rect(tc, 2, GH - 3, GW - 4, 1,      bord)
    draw_rect(tc, 2, 2,      1,      GH - 4, bord)
    draw_rect(tc, GW - 3, 2, 1,      GH - 4, bord)

    draw_text_shadow_c(tc, "VERSE  3",          GH // 2 - 30, PAL['MAGENTA'], PAL['PURPLE'], 4)
    draw_text_shadow_c(tc, "LINE 03 - SISYPHUS", GH // 2 + 12, PAL['RED'],     PAL['DKGREY'], 2)

    scanlines(tc)
    return tc


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path   = os.path.join(script_dir, OUT_FILE)

    print("=" * 60)
    print("  verse3/line03 — Sisyphus Climbing & RGB Glitch")
    print("=" * 60)
    
    bg = Background()
    slope = InfiniteSlope()
    sisyphus = SisyphusAndRock()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_path, fourcc, FPS, (W, H))
    if not writer.isOpened():
        print("Fallback to XVID")
        out_path = out_path.replace('.mp4', '.avi')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(out_path, fourcc, FPS, (W, H))

    title_frames = int(1.5 * FPS)
    main_frames  = int(DUR * FPS)

    print(f"Rendering title card ({title_frames} frames)...")
    for f in range(title_frames):
        bgr = upscale(title_frame(f / FPS, bg))
        writer.write(bgr)

    print(f"Rendering animation ({main_frames} frames)...")
    for f in range(main_frames):
        t   = f / FPS
        bgr = upscale(render_frame(t, bg, slope, sisyphus))
        writer.write(bgr)

    writer.release()
    print("DONE")

class Line03:
    pass

if __name__ == "__main__":
    main()
