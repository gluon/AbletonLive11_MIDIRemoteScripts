# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\midi_message_cache.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 754 bytes
from __future__ import absolute_import, print_function, unicode_literals
from .sysex import NUM_SET_PROPERTY_HEADER_BYTES

class MidiMessageCache:

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._messages = []

    def __call__(self, message):
        self._messages = list(filter(lambda m: m[:NUM_SET_PROPERTY_HEADER_BYTES] != message[:NUM_SET_PROPERTY_HEADER_BYTES]
, self._messages))
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages

    def clear(self):
        self._messages = []