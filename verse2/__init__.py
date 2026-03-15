from .scene import Verse2Scene

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C

# Entire verse 2 is one unified scene (32.5 s).
# The text / color / duration args are ignored by Verse2Scene.play().
LINES = [
    ("verse2", C.WHITE, 32.5, Verse2Scene),
]