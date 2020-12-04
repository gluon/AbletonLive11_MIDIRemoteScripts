#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/Skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors(object):

    class Session(object):
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED_HALF
        StopClip = Rgb.RED
        StopClipTriggered = Rgb.RED_BLINK
        StoppedClip = Rgb.RED_HALF
        Enabled = Rgb.YELLOW

    class Zooming(object):
        Selected = Rgb.AMBER
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class Mixer(object):
        Disabled = Rgb.BLACK

        class Volume(object):
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Pan(object):
            On = Rgb.ORANGE
            Off = Rgb.ORANGE_HALF

        class Mute(object):
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class Solo(object):
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

        class Arm(object):
            On = Rgb.RED
            Off = Rgb.RED_HALF

    class Sends(object):

        class Send0(object):
            On = Rgb.DARK_BLUE
            Off = Rgb.DARK_BLUE_HALF

        class Send1(object):
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

    class Mode(object):

        class SessionMode(object):
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class User1Mode(object):
            On = Rgb.DARK_BLUE
            Off = Rgb.DARK_BLUE_HALF

        class User2Mode(object):
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF

        class MixerMode(object):
            On = Rgb.LIGHT_BLUE
            GroupOn = Rgb.LIGHT_BLUE
            Off = Rgb.LIGHT_BLUE_HALF

        class VolumeMode(object):
            On = Rgb.GREEN
            GroupOn = Rgb.GREEN_HALF
            Off = Rgb.BLACK

        class PanMode(object):
            On = Rgb.ORANGE
            GroupOn = Rgb.ORANGE_HALF
            Off = Rgb.BLACK

        class SendAMode(object):
            On = Rgb.DARK_BLUE
            GroupOn = Rgb.DARK_BLUE_HALF
            Off = Rgb.BLACK

        class SendBMode(object):
            On = Rgb.BLUE
            GroupOn = Rgb.BLUE_HALF
            Off = Rgb.BLACK

    class Scrolling(object):
        Enabled = Rgb.GREEN_HALF
        Pressed = Rgb.GREEN
        Disabled = Rgb.BLACK


def make_default_skin():
    return Skin(Colors)
