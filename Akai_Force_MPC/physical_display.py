# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/physical_display.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 714 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, starmap
from ableton.v2.base import clamp, group
import ableton.v2.control_surface.elements as PhysicalDisplayElementBase

def message_length(message):
    length = len(message)
    return (
     clamp(length // 128, 0, 127), length % 128)


class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        message_string = display.display_string.strip()
        return chain(message_length(message_string), self._translate_string(message_string))