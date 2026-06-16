# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\note_pad.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 610 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.controls import PlayableControl

class NotePadMixin:

    def set_matrix(self, matrix):
        super().set_matrix(matrix)
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.playable_and_listenable)
            button.pressed_color = 'NotePad.Pressed'

    def _on_matrix_pressed(self, _):
        pass

    def _on_matrix_released(self, button):
        self._update_button_color(button)