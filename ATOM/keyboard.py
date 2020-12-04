#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/keyboard.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import PlayableComponent, ScrollComponent
from .note_pad import NotePadMixin
MAX_START_NOTE = 108
SHARP_INDICES = (1, 3, 4, 6, 10, 13, 15)

class KeyboardComponent(NotePadMixin, PlayableComponent, ScrollComponent):

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        self._start_note = 60
        super(KeyboardComponent, self).__init__(*a, **k)

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
        self._release_all_pads()

    def _update_button_color(self, button):
        button.color = u'Keyboard.{}'.format(u'Sharp' if button.index in SHARP_INDICES else u'Natural')

    def _note_translation_for_button(self, button):
        row, column = button.coordinate
        inverted_row = self.matrix.height - row - 1
        return (inverted_row * self.matrix.width + column + self._start_note, self._translation_channel)

    def _release_all_pads(self):
        for pad in self.matrix:
            if pad.is_pressed:
                pad._release_button()
