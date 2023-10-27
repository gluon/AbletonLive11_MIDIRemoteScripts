# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\session_ring_navigation_component.py
# Compiled at: 2022-11-28 08:01:31
# Size of source mod 2**32: 1437 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SessionRingTrackPager
from ableton.v2.control_surface.control import SendValueEncoderControl

class SessionRingNavigationComponent(Component):
    navigation_encoder = SendValueEncoderControl()

    def __init__(self, session_ring, *a, **k):
        (super(SessionRingNavigationComponent, self).__init__)(*a, **k)
        self._track_pager = SessionRingTrackPager(session_ring)
        self._SessionRingNavigationComponent__on_offset_changed.subject = session_ring
        self._SessionRingNavigationComponent__on_tracks_changed.subject = session_ring
        self._update_navigation_encoder()

    @navigation_encoder.value
    def navigation_encoder(self, value, _):
        if value < 0:
            self._track_pager.scroll_up()
        else:
            self._track_pager.scroll_down()

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._update_navigation_encoder()

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_navigation_encoder()

    def _update_navigation_encoder(self):
        self.navigation_encoder.value = int(self._track_pager.can_scroll_up()) | int(self._track_pager.can_scroll_down() << 1)