from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import liveobj_color_to_value_from_palette, memoize
from ableton.v3.control_surface import STANDARD_COLOR_PALETTE, STANDARD_FALLBACK_COLOR_TABLE
from ableton.v3.control_surface.elements import SimpleColor
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
    RED = make_simple_color(5)
    RED_BLINK = SimpleColor(5, channel=BLINK_CHANNEL)
    RED_PULSE = SimpleColor(5, channel=PULSE_CHANNEL)
    RED_HALF = SimpleColor(5, channel=HALF_BRIGHTNESS_CHANNEL)
    GREEN = make_simple_color(21)
    GREEN_BLINK = SimpleColor(21, channel=BLINK_CHANNEL)
    GREEN_PULSE = SimpleColor(21, channel=PULSE_CHANNEL)


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