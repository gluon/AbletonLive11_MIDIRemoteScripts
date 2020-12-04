#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/session_ring_selection_linking.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, index_if, listens, liveobj_changed, liveobj_valid
from ableton.v2.control_surface import SessionRingSelectionLinking as SessionRingSelectionLinkingBase

class SessionRingSelectionLinking(SessionRingSelectionLinkingBase):

    def __init__(self, selection_changed_notifier = None, *a, **k):
        super(SessionRingSelectionLinking, self).__init__(selection_changed_notifier=selection_changed_notifier, *a, **k)
        self._previously_selected_track = None
        self._currently_selected_track = None
        self.__on_selected_track_changed.subject = self._song.view
        self.__on_selected_track_changed()
        self.__on_selection_paged.subject = selection_changed_notifier

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._ensure_track_selection_history_is_synced()

    @listens(u'selection_paged')
    def __on_selection_paged(self):
        self._link_session_ring_by_paging()

    def _link_session_ring_by_paging(self):
        if not self._does_selection_change_cross_boundary():
            return
        current_offset = self._session_ring.track_offset
        all_tracks = self._session_ring.tracks_to_use()
        new_offset = clamp(current_offset + self._selection_delta(), 0, len(self._session_ring.tracks_to_use()))
        self._session_ring.set_offsets(new_offset, self._session_ring.scene_offset)

    def _link_session_ring_with_minimal_travel(self):
        if not self._does_selection_change_cross_boundary():
            return
        super(SessionRingSelectionLinking, self)._link_session_ring_with_minimal_travel()

    def _does_selection_change_cross_boundary(self):

        def is_track_in_session_ring(track):
            controlled_tracks = self._session_ring.controlled_tracks()
            return index_if(lambda t: t == track, controlled_tracks) < len(controlled_tracks)

        self._ensure_track_selection_history_is_synced()
        assert liveobj_valid(self._previously_selected_track)
        assert liveobj_valid(self._currently_selected_track)
        return is_track_in_session_ring(self._previously_selected_track) and not is_track_in_session_ring(self._song.view.selected_track)

    def _ensure_track_selection_history_is_synced(self):
        if liveobj_changed(self._currently_selected_track, self._song.view.selected_track):
            self._previously_selected_track = self._currently_selected_track
            self._currently_selected_track = self._song.view.selected_track

    def _selection_delta(self):
        delta = 0
        if liveobj_valid(self._currently_selected_track) and liveobj_valid(self._previously_selected_track):
            delta = self._track_index(self._currently_selected_track) - self._track_index(self._previously_selected_track)
        return delta

    def _track_index(self, track):
        return index_if(lambda t: t == track, self._session_ring.tracks_to_use())
