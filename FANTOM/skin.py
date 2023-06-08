# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/skin.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 1167 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface import Skin, default_skin, merge_skins
from ableton.v3.control_surface.elements import SimpleColor
from .colors import Basic, Rgb
STOPPED = SimpleColor(4)
TRIGGERED_PLAY = SimpleColor(7)

class Colors:

    class DefaultButton:
        Disabled = Basic.DISABLED

    class Session:
        ClipStopped = STOPPED
        ClipRecordButton = SimpleColor(2)
        SlotLacksStop = SimpleColor(5)
        SlotTriggeredPlay = SimpleColor(1)
        ClipTriggeredPlay = TRIGGERED_PLAY
        SlotTriggeredRecord = SimpleColor(3)
        ClipTriggeredRecord = SimpleColor(9)
        ClipStarted = SimpleColor(6)
        ClipRecording = SimpleColor(8)
        Scene = STOPPED
        SceneTriggered = TRIGGERED_PLAY

    class DrumGroup:
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE


skin = merge_skins(default_skin, Skin(Colors))