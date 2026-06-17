# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\physical_display.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 1816 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ableton.v2.base import first
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase
from .sysex import TEXT_PROPERTY_BYTE

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _translate_string(self, string):
        return list(map(self._translate_char, [c for c in string if c in self._translation_table]))


class ConfigurablePhysicalDisplayElement(PhysicalDisplayElement):

    def __init__(self, v_position=0, *a, **k):
        (super().__init__)(*a, **k)
        self._v_position = v_position

    def _build_display_message(self, display):

        def wrap_segment_message(segment):
            return chain(segment.position_identifier(), (
             TEXT_PROPERTY_BYTE, self._v_position), self._translate_string(str(segment).strip()), (0, ))

        return chain(*map(wrap_segment_message, display._logical_segments))


class SpecialPhysicalDisplayElement(PhysicalDisplayElement):

    def _send_message(self):
        if self._message_to_send is None:
            self._message_to_send = self._build_message(list(map(first, self._central_resource.owners)))
        inner_message = self._message_to_send[len(self._message_header):-len(self._message_tail)]
        if not self._is_whitespace(inner_message):
            self.send_midi(self._message_to_send)

    def _is_whitespace(self, message):
        return all([c == self.ascii_translations[' '] for c in message])