# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\ShiftableSelectorComponent.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 8745 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
import _Framework.Layer as Layer
import _Framework.ModeSelectorComponent as ModeSelectorComponent
from .consts import ABLETON_MODE, NOTE_MODE

class ShiftableSelectorComponent(ModeSelectorComponent):

    def __init__(self, select_buttons, master_button, arm_buttons, matrix, session, zooming, mixer, transport, slider_modes, mode_callback, note_matrix, background, *a, **k):
        (super(ShiftableSelectorComponent, self).__init__)(*a, **k)
        self._toggle_pressed = False
        self._note_mode_active = False
        self._invert_assignment = False
        self._select_buttons = select_buttons
        self._master_button = master_button
        self._slider_modes = slider_modes
        self._arm_buttons = arm_buttons
        self._transport = transport
        self._session = session
        self._zooming = zooming
        self._matrix = matrix
        self._mixer = mixer
        self._mode_callback = mode_callback
        self._note_matrix = note_matrix
        self._background = background
        self._master_button.add_value_listener(self._master_value)

    def disconnect(self):
        super(ShiftableSelectorComponent, self).disconnect()
        self._master_button.remove_value_listener(self._master_value)
        self._select_buttons = None
        self._master_button = None
        self._slider_modes = None
        self._arm_buttons = None
        self._transport = None
        self._session = None
        self._zooming = None
        self._matrix = None
        self._mixer = None
        self._mode_callback = None
        self._note_matrix = None
        self._background = None

    def set_mode_toggle(self, button):
        super(ShiftableSelectorComponent, self).set_mode_toggle(button)
        self.set_mode(0)

    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()

    def number_of_modes(self):
        return 2

    def _set_session_navigation_controls(self, left, right, up, down):
        self._session.set_track_bank_buttons(right, left)
        self._session.set_scene_bank_buttons(down, up)
        self._zooming.set_nav_buttons(up, down, left, right)

    def _set_transport_controls(self, play, stop, rec, overdub):
        self._transport.set_play_button(play)
        self._transport.set_stop_button(stop)
        self._transport.set_record_button(rec)
        self._transport.set_overdub_button(overdub)

    def update(self):
        super(ShiftableSelectorComponent, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                for index in range(len(self._select_buttons)):
                    strip = self._mixer.channel_strip(index)
                    strip.set_select_button(None)

                self._mixer.master_strip().set_select_button(None)
                self._set_transport_controls(self._select_buttons[0], self._select_buttons[1], self._select_buttons[2], self._select_buttons[3])
                if not self._note_mode_active:
                    self._set_session_navigation_controls(self._select_buttons[4], self._select_buttons[5], self._select_buttons[6], self._select_buttons[7])
                self._on_note_mode_changed()
            else:
                if self._mode_index == 1:
                    self._set_transport_controls(None, None, None, None)
                    self._set_session_navigation_controls(None, None, None, None)
                    for index in range(len(self._select_buttons)):
                        strip = self._mixer.channel_strip(index)
                        strip.set_select_button(self._select_buttons[index])

                    self._mixer.master_strip().set_select_button(self._master_button)
                else:
                    pass
            if self._mode_index == int(self._invert_assignment):
                self._slider_modes.set_mode_buttons(None)
                for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(self._arm_buttons[index])

            else:
                for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(None)

                self._slider_modes.set_mode_buttons(self._arm_buttons)

    def _toggle_value(self, value):
        self._toggle_pressed = value > 0
        self._recalculate_mode()

    def _recalculate_mode(self):
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())

    def _master_value(self, value):
        if self.is_enabled():
            if self._invert_assignment == self._toggle_pressed:
                if not self._master_button.is_momentary() or value > 0:
                    for button in self._select_buttons:
                        button.turn_off()

                    self._matrix.reset()
                    mode_byte = NOTE_MODE
                    if self._note_mode_active:
                        mode_byte = ABLETON_MODE
                    self._mode_callback(mode_byte)
                    self._note_mode_active = not self._note_mode_active
                    if self._note_mode_active:
                        for button in self._note_matrix:
                            button.clear_send_cache()

                        self._note_matrix.reset()
                    self._set_transport_controls(self._select_buttons[0], self._select_buttons[1], self._select_buttons[2], self._select_buttons[3])
                    self._transport.update()
                    if self._note_mode_active:
                        for button in self._note_matrix:
                            button.clear_send_cache()

                        self._note_matrix.reset()
                    if self._note_mode_active:
                        self._set_session_navigation_controls(None, None, None, None)
                        self._background.layer = Layer(left_button=(self._select_buttons[4]),
                          right_button=(self._select_buttons[5]),
                          up_button=(self._select_buttons[6]),
                          down_button=(self._select_buttons[7]))
                    else:
                        self._background.layer = None
                        self._set_session_navigation_controls(self._select_buttons[4], self._select_buttons[5], self._select_buttons[6], self._select_buttons[7])
                    self._zooming.set_ignore_buttons(self._note_mode_active)
                    self._on_note_mode_changed()

    def _on_note_mode_changed(self):
        if self.is_enabled():
            if self._invert_assignment == self._toggle_pressed:
                if self._note_mode_active:
                    self._master_button.turn_on()
                else:
                    self._master_button.turn_off()