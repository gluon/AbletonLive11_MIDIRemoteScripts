# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/midi_message_cache.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 792 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import filter, object
from .sysex import NUM_SET_PROPERTY_HEADER_BYTES

class MidiMessageCache(object):

    def __init__(self, *a, **k):
        (super(MidiMessageCache, self).__init__)(*a, **k)
        self._messages = []

    def __call__(self, message):
        self._messages = list(filter(lambda m: m[:NUM_SET_PROPERTY_HEADER_BYTES] != message[:NUM_SET_PROPERTY_HEADER_BYTES], self._messages))
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages

    def clear(self):
        self._messages = []