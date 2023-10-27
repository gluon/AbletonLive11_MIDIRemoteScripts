# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\firmware_mode.py
# Compiled at: 2023-09-17 09:50:55
# Size of source mod 2**32: 1706 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.elements import SysexElement

class FirmwareModeElement(SysexElement):

    def __init__(self, *a, **k):
        (super().__init__)(*a, **k)
        self._suppress_next_send_value = False

    def receive_value(self, value):
        self._suppress_next_send_value = True
        super().receive_value(value)

    def send_value(self, *a, **k):
        if self._suppress_next_send_value:
            self._suppress_next_send_value = False
            return
        (super().send_value)(*a, **k)

    def clear_send_cache(self):
        self._suppress_next_send_value = True