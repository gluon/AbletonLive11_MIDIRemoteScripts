from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import RadioButtonGroup

class FixedRadioButtonGroup(RadioButtonGroup):

    def __init__(self, control_count, *a, **k):
        (super(FixedRadioButtonGroup, self).__init__)(a, control_count=control_count, **k)

    class State(RadioButtonGroup.State):

        @property
        def active_control_count(self):
            return self._active_control_count

        @active_control_count.setter
        def active_control_count(self, control_count):
            self._active_control_count = control_count
            for index, control in enumerate(self._controls):
                control._get_state(self._manager).enabled = index < control_count