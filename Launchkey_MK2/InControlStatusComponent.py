# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\InControlStatusComponent.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 733 bytes
from __future__ import absolute_import, print_function, unicode_literals
import _Framework.ControlSurfaceComponent as ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class InControlStatusComponent(ControlSurfaceComponent):

    def __init__(self, set_is_in_control_on, *a, **k):
        (super(InControlStatusComponent, self).__init__)(*a, **k)
        self._set_is_in_control_on = set_is_in_control_on

    def set_in_control_status_button(self, button):
        self._on_in_control_value.subject = button

    @subject_slot('value')
    def _on_in_control_value(self, value):
        self._set_is_in_control_on(value >= 8)