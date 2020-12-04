#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/mode.py
from __future__ import absolute_import, print_function, unicode_literals
from future.moves.itertools import zip_longest
from ableton.v2.base import clamp, listens
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, control_list
from ableton.v2.control_surface.mode import ModesComponent, make_mode_button_control, to_camel_case_name
from .control import BinaryControl, TextDisplayControl
MAX_MODE_NUMBER = 8

class NavigatableModesComponent(ModesComponent):
    prev_mode_button = ButtonControl()
    next_mode_button = ButtonControl()

    def __init__(self, *a, **k):
        super(NavigatableModesComponent, self).__init__(*a, **k)
        self.__on_selected_mode_changed.subject = self

    @prev_mode_button.pressed
    def prev_mode_button(self, _):
        self._navigate_mode(-1)

    @next_mode_button.pressed
    def next_mode_button(self, _):
        self._navigate_mode(1)

    def _update_mode_nav_buttons(self):
        self.prev_mode_button.enabled = self._mode_list and self.selected_mode != self._mode_list[0]
        self.next_mode_button.enabled = self._mode_list and self.selected_mode != self._mode_list[-1]

    def _navigate_mode(self, direction):
        new_index = 0
        if self.selected_mode:
            old_index = self._mode_list.index(self.selected_mode)
            new_index = clamp(old_index + direction, 0, len(self._mode_list) - 1)
        self.selected_mode = self._mode_list[new_index]
        self._update_mode_nav_buttons()

    @listens(u'selected_mode')
    def __on_selected_mode_changed(self, _):
        self._update_selected_mode()

    def _update_selected_mode(self):
        self._update_mode_nav_buttons()


class DisplayingNavigatableModesComponent(NavigatableModesComponent):
    display_1 = TextDisplayControl(segments=(u'',))
    display_2 = TextDisplayControl(segments=(u'',))
    color_field_1 = ColorSysexControl()
    color_field_2 = ColorSysexControl()

    def _update_selected_mode(self):
        super(DisplayingNavigatableModesComponent, self)._update_selected_mode()
        self._update_mode_displays()

    def _update_mode_displays(self):
        if self.selected_mode:
            for display, color_field, name in zip_longest((self.display_1, self.display_2), (self.color_field_1, self.color_field_2), self.selected_mode.split(u'_')[:2]):
                display[0] = name.capitalize() if name else u''
                color_field.color = u'Mode.{}.On'.format(name.capitalize()) if name else u'DefaultButton.Disabled'


class DisplayingSkinableModesComponent(ModesComponent):
    mode_display = TextDisplayControl(segments=(u'',) * MAX_MODE_NUMBER)
    mode_color_fields = control_list(ColorSysexControl, MAX_MODE_NUMBER)
    mode_selection_fields = control_list(BinaryControl, MAX_MODE_NUMBER)
    selected_mode_color_field = ColorSysexControl()

    def __init__(self, *a, **k):
        super(DisplayingSkinableModesComponent, self).__init__(enable_skinning=True, *a, **k)
        self.__on_selected_mode_changed.subject = self

    def add_mode_button_control(self, mode_name, behaviour):
        super(DisplayingSkinableModesComponent, self).add_mode_button_control(mode_name, behaviour)
        self.mode_display[len(self._mode_list) - 1] = to_camel_case_name(mode_name, separator=u' ')
        self.mode_color_fields[len(self._mode_list) - 1].color = u'Mode.' + to_camel_case_name(mode_name) + u'.On'

    @listens(u'selected_mode')
    def __on_selected_mode_changed(self, _):
        self._update_selection_fields()
        self._update_selected_mode_color_field()

    def _update_selection_fields(self):
        for field, mode in zip(self.mode_selection_fields, self._mode_list):
            field.is_on = mode == self.selected_mode

    def _update_selected_mode_color_field(self):
        self.selected_mode_color_field.color = u'Mode.{}.On'.format(to_camel_case_name(self.selected_mode)) if self.selected_mode else u'DefaultButton.Disabled'
