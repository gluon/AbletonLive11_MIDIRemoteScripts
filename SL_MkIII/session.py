# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/session.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 1033 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if
import ableton.v2.control_surface.components as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def _update_stop_clips_led(self, index):
        super(SessionComponent, self)._update_stop_clips_led(index)
        self._update_stop_all_clips_button()

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            value_to_send = self._stop_clip_disabled_value
            tracks = self.song.tracks
            if find_if(lambda x: x.playing_slot_index >= 0 and x.fired_slot_index != -2, tracks):
                value_to_send = self._stop_clip_value
            elif find_if(lambda x: x.fired_slot_index == -2, tracks):
                value_to_send = self._stop_clip_triggered_value
            button.set_light(value_to_send)