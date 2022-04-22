# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/SessionComponent.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2746 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
import _Framework.SessionComponent as SessionComponentBase
from _Framework.SubjectSlot import subject_slot_group
from _Framework.Util import in_range
from .ComponentUtils import skin_scroll_component

class SessionComponent(SessionComponentBase):

    def __init__(self, *a, **k):
        self._stopped_clip_value = 0
        (super(SessionComponent, self).__init__)(*a, **k)

    def _enable_skinning(self):
        super(SessionComponent, self)._enable_skinning()
        self.set_stopped_clip_value('Session.StoppedClip')
        scroll_components = (
         self._horizontal_banking,
         self._horizontal_paginator,
         self._vertical_banking,
         self._vertical_paginator)
        list(map(skin_scroll_component, scroll_components))

    def set_stopped_clip_value(self, value):
        self._stopped_clip_value = value

    def set_stop_all_clips_button(self, button):
        if button:
            button.reset_state()
        super(SessionComponent, self).set_stop_all_clips_button(button)

    def _update_stop_clips_led(self, index):
        tracks_to_use = self.tracks_to_use()
        track_index = index + self.track_offset()
        if self.is_enabled():
            if self._stop_track_clip_buttons is not None:
                if index < len(self._stop_track_clip_buttons):
                    button = self._stop_track_clip_buttons[index]
                    if button is not None:
                        value_to_send = None
                        if track_index < len(tracks_to_use):
                            if tracks_to_use[track_index].clip_slots:
                                track = tracks_to_use[track_index]
                                if track.fired_slot_index == -2:
                                    value_to_send = self._stop_clip_triggered_value
                                elif track.playing_slot_index >= 0:
                                    value_to_send = self._stop_clip_value
                                else:
                                    value_to_send = self._stopped_clip_value
                        if value_to_send is None:
                            button.turn_off()
                        elif in_range(value_to_send, 0, 128):
                            button.send_value(value_to_send)
                        else:
                            button.set_light(value_to_send)

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            if button.is_pressed():
                button.set_light(self._stop_clip_value)
            else:
                button.set_light(self._stopped_clip_value)