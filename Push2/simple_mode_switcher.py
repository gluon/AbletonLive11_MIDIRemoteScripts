#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push2/simple_mode_switcher.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const
from pushbase.note_layout_switcher import ModeSwitcherBase

class SimpleModeSwitcher(ModeSwitcherBase):

    def __init__(self, session_modes = None, *a, **k):
        assert session_modes is not None
        super(SimpleModeSwitcher, self).__init__(*a, **k)
        self._session_modes = session_modes
        self._cycle_mode = session_modes.cycle_mode
        self._get_current_alternative_mode = const(session_modes)

    def _unlock_alternative_mode(self, locked_mode):
        super(SimpleModeSwitcher, self)._unlock_alternative_mode(locked_mode)
        self.locked_mode = None
