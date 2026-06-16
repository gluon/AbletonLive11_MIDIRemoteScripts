# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\session_ring.py
# Compiled at: 2023-09-14 15:51:08
# Size of source mod 2**32: 9522 bytes
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import const, depends, index_if, listenable_property, listens, nop
from .. import Component
from ..display import Renderable

class SessionRingModel:

    def __init__(self, num_tracks, num_scenes, include_returns, set_session_highlight=nop):
        self.num_tracks = num_tracks
        self.num_scenes = num_scenes
        self.include_returns = include_returns
        self.track_offset = 0
        self.scene_offset = 0
        self.callback = set_session_highlight

    def update_highlight(self):
        self.callback(self.track_offset, self.scene_offset, self.num_tracks, self.num_scenes, self.include_returns)

    def hide_highlight(self):
        self.callback(-1, -1, -1, -1, False)

    def move(self, tracks, scenes):
        self.track_offset += tracks
        self.scene_offset += scenes


class SessionRingComponent(Component, Renderable):

    @depends(set_session_highlight=(const(nop)))
    def __init__(self, name='Session_Ring', num_tracks=0, num_scenes=0, include_returns=False, include_master=False, right_align_non_player_tracks=False, tracks_to_use=None, snap_track_offset=False, set_session_highlight=nop, is_private=False, *a, **k):
        (super().__init__)(a, name=name, is_private=is_private, **k)
        self._session_ring = SessionRingModel(num_tracks,
          num_scenes,
          include_returns,
          set_session_highlight=set_session_highlight)
        if tracks_to_use is not None:
            self._tracks_to_use = tracks_to_use
        else:
            self._tracks_to_use = partial(self._get_tracks_to_use, include_returns, include_master)
        if right_align_non_player_tracks:
            self._controlled_tracks_formatter = self._right_align_non_player_tracks
        else:
            self._controlled_tracks_formatter = self._pad_tracks
        self._cached_track_list = []
        self._update_track_list()
        self._snap_track_offset = snap_track_offset
        self.notify_offset(0, 0)
        if self.is_enabled():
            self._update_highlight()
        self.register_slot(self.song, self._update_track_list, 'tracks')
        self.register_slot(self.song, self._update_track_list, 'visible_tracks')
        self._SessionRingComponent__on_scene_list_changed.subject = self.song

    @property
    def num_tracks(self):
        return self._session_ring.num_tracks

    @property
    def num_scenes(self):
        return self._session_ring.num_scenes

    @property
    def track_offset(self):
        return self._session_ring.track_offset

    @track_offset.setter
    def track_offset(self, offset):
        self.set_offsets(offset, self.scene_offset)

    @property
    def scene_offset(self):
        return self._session_ring.scene_offset

    @scene_offset.setter
    def scene_offset(self, offset):
        self.set_offsets(self.track_offset, offset)

    @listenable_property
    def offset(self):
        return (
         self.track_offset, self.scene_offset)

    def tracks_to_use(self):
        return self._cached_track_list

    def scenes_to_use(self):
        return self.song.scenes

    @listenable_property
    def tracks(self):
        index = self.track_offset
        tracks = self.tracks_to_use()[index:index + self.num_tracks]
        return self._controlled_tracks_formatter(tracks)

    @listenable_property
    def scenes(self):
        index = self.scene_offset
        return self.scenes_to_use()[index:index + self.num_scenes]

    def set_offsets(self, track_offset, scene_offset):
        track_increment = 0
        scene_increment = 0
        if len(self.tracks_to_use()) > track_offset:
            track_increment = track_offset - self.track_offset
        if len(self.song.scenes) > scene_offset:
            scene_increment = scene_offset - self.scene_offset
        self.move(track_increment, scene_increment)

    def move(self, tracks, scenes):
        if self._snap_track_offset:
            tracks = tracks - tracks % self.num_tracks
        self._session_ring.move(tracks, scenes)
        self._update_highlight()
        self.notify_offset(self.track_offset, self.scene_offset)
        self.notify_tracks()
        self.notify_scenes()

    def on_enabled_changed(self):
        self._update_highlight()

    def _update_track_list(self):
        current_track_list = list(self._tracks_to_use())
        if self._cached_track_list != current_track_list:
            self._cached_track_list = current_track_list
            self.notify_tracks()
        new_offset = min(self.track_offset, len(current_track_list) - 1)
        if new_offset != self.track_offset:
            self.track_offset = new_offset

    def _update_highlight(self):
        if self.is_enabled() and self.num_tracks > 0 and self.num_scenes > 0:
            self._session_ring.update_highlight()
        else:
            self._session_ring.hide_highlight()

    def _pad_tracks(self, tracks):
        size = len(tracks)
        if size < self.num_tracks:
            tracks += [None] * (self.num_tracks - size)
        return tracks

    def _right_align_non_player_tracks(self, tracks):
        num_tracks = self.num_tracks
        insertion_index = index_if(lambda t: t not in self.song.tracks
, tracks)
        tracks[insertion_index:insertion_index] = [None] * (num_tracks - len(tracks))
        return tracks

    def _get_tracks_to_use(self, include_returns, include_master):
        tracks = self.song.visible_tracks
        if include_returns:
            tracks += self.song.return_tracks
        if include_master:
            tracks += (self.song.master_track,)
        return tracks

    @listens('scenes')
    def __on_scene_list_changed(self):
        self.notify_scenes()
        new_offset = min(self.scene_offset, len(self.song.scenes) - 1)
        if new_offset != self.scene_offset:
            self.scene_offset = new_offset