# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/iRig_Keys_IO/session_ring.py
# Compiled at: 2021-06-29 09:33:48
# Size of source mod 2**32: 943 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionRingComponent

class SelectedTrackFollowingSessionRingComponent(SessionRingComponent):

    def __init__(self, *a, **k):
        (super(SelectedTrackFollowingSessionRingComponent, self).__init__)(*a, **k)
        self._SelectedTrackFollowingSessionRingComponent__on_selected_track_changed.subject = self.song.view
        self._SelectedTrackFollowingSessionRingComponent__on_selected_track_changed()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        tracks_to_use = self.tracks_to_use()
        selected_track = self.song.view.selected_track
        if selected_track in tracks_to_use:
            track_index = list(tracks_to_use).index(selected_track)
            new_offset = track_index - track_index % self.num_tracks
            self.track_offset = new_offset