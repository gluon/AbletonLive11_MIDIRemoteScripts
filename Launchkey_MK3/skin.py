# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\skin.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 909 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin, merge_skins
from novation.colors import Mono, Rgb
from novation.skin import skin as base_skin

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