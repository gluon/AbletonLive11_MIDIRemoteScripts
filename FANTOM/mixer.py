# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/mixer.py
# Compiled at: 2021-08-06 01:27:35
# Size of source mod 2**32: 2832 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens_group, liveobj_valid
import ableton.v2.control_surface.components as MixerComponentBase
from ableton.v2.control_surface.components import SimpleTrackAssigner
from ableton.v2.control_surface.control import InputControl
from .control import DisplayControl

class MixerComponent(MixerComponentBase):
    track_select_control = InputControl()
    track_info_display = DisplayControl()

    def __init__(self, *a, **k):
        (super(MixerComponent, self).__init__)(a, auto_name=True, track_assigner=SimpleTrackAssigner(), **k)

    def set_send_controls(self, controls):
        for index, strip in enumerate(self._channel_strips):
            send_controls = [controls.get_button(i, index) for i in range(2)] if controls else [None]
            strip.set_send_controls(send_controls)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value <= len(self._channel_strips):
            strip = self._master_strip
            if value:
                strip = self._channel_strips[(value - 1)]
            track = strip.track
            if liveobj_valid(track):
                if self.song.view.selected_track != track:
                    self.song.view.selected_track = track

    def _reassign_tracks(self):
        super(MixerComponent, self)._reassign_tracks()
        tracks = self._track_assigner.tracks(self._provider)
        self._MixerComponent__on_track_name_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_color_index_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_output_options_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_panning_mode_changed.replace_subjects([t.mixer_device for t in tracks if liveobj_valid(t)])
        self._update_track_info_display()

    def _update_track_info_display(self):
        tracks = self._track_assigner.tracks(self._provider)
        self.track_info_display.data = [t for t in tracks if liveobj_valid(t)]

    @listens_group('name')
    def __on_track_name_changed(self, _):
        self._update_track_info_display()

    @listens_group('color_index')
    def __on_track_color_index_changed(self, _):
        self._update_track_info_display()

    @listens_group('available_output_routing_types')
    def __on_track_output_options_changed(self, _):
        self._update_track_info_display()

    @listens_group('panning_mode')
    def __on_track_panning_mode_changed(self, _):
        self._update_track_info_display()