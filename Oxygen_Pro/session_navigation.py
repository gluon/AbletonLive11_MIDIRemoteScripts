<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Oxygen_Pro/session_navigation.py
# Compiled at: 2021-11-23 12:54:43
# Size of source mod 2**32: 740 bytes
from __future__ import absolute_import, print_function, unicode_literals
import ableton.v2.control_surface.components as SessionNavigationComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from ableton.v2.control_surface.control import EncoderControl

class SessionNavigationComponent(SessionNavigationComponentBase):
    scene_encoder = EncoderControl()

    @scene_encoder.value
    def scene_encoder(self, value, _):
        if value > 0:
            if self._vertical_banking.can_scroll_up():
                self._vertical_banking.scroll_up()
<<<<<<< HEAD
        else:
            if self._vertical_banking.can_scroll_down():
                self._vertical_banking.scroll_down()
=======
        elif self._vertical_banking.can_scroll_down():
            self._vertical_banking.scroll_down()
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
