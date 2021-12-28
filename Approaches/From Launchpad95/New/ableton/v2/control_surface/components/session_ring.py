#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/session_ring.py
from __future__ import absolute_import, print_function, unicode_literals
from ...base import const, depends, nop, listens
from ..component import Component

class SessionRingModel(object):

    def __init__(self, num_tracks, num_scenes, set_session_highlight = nop):
        assert num_tracks >= 0
        assert num_scenes >= 0
        assert callable(set_session_highlight)
        self.num_tracks = num_tracks
        self.num_scenes = num_scenes
        self.track_offset = 0
        self.scene_offset = 0
        self.callback = set_session_highlight

    def update_highlight(self, tracks, return_tracks):
        self.callback(self.track_offset, self.scene_offset, self.num_tracks, self.num_scenes, self._should_include_return_tracks(tracks, return_tracks))

    def hide_highlight(self):
        self.callback(-1, -1, -1, -1, False)

    def _should_include_return_tracks(self, tracks, return_tracks):
        return len(return_tracks) > 0 and return_tracks[0] in tracks

    def move(self, tracks, scenes):
        assert self.track_offset + tracks >= 0
        assert self.scene_offset + scenes >= 0
        self.track_offset += tracks
        self.scene_offset += scenes


class SessionRingComponent(Component):
    u"""
    Manages the set of controlled tracks and scenes from Live's session, aka
    the session ring.
    
    NOTE:
    The session highlight's visibility is controlled by this component's
    enabled state.
    """
    __events__ = (u'offset', u'tracks')

    @depends(set_session_highlight=const(nop))
    def __init__(self, num_tracks = 0, num_scenes = 0, set_session_highlight = nop, tracks_to_use = None, always_snap_track_offset = False, *a, **k):
        super(SessionRingComponent, self).__init__(*a, **k)
        self._session_ring = SessionRingModel(num_tracks, num_scenes, set_session_highlight=set_session_highlight)
        if tracks_to_use != None:
            assert callable(tracks_to_use)
            self._tracks_to_use = tracks_to_use
        else:
            self._tracks_to_use = lambda : self.song.visible_tracks
        self._cached_track_list = []
        self._update_track_list()
        self._snap_offsets = always_snap_track_offset
        self.notify_offset(0, 0)
        if self.is_enabled():
            self._update_highlight()
        self.__on_track_list_changed.subject = self.song
        self.__on_visible_tracks_changed.subject = self.song
        self.__on_scene_list_changed.subject = self.song

    def tracks_to_use(self):
        return self._cached_track_list

    def scenes(self):
        return self.song.scenes

    def set_offsets(self, track_offset, scene_offset):
        assert track_offset >= 0
        assert scene_offset >= 0
        track_increment = 0
        scene_increment = 0
        if len(self.tracks_to_use()) > track_offset:
            track_increment = track_offset - self.track_offset
        if len(self.song.scenes) > scene_offset:
            scene_increment = scene_offset - self.scene_offset
        self.move(track_increment, scene_increment)

    def move(self, tracks, scenes):
        if self._snap_offsets:
            tracks, scenes = self._snapped_offsets(tracks, scenes)
        self._session_ring.move(tracks, scenes)
        self._update_highlight()
        self.notify_offset(self._session_ring.track_offset, self._session_ring.scene_offset)
        self.notify_tracks()

    def _snapped_offsets(self, track_offset, scene_offset):
        snapped_track_offset = track_offset - track_offset % self.num_tracks
        return (snapped_track_offset, scene_offset)

    def controlled_tracks(self):
        index = self.track_offset
        return self.tracks_to_use()[index:index + self.num_tracks]

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

    @property
    def num_tracks(self):
        return self._session_ring.num_tracks

    @property
    def num_scenes(self):
        return self._session_ring.num_scenes

    def on_enabled_changed(self):
        self._update_highlight()

    @listens(u'tracks')
    def __on_track_list_changed(self):
        self._update_track_list()

    @listens(u'visible_tracks')
    def __on_visible_tracks_changed(self):
        self._update_track_list()

    def _update_track_list(self):
        current_track_list = self._tracks_to_use()
        new_offset = min(self.track_offset, len(current_track_list) - 1)
        if new_offset != self.track_offset:
            self.track_offset = new_offset
        if self._cached_track_list != current_track_list:
            self._cached_track_list = current_track_list
            self.notify_tracks()

    @listens(u'scenes')
    def __on_scene_list_changed(self):
        new_offset = min(self.scene_offset, len(self.song.scenes) - 1)
        if new_offset != self.scene_offset:
            self.scene_offset = new_offset

    def _update_highlight(self):
        if self.is_enabled() and self.num_tracks > 0 and self.num_scenes > 0:
            self._session_ring.update_highlight(self.tracks_to_use(), self.song.return_tracks)
        else:
            self._session_ring.hide_highlight()
