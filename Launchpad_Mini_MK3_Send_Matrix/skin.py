#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_Mini_MK3/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import object
from ableton.v2.control_surface import merge_skins, Skin
from ableton.v2.control_surface.elements import Color
from novation.colors import Rgb
from novation.skin import skin as base_skin

class Colors(object):

    class Mode(object):

        class Session(object):
            Launch = Color((Rgb.PALE_GREEN_HALF.midi_value, Rgb.WHITE_HALF.midi_value))
            Overview = Color((Rgb.BLUE.midi_value, Rgb.WHITE_HALF.midi_value))


skin = merge_skins(*(base_skin, Skin(Colors)))
