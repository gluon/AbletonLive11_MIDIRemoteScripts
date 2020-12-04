#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Komplete_Kontrol_S_Mk2/session_ring_navigation_component.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SessionRingTrackPager
from ableton.v2.control_surface.control import SendValueEncoderControl

class SessionRingNavigationComponent(Component):
    navigation_encoder = SendValueEncoderControl()

    def __init__(self, session_ring, *a, **k):
        super(SessionRingNavigationComponent, self).__init__(*a, **k)
        self._track_pager = SessionRingTrackPager(session_ring)
        self.__on_offset_changed.subject = session_ring
        self.__on_tracks_changed.subject = session_ring
        self._update_navigation_encoder()

    @navigation_encoder.value
    def navigation_encoder(self, value, _):
        if value < 0:
            self._track_pager.scroll_up()
        else:
            self._track_pager.scroll_down()

    @listens(u'offset')
    def __on_offset_changed(self, *_):
        self._update_navigation_encoder()

    @listens(u'tracks')
    def __on_tracks_changed(self):
        self._update_navigation_encoder()

    def _update_navigation_encoder(self):
        self.navigation_encoder.value = int(self._track_pager.can_scroll_up()) | int(self._track_pager.can_scroll_down() << 1)
