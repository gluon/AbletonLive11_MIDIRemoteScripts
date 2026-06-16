# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\playhead_component.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 3508 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import range
from past.utils import old_div
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface import Component

class PlayheadComponent(Component):

    def __init__(self, paginator=None, grid_resolution=None, follower=None, notes=list(range(8)), triplet_notes=list(range(6)), feedback_channels=[], *a, **k):
        (super(PlayheadComponent, self).__init__)(*a, **k)
        self._playhead = None
        self._clip = None
        self._paginator = paginator
        self._grid_resolution = grid_resolution
        self._follower = follower
        self._notes = tuple(notes)
        self._triplet_notes = tuple(triplet_notes)
        self._feedback_channels = feedback_channels
        self._on_page_changed.subject = self._paginator
        self._PlayheadComponent__on_grid_resolution_changed.subject = self._grid_resolution
        self._on_follower_is_following_changed.subject = self._follower

    def set_playhead(self, playhead):
        self._playhead = playhead
        self.update()

    def set_clip(self, clip):
        self._clip = clip
        self._on_playing_status_changed.subject = clip
        self._on_song_is_playing_changed.subject = self.song if clip else None
        self.update()

    @listens('page')
    def _on_page_changed(self):
        self.update()

    @listens('playing_status')
    def _on_playing_status_changed(self):
        self.update()

    @listens('is_playing')
    def _on_song_is_playing_changed(self):
        self.update()

    @listens('index')
    def __on_grid_resolution_changed(self, *a):
        self.update()

    @listens('is_following')
    def _on_follower_is_following_changed(self, value):
        self.update()

    def update(self):
        super(PlayheadComponent, self).update()
        if self._playhead:
            clip = None
            if self.is_enabled():
                if not self.song.is_playing or liveobj_valid(self._clip):
                    if self._clip.is_arrangement_clip or self._clip.is_playing:
                        clip = self._clip
                    self._playhead.clip = clip
                    self._playhead.set_feedback_channels(self._feedback_channels)
                    if clip:
                        is_triplet = self._grid_resolution.clip_grid[1]
                        notes = self._triplet_notes if is_triplet else self._notes
                        self._playhead.notes = list(notes)
                        self._playhead.wrap_around = self._follower.is_following and self._paginator.can_change_page
                        self._playhead.start_time = self._paginator.page_length * self._paginator.page_index
                        self._playhead.step_length = old_div(self._paginator.page_length, len(notes))