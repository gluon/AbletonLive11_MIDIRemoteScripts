# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\mode.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 650 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import Mode

class ExtendComboElementMode(Mode):

    def __init__(self, combo_pairs=None, *a, **k):
        (super(ExtendComboElementMode, self).__init__)(*a, **k)
        self._combo_pairs = combo_pairs

    def enter_mode(self):
        for combo, nested in self._combo_pairs:
            combo.register_control_element(nested)

    def leave_mode(self):
        for combo, nested in self._combo_pairs:
            combo.unregister_control_element(nested)