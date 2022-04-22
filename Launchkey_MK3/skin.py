# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK3/skin.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 873 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin, merge_skins
from novation.colors import Mono, Rgb
import novation.skin as base_skin

class Colors:

    class DefaultButton:
        On = Mono.ON

    class TrackNavigation:
        On = Mono.HALF
        Pressed = Mono.ON

    class Device:
        Navigation = Rgb.PURPLE_HALF
        NavigationPressed = Rgb.PURPLE

    class DrumGroup:
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.WHITE
        PadMutedSelected = Rgb.WHITE
        PadSoloedSelected = Rgb.WHITE

    class Mode:

        class Device:

            class Bank:
                Selected = Rgb.PURPLE
                Available = Rgb.PURPLE_HALF


skin = merge_skins(base_skin, Skin(Colors)*())