<<<<<<< HEAD
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
=======
# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.9 (default, Mar 30 2022, 13:51:17) 
# [Clang 13.1.6 (clang-1316.0.21.2.3)]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/view_control.py
# Compiled at: 2022-01-28 05:06:24
# Size of source mod 2**32: 6114 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ...base import EventObject, ObservablePropertyAlias, add_scroll_encoder, clamp, depends, index_if, skin_scroll_buttons
from .. import Component
from . import BasicSceneScroller, BasicTrackScroller, ScrollComponent, all_tracks

class _ScrollNotifier(EventObject):
    __events__ = ('scrolled', )

    def _do_scroll(self, delta):
        super()._do_scroll(delta)
        self.notify_scrolled()


class NotifyingTrackScroller(_ScrollNotifier, BasicTrackScroller):
    pass


class NotifyingTrackPager(NotifyingTrackScroller):

    @depends(session_ring=None)
    def __init__(self, session_ring=None, *a, **k):
        (super().__init__)(*a, **k)
        self._session_ring = session_ring

    def _do_scroll(self, delta):
        selected_track = self._song.view.selected_track
        tracks = all_tracks(self._song)
        selected_track_index = index_if(lambda t: t == selected_track, tracks)
        len_tracks = len(tracks)
        new_index = selected_track_index + delta * self._session_ring.num_tracks
        self._song.view.selected_track = tracks[clamp(new_index, 0, len_tracks - 1)]
        self.notify_scrolled()


class NotifyingSceneScroller(_ScrollNotifier, BasicSceneScroller):
    pass


class NotifyingScenePager(NotifyingSceneScroller):

    @depends(session_ring=None)
    def __init__(self, session_ring=None, *a, **k):
        (super().__init__)(*a, **k)
        self._session_ring = session_ring

    def _do_scroll(self, delta):
        selected_scene = self._song.view.selected_scene
        scenes = self._song.scenes
        selected_scene_index = index_if(lambda s: s == selected_scene, scenes)
        len_scene = len(scenes)
        new_index = selected_scene_index + delta * self._session_ring.num_scenes
        self._song.view.selected_scene = scenes[clamp(new_index, 0, len_scene - 1)]
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        self.notify_scrolled()


class ViewControlComponent(Component):
    __events__ = ('track_selection_scrolled', 'scene_selection_scrolled')

    @depends(session_ring=None)
<<<<<<< HEAD
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
=======
    def __init__(self, name='View_Control', session_ring=None, track_scroller_type=NotifyingTrackScroller, track_pager_type=NotifyingTrackPager, scene_scroller_type=NotifyingSceneScroller, scene_pager_type=NotifyingScenePager, *a, **k):
        (super().__init__)(a, name=name, **k)
        self._session_ring = session_ring
        self._scroll_tracks = ScrollComponent((self._create_scroller(track_scroller_type, 'track')),
          parent=self)
        self._page_tracks = ScrollComponent((self._create_pager(track_pager_type, 'track')),
          parent=self)
        self._scroll_scenes = ScrollComponent((self._create_scroller(scene_scroller_type, 'scene')),
          parent=self)
        self._page_scenes = ScrollComponent((self._create_pager(scene_pager_type, 'scene')),
          parent=self)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34
        song = self.song
        view = song.view
        self.register_slot(self._session_ring, self._update_track_scrollers, 'tracks')
        self.register_slot(song, self._update_track_scrollers, 'visible_tracks')
        self.register_slot(song, self._update_track_scrollers, 'return_tracks')
        self.register_slot(view, self._update_track_scrollers, 'selected_track')
        self.register_slot(song, self._update_scene_scrollers, 'scenes')
        self.register_slot(view, self._update_scene_scrollers, 'selected_scene')
<<<<<<< HEAD
=======
        add_scroll_encoder(self._scroll_tracks)
        add_scroll_encoder(self._scroll_scenes)
        for comp in (self._scroll_tracks, self._page_tracks):
            skin_scroll_buttons(comp, 'ViewControl.Track', 'ViewControl.TrackPressed')

        for comp in (self._scroll_scenes, self._page_scenes):
            skin_scroll_buttons(comp, 'ViewControl.Scene', 'ViewControl.ScenePressed')
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def set_next_track_button(self, button):
        self._scroll_tracks.set_scroll_down_button(button)

    def set_prev_track_button(self, button):
        self._scroll_tracks.set_scroll_up_button(button)

    def set_next_track_page_button(self, button):
        self._page_tracks.set_scroll_down_button(button)

    def set_prev_track_page_button(self, button):
        self._page_tracks.set_scroll_up_button(button)

    def set_track_encoder(self, control):
<<<<<<< HEAD
        self._scroll_tracks.set_scroll_encoder(control)
=======
        self._scroll_tracks.scroll_encoder.set_control_element(control)
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def set_next_scene_button(self, button):
        self._scroll_scenes.set_scroll_down_button(button)

    def set_prev_scene_button(self, button):
        self._scroll_scenes.set_scroll_up_button(button)

    def set_next_scene_page_button(self, button):
        self._page_scenes.set_scroll_down_button(button)

    def set_prev_scene_page_button(self, button):
        self._page_scenes.set_scroll_up_button(button)

    def set_scene_encoder(self, control):
<<<<<<< HEAD
        self._scroll_scenes.set_scroll_encoder(control)
=======
        self._scroll_scenes.scroll_encoder.set_control_element(control)

    def _create_scroller(self, scroller, scroller_type):
        scroller = scroller()
        self.register_disconnectable(ObservablePropertyAlias(self,
          property_host=scroller,
          property_name='scrolled',
          alias_name=('{}_selection_scrolled'.format(scroller_type))))
        return scroller

    def _create_pager(self, pager, pager_type):
        pager = pager(session_ring=(self._session_ring))
        self.register_disconnectable(ObservablePropertyAlias(self,
          property_host=pager,
          property_name='scrolled',
          alias_name=('{}_selection_scrolled'.format(pager_type))))
        return pager
>>>>>>> d4a7b269eef325b60d6e8b8cc6298fd52c04fa34

    def _update_track_scrollers(self):
        self._scroll_tracks.update()
        self._page_tracks.update()

    def _update_scene_scrollers(self):
        self._scroll_scenes.update()
        self._page_scenes.update()