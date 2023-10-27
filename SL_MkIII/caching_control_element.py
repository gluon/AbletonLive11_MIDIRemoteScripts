# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\caching_control_element.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 650 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface import ControlElement
from .sysex import SET_PROPERTY_MSG_HEADER

class CachingControlElement(ControlElement):

    @depends(message_cache=None)
    def __init__(self, message_cache=None, *a, **k):
        (super().__init__)(*a, **k)
        self._message_cache = message_cache

    def send_midi(self, message, **_):
        self._message_cache(message[len(SET_PROPERTY_MSG_HEADER):-1])

    def reset(self):
        pass