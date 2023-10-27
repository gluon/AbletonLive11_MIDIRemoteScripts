# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\keyboard.py
# Compiled at: 2022-12-08 12:23:09
# Size of source mod 2**32: 1542 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import PlayableComponent, ScrollComponent
from .note_pad import NotePadMixin
MAX_START_NOTE = 108
SHARP_INDICES = (1, 3, 4, 6, 10, 13, 15)

class KeyboardComponent(NotePadMixin, PlayableComponent, ScrollComponent):

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        self._start_note = 60
        (super().__init__)(*a, **k)

    def can_scroll_up(self):
        return self._start_note < MAX_START_NOTE

    def can_scroll_down(self):
        return self._start_note > 0

    def scroll_up(self):
        if self.can_scroll_up():
            self._move_start_note(12)

    def scroll_down(self):
        if self.can_scroll_down():
            self._move_start_note(-12)

    def _move_start_note(self, factor):
        self._start_note += factor
        self._update_note_translations()

    def _update_button_color(self, button):
        button.color = 'Keyboard.{}'.format('Sharp' if button.index in SHARP_INDICES else 'Natural')

    def _note_translation_for_button(self, button):
        row, column = button.coordinate
        inverted_row = self.matrix.height - row - 1
        return (
         inverted_row * self.matrix.width + column + self._start_note,
         self._translation_channel)