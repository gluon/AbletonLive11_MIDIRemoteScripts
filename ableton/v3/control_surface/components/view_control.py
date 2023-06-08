from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ...base import EventObject, ObservablePropertyAlias, all_visible_tracks, clamp, depends, scene_index, track_index
from .. import Component
from . import Scrollable, ScrollComponent

class NotifyingViewScroller(Scrollable, EventObject):
    __events__ = ('scrolled', )

    def __init__(self, song, scroll_scenes=False, page_size=1, *a, **k):
        (super().__init__)(*a, **k)
        self.song = song
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

    @staticmethod
    def _can_scroll_tracks(delta):
        tracks = all_visible_tracks()
        return track_index(track_list=tracks) + delta in range(len(tracks))

    def _can_scroll_scenes(self, delta):
        return scene_index() + delta in range(len(self.song.scenes))

    def _scroll_tracks(self, delta):
        tracks = all_visible_tracks()
        new_index = track_index(track_list=tracks) + delta
        self.song.view.selected_track = tracks[clamp(new_index, 0, len(tracks) - 1)]
        self.notify_scrolled()

    def _scroll_scenes(self, delta):
        scenes = list(self.song.scenes)
        new_index = scene_index() + delta
        self.song.view.selected_scene = scenes[clamp(new_index, 0, len(scenes) - 1)]
        self.notify_scrolled()


class ViewControlComponent(Component):
    __events__ = ('track_selection_scrolled', 'scene_selection_scrolled')

    @depends(session_ring=None)
    def __init__(self, name='View_Control', session_ring=None, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._session_ring = session_ring

        def scroller_factory(scroll_scenes=False, **k):
            scroller_type = 'Scene' if scroll_scenes else 'Track'
            scroller = NotifyingViewScroller(self.song, scroll_scenes=scroll_scenes, **k)
            self.register_disconnectable(ObservablePropertyAlias(self,
              property_host=scroller,
              property_name='scrolled',
              alias_name=('{}_selection_scrolled'.format(scroller_type.lower()))))
            component = ScrollComponent(scroller,
              parent=self,
              scroll_skin_name=('ViewControl.{}'.format(scroller_type)))
            return component

        self._scroll_tracks = scroller_factory()
        self._page_tracks = scroller_factory(page_size=(self._session_ring.num_tracks))
        self._scroll_scenes = scroller_factory(scroll_scenes=True)
        self._page_scenes = scroller_factory(scroll_scenes=True,
          page_size=(self._session_ring.num_scenes))
        song = self.song
        view = song.view
        self.register_slot(self._session_ring, self._update_track_scrollers, 'tracks')
        self.register_slot(song, self._update_track_scrollers, 'visible_tracks')
        self.register_slot(song, self._update_track_scrollers, 'return_tracks')
        self.register_slot(view, self._update_track_scrollers, 'selected_track')
        self.register_slot(song, self._update_scene_scrollers, 'scenes')
        self.register_slot(view, self._update_scene_scrollers, 'selected_scene')

    def set_next_track_button(self, button):
        self._scroll_tracks.set_scroll_down_button(button)

    def set_prev_track_button(self, button):
        self._scroll_tracks.set_scroll_up_button(button)

    def set_next_track_page_button(self, button):
        self._page_tracks.set_scroll_down_button(button)

    def set_prev_track_page_button(self, button):
        self._page_tracks.set_scroll_up_button(button)

    def set_track_encoder(self, control):
        self._scroll_tracks.set_scroll_encoder(control)

    def set_next_scene_button(self, button):
        self._scroll_scenes.set_scroll_down_button(button)

    def set_prev_scene_button(self, button):
        self._scroll_scenes.set_scroll_up_button(button)

    def set_next_scene_page_button(self, button):
        self._page_scenes.set_scroll_down_button(button)

    def set_prev_scene_page_button(self, button):
        self._page_scenes.set_scroll_up_button(button)

    def set_scene_encoder(self, control):
        self._scroll_scenes.set_scroll_encoder(control)

    def _update_track_scrollers(self):
        self._scroll_tracks.update()
        self._page_tracks.update()

    def _update_scene_scrollers(self):
        self._scroll_scenes.update()
        self._page_scenes.update()