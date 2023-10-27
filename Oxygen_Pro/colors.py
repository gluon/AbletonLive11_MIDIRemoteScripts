# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\colors.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 414 bytes
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