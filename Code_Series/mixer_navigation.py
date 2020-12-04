#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Code_Series/mixer_navigation.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import division
from past.utils import old_div
from ableton.v2.control_surface.components import SessionNavigationComponent, SessionRingScroller

class WrappingSessionRingTrackPager(SessionRingScroller):

    def can_scroll_up(self):
        return True

    def can_scroll_down(self):
        return True

    def do_scroll_up(self):
        width = self._session_ring.num_tracks
        track_offset = self._session_ring.track_offset
        new_track_offset = track_offset - width
        if new_track_offset < 0:
            new_track_offset = old_div(len(self._session_ring.tracks_to_use()) - 1, width) * width
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)

    def do_scroll_down(self):
        new_track_offset = self._session_ring.track_offset + self._session_ring.num_tracks
        if new_track_offset >= len(self._session_ring.tracks_to_use()):
            new_track_offset = 0
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)


class MixerNavigationComponent(SessionNavigationComponent):
    track_pager_type = WrappingSessionRingTrackPager
