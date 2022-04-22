# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/slider.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 531 bytes
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ..input_control_element import MIDI_NOTE_TYPE
from .encoder import EncoderElement

class SliderElement(EncoderElement):

    def __init__(self, msg_type, channel, identifier, *a, **k):
        (super(SliderElement, self).__init__)(
 msg_type, channel, identifier, *a, map_mode=Live.MidiMap.MapMode.absolute, **k)