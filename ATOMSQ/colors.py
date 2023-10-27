# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\colors.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 4565 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import BasicColors
from ableton.v3.control_surface.elements import ColorPart, ComplexColor, FallbackColor
from ableton.v3.live import liveobj_valid
from . import midi
BLINK_VALUE = 1
PULSE_VALUE = 2

def create_color(red, green, blue, on_value=127, fallback=None):
    color = ComplexColor((
     ColorPart(red, channel=(midi.RED_MIDI_CHANNEL)),
     ColorPart(green, channel=(midi.GREEN_MIDI_CHANNEL)),
     ColorPart(blue, channel=(midi.BLUE_MIDI_CHANNEL)),
     ColorPart(on_value)))
    if fallback is not None:
        return FallbackColor(color, fallback)
    return color


def create_color_for_liveobj(obj, is_scene=False):
    if liveobj_valid(obj):
        if obj.color_index is not None:
            return LIVE_COLOR_INDEX_TO_RGB.get(obj.color_index, 0)
    if is_scene:
        return Rgb.GREEN_HALF
    return Rgb.OFF


class Rgb:
    OFF = create_color(0, 0, 0, on_value=0, fallback=(BasicColors.OFF))
    ON = create_color(127, 127, 127, fallback=(BasicColors.ON))
    RED = create_color(127, 0, 0)
    RED_BLINK = create_color(127, 0, 0, on_value=BLINK_VALUE, fallback=(BasicColors.ON))
    RED_PULSE = create_color(127, 0, 0, on_value=PULSE_VALUE, fallback=(BasicColors.ON))
    RED_HALF = create_color(32, 0, 0, fallback=(BasicColors.OFF))
    GREEN = create_color(0, 127, 0, fallback=(BasicColors.ON))
    GREEN_BLINK = create_color(0, 127, 0, on_value=BLINK_VALUE, fallback=(BasicColors.ON))
    GREEN_PULSE = create_color(0, 127, 0, on_value=PULSE_VALUE, fallback=(BasicColors.ON))
    GREEN_HALF = create_color(0, 32, 0)
    GREEN_DIM = create_color(0, 12, 0, fallback=(BasicColors.OFF))
    BLUE = create_color(0, 16, 127)
    BLUE_HALF = create_color(0, 0, 32)
    PURPLE = create_color(65, 0, 65)
    PURPLE_HALF = create_color(17, 0, 17)
    YELLOW = create_color(127, 83, 3)
    YELLOW_HALF = create_color(52, 34, 1)


LIVE_COLOR_INDEX_TO_RGB = {0:create_color(102, 46, 46), 
 1:create_color(127, 34, 0), 
 2:create_color(51, 51, 0), 
 3:create_color(123, 122, 57), 
 4:create_color(95, 125, 0), 
 5:create_color(0, 39, 0), 
 6:create_color(25, 127, 25), 
 7:create_color(46, 127, 116), 
 8:create_color(0, 76, 76), 
 9:create_color(0, 51, 102), 
 10:create_color(16, 89, 85), 
 11:create_color(69, 21, 113), 
 12:create_color(110, 10, 30), 
 13:create_color(127, 127, 127), 
 14:create_color(127, 0, 0), 
 15:create_color(127, 32, 0), 
 16:create_color(51, 51, 0), 
 17:create_color(127, 82, 0), 
 18:create_color(17, 69, 17), 
 19:create_color(0, 31, 0), 
 20:create_color(0, 76, 38), 
 21:create_color(0, 127, 127), 
 22:create_color(0, 51, 102), 
 23:create_color(0, 0, 51), 
 24:create_color(38, 0, 76), 
 25:create_color(51, 0, 51), 
 26:create_color(110, 10, 30), 
 27:create_color(104, 104, 104), 
 28:create_color(89, 17, 17), 
 29:create_color(127, 49, 35), 
 30:create_color(105, 86, 56), 
 31:create_color(118, 127, 87), 
 32:create_color(86, 127, 23), 
 33:create_color(86, 127, 23), 
 34:create_color(86, 127, 23), 
 35:create_color(106, 126, 112), 
 36:create_color(102, 120, 124), 
 37:create_color(127, 76, 127), 
 38:create_color(127, 76, 127), 
 39:create_color(127, 25, 127), 
 40:create_color(114, 110, 112), 
 41:create_color(84, 84, 84), 
 42:create_color(127, 49, 35), 
 43:create_color(51, 51, 0), 
 44:create_color(51, 51, 0), 
 45:create_color(77, 102, 25), 
 46:create_color(86, 127, 23), 
 47:create_color(38, 76, 0), 
 48:create_color(30, 89, 56), 
 49:create_color(23, 69, 43), 
 50:create_color(23, 69, 43), 
 51:create_color(23, 69, 43), 
 52:create_color(119, 65, 119), 
 53:create_color(119, 65, 119), 
 54:create_color(89, 17, 17), 
 55:create_color(61, 61, 61), 
 56:create_color(69, 0, 0), 
 57:create_color(82, 21, 21), 
 58:create_color(51, 51, 0), 
 59:create_color(127, 82, 0), 
 60:create_color(0, 50, 0), 
 61:create_color(0, 50, 0), 
 62:create_color(5, 78, 71), 
 63:create_color(17, 49, 66), 
 64:create_color(0, 0, 127), 
 65:create_color(0, 51, 102), 
 66:create_color(38, 0, 76), 
 67:create_color(51, 0, 51), 
 68:create_color(102, 23, 55), 
 69:create_color(30, 30, 30)}