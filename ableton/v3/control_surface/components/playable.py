from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import listenable_property
from .. import Component
from ..controls import ButtonControl, PlayableControl, control_matrix

class PlayableComponent(Component):
    matrix = control_matrix(PlayableControl, color=None)
    select_button = ButtonControl(color=None)
    pressed_pads = listenable_property.managed([])

    def __init__(self, name='Playable', matrix_always_listenable=False, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._takeover_pads = False
        self._default_playable_mode = PlayableControl.Mode.playable_and_listenable if matrix_always_listenable else PlayableControl.Mode.playable
        self.matrix._control_type = partial(PlayableControl,
          mode=(self._default_playable_mode))

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

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        self._reset_selected_pads()
        self._update_led_feedback()
        self._update_note_translations()

    def _set_control_pads_from_script(self, takeover_pads):
        if takeover_pads != self._takeover_pads:
            self._takeover_pads = takeover_pads
            self._update_control_from_script()

    def _update_control_from_script(self):
        takeover_pads = self._takeover_pads or len(self.pressed_pads) > 0
        mode = PlayableControl.Mode.listenable if takeover_pads else self._default_playable_mode
        for button in self.matrix:
            button.set_mode(mode)

    @matrix.pressed
    def matrix(self, button):
        self._on_matrix_pressed(button)

    @matrix.released
    def matrix(self, button):
        self._on_matrix_released(button)

    def _on_matrix_pressed(self, button):
        self.pressed_pads = self.pressed_pads + [button]
        if len(self.pressed_pads) == 1:
            self._update_control_from_script()

    def _on_matrix_released(self, button):
        if button in self.pressed_pads:
            self.pressed_pads = [p for p in self.pressed_pads if p is not button]
            if not self.pressed_pads:
                self._update_control_from_script()
        self._update_led_feedback()

    @select_button.value
    def select_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    def _update_led_feedback(self):
        for button in self.matrix:
            self._update_button_color(button)

    def _update_button_color(self, button):
        pass

    def _update_note_translations(self):
        for button in self.matrix:
            if self._button_should_be_enabled(button):
                self._set_button_control_properties(button)
                button.enabled = True
            else:
                button.enabled = False

    def _reset_selected_pads(self):
        if self.pressed_pads:
            self.pressed_pads = []
            self._update_control_from_script()

    def _set_button_control_properties(self, button):
        identifier, channel = self._note_translation_for_button(button)
        button.identifier = identifier
        button.channel = channel

    def _button_should_be_enabled(self, button):
        identifier, _ = self._note_translation_for_button(button)
        return (identifier is None) or ((isinstance(identifier, int)) and (identifier < 128))

    def _note_translation_for_button(self, button):
        return (
         button.identifier, button.channel)

    def update(self):
        super().update()
        if self.is_enabled():
            self._set_control_pads_from_script(False)