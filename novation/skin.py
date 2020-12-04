#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb

class Colors(object):

    class DefaultButton(object):
        On = Rgb.GREEN
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Recording(object):
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.RED_BLINK
        CaptureTriggered = Rgb.WHITE

    class FixedLength(object):
        On = Rgb.BLUE
        Off = Rgb.WHITE_HALF
        Held = Rgb.BLUE_PULSE
        Option = Rgb.BLACK
        OptionInRange = Rgb.BLUE_PULSE
        OptionHeld = Rgb.BLUE

    class Transport(object):
        PlayOff = Mono.OFF
        PlayOn = Mono.ON
        ContinueOff = Mono.OFF
        ContinueOn = Mono.HALF
        CaptureOff = Mono.OFF
        CaptureOn = Mono.HALF
        MetronomeOff = Rgb.RED_HALF
        MetronomeOn = Rgb.AQUA

    class Action(object):
        Undo = Rgb.CREAM
        UndoPressed = Rgb.WHITE
        Redo = Rgb.CREAM
        RedoPressed = Rgb.WHITE
        Delete = Rgb.WHITE_HALF
        DeletePressed = Rgb.WHITE
        Duplicate = Rgb.WHITE_HALF
        DuplicatePressed = Rgb.WHITE
        Quantize = Rgb.WHITE_HALF
        QuantizePressed = Rgb.WHITE
        Double = Rgb.CREAM
        DoublePressed = Rgb.WHITE

    class Session(object):
        RecordButton = Rgb.RED_HALF
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipEmpty = Rgb.BLACK
        Scene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF
        Navigation = Rgb.WHITE_HALF
        NavigationPressed = Rgb.WHITE
        Select = Rgb.WHITE_HALF
        SelectPressed = Rgb.WHITE
        Delete = Rgb.WHITE_HALF
        DeletePressed = Rgb.WHITE
        Duplicate = Rgb.WHITE_HALF
        DuplicatePressed = Rgb.WHITE
        Quantize = Rgb.WHITE_HALF
        QuantizePressed = Rgb.WHITE
        Double = Rgb.CREAM
        DoublePressed = Rgb.WHITE
        ActionTriggered = Rgb.WHITE

    class Zooming(object):
        Selected = Rgb.OFF_WHITE
        Stopped = Rgb.LIGHT_BLUE_HALF
        Playing = Rgb.GREEN_PULSE
        Empty = Rgb.BLACK

    class Mixer(object):
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        EmptyTrack = Rgb.BLACK
        TrackSelected = Rgb.WHITE
        TrackNotSelected = Rgb.WHITE_HALF

    class DrumGroup(object):
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadAction = Rgb.WHITE
        Navigation = Rgb.YELLOW_HALF
        NavigationPressed = Rgb.YELLOW

    class Mode(object):

        class Volume(object):
            On = Rgb.GREEN
            Off = Rgb.WHITE_HALF

        class Pan(object):
            On = Rgb.ORANGE
            Off = Rgb.WHITE_HALF

        class SendA(object):
            On = Rgb.VIOLET
            Off = Rgb.WHITE_HALF

        class SendB(object):
            On = Rgb.DARK_BLUE
            Off = Rgb.WHITE_HALF

        class Stop(object):
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Mute(object):
            On = Rgb.YELLOW
            Off = Rgb.WHITE_HALF

        class Solo(object):
            On = Rgb.BLUE
            Off = Rgb.WHITE_HALF

        class Arm(object):
            On = Rgb.RED
            Off = Rgb.WHITE_HALF

        class Launch(object):
            On = Rgb.WHITE_HALF


skin = Skin(Colors)
