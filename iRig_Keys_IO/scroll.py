# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/iRig_Keys_IO/scroll.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 710 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import nop
import ableton.v2.control_surface.components as ScrollComponentBase
from ableton.v2.control_surface.control import EncoderControl

class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        scroll_step = nop
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
        elif value < 0:
            if self.can_scroll_up():
                scroll_step = self._do_scroll_up
        scroll_step()