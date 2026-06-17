# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\multi_entry_mode.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1096 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import Mode, tomode

class MultiEntryMode(Mode):

    def __init__(self, mode=None, *a, **k):
        (super(MultiEntryMode, self).__init__)(*a, **k)
        self._mode = tomode(mode)
        self._entry_count = 0

    def enter_mode(self):
        if self._entry_count == 0:
            self._mode.enter_mode()
        self._entry_count += 1

    def leave_mode(self):
        if self._entry_count == 1:
            self._mode.leave_mode()
        self._entry_count -= 1

    @property
    def is_entered(self):
        return self._entry_count > 0