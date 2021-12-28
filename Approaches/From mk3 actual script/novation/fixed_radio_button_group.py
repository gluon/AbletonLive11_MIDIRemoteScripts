#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/novation/fixed_radio_button_group.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.control import RadioButtonGroup

class FixedRadioButtonGroup(RadioButtonGroup):
    u"""
    RadioButtonGroup of a fixed size that always listens to the controls it's given to
    prevent unused controls from leaking into the track input.  Use active_control_count
    instead of control_count to set the number of controls that should be active in the
    group. Inactive controls will be disabled.
    """

    def __init__(self, control_count, *a, **k):
        super(FixedRadioButtonGroup, self).__init__(control_count=control_count, *a, **k)

    class State(RadioButtonGroup.State):

        @property
        def active_control_count(self):
            return self._active_control_count

        @active_control_count.setter
        def active_control_count(self, control_count):
            self._active_control_count = control_count
            for index, control in enumerate(self._controls):
                control._get_state(self._manager).enabled = index < control_count
