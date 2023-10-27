# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\colors.py
# Compiled at: 2023-06-30 09:18:52
# Size of source mod 2**32: 3456 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import BasicColors
from ableton.v3.control_surface.elements import FallbackColor, create_rgb_color
from ableton.v3.live import liveobj_color_to_midi_rgb_values

def create_color(r, g, b):
    return create_rgb_color((r, g, b, 32))


def create_blinking_color(r, g, b):
    return create_rgb_color((r, g, b, 2))


class Rgb:
    OFF = FallbackColor(create_color(0, 0, 0), BasicColors.OFF)
    WHITE_HALF = create_color(32, 32, 32)
    WHITE = create_color(127, 127, 127)
    RED = create_color(127, 0, 0)
    RED_HALF = create_color(32, 0, 0)
    RED_LOW = create_color(16, 0, 0)
    RED_BLINK = create_blinking_color(127, 0, 0)
    GREEN = create_color(0, 127, 0)
    GREEN_HALF = create_color(0, 32, 0)
    GREEN_BLINK = create_blinking_color(0, 127, 0)
    BLUE = create_color(0, 0, 127)
    OCEAN = create_color(20, 80, 127)
    AMBER = create_color(127, 50, 0)
    AMBER_HALF = create_color(20, 5, 0)
    YELLOW = create_color(127, 72, 0)
    YELLOW_HALF = create_color(32, 24, 0)


class Skin:

    class DefaultButton:
        On = Rgb.WHITE
        Off = Rgb.OFF
        Disabled = Rgb.OFF

    class Transport:
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.GREEN_HALF
        StopOn = Rgb.WHITE
        StopOff = Rgb.WHITE_HALF
        LoopOn = Rgb.YELLOW
        LoopOff = Rgb.YELLOW_HALF
        MetronomeOn = Rgb.WHITE
        MetronomeOff = Rgb.WHITE_HALF
        TapTempoPressed = Rgb.WHITE
        TapTempo = Rgb.WHITE_HALF
        SeekPressed = Rgb.WHITE
        Seek = Rgb.WHITE_HALF
        CanCaptureMidi = Rgb.WHITE

    class Recording:
        ArrangementRecordOn = Rgb.RED
        ArrangementRecordOff = Rgb.RED_HALF
        SessionRecordOn = Rgb.RED
        SessionRecordTransition = Rgb.RED_BLINK
        SessionRecordOff = Rgb.RED_HALF

    class UndoRedo:
        UndoPressed = Rgb.WHITE
        Undo = Rgb.WHITE_HALF
        RedoPressed = Rgb.WHITE
        Redo = Rgb.WHITE_HALF

    class ClipActions:
        Quantize = Rgb.WHITE_HALF
        QuantizePressed = Rgb.WHITE

    class ViewControl:
        TrackPressed = Rgb.WHITE
        Track = Rgb.WHITE_HALF

    class ViewToggle:
        SessionOn = Rgb.WHITE
        SessionOff = Rgb.WHITE_HALF

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_HALF
        NoTrack = Rgb.OFF

    class Session:
        Slot = Rgb.OFF
        SlotRecordButton = Rgb.RED_LOW
        NoSlot = Rgb.OFF
        ClipStopped = lambda x: create_color(*liveobj_color_to_midi_rgb_values(x))
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN
        ClipRecording = Rgb.RED

    class DrumGroup:
        PadEmpty = Rgb.WHITE_HALF
        PadFilled = lambda x: create_color(*liveobj_color_to_midi_rgb_values(x))
        PadSelected = Rgb.OCEAN
        PadMuted = Rgb.AMBER
        PadMutedSelected = Rgb.OCEAN
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.OCEAN
        PadPressed = Rgb.WHITE

    class Banking:
        PageOne = Rgb.WHITE_HALF
        PageTwo = Rgb.WHITE

    class ContinuousControlModes:

        class Device:
            On = Rgb.WHITE_HALF

        class Mixer:
            On = Rgb.WHITE