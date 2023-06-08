from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from future.utils import string_types
from past.utils import old_div
import _Framework.PhysicalDisplayElement as PhysicalDisplayElement
from .NumericalDisplaySegment import NumericalDisplaySegment

class NumericalDisplayElement(PhysicalDisplayElement):
    _ascii_translations = {
      '0': 48,
      '1': 49,
      '2': 50,
      '3': 51,
      '4': 52,
      '5': 53,
      '6': 54,
      '7': 55,
      '8': 56,
      '9': 57}

    def __init__(self, width_in_chars, num_segments):
        PhysicalDisplayElement.__init__(self, width_in_chars, num_segments)
        self._logical_segments = []
        self._translation_table = NumericalDisplayElement._ascii_translations
        width_without_delimiters = self._width - num_segments + 1
        width_per_segment = int(old_div(width_without_delimiters, num_segments))
        for index in range(num_segments):
            new_segment = NumericalDisplaySegment(width_per_segment, self.update)
            self._logical_segments.append(new_segment)

    def display_message(self, message):
        if not self._block_messages:
            message = NumericalDisplaySegment.adjust_string(message, self._width)
            self.send_midi(self._message_header + tuple([self._translate_char(c) for c in message]) + self._message_tail)

    def _translate_char(self, char_to_translate):
        if char_to_translate in list(self._translation_table.keys()):
            result = self._translation_table[char_to_translate]
        else:
            result = self._translation_table['0']
        return result