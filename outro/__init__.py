from .line01 import Line01
from .line02 import Line02
from .line03 import Line03
from .line04 import Line04
from .line05 import Line05
from .line06 import Line06
from .line07 import Line07
from .line08 import Line08

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C
LINES = [
    ("Sunset dripping in the water",          C.ORANGE,  2.6, Line01),
    ("Van gogh, nightscapes, dark towers",    C.BLUE,    2.6, Line02),
    ("We look up in the sky",                 C.CYAN,    2.2, Line03),
    ("We in it like it's ride or die",        C.WHITE,   2.4, Line04),
    ("Ahh ahhhh ahh ahhh ahhh ahh",          C.GREY,    2.2, Line05),
    ("We in it like it's ride or die",        C.WHITE,   2.4, Line06),
    ("Ahh ahhhh ahh ahhh ahhh ahh",          C.GREY,    2.2, Line07),
    ("We in it like it's ride or die.",       C.GOLD,    3.0, Line08),
]