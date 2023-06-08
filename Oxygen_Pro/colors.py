from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color

class Basic:
    ON = Color(127)
    OFF = Color(0)


class Rgb:
    GREEN = Color(12)
    GREEN_BLINK = Color(76)
    RED = Color(3)
    RED_BLINK = Color(67)
    AMBER = Color(11)
    WHITE = Color(63)