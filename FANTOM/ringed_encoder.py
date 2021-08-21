# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/ringed_encoder.py
# Compiled at: 2021-08-05 15:33:19
# Size of source mod 2**32: 562 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import EncoderElement

class RingedEncoderElement(EncoderElement):

    def is_mapped_manually(self):
        return not self._is_mapped and not self._is_being_forwarded

    def release_parameter(self):
        super(RingedEncoderElement, self).release_parameter()
        if not self.is_mapped_manually():
            if not self._parameter_to_map_to:
                self.send_value(0, force=True)