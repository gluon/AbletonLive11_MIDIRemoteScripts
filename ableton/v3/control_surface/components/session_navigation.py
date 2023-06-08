from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import clamp, depends, listens
from .. import Component
from . import Scrollable, ScrollComponent

class SessionRingScroller(Scrollable):

    def __init__(self, session_ring, respect_borders, scroll_scenes=False, page_size=1, *a, **k):
        (super().__init__)(*a, **k)
        self.session_ring = session_ring
        self.respect_borders = respect_borders
        self.page_size = page_size
        can_scroll = self._can_scroll_scenes if scroll_scenes else self._can_scroll_tracks
        self.can_scroll_up = partial(can_scroll, -1)
        self.can_scroll_down = partial(can_scroll, 1)
        self._do_scroll = self._scroll_scenes if scroll_scenes else self._scroll_tracks

    def scroll_up(self):
        if self.can_scroll_up():
            self._do_scroll(-self.page_size)

    def scroll_down(self):
        if self.can_scroll_down():
            self._do_scroll(self.page_size)

    def _max_track_offset(self):
        if self.respect_borders:
            return len(self.session_ring.tracks_to_use()) - self.session_ring.num_tracks
        return len(self.session_ring.tracks_to_use()) - 1

    def _max_scene_offset(self):
        if self.respect_borders:
            return len(self.session_ring.scenes_to_use()) - self.session_ring.num_scenes
        return len(self.session_ring.scenes_to_use()) - 1

    def _can_scroll_tracks(self, delta):
        offset = self.session_ring.track_offset
        return 0 < offset > delta or offset + delta in range(self._max_track_offset() + 1)

    def _can_scroll_scenes(self, delta):
        offset = self.session_ring.scene_offset
        return 0 < offset > delta or offset + delta in range(self._max_scene_offset() + 1)

    def _scroll_tracks(self, delta):
        new_offset = self.session_ring.track_offset + delta
        self.session_ring.set_offsets(clamp(new_offset, 0, self._max_track_offset()), self.session_ring.scene_offset)

    def _scroll_scenes(self, delta):
        new_offset = self.session_ring.scene_offset + delta
        self.session_ring.set_offsets(self.session_ring.track_offset, clamp(new_offset, 0, self._max_scene_offset()))


class SessionNavigationComponent(Component):

    @depends(session_ring=None)
    def __init__(self, name='Session_Navigation', session_ring=None, respect_borders=False, *a, **k):
        (super().__init__)(a, name=name, **k)

        def scroller_factory(**k):
            component = ScrollComponent(SessionRingScroller(session_ring, respect_borders, **k),
              parent=self,
              scroll_skin_name='Session.Navigation')
            return component

        self._vertical_banking = scroller_factory(scroll_scenes=True)
        self._horizontal_banking = scroller_factory()
        self._vertical_paging = scroller_factory(scroll_scenes=True,
          page_size=(session_ring.num_scenes))
        self._horizontal_paging = scroller_factory(page_size=(session_ring.num_tracks))
        self.register_slot(self.song, self._update_vertical, 'scenes')
        self.register_slot(session_ring, self._update_horizontal, 'tracks')
        self._SessionNavigationComponent__on_offset_changed.subject = session_ring

    def set_up_button(self, button):
        self._vertical_banking.set_scroll_up_button(button)

    def set_down_button(self, button):
        self._vertical_banking.set_scroll_down_button(button)

    def set_left_button(self, button):
        self._horizontal_banking.set_scroll_up_button(button)

    def set_right_button(self, button):
        self._horizontal_banking.set_scroll_down_button(button)

    def set_page_up_button(self, page_up_button):
        self._vertical_paging.set_scroll_up_button(page_up_button)

    def set_page_down_button(self, page_down_button):
        self._vertical_paging.set_scroll_down_button(page_down_button)

    def set_page_left_button(self, page_left_button):
        self._horizontal_paging.set_scroll_up_button(page_left_button)

    def set_page_right_button(self, page_right_button):
        self._horizontal_paging.set_scroll_down_button(page_right_button)

    def set_vertical_encoder(self, control):
        self._vertical_banking.set_scroll_encoder(control)

    def set_horizontal_encoder(self, control):
        self._horizontal_banking.set_scroll_encoder(control)

    def _update_vertical(self):
        if self.is_enabled():
            self._vertical_banking.update()
            self._vertical_paging.update()

    def _update_horizontal(self):
        if self.is_enabled():
            self._horizontal_banking.update()
            self._horizontal_paging.update()

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._update_vertical()
        self._update_horizontal()