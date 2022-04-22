# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_S_Mk2/channel_strip_component.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 3521 bytes
from __future__ import absolute_import, print_function, unicode_literals
from itertools import chain
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.control import SendValueControl
import _Komplete_Kontrol.channel_strip_component as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):
    track_arm_display = SendValueControl()

    def __init__(self, *a, **k):
        (super(ChannelStripComponent, self).__init__)(*a, **k)
        self._meter_display_callback = None

    def set_meter_display_callback(self, callback):
        self._meter_display_callback = callback

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self._on_implicit_arm_changed.subject = self._track if (liveobj_valid(self._track)) and (self._track.can_be_armed) else None

    def select_track(self):
        if liveobj_valid(self._track):
            if self.song.view.selected_track != self._track:
                self.song.view.selected_track = self._track

    def mute_track(self):
        if liveobj_valid(self._track):
            if self._track != self.song.master_track:
                self._track.mute = not self._track.mute

    def solo_track(self):
        if liveobj_valid(self._track):
            if self._track != self.song.master_track:
                solo_exclusive = self.song.exclusive_solo
                new_value = not self._track.solo
                respect_multi_selection = self._track.is_part_of_selection
                for track in chain(self.song.tracks, self.song.return_tracks):
                    self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)

    def update(self):
        super(ChannelStripComponent, self).update()
        self._update_output_listeners()

    def _update_output_listeners(self):
        has_track = liveobj_valid(self._track)
        with_audio = self._track if has_track and (self._track.has_audio_output) else None
        self._on_output_meter_left_changed.subject = with_audio
        self._on_output_meter_right_changed.subject = with_audio
        self._on_has_audio_output_changed.subject = self._track if has_track else None
        if with_audio:
            self._on_output_meter_left_changed()
        elif self._meter_display_callback:
            self._meter_display_callback((0, 0))

    def _on_arm_changed(self):
        self.track_arm_display.value = int(self._track.can_be_armed and (self._track.arm or self._track.implicit_arm)) if liveobj_valid(self._track) else 0

    @listens('implicit_arm')
    def _on_implicit_arm_changed(self):
        self._on_arm_changed()

    @listens('has_audio_output')
    def _on_has_audio_output_changed(self):
        self._update_output_listeners()

    @listens('output_meter_left')
    def _on_output_meter_left_changed(self):
        self._update_meter_display()

    @listens('output_meter_right')
    def _on_output_meter_right_changed(self):
        self._update_meter_display()

    def _update_meter_display(self):
        if self._meter_display_callback:
            self._meter_display_callback((
             int(self._track.output_meter_left * 127),
             int(self._track.output_meter_right * 127)))