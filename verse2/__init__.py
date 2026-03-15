from .line01 import Line01
from .line02 import Line02
from .line03 import Line03
from .line04 import Line04
from .line05 import Line05
from .line06 import Line06
from .line07 import Line07
from .line08 import Line08
from .line09 import Line09
from .line10 import Line10
from .line11 import Line11
from .line12 import Line12

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C
LINES = [
    ("My bandmate now flatmate",                               C.CYAN,    2.0, Line01),
    ("I thought we will work hard on our tracks",             C.CYAN,    2.6, Line02),
    ("Yet all he did was sleep and waste time and talk cap",  C.GREY,    3.0, Line03),
    ("I held back my anger tried to understand him",          C.WHITE,   2.8, Line04),
    ("I gave him all the chances and dealt it with patience", C.WHITE,   3.0, Line05),
    ("I bite my own words from the second verse of the first",C.ORANGE,  3.0, Line06),
    ("Track i know that it's my bad to think that we'll make it", C.ORANGE, 3.0, Line07),
    ("now fuck that",                                         C.RED,     1.6, Line08),
    ("Deep down i knew that you will leave, you will quit",   C.RED,     3.0, Line09),
    ("a weak mind, you lack will",                            C.RED,     2.2, Line10),
    ("I cut ties, i moved on, didn't look back",              C.GREEN,   2.6, Line11),
    ("I felt bad, i felt good, i felt free at last.",         C.GREEN,   3.0, Line12),
]