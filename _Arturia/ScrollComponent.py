<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import EncoderControl
from _Framework.ScrollComponent import ScrollComponent as ScrollComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Arturia/ScrollComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 821 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Control import EncoderControl
import _Framework.ScrollComponent as ScrollComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

class ScrollComponent(ScrollComponentBase):
    scroll_encoder = EncoderControl()

    def set_scroll_encoder(self, encoder):
        self.scroll_encoder.set_control_element(encoder)
        self.update()

    @scroll_encoder.value
    def scroll_encoder(self, value, encoder):
        scroll_step = None
        if value > 0 and self.can_scroll_down():
            scroll_step = self._do_scroll_down
<<<<<<< HEAD
        else:
            if value < 0:
                if self.can_scroll_up():
                    scroll_step = self._do_scroll_up
=======
        elif value < 0:
            if self.can_scroll_up():
                scroll_step = self._do_scroll_up
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        if scroll_step is not None:
            scroll_step()