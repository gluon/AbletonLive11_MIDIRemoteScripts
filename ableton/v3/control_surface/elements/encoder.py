# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/elements/encoder.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 684 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as EncoderElementBase
from ableton.v2.control_surface.elements.encoder import _map_modes
from .. import MIDI_CC_TYPE

class EncoderElement(EncoderElementBase):

    def __init__(self, identifier, channel=0, msg_type=MIDI_CC_TYPE, map_mode=_map_modes.absolute, needs_takeover=True, *a, **k):
        (super().__init__)(msg_type, channel, identifier, map_mode, *a, **k)
        self.set_needs_takeover(needs_takeover)