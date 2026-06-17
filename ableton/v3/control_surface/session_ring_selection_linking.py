# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\session_ring_selection_linking.py
# Compiled at: 2023-04-03 14:43:04
# Size of source mod 2**32: 3409 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ..base import EventObject, depends, index_if, listens
from ..live import scene_index

class SessionRingSelectionLinking(EventObject):

    @depends(song=None, session_ring=None)
    def __init__(self, song=None, session_ring=None, selection_changed_notifier=None, link_to_track_selection=True, link_to_scene_selection=False, *a, **k):
        (super().__init__)(*a, **k)
        self.song = song
        self._session_ring = session_ring
        if link_to_track_selection:
            self._SessionRingSelectionLinking__on_track_selection_scrolled.subject = selection_changed_notifier
        if link_to_scene_selection:
            self._SessionRingSelectionLinking__on_scene_selection_scrolled.subject = selection_changed_notifier

    @listens('track_selection_scrolled')
    def __on_track_selection_scrolled(self):
        if self.song.view.selected_track not in self._session_ring.tracks_to_use():
            return
        track_index = index_if(lambda t: t == self.song.view.selected_track
, self._session_ring.tracks_to_use())
        self._link_session_ring_with_minimal_travel('track', track_index)

    @listens('scene_selection_scrolled')
    def __on_scene_selection_scrolled(self):
        self._link_session_ring_with_minimal_travel('scene', scene_index())

    def _link_session_ring_with_minimal_travel(self, axis_name, current_index):
        ring_axis_offset = getattr(self._session_ring, '{}_offset'.format(axis_name))
        ring_axis_size = getattr(self._session_ring, 'num_{}s'.format(axis_name))
        ending_ring_index = ring_axis_offset + ring_axis_size - 1
        offset_start = current_index - ring_axis_offset
        offset_end = current_index - ending_ring_index
        adjustment = min(0, offset_start) + max(0, offset_end)
        new_offset = ring_axis_offset + adjustment
        if new_offset != ring_axis_offset:
            track_offset = new_offset
            scene_offset = self._session_ring.scene_offset
            if axis_name == 'scene':
                track_offset = self._session_ring.track_offset
                scene_offset = new_offset
            self._session_ring.set_offsets(track_offset, scene_offset)