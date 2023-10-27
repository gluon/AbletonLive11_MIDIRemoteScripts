# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_mini_mk2\colors.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 2162 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import memoize
from ableton.v3.control_surface import STANDARD_COLOR_PALETTE, STANDARD_FALLBACK_COLOR_TABLE
from ableton.v3.control_surface.elements import SimpleColor
from ableton.v3.live import liveobj_color_to_value_from_palette
HALF_BRIGHTNESS_CHANNEL = 1
FULL_BRIGHTNESS_CHANNEL = 6
PULSE_CHANNEL = 10
BLINK_CHANNEL = 14

@memoize
def make_simple_color(value):
    return SimpleColor(value)


def make_color_for_liveobj(obj):
    return make_simple_color(liveobj_color_to_value_from_palette(obj,
      palette=STANDARD_COLOR_PALETTE,
      fallback_table=STANDARD_FALLBACK_COLOR_TABLE))


class Basic:
    ON = make_simple_color(1)
    BLINK = make_simple_color(2)


class Rgb:
    BLACK = make_simple_color(0)
    GREY = make_simple_color(1)
    RED = make_simple_color(5)
    RED_BLINK = SimpleColor(5, channel=BLINK_CHANNEL)
    RED_PULSE = SimpleColor(5, channel=PULSE_CHANNEL)
    RED_HALF = SimpleColor(5, channel=HALF_BRIGHTNESS_CHANNEL)
    AMBER = make_simple_color(9)
    YELLOW = make_simple_color(13)
    GREEN = make_simple_color(21)
    GREEN_BLINK = SimpleColor(21, channel=BLINK_CHANNEL)
    GREEN_PULSE = SimpleColor(21, channel=PULSE_CHANNEL)
    OCEAN = make_simple_color(41)
    BLUE = make_simple_color(45)


class Skin:

    class Session:
        SlotRecordButton = Rgb.RED_HALF
        ClipStopped = make_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        SceneTriggered = Basic.BLINK
        StopClipTriggered = Basic.BLINK
        StopClip = Basic.ON

    class DrumGroup:
        PadEmpty = Rgb.GREY
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.OCEAN
        PadMuted = Rgb.AMBER
        PadMutedSelected = Rgb.OCEAN
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.OCEAN