from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listens, listens_group
from .. import Component
from ..controls import ButtonControl, control_matrix

class SessionOverviewComponent(Component):
    matrix = control_matrix(ButtonControl, color=None)

    @depends(session_ring=None)
    def __init__(self, name='Session_Overview', session_ring=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._track_bank_offset = 0
        self._scene_bank_offset = 0
        self._track_bank_size = 0
        self._session_ring = session_ring
        self._SessionOverviewComponent__on_session_offset_changed.subject = self._session_ring
        self.register_slot(self._session_ring, self.update, 'tracks')
        self.register_slot(self.song, self.update, 'scenes')

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        self.update()

    @matrix.pressed
    def matrix(self, button):
        y, x = button.coordinate
        track_offset = x * self._session_ring.num_tracks + self._track_bank_offset
        scene_offset = y * self._session_ring.num_scenes + self._scene_bank_offset
        if track_offset in range(len(self._session_ring.tracks_to_use())):
            if scene_offset in range(len(self.song.scenes)):
                self._session_ring.set_offsets(track_offset, scene_offset)

    @listens('offset')
    def __on_session_offset_changed(self, *_):
        self.update()

    @listens_group('playing_slot_index')
    def __on_playing_slot_index_changed(self, _):
        self._update_matrix()

    def update(self):
        super().update()
        if self.is_enabled() and self.matrix.control_elements:
            self._update_bank_offsets()
            self._update_matrix()
            self._SessionOverviewComponent__on_playing_slot_index_changed.replace_subjects(self._session_ring.tracks_to_use()[self._track_bank_offset:self._track_bank_offset + self._track_bank_size])
        else:
            self._SessionOverviewComponent__on_playing_slot_index_changed.replace_subjects([])

    def _block_is_within_selection(self, x, y, num_tracks, num_scenes):
        return self._session_ring.track_offset - self._track_bank_offset in range(num_tracks * (x - 1) + 1, num_tracks * (x + 1)) and self._session_ring.scene_offset - self._scene_bank_offset in range(num_scenes * (y - 1) + 1, num_scenes * (y + 1))

    def _block_has_playing_clips(self, tracks, num_tracks, num_scenes, track_offset, scene_offset):
        for track in tracks[track_offset:track_offset + num_tracks]:
            if track in self.song.tracks:
                if track.playing_slot_index in range(scene_offset, scene_offset + num_scenes):
                    return True

        return False

    def _update_matrix(self):
        num_tracks = self._session_ring.num_tracks
        num_scenes = self._session_ring.num_scenes
        tracks = self._session_ring.tracks_to_use()
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                track_offset = x * num_tracks + self._track_bank_offset
                scene_offset = y * num_scenes + self._scene_bank_offset
                if track_offset not in range(len(tracks)) or scene_offset not in range(len(self.song.scenes)):
                    self.matrix.get_control(y, x).color = 'Zooming.Empty'
                    continue
                if self._block_is_within_selection(x, y, num_tracks, num_scenes):
                    self.matrix.get_control(y, x).color = 'Zooming.Selected'
                else:
                    if self._block_has_playing_clips(tracks, num_tracks, num_scenes, track_offset, scene_offset):
                        self.matrix.get_control(y, x).color = 'Zooming.Playing'
                    else:
                        self.matrix.get_control(y, x).color = 'Zooming.Stopped'

    def _update_bank_offsets(self):
        scene_bank_size = self.matrix.height * self._session_ring.num_scenes
        self._scene_bank_offset = self._session_ring.scene_offset // scene_bank_size * scene_bank_size
        self._track_bank_size = self.matrix.width * self._session_ring.num_tracks
        self._track_bank_offset = self._session_ring.track_offset // self._track_bank_size * self._track_bank_size