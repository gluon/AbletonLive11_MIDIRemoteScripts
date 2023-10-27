# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\session_navigation.py
# Compiled at: 2022-11-29 09:57:03
# Size of source mod 2**32: 6220 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import listens
from ..component import Component
from .scroll import Scrollable, ScrollComponent

class SessionRingScroller(Scrollable):

    def __init__(self, session_ring=None, *a, **k):
        (super(SessionRingScroller, self).__init__)(*a, **k)
        self._session_ring = session_ring

    do_scroll_up = NotImplemented
    do_scroll_down = NotImplemented

    def scroll_up(self):
        if self.can_scroll_up():
            self.do_scroll_up()

    def scroll_down(self):
        if self.can_scroll_down():
            self.do_scroll_down()


class SessionRingTrackScroller(SessionRingScroller):

    def can_scroll_up(self):
        return self._session_ring.track_offset > 0

    def can_scroll_down(self):
        return self._session_ring.track_offset + 1 < len(self._session_ring.tracks_to_use())

    def do_scroll_up(self):
        self._session_ring.move(-1, 0)

    def do_scroll_down(self):
        self._session_ring.move(1, 0)


class SessionRingSceneScroller(SessionRingScroller):

    def can_scroll_up(self):
        return self._session_ring.scene_offset > 0

    def can_scroll_down(self):
        return self._session_ring.scene_offset + 1 < len(self._session_ring.scenes())

    def do_scroll_up(self):
        self._session_ring.move(0, -1)

    def do_scroll_down(self):
        self._session_ring.move(0, 1)


class SessionRingTrackPager(SessionRingScroller):

    def __init__(self, *a, **k):
        (super(SessionRingTrackPager, self).__init__)(*a, **k)
        self.page_size = self._session_ring.num_tracks

    def can_scroll_up(self):
        return self._session_ring.track_offset > 0

    def can_scroll_down(self):
        return self._session_ring.track_offset < len(self._session_ring.tracks_to_use()) - self.page_size

    def do_scroll_up(self):
        self._session_ring.set_offsets(max(0, self._session_ring.track_offset - self.page_size), self._session_ring.scene_offset)

    def do_scroll_down(self):
        self._session_ring.set_offsets(self._session_ring.track_offset + self.page_size, self._session_ring.scene_offset)


class SessionRingScenePager(SessionRingScroller):

    def __init__(self, *a, **k):
        (super(SessionRingScenePager, self).__init__)(*a, **k)
        self.page_size = self._session_ring.num_scenes

    def can_scroll_up(self):
        return self._session_ring.scene_offset > 0

    def can_scroll_down(self):
        return self._session_ring.scene_offset < len(self._session_ring.scenes()) - self.page_size

    def do_scroll_up(self):
        self._session_ring.set_offsets(self._session_ring.track_offset, max(0, self._session_ring.scene_offset - self.page_size))

    def do_scroll_down(self):
        self._session_ring.set_offsets(self._session_ring.track_offset, self._session_ring.scene_offset + self.page_size)


class SessionNavigationComponent(Component):
    track_scroller_type = SessionRingTrackScroller
    scene_scroller_type = SessionRingSceneScroller
    track_pager_type = SessionRingTrackPager
    scene_pager_type = SessionRingScenePager

    def __init__(self, session_ring=None, *a, **k):
        (super(SessionNavigationComponent, self).__init__)(*a, **k)
        self._session_ring = session_ring
        self._SessionNavigationComponent__on_offset_changed.subject = self._session_ring
        self._SessionNavigationComponent__on_tracks_changed.subject = self._session_ring
        self._SessionNavigationComponent__on_scene_list_changed.subject = self.song
        self._vertical_banking = ScrollComponent((self.scene_scroller_type(session_ring)),
          parent=self)
        self._horizontal_banking = ScrollComponent((self.track_scroller_type(session_ring)),
          parent=self)
        self._vertical_paginator = ScrollComponent((self.scene_pager_type(session_ring)),
          parent=self)
        self._horizontal_paginator = ScrollComponent((self.track_pager_type(session_ring)),
          parent=self)

    @listens('offset')
    def __on_offset_changed(self, track_offset, _):
        self._update_vertical()
        self._update_horizontal()

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_horizontal()

    @listens('scenes')
    def __on_scene_list_changed(self):
        self._update_vertical()

    def _update_vertical(self):
        if self.is_enabled():
            self._vertical_banking.update()
            self._vertical_paginator.update()

    def _update_horizontal(self):
        if self.is_enabled():
            self._horizontal_banking.update()
            self._horizontal_paginator.update()

    def set_up_button(self, button):
        self._vertical_banking.set_scroll_up_button(button)

    def set_down_button(self, button):
        self._vertical_banking.set_scroll_down_button(button)

    def set_left_button(self, button):
        self._horizontal_banking.set_scroll_up_button(button)
        self._horizontal_banking.update()

    def set_right_button(self, button):
        self._horizontal_banking.set_scroll_down_button(button)

    def set_page_up_button(self, page_up_button):
        self._vertical_paginator.set_scroll_up_button(page_up_button)

    def set_page_down_button(self, page_down_button):
        self._vertical_paginator.set_scroll_down_button(page_down_button)

    def set_page_left_button(self, page_left_button):
        self._horizontal_paginator.set_scroll_up_button(page_left_button)

    def set_page_right_button(self, page_right_button):
        self._horizontal_paginator.set_scroll_down_button(page_right_button)