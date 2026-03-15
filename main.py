#!/usr/bin/env python3
"""
MK-1 — ASCII Lyrics Video
──────────────────────────
Run:  python3 main.py
Exit: Ctrl+C

Structure:
  main.py          ← you are here (orchestrator)
  common.py        ← shared colors, helpers, LineAnimator base class
  verse1/          ← 15 line animators
  verse2/          ← 12 line animators
  verse3/          ← 15 line animators
  outro/           ← 8 line animators
"""

import sys
import os
import time
import math
import shutil

# ── Make sure imports resolve from this directory ────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import C, clear, flush, term_size, center_v

import verse1
import verse2
import verse3
import outro


# ── Title art ─────────────────────────────────────────────────────────────────
TITLE_ART = r"""
 ███████╗██╗  ██╗██╗   ██╗    ████████╗██████╗  █████╗ ███████╗███████╗██╗██╗  ██╗      ██████╗ ████████╗       ██████▄╗
 ██╔════╝██║ ██╔╝╚██╗ ██╔╝    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██║██║ ██╔╝      ██╔══██╗╚══██╔══╝       ╚════██║
 ███████╗█████╔╝  ╚████╔╝        ██║   ██████╔╝███████║█████╗  █████╗  ██║█████╔╝       ██████╔╝   ██║            ▄███╔╝
 ╚════██║██╔═██╗   ╚██╔╝         ██║   ██╔══██╗██╔══██║██╔══╝  ██╔══╝  ██║██╔═██╗       ██╔═══╝    ██║          ▄███══╝
 ███████║██║  ██╗   ██║          ██║   ██║  ██║██║  ██║██║     ██║     ██║██║  ██╗      ██║        ██║    ██╗   ███████╗
 ╚══════╝╚═╝  ╚═╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝      ╚═╝        ╚═╝    ╚═╝   ╚══════╝
"""


def show_intro():
    tw, th = term_size()
    clear()
    lines = TITLE_ART.strip("\n").split("\n")
    top   = center_v(len(lines) + 6, th)
    print("\n" * top)
    for line in lines:
        pad = max(0, (tw - len(line)) // 2)
        print(" " * pad + C.GOLD + C.BOLD + line + C.RESET)
    sub = "[ A F T E R  —  Mayank Rath ]"
    print("\n" + " " * max(0, (tw - len(sub)) // 2) + C.GREY + sub + C.RESET)
    time.sleep(0.1)


def show_section_header(label: str):
    """Animated section header — pulsing block bar."""
    FPS      = 24
    duration = 1.8
    elapsed  = 0.0
    dt       = 1.0 / FPS

    while elapsed < duration:
        t0      = time.time()
        tw, th  = term_size()
        clear()

        brightness = 0.5 + 0.5 * math.sin(elapsed * 6)
        bar_char   = "▓" if brightness > 0.5 else "░"
        bar        = bar_char * 8
        line       = f"{bar}  {label}  {bar}"
        pad        = max(0, (tw - len(line)) // 2)
        vpad       = th // 2 - 1

        sys.stdout.write("\n" * vpad)
        sys.stdout.write(" " * pad + C.GOLD + C.BOLD + line + C.RESET + "\n")
        flush()

        took = time.time() - t0
        time.sleep(max(0, dt - took))
        elapsed += dt


def show_blank(duration: float = 0.5):
    t0 = time.time()
    clear()
    flush()
    remaining = duration - (time.time() - t0)
    if remaining > 0:
        time.sleep(remaining)


def play_section(section_lines):
    """Play all (text, color, duration, AnimatorClass) tuples in a section."""
    for (text, color, duration, AnimClass) in section_lines:
        AnimClass().play(text, color, duration)


def show_end_card():
    tw, th = term_size()
    clear()
    lines = [
        "",
        C.GOLD + C.BOLD + "[ fin. ]" + C.RESET,
        "",
        C.GREY + "MK-1" + C.RESET,
    ]
    top = center_v(len(lines), th)
    print("\n" * top)
    for line in lines:
        visible_len = len(line.replace(C.GOLD, "").replace(C.BOLD, "")
                          .replace(C.RESET, "").replace(C.GREY, ""))
        pad = max(0, (tw - visible_len) // 2)
        print(" " * pad + line)
    time.sleep(2.5)


# ── Main ──────────────────────────────────────────────────────────────────────
def run():
    sys.stdout.write("\033[?25l")   # hide cursor
    flush()

    try:
        show_intro()

        # ── VERSE 1
        # show_section_header("── VERSE 1 ──")
        # show_blank(0.3)
        # play_section(verse1.LINES)

        # show_blank(0.6)

        # # ── VERSE 2
        # show_section_header("── VERSE 2 ──")
        # show_blank(0.3)
        # play_section(verse2.LINES)

        # show_blank(0.6)

        # ── VERSE 3
        show_section_header("── VERSE 3 ──")
        show_blank(0.3)
        play_section(verse3.LINES)

        show_blank(0.6)

        # ── OUTRO
        show_section_header("── OUTRO ──")
        show_blank(0.3)
        play_section(outro.LINES)

        show_end_card()

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h")   # restore cursor
        clear()
        flush()
        tw, _ = term_size()
        print(C.GREY + "[ stopped ]" + C.RESET)


if __name__ == "__main__":
    run()
