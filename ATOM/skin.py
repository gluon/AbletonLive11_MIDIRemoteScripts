from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v3.control_surface import BasicColors
from .colors import Rgb, create_color_for_liveobj

class Skin:

    class DefaultButton:
        Disabled = Rgb.BLACK

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        ImplicitArmOn = Rgb.RED
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        Selected = Rgb.WHITE
        NotSelected = Rgb.BLACK
        Empty = Rgb.BLACK

    class Session:
        Slot = Rgb.BLACK
        SlotRecordButton = Rgb.RED_HALF
        NoSlot = Rgb.BLACK
        ClipStopped = create_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        Scene = partial(create_color_for_liveobj, is_scene=True)
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class Zooming:
        Selected = Rgb.WHITE
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class NotePad:
        Pressed = Rgb.RED

    class Keyboard:
        Natural = Rgb.YELLOW
        Sharp = Rgb.BLUE

    class DrumGroup:
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.WHITE
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

    class EncoderModes:

        class Volume:
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF

        class Pan:
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF

        class SendA:
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF

        class SendB:
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF

    class SessionNavigationModes:

        class Default:
            On = BasicColors.OFF

    class TopLevelModes:

        class Default:
            On = BasicColors.OFF