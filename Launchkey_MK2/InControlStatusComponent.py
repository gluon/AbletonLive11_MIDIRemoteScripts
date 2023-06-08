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