# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Komplete_Kontrol/selection_linked_session_ring_component.py
# Compiled at: 2022-01-27 16:28:17
# Size of source mod 2**32: 833 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionRingComponent

class SelectionLinkedSessionRingComponent(SessionRingComponent):

    def __init__(self, *a, **k):
        (super(SelectionLinkedSessionRingComponent, self).__init__)(*a, **k)
        self._SelectionLinkedSessionRingComponent__on_selected_track_changed.subject = self.song.view
        self._SelectionLinkedSessionRingComponent__on_selected_track_changed()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        if selected_track not in self.controlled_tracks():
            all_tracks = list(self.tracks_to_use())
            self.track_offset = all_tracks.index(selected_track)