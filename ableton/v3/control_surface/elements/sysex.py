# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/elements/sysex.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 1071 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.elements as SysexElementBase

class SysexElement(SysexElementBase):

    def __init__(self, use_first_byte_as_value=False, *a, **k):
        (super().__init__)(*a, **k)
        self._use_first_byte_as_value = use_first_byte_as_value

    def receive_value(self, value):
        if self._use_first_byte_as_value:
            value = value[0]
        super().receive_value(value)

    def message_map_mode(self):
        raise AssertionError("SysexElement doesn't support mapping.")