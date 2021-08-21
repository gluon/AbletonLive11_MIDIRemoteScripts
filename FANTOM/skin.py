# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/skin.py
# Compiled at: 2021-08-06 01:27:35
# Size of source mod 2**32: 1817 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
from .colors import Basic, Rgb
STOPPED = Color(4)
TRIGGERED_PLAY = Color(7)

class Colors:

    class DefaultButton:
        On = Basic.ON
        Off = Basic.OFF
        Disabled = Basic.DISABLED

    class Transport:
        PlayOn = Basic.ON
        PlayOff = Basic.OFF
        CaptureOn = Basic.ON
        CaptureOff = Basic.DISABLED

    class Recording:
        On = Basic.ON
        Off = Basic.OFF
        Transition = Basic.ON

    class Automation:
        On = Basic.ON
        Off = Basic.OFF

    class Mixer:
        ArmOn = Basic.ON
        ArmOff = Basic.OFF
        SoloOn = Basic.ON
        SoloOff = Basic.OFF
        MuteOn = Basic.ON
        MuteOff = Basic.OFF

    class Session:
        ClipEmpty = Basic.OFF
        ClipStopped = STOPPED
        RecordButton = Color(2)
        SlotLacksStop = Color(5)
        SlotTriggeredPlay = Color(1)
        ClipTriggeredPlay = TRIGGERED_PLAY
        SlotTriggeredRecord = Color(3)
        ClipTriggeredRecord = Color(9)
        ClipStarted = Color(6)
        ClipRecording = Color(8)
        NoScene = Basic.OFF
        Scene = STOPPED
        SceneTriggered = TRIGGERED_PLAY
        StopClipTriggered = Basic.ON
        StopClip = Basic.OFF
        StopClipDisabled = Basic.OFF

    class DrumGroup:
        PadEmpty = Basic.OFF
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE


skin = Skin(Colors)