#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOMSQ/translating_background.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BackgroundComponent
from ableton.v2.control_surface.control import RadioButtonGroup
from .midi import USER_MODE_START_CHANNEL

class TranslatingBackgroundComponent(BackgroundComponent):
    channel_selection_buttons = RadioButtonGroup(control_count=6, channel=USER_MODE_START_CHANNEL)

    def __init__(self, *a, **k):
        super(TranslatingBackgroundComponent, self).__init__(*a, **k)
        self.channel_selection_buttons.checked_index = 0

    def set_channel_selection_buttons(self, buttons):
        self.channel_selection_buttons.set_control_element(buttons)

    @channel_selection_buttons.checked
    def channel_selection_buttons(self, button):
        self._set_channel_of_all_controls(button.index)

    def _clear_control(self, name, control):
        prior_control_group = self._control_map.get(name, None)
        if prior_control_group:
            for c in prior_control_group:
                c.use_default_message()

            prior_control_group.reset()
        super(TranslatingBackgroundComponent, self)._clear_control(name, control)
        self._set_channel_of_all_controls(self.channel_selection_buttons.checked_index)

    def _set_channel_of_all_controls(self, channel_offset):
        for control in self._control_map.values():
            if control:
                control.set_channel(channel_offset + USER_MODE_START_CHANNEL)
