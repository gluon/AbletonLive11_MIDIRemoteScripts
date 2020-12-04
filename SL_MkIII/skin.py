#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from novation.colors import Rgb

class Colors(object):

    class DefaultButton(object):
        On = Rgb.GREEN
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Session(object):
        RecordButton = Rgb.RED
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipStopped = Rgb.AMBER
        Scene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_PULSE
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF
        ClipEmpty = Rgb.BLACK
        Navigation = Rgb.WHITE

    class Mixer(object):
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        Pan = Rgb.ORANGE
        TrackSelect = Rgb.WHITE
        Send = Rgb.WHITE

    class Monitor(object):
        In = Rgb.LIGHT_BLUE
        Auto = Rgb.YELLOW
        Off = Rgb.YELLOW
        Disabled = Rgb.YELLOW_HALF

    class Transport(object):
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.GREEN_HALF
        StopEnabled = Rgb.WHITE
        StopDisabled = Rgb.WHITE_HALF
        SeekOn = Rgb.WHITE
        SeekOff = Rgb.WHITE_HALF
        LoopOn = Rgb.YELLOW
        LoopOff = Rgb.YELLOW_HALF
        MetronomeOn = Rgb.YELLOW
        MetronomeOff = Rgb.YELLOW_HALF

    class Recording(object):
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.BLACK

    class Mode(object):

        class Mute(object):
            On = Rgb.YELLOW

        class Solo(object):
            On = Rgb.BLUE

        class Monitor(object):
            On = Rgb.GREEN

        class Arm(object):
            On = Rgb.RED

        class Devices(object):
            On = Rgb.PURPLE
            Off = Rgb.PURPLE

        class Pan(object):
            On = Rgb.ORANGE
            Off = Rgb.ORANGE

        class Sends(object):
            On = Rgb.WHITE
            Off = Rgb.WHITE

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

    class ItemNavigation(object):
        NoItem = Rgb.BLACK
        ItemSelected = Rgb.PURPLE
        ItemNotSelected = Rgb.PURPLE_HALF

    class Device(object):
        On = Rgb.PURPLE

    class TrackNavigation(object):
        On = Rgb.LIGHT_BLUE
        Pressed = Rgb.LIGHT_BLUE

    class SceneNavigation(object):
        On = Rgb.WHITE
        Pressed = Rgb.WHITE

    class Action(object):
        Available = Rgb.WHITE


skin = Skin(Colors)
