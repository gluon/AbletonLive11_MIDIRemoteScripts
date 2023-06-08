<<<<<<< HEAD
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/iRig_Keys_IO/mixer.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 2521 bytes
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import forward_property, liveobj_valid
import ableton.v2.control_surface.components as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .scroll import ScrollComponent

class MixerComponent(MixerComponentBase):
    track_scroll_encoder = forward_property('_track_scrolling')('scroll_encoder')
    selected_track_arm_button = ButtonControl()

    def __init__(self, *a, **k):
        (super(MixerComponent, self).__init__)(*a, **k)
        self._track_scrolling = ScrollComponent(parent=self)
        self._track_scrolling.can_scroll_up = self._can_select_prev_track
        self._track_scrolling.can_scroll_down = self._can_select_next_track
        self._track_scrolling.scroll_up = self._select_prev_track
        self._track_scrolling.scroll_down = self._select_next_track

    @selected_track_arm_button.pressed
    def selected_track_arm_button(self, _):
        selected_track = self.song.view.selected_track
        if liveobj_valid(selected_track):
            if selected_track.can_be_armed:
                new_value = not selected_track.arm
                for track in self.song.tracks:
                    if track.can_be_armed:
                        if not (track == selected_track or track).is_part_of_selection or selected_track.is_part_of_selection:
                            track.arm = new_value
                        else:
                            if self.song.exclusive_arm:
                                if track.arm:
                                    track.arm = False

    def _can_select_prev_track(self):
        return self.song.view.selected_track != self._provider.tracks_to_use()[0]

    def _can_select_next_track(self):
        return self.song.view.selected_track != self._provider.tracks_to_use()[(-1)]

    def _select_prev_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[(index - 1)]

    def _select_next_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
<<<<<<< HEAD
        self.song.view.selected_track = tracks[index + 1]
=======
        self.song.view.selected_track = tracks[(index + 1)]
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
