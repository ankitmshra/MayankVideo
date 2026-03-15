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
from .line13 import Line13
from .line14 import Line14
from .line15 import Line15

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C
LINES = [
    ("I got the universe in my hand i can do anything",        C.MAGENTA, 3.0, Line01),
    ("Once flew close to the sun got my wings burnt",          C.ORANGE,  2.8, Line02),
    ("Had to become Brutus had to kill the king",              C.RED,     2.6, Line03),
    ("I carry us too much",                                    C.WHITE,   2.0, Line04),
    ("Put Rome in the ground i'm the ruler",                   C.GOLD,    2.4, Line05),
    ("Omnipotent with my dynasty mind palace is big like Caesar", C.GOLD, 3.0, Line06),
    ("I'm a born leader",                                      C.CYAN,    2.0, Line07),
    ("Straight outta the best kept secret",                    C.CYAN,    2.4, Line08),
    ("Art like Basquiat pieces",                               C.MAGENTA, 2.2, Line09),
    ("Diamonds in my ceiling",                                 C.BLUE,    2.0, Line10),
    ("Irony of a man with feelings",                           C.BLUE,    2.2, Line11),
    ("Got a carousel full of dreams and",                      C.MAGENTA, 2.4, Line12),
    ("A roller coaster full of heaters",                       C.ORANGE,  2.4, Line13),
    ("All of my homies are winners",                           C.GREEN,   2.2, Line14),
    ("Fuck the police they can't reach us.",                   C.RED,     2.6, Line15),
]