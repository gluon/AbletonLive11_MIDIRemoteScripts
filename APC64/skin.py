# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\skin.py
# Compiled at: 2023-06-08 07:52:37
# Size of source mod 2**32: 3522 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .colors import Basic, Rgb, make_color_for_liveobj

class Skin:

    class Transport:
        PlayOn = Basic.FULL
        PlayOff = Basic.HALF
        StopOn = Basic.HALF
        StopOff = Basic.HALF
        StopPressed = Basic.FULL
        RecordQuantizeOn = Basic.FULL
        RecordQuantizeOff = Basic.HALF

    class Recording:
        ArrangementRecordOn = Basic.FULL
        ArrangementRecordOff = Basic.HALF
        ArrangementOverdubOn = Basic.FULL
        ArrangementOverdubOff = Basic.HALF
        SessionRecordOn = Basic.FULL
        SessionRecordTransition = Basic.BLINK
        SessionRecordOff = Basic.HALF
        SessionOverdubOn = Basic.FULL
        SessionOverdubOff = Basic.HALF

    class UndoRedo:
        Undo = Basic.HALF
        Redo = Basic.HALF

    class ViewControl:
        Track = Basic.HALF

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        MuteOn = Rgb.YELLOW
        MuteOff = Rgb.YELLOW_HALF
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_HALF
        Selected = Rgb.WHITE
        NotSelected = make_color_for_liveobj

    class Session:
        SlotRecordButton = Rgb.RED_HALF
        ClipStopped = make_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        Scene = Basic.HALF
        SceneTriggered = Basic.BLINK
        StopClipTriggered = Rgb.GREEN_BLINK
        StopClip = Rgb.GREEN
        StopClipDisabled = Rgb.GREEN_HALF
        StopAllClips = Basic.HALF
        Navigation = Basic.HALF

    class Zooming:
        Selected = Rgb.AMBER
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.OFF

    class Device:
        Navigation = Basic.HALF

        class Bank:
            Navigation = Basic.HALF

    class DrumGroup:
        PadEmpty = Rgb.GREY
        PadFilled = make_color_for_liveobj
        PadSelected = Rgb.WHITE
        PadMuted = Rgb.AMBER
        PadMutedSelected = Rgb.WHITE
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.WHITE
        Scroll = Basic.HALF

    class ModifierBackground:
        ClearButton = Basic.HALF
        DuplicateButton = Basic.HALF
        QuantizeButton = Basic.HALF

    class Settings:
        FixedLengthOn = Basic.FULL
        FixedLengthOff = Basic.HALF

    class GlobalQuantization:
        NotSelected = Rgb.GREY
        Selected = Rgb.WHITE

    class EncoderModes:

        class Tempo:
            On = None
            Off = None

        class FixedLength:
            On = None
            Off = None

        class Quantize:
            On = None
            Off = None

    class TouchStripModes:

        class Device:
            Off = Basic.HALF

        class Volume:
            Off = Basic.HALF

        class Pan:
            Off = Basic.HALF

        class Send:
            Off = Basic.HALF

        class ChannelStrip:
            Off = Basic.HALF

        class Off:
            Off = Basic.HALF

    class TrackStateModes:

        class Arm:
            Off = Basic.HALF

        class Mute:
            Off = Basic.HALF

        class Solo:
            Off = Basic.HALF

        class ClipStop:
            Off = Basic.HALF