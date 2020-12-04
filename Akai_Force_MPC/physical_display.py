#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/physical_display.py
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain, starmap
from ableton.v2.base import clamp, group
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

def message_length(message):
    length = len(message)
    return (clamp(length // 128, 0, 127), length % 128)


class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        message_string = display.display_string.strip()
        return chain(message_length(message_string), self._translate_string(message_string))
