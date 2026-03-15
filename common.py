"""
common.py — shared colors, terminal helpers, and base animator class.
Every line module imports from here.
"""

import sys
import math
import time
import random
import shutil


# ── ANSI colors ───────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    UNDER   = "\033[4m"
    BLINK   = "\033[5m"
    GOLD    = "\033[38;5;220m"
    CYAN    = "\033[38;5;51m"
    MAGENTA = "\033[38;5;201m"
    RED     = "\033[38;5;196m"
    GREEN   = "\033[38;5;118m"
    WHITE   = "\033[38;5;255m"
    GREY    = "\033[38;5;245m"
    ORANGE  = "\033[38;5;208m"
    BLUE    = "\033[38;5;75m"
    PINK    = "\033[38;5;213m"
    YELLOW  = "\033[38;5;226m"
    PURPLE  = "\033[38;5;135m"
    TEAL    = "\033[38;5;43m"
    BG_BLACK = "\033[40m"


# ── Terminal helpers ──────────────────────────────────────────────────────────
def term_size():
    return shutil.get_terminal_size(fallback=(100, 30))

def clear():
    sys.stdout.write("\033[2J\033[H")

def flush():
    sys.stdout.flush()

def center_text(text, width):
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text

def center_v(lines, height):
    """Return top padding to vertically center `lines` count in `height`."""
    return max(0, (height - lines) // 2)


# ── Base Animator ─────────────────────────────────────────────────────────────
class LineAnimator:
    """
    Base class for every line animation.
    Subclass and override `frame(text, color, t, tw, th) -> str`.
    Call `.play(text, color, duration)` to run.
    """
    FPS = 24

    def frame(self, text: str, color: str, t: float, tw: int, th: int) -> str:
        raise NotImplementedError

    def play(self, text: str, color: str, duration: float):
        dt = 1.0 / self.FPS
        elapsed = 0.0
        while elapsed < duration:
            t0 = time.time()
            tw, th = term_size()
            clear()
            sys.stdout.write(self.frame(text, color, elapsed, tw, th))
            flush()
            took = time.time() - t0
            time.sleep(max(0, dt - took))
            elapsed += dt
