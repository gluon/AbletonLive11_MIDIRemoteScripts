# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\mixer.py
# Compiled at: 2022-11-28 08:01:32
# Size of source mod 2**32: 2588 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import forward_property, liveobj_valid
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
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
        return self.song.view.selected_track != self._provider.tracks_to_use()[-1]

    def _select_prev_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[index - 1]

    def _select_next_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[index + 1]