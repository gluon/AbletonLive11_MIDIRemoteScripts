# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/caching_control_element.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 638 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface import ControlElement
from .sysex import SET_PROPERTY_MSG_HEADER

class CachingControlElement(ControlElement):

    @depends(message_cache=None)
    def __init__(self, message_cache=None, *a, **k):
        (super(CachingControlElement, self).__init__)(*a, **k)
        self._message_cache = message_cache

    def send_midi(self, midi_event_bytes, **k):
        self._message_cache(midi_event_bytes[len(SET_PROPERTY_MSG_HEADER):-1])