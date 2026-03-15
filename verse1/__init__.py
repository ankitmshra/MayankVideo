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

# (text, color, duration, AnimatorClass)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import C
LINES = [
    #("Boom boom when i come in the game it goes boom boom",   C.CYAN,    .2, Line01),
    #("My pen kung fu like bruce lee go ahead and zoom zoom",  C.CYAN,    3.2, Line02),
    #("I play doom doom FPS with my gun i go and shoot shoot", C.RED,     3.2, Line03),
    #("You need to show ID at the club we are not the same",   C.WHITE,   3.0, Line04),
    #("Who knew,",                                              C.GREY,    1.4, Line05),
    #("In Halloween i'll play mmm....food",                    C.ORANGE,  2.5, Line06),
    #("Dune soundtrack playing in my ears on loop",            C.BLUE,    2.8, Line07),
    #("Going on vacations with Villeneuve view",               C.BLUE,    2.6, Line08),
    #("Chalamet with my energy i feel always new",             C.MAGENTA, 2.8, Line09),
    #("My shawty pretty like Zendaya she my boo boo",          C.MAGENTA, 2.8, Line10),
    #("Mmm hmm that's cute,",                                  C.GREY,    1.6, Line11),
    #("I flew across state to see you",                        C.CYAN,    2.4, Line12),
    #("My estate is building day by day it'll be huge",        C.GOLD,    2.8, Line13),
    #("I avoid news like the flu",                             C.WHITE,   2.2, Line14),
    #("Feeding information which is not true",                 C.RED,     2.5, Line14),
    #("You got no clue how they control you.",                 C.RED,     2.8, Line15),
]