# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/colors.py
# Compiled at: 2021-08-06 01:27:35
# Size of source mod 2**32: 416 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color

class Basic:
    OFF = Color(0)
    ON = Color(1)
    DISABLED = Color(2)


class Rgb:
    YELLOW = Color(3)
    LIGHT_BLUE = Color(6)
    RED = Color(13)
    ORANGE = Color(14)
    GREEN = Color(4)
    DARK_BLUE = Color(63)