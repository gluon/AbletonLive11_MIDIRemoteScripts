# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\physical_display.py
# Compiled at: 2022-11-29 09:57:02
# Size of source mod 2**32: 738 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, starmap
from ableton.v2.base import clamp, group
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

def message_length(message):
    length = len(message)
    return (
     clamp(length // 128, 0, 127), length % 128)


class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        message_string = display.display_string.strip()
        return chain(message_length(message_string), self._translate_string(message_string))