# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\colors.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 3839 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import memoize
from ableton.v3.control_surface.elements import SimpleColor
from ableton.v3.live import liveobj_valid
from . import midi

@memoize
def make_simple_color(value):
    return SimpleColor(value)


def make_color_for_liveobj(obj):
    if liveobj_valid(obj):
        if obj.color_index is not None:
            return LIVE_COLOR_INDEX_TO_RGB.get(obj.color_index, 0)
    return Rgb.OFF


class Basic:
    FULL = make_simple_color(1)
    HALF = SimpleColor(1, channel=(midi.HALF_BRIGHTNESS_LED_CHANNEL))
    BLINK = SimpleColor(1, channel=(midi.BLINK_LED_CHANNEL))


class Rgb:
    OFF = make_simple_color(0)
    GREY = make_simple_color(1)
    WHITE = make_simple_color(3)
    RED = make_simple_color(5)
    RED_HALF = SimpleColor(5, channel=(midi.HALF_BRIGHTNESS_LED_CHANNEL))
    RED_BLINK = SimpleColor(5, channel=(midi.BLINK_LED_CHANNEL))
    RED_PULSE = SimpleColor(5, channel=(midi.PULSE_LED_CHANNEL))
    AMBER = make_simple_color(9)
    YELLOW = make_simple_color(13)
    YELLOW_HALF = SimpleColor(13, channel=(midi.HALF_BRIGHTNESS_LED_CHANNEL))
    GREEN = make_simple_color(21)
    GREEN_HALF = SimpleColor(21, channel=(midi.HALF_BRIGHTNESS_LED_CHANNEL))
    GREEN_BLINK = SimpleColor(21, channel=(midi.BLINK_LED_CHANNEL))
    GREEN_PULSE = SimpleColor(21, channel=(midi.PULSE_LED_CHANNEL))
    BLUE = make_simple_color(45)
    BLUE_HALF = SimpleColor(45, channel=(midi.HALF_BRIGHTNESS_LED_CHANNEL))


LIVE_COLOR_INDEX_TO_RGB = {0:make_simple_color(4), 
 1:make_simple_color(9), 
 2:make_simple_color(61), 
 3:make_simple_color(12), 
 4:make_simple_color(17), 
 5:make_simple_color(21), 
 6:make_simple_color(20), 
 7:make_simple_color(33), 
 8:make_simple_color(40), 
 9:make_simple_color(45), 
 10:make_simple_color(40), 
 11:make_simple_color(53), 
 12:make_simple_color(57), 
 13:make_simple_color(2), 
 14:make_simple_color(5), 
 15:make_simple_color(9), 
 16:make_simple_color(61), 
 17:make_simple_color(13), 
 18:make_simple_color(17), 
 19:make_simple_color(21), 
 20:make_simple_color(65), 
 21:make_simple_color(33), 
 22:make_simple_color(41), 
 23:make_simple_color(45), 
 24:make_simple_color(49), 
 25:make_simple_color(48), 
 26:make_simple_color(53), 
 27:make_simple_color(2), 
 28:make_simple_color(60), 
 29:make_simple_color(8), 
 30:make_simple_color(61), 
 31:make_simple_color(16), 
 32:make_simple_color(16), 
 33:make_simple_color(17), 
 34:make_simple_color(18), 
 35:make_simple_color(16), 
 36:make_simple_color(36), 
 37:make_simple_color(48), 
 38:make_simple_color(48), 
 39:make_simple_color(69), 
 40:make_simple_color(2), 
 41:make_simple_color(2), 
 42:make_simple_color(8), 
 43:make_simple_color(61), 
 44:make_simple_color(61), 
 45:make_simple_color(18), 
 46:make_simple_color(17), 
 47:make_simple_color(18), 
 48:make_simple_color(68), 
 49:make_simple_color(68), 
 50:make_simple_color(38), 
 51:make_simple_color(41), 
 52:make_simple_color(48), 
 53:make_simple_color(52), 
 54:make_simple_color(4), 
 55:make_simple_color(2), 
 56:make_simple_color(5), 
 57:make_simple_color(9), 
 58:make_simple_color(9), 
 59:make_simple_color(13), 
 60:make_simple_color(18), 
 61:make_simple_color(76), 
 62:make_simple_color(65), 
 63:make_simple_color(68), 
 64:make_simple_color(45), 
 65:make_simple_color(38), 
 66:make_simple_color(49), 
 67:make_simple_color(49), 
 68:make_simple_color(95), 
 69:make_simple_color(2)}