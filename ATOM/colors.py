#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/colors.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface.elements import Color
from . import midi
BLINK_VALUE = 1
PULSE_VALUE = 2

class RgbColor(Color):

    def __init__(self, red, green, blue, on_value = 127, *a, **k):
        super(RgbColor, self).__init__(*a, **k)
        self._red = red
        self._green = green
        self._blue = blue
        self._on_value = on_value

    def draw(self, interface):
        interface.send_value(self._red, channel=midi.RED_MIDI_CHANNEL)
        interface.send_value(self._green, channel=midi.GREEN_MIDI_CHANNEL)
        interface.send_value(self._blue, channel=midi.BLUE_MIDI_CHANNEL)
        interface.send_value(self._on_value if self._red or self._green or self._blue else 0)


class Mono(object):
    OFF = Color(0)
    ON = Color(127)


class Rgb(object):
    BLACK = RgbColor(0, 0, 0)
    WHITE = RgbColor(109, 80, 27)
    RED = RgbColor(127, 0, 0)
    RED_BLINK = RgbColor(127, 0, 0, on_value=BLINK_VALUE)
    RED_PULSE = RgbColor(127, 0, 0, on_value=PULSE_VALUE)
    RED_HALF = RgbColor(32, 0, 0)
    GREEN = RgbColor(0, 127, 0)
    GREEN_BLINK = RgbColor(0, 127, 0, on_value=BLINK_VALUE)
    GREEN_PULSE = RgbColor(0, 127, 0, on_value=PULSE_VALUE)
    GREEN_HALF = RgbColor(0, 32, 0)
    BLUE = RgbColor(0, 16, 127)
    BLUE_HALF = RgbColor(0, 0, 32)
    YELLOW = RgbColor(127, 83, 3)
    YELLOW_HALF = RgbColor(52, 34, 1)
    PURPLE = RgbColor(65, 0, 65)
    PURPLE_HALF = RgbColor(17, 0, 17)
    LIGHT_BLUE = RgbColor(0, 91, 91)
    ORANGE = RgbColor(127, 18, 0)
    PEACH = RgbColor(127, 51, 6)
    PINK = RgbColor(127, 17, 30)


LIVE_COLOR_INDEX_TO_RGB = {0: RgbColor(102, 46, 46),
 1: RgbColor(127, 34, 0),
 2: RgbColor(51, 51, 0),
 3: RgbColor(123, 122, 57),
 4: RgbColor(95, 125, 0),
 5: RgbColor(0, 39, 0),
 6: RgbColor(25, 127, 25),
 7: RgbColor(46, 127, 116),
 8: RgbColor(0, 76, 76),
 9: RgbColor(0, 51, 102),
 10: RgbColor(16, 89, 85),
 11: RgbColor(69, 21, 113),
 12: RgbColor(110, 10, 30),
 13: RgbColor(127, 127, 127),
 14: RgbColor(127, 0, 0),
 15: RgbColor(127, 32, 0),
 16: RgbColor(51, 51, 0),
 17: RgbColor(127, 82, 0),
 18: RgbColor(17, 69, 17),
 19: RgbColor(0, 31, 0),
 20: RgbColor(0, 76, 38),
 21: RgbColor(0, 127, 127),
 22: RgbColor(0, 51, 102),
 23: RgbColor(0, 0, 51),
 24: RgbColor(38, 0, 76),
 25: RgbColor(51, 0, 51),
 26: RgbColor(110, 10, 30),
 27: RgbColor(104, 104, 104),
 28: RgbColor(89, 17, 17),
 29: RgbColor(127, 49, 35),
 30: RgbColor(105, 86, 56),
 31: RgbColor(118, 127, 87),
 32: RgbColor(86, 127, 23),
 33: RgbColor(86, 127, 23),
 34: RgbColor(86, 127, 23),
 35: RgbColor(106, 126, 112),
 36: RgbColor(102, 120, 124),
 37: RgbColor(127, 76, 127),
 38: RgbColor(127, 76, 127),
 39: RgbColor(127, 25, 127),
 40: RgbColor(114, 110, 112),
 41: RgbColor(84, 84, 84),
 42: RgbColor(127, 49, 35),
 43: RgbColor(51, 51, 0),
 44: RgbColor(51, 51, 0),
 45: RgbColor(77, 102, 25),
 46: RgbColor(86, 127, 23),
 47: RgbColor(38, 76, 0),
 48: RgbColor(30, 89, 56),
 49: RgbColor(23, 69, 43),
 50: RgbColor(23, 69, 43),
 51: RgbColor(23, 69, 43),
 52: RgbColor(119, 65, 119),
 53: RgbColor(119, 65, 119),
 54: RgbColor(89, 17, 17),
 55: RgbColor(61, 61, 61),
 56: RgbColor(69, 0, 0),
 57: RgbColor(82, 21, 21),
 58: RgbColor(51, 51, 0),
 59: RgbColor(127, 82, 0),
 60: RgbColor(0, 50, 0),
 61: RgbColor(0, 50, 0),
 62: RgbColor(5, 78, 71),
 63: RgbColor(17, 49, 66),
 64: RgbColor(0, 0, 127),
 65: RgbColor(0, 51, 102),
 66: RgbColor(38, 0, 76),
 67: RgbColor(51, 0, 51),
 68: RgbColor(102, 23, 55),
 69: RgbColor(30, 30, 30)}
