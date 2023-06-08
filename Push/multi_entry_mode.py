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