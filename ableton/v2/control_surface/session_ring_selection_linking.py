#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/session_ring_selection_linking.py
from __future__ import absolute_import, print_function, unicode_literals
from ..base.event import EventObject, listens
from ..base.dependency import depends
from ..base.util import index_if

class SessionRingSelectionLinking(EventObject):

    @depends(song=None)
    def __init__(self, session_ring = None, selection_changed_notifier = None, song = None, *a, **k):
        super(SessionRingSelectionLinking, self).__init__(*a, **k)
        assert session_ring is not None
        assert selection_changed_notifier is not None
        assert song is not None
        self._session_ring = session_ring
        self._song = song
        self._on_selection_scrolled.subject = selection_changed_notifier

    @listens(u'selection_scrolled')
    def _on_selection_scrolled(self):
        self._link_session_ring_with_minimal_travel()

    def _link_session_ring_with_minimal_travel(self):
        u"""
        Ensure that the selected track stays within the bounds of
        the session ring while changing the session ring offset as
        little as possible. If the selected track is already within
        the session ring, nothing will happen. If its index is greater
        than the rightmost session ring track's index, the offset is
        changed so the selected track is the new rightmost session
        ring track; and if it's smaller than the current track offset,
        it becomes the new track offset. Visually, the effect is that
        the session ring is "dragged by its edges" by the track selection.
        """
        if self._song.view.selected_track == self._song.master_track:
            return
        track_index = self._current_track_index()
        right_ring_index = self._session_ring.track_offset + self._session_ring.num_tracks - 1
        offset_left = track_index - self._session_ring.track_offset
        offset_right = track_index - right_ring_index
        adjustment = min(0, offset_left) + max(0, offset_right)
        new_track_offset = self._session_ring.track_offset + adjustment
        if new_track_offset != self._session_ring.track_offset:
            self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)

    def _current_track(self):
        return self._song.view.selected_track

    def _current_track_index(self):
        return index_if(lambda t: t == self._current_track(), self._session_ring.tracks_to_use())
