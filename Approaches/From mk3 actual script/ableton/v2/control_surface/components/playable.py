#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/playable.py
from __future__ import absolute_import, print_function, unicode_literals
from numbers import Number
from ...base import listenable_property
from ..component import Component
from ..control import PlayableControl, ButtonControl, control_matrix
from . import AccentComponent

def apply_to_list(original_list, operation, item):
    list_copy = original_list[:]
    getattr(list_copy, operation)(item)
    return list_copy


class PlayableComponent(Component):
    matrix = control_matrix(PlayableControl)
    select_button = ButtonControl()
    pressed_pads = listenable_property.managed([])

    def __init__(self, *a, **k):
        super(PlayableComponent, self).__init__(*a, **k)
        self._takeover_pads = False
        self._accent_component = AccentComponent(parent=self)

    def set_accent_button(self, button):
        self._accent_component.accent_button.set_control_element(button)

    def set_full_velocity(self, full_velocity):
        self._accent_component.set_full_velocity(full_velocity)

    def _set_control_pads_from_script(self, takeover_pads):
        u"""
        If takeover_pads, the matrix buttons will be controlled from
        the script. Otherwise they send midi notes to the track
        associated to the instrument.
        """
        if takeover_pads != self._takeover_pads:
            self._takeover_pads = takeover_pads
            self._update_control_from_script()

    def _update_control_from_script(self):
        takeover_pads = self._takeover_pads or len(self.pressed_pads) > 0
        mode = PlayableControl.Mode.listenable if takeover_pads else PlayableControl.Mode.playable
        for button in self.matrix:
            button.set_mode(mode)

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        self._reset_selected_pads()
        self._update_led_feedback()
        self._update_note_translations()

    @matrix.pressed
    def matrix(self, button):
        self._on_matrix_pressed(button)

    @matrix.released
    def matrix(self, button):
        self._on_matrix_released(button)

    def _on_matrix_pressed(self, button):
        self.pressed_pads = apply_to_list(self.pressed_pads, u'append', button)
        if len(self.pressed_pads) == 1:
            self._update_control_from_script()

    def _on_matrix_released(self, button):
        if button in self.pressed_pads:
            self.pressed_pads = apply_to_list(self.pressed_pads, u'remove', button)
            if not self.pressed_pads:
                self._update_control_from_script()
        self._update_led_feedback()

    @select_button.value
    def select_button(self, value, button):
        self._set_control_pads_from_script(bool(value))

    def _reset_selected_pads(self):
        if self.pressed_pads:
            self.pressed_pads = []
            self._update_control_from_script()

    def _update_led_feedback(self):
        for button in self.matrix:
            self._update_button_color(button)

    def _update_button_color(self, button):
        button.color = u'DefaultButton.Off'

    def _button_should_be_enabled(self, button):
        identifier, _ = self._note_translation_for_button(button)
        return identifier is None or isinstance(identifier, Number) and identifier < 128

    def _note_translation_for_button(self, button):
        return (button.identifier, button.channel)

    def _update_note_translations(self):
        for button in self.matrix:
            if self._button_should_be_enabled(button):
                self._set_button_control_properties(button)
                button.enabled = True
            else:
                button.enabled = False

    def _set_button_control_properties(self, button):
        identifier, channel = self._note_translation_for_button(button)
        button.identifier = identifier
        button.channel = channel

    def update(self):
        super(PlayableComponent, self).update()
        if self.is_enabled():
            self._set_control_pads_from_script(False)

    @property
    def width(self):
        if self.matrix.width:
            return self.matrix.width
        return 4

    @property
    def height(self):
        if self.matrix.height:
            return self.matrix.height
        return 4
