# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\mode.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 677 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import ImmediateBehaviour

class ReenterBehaviour(ImmediateBehaviour):

    def __init__(self, on_reenter=None, *a, **k):
        (super(ReenterBehaviour, self).__init__)(*a, **k)
        self.on_reenter = on_reenter

    def press_immediate(self, component, mode):
        was_active = component.selected_mode == mode
        super(ReenterBehaviour, self).press_immediate(component, mode)
        if was_active:
            self.on_reenter()