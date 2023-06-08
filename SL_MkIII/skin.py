from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from novation.colors import Rgb

class Colors:

    class DefaultButton:
        On = Rgb.GREEN
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Session:
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

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        MuteOn = Rgb.YELLOW_HALF
        MuteOff = Rgb.YELLOW
        Pan = Rgb.ORANGE
        TrackSelect = Rgb.WHITE
        Send = Rgb.WHITE

    class Monitor:
        In = Rgb.LIGHT_BLUE
        Auto = Rgb.YELLOW
        Off = Rgb.YELLOW
        Disabled = Rgb.YELLOW_HALF

    class Transport:
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

    class Recording:
        On = Rgb.RED
        Off = Rgb.RED_HALF
        Transition = Rgb.BLACK

    class Mode:

        class Mute:
            On = Rgb.YELLOW

        class Solo:
            On = Rgb.BLUE

        class Monitor:
            On = Rgb.GREEN

        class Arm:
            On = Rgb.RED

        class Devices:
            On = Rgb.PURPLE
            Off = Rgb.PURPLE

        class Pan:
            On = Rgb.ORANGE
            Off = Rgb.ORANGE

        class Sends:
            On = Rgb.WHITE
            Off = Rgb.WHITE

    class DrumGroup:
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

    class ItemNavigation:
        NoItem = Rgb.BLACK
        ItemSelected = Rgb.PURPLE
        ItemNotSelected = Rgb.PURPLE_HALF

    class Device:
        On = Rgb.PURPLE

    class TrackNavigation:
        On = Rgb.LIGHT_BLUE
        Pressed = Rgb.LIGHT_BLUE

    class SceneNavigation:
        On = Rgb.WHITE
        Pressed = Rgb.WHITE

    class Action:
        Available = Rgb.WHITE


skin = Skin(Colors)