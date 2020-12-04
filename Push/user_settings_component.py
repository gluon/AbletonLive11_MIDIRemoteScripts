#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/user_settings_component.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from builtins import range
from past.utils import old_div
from itertools import count
from ableton.v2.base import forward_property, listens_group
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.elements import adjust_string, DisplayDataSource
from pushbase.user_component import UserComponentBase
from pushbase import consts

def combine_strings(string1, string2, length):
    part_length = old_div(length - 1, 2)
    return u'{} {}'.format(adjust_string(string1, part_length), adjust_string(string2, part_length))


class UserSettingsComponent(Component):
    u""" Component for changing a list of settings """

    def __init__(self, *a, **k):
        super(UserSettingsComponent, self).__init__(*a, **k)
        self._name_sources = [ DisplayDataSource() for _ in range(4) ]
        self._value_sources = [ DisplayDataSource() for _ in range(4) ]
        self._info_source = DisplayDataSource()
        self._settings = []
        self._encoders = []
        self._value_display = None
        self._name_display = None

    def set_display_line1(self, display):
        self._value_display = display
        if display:
            display.set_data_sources(self._value_sources)

    def set_display_line2(self, display):
        self._name_display = display
        if display:
            display.set_data_sources(self._name_sources)

    def set_display_line3(self, display):
        if display:
            display.reset()

    def set_display_line4(self, display):
        if display:
            display.set_data_sources([self._info_source])

    def set_encoders(self, encoders):
        self._encoders = encoders or []
        self._on_encoder_value.replace_subjects(self._encoders, count())

    def _set_settings(self, settings):
        self._settings = list(settings.values())
        self._update_display()

    def _get_settings(self):
        return self._settings

    settings = property(_get_settings, _set_settings)

    def set_info_text(self, info_text):
        self._info_source.set_display_string(info_text)

    @listens_group(u'normalized_value')
    def _on_encoder_value(self, value, index):
        num_encoders = len(self._encoders)
        setting_index = -1
        if index % 2 == 0:
            setting_index = old_div(index, 2)
        elif index == num_encoders - 1:
            setting_index = old_div(num_encoders, 2)
        if 0 <= setting_index < len(self._settings) and self._settings[setting_index].change_relative(value):
            self._update_display()

    def _update_display(self):
        num_segments = len(self._name_sources)
        num_settings = len(self._settings)

        def setting_property(index, display, getter):
            value = getter(self._settings[index]) if 0 <= index < num_settings else u''
            index += 1
            if index == num_segments and index < num_settings:
                separators = num_segments - 1
                segment_length = old_div(display.width - separators, num_segments) if display else consts.DISPLAY_LENGTH
                value = combine_strings(value, getter(self._settings[index]), segment_length)
            return value

        for index in range(num_segments):
            self._name_sources[index].set_display_string(setting_property(index, self._name_display, lambda s: s.name))
            self._value_sources[index].set_display_string(setting_property(index, self._value_display, lambda s: str(s)))

    def update(self):
        super(UserSettingsComponent, self).update()
        if self.is_enabled():
            self._update_display()


class UserComponent(UserComponentBase):
    action_button = ButtonControl(**consts.SIDE_BUTTON_COLORS)
    settings_layer = forward_property(u'_settings')(u'layer')
    settings = forward_property(u'_settings')(u'settings')

    def __init__(self, *a, **k):
        super(UserComponent, self).__init__(*a, **k)
        self._settings = UserSettingsComponent(parent=self)
        self._settings.set_enabled(False)

    @action_button.pressed_delayed
    def action_button(self, button):
        self._settings.set_enabled(True)

    @action_button.released_delayed
    def hide_settings(self, button):
        self._settings.set_enabled(False)

    def set_settings_info_text(self, text):
        self._settings.set_info_text(text)

    @action_button.released_immediately
    def post_trigger_action(self, button):
        self.toggle_mode()
