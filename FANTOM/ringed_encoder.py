# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/ringed_encoder.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 536 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.elements import EncoderElement

class RingedEncoderElement(EncoderElement):

    def is_mapped_manually(self):
        return not self._is_mapped and not self._is_being_forwarded

    def release_parameter(self):
        super().release_parameter()
        if not self.is_mapped_manually():
            if not self._parameter_to_map_to:
                self.send_value(0, force=True)