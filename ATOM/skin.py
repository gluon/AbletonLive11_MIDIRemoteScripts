#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb

class Colors(object):

    class DefaultButton(object):
        On = Mono.ON
        Off = Mono.OFF
        Disabled = Mono.OFF
        RgbOff = Rgb.BLACK

    class Transport(object):
        PlayOn = Mono.ON
        PlayOff = Mono.OFF

    class Recording(object):
        On = Mono.ON
        Transition = Mono.ON
        Off = Mono.OFF

    class Mixer(object):
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        Selected = Rgb.WHITE
        EmptyTrack = Rgb.BLACK

    class Session(object):
        ClipEmpty = Rgb.BLACK
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        RecordButton = Rgb.RED_HALF
        Scene = Rgb.GREEN_HALF
        NoScene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class Zooming(object):
        Selected = Rgb.WHITE
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class NotePad(object):
        Pressed = Rgb.RED

    class Keyboard(object):
        Natural = Rgb.YELLOW
        Sharp = Rgb.BLUE

    class DrumGroup(object):
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadQuadrant0 = Rgb.BLUE
        PadQuadrant1 = Rgb.GREEN
        PadQuadrant2 = Rgb.YELLOW
        PadQuadrant3 = Rgb.PURPLE
        PadQuadrant4 = Rgb.ORANGE
        PadQuadrant5 = Rgb.LIGHT_BLUE
        PadQuadrant6 = Rgb.PINK
        PadQuadrant7 = Rgb.PEACH

    class Mode(object):

        class Volume(object):
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Pan(object):
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class SendA(object):
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

        class SendB(object):
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF


skin = Skin(Colors)
