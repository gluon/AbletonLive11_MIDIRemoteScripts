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