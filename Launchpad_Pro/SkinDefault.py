#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Pro/SkinDefault.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors(object):

    class DefaultButton(object):
        On = Rgb.GREEN
        Off = Rgb.GREEN_HALF
        Disabled = Rgb.BLACK

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
        Enabled = Rgb.GREEN
        Off = Rgb.GREEN_HALF

    class Zooming(object):
        Selected = Rgb.AMBER
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class Mixer(object):
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        Selected = Rgb.LIGHT_BLUE
        Unselected = Rgb.LIGHT_BLUE_HALF
        Volume = Rgb.GREEN
        Pan = Rgb.ORANGE
        Sends = Rgb.WHITE

    class Sends(object):
        A = Rgb.DARK_BLUE
        AAvail = Rgb.DARK_BLUE_HALF
        B = Rgb.BLUE
        BAvail = Rgb.BLUE_HALF
        C = Rgb.LIGHT_BLUE
        CAvail = Rgb.LIGHT_BLUE_HALF
        D = Rgb.MINT
        DAvail = Rgb.MINT_HALF
        E = Rgb.DARK_YELLOW
        EAvail = Rgb.DARK_YELLOW_HALF
        F = Rgb.YELLOW
        FAvail = Rgb.YELLOW_HALF
        G = Rgb.ORANGE
        GAvail = Rgb.ORANGE_HALF
        H = Rgb.RED
        HAvail = Rgb.RED_HALF

    class Device(object):
        On = Rgb.PURPLE
        Off = Rgb.PURPLE_HALF
        Disabled = Rgb.BLACK

    class Recording(object):
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.RED_BLINK

    class DrumGroup(object):
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.RED

    class Instrument(object):
        FeedbackRecord = Rgb.RED
        Feedback = Rgb.GREEN

    class Mode(object):

        class Session(object):
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Chromatic(object):
            On = Rgb.LIGHT_BLUE
            Off = Rgb.LIGHT_BLUE_HALF

        class Drum(object):
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class Device(object):
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF

        class User(object):
            On = Rgb.DARK_BLUE
            Off = Rgb.DARK_BLUE_HALF

        class RecordArm(object):
            On = Rgb.RED
            Off = Rgb.RED_HALF

        class TrackSelect(object):
            On = Rgb.LIGHT_BLUE
            Off = Rgb.LIGHT_BLUE_HALF

        class Mute(object):
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class Solo(object):
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

        class Volume(object):
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Pan(object):
            On = Rgb.ORANGE
            Off = Rgb.ORANGE_HALF

        class Sends(object):
            On = Rgb.WHITE
            Off = Rgb.DARK_GREY

        class StopClip(object):
            On = Rgb.RED
            Off = Rgb.RED_HALF

    class Scrolling(object):
        Enabled = Rgb.YELLOW_HALF
        Pressed = Rgb.YELLOW
        Disabled = Rgb.BLACK

    class Misc(object):
        UserMode = Rgb.DARK_BLUE
        Shift = Rgb.DARK_GREY
        ShiftOn = Rgb.WHITE


def make_default_skin():
    return Skin(Colors)
