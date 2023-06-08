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