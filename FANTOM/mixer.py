<<<<<<< HEAD
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens_group, liveobj_valid
from ableton.v3.control_surface.components import MixerComponent as MixerComponentBase
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/mixer.py
# Compiled at: 2022-01-27 16:28:16
# Size of source mod 2**32: 2511 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.base import listens_group, liveobj_valid
import ableton.v3.control_surface.components as MixerComponentBase
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from ableton.v3.control_surface.controls import InputControl
from .control import DisplayControl

class MixerComponent(MixerComponentBase):
    track_select_control = InputControl()
    track_info_display = DisplayControl()

    def set_track_select_control(self, control):
        self.track_select_control.set_control_element(control)

    def set_track_info_display(self, control):
        self.track_info_display.set_control_element(control)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value <= len(self._channel_strips):
            strip = self._master_strip
            if value:
                strip = self._channel_strips[value - 1]
            track = strip.track
            if liveobj_valid(track):
                if self.song.view.selected_track != track:
                    self.song.view.selected_track = track

    def _reassign_tracks(self):
        super()._reassign_tracks()
<<<<<<< HEAD
        tracks = self._provider.tracks
=======
        tracks = self._track_assigner.tracks(self._provider)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self._MixerComponent__on_track_name_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_color_index_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_output_options_changed.replace_subjects(tracks)
        self._MixerComponent__on_track_panning_mode_changed.replace_subjects([t.mixer_device for t in tracks if liveobj_valid(t)])
        self._update_track_info_display()

    def _update_track_info_display(self):
        tracks = self._provider.tracks
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