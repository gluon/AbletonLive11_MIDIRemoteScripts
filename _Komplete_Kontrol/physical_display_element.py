# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\physical_display_element.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 671 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
from itertools import chain
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        return chain(*map(lambda x: self._translate_string(str(x).strip())
, display._logical_segments))

    def _request_send_message(self):
        self._send_message()